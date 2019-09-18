# Este script se invoca de forma remota para crear la infraestructura de la aplicación de Tutorial
# La invocación se debe realizar de la siguiente forma:
# ./cli.sh -f /home/jcla/Projects/xld-scripts/tutorial/createXLDTutorialResources.py
# El usuario y la password están en el fichero /opt/xebialabs/xl-deploy-X-cli/conf/deployit.conf con el siguiente contenido
# cli.username=admin
# cli.password=password      <- la password se modifica la primera vez que ejecutemos el cli

# La aplicación la cargamos utilizando xl apply -f app.yaml

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
    dictionaryName = "Environments/dictionaries-tutorial/dictionary-application-tutorial-{0}".format(env)
    if not repository.exists(dictionaryName):
        myDict = factory.configurationItem(dictionaryName, 'udm.Dictionary', {})
        repository.create(myDict)
        print("Dictionary {0} created".format(dictionaryName))
    else:
        myDict = repository.read(dictionaryName)
        # Por ahora no necesitamos dictEntries
        # myDict.entries = dictEntries
        repository.update(myDict)
        print("Dictionary {0} updated".format(dictionaryName))

def createOrUpdateEnvironment(env):
    environmentName = "Environments/application-tutorial/application-tutorial-{0}/application-tutorial-{0}".format(env)
    dictionaryName = "Environments/dictionaries-tutorial/dictionary-application-tutorial-{0}".format(env)
    dictionaries = [dictionaryName]
    requiresOkTestManager = False
    requiresOkReleaseManager = False
    if env == "pre":
        requiresOkTestManager = True
    if env == "pro":
        requiresOkTestManager = True
        requiresOkReleaseManager = True
    myContainers = [
        "Infrastructure/KubernetesClusters/on-premise-cluster/ns-tutorial-{0}".format(env)
    ]
    # Calculamos los triggers
    if env == "dev":
        triggerEnvironmentName = "Development"
    elif env == "pre":
        triggerEnvironmentName = "Preproduction"
    else:
        triggerEnvironmentName = "Production"
    triggerFailed = "Configuration/Environments/{0}/Triggers/FailedDeploymentTrigger".format(triggerEnvironmentName)
    triggerSuccessful = "Configuration/Environments/{0}/Triggers/SuccessfulDeploymentTrigger".format(triggerEnvironmentName)
    triggers = [triggerFailed, triggerSuccessful]
    if not repository.exists(environmentName):
        myEnvironment = factory.configurationItem(environmentName, 'udm.Environment', {'members': myContainers, 'dictionaries': dictionaries, 'requiresOkTestManager': requiresOkTestManager, 'requiresOkReleaseManager': requiresOkReleaseManager, 'triggers': triggers})
        repository.create(myEnvironment)
        print("Environment {0} created".format(environmentName))
    else:
        myEnvironment = repository.read(environmentName)
        myEnvironment.members = myContainers
        myEnvironment.dictionaries = dictionaries
        myEnvironment.requiresOkTestManager = requiresOkTestManager
        myEnvironment.requiresOkReleaseManager = requiresOkReleaseManager
        myEnvironment.triggers = triggers
        repository.update(myEnvironment)
        print("Environment {0} updated".format(environmentName))

#        / ___|___  _ __ | |_ __ _(_)_ __   ___ _ __ ___ 
#        | |   / _ \| '_ \| __/ _` | | '_ \ / _ \ '__/ __|
#        | |__| (_) | | | | || (_| | | | | |  __/ |  \__ \
#         \____\___/|_| |_|\__\__,_|_|_| |_|\___|_|  |___/

