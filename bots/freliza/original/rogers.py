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

class Rogers:
	
	noRecall = ["Question","Retour","D�j�","Vide","Bref","Fin","Insulte","Parceque","N�gation","Oui","Faim","Reprise"]
	
	answers={}
	keywords={}
		
		
	answers["Question"] =[	"C'est moi qui pose les questions ici.",
				"Si je vous donnais des r�ponses, �a serait trop facile.",
				"Si j'avais des r�ponses � de telles questions, croyez-vous que je serais ici ?",
				"Mon role n'est pas de r�pondre � vos questions !",
				"L'approche rog�rienne � la th�rapie a des avantages mais aussi l'inconv�nient que je ne peux pas r�pondre � vos questions."]
	
	answers["Retour"]=[	"Cela vous fait quoi de me dire",
				"�a vous fait quoi",
				"Pourquoi dites-vous",
				"Pourriez-vous expliciter le fait",
				"Que se passe-t-il en vous quand vous prononcez � haute voix",
				"Comment peut-on finir par dire",
				"Je n'arrive pas � comprendre"]
				
	answers["D�j�"] = [	"Vous avez d�j� dit �a. Avan�ons.",
				"Oui, parfois il est utile de se r�p�ter. Mais j'ai bien compris ce point.",
				"Comme l'a bien dit Boris Vian :  'La mort n'est pas dr�le parce qu'elle ne supporte pas la r�p�tition.'",
				"Anatole France dirait :  'A l'endroit du public, r�p�ter c'est prouver.'",
				"Attendez-vous une autre r�ponse de ma part ?",
				"Quand on n'a pas de m�moire, on se r�p�te : quand on en a, on r�p�te les autres.","Encore !"]
		
	answers["Vide"] = [	"N'h�sitez pas, je suis votre docteur !",
				"Mais si vous ne dites rien, je ne peux vous aider.",
				"Vous �tes l�, parce que vous souffrez. Parlez-moi de vos souffrances !",
				"Le silence nous am�ne vers le rien."]
	
	answers["Bref"] = [	"Vous n'�tes pas prodigue de paroles !",
				"Il faudrait en dire un peu plus.",
				"Vous �tes un peu trop taciturne.",
				"Vous ne dites pas un mot de trop."]
		
	answers["Reprise"] = [	"Ramenons nos moutons et parlons un peu plus de xxx.",
				"Peut-�tre vous serait-il plus utile de reprendre notre discussion au sujet de xxx.",
				"Pourquoi ne continuez-vous pas de parler de xxx ?",
				"Cela nous am�ne trop loin. Une discussion au sujet de xxx vous aidera plus.",
				"Avons vous parliez de xxx, n'est-ce pas ?"]	
		
