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

#------------------------------------------------------------------------------
# AdminCEA.py - Jython procedures for CEA settings and SIP Application Routers
#------------------------------------------------------------------------------
#
#   This script includes the following application script procedures:
#
#   Group 1: Configure CEA settings
#      Ex1:  showCEASettingsForCell
#      Ex2:  configureCEASettingsForCell
#      Ex3:  showCEASettingsForServer
#      Ex4:  configureCEASettingsForServer
#      Ex5:  showCEASettingsForCluster
#      Ex6:  configureCEASettingsForCluster
#
#   Group 2: Manage SIP application routers
#      Ex7:  showAllRouters
#      Ex8:  showDefaultRouter
#      Ex9:  showAllCustomRouters
#      Ex10: showCustomRouter
#      Ex11: createRouter
#      Ex12: modifyRouter
#      Ex13: deleteRouter
#      Ex14: moveServerToCustomRouter
#      Ex15: moveServerToDefaultRouter
#      Ex16: moveClusterToCustomRouter
#      Ex17: moveClusterToDefaultRouter
#
#---------------------------------------------------------------------

import sys
import java
import AdminUtilities

# Setting up global variables within this script
bundleName = "com.ibm.ws.scripting.resources.scriptLibraryMessage"
resourceBundle = AdminUtilities.getResourceBundle(bundleName)

## Example 1: Show cell-level CEA settings ##
## AdminCEA.showCEASettingsForCell()

def showCEASettingsForCell(failonerror=AdminUtilities._BLANK_):
   if (failonerror==AdminUtilities._BLANK_):
      failonerror=AdminUtilities._FAIL_ON_ERROR_
   #endIf
   msgPrefix = "showCEASettingsForCell("+`failonerror`+"): "

   try:
      #--------------------------------------------------------------------
      # Set up globals
      #--------------------------------------------------------------------
      global AdminApp

      #--------------------------------------------------------------------
      # Show cell-level CEA settings
      #--------------------------------------------------------------------
      print "-------------------------------------------------------------------------------"
      print "AdminCEA:     Show cell-level CEA settings"
      print " "
      print "Usage: AdminCEA.showCEASettingsForCell()"
      print " "
      print "Return: If the command is successful, settings for system application commsvc."

      # Show CEA settings for cell
      appViewList = AdminUtilities.convertToList(AdminApp.view("commsvc"))
      for ln in appViewList:
         if (ln.find("Virtual host:") > -1):
            print ln
         elif (ln.find("Context Root:") > -1):
            print ln
      print " "

   except:
      typ, val, tb = sys.exc_info()
      if (typ==SystemExit):  raise SystemExit,`val`
      if (failonerror != "true"):
         print "Exception: %s %s " % (sys.exc_type, sys.exc_value)
         val = "%s %s" % (sys.exc_type, sys.exc_value)
         raise "ScriptLibraryException: ", `val`
         return -1
      else:
         return AdminUtilities.fail(msgPrefix+AdminUtilities.getExceptionText(typ, val, tb), failonerror)
      #endIf

   #endTry

   AdminUtilities.infoNotice(AdminUtilities._OK_+msgPrefix)
   return 1  # succeed

#endDef


## Example 2: Configure cell-level CEA settings ##
## AdminCEA.configureCEASettingsForCell("/commsvc.rest", "default_host")

def configureCEASettingsForCell(contextRoot, virtualHost, failonerror=AdminUtilities._BLANK_):
   if (failonerror==AdminUtilities._BLANK_):
      failonerror=AdminUtilities._FAIL_ON_ERROR_
   #endIf
   msgPrefix = "configureCEASettingsForCell("+`contextRoot`+", "+`virtualHost`+", "+`failonerror`+"): "

   try:
      #--------------------------------------------------------------------
      # Set up globals
      #--------------------------------------------------------------------
      global AdminApp

      #--------------------------------------------------------------------
      # Configure cell-level CEA settings
      #--------------------------------------------------------------------
      print "-------------------------------------------------------------------------------"
      print "AdminCEA:     Configure cell-level CEA settings"
      print "Context root: "+contextRoot
      print "Virtual host: "+virtualHost
      print " "
      print "Usage: AdminCEA.configureCEASettingsForCell(\""+contextRoot+"\", \""+virtualHost+"\")"
      print " "
      print "Return: If the command is successful, a value of 1 is returned."
      print " "

      # Verify required parameters
      if (contextRoot == ""):
         raise AttributeError(AdminUtilities._formatNLS(resourceBundle, "WASL6041E", ["contextRoot", contextRoot]))

      if (virtualHost == ""):
         raise AttributeError(AdminUtilities._formatNLS(resourceBundle, "WASL6041E", ["virtualHost", virtualHost]))

      # Verify that virtual host exists
      vhost = AdminConfig.getid("/VirtualHost:"+virtualHost+"/")
      if (len(vhost) == 0):
         raise AttributeError(AdminUtilities._formatNLS(resourceBundle, "WASL6040E", ["virtualHost", virtualHost]))
      #endIf

      # Configure CEA settings for cell
      AdminApp.edit("commsvc", "[ -CtxRootForWebMod [[ commsvc commsvc.rest.war,WEB-INF/web.xml " + contextRoot + " ]]]" )
      AdminApp.edit("commsvc", "[ -MapWebModToVH [[ commsvc commsvc.rest.war,WEB-INF/web.xml " + virtualHost + " ]]]" )

      # Save changes if auto-save is enabled in AdminUtilities.py
      if (AdminUtilities._AUTOSAVE_ == "true"):
         AdminConfig.save()

   except:
      typ, val, tb = sys.exc_info()
      if (typ==SystemExit):  raise SystemExit,`val`
      if (failonerror != "true"):
         print "Exception: %s %s " % (sys.exc_type, sys.exc_value)
         val = "%s %s" % (sys.exc_type, sys.exc_value)
         raise "ScriptLibraryException: ", `val`
         return -1
      else:
         return AdminUtilities.fail(msgPrefix+AdminUtilities.getExceptionText(typ, val, tb), failonerror)
      #endIf

   #endTry

   AdminUtilities.infoNotice(AdminUtilities._OK_+msgPrefix)
   return 1  # succeed

#endDef


## Example 3: Show server-level CEA settings ##
## AdminCEA.showCEASettingsForServer("AppSrvCEANode01", "server1")

def showCEASettingsForServer(nodeName, serverName, failonerror=AdminUtilities._BLANK_):
   if (failonerror==AdminUtilities._BLANK_):
      failonerror=AdminUtilities._FAIL_ON_ERROR_
   #endIf
   msgPrefix = "showCEASettingsForServer("+`nodeName`+", "+`serverName`+", "+`failonerror`+"): "

   try:
      #--------------------------------------------------------------------
      # Set up globals
      #--------------------------------------------------------------------
      global AdminConfig

      #--------------------------------------------------------------------
      # Show server-level CEA settings
      #--------------------------------------------------------------------
      print "-------------------------------------------------------------------------------"
      print "AdminCEA:                       Show server-level CEA settings"
      print "Node name:                      "+nodeName
      print "Server name:                    "+serverName
      print " "
      print "Usage: AdminCEA.showCEASettingsForServer(\""+nodeName+"\", \""+serverName+"\")"
      print " "
      print "Return: If successful, CEA settings defined for the application server."
      print " "

      # Verify required parameters
      if (nodeName == ""):
         raise AttributeError(AdminUtilities._formatNLS(resourceBundle, "WASL6041E", ["nodeName", nodeName]))

      if (serverName == ""):
         raise AttributeError(AdminUtilities._formatNLS(resourceBundle, "WASL6041E", ["serverName", serverName]))

      # Verify that node exists
      node = AdminConfig.getid("/Node:"+nodeName+"/")
      if (len(node) == 0):
         raise AttributeError(AdminUtilities._formatNLS(resourceBundle, "WASL6040E", ["nodeName", nodeName]))
      #endIf

      # Verify that server exists
      server = AdminConfig.getid("/Node:"+nodeName+"/Server:"+serverName+"/")
      if (len(server) == 0):
         raise AttributeError(AdminUtilities._formatNLS(resourceBundle, "WASL6040E", ["serverName", serverName]))
      #endIf

      # Verify that server is of the appropriate type and not assigned to a cluster
      if ((AdminConfig.showAttribute(server, "serverType") != "APPLICATION_SERVER") | (AdminConfig.showAttribute(server, "clusterName") is not None)):
         raise AttributeError(AdminUtilities._formatNLS(resourceBundle, "WASL6041E", ["serverName", serverName]))
      #endIf

      # Show CEA settings for server
      deployment = AdminConfig.getid("/Deployment:commsvc/")
      deployedObject = AdminConfig.showAttribute(deployment, "deployedObject")
      rawTargetMappings = AdminConfig.showAttribute(deployedObject, "targetMappings")
      targetMappingList = AdminUtilities.convertToList(rawTargetMappings)
      for targetMapping in targetMappingList:
         currentTarget = AdminConfig.showAttribute(targetMapping, "target")
         if (currentTarget.find("ServerTarget") > 0):
            if ((AdminConfig.showAttribute(currentTarget, "nodeName") == nodeName) & (AdminConfig.showAttribute(currentTarget, "name") == serverName)):
               print "Enable CEA:                     " + AdminConfig.showAttribute(targetMapping, "enable")
      if (len(AdminConfig.getid("/Node:" + nodeName + "/Server:" + serverName + "/CEASettings:/")) == 0):
         print " "
         print "One or more CEA settings have not been defined."
         print " "
      else:
         ceaSettingsID = AdminConfig.getid("/Node:" + nodeName + "/Server:" + serverName + "/CEASettings:/")
         ctiGatewayID = AdminConfig.getid("/Node:" + nodeName + "/Server:" + serverName + "/CEASettings:/CTIGateway:/")
         commsvcID = AdminConfig.getid("/Node:" + nodeName + "/Server:" + serverName + "/CEASettings:/Commsvc:/")
         print "Maximum request hold time:      " + AdminConfig.showAttribute(commsvcID, "maxRequestHoldTime")
         print "Telephony access method:        " + AdminConfig.showAttribute(ceaSettingsID, "telephonyAccessMethod")
         print "Gateway address:                " + AdminConfig.showAttribute(ctiGatewayID, "gatewayAddress")
         print "Gateway port:                   " + AdminConfig.showAttribute(ctiGatewayID, "gatewayPort")
         print "Gateway protocol:               " + AdminConfig.showAttribute(ctiGatewayID, "gatewayProtocol")
         print "Extract user name from request: " + AdminConfig.showAttribute(ctiGatewayID, "extractUsernameFromRequest")
         print "Super user name:                " + AdminConfig.showAttribute(ctiGatewayID, "superUsername")
         print "Third-party WSDL provider:      " + AdminConfig.showAttribute(commsvcID, "thirdPartyWSDLProvider")
         print " "

   except:
      typ, val, tb = sys.exc_info()
      if (typ==SystemExit):  raise SystemExit,`val`
      if (failonerror != "true"):
         print "Exception: %s %s " % (sys.exc_type, sys.exc_value)
         val = "%s %s" % (sys.exc_type, sys.exc_value)
         raise "ScriptLibraryException: ", `val`
         return -1
      else:
         return AdminUtilities.fail(msgPrefix+AdminUtilities.getExceptionText(typ, val, tb), failonerror)
      #endIf

   #endTry

   AdminUtilities.infoNotice(AdminUtilities._OK_+msgPrefix)
   return 1  # succeed

