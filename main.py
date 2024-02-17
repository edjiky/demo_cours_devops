#!/usr/bin/env python2
# -*- coding: utf-8 -*-

"""
Programme de bruitage et débruitage d'une image avec calcul du SNR
Par Mathis SERRIERES MANIECKI et David BALLARD
"""

#--- Bibliothèques ---
import tkinter as tk
from PIL import Image, ImageTk
import random as rdm
import tkinter.messagebox
import tkinter.filedialog
import skimage.io as io
import numpy as np
import math as math
import imageio


#--- Variables ---
CheminAcces = ""        #Chemin d'accès du fichier
image = ""              #Image de base
matrice_image = ""      #Matrice de base de l'image
image_choisie = 0       #Variable permettant de savoir si une image à été choisie ou non


#--- Sélection d'une image ---
def Fenetre_Selection_IMG():
    #Importation des variables globales
    global image
    global matrice_image
    global image_choisie
    global CheminAcces
    
    #Sélection de l'image
    CheminAcces = tk.filedialog.askopenfilename(title="Ouvrir une image", filetypes=[('png files','.png'),('all files','.*')])
    #Récupération et conversion de l'image
    image = io.imread(CheminAcces)
    matrice_image = 1.0 * np.array(image)
    
    #Déblocage des différents bruitages et débruitages
    if (CheminAcces != ""):
        image_choisie = 1
    #Modification du texte dans la fenêtre principale
    Chemin_Acces_Texte.config(text=CheminAcces)


#--- Fenêtre d'erreur ---
def Fenetre_Aucune_Image():
    #Création de la fenêtre fille
    fenetre = tk.Toplevel(fenetrePrincipale)                
    fenetre.title("Erreur")
    
    #Affichage du texte et du bouton dans la fenêtre
    tk.Label(fenetre, text="Vous devez sélectionner une image avant de continuer !").pack(padx=10, pady=10)
    tk.Button(fenetre, text='Retour', command=fenetre.destroy).pack(side=tk.BOTTOM, pady=10)
    
    #Boucle de la fenêtre
    fenetre.mainloop()


#--- Fenêtre Bruitage Poivre et Sel ---
def Fenetre_Bruitage_PoivreSel():
    #Sécurité si aucune image n'a été sélectionnée
    if (image_choisie == 0):
        #Lance la fenêtre d'erreur
        Fenetre_Aucune_Image()
    else:
        #Création de la fenêtre fille
        fenetre = tk.Toplevel(fenetrePrincipale)                
        fenetre.title("Bruitage Poivre et Sel")
       
        #- Cadre du haut -
        #Mise en page et affichage du texte
        haut = tk.Frame(fenetre, borderwidth=2, relief=tk.GROOVE)
        haut.pack(side=tk.TOP, padx=30, pady=30)
        tk.Label(haut, text="Bruitage d'une image en utilisant la méthode Poivre et Sel").pack(padx=10, pady=10)
        
        #- Cadre du centre -
        centre = tk.Frame(fenetre)
        centre.pack(fill="both", expand="yes", padx=20)
        
        #- Cadre de gauche -
		#Mise en page et affichage du texte
        centreGauche = tk.Frame(centre, borderwidth=2, relief=tk.GROOVE)
        centreGauche.pack(side=tk.LEFT, fill="both", expand="yes", padx=20)
        tk.Label(centreGauche, text="Image d'origine", pady=10).pack()
        #Récupération de l'image d'origine
        Image_Reference = ImageTk.PhotoImage(file=CheminAcces)
        #Création d'un Canvas permettant l'affichage de l'image
        Canvas_Reference = tk.Canvas(centreGauche, bg='white', width=matrice_image.shape[0], height=matrice_image.shape[1])
        Canvas_Reference.create_image(0, 0, anchor=tk.NW, image=Image_Reference)
        Canvas_Reference.pack()
       
        #- Cadre de droite -
		#Mise en page et affichage du texte
        centreDroite = tk.Frame(centre, borderwidth=2, relief=tk.GROOVE)
        centreDroite.pack(side=tk.RIGHT, fill="both", expand="yes", padx=20)
        tk.Label(centreDroite, text="Image bruitée", pady=10).pack()
        #Bruitage et enregistrement de l'image bruitée
        matrice_bruitage = Bruitage_PoivreSel(matrice_image, Valeur.get())
        imageio.imsave("Image_Bruitee.png", matrice_bruitage)
        Image_Bruitee = ImageTk.PhotoImage(file="Image_Bruitee.png")
        #Création d'un Canvas permettant l'affichage de l'image
        Canvas_Bruitage = tk.Canvas(centreDroite, width=matrice_image.shape[0], height=matrice_image.shape[1])
        Canvas_Bruitage.create_image(0, 0, anchor=tk.NW, image=Image_Bruitee)
        Canvas_Bruitage.pack()
       
        #- Cadre du SNR -
        #Exécution de la fonction du SNR
        SNR(matrice_image, matrice_bruitage)
        calcul = tk.LabelFrame(fenetre, text="Calcul du SNR :")
        calcul.pack(padx=20, pady=20)
        #Affichage des résultats du SNR
        tk.Label(calcul, textvariable=puissanceBruit).pack()
        tk.Label(calcul, textvariable=puissanceSignal).pack()
        tk.Label(calcul, textvariable=SNR_).pack()
        
        #- Cadre du bas -
		#Mise en page et affichage du bouton retour
        bas = tk.Frame(fenetre)
        bas.pack(side=tk.BOTTOM, padx=15, pady=15)
        tk.Button(bas, text='Retour', command=fenetre.destroy).pack(side=tk.BOTTOM)
        
        #Boucle de la fenêtre
        fenetre.mainloop()


