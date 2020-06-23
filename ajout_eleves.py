## Imports

 # Tabular Data Module
import csv

# Module that imports an object from another program 
from Choisir_ses_cours import Etablissement

# Module to represent structured information
import json

# Module for encoding user data
import base64

# Module that encrypts and decrypts a file
import hashlib

## Manipulations for the rest of the program

# New assignment of the class ' Etablissement '
mon_etablissement = Etablissement()

# Manipulation de CSV(Comma-separated values)
with open('csv/subject.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)  
    for row in reader:
        mon_etablissement.ajout_matiere(row['Classe'],row['Filiere'],row['Specialite'],row['Matieres'],int(row['Heures']))

## Functions Main

def get_classroom_option(collection):
    '''
    The function allows to create a script of the collection--> function in the establishment class
    '''
    # This function launches if the collection is not empty 
    if len(collection):
        # Creating a Dictioanire with the choices of the numbered collection of 1 a Len (collection)
        mapping = {str(i): d for i, d in zip(range(1,len(collection) + 1), collection)}
        # Dictionary Fill 
        for i, d in mapping.items():
            # Displays the number of choices  
            print('{}:{}'.format(i, d))
        # Ask the user to make a electing between the numbers (i)
        data = input('Your choice?')
        # as long as the choice is differrent of the total number (i)
        while data not in mapping:
            # The program Ask the selected choice 
            data = input('Incorrect data-what is your choice?')
        # returns the additional choice of numbers
        return mapping[data]
    # If the collection is empty then 
    else:
        # Return 'Aucune'
        return 'Nothing'

def add_users():
    '''
    This function allows you to create a new user 
    '''
    # Cette variable correspond à l'identifiant de l'utilisateur
    login = input('Id : ')
    # This variable is the user's password
    password = input('Password : ')
    # This variable is the first name of the user
    name = input('Name ? ')
    # This variable is the name of the user
    surname = input('Surname ? ')
    print('''
What year is it?''')
    # This variable is the user's class
    classe = get_classroom_option(mon_etablissement.liste_classes())
    print('''
What's his section ?''')
    # This variable corresponds to the user's die
    filiere = get_classroom_option(mon_etablissement.liste_filiere(classe))
    print('''
What is his specialty ? ''')
    # This variable corresponds to the speciality of the user
    specialite = get_classroom_option(mon_etablissement.liste_specialite(classe, filiere))
    
    # This variable corresponds to the database (base64, JSON) of the user's work
    data = base64.b64encode(bytearray(json.dumps(classe,filiere,specialite), 'utf-8'))
    
    # This manuipulation encrypts the user's password 
    password = encode_password(password)
    print('''
The new Pupil's ID '{} {}' is {} and its password is {}(Coded in md5 hashlib)'''.format(name,surname,login,password))
    # This writes to a CSV file thanks to an intermediate fihier
    with open('csv/user.csv' , 'a' , newline='') as csv_file:
        c = csv.writer(csv_file)
        # Populating the CSV
        c.writerow([login, password, name, surname,data])

def encode_password(cle):
    '''
    This function allows to encrypt the password (aesthetic)
    '''
    c = hashlib.md5()
    c.update(bytearray(cle, 'utf-8'))
    return c.hexdigest()
    
## Test

test=input('Test?(y/n): ')
if test == 'y':
    print('---------------------------TEST---------------------------------')
    
    print("The encryption of 'Nicolas' is  " ,encode_password('Nicolas'))
    print(get_classroom_option([]))
    print(get_classroom_option(['Apple', 'Pear', 'Banana', 'Strawberry']))
    
    print('------------------------End of Test-----------------------------------')
    
## Launch

if __name__ == '__main__':
    # Launch Main function 
    add_users()