#endDef


## Example 4: Configure server-level CEA settings ##
## AdminCEA.configureCEASettingsForServer("AppSrvCEANode01", "server1", "false | true", "30", "SIP_CTI_GATEWAY | THIRD_PARTY_WEB_SERVICE", "localhost", "5060", "TCP | UDP | TLS", "false | true", "ceauser", '""')

def configureCEASettingsForServer(nodeName, serverName, enableCEA, maxRequestHoldTime, telephonyAccessMethod, gatewayAddress, gatewayPort, gatewayProtocol, extractUsernameFromRequest, superUsername, thirdPartyWSDLProvider, failonerror=AdminUtilities._BLANK_):
   if (failonerror==AdminUtilities._BLANK_):
      failonerror=AdminUtilities._FAIL_ON_ERROR_
   #endIf
   msgPrefix = "configureCEASettingsForServer("+`nodeName`+", "+`serverName`+", "+`enableCEA`+", "+`maxRequestHoldTime`+", "+`telephonyAccessMethod`+", "+`gatewayAddress`+", "+`gatewayPort`+", "+`gatewayProtocol`+", "+`extractUsernameFromRequest`+", "+`superUsername`+", "+`thirdPartyWSDLProvider`+", "+`failonerror`+"): "

   try:
      #--------------------------------------------------------------------
      # Set up globals
      #--------------------------------------------------------------------
      global AdminConfig

      #--------------------------------------------------------------------
      # Configure server-level CEA settings
      #--------------------------------------------------------------------
      print "-------------------------------------------------------------------------------"
      print "AdminCEA:                       Configure server-level CEA settings"
      print "Node name:                      "+nodeName
      print "Server name:                    "+serverName
      print "Enable CEA:                     "+enableCEA
      print "Max request hold time:          "+maxRequestHoldTime
      print "Telephony access method:        "+telephonyAccessMethod
      print "Gateway address:                "+gatewayAddress
      print "Gateway port:                   "+gatewayPort
      print "Gateway protocol:               "+gatewayProtocol
      print "Extract user name from request: "+extractUsernameFromRequest
      print "Super user name:                "+superUsername
      print "Third-party WSDL provider:      "+thirdPartyWSDLProvider
      print " "
      print "Usage: AdminCEA.configureCEASettingsForServer(\""+nodeName+"\", \""+serverName+"\", \""+enableCEA+"\", \""+maxRequestHoldTime+"\", \""+telephonyAccessMethod+"\", \""+gatewayAddress+"\", \""+gatewayPort+"\", \""+gatewayProtocol+"\", \""+extractUsernameFromRequest+"\", \""+superUsername+"\", \""+thirdPartyWSDLProvider+"\")"
      print " "
      print "Return: If the command is successful, a value of 1 is returned."
      print " "

      # Verify required parameters
      if (nodeName == ""):
         raise AttributeError(AdminUtilities._formatNLS(resourceBundle, "WASL6041E", ["nodeName", nodeName]))

      if (serverName == ""):
         raise AttributeError(AdminUtilities._formatNLS(resourceBundle, "WASL6041E", ["serverName", serverName]))

      if (enableCEA == ""):
         raise AttributeError(AdminUtilities._formatNLS(resourceBundle, "WASL6041E", ["enableCEA", enableCEA]))

      if (maxRequestHoldTime == ""):
         raise AttributeError(AdminUtilities._formatNLS(resourceBundle, "WASL6041E", ["maxRequestHoldTime", maxRequestHoldTime]))

      if (telephonyAccessMethod == ""):
         raise AttributeError(AdminUtilities._formatNLS(resourceBundle, "WASL6041E", ["telephonyAccessMethod", telephonyAccessMethod]))

      if (gatewayAddress == ""):
         raise AttributeError(AdminUtilities._formatNLS(resourceBundle, "WASL6041E", ["gatewayAddress", gatewayAddress]))

      if (gatewayPort == ""):
         raise AttributeError(AdminUtilities._formatNLS(resourceBundle, "WASL6041E", ["gatewayPort", gatewayPort]))

      if (gatewayProtocol == ""):
         raise AttributeError(AdminUtilities._formatNLS(resourceBundle, "WASL6041E", ["gatewayProtocol", gatewayProtocol]))

      if (extractUsernameFromRequest == ""):
         raise AttributeError(AdminUtilities._formatNLS(resourceBundle, "WASL6041E", ["extractUsernameFromRequest", extractUsernameFromRequest]))

      if (superUsername == ""):
         raise AttributeError(AdminUtilities._formatNLS(resourceBundle, "WASL6041E", ["superUsername", superUsername]))

      if (thirdPartyWSDLProvider == ""):
         raise AttributeError(AdminUtilities._formatNLS(resourceBundle, "WASL6041E", ["thirdPartyWSDLProvider", thirdPartyWSDLProvider]))

      # Verify that node exists
      node = AdminConfig.getid("/Node:"+nodeName+"/")
      if (len(node) == 0):
         raise AttributeError(AdminUtilities._formatNLS(resourceBundle, "WASL6040E", ["nodeName", nodeName]))
      #endIf

      # Verify that server exists
      server = AdminConfig.getid("/Node:"+nodeName+"/Server:"+serverName+"/")
      if (len(server) == 0):
         raise AttributeError(AdminUtilities._formatNLS(resourceBundle, "WASL6040E", ["serverName", serverName]))
      #endIf

      # Verify that server is of the appropriate type and not assigned to a cluster
      if ((AdminConfig.showAttribute(server, "serverType") != "APPLICATION_SERVER") | (AdminConfig.showAttribute(server, "clusterName") is not None)):
         raise AttributeError(AdminUtilities._formatNLS(resourceBundle, "WASL6041E", ["serverName", serverName]))
      #endIf

      # Configure CEA settings for server
      deployment = AdminConfig.getid("/Deployment:commsvc/")
      deployedObject = AdminConfig.showAttribute(deployment, "deployedObject")
      rawTargetMappings = AdminConfig.showAttribute(deployedObject, "targetMappings")
      targetMappingList = AdminUtilities.convertToList(rawTargetMappings)
      for targetMapping in targetMappingList:
         currentTarget = AdminConfig.showAttribute(targetMapping, "target")
         if (currentTarget.find("ServerTarget") > 0):
            if ((AdminConfig.showAttribute(currentTarget, "nodeName") == nodeName) & (AdminConfig.showAttribute(currentTarget, "name") == serverName)):
               AdminConfig.modify(targetMapping, "[[enable " + enableCEA + "]]")
      if (len(AdminConfig.getid("/Node:" + nodeName + "/Server:" + serverName + "/CEASettings:/")) == 0):
         ceaSettingsID = AdminConfig.create("CEASettings", AdminConfig.getid("/Node:" + nodeName + "/Server:" + serverName + "/"), "[[telephonyAccessMethod " + telephonyAccessMethod + "]]")
         AdminConfig.create("CTIGateway", ceaSettingsID, "[[gatewayAddress " + gatewayAddress + "] [gatewayPort " + gatewayPort + "] [gatewayProtocol " + gatewayProtocol + "] [extractUsernameFromRequest " + extractUsernameFromRequest + "] [superUsername " + superUsername + "]]")
         AdminConfig.create("Commsvc", ceaSettingsID, "[[maxRequestHoldTime " + maxRequestHoldTime + "] [thirdPartyWSDLProvider " + thirdPartyWSDLProvider + "]]")
      else:
         AdminConfig.modify(AdminConfig.getid("/Node:" + nodeName + "/Server:" + serverName + "/CEASettings:/"), "[[telephonyAccessMethod " + telephonyAccessMethod + "]]")
         AdminConfig.modify(AdminConfig.getid("/Node:" + nodeName + "/Server:" + serverName + "/CEASettings:/CTIGateway:/"), "[[gatewayAddress " + gatewayAddress + "] [gatewayPort " + gatewayPort + "] [gatewayProtocol " + gatewayProtocol + "] [extractUsernameFromRequest " + extractUsernameFromRequest + "] [superUsername " + superUsername + "]]")
         AdminConfig.modify(AdminConfig.getid("/Node:" + nodeName + "/Server:" + serverName + "/CEASettings:/Commsvc:/"), "[[maxRequestHoldTime " + maxRequestHoldTime + "] [thirdPartyWSDLProvider " + thirdPartyWSDLProvider + "]]")

      # Save changes if auto-save is enabled in AdminUtilities.py
      if (AdminUtilities._AUTOSAVE_ == "true"):
         AdminConfig.save()

   except:
      typ, val, tb = sys.exc_info()
      if (typ==SystemExit):  raise SystemExit,`val`
      if (failonerror != "true"):
         print "Exception: %s %s " % (sys.exc_type, sys.exc_value)
         val = "%s %s" % (sys.exc_type, sys.exc_value)
         raise "ScriptLibraryException: ", `val`
         return -1
      else:
         return AdminUtilities.fail(msgPrefix+AdminUtilities.getExceptionText(typ, val, tb), failonerror)
      #endIf

   #endTry

   AdminUtilities.infoNotice(AdminUtilities._OK_+msgPrefix)
   return 1  # succeed

