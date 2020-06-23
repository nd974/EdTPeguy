#----------------------------------------------------------------------------------------------------------------------------------
# Name:       (L'Emploi du temps.py)
# Purpose:    (Creation du propre emploi du temps de l'eleve pour une meilleur autonomie et education)
#
# Author:     Nicolas Dolphin , Theo Sylvestre , Theo Letan 
#
# Created:    12/12/2017
#----------------------------------------------------------------------------------------------------------------------------------

"""
    Le module suivant est 
"""

## Imports

    # Tabular Data Module
import csv

## The Classes

# First Class
class Etablissement:
    
    def __init__(self):
        '''
        Initialization of the establishment
        '''
        self.lesclasses = {}
        
    def ajout_matiere(self, classe, filiere, specialite, matiere, nb_heures):
        '''
        This function orders to put the class the dies and speciliate in the keys of the dictionary  and to put the materials 
        and the hours in a new dictionary  in the value of the main dictionary 
        '''
        tuple = classe, filiere, specialite
        if tuple not in self.lesclasses:
            self.lesclasses[tuple] = {}
        self.lesclasses[tuple][matiere] = nb_heures
        
    def liste_classes(self):
        '''
        This function returns the list of Classes of the establishment
        '''
        myset = set()
        for key in self.lesclasses:
            myset.add(key[0])
        return list(myset)

    def liste_filiere(self,classe):
        '''
        This function returns the list of die specific to the selected class
        '''
        myset = set()
        for key in self.lesclasses:
            if key[0]==classe:
                myset.add(key[1])
        return list(myset)
        
    def liste_specialite(self,classe,filiere):
        '''
        This function returns the list of specialties specific to the class and the selected die
        '''
        myset = set()
        for key in self.lesclasses:
            if (key[0],key[1])==(classe,filiere):
                myset.add(key[2])
        return list(myset)
    
    def liste_matiere(self,classe,filiere,specialite):
        '''
        This function returns the list of materials specific to the class, the die and the selected specialty
        '''
        tuple = classe, filiere, specialite 
        return list(self.lesclasses[tuple].keys())    
        
    def nb_heures_par_matiere(self,classe,filiere,specialite,matiere):
        '''
        This function returns the total time of a selected material
        '''
        tuple = classe, filiere, specialite
        return self.lesclasses[tuple][matiere]
    
    def matiere_restantes(self,eleve):
        '''
        This function returns in a new dictionary the remaining materials/hours for a pupil gives
        '''
        return {m: h for m, h in self.lesclasses[eleve.classe, eleve.filiere, eleve.specialite].items() if (m not in eleve.cours or h > eleve.cours[m])}
        
# Second Class
class Eleve:
    def __init__(self,id,mdp,prenom,nom,classe, filiere, specilialite):
        '''
        Pupil initialization
        '''
        self.id = id
        self.mdp = mdp
        self.prenom = prenom
        self.nom = nom
        self.classe = classe
        self.filiere = filiere
        self.specialite = specilialite
        self.cours={}

    def prendre_cours(self,matiere, heures):        
        '''
        This function orders a pupil to take 'h' hours of material 
        '''
        if matiere not in self.cours:
            self.cours[matiere] = 0
        self.cours[matiere] += heures

##TEST
if __name__=='__main__':
    test=input('Test?(y/n): ')
    if test == 'y':
        # New assignment of the class ' Etablissement ' 
        mon_etablissement = Etablissement()
                
        #----------------------------------------------------Example of a pupil of the establishment--------------------------------------------------
        nicolas = Eleve('nicolas.dolphin','grilsua4','Nicolas','Dolphin','Terminale', 'S', 'spe_ISN')
        #---------------------------------------------------------------------------------------------------------------------------------------------
        
        #------------------------------------------------Manipulation of CSV(Comma-separated values)--------------------------------------------------
        with open('csv/subject.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile) 
            for row in reader:
                mon_etablissement.ajout_matiere(row['Classe'],row['Filiere'],row['Specialite'],row['Matieres'],int(row['Heures']))
        #--------------------------------------------------------------------------------------------------------------------------------------------
        
        #--------------------------------------------------------------Etablissement(class)-----------------------------------------------------------
        print(mon_etablissement.liste_classes())
        print(mon_etablissement.liste_filiere('Terminale'))
        print(mon_etablissement.liste_specialite('Terminale','S'))
        print(mon_etablissement.liste_matiere('Terminale','S','spe_ISN'))
        print(mon_etablissement.nb_heures_par_matiere('Terminale','S','spe_ISN','Maths'))
        print(mon_etablissement.matiere_restantes(nicolas))
        #---------------------------------------------------------------------------------------------------------------------------------------------
        
        #------------------------------------------------------------------Eleve(class)-----------------------------------------------------------
        nicolas.prendre_cours('Maths', 6)   
        print(mon_etablissement.matiere_restantes(nicolas))
        #---------------------------------------------------------------------------------------------------------------------------------------------