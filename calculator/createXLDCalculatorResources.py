# Este script se invoca de forma remota para crear la infraestructura de la aplicación de Calculadora
# La invocación se debe realizar de la siguiente forma:
# ./cli.sh -username admin -password ***** -f /home/jcla/Projects/xld-scripts/calculator/createXLDCalculatorResources.py

def createResource(name, type, props):
    if not repository.exists(name):
        if props:
            myCI = factory.configurationItem(name, type, props)
        else:
            myCI = factory.configurationItem(name, type)
        repository.create(myCI)
        print("CI {0} created".format(name))
    else:
        print("CI {0} existed".format(name))

def createOrUpdateDictionary(env):
    dictEntries = {
        'bdd.url': 'jdbc:mysql://localhost:3306/congruencias',
        'bdd.user': 'cng_user',
        'smoke.test.url': 'http://localhost:8080/congruencias/index',
        'url.webservices': 'http://localhost:8080/axis2/services/webservices.webservicesHttpEndpoint/'
    }
    encryptedDictEntries = {
        'bdd.pass': 'cng_password'
    }
    dictionaryName = "Environments/dictionaries-calculator/dictionary-application-calculator-{0}".format(env)
    if not repository.exists(dictionaryName):
        myDict = factory.configurationItem(dictionaryName, 'udm.Dictionary', {'entries': dictEntries, 'encryptedEntries': encryptedDictEntries})
        repository.create(myDict)
        print("Dictionary {0} created".format(dictionaryName))
    else:
        myDict = repository.read(dictionaryName)
        myDict.entries = dictEntries
        repository.update(myDict)
        print("Dictionary {0} updated".format(dictionaryName))

def createOrUpdateEnvironment(env):
    environmentName = "Environments/application-calculator/application-calculator-{0}/application-calculator-{0}".format(env)
    dictionaryName = "Environments/dictionaries-calculator/dictionary-application-calculator-{0}".format(env)
    dictionaries = [dictionaryName]
    myContainers = [
        "Infrastructure/UnixHosts/calculator-{0}/axis2".format(env),
        "Infrastructure/UnixHosts/calculator-{0}/tomcat/virutal-host-calculator".format(env),
        "Infrastructure/UnixHosts/calculator-{0}/smokeTest".format(env),
        "Infrastructure/UnixHosts/calculator-{0}/mysql-cli".format(env)
    ]
    if not repository.exists(environmentName):
        myEnvironment = factory.configurationItem(environmentName, 'udm.Environment', {'members': myContainers, 'dictionaries': dictionaries})
        repository.create(myEnvironment)
        print("Environment {0} created".format(environmentName))
    else:
        myEnvironment = repository.read(environmentName)
        myEnvironment.members = myContainers
        myEnvironment.dictionaries = dictionaries
        repository.update(myEnvironment)
        print("Environment {0} updated".format(environmentName))

#        / ___|___  _ __ | |_ __ _(_)_ __   ___ _ __ ___ 
#        | |   / _ \| '_ \| __/ _` | | '_ \ / _ \ '__/ __|
#        | |__| (_) | | | | || (_| | | | | |  __/ |  \__ \
#         \____\___/|_| |_|\__\__,_|_|_| |_|\___|_|  |___/

