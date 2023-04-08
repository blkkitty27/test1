# Importing key encyrption algorithm
# Import cryptography through cmd using pip command
import subprocess
import sys
subprocess.check_call([sys.executable, "-m", "pip", "install" , "cryptography"])
from cryptography.fernet import Fernet

# Create password manager class
class PasswordManager:
        # Create constructor to assign multiple values when class is called, key, password, password_dict
        def __init__(self):
            self.key = None
            self.password_file = None
            self.password_dict = {}
            
        # Create key using fernet algorithm for storage and access
        def create_key(self, path):
            self.key = Fernet.generate_key()
            # Store key in file(f=path as written by user),'wb'=writingbytes mode
            with open(path, 'wb') as f:
                f.write(self.key)
                
        # Function for loading the key
        def load_key(self,path):
            with open(path, 'rb') as f:
                self.key = f.read()

        # Function for creating password file        
        def create_password_file(self,path, initial_values=None):
            self.password_file = path
            # Add user input to file 
            if initial_values is not None:
                for key, value in initial_values.items():
                    self.add_password(key, value)

        # Function for loading existing password file
        def load_password_file(self, path):
            self.password_file = path
            # Open path in reading mode and define as 'f'
            with open(path, 'r') as f:
                #decrypt line by line as in f where f is password file using : as split identifier
                for line in f:
                    site, encrypted = line.split(":")
                    self.password_dict[site] = Fernet(self.key).decrypt(encrypted.encode()).decode()

        # Add password function
        def add_password(self, site, password):
            self.password_dict[site] = password
            # If inside a password file, allow user input for site and password, encrypt and save to file
            if self.password_file is not None:
                with open(self.password_file, 'a+') as f:
                    encrypted = Fernet(self.key).encrypt(password.encode())
                    f.write(site + ":" + encrypted.decode() + "\n")
                    
        # Getting a password 
        def get_password(self,site):
            return self.password_dict[site]
        
# This is the function for user input
def main():
    # Sample dictonairy
    password = {
        "email": "1234567",
        "facebook": "myfbpassword",
        "youtube": "youtube",
        "something": "myfavouritepassword_123"
        }
    pm = PasswordManager()

    # Creating user input options
    print("""What do you want to do?
    (1) Create new key
    (2) Load existing key
    (3) Create new password file
    (4) Load existing password file
    (5) Add a new password
    (6) Get a password
    (q) Quit
    """)

    # Sets done to false where done indicates start or end of program execution
    done = False

    # If done is false then ask user for input
    while not done:
        choice = input("Enter your choice:")

        if choice == "1":
            path= input("Enter path: ")
            pm.create_key(path)
            
        elif choice =="2":
            try: # Exception statement to prevent crashing from invalid input
                path = input("Enter path: ")
                pm.load_key(path)
                print ("Key has been loaded, you can now enter the name of the passwords file to view or add a new password")
            except:
                print("No key found with that name")
                
        elif choice =="3":
                path = input("Enter path: ")
                pm.create_password_file(path, password)
                
        elif choice == "4":
            try: # Exception statement to prevent crashing from invalid input
                path = input ("Enter path: ")
                pm.load_password_file(path)
            except:
                print("Key doesn't match")

        elif choice == "5":
            path = input("Enter the site: ")
            password = input("Enter the password: ")
            pm.add_password(site, password)

        elif choice == "6":
            try: # Exception statement to prevent crashing from invalid input
                site = input("What site do you want: ")
                print (f"Password for {site} is {pm.get_password(site)}")
            except:
                print("No password/site found")

        elif choice =="q":
            done = True
            print("Bye")

        else:
            print("Invalid selection")
if __name__ == "__main__":
    main()

                    
