# Este script se invoca de forma remota para crear los roles y los usuarios
# La invocación se debe realizar de la siguiente forma:
# ./cli.sh -f /home/jcla/Projects/xld-scripts/shared-configuration/createUsersRolesPermissions.py
# El usuario y la password están en el fichero /opt/xebialabs/xl-deploy-9.0.5-cli/conf/deployit.conf con el siguiente contenido
# cli.username=admin
# cli.password=password      <- la password se modifica la primera vez que ejecutemos el cli

# Create users
def createUsers():
    security.createUser('ahortal', 'ahortal')
    security.createUser('csantamaria', 'csantamaria')
    security.createUser('jclopez', 'jclopez')
    security.createUser('antonio', 'antonio')
    security.createUser('vsalguero', 'vsalguero')
    security.createUser('amateos', 'amateos')
    security.createUser('cvalero', 'cvalero')
    security.createUser('jccobo', 'jccobo')
    security.createUser('ahartman', 'ahartman')
    security.createUser('jmurcia', 'jmurcia')
    security.createUser('mvega', 'mvega')
    security.createUser('ycobo', 'ycobo')
    security.createUser('jsalguero', 'jsalguero')

# Agrupación de usuarios en listas para facilitar la asignación de roles
calculatorDev = ['ahortal', 'jmurcia']
calculatorPre = ['csantamaria', 'mvega']
calculatorPro = ['jclopez', 'ycobo']
tutorialDev = ['antonio', 'jsalguero']
tutorialPre = ['vsalguero']
tutorialPro = ['amateos']
votingAppDev = ['cvalero']
votingAppPre = ['jccobo']
votingAppPro = ['ahartman']

# Asignación de roles. Los roles, si no existen, se crean automáticamente.
def asignRoles():
    security.assignRole('calculatorDev', calculatorDev)
    security.assignRole('calculatorPre', calculatorPre)
    security.assignRole('calculatorPro', calculatorPro)
    security.assignRole('tutorialDev', tutorialDev)
    security.assignRole('tutorialPre', tutorialPre)
    security.assignRole('tutorialPro', tutorialPro)
    security.assignRole('voting-appDev', votingAppDev)
    security.assignRole('voting-appPre', votingAppPre)
    security.assignRole('voting-appPro', votingAppPro)

# Asignación de permisos a los distintos roles. Global permissions
def grantPermissions():
    # Asignamos permiso de login para todos los roles
    security.grant('login', 'calculatorDev')
    security.grant('login', 'calculatorPre')
    security.grant('login', 'calculatorPro')
    security.grant('login', 'tutorialDev')
    security.grant('login', 'tutorialPre')
    security.grant('login', 'tutorialPro')
    security.grant('login', 'voting-appDev')
    security.grant('login', 'voting-appPre')
    security.grant('login', 'voting-appPro')

    # Permitimos que los roles tengan acceso a los reports y logs de despliegue
    security.grant('report#view', 'calculatorDev')
    security.grant('report#view', 'calculatorPre')
    security.grant('report#view', 'calculatorPro')
    security.grant('report#view', 'tutorialDev')
    security.grant('report#view', 'tutorialPre')
    security.grant('report#view', 'tutorialPro')
    security.grant('report#view', 'voting-appDev')
    security.grant('report#view', 'voting-appPre')
    security.grant('report#view', 'voting-appPro')

def grantPermissions(application):
    # Debemos dar permiso de lectura a la aplicacion a los roles correspondientes.
    # No se autoriza a estos usuarios a crear nuevas versiones o modificar las existentes.
    security.grant("read", "{0}Dev".format(application), ["Applications/Applications/application-{0}".format(application)])
    security.grant("read", "{0}Pre".format(application), ["Applications/Applications/application-{0}".format(application)])
    security.grant("read", "{0}Pro".format(application), ["Applications/Applications/application-{0}".format(application)])
    # Autorizamos a estos grupos a desplegar las versiones de la aplicacion a los entornos correspondientes
    security.grant("read", "{0}Dev".format(application), ["Environments/application-{0}".format(application)])
    security.grant("read", "{0}Pre".format(application), ["Environments/application-{0}".format(application)])
    security.grant("read", "{0}Pro".format(application), ["Environments/application-{0}".format(application)])
    # Autorizamos acceso a los subdirectorios correspondientes

    security.grant("read", 'fichadecliente-uat', ['Environments/2.UAT']) # Es necesario dar permisos de lectura a la carpeta de nivel superior
    security.grant("read", 'fichadecliente-uat', ['Environments/2.UAT/fichadeclienteosp'])
    security.grant("read", 'fichadecliente-pro', ['Environments/4.Produccion'])
    security.grant("read", 'fichadecliente-pro', ['Environments/4.Produccion/fichadeclienteosp'])
    # Autorizamos a realizar los tres tipos de despliegues (deploy inicial, upgrade y undeploy), entorno UAT
    security.grant("deploy#initial", 'fichadecliente-uat', ['Environments/2.UAT/fichadeclienteosp'])
    security.grant("deploy#upgrade", 'fichadecliente-uat', ['Environments/2.UAT/fichadeclienteosp'])
    security.grant("deploy#undeploy", 'fichadecliente-uat', ['Environments/2.UAT/fichadeclienteosp'])
    # Autorizamos a realizar los tres tipos de despliegues (deploy inicial, upgrade y undeploy), entorno PRO
    security.grant("deploy#initial", 'fichadecliente-pro', ['Environments/4.Produccion/fichadeclienteosp'])
    security.grant("deploy#upgrade", 'fichadecliente-pro', ['Environments/4.Produccion/fichadeclienteosp'])
    security.grant("deploy#undeploy", 'fichadecliente-pro', ['Environments/4.Produccion/fichadeclienteosp'])