#--- Bruitage Poivre et Sel ---
def Bruitage_PoivreSel(image,bruitage):                  
    #Copie de la matrice originale
    bruitage = 100-bruitage
    image_bruitee = np.copy(image)                   	
    
    #Parcourt de la matrice
    for i in range(image_bruitee.shape[0]):
        for j in range(image_bruitee.shape[1]):     
            #On génère un nombre aléatoire entre 0 et 10 pour sélectionner le pixel à bruiter
            taux_bruitage = rdm.randint(0, bruitage)
            #Si le nombre aléatoire = 10
            if taux_bruitage == bruitage:
                #On génère un nombre aléatoire entre 0 et 1 pour la sélection de la couleur
                couleur_pixel = rdm.randint(0, 1)
                #Si le nombre aléatoire = 0
                if couleur_pixel == 0:
                    #On change le pixel en noir
                    image_bruitee[i,j] = 0
                else:
                    #On change le pixel en blanc
                    image_bruitee[i,j] = 255
    
    #On retourne la matrice modifiée
    return image_bruitee


#--- Fenêtre Bruitage Additif ---
def Fenetre_Bruitage_Additif():
    #Sécurité si aucune image n'a été sélectionnée
    if (image_choisie == 0):
        #Lance la fenêtre d'erreur
        Fenetre_Aucune_Image()
    else:
        #Création de la fenêtre fille
        fenetre = tk.Toplevel(fenetrePrincipale)                
        fenetre.title("Bruitage Additif")

        #- Cadre du haut -
        #Mise en page et affichage du texte
        haut = tk.Frame(fenetre, borderwidth=2, relief=tk.GROOVE)
        haut.pack(side=tk.TOP, padx=30, pady=30)
        tk.Label(haut, text="Bruitage d'une image en utilisant la méthode Additive").pack(padx=10, pady=10)
        
        #- Cadre du centre -
        centre = tk.Frame(fenetre)
        centre.pack(fill="both", expand="yes", padx=20)
        
        #- Cadre de gauche -
		#Mise en page et affichage du texte
        centreGauche = tk.Frame(centre, borderwidth=2, relief=tk.GROOVE)
        centreGauche.pack(side=tk.LEFT, fill="both", expand="yes", padx=20)
        tk.Label(centreGauche, text="Image d'origine", pady=10).pack()
        #Récupération de l'image d'origine
        Image_Reference = ImageTk.PhotoImage(file=CheminAcces)
		#Création d'un Canvas permettant l'affichage de l'image
        Canvas_Reference = tk.Canvas(centreGauche, bg='white', width=matrice_image.shape[0], height=matrice_image.shape[1])
        Canvas_Reference.create_image(0, 0, anchor=tk.NW, image=Image_Reference)
        Canvas_Reference.pack()

        #- Cadre de droite -
		#Mise en page et affichage du texte
        centreDroite = tk.Frame(centre, borderwidth=2, relief=tk.GROOVE)
        centreDroite.pack(side=tk.RIGHT, fill="both", expand="yes", padx=20)
        tk.Label(centreDroite, text="Image bruitée", pady=10).pack()
        #Bruitage et enregistrement de l'image bruitée
        matrice_bruitage = Bruitage_Additif(matrice_image, Valeur.get())
        imageio.imsave("Image_Bruitee.png", matrice_bruitage)
        Image_Bruitee = ImageTk.PhotoImage(file="Image_Bruitee.png")
        #Création d'un Canvas permettant l'affichage de l'image
        Canvas_Bruitage = tk.Canvas(centreDroite, width=matrice_image.shape[0], height=matrice_image.shape[1])
        Canvas_Bruitage.create_image(0, 0, anchor=tk.NW, image=Image_Bruitee)
        Canvas_Bruitage.pack()
        
        #- Cadre du SNR -
        #Exécution de la fonction du SNR
        SNR(matrice_image, matrice_bruitage)
        calcul = tk.LabelFrame(fenetre, text="Calcul du SNR :")
        calcul.pack(padx=20, pady=20)
        #Affichage des résultats du SNR
        tk.Label(calcul, textvariable=puissanceBruit).pack()
        tk.Label(calcul, textvariable=puissanceSignal).pack()
        tk.Label(calcul, textvariable=SNR_).pack()
        
        #- Cadre du bas -
		#Mise en page et affichage du bouton retour
        bas = tk.Frame(fenetre)
        bas.pack(side=tk.BOTTOM, padx=15, pady=15)
        tk.Button(bas, text='Retour', command=fenetre.destroy).pack(side=tk.BOTTOM)
        
        #Boucle de la fenêtre
        fenetre.mainloop()
        

