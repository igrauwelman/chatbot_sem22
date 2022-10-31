#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

####
# Copyright (C) 2006, 2007 Kim Gerdes
# kim AT gerdes.fr
#
# This program is free software; you can redistribute it and/or
 # modify it under the terms of the GNU General Public License
 # as published by the Free Software Foundation; either version 2
 # of the License, or (at your option) any later version.
#
# This script is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE
# See the GNU General Public License (www.gnu.org) for more details.
#
# You can retrieve a copy of the GNU General Public License
# from http://www.gnu.org/.  For a copy via US Mail, write to the
#     Free Software Foundation, Inc.
#     59 Temple Place - Suite 330,
#     Boston, MA  02111-1307
#     USA
####

import time, re
from random import choice
from frenchLinguist import FrenchLinguist
from rogers import Rogers


class Elizia:

    rogers = Rogers()
    linguist = FrenchLinguist()
    listeInterro=["pourquoi","quand","comment"]
    
    fini = False
    dicoDejaDitElizia = {}

    cas = "Retour" # contient le mot clé trouvé   
    patientInput = "???" # devrait être écrasé par le vrai input
    
    def analyse(self, texte, sess):
		""" ici se fait tout le boulot. """
		self.sess = sess
		avantPatient = sess.data.get('memoireinputsPatient')
		self.avantCas = sess.data.get('memoireCas')
		if not self.avantCas: self.avantCas=[]
		if avantPatient : memoireinputsPatient = avantPatient + [texte]
		else :
			memoireinputsPatient = [texte]
			avantPatient = []
		sess.data['memoireinputsPatient'] = memoireinputsPatient

		avantelizia = sess.data.get('dejaDitelizia')
		if avantelizia : self.dicoDejaDitElizia = avantelizia

		self.patientInput = texte.strip()
		if len(self.patientInput)>1 : self.patientInput = self.patientInput[0].lower()+self.patientInput[1:]
		self.patientInput = self.linguist.decontracte(self.patientInput)

		inputPropre = self.linguist.nettoyerTexte(self.patientInput)
		inputSplit = inputPropre.split()

		#voir si le patient a dit qqch
		if len(inputSplit)==0:
			self.cas = "Vide"
			return self.repo()

		# voir si le patient a pê posé une question :
		# donc si ça commence avec un mot interrogatif ou termine sur un point d'interrogation
		if inputSplit[0] in self.listeInterro or self.patientInput[-1]=="?":
			self.cas = "Question"

		elif texte in avantPatient :
			self.cas = "Déjà"
		#voir si le patient est très bref
		elif len(inputSplit)==1:
			self.cas = "Bref"

		# mots clés
		for nom in self.rogers.keywords.keys(): # pour chaque clé
			if self.cleTrouvee(self.rogers.keywords[nom],inputPropre,inputSplit):
				self.cas = nom

		# s'il n'a rien trouvé alors retourne la input
		# (cas self.cas = "Retour")
		return self.repo()


	def cleTrouvee(self,cles,texte,liste):
		"""
		cherche une liste cles dans un texte (string) et dans la liste de mots correspondante
		deux cas : clé est un mot : il doit apparaître entouré de blancs
		ou clé contient des espaces : peu importe, tant qu'il apparaît
		"""
		for c in cles :
			if " " in c and c in texte:
				return True
			elif c in liste :
				return True
		return False


	def repo(self):
		""" fonction importante qui rend la réponse et gêre les mémoires """

		ordered = False
		reponse = ""
		if self.cas in self.dicoDejaDitElizia.keys():
			memoire =  self.dicoDejaDitElizia[self.cas]
		else : memoire = []

		if self.cas == "Insulte":
			ordered = True
			if len(memoire) >= len(self.rogers.answers[self.cas])-2 :
				self.fini = True

		if self.cas == "Fin":
			self.fini = True

		if self.cas == "Retour" or self.cas == "Bref":
			ll = len(self.avantCas)
			for i in range(ll) :
				#print self.avantCas[ll-i-1]
				if self.avantCas[ll-i-1] not in self.rogers.noRecall :
					self.cas = "Reprise"
					casRepris = self.avantCas[ll-i-1]
					if casRepris in self.dicoDejaDitElizia.keys() : memoReprise =  self.dicoDejaDitElizia[casRepris]
					else : memoReprise = []
					reponse = " &nbsp;"+self.choisirReponse(casRepris,memoReprise,False)

					break

		reponse = self.choisirReponse(self.cas,memoire,ordered) + reponse

		if self.cas == "Reprise" : reponse = reponse.replace("xxx",casRepris)

		if self.cas == "Retour":
			reponse = reponse + self.linguist.phraseEnchassee(self.patientInput)

		#memoireReponses=memoire+[reponse] # se souvenir de ce qu'on a dit
		before = self.sess.data.get('memoireReponses')
		if before:
			memoireReponses = before + [reponse]
		else:
			memoireReponses = [reponse]
		self.sess.data['memoireReponses'] = memoireReponses

		beforeCas = self.sess.data.get('memoireCas')
		if before:
			memoireCas = beforeCas + [self.cas]
		else:
			memoireCas = [self.cas]
		self.sess.data['memoireCas'] = memoireCas

		beforeTemps = self.sess.data.get('memoireTemps')
		if beforeTemps:
			memoireTemps = beforeTemps + [repr(time.time())]
		else:
			memoireTemps = [repr(time.time())]
		self.sess.data['memoireTemps'] = memoireTemps


		return self.linguist.beautifier(reponse)


	def choisirReponse(self,casActuel,memoireActuel,ordered):
		# le [:] permet de faire une copie
		#       - pour qu'on ne touche pas à la liste originale
		listeReponseLocale=self.rogers.answers[casActuel][:]


		for rep in memoireActuel:
			if rep in listeReponseLocale: # normalement, ça devrait tjrs être dedans
				listeReponseLocale.remove(rep) # on enlève ce qu'on a déjà dit
			if ordered:
				reponse = listeReponseLocale[0]
			else:
				reponse = choice(listeReponseLocale) # choix par hasard parmi le reste

			memoireCas=memoireActuel+[reponse] # on retient la réponse (sans phrase du patient en cas Retour)

		# vider le mémoire sauf la dernière réponse au cas où on a déjà	utilisé toutes les réponses proposées

		if len(memoireCas) >= len(self.rogers.answers[casActuel]):
				while len(memoireCas)>1:
					memoireCas.pop(0)

		self.dicoDejaDitElizia[casActuel]=memoireCas
		self.sess.data['dejaDitelizia'] = self.dicoDejaDitElizia

		return reponse

