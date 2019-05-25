# coding: utf-8
import os
import sys
import csv
import urllib
#import xmltodict
import shutil
import pprint
import json
import glob
#import os.path.basename

import sys
defaultencoding = 'iso-8859-1'
if sys.getdefaultencoding() != defaultencoding:
    reload(sys)
    sys.setdefaultencoding(defaultencoding)

#Etape 1 : Recuperer le fichier CSV
#Ici on recupere le chemin du fichier contenant les valeurs CSV

reponse = raw_input("(a) CSV - Grobid , (b) JSON - TXT, (c) CSV - JSON , (d) JSON Generation\n")
print(reponse)

#Menu de navigation
if reponse == 'a':
	#CSV vers XML avec recuperation des PDF en ligne
	print("Transformation CSV -> XML")
	#nomFichier = reponse + ".csv
	data = open("Data.csv" , "r")

	#indice des colonnes contenant les informations qui nous interesse
	indiceColPDF = 8
	indiceColMS = 9

	#Param definissant les delimiteurs dans le document CSV
	#print(nomFichier)
	reader = csv.reader(data,delimiter=';')

	#Boucle principale
	#Etape 2 : Trier ce CSV pour ne recuperer que les lignes avec les bons MS
	#Etape 3 : Parmis ces lignes on ne recup que les valeurs lignes par lignes 
	#de la colonne contenant le lien vers le fichier PDF
	#Etape 4 : (a)On va recuperer un par un les PDF
	#les telecharger et (b) les passer individuellement sur GroBid TEI
	#pour obtenir un .XML par ligne
	#Etape 5 : Ces .XML vont ensuite etre transformes au format .JSON
	for row in reader:
		if(row[indiceColMS] != 'MS'):
			if float(row[indiceColMS]) >= 1 and float(row[indiceColMS]) <= 9:
				valeur = row[indiceColPDF]
				#apres cela on a plus que les lignes triees par MS
				#print(row)test recup des lignes
				#Etape 3 :
				#valeur contient desormais l'adr du lien PDF du CSV
				print(valeur)
				#Etape 4 (a):
				chaineNom = "pdfArticle"+row[0]+".pdf"
				print(chaineNom)
				chaineNom = "./in/"+chaineNom
				urllib.urlretrieve(valeur,chaineNom)

	#Etape 4 (b) :
	#on passe le document pdf sur l'API de Grobid pour obtenir un .XML TEI

	#reponse = input("Appliquer la transfo TEI ? (oui/non)")
	#if reponse == "o":
	os.system('python3.5 ./grobid-client.py --input ./in/ --output ./out/ processHeaderDocument')

	#rep = input('Presser une fois la transfo effectuee')

	#Etape 5 : JSON et Affinement
	chemin = './out/*.tei.xml'
	cheminMary = './out/json/*.json'
	fichiersTEI = glob.glob(chemin)
	i = 1
	print('Avant la boucle de transformation')
	for nom in fichiersTEI:
		with open(nom) as f:
			print('Pendant la transfo')
			doc = xmltodict.parse(f.read(),encoding='utf-8')
			chaineNomBis = "./out/json/jsonArticle"+str(i)+".json"
			f2 = open(chaineNomBis,"w")
			f2.write(json.dumps(doc,sort_keys=True))
			f2.close()
			#Recuperation des informations necessaires
			#fluxDon = json.dumps(doc,sort_keys=True)
			#auteur = fluxDon['persName']['forename']['#text']
			#settlement = 
			#Une fois les donnees recuperees on recreer un doc json clone
			#Permettant de ne garder que les champs qui nous interesse dans la structure que l'on souhaite
			pp = pprint.PrettyPrinter(indent=4)
			pp.pprint(json.dumps(doc))
			i = i+1