#--- Bruitage Additif ---
def Bruitage_Additif(image,bruitage):
    #Copie de la matrice originale
    image_bruitee = np.copy(image)
    
    #Parcourt de la matrice
    for j in range(image_bruitee.shape[0]):         
        for i in range(image_bruitee.shape[1]):
            #Création de la valeur à affecter à chaque pixel
            t = image_bruitee[j][i] + rdm.gauss(0,bruitage)       #Multiplication de la valeur du pixel avec la variable de gauss (mu,sigma)
            #Affecter la valeur en positif si elle est négative
            if (t) < 0:
                image_bruitee[j][i] = -t
            #Affecter 255 au pixel si il dépasse 255
            if (t) > 255:
                image_bruitee[j][i] = 255
            #Sinon, affecter la valeur au pixel désigné
            else:
                image_bruitee[j][i] = t
    
    #On retourne la matrice modifiée
    return image_bruitee


#--- Fenêtre Bruitage Multiplicatif ---
def Fenetre_Bruitage_Multiplicatif():
    #Sécurité si aucune image n'a été sélectionnée
    if (image_choisie == 0):
        #Lance la fenêtre d'erreur
        Fenetre_Aucune_Image()
    else:
        #Création de la fenêtre fille
        fenetre = tk.Toplevel(fenetrePrincipale)                
        fenetre.title("Bruitage Multiplicatif")
        
        #- Cadre du haut -
        #Mise en page et affichage du texte
        haut = tk.Frame(fenetre, borderwidth=2, relief=tk.GROOVE)
        haut.pack(side=tk.TOP, padx=30, pady=30)
        tk.Label(haut, text="Bruitage d'une image en utilisant la méthode Multiplicative").pack(padx=10, pady=10)
        
        #- Cadre du centre -
        centre = tk.Frame(fenetre)
        centre.pack(fill="both", expand="yes", padx=20)
        
        #- Cadre de gauche -
		#Mise en page et affichage du texte
        centreGauche = tk.Frame(centre, borderwidth=2, relief=tk.GROOVE)
        centreGauche.pack(side=tk.LEFT, fill="both", expand="yes", padx=20)
        tk.Label(centreGauche, text="Image de base", pady=10).pack()
        #Récupération de l'image d'origine
        Image_Reference = ImageTk.PhotoImage(file=CheminAcces)
        #Création d'un Canvas permettant l'affichage de l'image
        Canvas_Reference = tk.Canvas(centreGauche, bg='white', width=matrice_image.shape[0], height=matrice_image.shape[1])
        Canvas_Reference.create_image(0, 0, anchor=tk.NW, image=Image_Reference)
        Canvas_Reference.pack()

		#- Cadre de droite -
		#Mise en page et affichage du texte
        centreDroite = tk.Frame(centre, borderwidth=2, relief=tk.GROOVE)
        centreDroite.pack(side=tk.RIGHT, fill="both", expand="yes", padx=20)
        tk.Label(centreDroite, text="Image bruitée", pady=10).pack()
		#Bruitage et enregistrement de l'image bruitée
        matrice_bruitage = Bruitage_Multiplicatif(matrice_image, Valeur.get())
        imageio.imsave("Image_Bruitee.png", matrice_bruitage)
        Image_Bruitee = ImageTk.PhotoImage(file="Image_Bruitee.png")
		#Création d'un Canvas permettant l'affichage de l'image
        Canvas_Bruitage = tk.Canvas(centreDroite, width=matrice_image.shape[0], height=matrice_image.shape[1])
        Canvas_Bruitage.create_image(0, 0, anchor=tk.NW, image=Image_Bruitee)
        Canvas_Bruitage.pack()
        
		#- Cadre du SNR -
        #Exécution de la fonction du SNR
        SNR(matrice_image, matrice_bruitage)
        calcul = tk.LabelFrame(fenetre, text="Calcul du SNR :")
        calcul.pack(padx=20, pady=20)
        #Affichage des résultats du SNR
        tk.Label(calcul, textvariable=puissanceBruit).pack()
        tk.Label(calcul, textvariable=puissanceSignal).pack()
        tk.Label(calcul, textvariable=SNR_).pack()
        
        #- Cadre du bas -
		#Mise en page et affichage du bouton retour
        bas = tk.Frame(fenetre)
        bas.pack(side=tk.BOTTOM, padx=15, pady=15)
        tk.Button(bas, text='Retour', command=fenetre.destroy).pack(side=tk.BOTTOM)
        
        #Boucle de la fenêtre
        fenetre.mainloop()


