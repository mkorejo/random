# COPYRIGHT LICENSE: This information contains sample code provided in
# source code form. You may copy, modify, and distribute these sample
# programs in any form without payment to IBM for the purposes of
# developing, using, marketing or distributing application programs
# conforming to the application programming interface for the operating
# platform for which the sample code is written. Notwithstanding anything
# to the contrary, IBM PROVIDES THE SAMPLE SOURCE CODE ON AN "AS IS" BASIS
# AND IBM DISCLAIMS ALL WARRANTIES, EXPRESS OR IMPLIED, INCLUDING, BUT NOT
# LIMITED TO, ANY IMPLIED WARRANTIES OR CONDITIONS OF MERCHANTABILITY,
# SATISFACTORY QUALITY, FITNESS FOR A PARTICULAR PURPOSE, TITLE, AND ANY
# WARRANTY OR CONDITION OF NON-INFRINGEMENT. IBM SHALL NOT BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL OR CONSEQUENTIAL DAMAGES ARISING OUT
# OF THE USE OR OPERATION OF THE SAMPLE SOURCE CODE. IBM HAS NO OBLIGATION
# TO PROVIDE MAINTENANCE, SUPPORT, UPDATES, ENHANCEMENTS OR MODIFICATIONS TO
# THE SAMPLE SOURCE CODE.

# (C) Copyright IBM Corp. 2011.
# All Rights Reserved. Licensed Materials - Property of IBM.

# Usage:
# wsadmin -lang jython -f setupCEA.py <pbx_app_path> <plants_app_path> <ws_app_path> <node_name> <server_name>
# -or-
# wsadmin -lang jython -f setupCEA.py <pbx_app_path> <plants_app_path> <ws_app_path> <cell_name> <node_name> <server_name> <pbx_address> <pbx_port>

# Note: Customization of this script is not required or recommended. Use the
# variables in setupCEA.sh or setupCEA.bat to specify the properties of your
# WebSphere Application Server environment.

import sys
import time

## Configure server-level CEA settings ##
## configureCEASettingsForServer("localhostNode01Cell", "localhostNode01", "server1", "false | true", "30", "SIP_CTI_GATEWAY | THIRD_PARTY_WEB_SERVICE", "localhost", "5060", "TCP | UDP | TLS", "false | true", "ceauser", '""')

def configureCEASettingsForServer(cellName, nodeName, serverName, enableCEA, maxRequestHoldTime, telephonyAccessMethod, gatewayAddress, gatewayPort, gatewayProtocol, extractUsernameFromRequest, superUsername, thirdPartyWSDLProvider):
   deployment = AdminConfig.getid("/Deployment:commsvc/")
   deployedObject = AdminConfig.showAttribute(deployment, "deployedObject")
   rawTargetMappings = AdminConfig.showAttribute(deployedObject, "targetMappings")
   targetMappingList = convertToList(rawTargetMappings)
   for targetMapping in targetMappingList:
      currentTarget = AdminConfig.showAttribute(targetMapping, "target")
      if (currentTarget.find("ServerTarget") > 0):
         if ((AdminConfig.showAttribute(currentTarget, "nodeName") == nodeName) & (AdminConfig.showAttribute(currentTarget, "name") == serverName)):
            AdminConfig.modify(targetMapping, "[[enable " + enableCEA + "]]")
   if (len(AdminConfig.getid("/Cell:" + cellName + "/Node:" + nodeName + "/Server:" + serverName + "/CEASettings:/")) == 0):
      ceaSettingsID = AdminConfig.create("CEASettings", AdminConfig.getid("/Cell:" + cellName + "/Node:" + nodeName + "/Server:" + serverName + "/"), "[[telephonyAccessMethod " + telephonyAccessMethod + "]]")
      AdminConfig.create("CTIGateway", ceaSettingsID, "[[gatewayAddress " + gatewayAddress + "] [gatewayPort " + gatewayPort + "] [gatewayProtocol " + gatewayProtocol + "] [extractUsernameFromRequest " + extractUsernameFromRequest + "] [superUsername " + superUsername + "]]")
      AdminConfig.create("Commsvc", ceaSettingsID, "[[maxRequestHoldTime " + maxRequestHoldTime + "] [thirdPartyWSDLProvider " + thirdPartyWSDLProvider + "]]")
   else:
      AdminConfig.modify(AdminConfig.getid("/Cell:" + cellName + "/Node:" + nodeName + "/Server:" + serverName + "/CEASettings:/"), "[[telephonyAccessMethod " + telephonyAccessMethod + "]]")
      AdminConfig.modify(AdminConfig.getid("/Cell:" + cellName + "/Node:" + nodeName + "/Server:" + serverName + "/CEASettings:/CTIGateway:/"), "[[gatewayAddress " + gatewayAddress + "] [gatewayPort " + gatewayPort + "] [gatewayProtocol " + gatewayProtocol + "] [extractUsernameFromRequest " + extractUsernameFromRequest + "] [superUsername " + superUsername + "]]")
      AdminConfig.modify(AdminConfig.getid("/Cell:" + cellName + "/Node:" + nodeName + "/Server:" + serverName + "/CEASettings:/Commsvc:/"), "[[maxRequestHoldTime " + maxRequestHoldTime + "] [thirdPartyWSDLProvider " + thirdPartyWSDLProvider + "]]")
