import random
import os
import subprocess
import shutil
import keyring
from cryptography.fernet import Fernet

hidden_path = os.path.expanduser('~/.ballerina')
service_name = 'ballerina_pass'
key_name = 'pass_key'

def intro():
    r"""
.-. .-')     ('-.                           ('-.  _  .-')               .-') _    ('-.     
\  ( OO )   ( OO ).-.                      _(  OO)( \( -O )             ( OO ) )  ( OO ).-. 
 ;-----.\   / . --. / ,--.      ,--.     (,------.,------.  ,-.-') ,--./ ,--,'   / . --. / 
 | .-.  |   | \-.  \  |  |.-')  |  |.-')  |  .---'|   /`. ' |  |OO)|   \ |  |\   | \-.  \  
 | '-' /_).-'-'  |  | |  | OO ) |  | OO ) |  |    |  /  | | |  |  \|    \|  | ).-'-'  |  | 
 | .-. `.  \| |_.'  | |  |`-' | |  |`-' |(|  '--. |  |_.' | |  |(_/|  .     |/  \| |_.'  | 
 | |  \  |  |  .-.  |(|  '---.'(|  '---.' |  .--' |  .  '.',|  |_.'|  |\    |    |  .-.  | 
 | '--'  /  |  | |  | |      |  |      |  |  `---.|  |\  \(_|  |   |  | \   |    |  | |  | 
 `------'   `--' `--' `------'  `------'  `------'`--' '--' `--'   `--'  `--'    `--' `--' 

=====================================================================
Welcome to Ballerina - Your Sock Puppet and General Password Manager!
=====================================================================
Version: 1.0.0
Developer: Decoder Linux
License: MIT
Description: Generate and securely store passwords with ease :)
=====================================================================

"""
    print(intro.__doc__)

def generate_seckey():
    """
    This is to generate an encryption key that is unique for the machine.
    It detects the first run and generates the key.
    This ensures passwords remain safe. It cannot be moved to another machine
    """
    print('No existing key found!')
    print('Generating key for this machine.....')
    key_sec = Fernet.generate_key()
    keyring.set_password(service_name,key_name,key_sec.decode())
    print('Key Generated')
    print()

def generate_password(length):
    """
    This suggests user's strong password based on the given preferrences.
    """
    template = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$*+=()%&'
    upass = ''
    for n in range(1,length+1):
        temp_chr = random.choice(template)
        upass += temp_chr
    return upass

def clear_database():
    """
    This clears user's database on request of user
    """
    try:
        hidden_path = os.path.expanduser('~/.ballerina')
        shutil.rmtree(hidden_path)
        ask = input('Do you want to clear the key (y/n): ')
        if ask == 'y':
            key = keyring.get_password(service_name,key_name)
            if key:
                keyring.delete_password(service_name,key_name)
            else:
                print('No existing key found!')
        print('Database cleared..')
    except FileNotFoundError or Exception as e:
        print('No records found.Clearing error.')

def load_key():
    """
    This loads the key saved in the particular machine.
    This function plays very important role for encryption and decryption process.
    """
    key = keyring.get_password(service_name,key_name)
    return key

def show_usrs():
    """
    This retrives the saved users and displays.
    This is for knowing the profiles already saved.
    Users can select one among the displayed
    """
    path_2_usrs = os.path.join(hidden_path,'users')
    with open(path_2_usrs,'r') as user_f:
        lines = user_f.readlines()
    print('Stored Users:')
    for usr in lines:
        print(usr.strip())

def encrypt_and_service(name,service,passw_data):
    """
    After Suggesting a strong password, this encrypts and stores it.
    This saves the encrypted password.
    """
    #create safedir
    hidden_path = os.path.expanduser('~/.ballerina')
    os.makedirs(hidden_path,exist_ok=True)
    path_2_pass = os.path.join(hidden_path,name)
    path_2_ser = os.path.join(hidden_path,f'{name} ser')
    path_2_usrs = os.path.join(hidden_path,'users')
    #Load key and pass
    key = load_key()
    fernet_en = Fernet(key)
    #Encrypt key
    encrypted_data = fernet_en.encrypt(passw_data.encode())
    with open(path_2_pass,'ab') as pass_file:
        pass_file.write(encrypted_data + b'\n')
    with open(path_2_ser,'a') as ser_file:
        ser_file.write(f'{service}\n')
    with open(path_2_usrs,'a') as usrs_f:
        with open(path_2_usrs,'r') as r_u:
            checks = r_u.readlines()
        if f'{name}\n' not in checks:
            usrs_f.write(f'{name}\n')
    print('Stored in Database....\n')

def decrypt(name):
    """
    This is used for decrypting the stored credentials.
    This also displays them after decryption.
    """
    #open the files
    path_2_pass = os.path.join(hidden_path,name)
    path_2_ser = os.path.join(hidden_path,f'{name} ser')
    path_2_usrs = os.path.join(hidden_path,'users')
    with open(path_2_ser,'r') as service_pre:
        ser_lines = service_pre.readlines()
    #Load key and pass
    key = load_key()
    fernet_dec = Fernet(key)
    #Read file
    with open(path_2_pass,'rb') as pass_file:
        pass_lines = pass_file.readlines()
    print(f'{name}\'s Credentials')
    print('Service  Password')
    for servicess,encrypted_data in zip(ser_lines,pass_lines):
        decrypted_data = fernet_dec.decrypt(encrypted_data.strip()).decode()
        dec_ser = servicess.strip()
        print(f'{dec_ser} : {decrypted_data}')
        
def main():
    """
    It holds the branches.
    It is the motherboard of this program.
    """
    intro()
    #Checking for the key
    key = load_key()
    if not key:
        generate_seckey()
    while True:
        #Ask for user's input
        print('1) Add User\n2) Display Credentials\n3) Clear Database\n4) Exit\n')
        choice = int(input('rina: '))
        match choice:
            case 1:
                print()
                print('1) New user\n2) Add service to existing user')
                print()
                cr_choice = int(input('rina: '))
                if cr_choice == 1: 
                    print('\nData Entry')                
                    name = input('Enter username: ')
                    service = input('Enter service: ')
                    length = int(input('Enter Password Length: '))
                    print()
                    password = generate_password(length)
                    print(f'Your Password: {password}\n')
                    encrypt_and_service(name,service,password)
                    print()              
                elif cr_choice == 2:
                    print()
                    show_usrs()                   
                    name_here = input('\nSelect User: ')
                    ser = input('Enter Service: ')
                    leng = int(input('Enter Password Length: '))                  
                    password_h = generate_password(leng)
                    print(f'\nYour Password: {password_h}')
                    encrypt_and_service(name_here,ser,password_h)
                    print()           
            case 2:
                try:
                    subprocess.run(['sudo','-v'],check=True)
                    print()
                    show_usrs()
                    print()
                    print('\nEnter Users to show their creds...')
                    print()
                    user_name = input('Username: ')
                    print()
                    decrypt(user_name)
                    print()
                except subprocess.CalledProcessError:
                    print('Authentication failed.Please try again')
                    exit(1)  
                except FileNotFoundError:
                    print('Database empty.Create some....')
                    print()
            case 3:
                clear_database()
                break
            case 4:
                print('\nBye Bye!!')
                break



if __name__ == '__main__':
    main()