#--- Bruitage Multiplicatif ---
def Bruitage_Multiplicatif(image,bruitage):
    #Copie de la matrice originale
    image_bruitee = np.copy(image)
    bruit = bruitage * 0.01         #On initialise une valeur pour avoir le sigma à utiliser, sous 1
    
    #Parcourt de la matrice
    for j in range(image_bruitee.shape[0]):         
        for i in range(image_bruitee.shape[1]):
            #Création de la valeur à affecter à chaque pixel
            t = image_bruitee[j][i] * rdm.gauss(1,bruit)       #Multiplication de la valeur du pixel avec la variable de gauss (mu,sigma)
            #Affecter la valeur en positif si elle est négative
            if (t) < 0:
                image_bruitee[j][i] = -t
            #Affecter 255 au pixel si il dépasse 255
            if (t) > 255:
                image_bruitee[j][i] = 255
            #Sinon, affecter la valeur au pixel désigné
            else:
                image_bruitee[j][i] = t
    
    #On retourne la matrice modifiée
    return image_bruitee


#--- Fenêtre Débruitage Median ---
def Fenetre_Debruitage_Median():
    #Sécurité si aucune image n'a été sélectionnée
    if (image_choisie == 0):
        #Lance la fenêtre d'erreur
        Fenetre_Aucune_Image()
    else:
        #Création de la fenêtre fille
        fenetre = tk.Toplevel(fenetrePrincipale)                
        fenetre.title("Débruitage Median")
        
		#- Cadre du haut -
        #Mise en page et affichage du texte
        haut = tk.Frame(fenetre, borderwidth=2, relief=tk.GROOVE)
        haut.pack(side=tk.TOP, padx=30, pady=30)
        tk.Label(haut, text="Débruitage d'une image en utilisant la méthode Median").pack(padx=10, pady=10)
        
		#- Cadre du centre -
        centre = tk.Frame(fenetre)
        centre.pack(fill="both", expand="yes", padx=20)
        
		#- Cadre de gauche -
		#Mise en page et affichage du texte
        centreGauche = tk.Frame(centre, borderwidth=2, relief=tk.GROOVE)
        centreGauche.pack(side=tk.LEFT, fill="both", expand="yes", padx=20)
        tk.Label(centreGauche, text="Image d'origine", pady=10).pack()
        #Récupération de l'image d'origine
        Image_Reference = ImageTk.PhotoImage(file=CheminAcces)
		#Création d'un Canvas permettant l'affichage de l'image
        Canvas_Reference = tk.Canvas(centreGauche, bg='white', width=matrice_image.shape[0], height=matrice_image.shape[1])
        Canvas_Reference.create_image(0, 0, anchor=tk.NW, image=Image_Reference)
        Canvas_Reference.pack()

		#- Cadre de droite -
		#Mise en page et affichage du texte
        centreDroite = tk.Frame(centre, borderwidth=2, relief=tk.GROOVE)
        centreDroite.pack(side=tk.RIGHT, fill="both", expand="yes", padx=20)
        tk.Label(centreDroite, text="Image Débruitée", pady=10).pack()
        #Débruitage et enregistrement de l'image débruitée 
        matrice_debruitage = Debruitage_Median(matrice_image)
        imageio.imsave("Image_Debruitee.png", matrice_debruitage)
        Image_Debruitee = ImageTk.PhotoImage(file="Image_Debruitee.png")
		#Création d'un Canvas permettant l'affichage de l'image
        Canvas_Bruitage = tk.Canvas(centreDroite, width=matrice_image.shape[0], height=matrice_image.shape[1])
        Canvas_Bruitage.create_image(0, 0, anchor=tk.NW, image=Image_Debruitee)
        Canvas_Bruitage.pack()
        
		#- Cadre du SNR -
        #Exécution de la fonction du SNR
        SNR(matrice_image, matrice_debruitage)
        calcul = tk.LabelFrame(fenetre, text="Calcul du SNR :")
        calcul.pack(padx=20, pady=20)
        #Affichage des résultats du SNR
        tk.Label(calcul, textvariable=puissanceBruit).pack()
        tk.Label(calcul, textvariable=puissanceSignal).pack()
        tk.Label(calcul, textvariable=SNR_).pack()
        
		#- Cadre du bas -
		#Mise en page et affichage du bouton retour
        bas = tk.Frame(fenetre)
        bas.pack(side=tk.BOTTOM, padx=15, pady=15)
        tk.Button(bas, text='Retour', command=fenetre.destroy).pack(side=tk.BOTTOM)
        
        #Boucle de la fenêtre
        fenetre.mainloop()


