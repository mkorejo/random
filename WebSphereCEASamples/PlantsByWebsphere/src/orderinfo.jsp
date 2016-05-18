<!-- DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN"-->
<!-- 
COPYRIGHT LICENSE: This information contains sample code provided in
source code form. You may copy, modify, and distribute these sample
programs in any form without payment to IBM for the purposes of
developing, using, marketing or distributing application programs
conforming to the application programming interface for the operating
platform for which the sample code is written. Notwithstanding anything
to the contrary, IBM PROVIDES THE SAMPLE SOURCE CODE ON AN "AS IS" BASIS
AND IBM DISCLAIMS ALL WARRANTIES, EXPRESS OR IMPLIED, INCLUDING, BUT NOT
LIMITED TO, ANY IMPLIED WARRANTIES OR CONDITIONS OF MERCHANTABILITY,
SATISFACTORY QUALITY, FITNESS FOR A PARTICULAR PURPOSE, TITLE, AND ANY
WARRANTY OR CONDITION OF NON-INFRINGEMENT. IBM SHALL NOT BE LIABLE FOR ANY
DIRECT, INDIRECT, INCIDENTAL, SPECIAL OR CONSEQUENTIAL DAMAGES ARISING OUT
OF THE USE OR OPERATION OF THE SAMPLE SOURCE CODE. IBM HAS NO OBLIGATION
TO PROVIDE MAINTENANCE, SUPPORT, UPDATES, ENHANCEMENTS OR MODIFICATIONS TO
THE SAMPLE SOURCE CODE.
    