#endDef


## Example 5: Show cluster-level CEA settings ##
## AdminCEA.showCEASettingsForCluster("cluster1")

def showCEASettingsForCluster(clusterName, failonerror=AdminUtilities._BLANK_):
   if (failonerror==AdminUtilities._BLANK_):
      failonerror=AdminUtilities._FAIL_ON_ERROR_
   #endIf
   msgPrefix = "showCEASettingsForCluster("+`clusterName`+", "+`failonerror`+"): "

   try:
      #--------------------------------------------------------------------
      # Set up globals
      #--------------------------------------------------------------------
      global AdminConfig

      #--------------------------------------------------------------------
      # Show cluster-level CEA settings
      #--------------------------------------------------------------------
      print "-------------------------------------------------------------------------------"
      print "AdminCEA:                       Show cluster-level CEA settings"
      print "Cluster name:                   "+clusterName
      print " "
      print "Usage: AdminCEA.showCEASettingsForCluster(\""+clusterName+"\")"
      print " "
      print "Return: If the command is successful, CEA settings defined for the cluster."
      print " "

      # Verify required parameters
      if (clusterName == ""):
         raise AttributeError(AdminUtilities._formatNLS(resourceBundle, "WASL6041E", ["clusterName", clusterName]))

      # Verify that cluster exists
      cluster = AdminConfig.getid("/ServerCluster:"+clusterName+"/")
      if (len(cluster) == 0):
         raise AttributeError(AdminUtilities._formatNLS(resourceBundle, "WASL6040E", ["clusterName", clusterName]))
      #endIf

      # Show CEA settings for cluster
      deployment = AdminConfig.getid("/Deployment:commsvc/")
      deployedObject = AdminConfig.showAttribute(deployment, "deployedObject")
      rawTargetMappings = AdminConfig.showAttribute(deployedObject, "targetMappings")
      targetMappingList = AdminUtilities.convertToList(rawTargetMappings)
      for targetMapping in targetMappingList:
         currentTarget = AdminConfig.showAttribute(targetMapping, "target")
         if (currentTarget.find("ClusteredTarget") > 0):
            if (AdminConfig.showAttribute(currentTarget, "name") == clusterName):
               print "Enable CEA:                     " + AdminConfig.showAttribute(targetMapping, "enable")
      if (len(AdminConfig.getid("/ServerCluster:" + clusterName + "/CEASettings:/")) == 0):
         print " "
         print "One or more CEA settings have not been defined."
         print " "
      else:
         ceaSettingsID = AdminConfig.getid("/ServerCluster:" + clusterName + "/CEASettings:/")
         ctiGatewayID = AdminConfig.getid("/ServerCluster:" + clusterName + "/CEASettings:/CTIGateway:/")
         commsvcID = AdminConfig.getid("/ServerCluster:" + clusterName + "/CEASettings:/Commsvc:/")
         print "Maximum request hold time:      " + AdminConfig.showAttribute(commsvcID, "maxRequestHoldTime")
         print "Telephony access method:        " + AdminConfig.showAttribute(ceaSettingsID, "telephonyAccessMethod")
         print "Gateway address:                " + AdminConfig.showAttribute(ctiGatewayID, "gatewayAddress")
         print "Gateway port:                   " + AdminConfig.showAttribute(ctiGatewayID, "gatewayPort")
         print "Gateway protocol:               " + AdminConfig.showAttribute(ctiGatewayID, "gatewayProtocol")
         print "Extract user name from request: " + AdminConfig.showAttribute(ctiGatewayID, "extractUsernameFromRequest")
         print "Super user name:                " + AdminConfig.showAttribute(ctiGatewayID, "superUsername")
         print "Third-party WSDL provider:      " + AdminConfig.showAttribute(commsvcID, "thirdPartyWSDLProvider")
         print " "

   except:
      typ, val, tb = sys.exc_info()
      if (typ==SystemExit):  raise SystemExit,`val`
      if (failonerror != "true"):
         print "Exception: %s %s " % (sys.exc_type, sys.exc_value)
         val = "%s %s" % (sys.exc_type, sys.exc_value)
         raise "ScriptLibraryException: ", `val`
         return -1
      else:
         return AdminUtilities.fail(msgPrefix+AdminUtilities.getExceptionText(typ, val, tb), failonerror)
      #endIf

   #endTry

   AdminUtilities.infoNotice(AdminUtilities._OK_+msgPrefix)
   return 1  # succeed

#endDef


## Example 6: Configure cluster-level CEA settings ##
## AdminCEA.configureCEASettingsForCluster("cluster1", "false | true", "30", "SIP_CTI_GATEWAY | THIRD_PARTY_WEB_SERVICE", "localhost", "5060", "TCP | UDP | TLS", "false | true", "ceauser", '""')

