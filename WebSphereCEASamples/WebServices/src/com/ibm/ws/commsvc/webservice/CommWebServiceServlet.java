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

import java.io.IOException;
import java.io.PrintWriter;
import java.util.HashMap;

import javax.servlet.Servlet;
import javax.servlet.ServletConfig;
import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.servlet.http.HttpSession;

import com.ibm.ws.commsvc.webservice.impl.CallState;
import com.ibm.ws.commsvc.webservice.impl.CallStatus;

/**
 * The purposes of the class is create a front end to control the use
 * of a client leveraging the CEA web service interface.  The goal is 
 * to present web forms which allow the browser/user to have control
 * over a device.  It starts with opening a session with that device
 * where the status can be refreshed, a call can be made or ended, or
 * the monitoring session can be closed.
 * <p>
 * Once this application is installed on the same server where CEA is
 * installed, the initial request to get the app running is as follows.
 * <p>
 * http://cea_host:http_port/commsvc.ws.sample/CommWebServiceServlet
 */
public class CommWebServiceServlet extends HttpServlet {
	private static final long serialVersionUID = 1L;
    
	// Name of the attribute to add to the HttpSession to track state.
	// Storing a state object in the HttpSession is key to this application
	// as it allows follow on requests in the same HttpSession to track 
	// down the status of the phone that is being monitored.
	private static final String ATTRIBUTE_PHONE_SESSION = "PhoneSession";
	
	// URI path info included in GET / PUT requests
	// The servlet interaction is a bit REST-like, but only as a means
	// to make the servlet simple and easy to understand.
	private static final String PATH_MAKE_CALL          = "/makeCall";
	private static final String PATH_END_CALL           = "/endCall";
	private static final String PATH_GET_CALL_STATUS    = "/callStatus";
	private static final String PATH_OPEN_SESSION       = "/openSession";
	private static final String PATH_CLOSE_SESSION      = "/closeSession";
	
	// Name of the Servlet and context root included in requests.
	private static final String SERVLET_NAME = "CommWebServiceServlet";
	public static final String CONTEXT_ROOT = "commsvc.ws.sample";

	// Names of input form data presented in this application
	public static final String PEER_ADDRESS_OF_RECORD = "peerAddressOfRecord";
	public static final String ADDRESS_OF_RECORD = "addressOfRecord";
	
	// HashMap of all PhoneSession objects keyed by the address of record.
	// This is used to track down state when a notification arrives.
	// While follow on browser requests can leverage the HttpSession to track
	// down the correct PhoneSession object stored as an attribute, that same
	// option isn't available when the WS-Notification arrives with an event
	// that occurred on a phone.  That's where this HashMap is useful.  The 
	// notification includes the address of record of the phone, so that is used
	// to track down the associated PhoneSession state object.
	public static HashMap<String,PhoneSession> hmPhoneSessions = new HashMap<String,PhoneSession>();
	
	/**
     * @see HttpServlet#HttpServlet()
     */
    public CommWebServiceServlet() {
        super();
    }

	/**
	 * @see Servlet#init(ServletConfig)
	 */
	public void init(ServletConfig config) throws ServletException {
	}

	/**
	 * This method is called when a GET request arrives.  The path information is
	 * pulled off the URL and matched to the type of request being made so that
	 * the appropriate page can be returned.   
	 * @see HttpServlet#doGet(HttpServletRequest request, HttpServletResponse response)
	 */
	protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
		PhoneSession phoneSession = null;
		// Get the specific request from the path.
		String pathInfo = request.getPathInfo();
		if (pathInfo == null) {
			pathInfo = "";
		}
		// The result text that will be sent back to the calling browser.
		String result = null;
		
		try {
			// Match the request path to the available functions.
			if (pathInfo.startsWith(PATH_END_CALL)) {
				// The endCall button was pressed on the browser FORM.
				// Get the HttpSession from the request.
				HttpSession httpSession = request.getSession();
				// Look for the PhoneSession object as an attribute of the HttpSession.
				phoneSession = (PhoneSession)httpSession.getAttribute(ATTRIBUTE_PHONE_SESSION);
				// End the call.
				phoneSession.endCall();
				// Sleep a bit to get the call ended so that the response includes
				// status of the call having been shut down.  It might not be done yet in which
				// case the refresh button on the resulting form can be used to try again.
				Thread.sleep(2000);
				result = getStatusPage(phoneSession);
			} else if (pathInfo.startsWith(PATH_GET_CALL_STATUS)) {
				// The refresh button was pressed on the browser FORM.
				// Get the HttpSession from the request.
				HttpSession httpSession = request.getSession();
				// Look for the PhoneSession object as an attribute of the HttpSession.
				phoneSession = (PhoneSession)httpSession.getAttribute(ATTRIBUTE_PHONE_SESSION);
				// Get the latest call status via the web service.
				result = getStatusPage(phoneSession);
			} else if (pathInfo.startsWith(PATH_CLOSE_SESSION)) {
				// The closeSession button was pressed on the browser FORM.
				// Get the HttpSession from the request.
				HttpSession httpSession = request.getSession();
				// Look for the PhoneSession object as an attribute of the HttpSession.
				phoneSession = (PhoneSession)httpSession.getAttribute(ATTRIBUTE_PHONE_SESSION);
				// Close the session.
				phoneSession.closeSession();
				// Clean out the session attribute so a follow on request starts fresh.
				httpSession.removeAttribute(ATTRIBUTE_PHONE_SESSION);
				// Present the initial page to open a new session.
				result = getOpenSessionPage();
				// Remove this PhoneSession from the hashMap
				hmPhoneSessions.remove(phoneSession);
			} else {
				// Initial request to servlet with no path info.  Offer to open a monitoring session.
				result = getOpenSessionPage();
			}
		} catch (Exception e) {
			result = getErrorPage("Exception caught: " + e);
			e.printStackTrace();			
		}
		
