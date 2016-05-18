@REM COPYRIGHT LICENSE: This information contains sample code provided in
@REM source code form. You may copy, modify, and distribute these sample
@REM programs in any form without payment to IBM for the purposes of
@REM developing, using, marketing or distributing application programs
@REM conforming to the application programming interface for the operating
@REM platform for which the sample code is written. Notwithstanding anything
@REM to the contrary, IBM PROVIDES THE SAMPLE SOURCE CODE ON AN "AS IS" BASIS
@REM AND IBM DISCLAIMS ALL WARRANTIES, EXPRESS OR IMPLIED, INCLUDING, BUT NOT
@REM LIMITED TO, ANY IMPLIED WARRANTIES OR CONDITIONS OF MERCHANTABILITY,
@REM SATISFACTORY QUALITY, FITNESS FOR A PARTICULAR PURPOSE, TITLE, AND ANY
@REM WARRANTY OR CONDITION OF NON-INFRINGEMENT. IBM SHALL NOT BE LIABLE FOR ANY
@REM DIRECT, INDIRECT, INCIDENTAL, SPECIAL OR CONSEQUENTIAL DAMAGES ARISING OUT
@REM OF THE USE OR OPERATION OF THE SAMPLE SOURCE CODE. IBM HAS NO OBLIGATION
@REM TO PROVIDE MAINTENANCE, SUPPORT, UPDATES, ENHANCEMENTS OR MODIFICATIONS TO
@REM THE SAMPLE SOURCE CODE.

@REM (C) Copyright IBM Corp. 2011.
@REM All Rights Reserved. Licensed Materials - Property of IBM.

@echo off

REM setupCEA.bat

REM Use setupCEA.bat and setupCEA.py to set up an application server
REM environment suitable for evaluating the computer-telephony
REM integration and Web collaboration features included in IBM WebSphere
REM Application Server V8.0.
REM
REM You can configure the scripts to do one of the following:
REM   -Create and set up a new standalone application server profile
REM   -Set up an existing standalone application server
REM   -Set up an existing application server residing in a network
REM    deployment environment
REM
REM setupCEA.bat does the following:
REM   -Generates EJB deployment bindings in PlantsByWebSphereAjax for CEA
REM   -Creates a standalone application server profile (optional)
REM   -Starts the application server (standalone only)
REM   -Runs setupCEA.py, a wsadmin script that does the following:
REM     -Enables the CEA communications service
REM     -Adds required host aliases to the virtual host default_host
REM     -Installs the sample IP-PBX application
REM     -Defines the JDBC provider for PlantsByWebSphereAjax for CEA
REM     -Defines the data source for PlantsByWebSphereAjax for CEA
REM     -Installs PlantsByWebSphereAjax for CEA
REM     -Installs the Web service sample application
REM     -Restarts the application server (network deployment only)
REM   -Restarts the application server (standalone only)

REM Procedure
REM 1. Install IBM WebSphere Application Server Version 8.0. For further
REM    information, see the formal product documentation at
REM    http://www.ibm.com/software/webservers/appserv/was/library/
REM
REM    Important: The setup procedure for the PlantsByWebSphere Ajax Edition
REM    for CEA application requires the EJBDeploy tool for pre-EJB 3.0 modules.
REM    When installing WebSphere Application Server, be sure to include this
REM    optional feature. If you are using an existing installation that does
REM    not include the EJBDeploy tool, use IBM Installation Manager to modify
REM    the installation to include the tool before proceeding.
REM
REM 2. If you will be utilizing a standalone application server, place the
REM    CEA samples package on the system that contains (or will contain)
REM    the application server. If you will be utilizing an application server
REM    that resides in a network deployment environment, place the CEA samples
REM    package on the system that contains the deployment manager.
REM
REM 3. Customize this script to do one of the following:
REM    o  Create and set up a new standalone application server profile
REM       a. Adjust the appServerRoot, profileRoot, and tempPath settings to
REM          match your WebSphere Application Server installation.
REM       b. Set createAppServerProfile to true.
REM       c. Set networkDeployment to false.
REM       d. If necessary, customize remaining settings, ensuring that the
REM          topology settings are unique within the installation.
REM    o  Set up an existing standalone application server
REM       a. Adjust the appServerRoot, profileRoot, and tempPath settings to
REM          match your WebSphere Application Server installation.
REM       b. Set createAppServerProfile to false.
REM       c. Set networkDeployment to false.
REM       d. Set profileName, appServerNodeName, and appServerName to the
REM          profile, node, and server names of the application server.
REM       e. Customize the administrative security settings to match those of
REM          the application server.
REM    o  Set up an existing application server residing in a network
REM       deployment environment
REM       a. Adjust the appServerRoot, profileRoot, and tempPath settings to
REM          match your WebSphere Application Server installation.
REM       b. Set createAppServerProfile to false.
REM       c. Set networkDeployment to true.
REM       d. Set profileName to the name of the appropriate deployment
REM          manager profile.
REM       e. Set appServerNodeName and appServerName to the node and server
REM          names of the appropriate application server.
REM       f. Customize the administrative security settings to match those of
REM          the deployment manager cell.
REM       g. Start the appropriate deployment manager and node agent.
REM
REM 4. At a command prompt, change to the scripts directory of the CEA samples
REM    package and run this file (setupCEA.bat).