def configureCEASettingsForCluster(clusterName, enableCEA, maxRequestHoldTime, telephonyAccessMethod, gatewayAddress, gatewayPort, gatewayProtocol, extractUsernameFromRequest, superUsername, thirdPartyWSDLProvider, failonerror=AdminUtilities._BLANK_):
   if (failonerror==AdminUtilities._BLANK_):
      failonerror=AdminUtilities._FAIL_ON_ERROR_
   #endIf
   msgPrefix = "configureCEASettingsForCluster("+`clusterName`+", "+`enableCEA`+", "+`maxRequestHoldTime`+", "+`telephonyAccessMethod`+", "+`gatewayAddress`+", "+`gatewayPort`+", "+`gatewayProtocol`+", "+`extractUsernameFromRequest`+", "+`superUsername`+", "+`thirdPartyWSDLProvider`+", "+`failonerror`+"): "

   try:
      #--------------------------------------------------------------------
      # Set up globals
      #--------------------------------------------------------------------
      global AdminConfig

      #--------------------------------------------------------------------
      # Configure cluster-level CEA settings
      #--------------------------------------------------------------------
      print "-------------------------------------------------------------------------------"
      print "AdminCEA:                       Configure cluster-level CEA settings"
      print "Cluster name:                   "+clusterName
      print "Enable CEA:                     "+enableCEA
      print "Max request hold time:          "+maxRequestHoldTime
      print "Telephony access method:        "+telephonyAccessMethod
      print "Gateway address:                "+gatewayAddress
      print "Gateway port:                   "+gatewayPort
      print "Gateway protocol:               "+gatewayProtocol
      print "Extract user name from request: "+extractUsernameFromRequest
      print "Super user name:                "+superUsername
      print "Third-party WSDL provider:      "+thirdPartyWSDLProvider
      print " "
      print "Usage: AdminCEA.configureCEASettingsForCluster(\""+clusterName+"\", \""+enableCEA+"\", \""+maxRequestHoldTime+"\", \""+telephonyAccessMethod+"\", \""+gatewayAddress+"\", \""+gatewayPort+"\", \""+gatewayProtocol+"\", \""+extractUsernameFromRequest+"\", \""+superUsername+"\", \""+thirdPartyWSDLProvider+"\")"
      print " "
      print "Return: If the command is successful, a value of 1 is returned."
      print " "

      # Verify required parameters
      if (clusterName == ""):
         raise AttributeError(AdminUtilities._formatNLS(resourceBundle, "WASL6041E", ["clusterName", clusterName]))

      if (enableCEA == ""):
         raise AttributeError(AdminUtilities._formatNLS(resourceBundle, "WASL6041E", ["enableCEA", enableCEA]))

      if (maxRequestHoldTime == ""):
         raise AttributeError(AdminUtilities._formatNLS(resourceBundle, "WASL6041E", ["maxRequestHoldTime", maxRequestHoldTime]))

      if (telephonyAccessMethod == ""):
         raise AttributeError(AdminUtilities._formatNLS(resourceBundle, "WASL6041E", ["telephonyAccessMethod", telephonyAccessMethod]))

      if (gatewayAddress == ""):
         raise AttributeError(AdminUtilities._formatNLS(resourceBundle, "WASL6041E", ["gatewayAddress", gatewayAddress]))

      if (gatewayPort == ""):
         raise AttributeError(AdminUtilities._formatNLS(resourceBundle, "WASL6041E", ["gatewayPort", gatewayPort]))

      if (gatewayProtocol == ""):
         raise AttributeError(AdminUtilities._formatNLS(resourceBundle, "WASL6041E", ["gatewayProtocol", gatewayProtocol]))

      if (extractUsernameFromRequest == ""):
         raise AttributeError(AdminUtilities._formatNLS(resourceBundle, "WASL6041E", ["extractUsernameFromRequest", extractUsernameFromRequest]))

      if (superUsername == ""):
         raise AttributeError(AdminUtilities._formatNLS(resourceBundle, "WASL6041E", ["superUsername", superUsername]))

      if (thirdPartyWSDLProvider == ""):
         raise AttributeError(AdminUtilities._formatNLS(resourceBundle, "WASL6041E", ["thirdPartyWSDLProvider", thirdPartyWSDLProvider]))

      # Verify that cluster exists
      cluster = AdminConfig.getid("/ServerCluster:"+clusterName+"/")
      if (len(cluster) == 0):
         raise AttributeError(AdminUtilities._formatNLS(resourceBundle, "WASL6040E", ["clusterName", clusterName]))
      #endIf

      # Configure CEA settings for cluster
      deployment = AdminConfig.getid("/Deployment:commsvc/")
      deployedObject = AdminConfig.showAttribute(deployment, "deployedObject")
      rawTargetMappings = AdminConfig.showAttribute(deployedObject, "targetMappings")
      targetMappingList = AdminUtilities.convertToList(rawTargetMappings)
      for targetMapping in targetMappingList:
         currentTarget = AdminConfig.showAttribute(targetMapping, "target")
         if (currentTarget.find("ClusteredTarget") > 0):
            if (AdminConfig.showAttribute(currentTarget, "name") == clusterName):
               AdminConfig.modify(targetMapping, "[[enable " + enableCEA + "]]")
      if (len(AdminConfig.getid("/ServerCluster:" + clusterName + "/CEASettings:/")) == 0):
         ceaSettingsID = AdminConfig.create("CEASettings", AdminConfig.getid("/ServerCluster:" + clusterName + "/"), "[[telephonyAccessMethod " + telephonyAccessMethod + "]]")
         AdminConfig.create("CTIGateway", ceaSettingsID, "[[gatewayAddress " + gatewayAddress + "] [gatewayPort " + gatewayPort + "] [gatewayProtocol " + gatewayProtocol + "] [extractUsernameFromRequest " + extractUsernameFromRequest + "] [superUsername " + superUsername + "]]")
         AdminConfig.create("Commsvc", ceaSettingsID, "[[maxRequestHoldTime " + maxRequestHoldTime + "] [thirdPartyWSDLProvider " + thirdPartyWSDLProvider + "]]")
      else:
         AdminConfig.modify(AdminConfig.getid("/ServerCluster:" + clusterName + "/CEASettings:/"), "[[telephonyAccessMethod " + telephonyAccessMethod + "]]")
         AdminConfig.modify(AdminConfig.getid("/ServerCluster:" + clusterName + "/CEASettings:/CTIGateway:/"), "[[gatewayAddress " + gatewayAddress + "] [gatewayPort " + gatewayPort + "] [gatewayProtocol " + gatewayProtocol + "] [extractUsernameFromRequest " + extractUsernameFromRequest + "] [superUsername " + superUsername + "]]")
         AdminConfig.modify(AdminConfig.getid("/ServerCluster:" + clusterName + "/CEASettings:/Commsvc:/"), "[[maxRequestHoldTime " + maxRequestHoldTime + "] [thirdPartyWSDLProvider " + thirdPartyWSDLProvider + "]]")

      # Save changes if auto-save is enabled in AdminUtilities.py
      if (AdminUtilities._AUTOSAVE_ == "true"):
         AdminConfig.save()

   except:
      typ, val, tb = sys.exc_info()
      if (typ==SystemExit):  raise SystemExit,`val`
      if (failonerror != "true"):
         print "Exception: %s %s " % (sys.exc_type, sys.exc_value)
         val = "%s %s" % (sys.exc_type, sys.exc_value)
         raise "ScriptLibraryException: ", `val`
         return -1
      else:
         return AdminUtilities.fail(msgPrefix+AdminUtilities.getExceptionText(typ, val, tb), failonerror)
      #endIf

   #endTry

   AdminUtilities.infoNotice(AdminUtilities._OK_+msgPrefix)
   return 1  # succeed

#endDef


## Example 7: Show key attributes of all SIP Application Routers ##
## AdminCEA.showAllRouters()

def showAllRouters(failonerror=AdminUtilities._BLANK_):
   #--------------------------------------------------------------------
   # Set up globals
   #--------------------------------------------------------------------
   global AdminConfig

   #--------------------------------------------------------------------
   # Show key attributes of all SIP Application Routers
   #--------------------------------------------------------------------
   print "-------------------------------------------------------------------------------"
   print "AdminCEA: Show key attributes of all SIP Application Routers"
   print " "
   print "Usage: AdminCEA.showAllRouters()"
   print " "
   print "Return: Output of calls to showDefaultRouter() and showAllCustomRouters()."

   # Show key attributes of the default router
   showDefaultRouter(failonerror)

   # Show key attributes of all custom routers
   showAllCustomRouters(failonerror)

#endDef


## Example 8: Show key attributes of the default SIP application router ##
## AdminCEA.showDefaultRouter()

