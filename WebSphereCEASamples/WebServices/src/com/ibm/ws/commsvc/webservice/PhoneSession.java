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

package com.ibm.ws.commsvc.webservice;

import java.net.URL;

import javax.xml.namespace.QName;
import javax.xml.ws.soap.AddressingFeature;
import javax.xml.ws.wsaddressing.W3CEndpointReference;

import com.ibm.ws.commsvc.webservice.impl.CallState;
import com.ibm.ws.commsvc.webservice.impl.CallStatus;
import com.ibm.ws.commsvc.webservice.impl.CommWsRequest;
import com.ibm.ws.commsvc.webservice.impl.Controller;
import com.ibm.ws.commsvc.webservice.impl.ControllerService;

/**
 * The purpose of this class is to control the state and actions taken related
 * to a specific phone.  A reference to this object is kept in the HttpSession
 * and also a HashMap in the servlet code so it can be found in different 
 * contexts (servlet requests and WS-Notifications).
 */
public class PhoneSession {

	// Reference to the web service.
	private static Controller webService = null;

	// This phone's address of record.
	private String addressOfRecord = null;

	// URL to contact in order to trigger a call notification (WS-Notification)
	// - the host and port must be where the web service client resides
	// - the context root much match that of the WAR including this web services client
	// - the name at the end must match the service name found in the associated WSDL.
	private String notifyCallback = null;
	
	// While the openSession method must be called with the webService reference,
	// follow up calls related to the same session need to use this.  It allows
	// for the web services calls to include a reference to an EPR (endpoint 
	// reference).  This is critical for multiple reasons.  First, it allows for 
	// web service interface to be simpler eliminating the need to pass a state 
	// object as a parameter in all follow up requests.  The EPR itself has enough
	// information for the web service to track it.  It is also leveraged in a clustered
	// environment to ensure follow on requests go back to the same container 
	// monitoring the phone.
	private Controller webServiceWithEPR = null;

	// The current state of the call / phone.
	private String callState = CallState.CALL_STATUS_CLEARED.value();

	// When a call is active, the address of record for the party being called.
	private String calleeAddressOfRecord = null;

	// When a call is active, the address of record for the party that made the call.
	private String callerAddressOfRecord = null;

	// When a call is active, The call ID being used by this phone.
	private String callID = null;
	
	// The location of the web service.
	private String webServiceLocation = null;
	
	// Accessor methods
	public String getAddressOfRecord() { return addressOfRecord; }
	public String getCalleeAddressOfRecord() { return calleeAddressOfRecord; }
	public String getCallerAddressOfRecord() { return callerAddressOfRecord; }
	public String getCallState() { return callState; }
	public String getCallID() { return callID; }

	/**
	 * Get access to the web service.  To prevent from doing this for each instance
	 * of this object, save the reference as a singleton.
	 * @param wsdlLocation - the location of the web service, a URL string
	 * @return the web service interface upon which methods may be called
	 * @throws Exception
	 */
    public static Controller accessWebService(String wsdlLocation) throws Exception {
    	if (null == webService) {
	        // Access the web service client
	        URL url = new URL(wsdlLocation);
			QName serviceName = new QName("http://impl.webservice.commsvc.ws.ibm.com/", "ControllerService");
	        ControllerService service = new ControllerService(url, serviceName);
	        if (service != null) {
	        	webService = service.getControllerPort();
	        }
    	}
        return webService;
    }

	/**
	 * Constructor.
	 * @param addressOfRecord
	 */
	public PhoneSession(String addressOfRecord, String localAddr, int localPort, String protocol) {
		// Save the address of record representing the phone to be monitored.
		this.addressOfRecord = addressOfRecord;
		// Build the URL to be used for the WS-Notification callback.
		this.notifyCallback = protocol + "://" + localAddr + ":" + localPort 
							+ "/" + CommWebServiceServlet.CONTEXT_ROOT 
							+ "/CeaNotificationConsumer";
		// Build the URL to the local WSDL of the web service.
		webServiceLocation = protocol + "://" + localAddr + ":" + localPort 
		                   + "/commsvc.rest/ControllerService?wsdl";
	}
	
	/**
	 * This is called in order to start monitoring a phone 
	 */
	public void openSession() throws Exception {
		// Build the web service request object.
		CommWsRequest wsRequest = new CommWsRequest();
		wsRequest.setAddressOfRecord(addressOfRecord);
		wsRequest.setNotifyCallback(notifyCallback);

		// Access the web service.
		webService = accessWebService(webServiceLocation);
		// Call the web service to open the session.
		W3CEndpointReference EPR = webService.openSession(wsRequest);
		
		// Use the endpoint reference to create a new object to make web 
		// service calls on. The EPR includes information that allows the
		// web service to map future requests to this session.
		webServiceWithEPR = EPR.getPort(Controller.class, new AddressingFeature(true));
	}

	/**
	 * This is called from doPost() in order to make a call given the 
	 * form data that was posted.
	 * @param peerAddressOfRecord - the address of record of the device to receive the call
	 */
	public void makeCall(String peerAddressOfRecord) throws Exception {
		// Build the web service request object.
		CommWsRequest wsRequest = new CommWsRequest();
		wsRequest.setPeerAddressOfRecord(peerAddressOfRecord);
		
		// Call the web service to make the call.
		webServiceWithEPR.makeCall(wsRequest);
	}

	/**
	 * End a call via the web service.
	 */
	public void endCall() throws Exception {
		// Call the web service to end the call.
		webServiceWithEPR.endCall();
	}

	/**
	 * This is called from doGet() in order to stop monitoring a phone. 
	 */
	public void closeSession() throws Exception {
		// Call the web service to close the session.
		webServiceWithEPR.closeSession();
	}

	/**
	 * Update this phone session with new CallStatus information that arrived
	 * in a WS-Notification.
	 * @param callStatus
	 */
	public void updateState(CallStatus callStatus) {
		callState = callStatus.getCallStatus().value();
		// If the call state is cleared, null out any current call data.
		if (callState.equals(CallState.CALL_STATUS_CLEARED.value())) {
			calleeAddressOfRecord = null;
			callerAddressOfRecord = null;
			callID = null;			
		} else {
			// Update this object with the latest call data.
			calleeAddressOfRecord = callStatus.getCalleeAddressOfRecord();
			callerAddressOfRecord = callStatus.getCallerAddressOfRecord();
			callID = callStatus.getCallId();
		}
	}
	
}
