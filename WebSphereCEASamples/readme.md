<html lang="en-us" xml:lang="en-us">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
<meta name="security" content="public"/>
<meta name="Robots" content="index,follow"/>
<meta http-equiv="PICS-Label" content='(PICS-1.1 "http://www.icra.org/ratingsv02.html" l gen true r (cz 1 lz 1 nz 1 oz 1 vz 1) "http://www.rsac.org/ratingsv01.html" l gen true r (n 0 s 0 v 0 l 0) "http://www.classify.org/safesurf/" l gen true r (SS~~000 1))' />
<meta name="DC.Type" content="task"/>
<meta name="DC.Title" content="Communications Enabled Applications (CEA) Samples"/>
<meta name="abstract" content="You can use WebSphere Application Server V8.0 to add dynamic
web communications to an application or business process. Two main
services are provided, telephony access and multi-modal web interaction.
You can use this collection of sample applications to explore the
services and to start developing your own communications-enabled
applications."/>
<meta name="description" content="You can use WebSphere Application Server V8.0 to add dynamic
web communications to an application or business process. Two main
services are provided, telephony access and multi-modal web interaction.
You can use this collection of sample applications to explore the
services and to start developing your own communications-enabled
applications."/>
<meta name="DC.Coverage" content="sample"/>
<meta name="DC.Relation" scheme="URI" content="page_name.html"/>
<meta name="DC.Relation" scheme="URI" content="http://www.doowop.com/index.html"/>
<meta name="DC.Relation" scheme="URI" content="http://www14.software.ibm.com/webapp/wsbroker/redirect?version=matt&amp;product=was-nd-dist&amp;topic=topicID"/>
<meta name="DC.Audience.Job" content="programming"/>
<meta name="DC.Audience.Type" content="programmer"/>
<meta name="prodname" content="IBM WebSphere Application Server"/>
<meta name="version" content="matt"/>
<meta name="component" content="was-base was-express was-nd"/>
<meta name="platform" content="dist iseries zos"/>
<meta name="DC.Format" content="XHTML"/>
<meta name="DC.Identifier" content="sampletask"/>
<meta name="DC.Language" content="en-us"/>
<!-- All rights reserved. Licensed Materials Property of IBM -->
<!-- US Government Users Restricted Rights -->
<!-- Use, duplication or disclosure restricted by -->
<!-- GSA ADP Schedule Contract with IBM Corp. -->
<link rel="stylesheet" type="text/css" href="style/samples_readme.css"/>
<title>Communications Enabled Applications (CEA) Samples</title>
</head>
<body id="sampletask"><a name="sampletask"><!-- --></a>
<div id="sample_header">
    <img class="sample_header_icon_left" alt="WebSphere software logo" src="images/WS_BrandMark_18x120.png"/>
    <img class="sample_header_icon_right" alt="IBM Logo" src="images/ibm-logo-white.gif"/>
</div>


<h1 class="topictitle1">Communications Enabled Applications (CEA) samples</h1>


<div>
    <p>You can use WebSphere Application Server V8.0 to add dynamic
web communications to an application or business process. Two main
services are provided, telephony access and multi-modal web interaction.
You can use this collection of sample applications to explore the
services and to start developing your own communications-enabled
applications.</p>


    <div class="section">
        <p>Here is what you need to know about this sample
        before you proceed.</p>
    </div>

    <div class="section">
        <h4 class="sectiontitle">
        Time required to set up and configure this sample
        </h4>
        <dd>
            <p>1-2 hours</p>
        </dd>
    </div>

    <div class="section">
        <h4 class="sectiontitle">
        Prerequisites for use</h4>

        <dd>

            <div class="p">
                    <ul>
                        <li>WebSphere Application Server V8.0. This sample was tested most recently with Version <span>8.0</span> of the product.<p>
                        <b>Important</b>: The setup procedure for the PlantsByWebSphere Ajax Edition for CEA application requires the EJBDeploy tool for pre-EJB 3.0 modules. When installing WebSphere Application Server, be sure to include this optional feature. If you are using an existing installation that does not include the EJBDeploy tool, use IBM Installation Manager to modify the installation to include the tool before proceeding.</p></li>
                        <li>Rational Application Developer V8.0 (optional)</li>

                    </ul>
            </div>
        </dd>
    </div>

    <div class="section">
        <h4 class="sectiontitle">
        Copyright license</h4>

            <p>COPYRIGHT LICENSE: This information contains sample code provided in source code form. You may copy, modify, and distribute these sample programs in any form without payment to IBM for the purposes of developing, using, marketing or distributing application programs conforming to the application programming interface for the operating platform for which the sample code is written. Notwithstanding anything to the contrary, IBM PROVIDES THE SAMPLE SOURCE CODE ON AN "AS IS" BASIS AND IBM DISCLAIMS ALL WARRANTIES, EXPRESS OR IMPLIED, INCLUDING, BUT NOT LIMITED TO, ANY IMPLIED WARRANTIES OR CONDITIONS OF MERCHANTABILITY, SATISFACTORY QUALITY, FITNESS FOR A PARTICULAR PURPOSE, TITLE, AND ANY WARRANTY OR CONDITION OF NON-INFRINGEMENT. IBM SHALL NOT BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL OR CONSEQUENTIAL DAMAGES ARISING OUT OF THE USE OR OPERATION OF THE SAMPLE SOURCE CODE. IBM HAS NO OBLIGATION TO PROVIDE MAINTENANCE, SUPPORT, UPDATES, ENHANCEMENTS OR MODIFICATIONS TO THE SAMPLE SOURCE CODE.</p>

    </div>