def showDefaultRouter(failonerror=AdminUtilities._BLANK_):
   if (failonerror==AdminUtilities._BLANK_):
      failonerror=AdminUtilities._FAIL_ON_ERROR_
   #endIf
   msgPrefix = "showDefaultRouter("+`failonerror`+"): "

   try:
      #--------------------------------------------------------------------
      # Set up globals
      #--------------------------------------------------------------------
      global AdminConfig

      #--------------------------------------------------------------------
      # Show key attributes of the default SIP application router
      #--------------------------------------------------------------------
      print "-------------------------------------------------------------------------------"
      print "AdminCEA: Show key attributes of the default SIP application router"
      print " "
      print "Usage: AdminCEA.showDefaultRouter()"
      print " "
      print "Return: If successful, key attributes of the default SIP application router."

      # Correct format of base SAR objects (if necessary)
      if (len(AdminConfig.list("SIPApplicationRouters")) == 0):
         AdminConfig.create("SIPApplicationRouters", AdminConfig.getid("/Cell:/"), [])
         AdminConfig.create("DefaultSIPApplicationRouter", AdminConfig.getid("/SIPApplicationRouters:/"), [])

      # Show key attributes of default router

      # Create list of clusters assigned to default router
      rawAllClusters = AdminConfig.getid("/ServerCluster:/")
      darClusterList = AdminUtilities.convertToList(rawAllClusters)
      rawClusterTargets = AdminConfig.getid("/SARClusterTarget:/")
      clusterTargetList = AdminUtilities.convertToList(rawClusterTargets)
      if (len(clusterTargetList) > 0):
         for clusterTarget in clusterTargetList:
            clusterName = AdminConfig.showAttribute(clusterTarget, "name")
            cluster = AdminConfig.getid("/ServerCluster:" + clusterName + "/")
            darClusterList.remove(cluster)

      # Create list of servers assigned to the default router
      darServerList = []

      # Add application servers that are not members of a cluster
      rawAllServers = AdminConfig.getid("/Server:/")
      allServerList = AdminUtilities.convertToList(rawAllServers)
      if (len(allServerList) > 0):
         for server in allServerList:
            if (AdminConfig.showAttribute(server, "serverType") == "APPLICATION_SERVER"):
               if (AdminConfig.showAttribute(server, "clusterName") is None):
                  darServerList.append(server)

      # Remove application servers assigned to a custom router
      rawServerTargets = AdminConfig.getid("/SARServerTarget:/")
      serverTargetList = AdminUtilities.convertToList(rawServerTargets)
      if (len(serverTargetList) > 0):
         for serverTarget in serverTargetList:
            nodeName = AdminConfig.showAttribute(serverTarget, "nodeName")
            serverName = AdminConfig.showAttribute(serverTarget, "name")
            server = AdminConfig.getid("/Node:" + nodeName + "/Server:" + serverName + "/")
            darServerList.remove(server)

      print "\nRouter: DefaultSIPApplicationRouter"
      print "\nTargets and Application Startup Order:"
      if ((len(darClusterList) > 0) | (len(darServerList) > 0)):
         cellName = AdminConfig.showAttribute(AdminConfig.getid("/Cell:/"), "name")
         if (len(darClusterList) > 0):
            for cluster in darClusterList:
               clusterName = AdminConfig.showAttribute(cluster, "name")
               print "\n/ServerCluster:" + clusterName + "/"
               scope = "WebSphere:cell=" + cellName + ",cluster=" + clusterName
               apps = AdminApp.list(scope)
               apps = AdminUtilities.convertToList(apps)
               if (len(apps) > 0):
                  for app in apps:
                     deployment = AdminConfig.getid("/Deployment:"+app+"/")
                     appDeployment = AdminConfig.showAttribute(deployment, "deployedObject")
                     weight = AdminConfig.showAttribute(appDeployment, "startingWeight")
                     print "   " + app + " (" + weight + ")"
               else:
                  print "   No Applications Deployed"
         if (len(darServerList) > 0):
            for server in darServerList:
               serverName = server[0:server.find("(")]
               nodeName = server[server.find("nodes/")+6:server.find("servers/")-1]
               print "\n/Node:" + nodeName + "/Server:" + serverName + "/"
               scope = "WebSphere:cell=" + cellName + ",node=" + nodeName + ",server=" + serverName
               apps = AdminApp.list(scope)
               apps = AdminUtilities.convertToList(apps)
               if (len(apps) > 0):
                  for app in apps:
                     deployment = AdminConfig.getid("/Deployment:"+app+"/")
                     appDeployment = AdminConfig.showAttribute(deployment, "deployedObject")
                     weight = AdminConfig.showAttribute(appDeployment, "startingWeight")
                     print "   " + app + " (" + weight + ")"
               else:
                  print "   No Applications Deployed"

         print "\nUse the following command to modify the application startup order:"
         print "AdminApplication.configureStartingWeightForAnApplication(app, weight)"
      else:
         print "None"

   except:
      typ, val, tb = sys.exc_info()
      if (typ==SystemExit):  raise SystemExit,`val`
      if (failonerror != "true"):
         print "Exception: %s %s " % (sys.exc_type, sys.exc_value)
         val = "%s %s" % (sys.exc_type, sys.exc_value)
         raise "ScriptLibraryException: ", `val`
         return -1
      else:
         return AdminUtilities.fail(msgPrefix+AdminUtilities.getExceptionText(typ, val, tb), failonerror)
      #endIf

   #endTry

   print " "
   AdminUtilities.infoNotice(AdminUtilities._OK_+msgPrefix)

#endDef


## Example 9: Show key attributes of all custom SIP Application Routers ##
## AdminCEA.showAllCustomRouters()

def showAllCustomRouters(failonerror=AdminUtilities._BLANK_):
   if (failonerror==AdminUtilities._BLANK_):
      failonerror=AdminUtilities._FAIL_ON_ERROR_
   #endIf
   msgPrefix = "showAllCustomRouters("+`failonerror`+"): "

   try:
      #--------------------------------------------------------------------
      # Set up globals
      #--------------------------------------------------------------------
      global AdminConfig

      #--------------------------------------------------------------------
      # Show key attributes of all custom SIP Application Routers
      #--------------------------------------------------------------------
      print "-------------------------------------------------------------------------------"
      print "AdminCEA: Show key attributes of all custom SIP Application Routers"
      print " "
      print "Usage: AdminCEA.showAllCustomRouters()"
      print " "
      print "Return: If successful, key attributes of all custom SIP Application Routers."

      # Correct format of base SAR objects (if necessary)
      if (len(AdminConfig.list("SIPApplicationRouters")) == 0):
         AdminConfig.create("SIPApplicationRouters", AdminConfig.getid("/Cell:/"), [])
         AdminConfig.create("DefaultSIPApplicationRouter", AdminConfig.getid("/SIPApplicationRouters:/"), [])

      # Show key attributes of all custom routers
      rawRouters = AdminConfig.getid("/SIPApplicationRouter:/")
      routerList = AdminUtilities.convertToList(rawRouters)
      if (len(routerList) > 0):
         for router in routerList:
            print "\nRouter: " + AdminConfig.showAttribute(router, "name")
            print "\nProvider: " + AdminConfig.showAttribute(router, "sipApplicationRouterProvider")
            print "\nTargets:"
            rawTargets = AdminConfig.showAttribute(router, "targets")
            targetList = AdminUtilities.convertToList(rawTargets)
            if (len(targetList) == 0):
               print "None"
            else:
               for target in targetList:
                  if (target.find("ClusterTarget") > 0):
                     print "/ServerCluster:" + AdminConfig.showAttribute(target, "name") + "/"
               for target in targetList:
                  if (target.find("ServerTarget") > 0):
                     print "/Node:" + AdminConfig.showAttribute(target, "nodeName") + "/Server:" + AdminConfig.showAttribute(target, "name") + "/"
      else:
         print "\nNo custom routers exist"

   except:
      typ, val, tb = sys.exc_info()
      if (typ==SystemExit):  raise SystemExit,`val`
      if (failonerror != "true"):
         print "Exception: %s %s " % (sys.exc_type, sys.exc_value)
         val = "%s %s" % (sys.exc_type, sys.exc_value)
         raise "ScriptLibraryException: ", `val`
         return -1
      else:
         return AdminUtilities.fail(msgPrefix+AdminUtilities.getExceptionText(typ, val, tb), failonerror)
      #endIf

   #endTry

   print " "
   AdminUtilities.infoNotice(AdminUtilities._OK_+msgPrefix)

#endDef


## Example 10: Show key attributes of a custom SIP application router ##
## AdminCEA.showCustomRouter("RouterOne")

def showCustomRouter(routerName, failonerror=AdminUtilities._BLANK_):
   if (failonerror==AdminUtilities._BLANK_):
      failonerror=AdminUtilities._FAIL_ON_ERROR_
   #endIf
   msgPrefix = "showCustomRouter("+`routerName`+", "+`failonerror`+"): "

   try:
      #--------------------------------------------------------------------
      # Set up globals
      #--------------------------------------------------------------------
      global AdminConfig

      #--------------------------------------------------------------------
      # Show key attributes of a custom SIP application router
      #--------------------------------------------------------------------
      print "-------------------------------------------------------------------------------"
      print "AdminCEA:    Show key attributes of a custom SIP application router"
      print "Router name: "+routerName
      print " "
      print "Usage: AdminCEA.showCustomRouter(\""+routerName+"\")"
      print " "
      print "Return: If successful, key attributes of a custom SIP application router."

      # Correct format of base SAR objects (if necessary)
      if (len(AdminConfig.list("SIPApplicationRouters")) == 0):
         AdminConfig.create("SIPApplicationRouters", AdminConfig.getid("/Cell:/"), [])
         AdminConfig.create("DefaultSIPApplicationRouter", AdminConfig.getid("/SIPApplicationRouters:/"), [])

      # Verify required parameters
      if (routerName == ""):
         raise AttributeError(AdminUtilities._formatNLS(resourceBundle, "WASL6041E", ["routerName", routerName]))

      # Verify that router exists
      router = AdminConfig.getid("/SIPApplicationRouter:" + routerName + "/")
      if (len(router) == 0):
         raise AttributeError(AdminUtilities._formatNLS(resourceBundle, "WASL6040E", ["routerName", routerName]))
      #endIf

      # Show key attributes of custom router
      print "\nRouter: " + AdminConfig.showAttribute(router, "name")
      print "\nProvider: " + AdminConfig.showAttribute(router, "sipApplicationRouterProvider")
      print "\nTargets:"
      rawTargets = AdminConfig.showAttribute(router, "targets")
      targetList = AdminUtilities.convertToList(rawTargets)
      if (len(targetList) == 0):
         print "None"
      else:
         for target in targetList:
            if (target.find("ClusterTarget") > 0):
               print "/ServerCluster:" + AdminConfig.showAttribute(target, "name") + "/"
         for target in targetList:
            if (target.find("ServerTarget") > 0):
               print "/Node:" + AdminConfig.showAttribute(target, "nodeName") + "/Server:" + AdminConfig.showAttribute(target, "name") + "/"

   except:
      typ, val, tb = sys.exc_info()
      if (typ==SystemExit):  raise SystemExit,`val`
      if (failonerror != "true"):
         print "Exception: %s %s " % (sys.exc_type, sys.exc_value)
         val = "%s %s" % (sys.exc_type, sys.exc_value)
         raise "ScriptLibraryException: ", `val`
         return -1
      else:
         return AdminUtilities.fail(msgPrefix+AdminUtilities.getExceptionText(typ, val, tb), failonerror)
      #endIf

   #endTry

   print " "
   AdminUtilities.infoNotice(AdminUtilities._OK_+msgPrefix)

