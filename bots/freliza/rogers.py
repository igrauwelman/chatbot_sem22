#!/usr/bin/python

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
	
	noRecall = ["Question","Retour","Déjà","Vide","Bref","Fin","Insulte","Parceque","Négation","Oui","Faim","Reprise"]
	
	answers={}
	keywords={}
		
		
	answers["Question"] =[	"C'est moi qui pose les questions ici.",
				"Si je vous donnais des réponses, ça serait trop facile.",
				"Si j'avais des réponses à de telles questions, croyez-vous que je serais ici ?",
				"Mon role n'est pas de répondre à vos questions !",
				"L'approche rogérienne à la thérapie a des avantages mais aussi l'inconvénient que je ne peux pas répondre à vos questions."]
	
	answers["Retour"]=[	"Cela vous fait quoi de me dire",
				"Ça vous fait quoi",
				"Pourquoi dites-vous",
				"Pourriez-vous expliciter le fait",
				"Que se passe-t-il en vous quand vous prononcez à haute voix",
				"Comment peut-on finir par dire",
				"Je n'arrive pas à comprendre"]
				
	answers["Déjà"] = [	"Vous avez déjà dit ça. Avançons.",
				"Oui, parfois il est utile de se répéter. Mais j'ai bien compris ce point.",
				"Comme l'a bien dit Boris Vian :  'La mort n'est pas drôle parce qu'elle ne supporte pas la répétition.'",
				"Anatole France dirait :  'A l'endroit du public, répéter c'est prouver.'",
				"Attendez-vous une autre réponse de ma part ?",
				"Quand on n'a pas de mémoire, on se répète : quand on en a, on répète les autres.","Encore !"]
		
	answers["Vide"] = [	"N'hésitez pas, je suis votre docteur !",
				"Mais si vous ne dites rien, je ne peux vous aider.",
				"Vous êtes là, parce que vous souffrez. Parlez-moi de vos souffrances !",
				"Le silence nous amène vers le rien."]
	
	answers["Bref"] = [	"Vous n'êtes pas prodigue de paroles !",
				"Il faudrait en dire un peu plus.",
				"Vous êtes un peu trop taciturne.",
				"Vous ne dites pas un mot de trop."]
		
	answers["Reprise"] = [	"Ramenons nos moutons et parlons un peu plus de xxx.",
				"Peut-être vous serait-il plus utile de reprendre notre discussion au sujet de xxx.",
				"Pourquoi ne continuez-vous pas de parler de xxx ?",
				"Cela nous amène trop loin. Une discussion au sujet de xxx vous aidera plus.",
				"Avons vous parliez de xxx, n'est-ce pas ?"]	
		