#endDef


## Obtain the port assigned to an endpoint ##
## getServerPort("localhostNode01Cell", "localhostNode01", "server1", "SIP_DEFAULTHOST")

def getServerPort(cellName, nodeName, serverName, endPointName):
   rawServerEntries = AdminConfig.list("ServerEntry", AdminConfig.getid("/Cell:" + cellName + "/Node:" + nodeName + "/"))
   serverEntryList = convertToList(rawServerEntries)
   for serverEntry in serverEntryList:
      sName = AdminConfig.showAttribute(serverEntry, "serverName")
      if sName == serverName:
         rawSpecialEndPoints = AdminConfig.showAttribute(serverEntry, "specialEndpoints")
         specialEndPointList = convertToList(rawSpecialEndPoints)
         for specialEndPoint in specialEndPointList:
            endPointNm = AdminConfig.showAttribute(specialEndPoint, "endPointName")
            if endPointNm == endPointName:
               endPoint = AdminConfig.showAttribute(specialEndPoint, "endPoint")
               return AdminConfig.showAttribute(endPoint, "port")
#endDef


## Add host alias if not present ##
## addHostAlias("localhostNode01Cell", "localhostNode01", "server1", "default_host", "SIP_DEFAULTHOST")

def addHostAlias(cellName, nodeName, serverName, virtualHost, endPointName):
   serverPort = getServerPort(cellName, nodeName, serverName, endPointName)
   rawHostAliases = AdminConfig.list("HostAlias", AdminConfig.getid("/Cell:" + cellName + "/VirtualHost:" + virtualHost + "/"))
   hostAliasList = convertToList(rawHostAliases)
   for hostAliasEntry in hostAliasList:
      hostName = AdminConfig.showAttribute(hostAliasEntry, "hostname")
      portNumber = AdminConfig.showAttribute(hostAliasEntry, "port")
      if ((hostName == "*") & (portNumber == serverPort)):
         print "Host alias for " + endPointName + " port " + serverPort + " exists in " + virtualHost
         return
   print "Adding host alias for " + endPointName + " port " + serverPort + " to " + virtualHost
   AdminConfig.create("HostAlias", AdminConfig.getid("/Cell:" + cellName + "/VirtualHost:" + virtualHost + "/"), "[[hostname *] [port " + serverPort + "]]")
#endDef


## Save changes, synchronize, and sleep ##
## saveChanges("localhostNode01Cell")

