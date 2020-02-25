# import the necessary packages
import numpy as np
import csv

class Searcher:
	def __init__(self, indexPath):
		#chemin d'indextation 
		self.indexPath = indexPath

	def search(self, queryVector, limit=101):
		#on initialise un dictionnaire vide
		results = {}

		#on ouvre le fichier la on veut indexer
		with open(self.indexPath) as f:
			#on initialise le lecteur CSV
			reader = csv.reader(f)

			for row in reader:
				#pour chaque image dans .csv on calcule la distance par rapport
				# à l'image selectionné ( query )
				vector = [float(x) for x in row[1:]]
				d = self.chi2_distance(vector, queryVector)

				#Update le dictionnaire
				# dictionnaire key : image id
				# dictionnaire value : similarité
				results[row[0]] = d

			#close reader
			f.close()

		#on fait un sort des valeurs
		results = sorted([(v,k) for (k,v) in results.items()])

		#on retourne les 2..3...4.. premiers images similaires // whatever
		return results[:5]


	# Notre fonction qui calcule la distance 
	def chi2_distance(self, histA, histB, eps=1e-10):
		d = 0.5 * np.sum([((a-b)**2)/(a+b+eps)
			for (a,b) in zip(histA, histB)])

		# on retourne la distance
		return d