#endDef


## Example 11: Create a new custom SIP Application Router ##
## AdminCEA.createRouter("RouterOne", "RouterProviderOne")

def createRouter(routerName, routerProvider, failonerror=AdminUtilities._BLANK_):
   if (failonerror==AdminUtilities._BLANK_):
      failonerror=AdminUtilities._FAIL_ON_ERROR_
   #endIf
   msgPrefix = "createRouter("+`routerName`+", "+`routerProvider`+", "+`failonerror`+"): "

   try:
      #--------------------------------------------------------------------
      # Set up globals
      #--------------------------------------------------------------------
      global AdminConfig

      #--------------------------------------------------------------------
      # Create a new custom SIP Application Router
      #--------------------------------------------------------------------
      print "-------------------------------------------------------------------------------"
      print "AdminCEA:        Create a new custom SIP Application Router"
      print "Router name:     "+routerName
      print "Router provider: "+routerProvider
      print " "
      print "Usage: AdminCEA.createRouter(\""+routerName+"\", \""+routerProvider+"\")"
      print " "
      print "Return: If the command is successful, a value of 1 is returned."
      print " "

      # Correct format of base SAR objects (if necessary)
      if (len(AdminConfig.list("SIPApplicationRouters")) == 0):
         AdminConfig.create("SIPApplicationRouters", AdminConfig.getid("/Cell:/"), [])
         AdminConfig.create("DefaultSIPApplicationRouter", AdminConfig.getid("/SIPApplicationRouters:/"), [])

      # Verify required parameters
      if (routerName == ""):
         raise AttributeError(AdminUtilities._formatNLS(resourceBundle, "WASL6041E", ["routerName", routerName]))

      if (routerProvider == ""):
         raise AttributeError(AdminUtilities._formatNLS(resourceBundle, "WASL6041E", ["routerProvider", routerProvider]))

      # Verify that router does not already exist
      router = AdminConfig.getid("/SIPApplicationRouter:" + routerName + "/")
      if (len(router) > 0):
         raise AttributeError(AdminUtilities._formatNLS(resourceBundle, "WASL6046E", [routerName]))
      #endIf

      # Create the router
      AdminConfig.create("SIPApplicationRouter", AdminConfig.getid("/SIPApplicationRouters:/"), "[[name " + routerName + "] [sipApplicationRouterProvider " + routerProvider + "]]")

      # Save changes if auto-save is enabled in AdminUtilities.py
      if (AdminUtilities._AUTOSAVE_ == "true"):
         AdminConfig.save()

   except:
      typ, val, tb = sys.exc_info()
      if (typ==SystemExit):  raise SystemExit,`val`
      if (failonerror != "true"):
         print "Exception: %s %s " % (sys.exc_type, sys.exc_value)
         val = "%s %s" % (sys.exc_type, sys.exc_value)
         raise "ScriptLibraryException: ", `val`
         return -1
      else:
         return AdminUtilities.fail(msgPrefix+AdminUtilities.getExceptionText(typ, val, tb), failonerror)
      #endIf

   #endTry

   AdminUtilities.infoNotice(AdminUtilities._OK_+msgPrefix)
   return 1  # succeed

#endDef


## Example 12: Modify the name and provider of a SIP Application Router ##
## AdminCEA.modifyRouter("RouterOne", "Router1", "RouterProvider1")

def modifyRouter(routerName, newRouterName, newRouterProvider, failonerror=AdminUtilities._BLANK_):
   if (failonerror==AdminUtilities._BLANK_):
      failonerror=AdminUtilities._FAIL_ON_ERROR_
   #endIf
   msgPrefix = "modifyRouter("+`routerName`+", "+`newRouterName`+", "+`newRouterProvider`+", "+`failonerror`+"): "

   try:
      #--------------------------------------------------------------------
      # Set up globals
      #--------------------------------------------------------------------
      global AdminConfig

      #--------------------------------------------------------------------
      # Modify the name and provider of a SIP Application Router
      #--------------------------------------------------------------------
      print "-------------------------------------------------------------------------------"
      print "AdminCEA:            Modify the name and provider of a SIP Application Router"
      print "Router name:         "+routerName
      print "New router name:     "+newRouterName
      print "New router provider: "+newRouterProvider
      print " "
      print "Usage: AdminCEA.modifyRouter(\""+routerName+"\", \""+newRouterName+"\", \""+newRouterProvider+"\")"
      print " "
      print "Return: If the command is successful, a value of 1 is returned."
      print " "

      # Correct format of base SAR objects (if necessary)
      if (len(AdminConfig.list("SIPApplicationRouters")) == 0):
         AdminConfig.create("SIPApplicationRouters", AdminConfig.getid("/Cell:/"), [])
         AdminConfig.create("DefaultSIPApplicationRouter", AdminConfig.getid("/SIPApplicationRouters:/"), [])

      # Verify required parameters
      if (routerName == ""):
         raise AttributeError(AdminUtilities._formatNLS(resourceBundle, "WASL6041E", ["routerName", routerName]))

      if (newRouterName == ""):
         raise AttributeError(AdminUtilities._formatNLS(resourceBundle, "WASL6041E", ["newRouterName", newRouterName]))

      if (newRouterProvider == ""):
         raise AttributeError(AdminUtilities._formatNLS(resourceBundle, "WASL6041E", ["newRouterProvider", newRouterProvider]))

      # Verify that router exists
      router = AdminConfig.getid("/SIPApplicationRouter:" + routerName + "/")
      if (len(router) == 0):
         raise AttributeError(AdminUtilities._formatNLS(resourceBundle, "WASL6040E", ["routerName", routerName]))
      #endIf

      # Verify that new router name does not already exist
      newRouter = AdminConfig.getid("/SIPApplicationRouter:" + newRouterName + "/")
      if (len(newRouter) > 0):
         raise AttributeError(AdminUtilities._formatNLS(resourceBundle, "WASL6046E", [newRouterName]))
      #endIf

      # Modify the name and provider of the router
      AdminConfig.modify(AdminConfig.getid("/SIPApplicationRouter:" + routerName + "/"), "[[name " + newRouterName + "] [sipApplicationRouterProvider " + newRouterProvider + "]]")

      # Save changes if auto-save is enabled in AdminUtilities.py
      if (AdminUtilities._AUTOSAVE_ == "true"):
         AdminConfig.save()

   except:
      typ, val, tb = sys.exc_info()
      if (typ==SystemExit):  raise SystemExit,`val`
      if (failonerror != "true"):
         print "Exception: %s %s " % (sys.exc_type, sys.exc_value)
         val = "%s %s" % (sys.exc_type, sys.exc_value)
         raise "ScriptLibraryException: ", `val`
         return -1
      else:
         return AdminUtilities.fail(msgPrefix+AdminUtilities.getExceptionText(typ, val, tb), failonerror)
      #endIf

   #endTry

   AdminUtilities.infoNotice(AdminUtilities._OK_+msgPrefix)
   return 1  # succeed

#endDef


## Example 13: Delete a SIP Application Router and any targets assigned to it ##
## AdminCEA.deleteRouter("RouterOne")