createResource("Infrastructure/UnixHosts", "core.Directory", None)
createResource("Infrastructure/UnixHosts/calculator-dev", "overthere.SshHost", {'os': 'UNIX', 'connectionType': 'SCP', 'address': 'localhost', 'port': '2222', 'username': 'tomcat', 'privateKeyFile': '/home/jcla/.ssh/id_rsa'})
createResource("Infrastructure/UnixHosts/calculator-pre", "overthere.SshHost", {'os': 'UNIX', 'connectionType': 'SCP', 'address': 'localhost', 'port': '2223', 'username': 'tomcat', 'privateKeyFile': '/home/jcla/.ssh/id_rsa'})
createResource("Infrastructure/UnixHosts/calculator-pro", "overthere.SshHost", {'os': 'UNIX', 'connectionType': 'SCP', 'address': 'localhost', 'port': '2224', 'username': 'tomcat', 'privateKeyFile': '/home/jcla/.ssh/id_rsa'})
createResource("Infrastructure/UnixHosts/calculator-dev/axis2", "axis2.Deployer", {'axis2ServicesDirectory': '/opt/apache-tomcat-8.5.8/webapps/axis2/WEB-INF/services'})
createResource("Infrastructure/UnixHosts/calculator-pre/axis2", "axis2.Deployer", {'axis2ServicesDirectory': '/opt/apache-tomcat-8.5.8/webapps/axis2/WEB-INF/services'})
createResource("Infrastructure/UnixHosts/calculator-pro/axis2", "axis2.Deployer", {'axis2ServicesDirectory': '/opt/apache-tomcat-8.5.8/webapps/axis2/WEB-INF/services'})
tomcatProps = {
    'home': '/opt/apache-tomcat-8.5.8',
    'startCommand': 'sudo service tomcat start',
    'stopCommand': 'sudo service tomcat stop',
    'statusCommand': 'sudo service tomcat status'
}
createResource("Infrastructure/UnixHosts/calculator-dev/tomcat", "tomcat.Server", tomcatProps)
createResource("Infrastructure/UnixHosts/calculator-pre/tomcat", "tomcat.Server", tomcatProps)
createResource("Infrastructure/UnixHosts/calculator-pro/tomcat", "tomcat.Server", tomcatProps)
virtualHostProps = {
    'appBase': 'webapps',
    'hostname': 'localhost'
}
createResource("Infrastructure/UnixHosts/calculator-dev/tomcat/virutal-host-calculator", "tomcat.VirtualHost", virtualHostProps)
createResource("Infrastructure/UnixHosts/calculator-pre/tomcat/virutal-host-calculator", "tomcat.VirtualHost", virtualHostProps)
createResource("Infrastructure/UnixHosts/calculator-pro/tomcat/virutal-host-calculator", "tomcat.VirtualHost", virtualHostProps)
createResource("Infrastructure/UnixHosts/calculator-dev/smokeTest", "smoketest.Runner", {'powershellInstalled': False})
createResource("Infrastructure/UnixHosts/calculator-pre/smokeTest", "smoketest.Runner", {'powershellInstalled': False})
createResource("Infrastructure/UnixHosts/calculator-pro/smokeTest", "smoketest.Runner", {'powershellInstalled': False})
bddProps = {
    'username': 'cng_user',
    'password': 'cng_password',
    'mySqlHome': '/usr',
    'databaseName': 'congruencias'
}
createResource("Infrastructure/UnixHosts/calculator-dev/mysql-cli", "sql.MySqlClient", bddProps)
createResource("Infrastructure/UnixHosts/calculator-pre/mysql-cli", "sql.MySqlClient", bddProps)
createResource("Infrastructure/UnixHosts/calculator-pro/mysql-cli", "sql.MySqlClient", bddProps)

# |  _ \(_) ___| |_(_) ___  _ __   __ _ _ __(_) ___  ___ 
# | | | | |/ __| __| |/ _ \| '_ \ / _` | '__| |/ _ \/ __|
# | |_| | | (__| |_| | (_) | | | | (_| | |  | |  __/\__ \
# |____/|_|\___|\__|_|\___/|_| |_|\__,_|_|  |_|\___||___/

createResource("Environments/dictionaries-calculator", "core.Directory", None)
createOrUpdateDictionary('dev')
createOrUpdateDictionary('pre')
createOrUpdateDictionary('pro')

# | ____|_ ____   _(_)_ __ ___  _ __  _ __ ___   ___ _ __ | |_ ___ 
# |  _| | '_ \ \ / / | '__/ _ \| '_ \| '_ ` _ \ / _ \ '_ \| __/ __|
# | |___| | | \ V /| | | | (_) | | | | | | | | |  __/ | | | |_\__ \
# |_____|_| |_|\_/ |_|_|  \___/|_| |_|_| |_| |_|\___|_| |_|\__|___/

# Necesitamos crear un entorno que agrupe los distintos elementos que hemos creado antes
# Primero creamos la estructura de directorios
createResource("Environments/application-calculator", "core.Directory", None)
createResource("Environments/application-calculator/application-calculator-dev", "core.Directory", None)
createResource("Environments/application-calculator/application-calculator-pre", "core.Directory", None)
createResource("Environments/application-calculator/application-calculator-pro", "core.Directory", None)
createOrUpdateEnvironment('dev')
createOrUpdateEnvironment('pre')
createOrUpdateEnvironment('pro')

#    / \   _ __  _ __ | (_) ___ __ _| |_(_) ___  _ __  ___ 
#   / _ \ | '_ \| '_ \| | |/ __/ _` | __| |/ _ \| '_ \/ __|
#  / ___ \| |_) | |_) | | | (_| (_| | |_| | (_) | | | \__ \
# /_/   \_\ .__/| .__/|_|_|\___\__,_|\__|_|\___/|_| |_|___/

createResource("Applications/Applications", "core.Directory", None)
createResource("Applications/Applications/application-calculator", "core.Directory", None)
createResource("Applications/Applications/application-calculator/front", "udm.Application", None)
createResource("Applications/Applications/application-calculator/webservices", "udm.Application", None)