</div>

<div class="section">
    <h4 class="sectiontitle">
    About this task</h4>

    <p>The following key phrases are associated with this sample: Session Initiation Protocol (SIP), computer-telephony integration (CTI), and web
collaboration.</p>
</div>

<div class="section">
    <h4 class="sectiontitle">
    Procedure </h4>
<steps>
<p><b>Applications</b></p>
<p>The CEA samples package includes the following applications:</p>
<ul>
<li>PlantsByWebSphere Ajax Edition for CEA</li>
<li>Web Services sample application</li>
<li>Sample Internet Protocol Private Branch eXchange (IP-PBX) application</li>
</ul>
<p><b>Installation and configuration scripts</b></p>
<p>You can use a set of simple customizable scripts to set up a basic
application server environment that is suitable for exploring the computer-telephony
integration and web collaboration capabilities that are included in WebSphere
Application Server. When you run the primary scripts, setupCEA.bat and setupCEA.sh,
the following actions occur:</p>
<ul>
<li>EJB deployment bindings in PlantsByWebSphere Ajax Edition for CEA are generated.</li>
<li>(Optional) A stand-alone application server profile is created.</li>
<li>(Stand-alone only) The application server is started.</li>
<li>The wsadmin script, setupCEA.py, runs and completes the following actions:</li>
<ul>
<li>Enables the CEA communications service (a system application).</li>
<li>Adds required host aliases to the virtual host default_host.</li>
<li>Installs the sample IP-PBX application.</li>
<li>Defines a JDBC provider for PlantsByWebSphere Ajax Edition for CEA.</li>
<li>Defines a data source for PlantsByWebSphere Ajax Edition for CEA.</li>
<li>Installs PlantsByWebSphere Ajax Edition for CEA.</li>
<li>Installs the Web services sample application.</li>
<li>(Network deployment only) Restarts the application server.</li>
</ul>
<li>(Stand-alone only) The application server is restarted.</li>
</ul>
<p>To learn more about the setup scripts, see the comments included
in the setupCEA.bat or setupCEA.sh files. Both files are located in the scripts
directory of the CEA samples package.</p>

<p><b>Sample IP-PBX Application</b></p>
<p>The sample Internet Protocol Private Branch eXchange (IP-PBX) application is suitable for demonstrations and
light testing. The sample IP-PBX application is in the form of an enterprise application
that can be installed on an application server. The application, commsvc.pbx.ear,
is located in the installableApps directory of the CEA samples package.</p>
<p>For complete setup and usage instructions, see the end-to-end path
Setting up and using the communications enabled application samples in the
<a href="http://www.ibm.com/software/webservers/appserv/was/library/">
WebSphere Application Server Information Center</a>.</p>

<p><b>PlantsByWebSphere Ajax Edition for CEA</b></p>
<p>PlantsByWebSphere Ajax Edition for CEA applications is an online
plant nursery that exhibits the common characteristics of a Java
EE application consisting of a model (EJB modules), view (JavaServer Pages), and controller
(servlets) design pattern. You can experiment with
AJAX and Java EE. This version of PlantsByWebSphere Ajax Edition has
been enhanced to showcase the computer-telephony integration and web
collaboration capabilities of WebSphere Application Server.</p>
<p>For complete setup and usage instructions, see the end-to-end path
Setting up and using the communications enabled application samples in the
<a href="http://www.ibm.com/software/webservers/appserv/was/library/">
WebSphere Application Server Information Center</a>. Additional usage information
is included in the
<a href="PlantsByWebSphere/docs/index.html">PlantsByWebSphere Ajax Edition for CEA documentation</a>.
</p>

<p><b>CEA Web Services sample application</b></p>
<p>The CEA Web Services sample application provides an interface to
control a phone. It is implemented as a basic servlet that calls
the CEA Web Services APIs.</p>
<p>Environment requirements</p>
<p>This sample involves a telephony feature of the CEA communications service; therefore, an
IP-PBX system must be configured and started. In addition, use the administrative console
or wsadmin tool to configure the CEA communications service. In addition, any phone that is
used with this sample must be started and registered with the IP-PBX system. Minimally,
you must register two phones with the IP-PBX system. The first phone is monitored, and the
next phone is called.</p>
<p>For complete setup and usage instructions, see the end-to-end path
Setting up and using the communications enabled application samples in the
<a href="http://www.ibm.com/software/webservers/appserv/was/library/">
WebSphere Application Server Information Center</a>.</p>
</steps>
</div>

<br />

<div id="sample_header">
   <!--The footer uses the same banner as the header  -->
</div>

</body>
</html>