#--- Débruitage Median ---
def Debruitage_Median(image):
    #Copie de la matrice originale
    image_debruitee = np.copy(image)
    pixel = np.zeros((9))
    
    #Parcourt de la matrice
    for i in range(image_debruitee.shape[0]-1):
        for j in range(image_debruitee.shape[1]-1):
            #Sélectionner chaque pixel en fonction de sa position
            pixel[0] = image_debruitee[i-1,j-1]
            pixel[1] = image_debruitee[i-1,j]
            pixel[2] = image_debruitee[i-1,j+1]
            pixel[3] = image_debruitee[i,j-1]
            pixel[4] = image_debruitee[i,j]
            pixel[5] = image_debruitee[i,j+1]
            pixel[6] = image_debruitee[i+1,j-1]
            pixel[7] = image_debruitee[i+1,j]
            pixel[8] = image_debruitee[i+1,j+1]
            #Trier les pixels
            s = np.sort(pixel)  
            image_debruitee[i,j] = s[4]
    
    #On retourne la matrice modifiée
    return image_debruitee


#--- Fenêtre Débruitage Convulsion ---
def Fenetre_Debruitage_Convolution():
    #Sécurité si aucune image n'a été sélectionnée
    if (image_choisie == 0):
        #Lance la fenêtre d'erreur
        Fenetre_Aucune_Image()
    else:
        #Création de la fenêtre fille
        fenetre = tk.Toplevel(fenetrePrincipale)                
        fenetre.title("Débruitage Convolution")
        
        #- Cadre du haut -
        #Mise en page et affichage du texte
        haut = tk.Frame(fenetre, borderwidth=2, relief=tk.GROOVE)
        haut.pack(side=tk.TOP, padx=30, pady=30)
        tk.Label(haut, text="Débruitage d'une image en utilisant la méthode Convolution").pack(padx=10, pady=10)
        
        #- Cadre du centre -
        centre = tk.Frame(fenetre)
        centre.pack(fill="both", expand="yes", padx=20)
        
        #- Cadre de gauche -
		#Mise en page et affichage du texte
        centreGauche = tk.Frame(centre, borderwidth=2, relief=tk.GROOVE)
        centreGauche.pack(side=tk.LEFT, fill="both", expand="yes", padx=20)
        tk.Label(centreGauche, text="Image d'origine", pady=10).pack()
        #Récupération de l'image d'origine
        Image_Reference = ImageTk.PhotoImage(file=CheminAcces)
		#Création d'un Canvas permettant l'affichage de l'image
        Canvas_Reference = tk.Canvas(centreGauche, bg='white', width=matrice_image.shape[0], height=matrice_image.shape[1])
        Canvas_Reference.create_image(0, 0, anchor=tk.NW, image=Image_Reference)
        Canvas_Reference.pack()

		#- Cadre de droite -
		#Mise en page et affichage du texte
        centreDroite = tk.Frame(centre, borderwidth=2, relief=tk.GROOVE)
        centreDroite.pack(side=tk.RIGHT, fill="both", expand="yes", padx=20)
        tk.Label(centreDroite, text="Image Débruitée", pady=10).pack()
        #Débruitage et enregistrement de l'image débruitée 
        matrice_debruitage = Debruitage_Convolution(matrice_image)
        imageio.imsave("Image_Debruitee.png", matrice_debruitage)
        Image_Debruitee = ImageTk.PhotoImage(file="Image_Debruitee.png")
		#Création d'un Canvas permettant l'affichage de l'image
        Canvas_Bruitage = tk.Canvas(centreDroite, width=matrice_image.shape[0], height=matrice_image.shape[1])
        Canvas_Bruitage.create_image(0, 0, anchor=tk.NW, image=Image_Debruitee)
        Canvas_Bruitage.pack()

		#- Cadre du SNR -
        #Exécution de la fonction du SNR
        SNR(matrice_image, matrice_debruitage)
        calcul = tk.LabelFrame(fenetre, text="Calcul du SNR :")
        calcul.pack(padx=20, pady=20)
        #Affichage des résultats du SNR
        tk.Label(calcul, textvariable=puissanceBruit).pack()
        tk.Label(calcul, textvariable=puissanceSignal).pack()
        tk.Label(calcul, textvariable=SNR_).pack()
        
		#- Cadre du bas -
		#Mise en page et affichage du bouton retour
        bas = tk.Frame(fenetre)
        bas.pack(side=tk.BOTTOM, padx=15, pady=15)
        tk.Button(bas, text='Retour', command=fenetre.destroy).pack(side=tk.BOTTOM)
        
        #Boucle de la fenêtre
        fenetre.mainloop()


