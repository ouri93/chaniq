/**
 * Projet Name : Dynamic Form Processing with PHP
 * URL: http://techstream.org/Web-Development/PHP/Dynamic-Form-Processing-with-PHP
 *
 * Licensed under the MIT license.
 * http://www.opensource.org/licenses/mit-license.php
 * 
 * Copyright 2013, Tech Stream
 * http://techstream.org
 */

function addRow(tableID) {
	var table = document.getElementById(tableID);
	var rowCount = table.rows.length;
	if(rowCount < 10){							// limit the user from creating fields more than your limits
		var row = table.insertRow(rowCount);
		var colCount = table.rows[0].cells.length;
		for(var i=0; i<colCount; i++) {
			var newcell = row.insertCell(i);
			newcell.innerHTML = table.rows[0].cells[i].innerHTML;
		}
	}else{
		 alert("Maximum number of pool members are 10.");
			   
	}
}

function deleteRow(tableID) {
	var table = document.getElementById(tableID);
	var rowCount = table.rows.length;
	for(var i=0; i<rowCount; i++) {
		var row = table.rows[i];
		var chkbox = row.cells[0].childNodes[0];
		if(null != chkbox && true == chkbox.checked) {
			if(rowCount <= 1) { 						// limit the user from removing all the fields
				alert("Cannot Remove all pool members.");
				break;
			}
			table.deleteRow(i);
			rowCount--;
			i--;
		}
	}
}



function dnsValidation(objdns){
    // DNS Name Validation
    document.getElementById(objdns).addEventListener("focusout", dnsValidation);
    
    var val = document.getElementById(objdns).value;
    if (/^[a-zA-Z0-9][a-zA-Z0-9-]{1,61}[a-zA-Z0-9](?:\.[a-zA-Z]{2,})+$/.test(val)){
        //alert("Valid Domain Name: " + val);
        document.getElementById(objdns).style.borderColor="#E1E1E1";
        return true;
    }
    else
    {
        //Allow IP address as DNS name
        if(strIpValidation(val)){
            return true;
        }
        else{
            //alert("Enter Valid Domain Name!");
            document.getElementById(objdns).value = "";
            document.getElementById(objdns).style.borderColor="red";
            //document.getElementById(objdns).focus(); -- Looping issue
            return false;
        }
   }
}

function strIpValidation(ipaddr){
    if (/^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$/.test(ipaddr)) {
        return true;    
    }
    else{
        return false;        
    }    
}

function ipValidation(objip){
    // DNS Name Validation
    document.getElementById(objip).addEventListener("focusout", ipValidation);
    
    var val = document.getElementById(objip).value;
    if (/^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$/.test(val)) {
        document.getElementById(objip).style.borderColor="#E1E1E1";
        return true;    
    }
    else{
        //alert("Use Valid IP Address Format!");
        document.getElementById(objip).value = "";
        document.getElementById(objip).style.borderColor="red";
        //document.getElementById(objdns).focus(); -- Looping issue
        return false;        
    }

    
}

function portValidation(objport){
    // DNS Name Validation
    document.getElementById(objport).addEventListener("focusout", portValidation);
    
    var val = document.getElementById(objport).value;
    if (Number(val) >= 1 && Number(val) <= 65535) {
        document.getElementById(objport).style.borderColor="#E1E1E1";
        return true;    
    }
    else{
        //alert("Port number should be 0 < port < 65536!");
        document.getElementById(objport).value = "";
        document.getElementById(objport).style.borderColor="red";
        return false;        
    }

    
}


function optEnDis(lbmethod){
	val = document.getElementById(lbmethod).value;
	
}


// This Javascript code has been replaced by jQuery
function p_pglessthan(opt_sel){
	
	val = document.getElementById(opt_sel).value;
	if (val == "Lessthan"){
		//alert("Less than selected!");
		document.getElementById("p_lessthan").disabled = false;
		document.getElementById("pri_group_val").disabled = false;
	}
	else{
		document.getElementById("p_lessthan").disabled = true;
		document.getElementById("pri_group_val").disabled = true;
	}
}
