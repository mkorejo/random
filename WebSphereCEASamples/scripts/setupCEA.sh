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

# setupCEA.sh

# Use setupCEA.sh and setupCEA.py to set up an application server
# environment suitable for evaluating the computer-telephony
# integration and Web collaboration features included in IBM WebSphere
# Application Server V8.0.
#
# You can configure the scripts to do one of the following:
#   -Create and set up a new standalone application server profile
#   -Set up an existing standalone application server
#   -Set up an existing application server residing in a network
#    deployment environment
#
# setupCEA.sh does the following:
#   -Generates EJB deployment bindings in PlantsByWebSphereAjax for CEA
#   -Creates a standalone application server profile (optional)
#   -Starts the application server (standalone only)
#   -Runs setupCEA.py, a wsadmin script that does the following:
#     -Enables the CEA communications service
#     -Adds required host aliases to the virtual host default_host
#     -Installs the sample IP-PBX application
#     -Defines the JDBC provider for PlantsByWebSphereAjax for CEA
#     -Defines the data source for PlantsByWebSphereAjax for CEA
#     -Installs PlantsByWebSphereAjax for CEA
#     -Installs the Web service sample application
#     -Restarts the application server (network deployment only)
#   -Restarts the application server (standalone only)

# Procedure
# 1. Install IBM WebSphere Application Server Version 8.0. For further
#    information, see the formal product documentation at
#    http://www.ibm.com/software/webservers/appserv/was/library/
#
#    Important: The setup procedure for the PlantsByWebSphere Ajax Edition
#    for CEA application requires the EJBDeploy tool for pre-EJB 3.0 modules.
#    When installing WebSphere Application Server, be sure to include this
#    optional feature. If you are using an existing installation that does
#    not include the EJBDeploy tool, use IBM Installation Manager to modify
#    the installation to include the tool before proceeding.
#
# 2. If you will be utilizing a standalone application server, place the
#    CEA samples package on the system that contains (or will contain)
#    the application server. If you will be utilizing an application server
#    that resides in a network deployment environment, place the CEA samples
#    package on the system that contains the deployment manager.
#
# 3. Customize this script to do one of the following:
#    o  Create and set up a new standalone application server profile
#       a. Adjust the appServerRoot, profileRoot, and tmpPath settings to
#          match your WebSphere Application Server installation.
#       b. Set createAppServerProfile to true.
#       c. Set networkDeployment to false.
#       d. If necessary, customize remaining settings, ensuring that the
#          topology settings are unique within the installation.
#    o  Set up an existing standalone application server
#       a. Adjust the appServerRoot, profileRoot, and tmpPath settings to
#          match your WebSphere Application Server installation.
#       b. Set createAppServerProfile to false.
#       c. Set networkDeployment to false.
#       d. Set profileName, appServerNodeName, and appServerName to the
#          profile, node, and server names of the application server.
#       e. Customize the administrative security settings to match those of
#          the application server.
#    o  Set up an existing application server residing in a network
#       deployment environment
#       a. Adjust the appServerRoot, profileRoot, and tmpPath settings to
#          match your WebSphere Application Server installation.
#       b. Set createAppServerProfile to false.
#       c. Set networkDeployment to true.
#       d. Set profileName to the name of the appropriate deployment
#          manager profile.
#       e. Set appServerNodeName and appServerName to the node and server
#          names of the appropriate application server.
#       f. Customize the administrative security settings to match those of
#          the deployment manager cell.
#       g. Start the appropriate deployment manager and node agent.
#
# 4. At a command prompt, change to the scripts directory of the CEA samples
#    package and run this file (setupCEA.sh).

appServerRoot=/opt/IBM/WebSphere/AppServer
profileRoot=/opt/IBM/WebSphere/AppServer/profiles
tmpPath=/tmp

createAppServerProfile=true
networkDeployment=false

profileName=AppSrvCEA

appServerNodeName=localhostNode01
appServerName=server1

adminSecurity=false
adminUserName=
adminPassword=

# Note: Customization of the content below is not required or recommended.

echo -e "\nGenerating EJB deployment bindings in CEA PlantsByWebSphereAjax sample\n$(date)"
plantsAppUndeployedPath=../installableApps/PlantsByWebSphere.ear
plantsAppPath=../installableApps/PlantsByWebSphere_Deployed.ear
$appServerRoot/bin/ejbdeploy.sh $plantsAppUndeployedPath $tmpPath $plantsAppPath -dbvendor DERBY_V10

if [ ! -e $plantsAppPath ] ; then
   echo -e "\nERROR: PlantsByWebSphere_Deployed.ear was not generated by the EJBDeploy tool."
   echo "The setup procedure for the PlantsByWebSphere Ajax Edition for CEA application"
   echo "requires the EJBDeploy tool for pre-EJB 3.0 modules. If you are using a"
   echo "WebSphere Application Server installation that does not include the EJBDeploy"
   echo "tool, use IBM Installation Manager to modify the installation to include the"
   echo "tool."
   exit
fi

if [ "$createAppServerProfile" == "true" ] ; then
   echo -e "\nCreating application server profile $profileName\n$(date)"
   if [ "$adminSecurity" == "false" ] ; then
      $appServerRoot/bin/manageprofiles.sh -create -profileName $profileName -profilePath $profileRoot/$profileName -templatePath $appServerRoot/profileTemplates/default -nodeName $appServerNodeName -serverName $appServerName -hostName localhost -enableAdminSecurity false -isDefault false
   elif [ "$adminSecurity" == "true" ] ; then
      $appServerRoot/bin/manageprofiles.sh -create -profileName $profileName -profilePath $profileRoot/$profileName -templatePath $appServerRoot/profileTemplates/default -nodeName $appServerNodeName -serverName $appServerName -hostName localhost -enableAdminSecurity true -adminUserName $adminUserName -adminPassword $adminPassword -samplesPassword $adminPassword -isDefault false
   fi
fi

if [ "$networkDeployment" == "false" ] ; then
   echo -e "\nStarting the application server\n$(date)"
   $profileRoot/$profileName/bin/startServer.sh $appServerName
fi

pbxAppPath=../installableApps/commsvc.pbx.ear
wsAppPath=../installableApps/commsvc.ws.sample.ear

echo -e "\nRunning wsadmin script setupCEA.py\n$(date)"
if [ "$adminSecurity" == "false" ] ; then
   $profileRoot/$profileName/bin/wsadmin.sh -lang jython -f ./setupCEA.py $pbxAppPath $plantsAppPath $wsAppPath $appServerNodeName $appServerName
elif [ "$adminSecurity" == "true" ] ; then
   $profileRoot/$profileName/bin/wsadmin.sh -lang jython -f ./setupCEA.py -userName $adminUserName -password $adminPassword $pbxAppPath $plantsAppPath $wsAppPath $appServerNodeName $appServerName
fi

if [ "$networkDeployment" == "false" ] ; then
   echo -e "\nStopping the application server\n$(date)"
   if [ "$adminSecurity" == "false" ] ; then
      $profileRoot/$profileName/bin/stopServer.sh $appServerName
   elif [ "$adminSecurity" == "true" ] ; then
      $profileRoot/$profileName/bin/stopServer.sh $appServerName -username $adminUserName -password $adminPassword
   fi
   echo -e "\nStarting the application server\n$(date)"
   $profileRoot/$profileName/bin/startServer.sh $appServerName
fi