#--- Débruitage Convulsion ---
def Debruitage_Convolution(image):
    #Copie de la matrice originale
    image_debruitee = np.copy(image)
    pixel = np.zeros((9))
    
    #Parcourt de la matrice
    for i in range(image_debruitee.shape[0]-1):
        for j in range(image_debruitee.shape[1]-1):
            #Sélectionner chaque pixel en fonction de sa position
            pixel[0] = image_debruitee[i-1,j-1]
            pixel[1] = image_debruitee[i-1,j]
            pixel[2] = image_debruitee[i-1,j+1]
            pixel[3] = image_debruitee[i,j-1]
            pixel[4] = image_debruitee[i,j]
            pixel[5] = image_debruitee[i,j+1]
            pixel[6] = image_debruitee[i+1,j-1]
            pixel[7] = image_debruitee[i+1,j]
            pixel[8] = image_debruitee[i+1,j+1]
            #Moyenne des pixels
            somme = (pixel[0]+pixel[1]+pixel[2]+pixel[3]+pixel[4]+pixel[5]+pixel[6]+pixel[7]+pixel[8])/9
            image_debruitee[i,j] = somme
    
    #On retourne la matrice modifiée
    return image_debruitee
    

#--- Fenêtre Débruitage Kawahara ---
def Fenetre_Debruitage_Kuwahara():
    #Sécurité si aucune image n'a été sélectionnée
    if (image_choisie == 0):
        #Lance la fenêtre d'erreur
        Fenetre_Aucune_Image()
    else:
        #Création de la fenêtre fille
        fenetre = tk.Toplevel(fenetrePrincipale)                
        fenetre.title("Débruitage Kuwahara")
        
        #- Cadre du haut -
        #Mise en page et affichage du texte
        haut = tk.Frame(fenetre, borderwidth=2, relief=tk.GROOVE)
        haut.pack(side=tk.TOP, padx=30, pady=30)
        tk.Label(haut, text="Débruitage d'une image en utilisant la méthode Kuwahara").pack(padx=10, pady=10)
        
        #- Cadre du centre -
        centre = tk.Frame(fenetre)
        centre.pack(fill="both", expand="yes", padx=20)
        
        #- Cadre de gauche -
		#Mise en page et affichage du texte
        centreGauche = tk.Frame(centre, borderwidth=2, relief=tk.GROOVE)
        centreGauche.pack(side=tk.LEFT, fill="both", expand="yes", padx=20)
        tk.Label(centreGauche, text="Image d'origine", pady=10).pack()
        #Récupération de l'image d'origine
        Image_Reference = ImageTk.PhotoImage(file=CheminAcces)
        #Création d'un Canvas permettant l'affichage de l'image
        Canvas_Reference = tk.Canvas(centreGauche, bg='white', width=matrice_image.shape[0], height=matrice_image.shape[1])
        Canvas_Reference.create_image(0, 0, anchor=tk.NW, image=Image_Reference)
        Canvas_Reference.pack()

        #- Cadre de droite -
		#Mise en page et affichage du texte
        centreDroite = tk.Frame(centre, borderwidth=2, relief=tk.GROOVE)
        centreDroite.pack(side=tk.RIGHT, fill="both", expand="yes", padx=20)
        tk.Label(centreDroite, text="Image Débruitée", pady=10).pack()
        #Débruitage et enregistrement de l'image débruitée 
        matrice_debruitage = Debruitage_Kuwahara(matrice_image)
        imageio.imsave("Image_Debruitee.png", matrice_debruitage)
        Image_Debruitee = ImageTk.PhotoImage(file="Image_Debruitee.png")
        #Création d'un Canvas permettant l'affichage de l'image
        Canvas_Bruitage = tk.Canvas(centreDroite, width=matrice_image.shape[0], height=matrice_image.shape[1])
        Canvas_Bruitage.create_image(0, 0, anchor=tk.NW, image=Image_Debruitee)
        Canvas_Bruitage.pack()
        
        #- Cadre du SNR -
        #Exécution de la fonction du SNR
        SNR(matrice_image, matrice_debruitage)
        calcul = tk.LabelFrame(fenetre, text="Calcul du SNR :")
        calcul.pack(padx=20, pady=20)
        #Affichage des résultats du SNR
        tk.Label(calcul, textvariable=puissanceBruit).pack()
        tk.Label(calcul, textvariable=puissanceSignal).pack()
        tk.Label(calcul, textvariable=SNR_).pack()
        
		#- Cadre du bas -
		#Mise en page et affichage du bouton retour
        bas = tk.Frame(fenetre)
        bas.pack(side=tk.BOTTOM, padx=15, pady=15)
        tk.Button(bas, text='Retour', command=fenetre.destroy).pack(side=tk.BOTTOM)
        
        #Boucle de la fenêtre
        fenetre.mainloop()