############################## fin cas sp�ciaux


	keywords["Fin"] = [	"au revoir","bye bye","�a suffit"]
	answers["Fin"] = [	"Au revoir.<br>Ma secr�taire vous enverra la facture sous peu.",
				"S'il vous reste de l'argent sur votre carte de cr�dit, alors on se reverra demain.",
				"Bonne gu�rison !<br>Et n'oubliez pas de r�gler sous sept jours.",
				"Si vous n'avez pas d�pass� votre autorisation de d�couvert, on se reverra demain."]
		
		
	keywords["Insulte"] = [	"chier","chie","chi�","chiez","chiant","merde","sous-merde",
				"emmerde","emmerdeur","emmerdeuse","emmerdez","emmerder",
				"conasse","connasse","conne","p�tasse","poufiasse","grogniasse","grognasse","abrutie","fiotte",
				"connard","abruti","salopard","tasspe","sale porc","batard",
				"pute","putain", "salope","salop","salaud","pestiff�r�",
				"con","couille", "bite", "cul", 
				"p�d�","pd","tafiole","tapette","p�dale",
				"bordel","raclure","foutre","nique","niquer"]
	answers["Insulte"] = [	"Ne soyez pas grossier, s'il vous plait!" ,
				"Recentrez-vous sur votre objectif !",
				"Veillez � soigner votre langage !",
				"Vous semblez ne pas avoir compris le but de cette th�rapie !",
				"Insulter ceux qui veulent vous aider ne vous m�nera � rien !",
				"Non mais vous vous croyez o� ? C'est mon dernier avertissement!",
				"Je ne continue pas dans ces conditions. Au revoir",
				"Vous insisitez !!!!"]
			
	keywords["Parceque"] = ["parce que","puisque","donc", "alors"]
	answers["Parceque"] = [ "Le but de cette th�rapie est de trouver les faits, pas de raisonner.",
				"Cela ne me semble pas �tre une implication n�cessaire.",
				"Arr�tez de vous trouver des excuses.",
				"Parlez-moi plus de votre logique.","Pourquoi cette contradiction ?"]
			
	keywords["N�gation"] =    ["rien","jamais","aucun","aucune","non","pas du tout","pire"]
	answers["N�gation"] =  [	"Vous n'�tes pas un peu n�gatif ?",
					"Think positive !",
					"Nier ne sert � rien."]
						
	keywords["votre famille"] =   [	"m�re","p�re","papa","maman","Papa","Maman","fils",
					"fille","fr�re","soeur","famille","�ducation",
					"bru", "gendre", "oncle", "tante", "inceste", "belle-famille", "enfant", "grands-parents"]
	answers["votre famille"] =   [   	"Parlez un peu plus de votre famille, s'il vous pla�t",
					"Que signifie la famille pour vous ?",
					"�tes-vous sure d'avoir r�solu votre Oedipe ?",
					"La famille est un facteur important dans le vie de tous.",
					"Que pensez vous de vos rapports familiaux ?", 
					"Que pouvez vous dire de votre enfance ?", 
					"Pourrez vous un jour pardonner ?", 
					"D�finissez vos relations avec vos parents.", 
					"On ne choisit pas sa famille mais on vit avec, ainsi que ses d�fauts et ses qualit�s."]

						
	keywords["vos amis"] =   [	"ami","amis","copain","copains","copine","copines","pote"]
	answers["vos amis"] =  [   	"Il peut �tre important de s'�taler un peu plus sur vos amis.",
				"L'amiti� signifie quoi pour vous ?",
				"Oui, personne ne peut vivre sans amis."]
						
	keywords["vos probl�mes"] =    [	"malaise","malheureux","probl�me","probl�mes","malheur","malheurs", "malheur","mal","noir",
					"malheureuse","pas heureux","m�lancolie","m�lancolique","d�prime","d�prim�",
					"d�prim�e","triste","tristesse",
					"d�pression","d�pressif","d�pressive","las","lasse","lass�","lass�e", "fatigue","fatigu�","fatigu�e",
					"difficile","divorce","enterrement","enfer","d�mon","s�paration",
					"difficult�s","difficult�","catastrophe","mourrir","mort","suicider","suicide", "morbide"]
	answers["vos probl�mes"] = [   	"Reprennez-vous, vous �tes trop n�gatif.", 
					"Courage, la th�rapie est justement l� pour aider � reprendre confiance en vous.", 
					"Vous semblez perdre pied.",
					"Est-il poissible que vous avez besoin de plus de confiance ?",
					"Parler vous redonnera confiance en vous",
					"Le bonheur est dans le pr�.", 
					"Croquez la vie � pleine dents!", 
					"Ne soyez pas triste, la vie est belle.", 
					"Si rien ne va allez voir un psy!", 
					"Rien ne sert de sauter il faut r�agir � temps!", 
					"Pas de panique ! Eliza s'occupe de tout!", 
					"Rien ne vaut le chocolat pour remonter le moral!", 
					"Rire prolonge la vie pensez-y...", 
					"La vie est courte profitez-en!", 
					"Respirez !! �a calme...", 
					"Comment vous sentez-vous?", 
					"A malheur bonheur est bon.", 
					"Prenez la vie par le bon bout et �a ira mieux!",]
	
						
	keywords["votre avenir"] =    [	"projet","r�ussir","r�ussite","projets","avenir","futur","concr�tiser",
					"concr�tis�","espoir","demain","espoirs","r�alisation","r�alisations", "esp�re","souhait","souhaite"]
	answers["votre avenir"] =        [   	"C'est encourageant, vous construisez des projets!",
						"Comment vous projetez-vous dans l'avenir?", 
						"Comment construisez-vous votre futur?",
						"Comment vous imaginez-vous dans quelques ann�es?",
						"Avez-vous foi en votre avenir?", 
						"�tes-vous confiant quant � votre avenir?"]      
						
	keywords["vos craintes"] =   [ 	"peur", "peurs","crainte","craintes", "crains","h�site", "h�sitations",
					"h�sitation","incertain","incertaine","dubitatif","dubitative"]
	answers["vos craintes"] =   [   "Mais d'o� vient votre incertitude?",
					"Il faut que vous ayez plus confiance en vous",
					"Soyez rassur�, je suis l� pour vous �couter.",
					"La confiance en soi vous m�nera vers la gu�rison.",
					"Commencez par vous faire confiance."]
									
	keywords["vos envies"] =   [ 	"envie","d�sir","envies","souhaite","d�sirs","souhait"]
	answers["vos envies"] =        ["Mais de quoi avez-vous r�ellement envie?",
					"En avez-vous r�ellement envie?",
					"�tes-vous sure que vos souhaits correspondent � vos besoins ?"] 
	keywords["vos peurs"] =   [ 	"peur","peurs","cauchemar","crainte","craintes","effray�","pers�cution","psychose",
					"n�vrose","panique","vertige",
					"trouillard","anxi�t�","phobie","parano�a"]
	answers["vos peurs"] =        [ "�tes-vous sujet � des peurs li�es au vide ou � l'enfermement?",
					"De quoi avez-vous vraiment peur ?",
					"Qu'est-ce qui vous effraie ?"]
						
	keywords["vos r�ves"] =   [ 	"r�ves","r�ve","d�sir","image',images","d�sirs","fantasme","fantasmes"]
	answers["vos r�ves"] =        [ "S'agit-il plutot de d�sir ou d'interdit li� � votre journ�e pr�c�dente ?",
					"A votre avis, en quoi ce r�ve est-il r�v�lateur de votre situation actuelle ?",
					"Comment pouvez-vous m'expliquer le sens de ces images ?",
					"Quelles interpr�tations pouvez-vous en faire ?"]
						
	keywords["la religion"] =    [ 	"religion","dieu","d�esse","crois","ange","pri�re","prie","moine",
					"perdu","�glise","pr�tre","croyances","croyance","�sot�rique","�sot�risme","gourou",
					"astrologie","�toile"]
	answers["la religion"] =        [   	"Que pensez-vous de la phrase 'La religion est l'opium du peuple' ?",
						"Croire est ne pas savoir.",
						"Sans votre religion, vous sentiriez-vous plus libre ?",
						"Pourquoi parlez-vous de vos croyances ?"] 
						
	keywords["cin�ma"] =    [ 	"cin�ma","film","films","acteur","actrice","acteurs","actrices","cannes"]
	answers["cin�ma"] = [   	"Vous allez souvent au cin�ma ?",
					"Est-ce que vous aimez les films de gladiateurs ?",
					"Est-ce que vous aimez les films d'aventure ?",
					"Que pensez-vous des films de cul ?",
					"Que pensez-vous des films d'amour ?" ,
					"Mais je ne comprends pas, pourquoi parlez-vous de �a ?",
					"Quel genre de film repr�sente le mieux vos difficult�s actuelles ?"]
						
	keywords["l'universit�"] =   [ 	"�tude","�tudes","universit�","fac","facult�","profession",
					"professionnel","professionnelle","examen",
					"examens","partiel","partiels","classe","cours","camarade","camarades"]
	answers["l'universit�"] =     [ "Mais quel m�tier voudriez-vous faire ?",
					"Vos buts professionnels sont-ils r�alistes ?",
					"Construisez-vous un projet � travers votre formation ?",
					"Vous sentez-vous bien dans vos �tudes ?",
					"Avez-vous de bonnes m�thodes de travail ?",
					"Essayez-vous de vous int�grer?",
					"""S�n�que a dit "Etudie, non pour savoir plus, mais pour savoir mieux." Qu'en pensez-vous?""",
					'Montesquieu dirait: "Il faut avoir beaucoup �tudi� pour savoir peu."',
					"Vos �tudes vous correspondent-elles ?"]
						
	keywords["votre relation avec l'animal"] =    [ 	"�l�phant","poule","singe","cheval","chat","chien","oiseau","vache","h�ron",
					"pigeon","araign�e","f�lin","ch�vre","ver","moustique","insecte","animal","fourrure","l�opard","lion",
					"panth�re","poisson","grenouille","panda","koala","prince charmant","environnement","enfant","ferme",
					"campagne","pie"]
	answers["votre relation avec l'animal"] =        [   	"Avez-vous peur d'un animal?",
						"Quel animal vous incarne le mieux?",
						"Vous aimez les animaux ?",
						"Que vous apportent les animaux?", 
						"Que pensez-vous de votre relation au monde animalier ?",
						"Les psychologues pour animaux ont beaucoup de succ�s. Que diriez-vous d'aller consulter ?",
						"La ferme est un lieu convivial allez-y cela vous fera du bien.",
						"En quel animal aimeriez-vous vous r�incarner?",
						"Quel est votre animal pr�f�r�?",
						"Poss�der un animal vous apaisera.",
						"Avez vous d�j� envisagez de prendre un animal de compagnie ?"]
						
	keywords["Oui"] =    [ "oui","d'accord","bien","ok"]
	answers["Oui"] =  [   	"Mais encore ?",
				"Vous �tes sure ?",
				"C'est tr�s positif.",
				"Bien... Bien...Bien...",
				"C'est bien d'etre positif, mais essayez d'approfondir la question !"]
						
	keywords["Faim"] =    [ "faim","sandwich","ventre","soif","d�jeuner","diner","d�ner","pomme","poire",
				"poulet","steak","fromage","pain","croissant","baguette","nutella","sausissson","yaourt",
				"confiture","poireau","salade","r�gime","gras","graisse","huile","gros","grosse",
				"caf�","banane","cookies","brownies","chips","coca cola","mc donald","hamburger",
				"quick","kfc","biscuits","biscuit","aliments","aliment","frite","frites",
					"bonbons","bonbon"	]
	answers["Faim"] =     [ "Avez-vous faim ?",
				"Avez-vous bien mang� avant de venir en consultation ?",
				"Les r�gimes peuvent vous rendre malheureux.",
				"Avez-vous d�j� pens� qu'il pourrait s'agir d'un probl�me de nouriture ?",
				"Quel est votre r�pas favori ?",
				"Il faut que vous mangiez plus �quilibr�.",
				"Avez-vous d�j� pens� � consulter un nutritionniste ?",
				"Mangez moins et dites m'en plus � votre sujet !"]
						
	keywords["vos v�tement"] =    [ "fringue","pantalon","chemise","chaussette","cuissarde",
					"bouton","tissu","chaussure","chapeau","beret","gants",
					"mit�ne","�charpe","tunique","toge","santiague","botte",
					"sandalette","botine","basket","polo"]
	answers["vos v�tement"] =    [ 	"Avez vous pens� � un relooking ?",
					"Avez vous la fi�vre acheteuse ?",
					"Allez faire les boutiques, �a vous fera du bien !"]
						
	keywords["votre m�tier"] =    [ "instituteur","institutrice","boulanger","boucher","charcutier",
					"chauffeur","barman","commer�ant","ing�nieur","m�decin","vendeur",
					"infirmi�re","chirurgien","avocat","libraire"]
	answers["votre m�tier"] =    [ 	"Avez-vous toujours voulu faire cette profession?",
					"Vous vous entendez bien avec vos coll�gues?",
					"Vous vous sentez bien sur votre lieu de travail?"]
										
										
	keywords["vos vacances"] =    [	"plage","mer","plages","ski","vacance","vacances","farniente","fatigue","voyages",
					"voyage","cong�s","cong�","soleil","d�tente","ballon","raquette",
					"surf","plong�e","bateau","palmiers","palmier","cocotier","cocotiers",
					"montagnes","montagne","nature","natures","campagne","campagnes",
					"piscines","piscine"]
	answers["vos vacances"] =    [  "Pensez-vous � prendre un peu de vacances?",
					"O� comptez-vous partir?",
					"Vous avez le teint p�le, vous avez besoin d'un bon bol d'air.",
					"Allez voir votre patron et prenez quelques jours de cong� !"]
					
	keywords['votre sexualit�'] = [	"sexe", "partenaire", "plaisir", "fantasme", "fantasmes", "mari", "couple", "sexuelle", 
					"sexualit�", "sensuel", "sensualit�", "orgasme", "orgasmes", "fusion", "excitation", 
					"passion", "jouissance", "domination", "soumission", "amant", "maitresse", "amants", 
					"caresses", "caresse", "baiser", "baisers", "pulsion", "pulsions", "masturbation"]
	answers['votre sexualit�'] = [	"Comment d�finiriez-vous votre sexualit� ?", "Vous sentez vous pleinement �panoui(e) ?", 
					"""Alfred Capus disait : " l'amour, c'est quand on obtient pas tout de suite ce qu'on d�sire ", qu'en pensez-vous ?""",
					"Pour vous, amour et sexualit�, sont-ils des notions ind�pendantes ?", 
					"Reprenez confiance en vous, osez ! Vous vous sentirez mieux !", 
					"Parlez-vous de sexualit� avec votre partenaire ?", 
					"Accedez vous au plaisir facilement ?", 
					"Essayez d'en parler � vos ami(e)s, vous verrez que vous n'�tes pas seul(e).", 
					"N'ayez pas honte de vos sentiments, parlez plus librement."]
							
							
	# r�agir � d'autres mots cl�s
	# par exemple : famille, amis, r�ves, sentiments, sexe, �tudes,
	#               musique, tutoiement, maladie, insultes, dieu,
	#               vulgarit�s, doutes, bonheur, tristesse,
	#               suicide, crime, animaux, mode, contradiction
	#               informatique, linguistique, ...........
	# � faire...

	# d'autres id�es : engager une conversation qui permet de conna�tre
	# le nom, le sexe, l'�ge du patient
	# ou extraire automatiquement le sexe gr�ce � des phrase comme
	# je suis content / je suis contente
	#