def saveChanges(cellName):
   AdminConfig.save()
   if (AdminConfig.showAttribute(AdminConfig.getid("/Cell:" + cellName + "/"), "cellType") == "DISTRIBUTED"):
      print "\nSynchronizing changes"
      print time.ctime()
      AdminControl.invoke(AdminControl.queryNames("type=DeploymentManager,*"), "syncActiveNodes", "true")
      print "\nSleeping 60 seconds to allow all processing to complete"
      print time.ctime()
      time.sleep(60)
   elif (AdminConfig.showAttribute(AdminConfig.getid("/Cell:" + cellName + "/"), "cellRegistered") == "true"):
      print "\nSleeping 30 seconds to allow all processing to complete"
      print time.ctime()
      time.sleep(30)
#endDef


## Convert string list to Jython list ##
## convertToList(stringList)

def convertToList(inlist):
   outlist = []
   if (len(inlist) > 0):
      if (inlist[0] == '[' and inlist[len(inlist) - 1] == ']'):
         # Handle case where configuration name contains one or more spaces
         if (inlist[1] == "\"" and inlist[len(inlist)-2] == "\""):
            clist = inlist[1:len(inlist) -1].split(")\" ")
         else:
            clist = inlist[1:len(inlist) - 1].split(" ")
      else:
         clist = inlist.split(java.lang.System.getProperty("line.separator"))
      for elem in clist:
         elem = elem.rstrip();
         if (len(elem) > 0):
            if (elem[0] == "\"" and elem[len(elem) -1] != "\""):
               elem = elem+")\""
            outlist.append(elem)
   return outlist
#endDef


# Main - Server

if(len(sys.argv) == 5):
   pbxAppPath = sys.argv[0]
   plantsAppPath = sys.argv[1]
   wsAppPath = sys.argv[2]
   cellName = AdminConfig.showAttribute(AdminConfig.getid("/Cell:/"), "name")
   nodeName = sys.argv[3]
   serverName = sys.argv[4]
   pbxAddress = "localhost"
   pbxPort = getServerPort(cellName, nodeName, serverName, "SIP_DEFAULTHOST")
elif(len(sys.argv) == 8):
   pbxAppPath = sys.argv[0]
   plantsAppPath = sys.argv[1]
   wsAppPath = sys.argv[2]
   cellName = sys.argv[3]
   nodeName = sys.argv[4]
   serverName = sys.argv[5]
   pbxAddress = sys.argv[6]
   pbxPort = sys.argv[7]
else:
   print "\nUsage:"
   print "wsadmin -lang jython -f setupCEA.py <pbx_app_path> <plants_app_path> <ws_app_path> <node_name> <server_name>"
   print "-or-"
   print "wsadmin -lang jython -f setupCEA.py <pbx_app_path> <plants_app_path> <ws_app_path> <cell_name> <node_name> <server_name> <pbx_address> <pbx_port>"
   sys.exit()

print "\nConfiguring CEA Settings"
print time.ctime()
configureCEASettingsForServer(cellName, nodeName, serverName, 'true', '30', 'SIP_CTI_GATEWAY', pbxAddress, pbxPort, 'TCP', 'false', 'ceauser', '""')

print "\nAdding host aliases as required"
print time.ctime()
addHostAlias(cellName, nodeName, serverName, "default_host", "WC_defaulthost")
addHostAlias(cellName, nodeName, serverName, "default_host", "WC_defaulthost_secure")
addHostAlias(cellName, nodeName, serverName, "default_host", "SIP_DEFAULTHOST")
addHostAlias(cellName, nodeName, serverName, "default_host", "SIP_DEFAULTHOST_SECURE")

print "\nInstalling the sample IP-PBX application"
print time.ctime()
AdminApp.install(pbxAppPath, '[-nopreCompileJSPs -distributeApp -nouseMetaDataFromBinary -nodeployejb -appname commsvc.pbx -createMBeansForResources -noreloadEnabled -nodeployws -validateinstall warn -noprocessEmbeddedConfig -filepermission .*\.dll=755#.*\.so=755#.*\.a=755#.*\.sl=755 -noallowDispatchRemoteInclude -noallowServiceRemoteInclude -asyncRequestDispatchType DISABLED -nouseAutoLink -MapModulesToServers [[CSTASipPbx commsvc.pbx.war,WEB-INF/sip.xml WebSphere:cell=' + cellName + ',node=' + nodeName + ',server=' + serverName + ' ]]]')