#--- Débruitage Kuwahara ---
def variance(liste):
    #Déclaration des variables locales
    t=0
    m=(sum(liste)/len(liste))**2
    
    #Parcourt de la liste
    for i in range(len(liste)):
        t+=(liste[i]-m)**2
    
    #Retourne la variance
    return t/len(liste)


def Debruitage_Kuwahara(image):
    #Copie de la matrice originale
    image_debruitee = np.copy(image)
    #Déclaration des variables locales
    z1 = []
    z2 = []
    z3 = []
    z4 = []

    #Parcourt de la matrice
    for i in range(0,image_debruitee.shape[0]):
        for j in range(0,image_debruitee.shape[1]):
            for i1 in range(i-2,i+1):
                for j1 in range(j-2,j+1):
                    if not(i1 < 0 or i1 >= image.shape[0] or j1 < 0 or j1 >= image.shape[1]):
                        z1.append(image_debruitee[i1,j1])
            for i1 in range(i-2,i+1):
                for j1 in range(j,j+3):
                    if not(i1 < 0 or i1 >= image.shape[0] or j1 < 0 or j1 >= image.shape[1]):
                        z2.append(image_debruitee[i1,j1])
            for i1 in range(i,i+3):
                for j1 in range(j-2,j+1):
                    if not(i1 < 0 or i1 >= image.shape[0] or j1 < 0 or j1 >= image.shape[1]):
                        z3.append(image_debruitee[i1,j1])
            for i1 in range(i,i+3):
                for j1 in range(j,j+3):
                    if not(i1 < 0 or i1 >= image.shape[0] or j1 < 0 or j1 >= image.shape[1]):
                        z4.append(image_debruitee[i1,j1])
            
            #Calcul de la variance
            variances = []
            variances.append(variance(z1))
            variances.append(variance(z2))
            variances.append(variance(z3))
            variances.append(variance(z4))
            index_variance_min = variances.index(min(variances))
            if (index_variance_min == 0):
                image_debruitee[i,j] = sum(z1) / len(z1)
            elif (index_variance_min == 1):
                image_debruitee[i,j] = sum(z2) / len(z2)
            elif (index_variance_min == 2):
                image_debruitee[i,j] = sum(z3) / len(z3)
            elif (index_variance_min == 3):
                image_debruitee[i,j] = sum(z4) / len(z4)
            
            #Réinitialisation des variables locales
            z1 = []
            z2 = []
            z3 = []
            z4 = []

    #On retourne la matrice modifiée
    return image_debruitee


