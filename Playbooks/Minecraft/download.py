# By Greg Cavaretta
# Server setup script - v1.1

#imports
import sys
import subprocess
import os, stat
from os import path

#check if minecraft is already installed then don't do anything else
if path.exists("server.properties"):
    print("The minecraft file already exists")
    exit(0)


#Check to see if program is running as sudo 
#This is a must otherwise, program can't install anything
user = os.getenv("SUDO_USER")
if user is None:
    print ("This program need 'sudo' permissions!")
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
    


#Import shutil
try:
    import shutil
except ImportError: #If not found, then download
    subprocess.call([sys.executable, "-m", "pip", "install", 'shutil'])
finally: #then import
    import shutil
    

#This function will make a new service file that will start minecraft at boot of server
def makeServiceFile():
    f = open("minecraftStartup.service","w+")
    
    f.write("[Unit]")
    f.write("\nDescription=\"Run minecraft\"")
    f.write("\n[Service]")
    f.write("\nExecStart=LD_LIBRARY_PATH=$USER/bedrock_server")
    f.write("\n[Intstall]")
    f.write("\nWantedBy=multi.user.target")
    f.close()
#END OF FUNCTION
    
    
    
#MARK: Download scripts and zips
#Everything should be good at this point

print('Downloading BedRock zip')

url = 'https://minecraft.azureedge.net/bin-linux/bedrock-server-1.13.2.0.zip'
r = requests.get(url)

with open('./bedrock-server-1.13.2.0.zip', 'wb') as f:
    f.write(r.content)

# Retrieve HTTP meta-data
#MARK: TODO: if check to see if download successful
print(r.status_code)
print(r.headers['content-type'])
print(r.encoding)


#MARK: Unzip bedrock server files
print('Unzipping bedrock-server-1.13.2.0.zip')
# Create a ZipFile Object and load bedrock_server.zip in it
with ZipFile('./bedrock-server-1.13.2.0.zip', 'r') as zo:
    # Extract all the contents of zip file in current directory
    zo.extractall('./')


#MARK: This install the service
#This handles moving the startup service from the install dir to the system services
sourceDIR = './minecraftStartup.service'
systemdDIR = '/lib/systemd/system/minecraftStartup.service'

#Create the service file
makeServiceFile()

#CHMOD service
os.chmod(sourceDIR, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO) #Read, write, and execute by user.

print("Moving service")
#move the service
dest = shutil.move(sourceDIR, systemdDIR)

