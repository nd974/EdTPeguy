## Importations

    # module Tkinter et ses collections
from tkinter import *
from tkinter.messagebox import *

    # module de données tabulaires
import csv

    # module qui permet de lancer de nouveaux processus
from subprocess import call

    # Methode pour importer les objets 'Etablissement' et 'Eleve'
from Choisir_ses_cours import Etablissement,Eleve

## Manipulations pour la suite du programme 

# Nouvelle Affectation de la class 'Etablissement' 
mon_etablissement = Etablissement()

# exemple d'un eleve de l'Etablissement >>> a ameliorer cf "TODO"
nicolas = Eleve('nicolas','dolphin','Nicolas','Dolphin','Terminale', 'S', 'spe_ISN')

# Manipulation de CSV(Comma-separated values)
with open('csv/subject.csv', newline='') as csvfile:#ouverture du fivhier csv
    reader = csv.DictReader(csvfile)#creation un variable qui permet de lire le  csv pour acceder au donnees  
    for row in reader:#lecture en ligne du fichier
        mon_etablissement.ajout_matiere(row['Classe'],row['Filiere'],row['Specialite'],row['Matieres'],int(row['Heures']))

## Tkinter (GUI)

# Création de la fenêtre principale (ELEVE)
ELEVE=Tk()

#Cadre pour le titre 'Emploi du temps'
LB1=LabelFrame(ELEVE)
LB1.pack(fill= BOTH, expand= "yes")

#Titre 'Emploi du temps'
titre1=Label(LB1,text='EMPLOI DU TEMPS',fg='red',font='size 22')
titre1.pack(fill=BOTH,expand='yes',side=BOTTOM)

#Cadre contenant la structure de l'emploi du temps
LB2=LabelFrame(ELEVE)
LB2.pack(fill= BOTH, expand= "yes")

# Affichage (bouton pour les bordures) des jours de la semaine 'Lundi,Mardi,...'
journée = ['Lundi','Mardi','Mercredi','Jeudi','Vendredi']
for jour,ligne in zip(journée,range(5)):
    jours = Button(LB2,text=jour,width=35,state=DISABLED,disabledforeground='black')
    jours.grid(row=0,column=ligne+1)

# Affichage (bouton pour les bordures) des heures par jour '8h,9h,...'
for m in range(11):
    k=8
    heures=Button(LB2, text=str(k+m), width=10,height=2,state=DISABLED,disabledforeground='black')
    heures.grid(row=m+1,column=0,sticky=NSEW)
    
# Creation des bouttons pour remplir l'emploi du temps
for ligne in range(11):# sur les 11h de travail et
    for colone in range(5): # sur les 5 jours de travail
        #Remplissage
        e = Button(LB2)
        e.grid(row=ligne+1, column=colone+1, sticky=NSEW)
        e.config(command = lambda p=e :choix_etudes(p))

# Creation d'un boutton pour valider l'emploi du temps a certaines condition 
FIN_edt=Button(LB2,height=30,width=30,bitmap='@images/confirme.xbm',bd=5,fg='green')
FIN_edt.config(command=lambda:Validation_edt())

#Creation d'un boutton pour supprimer les cours inscrit precedement dans l'emploi du temps
Suppr=Button(LB2,height=30,width=30,bitmap='@images/croix_rouge.xbm',bd=5,fg='red')
Suppr.config(command=lambda:Supprimer())

## Fonctions principale

def Supprimer() :
    '''
    Cette fonction demande a l'utilisateur si il veut supprimer les cours inscrit precedement dans l'emploi du temps
    >>> si oui alors la page ELEVE se detruit son avoir inscrit l'Eleve et colle ce meme programme 'Eleve.py' vierge pour recommencer 
    >>> si non rien ne ce passe
    '''
    if askyesno("", "  Voulez vous vraiment supprimer les cours que vous avez mis ?"):
        ELEVE.destroy()
        call('python Eleve.py')

def choix_etudes(e):
    '''
    Cette fonction se declenche lors de l'appui du bouton principale qui correspond a l'heure et le jour choisis 
    '''
    
    def clic(evt):
        '''
        Ce gestionnaire d'Event se declenche lors du choix de la matiere dans la ListBox principale qui correspond 
        a l'heure et le jour choisis 
        '''
        # Creation d'une entree qui contiendra le choix de la matiere  
        matiere_choisi=Entry(e)
        matiere_choisi.pack(fill=BOTH,expand=YES,side=LEFT)
            
        # Manipulation de la liste des matieres 
        index = choix.curselection()[0]
        seltext = choix.get(index)
            
        # Insertion de la matiere dans l'entree cree precedemment
        matiere_choisi.insert(0,seltext)
        
        # Enleve une heure de la semaine de la matiere 
        nicolas.prendre_cours(seltext,1)
            
        # Destruction de la liste des matiere et de la barre de defilement 
        choix.destroy()
        yscroll.destroy()
        
        # Configuration de l'entrée de la matiere choisis (affichage)
        matiere_choisi.config(state=DISABLED,disabledforeground='black')
                 
        # Affichage du boutton pour supprimer les cours inscrit precedement dans l'emploi du temps
        Suppr.grid(row=12,column=3)
    
    # Pour eviter les beug le bouton ne pouras pas etre reappuyer 
    e.config(state=DISABLED)
    
    # Creation de la ListBox de l'eleve a prendre et d'une barre de defillement 
    choix=Listbox(e,height=1)
    yscroll = Scrollbar(e,command=choix.yview, orient=VERTICAL)
    yscroll.pack(side=RIGHT,fill=Y)
    choix.pack(fill=BOTH,expand=YES)
    
    # Necessaire pour que la barre de defillement soit complementaire avec la ListBox
    choix.configure(yscrollcommand=yscroll.set)
    
    # Remplisage de la ListBox avec les matieres que l'eleve doit prendre 
    for w in mon_etablissement.matiere_restantes(nicolas):
        choix.insert(END,str(w))
        choix.bind('<ButtonRelease-1>',clic)# Creation d'un Evenement lors du choix de la matiere --> VOIR L'EVENEMENT DE LA FONCTION choix()
        
    # Si je n'ai plus de matieres
    if  mon_etablissement.matiere_restantes(nicolas) == {}:
        
        # Detruit la liste de selection (vide) et ma barre de défilement verticale 
        choix.destroy()
        yscroll.destroy()
        
        # Affiche les bouton pour achever mon emploi du temps 
        FIN_edt.grid(row=12,column=4)
        Suppr.grid(row=12,column=2)

def Validation_edt():
    '''
    Cette fonction demande a l'eleve 2 fois si il accepte d'etre inscrit au cours qu'il a renseignée 
    >>> si oui la fonction inscrit l'eleve a ces cours et ferme le programme
    >>> sinon il doit recommencer depuis le debut le programme detruit la page et la reactualise 
    '''
    if askyesno('',"Es ce que cet emploi du temps vous convient?"):
        if askyesno('','''     Vous ne pourez pas vous désinscire a ces cours 
            Etes vous sure de vous inscire  ?'''):
            showinfo("", '''  Merci de votre insciption !
            Bon cours!''')
            ELEVE.destroy()
        else :
            showinfo("", "  Veuillez inscrire vous cours dans les emplacement !")
            ELEVE.destroy()
            call('python3 Eleve.py')
    else :
        showinfo("", "  Veuillez inscrire vous cours dans les emplacement !")
        ELEVE.destroy()
        call('python3 Eleve.py')

## Lancement

if __name__ !=  '__main__':
    #Dans le cas où ce module a etait importé depuis un autre programme, cette partie du code se lance.
    ELEVE.mainloop()