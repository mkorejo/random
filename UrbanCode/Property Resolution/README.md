## Property Reporting
Sometimes, you may find while using UrbanCode Deploy that you have too many properties and little confidence around what property values will be used for a particular deployment. Resource properties in particular can be difficult to predict if you are not careful about where they are used and how. Traversing a set of UrbanCode Deploy resources is not trivial because there may be a large number of resources below an environment base resource, you may have more than one environment base resource in an environment, and there are a number of different ways to structure resources using groups, tags, etc.

This [Resources Utilities plugin](https://github.com/IBM-UrbanCode/Resource-Utilities-UCD) for IBM UrbanCode Deploy is quite handy for getting information about all resources below an environment base resource. One can also use the UrbanCode Deploy APIs to get information about which base resources are in an environment, as well as details on all other properties associated with an application environment defined on the application, components, or environments themselves.

`Property Reporting` is a generic process in UrbanCode Deploy that uses the [Resources Utilities plugin](https://github.com/IBM-UrbanCode/Resource-Utilities-UCD), the [Web Utilities plugin](https://developer.ibm.com/urbancode/plugin/web-utilities-ibmucd), and the standard Groovy plugin. The process produces an output file that shows you all properties that would be used for a process request against an application environment. The output is tab-delimited, and several intermediary output files are also produced:

![Sample Output](https://github.com/mkorejo/random/tree/master/UrbanCode/Property\ Resolution/output.png "Sample Output")

There are two main paths through the process: one which looks at resources and their properties and one that looks at everything else. For the resources, there is post-processing script to count the number of base resources and save them off, and then a switch to determine if there is a second base resource. Currently, the process only works for environments with up to two base resources but could be extended to accommodate three or more. Both the post-processing script and the process itself would have to be updated.

![Process Screenshot](https://github.com/mkorejo/random/tree/master/UrbanCode/Property\ Resolution/process.png "Process Screenshot")

Before importing `Property+Reporting.json` you must install the required plugins. After importing you must set the password for each `Send HTTP Call` step (4) as well as for the process itself. Use IDs when specifying `Application` and `Application Environment`!