if reponse == 'b':
	#JSON vers TXT (avec sauvegarde en csv)
	print("Transformation JSON -> txt (champs abstract et id")
	cheminJSON = './out/refract/*.json'
	fichiersJSON = glob.glob(cheminJSON)
	print('Debut de la chaine de transformation')
	chaineCSV = "id;annee\n"
	for nom in fichiersJSON:
		with open(nom) as f:
			#extraire a partir d une liste de json une liste au format txt (id et abstract)
			#recuperation des JSON
			try:
				valeurs = json.load(f)
				idArt = str(valeurs['idArt'].encode('utf-8','strict'))
				abstract = str(valeurs['abstract']).encode('utf-8','strict')
				annee = str(valeurs['year'].encode('utf-8','strict'))
				print('Transformation article_'+str(idArt)+' : en cours . . .')
				chaineEcritureTXT = "./out/refract/txt/article_" + str(idArt) + ".txt"
				#test
				#chaine = "Id de l'Article : "+idArt+"\nResume de l'Article : "+abstract
				#ecriture dans txt
				f2 = open(chaineEcritureTXT,"w")
				f2.write(abstract)
				f2.close()
				chaineCSV = chaineCSV + os.path.basename(f.name) + "," + annee + "\n"
				idArt = ""
				abstract = ""
				annee = ""
			except ValueError as e:
       				print "Could not load {}, invalid JSON".format({})
				#on copie colle le fichier brut directement dans le repertoire
				cheminFichier_Erreur = str("./out/refract/erreur/" + os.path.basename(f.name))
				shutil.copyfile(f.name, cheminFichier_Erreur)
	#print('Sauvegarde des données : id et annees effectuee dans out/refract/csv !')
	#test ecriture csv
	#print(chaineCSV)
	f3 = open("./out/refract/csv/metadata.csv","w")
	f3.write(chaineCSV)
	f3.close()

if reponse == 'c':
	#CSV vers JSON
	print("Transformation CSV -> JSON (tout les champs")
	cheminCSV = './out/CSVToJSON/*.csv'
	i = 1
	fichiersCSV = glob.glob(cheminCSV)
	print('Debut de la chaine de transformation')
	indiceColMS = 8
	for nom in fichiersCSV:
		with open(nom) as f:
			reader = csv.reader(f,delimiter=';')
			for row in reader:
				if(row[indiceColMS] != 'MS'):
					#if float(row[indiceColMS]) >= 1 and float(row[indiceColMS]) <= 8:
						idArticle = str(row[0].encode('utf-8','strict'))
						series = str(row[1].encode('utf-8','strict'))
						booktitle = str(row[2].encode('utf-8','strict'))
						year = str(row[3].encode('utf-8','strict'))
						title = str(row[4].encode('utf-8','strict'))
						abstract = str(row[5].encode('utf-8','strict'))
						authors = str(row[6].encode('utf-8','strict'))
						pdf1page = str(row[7].encode('utf-8','strict'))
						pdfarticle = str(row[8].encode('utf-8','strict'))
						MS = str(row[9])
						place = str(row[10])
						Latitude = str(row[11])
						Longitude = str(row[12])
						
						chaineNom = "article_"+row[0]+".json"
						print(chaineNom)
						chaineNom = "./out/CSVToJSON/json/" + chaineNom
						f2 = open(chaineNom,"w")
						f2.write('{\n"idArt": "'+str(idArticle)+ '",\n"series": "'+str(series)+'",\n"booktitle": "' + str(booktitle)+ '",\n"year": "'+str(year)+ '",\n"title": "'+str(title)+ '",\n"abstract": "'+str(abstract)+'",\n"authors": "'+str(authors)+'",\n"pdf1page": "' + str(pdf1page)+'",\n"pdfarticle": "'+str(pdfarticle)+ '",\n"metaSession": "'+str(MS)+'",\n"place": "'+str(place) +'",\n"Latitude": " '+str(Latitude)+' ",\n"Longitude": "'+str(Longitude)+'"\n}')
						f2.close()