createResource("Infrastructure/KubernetesClusters", "core.Directory", None)
caCertOnPremise = '''
----BEGIN CERTIFICATE-----
MIICyDCCAbCgAwIBAgIBADANBgkqhkiG9w0BAQsFADAVMRMwEQYDVQQDEwprdWJl
cm5ldGVzMB4XDTE5MDkxNzIxMjU1NVoXDTI5MDkxNDIxMjU1NVowFTETMBEGA1UE
AxMKa3ViZXJuZXRlczCCASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEBAPzi
ufuhXF/vEN6fod9pImBm2zgIJbUXuKuCErTaPx3WA+tjtvldfy8txVnIob8I0opc
7BESPBOtidqi1ikSn9dPKCNUg1aeDnzXlY8YJLGMI7I9SGR9FmwPWbb2PsOvpxFp
IEwW2dXlBRThfp8A5EARaOW69OArri+kioZq8SlQtRg7cxUq8gegYDt5RO4X1K9N
JKq/+XC3dYosC6OksfBtRh1Ym6yRGKAaCku5qDSOfyJikJ6eLNGwvdbvfknJZBU+
OAu5VqlIqrM+F+8MRutZAsQKMTburbTI60zFPUeo/gKSioUQSG/e13oniT1HUWV+
KFd4lI8bfFI6wz0F7xMCAwEAAaMjMCEwDgYDVR0PAQH/BAQDAgKkMA8GA1UdEwEB
/wQFMAMBAf8wDQYJKoZIhvcNAQELBQADggEBAKaY2iWrsvMi90050G3fEmGjSK0y
n5m8u4d8++YBlaxbPL76C+RkuLzAyO2hM+aa0WGhbvULLHF8XB3Sy0HkSx4H64rb
JzBr6DH5Y1PxqMe/VvSCKV5GpbBbASm4u9UajGvppEF3sZLjsY/aUGuD5MVWs2sW
o9veu+ATVVz8voH/w0nPsv9/Chkz7htvAHcqapaQxAbW3oBSPhurTtSjlAI2NPmm
78s/lzzMQ/7L4q4kShJucHsPFOKlUIt7g4Z1MOzWj206DZCxwLC7cr2U1e7tLPao
OrxxG4DNBvsj0kTOVrhOPo3ZnqVRRamRwXEwfgx+fdp5PproIH6pwao9DK4=
-----END CERTIFICATE-----
'''
tokenOnPremise = 'eyJhbGciOiJSUzI1NiIsImtpZCI6IiJ9.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJrdWJlLXN5c3RlbSIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VjcmV0Lm5hbWUiOiJhZG1pbi11c2VyLXRva2VuLThwNmNxIiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZXJ2aWNlLWFjY291bnQubmFtZSI6ImFkbWluLXVzZXIiLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlcnZpY2UtYWNjb3VudC51aWQiOiI4NGIzNzAwZC0wOTY4LTQxMzMtYmM1ZC1jZmQzZTE3ZjA0N2UiLCJzdWIiOiJzeXN0ZW06c2VydmljZWFjY291bnQ6a3ViZS1zeXN0ZW06YWRtaW4tdXNlciJ9.eG1Mjen1JPo--zGjK65DfO0J9JTty0O5nZphkKaqfIR9Hzkr7tYBwzzihQmHXy1-yjSPD-n2bQG6SyKWfSYkyc8D0j_Ozjl-wViw0aKcFzz0lAq6SGYQ1ipco-pUbrN_hnnrgEX2UsxaRXvRYNqj-d0TUg4hahr17WuYgsolHgVlPaaLd8-zN1p3vt5AsdfixKxfgtiRCt9JM0V8ibRmkfzo6GamrZr8ASXm44iQH5Dn1PxypZRggtXSEZ7_PkYf4Ap9FP6kC01r1mMOl77VytzY2QtVE8O7ij0TSOFgzXcT2AMsi0th2vCkSSYOcACedbcy2l10z1jd3nBtKDGj_Q'
createResource("Infrastructure/KubernetesClusters/on-premise-cluster", "k8s.Master", {'apiServerURL': 'https://172.42.42.100:6443', 'skipTLS': True, 'caCert': caCertOnPremise, 'token': tokenOnPremise})
createResource("Infrastructure/KubernetesClusters/on-premise-cluster/ns-tutorial-dev", "k8s.Namespace", {'namespaceName': 'ns-tutorial-dev'})
createResource("Infrastructure/KubernetesClusters/on-premise-cluster/ns-tutorial-pre", "k8s.Namespace", {'namespaceName': 'ns-tutorial-pre'})
createResource("Infrastructure/KubernetesClusters/on-premise-cluster/ns-tutorial-pro", "k8s.Namespace", {'namespaceName': 'ns-tutorial-pro'})


