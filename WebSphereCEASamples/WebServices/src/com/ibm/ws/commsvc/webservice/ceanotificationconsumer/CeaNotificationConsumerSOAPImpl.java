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

package com.ibm.ws.commsvc.webservice.ceanotificationconsumer;

import java.util.List;

import org.oasis_open.docs.wsn.b_2.NotificationMessageHolderType;
import org.oasis_open.docs.wsn.b_2.Notify;
import org.oasis_open.docs.wsn.b_2.NotificationMessageHolderType.Message;
import org.w3c.dom.Element;
import org.w3c.dom.Node;
import org.w3c.dom.NodeList;

import com.ibm.ws.commsvc.webservice.CommWebServiceServlet;
import com.ibm.ws.commsvc.webservice.impl.CallState;
import com.ibm.ws.commsvc.webservice.impl.CallStatus;

@javax.jws.WebService(
		endpointInterface = "com.ibm.ws.commsvc.webservice.ceanotificationconsumer.NotificationConsumer", 
		targetNamespace = "http://webservice.commsvc.ws.ibm.com/CeaNotificationConsumer/", 
		serviceName = "CeaNotificationConsumer", 
		portName = "CeaNotificationConsumerSOAP",
		wsdlLocation = "WEB-INF/wsdl/CeaNotificationConsumer.wsdl")
public class CeaNotificationConsumerSOAPImpl {

	/**
	 * This is the key method.  It is called automatically by the server's 
	 * notification broker when a notification takes place.
	 * @param notify
	 */
    public void notify(Notify notify) {
		CallStatus callStatus = null;
		
		// Extract the list of notification messages.
        List<NotificationMessageHolderType> notificationMessages = null;
        notificationMessages = notify.getNotificationMessage();

        // Loop through the messages.
        for (int i=0; i< notificationMessages.size(); i++) {
        	NotificationMessageHolderType notificationMessage = notificationMessages.get(i);
		    // Get the message content as a DOM Element.
		    Message message = notificationMessage.getMessage();
		    // Build a CallStatus object out of the notification.
		    Element messageContents = (Element) (message.getAny());
		    NodeList nodeList = messageContents.getChildNodes();
		    int numNodes = nodeList.getLength();
		    callStatus = new CallStatus();
		    for (int j=0; j<numNodes; j++) {
		    	Node node = nodeList.item(j);
		    	String nodeText = node.getTextContent();
		    	String nodeName = node.getNodeName();
		    	// Match the text to a member of the CallStatus object and set it.
		    	if ("callStatus".equals(nodeName)) {
		    		callStatus.setCallStatus(CallState.valueOf(nodeText));
		    	} else if ("addressOfRecord".equals(nodeName)) {
		    		callStatus.setAddressOfRecord(nodeText);
		    	} else if ("callerAddressOfRecord".equals(nodeName)) {
		    		callStatus.setCallerAddressOfRecord(nodeText);
		    	} else if ("calleeAddressOfRecord".equals(nodeName)) {
		    		callStatus.setCalleeAddressOfRecord(nodeText);
		    	} else if ("callId".equals(nodeName)) {
		    		callStatus.setCallId(nodeText);
		    	} else if ("callFailureReason".equals(nodeName)) {
		    		callStatus.setCallFailureReason(nodeText);
		    	} 
		    }
		    
		    // Update the status of the associated PhoneSession state object.
		    CommWebServiceServlet.updatePhoneSession(callStatus);
		}
    }

}