############################## fin cas spéciaux


	keywords["Fin"] = [	"au revoir","bye bye","ça suffit"]
	answers["Fin"] = [	"Au revoir.<br>Ma secrétaire vous enverra la facture sous peu.",
				"S'il vous reste de l'argent sur votre carte de crédit, alors on se reverra demain.",
				"Bonne guérison !<br>Et n'oubliez pas de régler sous sept jours.",
				"Si vous n'avez pas dépassé votre autorisation de découvert, on se reverra demain."]
		
		
	keywords["Insulte"] = [	"chier","chie","chié","chiez","chiant","merde","sous-merde",
				"emmerde","emmerdeur","emmerdeuse","emmerdez","emmerder",
				"conasse","connasse","conne","pétasse","poufiasse","grogniasse","grognasse","abrutie","fiotte",
				"connard","abruti","salopard","tasspe","sale porc","batard",
				"pute","putain", "salope","salop","salaud","pestifféré",
				"con","couille", "bite", "cul", 
				"pédé","pd","tafiole","tapette","pédale",
				"bordel","raclure","foutre","nique","niquer"]
	answers["Insulte"] = [	"Ne soyez pas grossier, s'il vous plait!" ,
				"Recentrez-vous sur votre objectif !",
				"Veillez à soigner votre langage !",
				"Vous semblez ne pas avoir compris le but de cette thérapie !",
				"Insulter ceux qui veulent vous aider ne vous mènera à rien !",
				"Non mais vous vous croyez où ? C'est mon dernier avertissement!",
				"Je ne continue pas dans ces conditions. Au revoir",
				"Vous insisitez !!!!"]
			
	keywords["Parceque"] = ["parce que","puisque","donc", "alors"]
	answers["Parceque"] = [ "Le but de cette thérapie est de trouver les faits, pas de raisonner.",
				"Cela ne me semble pas être une implication nécessaire.",
				"Arrêtez de vous trouver des excuses.",
				"Parlez-moi plus de votre logique.","Pourquoi cette contradiction ?"]
			
	keywords["Négation"] =    ["rien","jamais","aucun","aucune","non","pas du tout","pire"]
	answers["Négation"] =  [	"Vous n'êtes pas un peu négatif ?",
					"Think positive !",
					"Nier ne sert à rien."]
						
	keywords["votre famille"] =   [	"mère","père","papa","maman","Papa","Maman","fils",
					"fille","frère","soeur","famille","éducation",
					"bru", "gendre", "oncle", "tante", "inceste", "belle-famille", "enfant", "grands-parents"]
	answers["votre famille"] =   [   	"Parlez un peu plus de votre famille, s'il vous plaît",
					"Que signifie la famille pour vous ?",
					"Êtes-vous sure d'avoir résolu votre Oedipe ?",
					"La famille est un facteur important dans le vie de tous.",
					"Que pensez vous de vos rapports familiaux ?", 
					"Que pouvez vous dire de votre enfance ?", 
					"Pourrez vous un jour pardonner ?", 
					"Définissez vos relations avec vos parents.", 
					"On ne choisit pas sa famille mais on vit avec, ainsi que ses défauts et ses qualités."]

						
	keywords["vos amis"] =   [	"ami","amis","copain","copains","copine","copines","pote"]
	answers["vos amis"] =  [   	"Il peut être important de s'étaler un peu plus sur vos amis.",
				"L'amitié signifie quoi pour vous ?",
				"Oui, personne ne peut vivre sans amis."]
						
	keywords["vos problèmes"] =    [	"malaise","malheureux","problème","problèmes","malheur","malheurs", "malheur","mal","noir",
					"malheureuse","pas heureux","mélancolie","mélancolique","déprime","déprimé",
					"déprimée","triste","tristesse",
					"dépression","dépressif","dépressive","las","lasse","lassé","lassée", "fatigue","fatigué","fatiguée",
					"difficile","divorce","enterrement","enfer","démon","séparation",
					"difficultés","difficulté","catastrophe","mourrir","mort","suicider","suicide", "morbide"]
	answers["vos problèmes"] = [   	"Reprennez-vous, vous êtes trop négatif.", 
					"Courage, la thérapie est justement là pour aider à reprendre confiance en vous.", 
					"Vous semblez perdre pied.",
					"Est-il poissible que vous avez besoin de plus de confiance ?",
					"Parler vous redonnera confiance en vous",
					"Le bonheur est dans le pré.", 
					"Croquez la vie à pleine dents!", 
					"Ne soyez pas triste, la vie est belle.", 
					"Si rien ne va allez voir un psy!", 
					"Rien ne sert de sauter il faut réagir à temps!", 
					"Pas de panique ! Eliza s'occupe de tout!", 
					"Rien ne vaut le chocolat pour remonter le moral!", 
					"Rire prolonge la vie pensez-y...", 
					"La vie est courte profitez-en!", 
					"Respirez !! Ça calme...", 
					"Comment vous sentez-vous?", 
					"A malheur bonheur est bon.", 
					"Prenez la vie par le bon bout et ça ira mieux!",]
	
						
	keywords["votre avenir"] =    [	"projet","réussir","réussite","projets","avenir","futur","concrétiser",
					"concrétisé","espoir","demain","espoirs","réalisation","réalisations", "espère","souhait","souhaite"]
	answers["votre avenir"] =        [   	"C'est encourageant, vous construisez des projets!",
						"Comment vous projetez-vous dans l'avenir?", 
						"Comment construisez-vous votre futur?",
						"Comment vous imaginez-vous dans quelques années?",
						"Avez-vous foi en votre avenir?", 
						"Êtes-vous confiant quant à votre avenir?"]      
						
	keywords["vos craintes"] =   [ 	"peur", "peurs","crainte","craintes", "crains","hésite", "hésitations",
					"hésitation","incertain","incertaine","dubitatif","dubitative"]
	answers["vos craintes"] =   [   "Mais d'où vient votre incertitude?",
					"Il faut que vous ayez plus confiance en vous",
					"Soyez rassuré, je suis là pour vous écouter.",
					"La confiance en soi vous mènera vers la guérison.",
					"Commencez par vous faire confiance."]
									
	keywords["vos envies"] =   [ 	"envie","désir","envies","souhaite","désirs","souhait"]
	answers["vos envies"] =        ["Mais de quoi avez-vous réellement envie?",
					"En avez-vous réellement envie?",
					"Êtes-vous sure que vos souhaits correspondent à vos besoins ?"] 
	keywords["vos peurs"] =   [ 	"peur","peurs","cauchemar","crainte","craintes","effrayé","persécution","psychose",
					"névrose","panique","vertige",
					"trouillard","anxiété","phobie","paranoïa"]
	answers["vos peurs"] =        [ "Êtes-vous sujet à des peurs liées au vide ou à l'enfermement?",
					"De quoi avez-vous vraiment peur ?",
					"Qu'est-ce qui vous effraie ?"]
						
	keywords["vos rêves"] =   [ 	"rêves","rêve","désir","image',images","désirs","fantasme","fantasmes"]
	answers["vos rêves"] =        [ "S'agit-il plutot de désir ou d'interdit lié à votre journée précédente ?",
					"A votre avis, en quoi ce rêve est-il révélateur de votre situation actuelle ?",
					"Comment pouvez-vous m'expliquer le sens de ces images ?",
					"Quelles interprétations pouvez-vous en faire ?"]
						
	keywords["la religion"] =    [ 	"religion","dieu","déesse","crois","ange","prière","prie","moine",
					"perdu","église","prêtre","croyances","croyance","ésotérique","ésotérisme","gourou",
					"astrologie","étoile"]
	answers["la religion"] =        [   	"Que pensez-vous de la phrase 'La religion est l'opium du peuple' ?",
						"Croire est ne pas savoir.",
						"Sans votre religion, vous sentiriez-vous plus libre ?",
						"Pourquoi parlez-vous de vos croyances ?"] 
						
	keywords["cinéma"] =    [ 	"cinéma","film","films","acteur","actrice","acteurs","actrices","cannes"]
	answers["cinéma"] = [   	"Vous allez souvent au cinéma ?",
					"Est-ce que vous aimez les films de gladiateurs ?",
					"Est-ce que vous aimez les films d'aventure ?",
					"Que pensez-vous des films de cul ?",
					"Que pensez-vous des films d'amour ?" ,
					"Mais je ne comprends pas, pourquoi parlez-vous de ça ?",
					"Quel genre de film représente le mieux vos difficultés actuelles ?"]
						
	keywords["l'université"] =   [ 	"étude","études","université","fac","faculté","profession",
					"professionnel","professionnelle","examen",
					"examens","partiel","partiels","classe","cours","camarade","camarades"]
	answers["l'université"] =     [ "Mais quel métier voudriez-vous faire ?",
					"Vos buts professionnels sont-ils réalistes ?",
					"Construisez-vous un projet à travers votre formation ?",
					"Vous sentez-vous bien dans vos études ?",
					"Avez-vous de bonnes méthodes de travail ?",
					"Essayez-vous de vous intégrer?",
					"""Sénèque a dit "Etudie, non pour savoir plus, mais pour savoir mieux." Qu'en pensez-vous?""",
					'Montesquieu dirait: "Il faut avoir beaucoup étudié pour savoir peu."',
					"Vos études vous correspondent-elles ?"]
						
	keywords["votre relation avec l'animal"] =    [ 	"éléphant","poule","singe","cheval","chat","chien","oiseau","vache","héron",
					"pigeon","araignée","félin","chèvre","ver","moustique","insecte","animal","fourrure","léopard","lion",
					"panthère","poisson","grenouille","panda","koala","prince charmant","environnement","enfant","ferme",
					"campagne","pie"]
	answers["votre relation avec l'animal"] =        [   	"Avez-vous peur d'un animal?",
						"Quel animal vous incarne le mieux?",
						"Vous aimez les animaux ?",
						"Que vous apportent les animaux?", 
						"Que pensez-vous de votre relation au monde animalier ?",
						"Les psychologues pour animaux ont beaucoup de succès. Que diriez-vous d'aller consulter ?",
						"La ferme est un lieu convivial allez-y cela vous fera du bien.",
						"En quel animal aimeriez-vous vous réincarner?",
						"Quel est votre animal préféré?",
						"Posséder un animal vous apaisera.",
						"Avez vous déjà envisagez de prendre un animal de compagnie ?"]
						
	keywords["Oui"] =    [ "oui","d'accord","bien","ok"]
	answers["Oui"] =  [   	"Mais encore ?",
				"Vous êtes sure ?",
				"C'est très positif.",
				"Bien... Bien...Bien...",
				"C'est bien d'etre positif, mais essayez d'approfondir la question !"]
						
	keywords["Faim"] =    [ "faim","sandwich","ventre","soif","déjeuner","diner","dîner","pomme","poire",
				"poulet","steak","fromage","pain","croissant","baguette","nutella","sausissson","yaourt",
				"confiture","poireau","salade","régime","gras","graisse","huile","gros","grosse",
				"café","banane","cookies","brownies","chips","coca cola","mc donald","hamburger",
				"quick","kfc","biscuits","biscuit","aliments","aliment","frite","frites",
					"bonbons","bonbon"	]
	answers["Faim"] =     [ "Avez-vous faim ?",
				"Avez-vous bien mangé avant de venir en consultation ?",
				"Les régimes peuvent vous rendre malheureux.",
				"Avez-vous déjà pensé qu'il pourrait s'agir d'un problème de nouriture ?",
				"Quel est votre répas favori ?",
				"Il faut que vous mangiez plus équilibré.",
				"Avez-vous déjà pensé à consulter un nutritionniste ?",
				"Mangez moins et dites m'en plus à votre sujet !"]
						
	keywords["vos vêtement"] =    [ "fringue","pantalon","chemise","chaussette","cuissarde",
					"bouton","tissu","chaussure","chapeau","beret","gants",
					"mitène","écharpe","tunique","toge","santiague","botte",
					"sandalette","botine","basket","polo"]
	answers["vos vêtement"] =    [ 	"Avez vous pensé à un relooking ?",
					"Avez vous la fièvre acheteuse ?",
					"Allez faire les boutiques, ça vous fera du bien !"]
						
	keywords["votre métier"] =    [ "instituteur","institutrice","boulanger","boucher","charcutier",
					"chauffeur","barman","commerçant","ingénieur","médecin","vendeur",
					"infirmière","chirurgien","avocat","libraire"]
	answers["votre métier"] =    [ 	"Avez-vous toujours voulu faire cette profession?",
					"Vous vous entendez bien avec vos collègues?",
					"Vous vous sentez bien sur votre lieu de travail?"]
										
										
	keywords["vos vacances"] =    [	"plage","mer","plages","ski","vacance","vacances","farniente","fatigue","voyages",
					"voyage","congés","congé","soleil","détente","ballon","raquette",
					"surf","plongée","bateau","palmiers","palmier","cocotier","cocotiers",
					"montagnes","montagne","nature","natures","campagne","campagnes",
					"piscines","piscine"]
	answers["vos vacances"] =    [  "Pensez-vous à prendre un peu de vacances?",
					"Où comptez-vous partir?",
					"Vous avez le teint pâle, vous avez besoin d'un bon bol d'air.",
					"Allez voir votre patron et prenez quelques jours de congé !"]
					
	keywords['votre sexualité'] = [	"sexe", "partenaire", "plaisir", "fantasme", "fantasmes", "mari", "couple", "sexuelle", 
					"sexualité", "sensuel", "sensualité", "orgasme", "orgasmes", "fusion", "excitation", 
					"passion", "jouissance", "domination", "soumission", "amant", "maitresse", "amants", 
					"caresses", "caresse", "baiser", "baisers", "pulsion", "pulsions", "masturbation"]
	answers['votre sexualité'] = [	"Comment définiriez-vous votre sexualité ?", "Vous sentez vous pleinement épanoui(e) ?", 
					"""Alfred Capus disait : " l'amour, c'est quand on obtient pas tout de suite ce qu'on désire ", qu'en pensez-vous ?""",
					"Pour vous, amour et sexualité, sont-ils des notions indépendantes ?", 
					"Reprenez confiance en vous, osez ! Vous vous sentirez mieux !", 
					"Parlez-vous de sexualité avec votre partenaire ?", 
					"Accedez vous au plaisir facilement ?", 
					"Essayez d'en parler à vos ami(e)s, vous verrez que vous n'êtes pas seul(e).", 
					"N'ayez pas honte de vos sentiments, parlez plus librement."]
							
							
	# réagir à d'autres mots clés
	# par exemple : famille, amis, rèves, sentiments, sexe, études,
	#               musique, tutoiement, maladie, insultes, dieu,
	#               vulgarités, doutes, bonheur, tristesse,
	#               suicide, crime, animaux, mode, contradiction
	#               informatique, linguistique, ...........
	# à faire...

	# d'autres idées : engager une conversation qui permet de connaître
	# le nom, le sexe, l'âge du patient
	# ou extraire automatiquement le sexe grâce à des phrase comme
	# je suis content / je suis contente
	#