def deleteRouter(routerName, failonerror=AdminUtilities._BLANK_):
   if (failonerror==AdminUtilities._BLANK_):
      failonerror=AdminUtilities._FAIL_ON_ERROR_
   #endIf
   msgPrefix = "deleteRouter("+`routerName`+", "+`failonerror`+"): "

   try:
      #--------------------------------------------------------------------
      # Set up globals
      #--------------------------------------------------------------------
      global AdminConfig

      #--------------------------------------------------------------------
      # Delete a SIP Application Router and any targets assigned to it
      #--------------------------------------------------------------------
      print "-------------------------------------------------------------------------------"
      print "AdminCEA:    Delete a SIP Application Router and any targets assigned to it"
      print "Router name: "+routerName
      print " "
      print "Usage: AdminCEA.deleteRouter(\""+routerName+"\")"
      print " "
      print "Return: If the command is successful, a value of 1 is returned."
      print " "

      # Correct format of base SAR objects (if necessary)
      if (len(AdminConfig.list("SIPApplicationRouters")) == 0):
         AdminConfig.create("SIPApplicationRouters", AdminConfig.getid("/Cell:/"), [])
         AdminConfig.create("DefaultSIPApplicationRouter", AdminConfig.getid("/SIPApplicationRouters:/"), [])

      # Verify required parameters
      if (routerName == ""):
         raise AttributeError(AdminUtilities._formatNLS(resourceBundle, "WASL6041E", ["routerName", routerName]))

      # Verify that router exists
      router = AdminConfig.getid("/SIPApplicationRouter:" + routerName + "/")
      if (len(router) == 0):
         raise AttributeError(AdminUtilities._formatNLS(resourceBundle, "WASL6040E", ["routerName", routerName]))
      #endIf

      # Delete router and any targets assigned to it
      rawTargets = AdminConfig.showAttribute(AdminConfig.getid("/SIPApplicationRouter:" + routerName + "/"), "targets")
      targetList = AdminUtilities.convertToList(rawTargets)
      if (len(targetList) > 0):
        for target in targetList:
          AdminConfig.remove(target)
      AdminConfig.remove(AdminConfig.getid("/SIPApplicationRouter:" + routerName + "/"))

      # Save changes if auto-save is enabled in AdminUtilities.py
      if (AdminUtilities._AUTOSAVE_ == "true"):
         AdminConfig.save()

   except:
      typ, val, tb = sys.exc_info()
      if (typ==SystemExit):  raise SystemExit,`val`
      if (failonerror != "true"):
         print "Exception: %s %s " % (sys.exc_type, sys.exc_value)
         val = "%s %s" % (sys.exc_type, sys.exc_value)
         raise "ScriptLibraryException: ", `val`
         return -1
      else:
         return AdminUtilities.fail(msgPrefix+AdminUtilities.getExceptionText(typ, val, tb), failonerror)
      #endIf

   #endTry

   AdminUtilities.infoNotice(AdminUtilities._OK_+msgPrefix)
   return 1  # succeed

#endDef


## Example 14: Move a server to a custom SIP Application Router ##
## AdminCEA.moveServerToCustomRouter("AppSrvCEANode01", "server1", "RouterOne")

def moveServerToCustomRouter(nodeName, serverName, routerName, failonerror=AdminUtilities._BLANK_):
   if (failonerror==AdminUtilities._BLANK_):
      failonerror=AdminUtilities._FAIL_ON_ERROR_
   #endIf
   msgPrefix = "moveServerToCustomRouter("+`nodeName`+", "+`serverName`+", "+`routerName`+", "+`failonerror`+"): "

   try:
      #--------------------------------------------------------------------
      # Set up globals
      #--------------------------------------------------------------------
      global AdminConfig

      #--------------------------------------------------------------------
      # Move a server to a custom SIP Application Router
      #--------------------------------------------------------------------
      print "-------------------------------------------------------------------------------"
      print "AdminCEA:    Move a server to a custom SIP Application Router"
      print "Node name:   "+nodeName
      print "Server name: "+serverName
      print "Router name: "+routerName
      print " "
      print "Usage: AdminCEA.moveServerToCustomRouter(\""+nodeName+"\", \""+serverName+"\", \""+routerName+"\")"
      print " "
      print "Return: If the command is successful, a value of 1 is returned."
      print " "

      # Correct format of base SAR objects (if necessary)
      if (len(AdminConfig.list("SIPApplicationRouters")) == 0):
         AdminConfig.create("SIPApplicationRouters", AdminConfig.getid("/Cell:/"), [])
         AdminConfig.create("DefaultSIPApplicationRouter", AdminConfig.getid("/SIPApplicationRouters:/"), [])

      # Verify required parameters
      if (nodeName == ""):
         raise AttributeError(AdminUtilities._formatNLS(resourceBundle, "WASL6041E", ["nodeName", nodeName]))

      if (serverName == ""):
         raise AttributeError(AdminUtilities._formatNLS(resourceBundle, "WASL6041E", ["serverName", serverName]))

      if (routerName == ""):
         raise AttributeError(AdminUtilities._formatNLS(resourceBundle, "WASL6041E", ["routerName", routerName]))

      # Verify that node exists
      node = AdminConfig.getid("/Node:"+nodeName+"/")
      if (len(node) == 0):
         raise AttributeError(AdminUtilities._formatNLS(resourceBundle, "WASL6040E", ["nodeName", nodeName]))
      #endIf

      # Verify that server exists
      server = AdminConfig.getid("/Node:"+nodeName+"/Server:"+serverName+"/")
      if (len(server) == 0):
         raise AttributeError(AdminUtilities._formatNLS(resourceBundle, "WASL6040E", ["serverName", serverName]))
      #endIf

      # Verify that server is of the appropriate type and not assigned to a cluster
      if ((AdminConfig.showAttribute(server, "serverType") != "APPLICATION_SERVER") | (AdminConfig.showAttribute(server, "clusterName") is not None)):
         raise AttributeError(AdminUtilities._formatNLS(resourceBundle, "WASL6041E", ["serverName", serverName]))
      #endIf

      # Verify that router exists
      router = AdminConfig.getid("/SIPApplicationRouter:" + routerName + "/")
      if (len(router) == 0):
         raise AttributeError(AdminUtilities._formatNLS(resourceBundle, "WASL6040E", ["routerName", routerName]))
      #endIf

      # Move server to default router
      rawTargets = AdminConfig.getid("/SARServerTarget:/")
      targetList = AdminUtilities.convertToList(rawTargets)
      if (len(targetList) > 0):
         for target in targetList:
            if (AdminConfig.showAttribute(target, "nodeName") == nodeName):
               if (AdminConfig.showAttribute(target, "name") == serverName):
                  AdminConfig.remove(target)

      # Move server to custom router
      rawTargets = AdminConfig.showAttribute(AdminConfig.getid("/SIPApplicationRouter:" + routerName + "/"), "targets")
      targetList = AdminUtilities.convertToList(rawTargets)
      newTarget = AdminConfig.create("SARServerTarget", AdminConfig.getid("/SIPApplicationRouters:/"), "[[name " + serverName + "] [nodeName " + nodeName + "]]")
      targetList.append(newTarget)
      targetString = " ".join(targetList)
      AdminConfig.modify(AdminConfig.getid("/SIPApplicationRouter:" + routerName + "/"), "[[targets \"" + targetString + "\"]]")

      # Save changes if auto-save is enabled in AdminUtilities.py
      if (AdminUtilities._AUTOSAVE_ == "true"):
         AdminConfig.save()

   except:
      typ, val, tb = sys.exc_info()
      if (typ==SystemExit):  raise SystemExit,`val`
      if (failonerror != "true"):
         print "Exception: %s %s " % (sys.exc_type, sys.exc_value)
         val = "%s %s" % (sys.exc_type, sys.exc_value)
         raise "ScriptLibraryException: ", `val`
         return -1
      else:
         return AdminUtilities.fail(msgPrefix+AdminUtilities.getExceptionText(typ, val, tb), failonerror)
      #endIf

   #endTry

   AdminUtilities.infoNotice(AdminUtilities._OK_+msgPrefix)
   return 1  # succeed

#endDef


## Example 15: Move a server to the default SIP Application Router ##
## AdminCEA.moveServerToDefaultRouter("AppSrvCEANode01", "server1")

def moveServerToDefaultRouter(nodeName, serverName, failonerror=AdminUtilities._BLANK_):
   if (failonerror==AdminUtilities._BLANK_):
      failonerror=AdminUtilities._FAIL_ON_ERROR_
   #endIf
   msgPrefix = "moveServerToDefaultRouter("+`nodeName`+", "+`serverName`+", "+`failonerror`+"): "

   try:
      #--------------------------------------------------------------------
      # Set up globals
      #--------------------------------------------------------------------
      global AdminConfig

      #--------------------------------------------------------------------
      # Move a server to the default SIP Application Router
      #--------------------------------------------------------------------
      print "-------------------------------------------------------------------------------"
      print "AdminCEA:    Move a server to the default SIP Application Router"
      print "Node name:   "+nodeName
      print "Server name: "+serverName
      print " "
      print "Usage: AdminCEA.moveServerToDefaultRouter(\""+nodeName+"\", \""+serverName+"\")"
      print " "
      print "Return: If the command is successful, a value of 1 is returned."
      print " "

      # Correct format of base SAR objects (if necessary)
      if (len(AdminConfig.list("SIPApplicationRouters")) == 0):
         AdminConfig.create("SIPApplicationRouters", AdminConfig.getid("/Cell:/"), [])
         AdminConfig.create("DefaultSIPApplicationRouter", AdminConfig.getid("/SIPApplicationRouters:/"), [])

      # Verify required parameters
      if (nodeName == ""):
         raise AttributeError(AdminUtilities._formatNLS(resourceBundle, "WASL6041E", ["nodeName", nodeName]))

      if (serverName == ""):
         raise AttributeError(AdminUtilities._formatNLS(resourceBundle, "WASL6041E", ["serverName", serverName]))

      # Verify that node exists
      node = AdminConfig.getid("/Node:"+nodeName+"/")
      if (len(node) == 0):
         raise AttributeError(AdminUtilities._formatNLS(resourceBundle, "WASL6040E", ["nodeName", nodeName]))
      #endIf

      # Verify that server exists
      server = AdminConfig.getid("/Node:"+nodeName+"/Server:"+serverName+"/")
      if (len(server) == 0):
         raise AttributeError(AdminUtilities._formatNLS(resourceBundle, "WASL6040E", ["serverName", serverName]))
      #endIf

      # Verify that server is of the appropriate type and not assigned to a cluster
      if ((AdminConfig.showAttribute(server, "serverType") != "APPLICATION_SERVER") | (AdminConfig.showAttribute(server, "clusterName") is not None)):
         raise AttributeError(AdminUtilities._formatNLS(resourceBundle, "WASL6041E", ["serverName", serverName]))
      #endIf

      # Move server to default router
      rawTargets = AdminConfig.getid("/SARServerTarget:/")
      targetList = AdminUtilities.convertToList(rawTargets)
      if (len(targetList) > 0):
         for target in targetList:
            if (AdminConfig.showAttribute(target, "nodeName") == nodeName):
               if (AdminConfig.showAttribute(target, "name") == serverName):
                  AdminConfig.remove(target)

      # Save changes if auto-save is enabled in AdminUtilities.py
      if (AdminUtilities._AUTOSAVE_ == "true"):
         AdminConfig.save()

   except:
      typ, val, tb = sys.exc_info()
      if (typ==SystemExit):  raise SystemExit,`val`
      if (failonerror != "true"):
         print "Exception: %s %s " % (sys.exc_type, sys.exc_value)
         val = "%s %s" % (sys.exc_type, sys.exc_value)
         raise "ScriptLibraryException: ", `val`
         return -1
      else:
         return AdminUtilities.fail(msgPrefix+AdminUtilities.getExceptionText(typ, val, tb), failonerror)
      #endIf

   #endTry

   AdminUtilities.infoNotice(AdminUtilities._OK_+msgPrefix)
   return 1  # succeed

