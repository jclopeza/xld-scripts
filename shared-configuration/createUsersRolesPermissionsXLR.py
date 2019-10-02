# Este script se invoca de forma remota para crear Usuarios y Roles en XLR
# La invocación se debe realizar de la siguiente forma:
# ./cli.sh -f /home/jcla/Projects/xld-scripts/shared-configuration/createUsersRolesPermissionsXLR.py user password
# El usuario y la password están en el fichero /opt/xebialabs/xl-deploy-X-cli/conf/deployit.conf con el siguiente contenido
# cli.username=admin
# cli.password=password      <- la password se modifica la primera vez que ejecutemos el cli
#
# En el fichero cna.yaml se encuentra la template de XLR que genera lo necesario

import sys
user = sys.argv[1]      # Para conectar con XLR
password = sys.argv[2]  # Para conectar con XLR

import urllib2
import json
import base64

def callXLR(url, data):
    req = urllib2.Request(url)
    base64string = base64.b64encode("{0}:{1}".format(user, password))
    req.add_header("Authorization", "Basic %s" % base64string)
    req.add_header('Content-Type','application/json')
    if data is not None:
        data = json.dumps(data)
        return urllib2.urlopen(req, data)
    else:
        return urllib2.urlopen(req)

users = [
    {
        "login": "agiraldo",
        "data": {
            "fullName": "Alfredo Giraldo",
            "password": "agiraldo",
            "email": "agiraldo@gmail.com",
            "loginAllowed": True,
            "firstDayOfWeek": 1
        }
    },
    {
        "login": "ahartman",
        "data": {
            "fullName": "Alberto Hartman",
            "password": "ahartman",
            "email": "ahartman@gmail.com",
            "loginAllowed": True,
            "firstDayOfWeek": 1
        }
    },
    {
        "login": "ahortalq",
        "data": {
            "fullName": "Azucena Hortal Quirante",
            "password": "ahortalq",
            "email": "ahortalq@gmail.com",
            "loginAllowed": True,
            "firstDayOfWeek": 1
        }
    },
    {
        "login": "amateos",
        "data": {
            "fullName": "Alberto Mateos",
            "password": "amateos",
            "email": "amateos@gmail.com",
            "loginAllowed": True,
            "firstDayOfWeek": 1
        }
    },
    {
        "login": "antonio",
        "data": {
            "fullName": "Antonio Psicólogo",
            "password": "antonio",
            "email": "antonio@gmail.com",
            "loginAllowed": True,
            "firstDayOfWeek": 1
        }
    },
    {
        "login": "charo",
        "data": {
            "fullName": "Rosario Santamaría Cervantes",
            "password": "charo",
            "email": "charo@gmail.com",
            "loginAllowed": True,
            "firstDayOfWeek": 1
        }
    },
    {
        "login": "cvalero",
        "data": {
            "fullName": "Carmen Valero",
            "password": "cvalero",
            "email": "cvalero@gmail.com",
            "loginAllowed": True,
            "firstDayOfWeek": 1
        }
    },
    {
        "login": "isanchez",
        "data": {
            "fullName": "Inmaculada Sáncez",
            "password": "isanchez",
            "email": "isanchez@gmail.com",
            "loginAllowed": True,
            "firstDayOfWeek": 1
        }
    },
    {
        "login": "jccobo",
        "data": {
            "fullName": "Juan Carlos Cobo",
            "password": "jccobo",
            "email": "jccobo@gmail.com",
            "loginAllowed": True,
            "firstDayOfWeek": 1
        }
    },
    {
        "login": "jcla",
        "data": {
            "fullName": "José Carlos",
            "password": "jcla",
            "email": "jcla@gmail.com",
            "loginAllowed": True,
            "firstDayOfWeek": 1
        }
    },
    {
        "login": "jmurcia",
        "data": {
            "fullName": "Juan Murcia",
            "password": "jmurcia",
            "email": "jmurcia@gmail.com",
            "loginAllowed": True,
            "firstDayOfWeek": 1
        }
    },
    {
        "login": "jsalguero",
        "data": {
            "fullName": "Juan Salguero",
            "password": "jsalguero",
            "email": "jsalguero@gmail.com",
            "loginAllowed": True,
            "firstDayOfWeek": 1
        }
    },
    {
        "login": "mvega",
        "data": {
            "fullName": "Maria Vega",
            "password": "mvega",
            "email": "mvega@gmail.com",
            "loginAllowed": True,
            "firstDayOfWeek": 1
        }
    },
    {
        "login": "vsalguero",
        "data": {
            "fullName": "Vanesa Salguero",
            "password": "vsalguero",
            "email": "vsalguero@gmail.com",
            "loginAllowed": True,
            "firstDayOfWeek": 1
        }
    },
    {
        "login": "ycobo",
        "data": {
            "fullName": "Yolanda Cobo",
            "password": "ycobo",
            "email": "ycobo@gmail.com",
            "loginAllowed": True,
            "firstDayOfWeek": 1
        }
    },

]
roles = ['desarrollo', 'automatizacion', 'cloud', 'provisioning', 'seguridad']

def loadUsers():
    for u in users:
        url = "http://localhost:5516/api/v1/users/{0}".format(u["login"])
        try:
            response = callXLR(url, None)
            print("Ya existe el usuario {0}".format(u["login"]))
        except urllib2.HTTPError as err:
            if err.code == 404:
                print("Creamos el usuario {0}".format(u["login"]))
                data = u["data"]
                response = callXLR(url, data)

def loadRoles():
    for r in roles:
        print("Evaluando rol {0}".format(r))
        url = "http://localhost:5516/api/v1/roles/{0}".format(r)
        try:
            response = callXLR(url, None)
            print("Ya existe el rol {0}".format(r))
        except urllib2.HTTPError as err:
            print("Codigo de error = {0}".format(err.code))
            if err.code == 404:
                print("Creamos el rol {0}".format(r))
                data = {
                    "name" : r
                }
                response = callXLR(url, data)

loadRoles()
loadUsers()