		PrintWriter out = response.getWriter();
		out.println(result);
	}
	
	/**
	 * This method is called when a POST is made from one of the web pages /
	 * forms returned from calling doGet().  This is where the requested action
	 * takes place.
	 * @see HttpServlet#doPost(HttpServletRequest request, HttpServletResponse response)
	 */
	protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
		PhoneSession phoneSession = null;
		
		// Get the specific request from the path.
		String pathInfo = request.getPathInfo();
		if (pathInfo == null) {
			pathInfo = "";
		}
		// The result text that will be sent back to the calling browser.
		String result = null;

		try {
			// Match the request path to the available functions.
			if (pathInfo.startsWith(PATH_MAKE_CALL)) {
				// The makeCall button was pressed on the browser FORM.
				// Extract the target phone number (peer address of record)
				String peerAddressOfRecord = request.getParameter(PEER_ADDRESS_OF_RECORD);
				// Ensure non null and non empty inputs.
				if (peerAddressOfRecord == null || peerAddressOfRecord.trim().equals("")) {
					result = getErrorPage("Invalid inputs: peerAddressOfRecord=" + peerAddressOfRecord);
				} else {
					// Get the HttpSession from the request.
					HttpSession httpSession = request.getSession();
					// Get the PhoneSession object formerly saved as an attribute of the HttpSession.
					phoneSession = (PhoneSession)httpSession.getAttribute(ATTRIBUTE_PHONE_SESSION);
					// Make the call via the web service.
					phoneSession.makeCall(peerAddressOfRecord);
					// Sleep a bit to get the call set up so that the response includes
					// status of the call having been set up.  It might not be done yet in which
					// case the refresh button on the resulting form can be used to try again.
					Thread.sleep(2000);
					// Return the latest status of the call.
					result = getStatusPage(phoneSession);
				}
			} else if (pathInfo.startsWith(PATH_OPEN_SESSION)) {
				// The openSession button was pressed on the browser FORM.
				// Extract the address of record passed in on the form.
				String addressOfRecord = request.getParameter(ADDRESS_OF_RECORD);
				// Ensure non null and non empty inputs.
				if (addressOfRecord == null || addressOfRecord.trim().equals("")) {
					result = getErrorPage("Invalid inputs: addressOfRecord=" + addressOfRecord);
					// Fetch the initial page to open a session.
					result = getOpenSessionPage();
				} else {
					// Extract the host and port of this servlet.
					String localAddr = request.getLocalAddr();
					int localPort = request.getLocalPort();
					// Extract the protocol from the request.
					String requestUrl = request.getRequestURL().toString();
					String protocol = requestUrl.substring(0, requestUrl.indexOf(":"));
					// Create an instance of the PhoneSession.
					phoneSession = new PhoneSession(addressOfRecord, localAddr, localPort, protocol);
					// Add this new PhoneSession to the array.
					hmPhoneSessions.put(addressOfRecord, phoneSession);
					// Make the call via the web service.
					phoneSession.openSession();
					// Get the HttpSession from the request.
					HttpSession httpSession = request.getSession();
					// Store the PhoneSession object as an attribute of the HttpSession.
					httpSession.setAttribute(ATTRIBUTE_PHONE_SESSION, phoneSession);
					// Return the latest status.
					result = getStatusPage(phoneSession);
				}
			} else {
				// Unexpected request.  Present initial page to open a session.
				result = getOpenSessionPage();
			}
		} catch (Exception e) {
			result = getErrorPage("Exception caught: " + e);
			e.printStackTrace();
		}
		
		PrintWriter out = response.getWriter();
		out.println(result);
		
	}
	
	/**
	 * Update the static map of PhoneSession state objects based on a notification 
	 * that was received.
	 * @param callStatus
	 */
	public static void updatePhoneSession(CallStatus callStatus) {
		// Extract the address of record representing the phone associated with this notification.
		String addressOfRecord = callStatus.getAddressOfRecord();
		// Search the static HashMap for the PhoneSession.
		PhoneSession phoneSession = hmPhoneSessions.get(addressOfRecord);
		if (phoneSession != null) {
			// Found it.  Update the object with the information in the notification.
			phoneSession.updateState(callStatus);
		} else {
			throw new RuntimeException("Unable to find PhoneSession for " + addressOfRecord);
		}
	}

	/**
	 * Return a web page that provides status on a session monitoring a phone.
	 * Depending on the state of the phone, options are provided to make a new
	 * call, end an existing call, or close the monitoring session altogether.
	 * @param phoneSession - phone session state object for which status is requested
	 * @return - String data that should be sent back to the browser
	 */
	private String getStatusPage(PhoneSession phoneSession) {
		StringBuffer sbResult = new StringBuffer("");
		
		if (null != phoneSession) {
			// Found call information in the session.
			sbResult.append("<HTML>\n");
			sbResult.append("<BODY>\n");
			sbResult.append("<H1>Phone Status</H1>\n");
			sbResult.append("<UL>\n");
			sbResult.append("<LI><B>Address of record:</B> " + phoneSession.getAddressOfRecord() + "<BR>\n");
			sbResult.append("<LI><B>Call status:</B> " + phoneSession.getCallState() + "<BR>\n");
			sbResult.append("<LI><B>Caller:</B> " + phoneSession.getCallerAddressOfRecord() + "<BR>\n");
			sbResult.append("<LI><B>Callee:</B> " + phoneSession.getCalleeAddressOfRecord() + "<BR>\n");
			sbResult.append("<LI><B>Call ID:</B> " + phoneSession.getCallID() + "<BR>\n");
			sbResult.append("</UL>\n");
			// Expose a button to get a call status update.
			sbResult.append(createGetForm(PATH_GET_CALL_STATUS, "Refresh call status"));
			sbResult.append("<HR>\n");
			
			// Expose a button to make a call if the phone is inactive
			if (phoneSession.getCallState().equals(CallState.CALL_STATUS_CLEARED.value()) 
					|| phoneSession.getCallState().equals(CallState.CALL_STATUS_SESSION_OPEN.value())) {
				sbResult.append("<FORM action=\"/" + CONTEXT_ROOT + "/" + SERVLET_NAME + PATH_MAKE_CALL + "\" method=\"post\">\n");
				sbResult.append("Peer address of record: <INPUT type=\"text\" name=\"" + PEER_ADDRESS_OF_RECORD + "\">\n");
				sbResult.append("<INPUT type=\"submit\" value=\"Make call\">\n");
				sbResult.append("</FORM>\n");
			} 
			
			// Expose a button to end the call, if the call is active.
			else if (phoneSession.getCallState().equals(CallState.CALL_STATUS_ESTABLISHED.value())) {
				sbResult.append(createGetForm(PATH_END_CALL, "End the call"));
			}

			// Expose a button to close the session.
			sbResult.append(createGetForm(PATH_CLOSE_SESSION, "Close the session"));
			
			sbResult.append("</BODY></HTML>");
		} else {
			sbResult.append("<HTML><BODY>\n");
			sbResult.append("No session information found.\n");
			sbResult.append("</BODY></HTML>");
		}
		return sbResult.toString();
	}
	
	/**
	 * Return a web page that presents a form to open a session.  This has the affect
	 * of registering for call notification.
	 * @return - String data that should be sent back to the browser
	 */
	private String getOpenSessionPage() {
		StringBuffer sbResult = new StringBuffer("");
		sbResult.append("<HTML>\n");
		sbResult.append("<BODY>\n");
		sbResult.append("<FORM action=\"/" + CONTEXT_ROOT + "/" + SERVLET_NAME + PATH_OPEN_SESSION + "\" method=\"post\">\n");
		sbResult.append("<H1>CEA Web Service Sample</H1><HR>\n");
		sbResult.append("<H1>Open a session to monitor a phone</H1>\n");
		sbResult.append("Phone address of record: <INPUT type=\"text\" name=\"" + ADDRESS_OF_RECORD + "\"><BR>\n");
		sbResult.append("<P>\n");
		sbResult.append("<INPUT type=\"submit\" value=\"Open session\">\n");
		sbResult.append("</FORM></BODY></HTML>");
		return sbResult.toString();
	}
	
	/**
	 * Return a web page that shows an error occurred.
	 * @param error - String to be used in the error page returned
	 * @return - String data that should be sent back to the browser
	 */
	private String getErrorPage(String error) {
		StringBuffer sbResult = new StringBuffer("");
		sbResult.append("<HTML>\n");
		sbResult.append("<BODY>\n");
		sbResult.append("<H1>Error</H1>\n");
		sbResult.append("Details: " + error + "<BR>\n");
		sbResult.append("Available options:\n");
		sbResult.append(createGetForm(PATH_OPEN_SESSION, "Open a session"));
		sbResult.append("</BODY></HTML>");
		return sbResult.toString();
	}

	
	/**
	 * Utility method to create a form with the given action and description
	 * @param action - the path that will be added to the URL to determine the action
	 * @param description - the label on the button of the form.
	 * @return - text that makes up a form
	 */
	private String createGetForm(String action, String description) {
		StringBuffer sbResult = new StringBuffer("");
		sbResult.append("<FORM action=\"/" + CONTEXT_ROOT + "/" + SERVLET_NAME + action + "\" method=\"get\">\n");
		sbResult.append("<INPUT type=\"submit\" value=\"" + description + "\">\n");
		sbResult.append("</FORM>\n");
		return sbResult.toString();
	}
	
}