#--- Calcul du SNR ---
def SNR(image, image_bruitee):
    #Importation des variables globales
    global puissanceBruit
    global puissanceSignal
    global SNR_
    
    #Définition des variables locales
    P_bruit = 0.0
    P_signal = 0.0
    _snr = 0.0
    
    #Parcours de l'image
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            P_signal = P_signal + image[i,j] ** 2
            P_bruit = P_bruit + (image_bruitee[i,j] - image[i,j]) ** 2     #Puissance du bruit = image bruité - image de base
    
    #Calcul du SNR
    _snr = 10 * np.log(P_signal/P_bruit)
    
    #Modification du texte dans la fenêtre principale
    puissanceBruit.set("Puissance du bruit : "+str(float(P_bruit)))
    puissanceSignal.set("Puissance du signal : "+str(float(P_signal)))
    SNR_.set("SNR : "+str(float(_snr)))


#--- Menu Principal ---
#Création de la fenêtre principale
fenetrePrincipale = tk.Tk()
fenetrePrincipale.title('Algorithme de Bruitage et Débruitage')
fenetrePrincipale.geometry('800x640')

#- Cadre du haut -
#Mise en page et affichage du texte
haut = tk.Frame(fenetrePrincipale, borderwidth=2, relief=tk.GROOVE)
haut.pack(side=tk.TOP, padx=30, pady=30)
tk.Label(haut, text="Algorithme Python de bruitage et de débruitage d'une image avec calcul du SRN.\n Auteurs : David BALLARD, Mathis SERRIERES MANIECKI").pack(padx=10, pady=10)

#- Cadre de sélection de l'image -
#Mise en page et affichage du texte
selection = tk.Frame(fenetrePrincipale, relief=tk.GROOVE)
selection.pack(side=tk.TOP, padx=5, pady=5)
tk.Label(selection, text="Image sélectionnée :").pack()
#Texte affecté au chemin d'accès du fichier sélectionné
Chemin_Acces_Texte = tk.Label(selection, text="Aucune image sélectionnée.", pady=5)
Chemin_Acces_Texte.pack()
#Bouton de sélection de l'image
tk.Button(selection, text ='Sélectionner une image', command = Fenetre_Selection_IMG).pack(side = tk.BOTTOM)

#- Cadre du centre -
centre = tk.Frame(fenetrePrincipale, relief=tk.GROOVE)
centre.pack(side=tk.TOP, fill="both", expand="yes", padx=20)

#- Cadre de gauche -
#Mise en page et affichage du texte et des différents boutons
centreGauche = tk.Frame(centre, borderwidth=2, relief=tk.GROOVE)
centreGauche.pack(side=tk.LEFT, fill="both", expand="yes", padx=15, pady=15)
tk.Label(centreGauche, text="Algorithme de Bruitage\n", pady=15).pack()
tk.Button(centreGauche, text ='Bruitage Poivre et Sel', command = Fenetre_Bruitage_PoivreSel).pack(pady = 10)
tk.Button(centreGauche, text ='Bruitage Additif', command = Fenetre_Bruitage_Additif).pack(pady = 10)
tk.Button(centreGauche, text ='Bruitage Multiplicatif', command = Fenetre_Bruitage_Multiplicatif).pack(pady = 10)
#Création d'une variable permettant de choisir le taux de bruitage appliqué
Valeur = tk.IntVar()
Valeur.set(30)
boite = tk.Spinbox(centreGauche,from_=0,to=100,increment=1,textvariable=Valeur,width=5)
boite.pack(side=tk.BOTTOM, padx=30 , pady=10)
tk.Label(centreGauche, text="\nNiveau de bruitage :").pack()

#- Cadre de droite -
#Mise en page et affichage du texte et des différents boutons
centreDroite = tk.Frame(centre, borderwidth=2, relief=tk.GROOVE)
centreDroite.pack(side=tk.RIGHT, fill="both", expand="yes", padx=15, pady=15)
tk.Label(centreDroite, text="Algorithme de Débruitage\n", pady=15).pack()
tk.Button(centreDroite, text ='Débruitage Médian', command = Fenetre_Debruitage_Median).pack(pady = 10)
tk.Button(centreDroite, text ='Débruitage Convolution', command = Fenetre_Debruitage_Convolution).pack(pady = 10)
tk.Button(centreDroite, text ='Débruitage Kuwahara', command = Fenetre_Debruitage_Kuwahara).pack(pady = 10)

#- Cadre du bas -
#Mise en page et affichage du bouton quitter
bas = tk.Frame(fenetrePrincipale)
bas.pack(side=tk.BOTTOM, padx=30, pady=30)
tk.Button(bas, text="Quitter", command=fenetrePrincipale.destroy).pack(side=tk.BOTTOM, pady=20)

#Définition des variables dynamiques pour Tkinter
puissanceBruit = tk.StringVar()
puissanceSignal = tk.StringVar()
SNR_ = tk.StringVar()

#Boucle de la fenêtre
fenetrePrincipale.mainloop()