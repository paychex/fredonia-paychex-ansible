# By Greg Cavaretta
# Server setup script - v1.0

#imports
import sys
import subprocess
import os

#Check to see if program is running as sudo
#This is a must otherwise, program can't install anything
user = os.getenv("SUDO_USER")
if user is None:
    print "This program need 'sudo' permissions!"
    exit()

#Check to see if requests is installed
#Try to import requests
try:
    import requests
except ImportError: #If not found, then download
    subprocess.call([sys.executable, "-m", "pip", "install", 'requests'])
finally: #then import
    import requests
    

#Reason for this is because the function is Async and "Safer" than using gzip/tar etc...
#Import ZipFile
try:
    from zipfile import ZipFile
except ImportError: #If not found, then download
    subprocess.call([sys.executable, "-m", "pip", "install", 'ZipFile'])
finally: #then import
    from zipfile import ZipFile
        
    
    
#MARK: Download scripts and zips
#Everything should be good at this point

print('Downloading BedRock zip')

url = 'https://github.com/paychex/fredonia-paychex-ansible/blob/Minecraft_setup/Infrastructure/ServerDeployment/bedrock_server.zip?raw=true'
r = requests.get(url)

with open('./test/bedrock_server.zip', 'wb') as f:
    f.write(r.content)

# Retrieve HTTP meta-data
#MARK: TODO: if check to see if download successful
print(r.status_code)
print(r.headers['content-type'])
print(r.encoding)


#Download EasyMessages plugin
print('Downloading EasyMessages plugin for minecraft')
url = 'https://github.com/paychex/fredonia-paychex-ansible/blob/Minecraft_setup/Infrastructure/ServerDeployment/EasyMessages_v1.2.0.phar?raw=true'
r = requests.get(url)
with open('./test/EasyMessages_v1.2.0.phar', 'wb') as f:
    f.write(r.content)

# Retrieve HTTP meta-data
#MARK: TODO: if check to see if download successful
print(r.status_code)
print(r.headers['content-type'])
print(r.encoding)


#MARK: Unzip bedrock server files
print('Unzipping bedrock_server.zip')
# Create a ZipFile Object and load bedrock_server.zip in it
with ZipFile('./test/bedrock_server.zip', 'r') as zo:
    # Extract all the contents of zip file in current directory
    zo.extractall('./test')



