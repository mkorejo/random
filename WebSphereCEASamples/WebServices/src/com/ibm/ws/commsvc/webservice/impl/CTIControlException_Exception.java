// COPYRIGHT LICENSE: This information contains sample code provided in
// source code form. You may copy, modify, and distribute these sample
// programs in any form without payment to IBM for the purposes of
// developing, using, marketing or distributing application programs
// conforming to the application programming interface for the operating
// platform for which the sample code is written. Notwithstanding anything
// to the contrary, IBM PROVIDES THE SAMPLE SOURCE CODE ON AN "AS IS" BASIS
// AND IBM DISCLAIMS ALL WARRANTIES, EXPRESS OR IMPLIED, INCLUDING, BUT NOT
// LIMITED TO, ANY IMPLIED WARRANTIES OR CONDITIONS OF MERCHANTABILITY,
// SATISFACTORY QUALITY, FITNESS FOR A PARTICULAR PURPOSE, TITLE, AND ANY
// WARRANTY OR CONDITION OF NON-INFRINGEMENT. IBM SHALL NOT BE LIABLE FOR ANY
// DIRECT, INDIRECT, INCIDENTAL, SPECIAL OR CONSEQUENTIAL DAMAGES ARISING OUT
// OF THE USE OR OPERATION OF THE SAMPLE SOURCE CODE. IBM HAS NO OBLIGATION
// TO PROVIDE MAINTENANCE, SUPPORT, UPDATES, ENHANCEMENTS OR MODIFICATIONS TO
// THE SAMPLE SOURCE CODE.
//
// (C) Copyright IBM Corp. 2008, 2011.
// All Rights Reserved. Licensed Materials - Property of IBM.
//
// Generated By:JAX-WS RI IBM 2.1.1 in JDK 6 (JAXB RI IBM JAXB 2.1.3 in JDK 1.6)
//


package com.ibm.ws.commsvc.webservice.impl;

import javax.xml.ws.WebFault;

@WebFault(name = "CTIControl", targetNamespace = "http://impl.webservice.commsvc.ws.ibm.com/")
public class CTIControlException_Exception
    extends Exception
{

    /**
     * Java type that goes as soapenv:Fault detail element.
     * 
     */
    private CTIControlException faultInfo;

    /**
     * 
     * @param faultInfo
     * @param message
     */
    public CTIControlException_Exception(String message, CTIControlException faultInfo) {
        super(message);
        this.faultInfo = faultInfo;
    }

    /**
     * 
     * @param faultInfo
     * @param message
     * @param cause
     */
    public CTIControlException_Exception(String message, CTIControlException faultInfo, Throwable cause) {
        super(message, cause);
        this.faultInfo = faultInfo;
    }

    /**
     * 
     * @return
     *     returns fault bean: com.ibm.ws.commsvc.webservice.impl.CTIControlException
     */
    public CTIControlException getFaultInfo() {
        return faultInfo;
    }

}