(C) COPYRIGHT International Business Machines Corp., 2009, 2010
All Rights Reserved * Licensed Materials - Property of IBM
-->

    <html>
    <head>
    <title></title>
      	<script type="text/javascript" src="/PlantsByWebSphereAjax/applycss.js" language="JavaScript"></script>
    
   
    	<script type="text/javascript" src="/PlantsByWebSphereAjax/ceadojo/dojo/dojo.js.uncompressed.js"
	  		djconfig="parseOnLoad: true, isDebug: false"></script>
       	
        <script type="text/javascript">
         	ceadojo.require("dijit.form.TextBox");
			ceadojo.require("dijit.form.ValidationTextBox");
			ceadojo.require("dijit.form.NumberTextBox");
			ceadojo.require("dijit.form.CurrencyTextBox");
			ceadojo.require("dijit.form.DateTextBox");
			ceadojo.require("dijit.form.TimeTextBox");
			ceadojo.require("dijit.form.FilteringSelect");
			ceadojo.require("dijit.form.CheckBox");
			ceadojo.require("dijit.form.ComboBox");
			ceadojo.require("dojox.wire");
			ceadojo.require("dojox.wire.ml.Invocation");
			ceadojo.require("dojox.wire.ml.DataStore");
			ceadojo.require("dojox.wire.ml.Transfer");
			ceadojo.require("dojox.wire.ml.Data");
            ceadojo.require("dojox.validate.us");
			ceadojo.require("dojo.currency");
			ceadojo.require("dojo.date.locale");
			ceadojo.require("dojo.data.ItemFileReadStore");
            ceadojo.require("dojo.parser");	// scan page for widgets and instantiate them
		</script>

        <style>
        
             @import "/PlantsByWebSphereAjax/ceadojo/dijit/themes/tundra/tundra.css";
             @import "/PlantsByWebSphereAjax/ceadojo/cea/widget/TwoWayForm/TwoWayForm.css";
		         
          .testExample {
				background-color:#fbfbfb;
				padding:1em;
				margin-bottom:1em;
				border:1px solid #bfbfbf;
			}
        
        

    	  span.invalid, span.missing {
    			display: inline;
    			margin-left: 1em;
    			font-weight: bold;
    			font-style: italic;
    			font-family: Arial, Verdana, sans-serif;
    			color: #f66;
    			font-size: 0.9em;
    		}
    
    		.errorMessage {
    			font-weight:bold;
    			font-family:Arial, Verdana, sans-serif;
    			color:#ff0000;
    			font-size:0.9em;
    		}
    		.warningMessage {
    			font-weight:bold;
    			font-family:Arial, Verdana, sans-serif;
    			color:#ff9900;
    			font-size:0.9em;
    		}
    		.noticeMessage {
    			font-weight: normal;
    			font-family:Arial, Verdana, sans-serif;
    			color:#663;
    			font-size:0.9em;}  

            .medium.dojoValidateEmpty {
                background-color: #FFFFFF;
                
             }
             
             .small {
				width: 2.5em;
			}
			.medium {
				width: 10em;
			}
			.long {
				width: 20em;
			}


			.noticeMessage {
				color:#093669;
				font-size:0.95em;
				margin-left:0.5em;
			}

			.dojoTitlePaneLabel label {
				font-weight:bold;
			}

                  
    	</style>
    	
        <script>
             //Insert our dynamic combo that creates the expiry dates based off the browser info.
		//This caluclates the exiry date info for the combo based off the current user's system date
		//The back end still has to validate this, of course, but this way the dates showin is always
		//current + 10 years.  Keeps from having to edit the form to add new years later.
		
				var data = {identifier: "name", items: []}
				var cDate = new Date();
				var year = cDate.getFullYear();
				var i
				for (i = 0; i < 10; i++) {
					data.items.push({name: "" + (year + i)});
				}
                console.log(data);
                dStore = new ceadojo.data.ItemFileReadStore({data: data});

        function filterCC(value) {
            var result = "";
            var leadingLength;

            if (value.length <= 4) {
               return value;
            }

            leadingLength = value.length - 4;

            for (var i = 0; i < leadingLength; ++i) {
               result += "*";
            }

            result += value.substring (leadingLength);

            return result;
        }

    	function verifyForm()
    	{
    		var billship = document.billship;
    
    		if ((!exists(billship.bname.value)) ||
    			  (!exists(billship.baddr1.value)) ||
    			  (!exists(billship.bcity.value)) ||
    			  (!exists(billship.bstate.value)) ||
    			  (!exists(billship.bzip.value)) ||
    			  (!exists(billship.bphone.value)) ||
    			  (!exists(document.getElementById('sname').value)) ||
    			  (!exists(document.getElementById('saddr1').value)) ||
    			  (!exists(document.getElementById('scity').value)) ||
    			  (!exists(document.getElementById('sstate').value)) ||
    			  (!exists(document.getElementById('szip').value)) ||
    			  (!exists(document.getElementById('sphone').value)) ||
    			  (!exists(document.getElementById('ccardnum').value)) ||
    			  (!exists(document.getElementById('ccholdername').value)))
    		{
    			alert("All required fields must be filled in.");
    			return false;
    		}
    		else if (!verifyNum(billship.bzip.value)) {
    		    alert("Billing Zip Code is not valid.");
    		    return false;
    		}
    		else if (!verifyNum(document.getElementById('szip').value)) {
    		    alert("Shipping Zip Code is not valid.");
    		    return false;
    		}
    		else if (!verifyPhone(billship.bphone.value)) {
    			alert("Billing Phone is not valid.");
    		    return false;
    		}
    		else if(!verifyPhone(document.getElementById('sphone').value)) {
    		    alert("Shipping Phone is not valid.");
    		    return false;
    		}
    		else if (!verifyCreditCard(document.getElementById('ccardnum').value)) {
		    	alert("Credit Card Number is not valid.");
		  		return false;
			}
    
    		return true;
    
    
    	}
    
    	function verifyNum(numVal)
    	{
    		 var result = false;
    	    for (var i = 0; i < numVal.length; i++) {
    	        if (parseFloat(numVal.charAt(i))) {
    	            result = true;
    	            break;
    			  }
    		 }
    	    return result;
    	}
    
    	function verifyPhone(phoneVal)
    	{
    		var result = false;
    		var cnt = 0;
    		for (var i = 0; i < phoneVal.length; i++) {
    	        if (parseFloat(phoneVal.charAt(i))) {
    	            cnt++;
    	            if (cnt >= 7) {
    						 result = true;
    						 break;
    					}
    			  }
    		 }
    	    return result;
    	}
    	
    	function verifyCreditCard(ccnum)
		{
			var result=false;

			if (!isNaN(parseFloat(ccnum))) {
				result=true;
			}

			return result;
		}
    
    
    	function exists(inputVal)
    	{
    		var result = false;
    	    for (var i = 0; i <= inputVal.length; i++) {
    	        if ((inputVal.charAt(i) != " ") && (inputVal.charAt(i) != "")) {
    	            result = true;
    	            break;
    			}
    	 	}
    
    	    return result;
    	}
    <%@ page import="com.ibm.websphere.samples.plantsbywebsphereejb.StoreItem,java.util.*" session="true" isThreadSafe="true" isErrorPage="false" %>
    
    <%
    com.ibm.websphere.samples.plantsbywebsphereejb.ShoppingCart shoppingCart = 
      (com.ibm.websphere.samples.plantsbywebsphereejb.ShoppingCart)
      session.getAttribute(com.ibm.websphere.samples.plantsbywebsphereejb.Util.ATTR_CART);
            
    java.util.Vector cartitems = null;
    float  total     = 0;
    double stdGround = 4.99;
    double secDay = 8.99;
    double nextDay = 12.99;
    
    if (shoppingCart != null)
    {
       cartitems = shoppingCart.getItems();
       total = shoppingCart.getTotalCost();
    }
    %>    
    
    	function setShipRate()
    	{
          
            switch(document.billship.shippingMethod.selectedIndex) {
    
                case 1:
                    document.getElementById('changeShipType').innerHTML = '<font size="2" face="Verdana, Arial, Helvetica, sans-serif">Shipping, Second Day Air:</font>';
    				document.getElementById('changeCost').innerHTML = '<font size="2" face="Verdana, Arial, Helvetica, sans-serif">$8.99</font>';   				
    				document.getElementById('changeTotal').innerHTML = '<font size="2" face="Verdana, Arial, Helvetica, sans-serif"><b><%= java.text.NumberFormat.getCurrencyInstance(java.util.Locale.US).format(new Float(total + 8.99)) %></b></font>';
    				break;
                case 2:
                    document.getElementById('changeShipType').innerHTML = '<font size="2" face="Verdana, Arial, Helvetica, sans-serif">Shipping, Next Day Air:</font>';
    				document.getElementById('changeCost').innerHTML = '<font size="2" face="Verdana, Arial, Helvetica, sans-serif">$12.99</font>';
                    document.getElementById('changeTotal').innerHTML = '<font size="2" face="Verdana, Arial, Helvetica, sans-serif"><b><%= java.text.NumberFormat.getCurrencyInstance(java.util.Locale.US).format(new Float(total + 12.99)) %></b></font>';
    				break;
    			default:
                    document.getElementById('changeShipType').innerHTML = '<font size="2" face="Verdana, Arial, Helvetica, sans-serif">Shipping, Standard Ground:</font>';
    				document.getElementById('changeCost').innerHTML = '<font size="2" face="Verdana, Arial, Helvetica, sans-serif">$4.99</font>';
                    document.getElementById('changeTotal').innerHTML = '<font size="2" face="Verdana, Arial, Helvetica, sans-serif"><b><%= java.text.NumberFormat.getCurrencyInstance(java.util.Locale.US).format(new Float(total + 4.99)) %></b></font>';
    		}    	
        }
	
		//We don't want the NumberFormat boxes on this page to format the value,
		//so extend and replace the format function.  The ideal way would be to subclass
		//the widget, then use the subclass ... but in this case it was faster to just
		//redefine the function on the class for this page.
		var removeFormat = {
		    format: function(value, constraints) {
                return value;
			}
		}
        ceadojo.extend(ceadijit.form.NumberTextBox, removeFormat);

	</script>
    
    
    </head>
    <body CLASS="tundra"> 
            
    <%
		com.ibm.websphere.samples.plantsbywebsphereejb.CustomerInfo customerInfo = 
      	(com.ibm.websphere.samples.plantsbywebsphereejb.CustomerInfo) 
      	session.getAttribute(com.ibm.websphere.samples.plantsbywebsphereejb.Util.ATTR_CUSTOMER);
		String[] shippingMethods = com.ibm.websphere.samples.plantsbywebsphereejb.Util.getFullShippingMethodStrings();
	%>

    <form ceaCollabOnSubmit="return verifyForm(this);" target="_self" name="billship" method="post" action="/PlantsByWebSphereAjax/servlet/ShoppingServlet?action=orderinfodone" ceadojoType="cea.widget.TwoWayForm">
    <table border="0" cellpadding="0" cellspacing="5" width="100%">
    	<tr>
        	<td><p class="trail"><a class="trail" class="footer" href="/PlantsByWebSphereAjax/index.html"  >Home</a> &gt; <a class="trail" class="footer" href="/PlantsByWebSphereAjax/servlet/ShoppingServlet?action=gotocart"  >Shopping Cart</a></p></td>
      	</tr>
    
    	<tr>  <!-- BEGIN CHECKOUT HEADING -->
    		<td nowrap>
    		      	<table cellpadding="0" cellspacing="0" border="0" width="80%">
    
    		        <tr>
    		          	<td width="100%" valign="middle"><H1>Checkout</H1></td>
    		          	<td align="right" valign="middle" nowrap></td>
    			      	<td valign="middle"></td>
    			    </tr>
    
    		        <tr>
    		          	<td colspan="3"><p>Enter the billing and shipping information for your order below. After you have completed all the required fields, click
    		          		the "Checkout Now" button.</p><br></td>
    		        </tr>
    				</table>
    		</td>
    
    
       	</tr> <!-- END CHECKOUT HEADING -->
		<tr>  <!-- BEGIN BILLING ADDRESS -->

	    <td colspan="3">
					<table cellpadding="0" cellspacing="3" border="0" width="100%">

			        <tr>
			          	<td colspan="3">
			          	<table border="0" cellpadding="0" cellspacing="5">
			          	<h4 align="left"><B>1. Billing Address</B></h4>
			          	<colgroup class="label">
			          	<colgroup>
			          	<colgroup>			          	
			          	</table>
			          	</TD>
                        
			        </tr>

					</table>
					
					<table cellpadding="0" cellspacing="5" border="0" width="100%">
					<tr>
			    		<td nowrap width="120"><P><label for="bname">Full Name&nbsp;</label></td>
				    	<TD><IMG border="0" src="/PlantsByWebSphereAjax/images/required.gif" width="10" height="15" alt="Required indicator"></TD>
				    	<TD width="100%"><P><input id="bname" type="text" name="bname" class="medium"
						 	ceadojoType="dijit.form.ValidationTextBox"
					        propercase="true"
					        required="true"
					        promptMessage="Enter Name" ceaCollabValidation="default" ceaCollabWriteAccess="writer"/>                                 
                                </P></TD>
					</tr>

                  
					<tr>
						<td nowrap width="120"><p><label for="baddr1">Address Line 1&nbsp;</label></td>
				    	<td><img border="0" src="/PlantsByWebSphereAjax/images/required.gif" width="10" height="15" alt="Required indicator"></td>
				    	<td width="100%"><p><input type="text" id="baddr1" name="baddr1" class="medium"
							ceadojoType="dijit.form.ValidationTextBox"
					        lowercase="false"
					        required="true"
					        promptMessage="Enter Address" ceaCollabValidation="default" ceaCollabWriteAccess="writer"/>
                                </p></td>

					</tr>

					<tr>
				    	<td nowrap><p><label for="baddr2">Address Line 2&nbsp;</label></td>
				    	<td></td>
				    	<!-- <td><p><input type="text" id="baddr2" name="baddr2" class="medium" value="<%= customerInfo.getAddr2() %>"></p></td> -->
                        
				    	<td width="100%"><p><input type="text" id="baddr2" name="baddr2" class="medium"
							ceadojoType="dijit.form.ValidationTextBox"
					        lowercase="false"
					        required="false"
					        promptMessage="Enter Address" ceaCollabValidation="default" ceaCollabWriteAccess="writer"/>
                                </p></td>
                        
					</tr>

					<tr>
					    <td nowrap><p><label for="bcity">City&nbsp;</label></td>

				    	<td><img border="0" src="/PlantsByWebSphereAjax/images/required.gif" width="10" height="15" alt="Required indicator"></td>
				    	<td><p><input type="text" id="bcity" name="bcity" class="medium"
						    ceadojoType="dijit.form.ValidationTextBox"
					        lowercase="false"
					        required="true"
					        promptMessage="Enter City" ceaCollabValidation="default" ceaCollabWriteAccess="writer" /></P></TD>
					</tr>

					<tr>
					    <td nowrap><p><label for="bstate">State&nbsp;</label></td>
					    <td><img border="0" src="/PlantsByWebSphereAjax/images/required.gif" width="10" height="15" alt="Required indicator"></td>
				    	<td width="100%">
                            <p>
                                <input type="text" id="bstate" name="bstate" class="medium"
            						   ceadojoType="dijit.form.ValidationTextBox"
            					       uppercase="true"
            					       required="true"
            					       promptMessage="Enter State" ceaCollabValidation="default" ceaCollabWriteAccess="writer" /></P></TD>
                            
                        
					</tr>

					<tr>
					    <td nowrap><p><label for="bzip">Zip Code&nbsp;</label></td>
					    <td><img border="0" src="/PlantsByWebSphereAjax/images/required.gif" width="10" height="15" alt="Required indicator"></td>
					    <td><p><input type="text" id="bzip" name="bzip" class="medium"
							  ceadojoType="dijit.form.NumberTextBox"
					          size=5
					          maxlength="9"
                              required="true"
                              places="9"
                              promptMessage="Enter ZipCode"  ceaCollabValidation="default" ceaCollabWriteAccess="writer"/></p></td>
					</tr>

					<tr>
					    <td nowrap><p><label for="bphone">Phone (daytime)&nbsp;</label></td>
					    <td><img border="0" src="/PlantsByWebSphereAjax/images/required.gif" width="10" height="15" alt="Required indicator"></td>

				    	<td width="100%"><p><input type="text" id="bphone" name="bphone" class="medium"
							ceadojoType="dijit.form.ValidationTextBox"
					        lowercase="false"
					        required="true"
					        promptMessage="Enter Phone" ceaCollabValidation="default" ceaCollabWriteAccess="writer"/>
                                </p></td>

					</tr>
					</table>
				</td>	 <!-- END BILLING ADDRESS -->



				<td colspan="3">  <!-- BEGIN SHIPPING ADDRESS -->

						<table border="0" cellpadding="0" cellspacing="3" width="100%">
						<h4 align="left"><B>2. Shipping Information</B></h4>
						<colgroup class="label">
						<colgroup>
						<colgroup>

						<tr>
						  <td colspan="3">
						    <table border="0" cellpadding="0" cellspacing="3" width="100%">
						      <tr>

						        <td valign="middle" nowrap><p><input type="checkbox" id="shipisbill" ceadojoType="dijit.form.CheckBox">&nbsp;</p></td>
						        <td valign="middle" nowrap><p>Check here if the shipping address is the same as the billing address.</p></td>
						      </tr>
						    </table>
						  </td>
						</tr>

						<TR>
						  <TD nowrap><P><label for="sname">Full Name&nbsp;</label></TD>

						  <TD><IMG border="0" src="/PlantsByWebSphereAjax/images/required.gif" width="10" height="15" alt="Required indicator"></TD>
						  <TD width="100%"><P><input type="text" id="sname" name="_sname" class="medium"
								ceadojoType="dijit.form.ValidationTextBox" ceaCollabValidation="default" ceaCollabWriteAccess="writer"
					            propercase="true"
					            required="true"
					            promptMessage="Enter Name" /></P></TD>
						</TR>

						<tr>
						  <td nowrap><p><label for="saddr1">Address Line 1&nbsp;</label></td>
						  <td><img border="0" src="/PlantsByWebSphereAjax/images/required.gif" width="10" height="15" alt="Required indicator"></td>
						  <td width="100%"><p><input type="text" id="saddr1" name="_saddr1" class="medium"
								ceadojoType="dijit.form.ValidationTextBox" ceaCollabValidation="default" ceaCollabWriteAccess="writer"
					            lowercase="false"
					            required="true"
					            promptMessage="Enter Name"/></p></td>
						</tr>

						<tr>
						  <td nowrap width="120"><p><label for="saddr2">Address Line 2&nbsp;</label></td>
						  <td></td>
						  <td width="100%"><p><input type="text" id="saddr2" name="_saddr2" class="medium"
								ceadojoType="dijit.form.ValidationTextBox" ceaCollabValidation="default" ceaCollabWriteAccess="writer"
					            lowercase="false"
					            required="false"
					            promptMessage="Enter Address"/></p></td>
						</tr>

						<tr>
						  <td nowrap><p><label for="scity">City&nbsp;</label></td>
						  <td><img border="0" src="/PlantsByWebSphereAjax/images/required.gif" width="10" height="15" alt="Required indicator"></td>

						  <td><p><input type="text" id="scity" name="_scity" class="medium"
								ceadojoType="dijit.form.ValidationTextBox" ceaCollabValidation="default" ceaCollabWriteAccess="writer"
					            lowercase="false"
					            required="true"
					            promptMessage="Enter City"/></p></td>
						</tr>

						<tr>
						  <td nowrap><p><label for="sstate">State&nbsp;</label></td>
						  <td><img border="0" src="/PlantsByWebSphereAjax/images/required.gif" width="10" height="15" alt="Required indicator"></td>
						  <td><p>
                                <input type="text" id="sstate" name="_sstate" class="medium"
            						   ceadojoType="dijit.form.ValidationTextBox" ceaCollabValidation="default" ceaCollabWriteAccess="writer"
            					       uppercase="true"
            					       required="true"
            					       promptMessage="Enter State" /></P></TD>
						</tr>

						<tr>
						  <td nowrap><p><label for="szip">Zip Code&nbsp;</label></td>
						  <td><img border="0" src="/PlantsByWebSphereAjax/images/required.gif" width="10" height="15" alt="Required indicator"></td>
						  <td><p><input type="text" id="szip" name="_szip" class="medium" value=""
							  ceadojoType="dijit.form.NumberTextBox" ceaCollabValidation="default" ceaCollabWriteAccess="writer"
					          size=5
					          maxlength="9"
                              required="true"
                              promptMessage="Enter ZipCode"/></p></td>
						</tr>

						<tr>
						  <td nowrap><p><label for="sphone">Phone (daytime)&nbsp;</label></td>
						  <td><img border="0" src="/PlantsByWebSphereAjax/images/required.gif" width="10" height="15" alt="Required indicator"></td>

						  <td><p><input type="text" id="sphone" name="_sphone" class="medium" value=""
							  ceadojoType="dijit.form.TextBox" ceaCollabValidation="default" ceaCollabWriteAccess="writer"
                              lowercase="false"
                              required="true"
                              size="2"
                              promotMessage="Enter Phone"/> </p></td>
                                    
						</tr>

						</table>
                        
                        <!-- These are the real values that get submitted over. -->
                        <input type="hidden" id="_sname"  name="sname"  value=""></input>
                        <input type="hidden" id="_saddr1" name="saddr1" value=""></input>
                        <input type="hidden" id="_saddr2" name="saddr2" value=""></input>
                        <input type="hidden" id="_scity"  name="scity"  value=""></input>
                        <input type="hidden" id="_sstate" name="sstate" value=""></input>
                        <input type="hidden" id="_szip"   name="szip"   value=""></input>
                        <input type="hidden" id="_sphone" name="sphone" value=""></input>
                        
					  </td>

					  </tr>	 <!-- END SHIPPING INFORMATION -->

					  	  <tr>	 <!-- BEGIN SHIPPING METHOD -->
					  	  <td colspan="3" align="top">

                           					  	  	<table border="0" cellspacing="3" Cellpadding="0" width="100%">
					  	  	<h4 align="left"><B>3. Shipping Method</B></h4>
					  	  	<tr> </TR>
					  	   	  <tr>
					  	  	   <td colspan="3"><p>Select a shipping method below.</p><br></td>
					  	  	  </tr>
                              
                               
                              
					  	  	   <td width="120" nowrap><p><label for="shippingMethod">Shipping Method&nbsp;</label></p></td>
					  	  	   <td><img border="0" src="/PlantsByWebSphereAjax/images/required.gif" width="10" height="15" alt="Required indicator"></td>

					  	  	   <td class="item" width="100%">
					  	  	   					  	  	   	   <p>
					  	  	   	   <select id="shippingMethod" ceadojoType="dijit.form.FilteringSelect" ceaCollabWriteAccess="writer" ceaCollabValidation="default" name="shippingMethod" onChange="javascript:setShipRate();">
                                                 <%for (int i = 0; i < shippingMethods.length; i++)
                                                 {
                                                 if (i == 0)
                                                    {%> <option selected value="<%=i%>"><%=shippingMethods[i]%>
                                                  <%}
                                                 else
                                                    {%> <option value="<%=i%>"><%=shippingMethods[i]%>
                                                  <%}
                                                 } %>
                                    </select> </p>					  	  	
					  	  	   </td>
					  	  	   	   
                              <tr>
					  	  	  
					  	  	    <td nowrap width="120"><p><label for="cc">Credit Card&nbsp;</label></td>
					  	  	    <td><img border="0" src="/PlantsByWebSphereAjax/images/required.gif" width="10" height="15" alt="required indicator"></td>


					  	  	    <td><p>
					  	  			<select id="ccardname" ceadojoType="dijit.form.FilteringSelect" ceaCollabWriteAccess="reader" size="1" name="ccardname">
					  	  	        <option value="American Express">American Express</option>
					  	  	        <option value="Discover">Discover</option>
					  	  	        <option value="MasterCard">MasterCard</option>
					  	  	        <option value="VISA">VISA</option></select></p></td>
					  	  	  
                              </tr>

					  	  	  <tr>
					  	  	    <td nowrap><p><label for="cn">Card Number&nbsp;</label></td>
					  	  	    <td><img border="0" src="/PlantsByWebSphereAjax/images/required.gif" width="10" height="15" alt="required indicator"></td>
					  	  	    <td><p><input type="text" id="ccardnum" ceadojoType="dijit.form.TextBox" ceaCollabFilter="filterCC" ceaCollabWriteAccess="reader" class="medium"
					  					/></P></td>
					  	  	  </tr>

					  	  	  <tr>
					  	  	    <td nowrap><p><label for="em">Expiration Month&nbsp;</label></td>
					  	  	    <td><img border="0" src="/PlantsByWebSphereAjax/images/required.gif" width="10" height="15" alt="required indicator"></td>

					  	  	    <td><p><select ceadojoType="dijit.form.FilteringSelect" ceaCollabWriteAccess="reader" id="ccexpiresmonth" size="1" name="ccexpiresmonbh">
					  	  	        <option value="01">01</option>
					  	  	        <option value="02">02</option>
					  	  	        <option value="03">03</option>
					  	  	        <option value="04">04</option>
					  	  	        <option value="05">05</option>

					  	  	        <option value="06">06</option>
					  	  	        <option value="07">07</option>
					  	  	        <option value="08">08</option>
					  	  	        <option value="09">09</option>
					  	  	        <option value="10">10</option>
					  	  	        <option value="11">11</option>

					  	  	        <option value="12">12</option></select></p></td>
					  	  	  </tr>
					  	  	  <tr>
					  	  	    <td nowrap><p><label for="ey">Expiration Year&nbsp;</label></td>
					  	  	    <td><img border="0" src="/PlantsByWebSphereAjax/images/required.gif" width="10" height="15" alt="required indicator"></td>
					  	  	    <td><p><select ceadojoType="dijit.form.ComboBox" ceaCollabWriteAccess="reader" store="dStore" size="1" name="ccexpiresyear" id="ccexpiresyear">
                                    </select></p></td>
					  	  	  </tr>
					  	  	  <tr>

					  	  	    <td nowrap><p><label for="cn">Cardholder Name&nbsp;</label></td>
					  	  	    <td><img border="0" src="/PlantsByWebSphereAjax/images/required.gif" width="10" height="15" alt="required indicator"></td>
					  	  	    <td><p><input type="text" id="ccholdername" class="medium" value=""
					  				ceadojoType="dijit.form.ValidationTextBox" ceaCollabWriteAccess="reader"
					                    propercase="true"
					                    required="true"
					                    promptMessage="Enter Name" />
                                    </P></TD>
					  		  </tr>
					  	  	  </table>
                              </td> <!-- END SHIPPING METHOD -->

        	  	 
	  	 <td align="top"> <!-- YOUR ORDER -->
		 		 <h4>4. Your Order</h4>
		 		 <table cellpadding="0" cellspacing="3" border="0" width="80%">

		 		 	<tr>
		 		 		<td colspan="3"><p>Below is your final order.  To make any changes to your order, click the "Continue Shopping" button below.</p><br></td>

		 		 	</tr>
		 		 </table>


		 		 <table border="0" cellpadding="1" cellspacing="0" width="80%">

		 		 		<tr bgcolor="#ffffdd" align="center"><p><b>Order Details</b></p></tr>
		 		        <tr bgcolor="#eeeecc">
		 		        	<th><img src="/PlantsByWebSphereAjax/images/1x1_trans.gif" width="4" height="4" align="left" border="0" alt=""></th>
		 		         	<th class="item" align="left">ITEM #</th>
		 		        	<th class="item" align="left" nowrap>ITEM DESCRIPTION</th>
		 		        	<th class="item" align="left">PACKAGING</th>
		 		        	<th class="item" align="left">QUANTITY</th>

		 		        	<th class="item" align="left">PRICE</th>
		 		        	<th class="item" align="left">SUBTOTAL</th>
		 		         	<th><img src="/PlantsByWebSphereAjax/images/1x1_trans.gif" width="4" height="4" align="left" border="0" alt=""></th>
		 		        </tr>
		<%
          if (cartitems != null)
          {
             int cnt = 0;
             for (java.util.Enumeration e = cartitems.elements(); e.hasMoreElements();)
             {
               com.ibm.websphere.samples.plantsbywebsphereejb.StoreItem  storeItem = (com.ibm.websphere.samples.plantsbywebsphereejb.StoreItem) e.nextElement();

               String id      =  storeItem.getID();
               String name    =  storeItem.getName();
               int quantity   =  storeItem.getQuantity();
               float price    =  storeItem.getPrice();
               String pkginfo =  storeItem.getPkginfo();

               String priceString = java.text.NumberFormat.getCurrencyInstance(java.util.Locale.US).format(new Float(price));
               String subtotalPriceString = java.text.NumberFormat.getCurrencyInstance(java.util.Locale.US).format(new Float(price * quantity));
               
           %>		 		        

			   <tr bgcolor="#ffffdd">
                 <td valign="top"><img src="/PlantsByWebSphereAjax/images/1x1_trans.gif" width="2" height="22" align="left" border="0" alt=""></td>
                 <td valign="top" nowrap><p><%= id %> </p></td>
                 <td valign="top" nowrap><p><b><%= name %></b></p></td>
                 <td valign="top"><p><%= pkginfo%></p></td>
                 <td valign="top"><p><%= quantity%> </p></td>
                 <td align="right" valign="top"><p><%= priceString %></p></td>
                 <td align="right" valign="top"><p><%= subtotalPriceString %></p></td>
                 <td valign="top"><img src="/PlantsByWebSphereAjax/images/1x1_trans.gif" width="2" height="22" align="left" border="0" alt=""></td>
               </tr>

		 <%
               cnt++;
              }
           }
         %>	 		    
		 		    
		 		    
		 		    
		 		    <tr bgcolor="#ffffdd">
		 		        	<td align="right" valign="top" colspan="8"><hr size="1" noshade></td>
		 		        </tr>

		 		        <tr bgcolor="#ffffdd">
		 		        	<td align="right" valign="top" colspan="6"><p>Order Subtotal: </p></td>
		 		        	<td valign="top" align="right"><p><%= java.text.NumberFormat.getCurrencyInstance(java.util.Locale.US).format(new Float(total))%></p></td>

		 		        	<td valign="top"><img src="/PlantsByWebSphereAjax/images/1x1_trans.gif" width="2" height="22" align="left" border="0" alt=""></td>
		 		        </tr>


		 		        <tr bgcolor="#ffffdd">
		 		        	<td nowrap align="right" valign="top" colspan="6" id="changeShipType"><p>Shipping, Standard Ground:</p></td>


		 		        	<td align="right" valign="top" id="changeCost"><p>$4.99</p></td>

		 		        <td valign="top"><img src="/PlantsByWebSphereAjax/images/1x1_trans.gif" width="2" height="22" align="left" border="0" alt=""></td>
		 		        </tr>

		 		        <tr bgcolor="#ffffdd">
		 		        	<td align="right" valign="top" colspan="8"><hr size="1" noshade></td>
		 		        </tr>

		 		        <tr bgcolor="#ffffdd">
		 		        	<td align="right" valign="top" colspan="6"><p><b>Order Total: </b></p></td>
		 		        	<td style="font-family: Verdana, Arial, Helvetica, sans-serif; font-size: .9em;" align="right" valign="top" id="changeTotal"><p><b><%= java.text.NumberFormat.getCurrencyInstance(java.util.Locale.US).format(new Float(total + 4.99))%></b></p></td>
		 		        	<td valign="top"><img src="/PlantsByWebSphereAjax/images/1x1_trans.gif" width="2" height="22" align="left" border="0" alt=""></td>

		 		        </tr>
		 		        <tr>
		 		        	<td colspan="8" valign="top">&nbsp;</td>

		 		        </tr>
		 		        <tr>
                            
                            <td align="right" colspan="10">
                                <table cellpadding="0" cellspacing="0" border="0">
                                    <tr>
                                    
                                    <td nowrap ALIGN="right">

                                    <a href="/PlantsByWebSphereAjax/"  >
                                    <img src="/PlantsByWebSphereAjax/images/button_continue_shopping.gif" alt="Continue Shopping" border="0"></a>
                            </td>
                    
                            <td>                                                                                          
                                <input type="image" name="Checkout Now" value="completecheckout" alt="Checkout Now" src="/PlantsByWebSphereAjax/images/button_checkout_now.gif">                            </td>

                        </tr>
                </table>
              </td>
            </tr>
		      
		        </table>
		 </td>
		</table>
    </FORM>


	<table bgcolor="#669966" border="1" cellpadding="0" cellspacing="0" width="100%">
	
  	<tr>
    	<td width="1"><img border="0" src="/PlantsByWebSphereAjax/images/1x1_trans.gif" width="1" height="1" alt=""></td>
  	</tr>
	</table>
		
	<table border="0" cellpadding="5" cellspacing="0" width="100%">
  	<tr>
   		<td>
      		<img src="/PlantsByWebSphereAjax/images/poweredby_WebSphere.gif" alt="Powered by WebSphere">
    	</td> 
    
    	<td>
      		<p class="footer"><a class="footer" href="/PlantsByWebSphereAjax/servlet/ShoppingServlet?action=shopping&category=0"  >Flowers</a>&nbsp;&nbsp;:&nbsp;
                  <a class="footer" href="/PlantsByWebSphereAjax/servlet/ShoppingServlet?action=shopping&category=1"  >Fruits &amp; Vegetables</a>&nbsp;&nbsp;:&nbsp;
                  <a class="footer" href="/PlantsByWebSphereAjax/servlet/ShoppingServlet?action=shopping&category=2"  >Trees</a>&nbsp;&nbsp;:&nbsp;
                  <a class="footer" href="/PlantsByWebSphereAjax/servlet/ShoppingServlet?action=shopping&category=3"  >Accessories</a><br>
                  <a class="footer" href="/PlantsByWebSphereAjax/index.html" target="_top">Home</a>&nbsp;&nbsp;:&nbsp;
                  <a class="footer" href="/PlantsByWebSphereAjax/cart.jsp"  >Shopping Cart</a>&nbsp;&nbsp;:&nbsp;
                  <a class="footer" href="/PlantsByWebSphereAjax/servlet/AccountServlet?action=account"  >My Account</a>&nbsp;&nbsp;:&nbsp;
                  <a class="footer" href="/PlantsByWebSphereAjax/login.jsp"  >Login</a>&nbsp;&nbsp;:&nbsp;
                  <a class="footer" href="/PlantsByWebSphereAjax/help.jsp" target="_blank">Options</a></p>
    	</td>
  	</tr>
	</table>
		      

    <!-- Wires code.  This sets up markup linkage between fields in the page and events to occur when certian boxes are clicked. -->
    
	<!-- 
		Enable/disable the right hand side of the shipping address view based on the checkbox events. 
	-->
	<div ceadojoType="dojox.wire.ml.Action"
		trigger="shipisbill"
		triggerEvent="onChange">
		<div ceadojoType="dojox.wire.ml.Invocation" object="sname"    method="setDisabled" parameters="arguments[0]"></div>
		<div ceadojoType="dojox.wire.ml.Invocation" object="saddr1"   method="setDisabled" parameters="arguments[0]"></div>
		<div ceadojoType="dojox.wire.ml.Invocation" object="saddr2"   method="setDisabled" parameters="arguments[0]"></div>
		<div ceadojoType="dojox.wire.ml.Invocation" object="scity"    method="setDisabled" parameters="arguments[0]"></div>
		<div ceadojoType="dojox.wire.ml.Invocation" object="sstate"   method="setDisabled" parameters="arguments[0]"></div>
		<div ceadojoType="dojox.wire.ml.Invocation" object="szip"     method="setDisabled" parameters="arguments[0]"></div>
        <div ceadojoType="dojox.wire.ml.Invocation" object="sphone"   method="setDisabled" parameters="arguments[0]"></div>
	</div>    
    
	<!-- 
		Clone the values of form fields while typing based on the setting of the checkbox.
	-->
	<div ceadojoType="dojox.wire.ml.Action"
		trigger="bname"
		triggerEvent="onChange">
		<div ceadojoType="dojox.wire.ml.ActionFilter" required="shipisbill.checked" requiredValue="true" type="boolean"></div>        
		<div ceadojoType="dojox.wire.ml.Transfer" source="bname.value" target="sname.value"></div>
	</div>    
	<div ceadojoType="dojox.wire.ml.Action"
		trigger="baddr1"
		triggerEvent="onChange">
		<div ceadojoType="dojox.wire.ml.ActionFilter" required="shipisbill.checked" requiredValue="true" type="boolean"></div>        
		<div ceadojoType="dojox.wire.ml.Transfer" source="baddr1.value" target="saddr1.value"></div>
	</div>    
	<div ceadojoType="dojox.wire.ml.Action"
		trigger="baddr2"
		triggerEvent="onChange">
		<div ceadojoType="dojox.wire.ml.ActionFilter" required="shipisbill.checked" requiredValue="true" type="boolean"></div>        
		<div ceadojoType="dojox.wire.ml.Transfer" source="baddr2.value" target="saddr2.value"></div>
	</div>
	<div ceadojoType="dojox.wire.ml.Action"
		trigger="bcity"
		triggerEvent="onChange">
		<div ceadojoType="dojox.wire.ml.ActionFilter" required="shipisbill.checked" requiredValue="true" type="boolean"></div>        
		<div ceadojoType="dojox.wire.ml.Transfer" source="bcity.value" target="scity.value"></div>
	</div>    
	<div ceadojoType="dojox.wire.ml.Action"
		trigger="bstate"
		triggerEvent="onChange">
		<div ceadojoType="dojox.wire.ml.ActionFilter" required="shipisbill.checked" requiredValue="true" type="boolean"></div>        
		<div ceadojoType="dojox.wire.ml.Transfer" source="bstate.value" target="sstate.value"></div>
	</div>    
	<div ceadojoType="dojox.wire.ml.Action"
		trigger="bzip"
		triggerEvent="onChange">
		<div ceadojoType="dojox.wire.ml.ActionFilter" required="shipisbill.checked" requiredValue="true" type="boolean"></div>        
		<div ceadojoType="dojox.wire.ml.Transfer" source="bzip.value" target="szip.value"></div>
	</div>    
	<div ceadojoType="dojox.wire.ml.Action"
		trigger="bphone"
		triggerEvent="onChange">
		<div ceadojoType="dojox.wire.ml.ActionFilter" required="shipisbill.checked" requiredValue="true" type="boolean"></div>        
		<div ceadojoType="dojox.wire.ml.Transfer" source="bphone.value" target="sphone.value"></div>
	</div>    


    <!-- Keep the hidden fields up to date since they are what are parsed on the other side. -->
	<div ceadojoType="dojox.wire.ml.Action"
		trigger="sname"
		triggerEvent="setValue">
		<div ceadojoType="dojox.wire.ml.Transfer" source="sname.value" target="_sname.value"></div>
	</div>    
	<div ceadojoType="dojox.wire.ml.Action"
		trigger="saddr1"
		triggerEvent="setValue">
		<div ceadojoType="dojox.wire.ml.Transfer" source="saddr1.value" target="_saddr1.value"></div>
	</div>    
	<div ceadojoType="dojox.wire.ml.Action"
		trigger="saddr2"
		triggerEvent="setValue">
		<div ceadojoType="dojox.wire.ml.Transfer" source="saddr2.value" target="_saddr2.value"></div>
	</div>    
	<div ceadojoType="dojox.wire.ml.Action"
		trigger="scity"
		triggerEvent="setValue">
		<div ceadojoType="dojox.wire.ml.Transfer" source="scity.value" target="_scity.value"></div>
	</div>    
	<div ceadojoType="dojox.wire.ml.Action"
		trigger="sstate"
		triggerEvent="setValue">
		<div ceadojoType="dojox.wire.ml.Transfer" source="sstate.value" target="_sstate.value"></div>
	</div>    
	<div ceadojoType="dojox.wire.ml.Action"
		trigger="szip"
		triggerEvent="setValue">
		<div ceadojoType="dojox.wire.ml.Transfer" source="szip.value" target="_szip.value"></div>
	</div>    
    <div ceadojoType="dojox.wire.ml.Action"
		trigger="sphone"
		triggerEvent="setValue">
		<div ceadojoType="dojox.wire.ml.Transfer" source="sphone.value" target="_sphone.value"></div>
	</div>    
	
    <!-- 
		Clone the values of form fields from billing over to shipping over if the 
		shipisbill checkbox is set back to true.
	-->
	<div ceadojoType="dojox.wire.ml.Action"
		trigger="shipisbill"
		triggerEvent="onChange">
		<div ceadojoType="dojox.wire.ml.ActionFilter" required="arguments[0]" requiredValue="true" type="boolean"></div>        

		<div ceadojoType="dojox.wire.ml.Transfer" source="bname.value" target="sname.value"></div>
		<div ceadojoType="dojox.wire.ml.Transfer" source="baddr1.value" target="saddr1.value"></div>
		<div ceadojoType="dojox.wire.ml.Transfer" source="baddr2.value" target="saddr2.value"></div>
		<div ceadojoType="dojox.wire.ml.Transfer" source="bcity.value" target="scity.value"></div>
		<div ceadojoType="dojox.wire.ml.Transfer" source="bstate.value" target="sstate.value"></div>
		<div ceadojoType="dojox.wire.ml.Transfer" source="bzip.value" target="szip.value"></div>
        <div ceadojoType="dojox.wire.ml.Transfer" source="bphone.value" target="sphone.value"></div>
	</div>

    <!-- End wires code -->

       
    </body>
</html>