def createDirectoryApplication(application):
    if not repository.exists("Applications/" + application):
        myApp = factory.configurationItem("Applications/" + application, "core.Directory")
        repository.create(myApp)

def createDirectoriesEnvironments(application):
    for envDir in ['1.Integracion', '2.UAT', '3.Produccion']:
        if not repository.exists("Environments/" + envDir):
            myDir = factory.configurationItem("Environments/" + envDir, "core.Directory")
            repository.create(myDir)
        if not repository.exists("Environments/" + envDir + "/" + application):
            myEnvDir = factory.configurationItem("Environments/" + envDir + "/" + application, "core.Directory")
            repository.create(myEnvDir)

def grantPermissionsApplication(application, applicationUsersDEV, applicationUsersUAT, applicationUsersPRO):
    # Asignación de roles a usuarios. Es necesario definir 3 roles. Para dev, uat y pro.
    security.assignRole(application + "-dev", applicationUsersDEV)
    security.assignRole(application + "-uat", applicationUsersUAT)
    security.assignRole(application + "-pro", applicationUsersPRO)

    # Aseguramos que existe el directorio de la aplicación
    createDirectoryApplication(application)
    
    # Concedemos permiso de login, reports y read a los nuevos roles
    for env in ['dev', 'uat', 'pro']:
        rol = application + "-" + env
        # Asignamos permiso de login para todos los roles
        security.grant('login', rol)
        # Permitimos que los roles tengan acceso a los reports y logs de despliegue
        security.grant('report#view', rol)
        # Todos los roles tendrán permiso de lectura a la nueva aplicacion
        security.grant("read", rol, ["Applications/" + application])

    # Los usuarios con role DEV, deben poder crear nuevas versiones en XL Deploy
    # rol = application + "-dev"
    # security.grant('import#initial', rol, ["Applications/" + application])
    # security.grant('import#remove', rol, ["Applications/" + application])
    # security.grant('import#upgrade', rol, ["Applications/" + application])
    # Las versiones deberían ser inmutables, por lo tanto debería evitarse conceder el permiso repo#edit
    # En cualquier caso, si se desea conceder, descomentar la siguiente línea
    # security.grant('repo#edit', rol, ["Applications/" + application])

    # Acceso a los entornos de despliegue
    # Aseguramos que existen los directorios y la estructura correcta antes de realizar la asignación de permisos
    createDirectoriesEnvironments(application)

    # Creación de environments y asignación de permisos
    security.grant("read", application + "-dev", ['Environments/1.Integracion']) # Es necesario dar permisos de lectura a la carpeta de nivel superior
    security.grant("read", application + "-dev", ['Environments/1.Integracion/' + application])
    security.grant("read", application + "-uat", ['Environments/2.UAT'])
    security.grant("read", application + "-uat", ['Environments/2.UAT/' + application])
    security.grant("read", application + "-pro", ['Environments/3.Produccion'])
    security.grant("read", application + "-pro", ['Environments/3.Produccion/' + application])
    # Autorizamos a realizar los tres tipos de despliegues (deploy inicial, upgrade y undeploy), entorno DEV
    security.grant("deploy#initial", application + "-dev", ['Environments/1.Integracion/' + application])
    security.grant("deploy#upgrade", application + "-dev", ['Environments/1.Integracion/' + application])
    security.grant("deploy#undeploy", application + "-dev", ['Environments/1.Integracion/' + application])
    # Autorizamos a realizar los tres tipos de despliegues (deploy inicial, upgrade y undeploy), entorno UAT
    security.grant("deploy#initial", application + "-uat", ['Environments/2.UAT/' + application])
    security.grant("deploy#upgrade", application + "-uat", ['Environments/2.UAT/' + application])
    security.grant("deploy#undeploy", application + "-uat", ['Environments/2.UAT/' + application])
    # Autorizamos a realizar los tres tipos de despliegues (deploy inicial, upgrade y undeploy), entorno PRO
    security.grant("deploy#initial", application + "-pro", ['Environments/3.Produccion/' + application])
    security.grant("deploy#upgrade", application + "-pro", ['Environments/3.Produccion/' + application])
    security.grant("deploy#undeploy", application + "-pro", ['Environments/3.Produccion/' + application])

def loadDataOrange():
    createUsersOpenApi()
    createUsersCfmFdc()
    createUsersFdc()
    groupUsers()
    asignRolesOrange()
    grantPermissionsOrange()
    grantPermissionsFichaDeCliente()
    grantPermissionsOpenApi()
