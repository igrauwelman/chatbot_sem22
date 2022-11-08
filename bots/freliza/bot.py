from .rogers import Rogers
from .frenchLinguist import FrenchLinguist
from chat.models import FrenchLex
import time
import random

class Bot:

    name = 'French Eliza'
    avatar = 'avatar/perroquet.png'

    def __init__(self):
        self.rogers = Rogers()
        self.linguist = FrenchLinguist()
        FrenchLex.read_lex()
        self.listeInterro =["pourquoi" ,"quand" ,"comment"]

        self.fini = False
        self.dicoDejaDitElizia = {}

        self.cas = "Retour" # contient le mot clé trouvé
        self.patientInput = "???" # devrait être écrasé par le vrai input

        self.session = None

    def welcome(self):
        return "Mettez-vous à l'aise et parlez-moi ouvertement de vos problèmes!"

    def cleTrouvee(self, cles, texte, liste):
        """
        cherche une liste cles dans un texte (string) et dans la liste de mots correspondante
        deux cas : clé est un mot : il doit apparaître entouré de blancs
        ou clé contient des espaces : peu importe, tant qu'il apparaît
        """
        for c in cles :
            if " " in c and c in texte:
                return True
            elif c in liste:
                return True
        return False

    def chat(self, last_user_message, session):
        """ ici se fait tout le boulot. """

        self.session = session
        avantPatient = self.session.data.get('memoireinputsPatient', None)
        self.avantCas = self.session.data.get('memoireCas', [])
        if avantPatient:
            memoireinputsPatient = avantPatient + [last_user_message]
        else:
            memoireinputsPatient = [last_user_message]
            avantPatient = []
        self.session.data['memoireinputsPatient'] = memoireinputsPatient

        avantelizia = self.session.data.get('dejaDitelizia', None)
        if avantelizia:
            self.dicoDejaDitElizia = avantelizia

        self.patientInput = last_user_message.strip()
        if len(self.patientInput ) >1:
            self.patientInput = self.patientInput[0].lower( ) +self.patientInput[1:]
        self.patientInput = self.linguist.decontracte(self.patientInput)

        inputPropre = self.linguist.nettoyerTexte(self.patientInput)
        inputSplit = inputPropre.split()

        # voir si le patient a dit qqch
        if len(inputSplit ) == 0:
            self.cas = "Vide"
            return self.repo()

        # voir si le patient a pê posé une question :
        # donc si ça commence avec un mot interrogatif ou termine sur un point d'interrogation
        if inputSplit[0] in self.listeInterro or self.patientInput[-1 ] == "?":
            self.cas = "Question"
        elif last_user_message in avantPatient :
            self.cas = "Déjà"
        # voir si le patient est très bref
        elif len(inputSplit) == 1:
            self.cas = "Bref"

        # mots clés
        for nom in self.rogers.keywords.keys(): # pour chaque clé
            if self.cleTrouvee(self.rogers.keywords[nom] ,inputPropre ,inputSplit):
                self.cas = nom

        # s'il n'a rien trouvé alors retourne la input
        # (cas self.cas = "Retour")
        return self.repo()


    def repo(self):
        """ fonction importante qui rend la réponse et gêre les mémoires """

        ordered = False
        reponse = ""
        if self.cas in self.dicoDejaDitElizia.keys():
            memoire = self.dicoDejaDitElizia[self.cas]
        else:
            memoire = []

        if self.cas == "Insulte":
            ordered = True
            if len(memoire) >= len(self.rogers.answers[self.cas] ) -2 :
                self.fini = True

        if self.cas == "Fin":
            self.fini = True

        if self.cas == "Retour" or self.cas == "Bref":
            ll = len(self.avantCas)
            for i in range(ll) :
                # print self.avantCas[ll-i-1]
                if self.avantCas[ll-i-1] not in self.rogers.noRecall :
                    self.cas = "Reprise"
                    casRepris = self.avantCas[ll-i-1]
                    if casRepris in self.dicoDejaDitElizia.keys():
                        memoReprise = self.dicoDejaDitElizia[casRepris]
                    else:
                        memoReprise = []
                    reponse = " &nbsp; " +self.choisirReponse(casRepris ,memoReprise ,False)
                    break

        reponse = self.choisirReponse(self.cas ,memoire ,ordered) + reponse

        if self.cas == "Reprise":
            reponse = reponse.replace("xxx" ,casRepris)

        if self.cas == "Retour":
            reponse = reponse + self.linguist.phraseEnchassee(self.patientInput)

        # memoireReponses=memoire+[reponse] # se souvenir de ce qu'on a dit
        before = self.session.data.get('memoireReponses', None)
        if before:
            memoireReponses = before + [reponse]
        else:
            memoireReponses = [reponse]
        self.session.data['memoireReponses'] = memoireReponses

        beforeCas = self.session.data.get('memoireCas', None)
        if before:
            memoireCas = beforeCas + [self.cas]
        else:
            memoireCas = [self.cas]
        self.session.data['memoireCas'] = memoireCas

        beforeTemps = self.session.data.get('memoireTemps', None)
        if beforeTemps:
            memoireTemps = beforeTemps + [repr(time.time())]
        else:
            memoireTemps = [repr(time.time())]
        self.session.data['memoireTemps'] = memoireTemps

        return self.linguist.beautifier(reponse)


    def choisirReponse(self, casActuel, memoireActuel, ordered):
        # le [:] permet de faire une copie
        #       - pour qu'on ne touche pas à la liste originale
        listeReponseLocale =self.rogers.answers[casActuel][:]

        for rep in memoireActuel:
            if rep in listeReponseLocale: # normalement, ça devrait tjrs être dedans
                listeReponseLocale.remove(rep) # on enlève ce qu'on a déjà dit
        if ordered:
            reponse = listeReponseLocale[0]
        else:
            reponse = random.choice(listeReponseLocale) # choix par hasard parmi le reste

        memoireCas = memoireActuel +[reponse] # on retient la réponse (sans phrase du patient en cas Retour)

        # vider le mémoire sauf la dernière réponse au cas où on a déjà	utilisé toutes les réponses proposées

        if len(memoireCas) >= len(self.rogers.answers[casActuel]):
            while len(memoireCas) >1:
                memoireCas.pop(0)

        self.dicoDejaDitElizia[casActuel] =memoireCas
        self.session.data['dejaDitelizia'] = self.dicoDejaDitElizia

        return reponse