print "\nDefining the JDBC provider for the CEA PlantsByWebSphereAjax sample application"
print time.ctime()
jdbcProvider = AdminTask.createJDBCProvider('[-scope Cell=' + cellName + ',Node=' + nodeName + ',Server=' + serverName + ' -databaseType Derby -providerType "Derby JDBC Provider" -implementationType "XA data source" -name "Derby Provider for PlantsByWebSphereAjax (XA)" -description "Derby embedded XA JDBC Provider. This provider is only configurable in version 6.0.2 and later nodes" -classpath [${DERBY_JDBC_DRIVER_PATH}/derby.jar ] -nativePath "" ]')

print "\nDefining the data source for the CEA PlantsByWebSphereAjax sample application"
print time.ctime()
AdminTask.createDatasource(jdbcProvider, '[-name PLANTSDB -jndiName jdbc/PlantsByWebSphereAjaxDataSource -dataStoreHelperClassName com.ibm.websphere.rsadapter.DerbyDataStoreHelper -containerManagedPersistence true -componentManagedAuthenticationAlias -xaRecoveryAuthAlias -configureResourceProperties [[databaseName java.lang.String "${APP_INSTALL_ROOT}/${CELL}/PlantsByWebSphereAjax.ear/Database/PLANTSDB"]]]')

print "\nInstalling the CEA PlantsByWebSphereAjax sample application"
print time.ctime()
AdminApp.install(plantsAppPath, '[ -nopreCompileJSPs -distributeApp -nouseMetaDataFromBinary -nodeployejb -appname PlantsByWebSphereAjax -createMBeansForResources -noreloadEnabled -nodeployws -validateinstall warn -noprocessEmbeddedConfig -filepermission .*\.dll=755#.*\.so=755#.*\.a=755#.*\.sl=755 -noallowDispatchRemoteInclude -noallowServiceRemoteInclude -asyncRequestDispatchType DISABLED -nouseAutoLink -MapModulesToServers [[ "PlantsByWebSphere EJB Module" PlantsByWebSphereAjax_EJB.jar,META-INF/ejb-jar.xml WebSphere:cell=' + cellName + ',node=' + nodeName + ',server=' + serverName + ' ][ "PlantsByWebSphere Web Application" PlantsByWebSphere.war,WEB-INF/web.xml WebSphere:cell=' + cellName + ',node=' + nodeName + ',server=' + serverName + ' ]]]' )

print "\nInstalling the CEA Web services sample application"
print time.ctime()
AdminApp.install(wsAppPath, '[ -nopreCompileJSPs -distributeApp -nouseMetaDataFromBinary -nodeployejb -appname commsvc.ws.sample -createMBeansForResources -noreloadEnabled -nodeployws -validateinstall warn -noprocessEmbeddedConfig -filepermission .*\.dll=755#.*\.so=755#.*\.a=755#.*\.sl=755 -noallowDispatchRemoteInclude -noallowServiceRemoteInclude -asyncRequestDispatchType DISABLED -nouseAutoLink -MapModulesToServers [[ commsvc.ws.sample commsvc.ws.sample.war,WEB-INF/web.xml WebSphere:cell=' + cellName + ',node=' + nodeName + ',server=' + serverName + ' ]]]' )

print "\nSaving changes"
print time.ctime()
saveChanges(cellName)

if (AdminConfig.showAttribute(AdminConfig.getid("/Cell:" + cellName + "/"), "cellType") == "DISTRIBUTED"):
   print "\nStopping the application server"
   print time.ctime()
   try:
      AdminControl.stopServer(serverName, nodeName)
   except:
      pass
   print "\nStarting the application server"
   print time.ctime()
   AdminControl.startServer(serverName, nodeName)