#endDef


## Example 16: Move a cluster to a custom SIP Application Router ##
## AdminCEA.moveClusterToCustomRouter("cluster1", "RouterOne")

def moveClusterToCustomRouter(clusterName, routerName, failonerror=AdminUtilities._BLANK_):
   if (failonerror==AdminUtilities._BLANK_):
      failonerror=AdminUtilities._FAIL_ON_ERROR_
   #endIf
   msgPrefix = "moveClusterToCustomRouter("+`clusterName`+", "+`routerName`+", "+`failonerror`+"): "

   try:
      #--------------------------------------------------------------------
      # Set up globals
      #--------------------------------------------------------------------
      global AdminConfig

      #--------------------------------------------------------------------
      # Move a cluster to a custom SIP Application Router
      #--------------------------------------------------------------------
      print "-------------------------------------------------------------------------------"
      print "AdminCEA:     Move a cluster to a custom SIP Application Router"
      print "Cluster name: "+clusterName
      print "Router name:  "+routerName
      print " "
      print "Usage: AdminCEA.moveClusterToCustomRouter(\""+clusterName+"\", \""+routerName+"\")"
      print " "
      print "Return: If the command is successful, a value of 1 is returned."
      print " "

      # Correct format of base SAR objects (if necessary)
      if (len(AdminConfig.list("SIPApplicationRouters")) == 0):
         AdminConfig.create("SIPApplicationRouters", AdminConfig.getid("/Cell:/"), [])
         AdminConfig.create("DefaultSIPApplicationRouter", AdminConfig.getid("/SIPApplicationRouters:/"), [])

      # Verify required parameters
      if (clusterName == ""):
         raise AttributeError(AdminUtilities._formatNLS(resourceBundle, "WASL6041E", ["clusterName", clusterName]))

      if (routerName == ""):
         raise AttributeError(AdminUtilities._formatNLS(resourceBundle, "WASL6041E", ["routerName", routerName]))

      # Verify that cluster exists
      cluster = AdminConfig.getid("/ServerCluster:"+clusterName+"/")
      if (len(cluster) == 0):
         raise AttributeError(AdminUtilities._formatNLS(resourceBundle, "WASL6040E", ["clusterName", clusterName]))
      #endIf

      # Verify that router exists
      router = AdminConfig.getid("/SIPApplicationRouter:" + routerName + "/")
      if (len(router) == 0):
         raise AttributeError(AdminUtilities._formatNLS(resourceBundle, "WASL6040E", ["routerName", routerName]))
      #endIf

      # Move cluster to default router
      rawTargets = AdminConfig.getid("/SARClusterTarget:/")
      targetList = AdminUtilities.convertToList(rawTargets)
      if (len(targetList) > 0):
         for target in targetList:
            if (AdminConfig.showAttribute(target, "name") == clusterName):
               AdminConfig.remove(target)

      # Move cluster to custom router
      rawTargets = AdminConfig.showAttribute(AdminConfig.getid("/SIPApplicationRouter:" + routerName + "/"), "targets")
      targetList = AdminUtilities.convertToList(rawTargets)
      newTarget = AdminConfig.create("SARClusterTarget", AdminConfig.getid("/SIPApplicationRouters:/"), "[[name " + clusterName + "]]")
      targetList.append(newTarget)
      targetString = " ".join(targetList)
      AdminConfig.modify(AdminConfig.getid("/SIPApplicationRouter:" + routerName + "/"), "[[targets \"" + targetString + "\"]]")

      # Save changes if auto-save is enabled in AdminUtilities.py
      if (AdminUtilities._AUTOSAVE_ == "true"):
         AdminConfig.save()

   except:
      typ, val, tb = sys.exc_info()
      if (typ==SystemExit):  raise SystemExit,`val`
      if (failonerror != "true"):
         print "Exception: %s %s " % (sys.exc_type, sys.exc_value)
         val = "%s %s" % (sys.exc_type, sys.exc_value)
         raise "ScriptLibraryException: ", `val`
         return -1
      else:
         return AdminUtilities.fail(msgPrefix+AdminUtilities.getExceptionText(typ, val, tb), failonerror)
      #endIf

   #endTry

   AdminUtilities.infoNotice(AdminUtilities._OK_+msgPrefix)
   return 1  # succeed

#endDef


## Example 17: Move a cluster to the default SIP Application Router ##
## AdminCEA.moveClusterToDefaultRouter("cluster1")

def moveClusterToDefaultRouter(clusterName, failonerror=AdminUtilities._BLANK_):
   if (failonerror==AdminUtilities._BLANK_):
      failonerror=AdminUtilities._FAIL_ON_ERROR_
   #endIf
   msgPrefix = "moveClusterToDefaultRouter("+`clusterName`+", "+`failonerror`+"): "

   try:
      #--------------------------------------------------------------------
      # Set up globals
      #--------------------------------------------------------------------
      global AdminConfig

      #--------------------------------------------------------------------
      # Move a cluster to the default SIP Application Router
      #--------------------------------------------------------------------
      print "-------------------------------------------------------------------------------"
      print "AdminCEA:     Move a cluster to the default SIP Application Router"
      print "Cluster name: "+clusterName
      print " "
      print "Usage: AdminCEA.moveClusterToDefaultRouter(\""+clusterName+"\")"
      print " "
      print "Return: If the command is successful, a value of 1 is returned."
      print " "

      # Correct format of base SAR objects (if necessary)
      if (len(AdminConfig.list("SIPApplicationRouters")) == 0):
         AdminConfig.create("SIPApplicationRouters", AdminConfig.getid("/Cell:/"), [])
         AdminConfig.create("DefaultSIPApplicationRouter", AdminConfig.getid("/SIPApplicationRouters:/"), [])

      # Verify required parameters
      if (clusterName == ""):
         raise AttributeError(AdminUtilities._formatNLS(resourceBundle, "WASL6041E", ["clusterName", clusterName]))

      # Verify that cluster exists
      cluster = AdminConfig.getid("/ServerCluster:"+clusterName+"/")
      if (len(cluster) == 0):
         raise AttributeError(AdminUtilities._formatNLS(resourceBundle, "WASL6040E", ["clusterName", clusterName]))
      #endIf

      # Move cluster to default router
      rawTargets = AdminConfig.getid("/SARClusterTarget:/")
      targetList = AdminUtilities.convertToList(rawTargets)
      if (len(targetList) > 0):
         for target in targetList:
            if (AdminConfig.showAttribute(target, "name") == clusterName):
               AdminConfig.remove(target)

      # Save changes if auto-save is enabled in AdminUtilities.py
      if (AdminUtilities._AUTOSAVE_ == "true"):
         AdminConfig.save()

   except:
      typ, val, tb = sys.exc_info()
      if (typ==SystemExit):  raise SystemExit,`val`
      if (failonerror != "true"):
         print "Exception: %s %s " % (sys.exc_type, sys.exc_value)
         val = "%s %s" % (sys.exc_type, sys.exc_value)
         raise "ScriptLibraryException: ", `val`
         return -1
      else:
         return AdminUtilities.fail(msgPrefix+AdminUtilities.getExceptionText(typ, val, tb), failonerror)
      #endIf

   #endTry

   AdminUtilities.infoNotice(AdminUtilities._OK_+msgPrefix)
   return 1  # succeed

#endDef