if reponse == 'd':
	#Generation JSON
	print("Generation de JSON fusionnes\n")
	#Repertoires des JSON qui serront a fusionner
	cheminJSON1 = './out/assemble/listeArticles/*.json'
	cheminJSON2 = './out/assemble/listeArticles_complement_metaSession/*.json'
	cheminJSON3 = './out/assemble/listeArticles_complement_villeAuteur/*.json'
	i = 1
	fichiersJSON1 = glob.glob(cheminJSON1)
	print('Debut de la chaine de transformation')
	for nom in fichiersJSON1:
		with open(nom) as f:
			#extraire les donnees du repertoire 1
			try:			
				valeurs = json.load(f)
				if 'year' not in valeurs:
					print("Pas de champs 'year' dans les json a l'iteration  : " + str(i) + " du repertoire 1")
					year1 = ""
				else:
					year1 = str(valeurs['year'].encode('utf-8','strict'))
			
				if 'pdf1page' not in valeurs:
					#raise ValueError("Pas de champs 'pdf1page' dans les json a l'iteration  : " + str(i) + " du repertoire 1")
					pdf1page1 = ""
				else:
					pdf1page1 = str(valeurs['pdf1page'].encode('utf-8','strict'))

				if 'pdfarticle' not in valeurs:
					#raise ValueError("Pas de champs 'pdfarticle' dans les json a l'iteration  : " + str(i) + " du repertoire 1")
					pdfarticle1 = ""
				else: 
					pdfarticle1 = str(valeurs['pdfarticle'].encode('utf-8','strict'))
			
				if 'abstract' not in valeurs:
					#raise ValueError("Pas de champs 'abstract' dans les json a l'iteration  : " + str(i) + " du repertoire 1")
					abstract1 = ""
				else: 
						abstract1 = str(valeurs['abstract'].encode('utf-8','strict'))
									

				if 'title' not in valeurs:
					#raise ValueError("Pas de champs 'title' dans les json a l'iteration  : " + str(i) + " du repertoire 1")
					title1 = ""
				else:
					title1 = str(valeurs['title'].encode('utf-8','strict'))
		
				if 'series' not in valeurs:
					#raise ValueError("Pas de champs 'series' dans les json a l'iteration  : " + str(i) + " du repertoire 1")
					series1 = ""
				else: 
					series1 = str(valeurs['series'].encode('utf-8','strict'))
			
				if 'location' not in valeurs:
					#raise ValueError("Pas de champs 'location' dans les json a l'iteration  : " + str(i) + " du repertoire 1")
					location1 = ""
				else: 
					location1 = str(valeurs['location'])	
	
			
				if 'booktitle' not in valeurs:
					#raise ValueError("Pas de champs 'booktitle' dans les json a l'iteration  : " + str(i) + " du repertoire 1")
					booktitle1 = ""
				else: 
					booktitle1 = str(valeurs['booktitle'].encode('utf-8','strict'))	

				if 'idArt' not in valeurs:
					#raise ValueError("Pas de champs 'idArt' dans les json a l'iteration  : " + str(i) + " du repertoire 1")
					idArt1 = ""
				else:
					idArt1 = str(valeurs['idArt'].encode('utf-8','strict'))

				if 'authors' not in valeurs:
					#raise ValueError("Pas de champs 'authors' dans les json a l'iteration  : " + str(i) + " du repertoire 1")
					authors1 = ""
				else: 
					j = 0
					#print(len(valeurs['authors']))
					if len(valeurs['authors']) > 1 :
						#Si il y'a plusieurs auteurs
						while j < len(valeurs['authors']):
							if j == 0 :
								authors1 = "['"+str(valeurs['authors'][j].encode('utf-8','strict'))+"'"
								j = j+1
							else:	
								if j == (len(valeurs['authors'])-1):
									authors1 = authors1 + "," + "'" + str(valeurs['authors'][j].encode('utf-8','strict')) + "']"
									j = j +1
								else: 
									authors1 = authors1 + "," + "'" + str(valeurs['authors'][j].encode('utf-8','strict')) + "'"
									j = j +1
					else:
						authors1 = str(valeurs['authors'][0].encode('utf-8','strict'))
				if 'place' not in valeurs:
					#raise ValueError("Pas de champs 'authors' dans les json a l'iteration  : " + str(i) + " du repertoire 1")
					place1 = ""
				else: 
					place1 = str(valeurs['place'])
			
				#Verification dans le repertoire complement metaSession
				print(os.path.basename(f.name))
				chaineVerif_metaSession = str("./out/assemble/listeArticles_complement_metaSession/" + os.path.basename(f.name))
				if(os.path.isfile(chaineVerif_metaSession)):
					#alors le fichier concerne par l'article a un complement metaSession
					f2 = open(chaineVerif_metaSession)
					#recuperation de ses valeurs
					valeurs_metaSession = json.load(f2)

					if 'metaSession' not in valeurs_metaSession:
						#raise ValueError("Pas de champs 'metaSession'")
						print("pas de placeAut")
						metaSession2 = ""
					else: 
						metaSession2 = str(valeurs_metaSession['metaSession'].encode('utf-8','strict'))
				else:
					#Dans le cas ou il n'existe pas de correspondance avec un complement metaSession on definit la valeur comme vide
					metaSession2 = ""			

				chaineVerif_Ville = str("./out/assemble/listeArticles_complement_villeAuteur/" + os.path.basename(f.name))
				if(os.path.isfile(chaineVerif_Ville)):
					#alors le fichier concerne par l'article a un complement listeArticles_complement_villeAuteur
					f3 = open(chaineVerif_Ville)
					#recuperation de ses valeurs
					valeurs_Ville = json.load(f3)

					if 'placeAut' not in valeurs_Ville:
						#raise ValueError("Pas de champs 'placeAut'")
						print("pas de placeAut")
						placeAut3 = ""
					else: 
						j = 0
						un = str(valeurs_Ville['placeAut'][0]['place']).encode('utf-8')
						deux = str(valeurs_Ville['placeAut'][0]['country']).encode('utf-8')
						trois = str(valeurs_Ville['placeAut'][0]['location']['lat']).encode('utf-8')
						quatre = str(valeurs_Ville['placeAut'][0]['location']['lon']).encode('utf-8')
						placeAut3='[{\n"place":'+'"'+un+'",'+'\n"country":'+'"'+deux+'"'+"," +'\n"location":{\n\t"lat":'+'"'+trois+'",'+'\n\t"lon":'+'"'+quatre+'"'+"\n}\n"
						
						
				#else:
					#Dans le cas ou il n'existe pas de correspondance avec un complement ville on definit la valeur comme vide
					#placeAut3 = ""

				#Une fois les valeurs recuperees on va creer le fichier json fusionne dans rep3
				chaineEcritureJSON = "./out/assemble/fusion/" + os.path.basename(f.name)
				fusion_year = year1
				fusion_metaSession = metaSession2
				fusion_pdf1page = pdf1page1
				fusion_pdfarticle = pdfarticle1
				fusion_abstract = abstract1
				fusion_title = title1
				fusion_placeAut = placeAut3
				fusion_series = series1
				fusion_location = location1
				fusion_place = place1
				fusion_booktitle = booktitle1
				fusion_idArt = idArt1
				fusion_authors = authors1
				print(str(fusion_authors))
				
				#Maintenant que l'on a toutes les valeurs on peut creer le nouveau fichier JSON de concatenation
				f4 = open(chaineEcritureJSON,"w")
				f4.write('{\n"year": "'+str(fusion_year)+ '",\n"metaSession": "'+str(fusion_metaSession)+'",\n"pdf1page": "' + str(fusion_pdf1page)+ '",\n"pdfarticle": "'+str(fusion_pdfarticle)+ '",\n"abstract": "'+str(fusion_abstract)+ '",\n"title": "'+str(fusion_title)+'",\n"placeAut":'+str(fusion_placeAut)+'}],\n"series": "' + str(fusion_series)+'",\n"location": "' + str(fusion_location)+'",\n"place": "' + str(fusion_place)+'",\n"booktitle": "' + str(fusion_booktitle)+'",\n"idArt": "' + str(fusion_idArt)+'",\n"authors": "'+str(fusion_authors)+'"\n}')
				f4.close()
				f.close()

			except ValueError as e:
       				print(e)
				#on copie colle le fichier brut directement dans le repertoire
				cheminFichier_Erreur = str("./out/assemble/fusion/erreur/" + os.path.basename(f.name))
				shutil.copyfile(f.name, cheminFichier_Erreur)
				
				print('***************************************')
