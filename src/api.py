from json import loads
import requests

url = "" # backend url

def signup(name, lastname, password, email):
    post = {
        "name": name,
        "lastname": lastname,
        "password": password,
        "email": email,
        "phone": "None"
    }
    x = requests.post(url + "/auth/new", data=post)
    res = loads(x.text)
    if res["statusCode"] != 201:
        return False
    else:
        return "Hesap başarıyla oluşturuldu."

def login(email, password):
    post = {
        "password": email,
        "email": password,
    }
    x = requests.post(url + "/auth/login", data=post)
    res = loads(x.text)
    if res["statusCode"] != 200:
        return False
    else:
        token = res["data"]
        return token

def getUserInfo(token):
    header = {
        "Authorization": token
    }
    x = requests.get(url + "/auth/@me", headers=header)
    res = loads(x.text)
    if res["statusCode"] == 404:
        return False
    else:
        return res["data"]

def getAllPasswords(token):
    header = {
        "Authorization": token
    }
    x = requests.get(url + "/password/all", headers=header)
    res = loads(x.text)
    if res["statusCode"] != 404:
        a = {}
        for i in res['data']:
            a[i["name"]] = i["password"]
        return a
    else:
        return False

def getPasswordByName(token, name):
    x = getAllPasswords(token)[name]
    return x

def addPassword(token, name, password):
    header = {
        "Authorization": token
    }
    post = {
        "name": name,
        "password": password
    }
    x = requests.post(url + "/password", data=post, headers=header)
    res = loads(x.text)
    if res["statusCode"] != 409:
        return True
    else:
        return False

def deletePassword(token, name):
    header = {
        "Authorization": token
    }
    x = requests.delete(url + f"/password/{name}", headers=header)
    res = loads(x.text)
    if res["statusCode"] != 200:
        return False
    else:
        return True

def editPassword(token, oldname, name, password):
    header = {
        "Authorization": token
    }
    post = {
        "name": name,
        "password": password
    }
    x = requests.patch(url + f"/password/{oldname}", headers=header, data=post)
    res = loads(x.text)
    if res["statusCode"] != 200:
        return False
    else:
        return True

# larei & forcex was here.