# |  _ \(_) ___| |_(_) ___  _ __   __ _ _ __(_) ___  ___ 
# | | | | |/ __| __| |/ _ \| '_ \ / _` | '__| |/ _ \/ __|
# | |_| | | (__| |_| | (_) | | | | (_| | |  | |  __/\__ \
# |____/|_|\___|\__|_|\___/|_| |_|\__,_|_|  |_|\___||___/

createResource("Environments/dictionaries-tutorial", "core.Directory", None)
createOrUpdateDictionary('dev')
createOrUpdateDictionary('pre')
createOrUpdateDictionary('pro')

# | ____|_ ____   _(_)_ __ ___  _ __  _ __ ___   ___ _ __ | |_ ___ 
# |  _| | '_ \ \ / / | '__/ _ \| '_ \| '_ ` _ \ / _ \ '_ \| __/ __|
# | |___| | | \ V /| | | | (_) | | | | | | | | |  __/ | | | |_\__ \
# |_____|_| |_|\_/ |_|_|  \___/|_| |_|_| |_| |_|\___|_| |_|\__|___/

# Necesitamos crear un entorno que agrupe los distintos elementos que hemos creado antes
# Primero creamos la estructura de directorios
createResource("Environments/application-tutorial", "core.Directory", None)
createResource("Environments/application-tutorial/application-tutorial-dev", "core.Directory", None)
createResource("Environments/application-tutorial/application-tutorial-pre", "core.Directory", None)
createResource("Environments/application-tutorial/application-tutorial-pro", "core.Directory", None)
createOrUpdateEnvironment('dev')
createOrUpdateEnvironment('pre')
createOrUpdateEnvironment('pro')

#    / \   _ __  _ __ | (_) ___ __ _| |_(_) ___  _ __  ___ 
#   / _ \ | '_ \| '_ \| | |/ __/ _` | __| |/ _ \| '_ \/ __|
#  / ___ \| |_) | |_) | | | (_| (_| | |_| | (_) | | | \__ \
# /_/   \_\ .__/| .__/|_|_|\___\__,_|\__|_|\___/|_| |_|___/

createResource("Applications/Applications", "core.Directory", None)
createResource("Applications/Applications/application-tutorial", "core.Directory", None)
createResource("Applications/Applications/application-tutorial/tutorial", "udm.Application", None)

#  / ___|___  _ __  / _(_) __ _ _   _ _ __ __ _| |_(_) ___  _ __  
# | |   / _ \| '_ \| |_| |/ _` | | | | '__/ _` | __| |/ _ \| '_ \ 
# | |__| (_) | | | |  _| | (_| | |_| | | | (_| | |_| | (_) | | | |
#  \____\___/|_| |_|_| |_|\__, |\__,_|_|  \__,_|\__|_|\___/|_| |_|

def getEnvironments(application):
    environments = []
    for env in ['dev', 'pre', 'pro']:
        environmentName = "Environments/application-{0}/application-{0}-{1}/application-{0}-{1}".format(application, env)
        environments = environments + [environmentName]
    return environments

# Creamos el pipeline
createResource("Configuration/pipeline-tutorial", "release.DeploymentPipeline", {'pipeline': getEnvironments('tutorial')})

# Y lo asociamos
tutorial = repository.read("Applications/Applications/application-tutorial/tutorial")
tutorial.pipeline = "Configuration/pipeline-tutorial"
repository.update(tutorial)
