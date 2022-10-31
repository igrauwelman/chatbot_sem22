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

import re, cgitb, cgi, MySQLdb
cgitb.enable()


Elizahost = "Elizahost"
Elizauser = "Elizauser"
Elizapasswd = "Elizapasswd"
Elizadb ="Elizadb"
lefffile = '/path/to/e/l/i/elizia/www/montablefff.txt'


class Lefff:
    """ cette classe gère tout ce qui a voir avec le lefff :
    la lecture du fichier,
    la création d'index
    la recherche dans les différents dictionnaires interne
    """
    def connect(self):
    	messageText = "Database Status: "
	try: 
		#self.connection = MySQLdb.connect(host="localhost", user="eliza", passwd="eliza", db="lefff" ) 
		
		self.connection = MySQLdb.connect(host=Elizahost, user=Elizauser, passwd=Elizapasswd, db=Elizadb ) 
		
		#self.connection.charset="latin1"
		self.cursor = self.connection.cursor() 
	except MySQLdb.OperationalError, message:
		messageText += str("Error %d:\n%s" % (message[ 0 ], message[ 1 ] ))
	else:
		messageText += "Houray, I'm connected!"
	return messageText



    def lookupDico(self,forme):
        """ chercher le mot 'forme' dans le dico
        """
        infos=[]
	forme = unicode(forme,"iso-8859-1")
	if self.cursor:
		self.cursor.execute ("SELECT lemma, code FROM verbes WHERE form='" + forme + "'")
		while (1):
			row = self.cursor.fetchone ()
			if row == None:
				break
			infos[0:0]=[row]
        return infos


    def contientVerbe(self,liste):
        for mot in liste :
            if self.lookupDico(mot) != [] :
                return True
        return False

    def changePersonne(self,verbe,anciennePersonne,nouvellePersonne,
                        pluriel=True,indicative=True):
        """ prend un verbe comme entrée,
            et rend la meme forme Ã  la nouvelle personne.
            On préfère le pluriel.
            Si on a le choix entre indicative et subjonctive,
            on prÃ©fÃ¨re l'indicative, sauf si la variable 'indicative' est mise
            Ã  'False'
        """
        codeMode=""
        personne=""
        lemme=""
        infos = self.lookupDico(verbe)

        # s'il ne connait pas le verbe, alors on le laisse tel quel.
        if infos == []:
            return verbe

        # essayons de trouver les bons codes pour la personne recherchÃ©e
        for info in infos:
            if str(anciennePersonne) in info:
                for c in info[1]:
                    if c.isdigit():
                        break
                    codeMode+=c
                personne = info[1][-1]
                lemme = info[0]

        # si je ne trouve pas la bonne personne, je prend les codes
        # de la 1Ã¨re info dans la liste.
        if codeMode=="":
            for c in infos[0][1]:
                    if c.isdigit():
                        break
                    codeMode+=c
            personne = infos[0][1][-1]
            lemme = infos[0][0]

        # cas spÃ©cial de forme identique indicative et subjonctive
        if codeMode == "PS":
            if indicative : codeMode = "P"
            else : codeMode = "S"

        # cas spÃ©cial de passage au pluriel de politesse
        if pluriel: personne = "p"
        else : personne = "s"

	lemme = unicode(lemme,"iso-8859-1")
        marecherche = "SELECT form FROM verbes WHERE lemma='" + lemme + "'"
        marecherche += " AND code LIKE '%"+ codeMode + "%'"
        marecherche += " AND code LIKE '%"+ str(nouvellePersonne) + "%'"
        marecherche += " AND code LIKE '%"+ personne + "%'"
	#print "===<br>"+marecherche.encode('iso-8859-1')+"<br>"
        self.cursor.execute (marecherche)
        while (1):
            row = self.cursor.fetchone ()
	    #print "***"+str(row)+"***<br>"
            if row == None:
                break
            return row[0]
        # rien trouvÃ©, je rends le verbe tel quel
        return verbe
