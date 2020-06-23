## Imports

    # Module Tkinter (GUI) and its collections
from tkinter import *
from tkinter.messagebox import *

    # Module that encrypts and decrypts a file
import hashlib

    # Tabular Data Module
import csv

    # Module that allows you to launch new processes
from subprocess import call

    # Module to create tuple subclasses with named fields
from collections import namedtuple

## Manipulations for the rest of the program 

# Create a nametuple to assign the CSV ' user ' entries in a dictionary
USER = namedtuple('USER', 'login,password,firstname,lastname,data')
    
def user_login():
    '''
        This function reads and the CSV ' user ' information
        and returns the sets of input thanks to a nametuple (USER)
    '''
    users = list()
    with open('csv/user.csv', 'r') as eleves_csv:
        reader = csv.DictReader(eleves_csv)
        for row in reader:
             file=USER(row['login'],row['password'], row['firstname'], row['lastname'], row['data'])
             users.append(file)
    return users

# Create a dictionary that includes the Identifaint and the additional passwords (identifiers) of all students in the establishment
dictionaire_identification={}

for e in user_login():
    # Fill Dictionary creates precede
    dictionaire_identification[e.login]=(e.password)
    
## Tkinter (GUI) 

# Creating the main window (IDENTIFICATION)
IDENTIFICATION = Tk()

# Fenetre of the identifier
Label1=Label(IDENTIFICATION)
Label1.pack(fill= BOTH, expand= 'yes')

# Password Fenetre
Label2=Label(IDENTIFICATION)
Label2.pack(fill= BOTH, expand= 'yes')

# Create of the two varibles-string-corresponding to the input of logins and passwords
v1=StringVar()# -> identifier
v2=StringVar()# -> password

# Creating an Entry widget (input field, ' identifier ')
entry1=Entry(Label1,textvariable= v1)
entry1.pack(side=BOTTOM)

# Creating a Label Widget (text ' identifier ')
identifiant=Label(Label1,text='Identifiant',width=22)
identifiant.pack(fill=X,side=BOTTOM)

# Separate 1 for view
Label3=Label(Label2)
Label3.pack(fill= BOTH, expand= 'yes',side=LEFT)

# Separate 2 for view
Label4=Label(Label2)
Label4.pack(fill= BOTH, expand= 'yes',side=LEFT)

# Creating a Label widget (text ' password ')
mdp=Label(Label4,text='    Mot de passe')
mdp.grid(row=0, column=2)

# Creating an Entry widget (input field, ' password ')
entry2=Entry(Label4,textvariable= v2,show='*',width=17)
entry2.grid(row=1, column=2)

# Password View button
oeil=Button(Label4,bitmap='@images/oeil_affichage.xbm',height=15,width=15)
oeil.config(command=lambda:visualisation())
oeil.grid(row=1, column=20)

# Label showing a picture of a user's icon 
icone=Label(Label1,width=100,height=100,bitmap='@images/icone.xbm',fg='blue')  
icone.pack(side=BOTTOM)

# Creating a button widget (connect button)
bouton=Button(Label4,text='CONNEXION',bg='black',fg='white')
bouton.config(command=lambda:confirmation())
bouton.grid(row=2,column=2,columnspan=20)

## Functions Main 

def confirmation():
    '''
        This function retrieves the idenfiant and password
        To see if the input matches the key (ID)
        and values (password) of the dictionaries (dictionaire_identification)
        = > The password is good: Following his profession a new program launches
        = > The password is incorrect: Access is denied
    '''
    
    # No input = > Access refuses
    if v1.get() == '' or v2.get() == '':
        showerror('ERROR', '''             No seizures!!
        Please enter an entry ''' )
        
    # Id = False = > Access Denied
    elif v1.get() not in dictionaire_identification.keys():
        showerror('ERROR', '  The identifier is incorrect !')

    # Password = False = > Access Denied
    elif encode_password(v2.get()) not in dictionaire_identification[v1.get()]:
        showerror('ERROR', ' The password is incorrect !')
        
    # Username and password = True = > Access allowed
    else:
        IDENTIFICATION.destroy()
        import Eleve
            
def encode_password(cle):
    '''
        This function encodes in MD5 thanks to the Hashlib module the password input 2
    '''
    
    e = hashlib.md5()
    e.update(bytearray(cle,'utf-8'))
    return e.hexdigest()
    
## Functions (secondary) for Aesthetic 

def visualisation():
    '''
        This function displays LAGT seizure of the password
    '''
    
    entry2.config(show='')
    oeil.config(command=lambda:masque(),bitmap='@images/oeil_desaffichage.xbm')

def masque():
    '''
        This function hides the password seizure
    '''
    
    entry2.config(show='*')
    oeil.config(command=lambda:visualisation(),bitmap='@images/oeil_affichage.xbm')
    
## Test
test=input('Test?(y/n): ')
if test == 'y':
    print('---------------------------TEST---------------------------------')
    
    print(dictionaire_identification)
    print("The encryption of 'Nicolas' is  " ,encode_password('Nicolas'))
    
    print('------------------------End of Test-----------------------------------')
    
## Launch
if __name__ == '__main__':
    # Launch of the main window (IDENTIFICATION)
    IDENTIFICATION.mainloop()
    