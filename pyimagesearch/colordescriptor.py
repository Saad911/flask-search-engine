import numpy as np
import cv2

class ColorDescriptor:
	def __init__(self, bins):
		# enregistrer les bin de l'histogramme
		self.bins = bins

	def describe(self, image):
		# conversion du BGR vers HSV
		image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
		# tableau features pour la quantification
		features = []

		# puis on récupére les dimensions et le centre d'image
		(h, w) = image.shape[:2]
		(cX, cY) = (int(w * 0.5), int(h * 0.5))

		# on divise l'image / 4 rectanle ( haut droite / haut gauche and bas droit / bas gauche)
		segments = [(0, cX, 0, cY), (cX, w, 0, cY), (cX, w, cY, h),
			(0, cX, cY, h)]
 
		# construction d'un ellipse qui represente le centre d'image
		(axesX, axesY) = (int(w * 0.75) // 2, int(h * 0.75) // 2)
		ellipMask = np.zeros(image.shape[:2], dtype = "uint8")
		cv2.ellipse(ellipMask, (cX, cY), (axesX, axesY), 0, 0, 360, 255, -1)
 
		for (startX, endX, startY, endY) in segments:
			
			#construction d'un mask pour chaque rectanle et soutraction du centre de
			#l'ellipse
			cornerMask = np.zeros(image.shape[:2], dtype = "uint8")
			cv2.rectangle(cornerMask, (startX, startY), (endX, endY), 255, -1)
			cornerMask = cv2.subtract(cornerMask, ellipMask)
			#on recupere l'histogramme de couleur et on update 
			# le tableau des vecteurs
			hist = self.histogram(image, cornerMask)
			features.extend(hist)
		# puis on récupère l'hsitogramme de couleur de la partie ellipse
		# et on ajoute au tableau de vecteur
		hist = self.histogram(image, ellipMask)
		features.extend(hist)
		# on retourne le vecteur
		return features

	def histogram(self, image, mask):
		# extract a 3D color histogram from the masked region of the
		# image, using the supplied number of bins per channel; then
		# normalize the histogram
		hist = cv2.calcHist([image], [0, 1, 2], mask, self.bins,
			[0, 180, 0, 256, 0, 256])
		# on normalise 
		cv2.normalize(hist,hist)
		hist = hist.flatten()
 
		# on retourne l'histogramme
		return hist