set appServerRoot=C:\Program Files\IBM\WebSphere\AppServer
set profileRoot=C:\Program Files\IBM\WebSphere\AppServer\profiles
set tempPath=C:\temp

set createAppServerProfile=true
set networkDeployment=false

set profileName=AppSrvCEA

set appServerNodeName=localhostNode01
set appServerName=server1

set adminSecurity=false
set adminUserName=
set adminPassword=

REM Note: Customization of the content below is not required or recommended.

echo. & echo Generating EJB deployment bindings in CEA PlantsByWebSphereAjax sample & echo %date%  %time%
set plantsAppUndeployedPath=../installableApps/PlantsByWebSphere.ear
set plantsAppPath=../installableApps/PlantsByWebSphere_Deployed.ear
call "%appServerRoot%\bin\ejbdeploy" "%plantsAppUndeployedPath%" "%tempPath%" "%plantsAppPath%" -dbvendor DERBY_V10

if not exist %plantsAppPath% (
   echo.
   echo ERROR: PlantsByWebSphere_Deployed.ear was not generated by the EJBDeploy tool.
   echo The setup procedure for the PlantsByWebSphere Ajax Edition for CEA application
   echo requires the EJBDeploy tool for pre-EJB 3.0 modules. If you are using a
   echo WebSphere Application Server installation that does not include the EJBDeploy
   echo tool, use IBM Installation Manager to modify the installation to include the
   echo tool.
   goto:eof
)

if %createAppServerProfile% == true (
   echo. &  echo Creating application server profile %profileName% & echo %date%  %time%
   if %adminSecurity% == false (
      call "%appServerRoot%\bin\manageprofiles" -create -profileName "%profileName%" -profilePath "%profileRoot%\%profileName%" -templatePath "%appServerRoot%\profileTemplates\default" -nodeName "%appServerNodeName%" -serverName "%appServerName%" -hostName localhost -isDefault false -winserviceCheck false
   ) else if %adminSecurity% == true (
      call "%appServerRoot%\bin\manageprofiles" -create -profileName "%profileName%" -profilePath "%profileRoot%\%profileName%" -templatePath "%appServerRoot%\profileTemplates\default" -nodeName "%appServerNodeName%" -serverName "%appServerName%" -hostName localhost -enableAdminSecurity true -adminUserName "%adminUserName%" -adminPassword "%adminPassword%" -samplesPassword "%adminPassword%" -isDefault false -winserviceCheck false
   )
)

if %networkDeployment% == false (
   echo. & echo Starting the application server & echo %date%  %time%
   call "%profileRoot%\%profileName%\bin\startServer" "%appServerName%"
)

set pbxAppPath=../installableApps/commsvc.pbx.ear
set wsAppPath=../installableApps/commsvc.ws.sample.ear

echo. & echo Running wsadmin script setupCEA.py & echo %date%  %time%
if %adminSecurity% == false (
   call "%profileRoot%\%profileName%\bin\wsadmin" -lang jython -f "setupCEA.py" "%pbxAppPath%" "%plantsAppPath%" "%wsAppPath%" "%appServerNodeName%" "%appServerName%"
) else if %adminSecurity% == true (
   call "%profileRoot%\%profileName%\bin\wsadmin" -lang jython -f "setupCEA.py" -userName "%adminUserName%" -password "%adminPassword%" "%pbxAppPath%" "%plantsAppPath%" "%wsAppPath%" "%appServerNodeName%" "%appServerName%"
)

if %networkDeployment% == false (
   echo. & echo Stopping the application server & echo %date%  %time%
   if %adminSecurity% == false (
      call "%profileRoot%\%profileName%\bin\stopServer" "%appServerName%"
   ) else if %adminSecurity% == true (
      call "%profileRoot%\%profileName%\bin\stopServer" "%appServerName%" -username "%adminUserName%" -password "%adminPassword%"
   )
   echo. & echo Starting the application server & echo %date%  %time%
   call "%profileRoot%\%profileName%\bin\startServer" "%appServerName%"
)
