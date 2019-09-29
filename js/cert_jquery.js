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
    //document.getElementById(objdns).addEventListener("focusout", dnsValidation);

    document.getElementById(objdns).style.borderColor="#E1E1E1";
    
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

function simpleDnsValidation(objdns){
    // DNS Name Validation
    //document.getElementById(objdns).addEventListener("focusout", dnsValidation);

    document.getElementById(objdns).style.borderColor="#E1E1E1";
    
    var len = document.getElementById(objdns).value.length;
    
    var val = document.getElementById(objdns).value;
    if (/^[a-zA-Z0-9][a-zA-Z0-9-_\.]{1,61}[a-zA-Z0-9](?:\S[a-zA-Z]{2,})+$/.test(val)){
        //alert("Valid Domain Name: " + val);
        return true;
    }
    else if (len > 1 && len < 128) return true;
    else if (len < 1 || len > 127) {
    	document.getElementById(objdns).value = "";
        document.getElementById(objdns).style.borderColor="red";
        //document.getElementById(objdns).focus(); -- Looping issue
        return false;
    }
    return false;
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
    //document.getElementById(objip).addEventListener("focusout", ipValidation);
    document.getElementById(objip).style.borderColor="#E1E1E1";
    
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
    //document.getElementById(objport).addEventListener("focusout", portValidation);
    document.getElementById(objport).style.borderColor="#E1E1E1";
    
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

function loadOptNamesProcessData(response_in, selID) {
	var strResult = '';
	//Remove existing profile types and then add new ones
	$('#' + selID + ' option').each(function(index) {
		if (index != 0) $(this).remove();
	});
	
	$.each(response_in, function(index) {
		if (response_in[index] != "none"){
			if (response_in[index] == "tcp" && selID == 'vs_tcpprofile') strResult += "<option value='" + response_in[index] + "' selected>" + response_in[index] + "</option>";
			else strResult += "<option value='" + response_in[index] + "'>" + response_in[index] + "</option>";
		}
	});
	
	//alert("Return output: " + strResult);
	$('#' + selID).append(strResult);
}

function loadOptNames(ltmIP, loadType, selID){
	var callingUrl = '';
	if (loadType != 'ALL') callingUrl = 'get_profile_names';
	else callingUrl = 'get_pool_monitors';

	ajxOut = $.ajax({
		url: '/content/' + callingUrl + '.php',
		type: 'POST',
		dataType: 'JSON',
		data: {method:callingUrl, DevIP:ltmIP, LoadTypeName:loadType},
		error: function(jqXHR, textStatus, errorThrown){
			alert("Ajax call failed!");
            console.log('jqXHR:');
            console.log(jqXHR);
            console.log('textStatus:');
            console.log(textStatus);
            console.log('errorThrown:');
            console.log(errorThrown);
		}
	});
	ajxOut.done(function (response_in) {
			loadOptNamesProcessData(response_in, selID);
	});
}

//JQueury 
$(function () {
	$('#div_ltmchoice').on('change', function() {
		var nameAndIp = $('#ltmSelBox option:selected').val();
		if (nameAndIp == 'Select...') return;
		
		//$('body').fadeOut();
		
		var arr = nameAndIp.split(":");
		
		//$('body').fadeIn();

	});

    $('#cert_import_btn').on('click', function() {
    	//alert("Cert Import button clicked!");
    	$('#cert_iframe_fieldset').empty();
    	$('#cert_iframe_fieldset').append('<legend>Import Cert/Key Configuration</legend>');
    	$('#cert_iframe_fieldset').append('<iframe src="/content/if_ssl_import.php" scrolling="no" width="700px" height="600" frameborder="0"></iframe>');
    });

    $('#cert_create_btn').on('click', function() {
    	//alert("Cert Create button clicked!");
    	$('#cert_iframe_fieldset').empty();
    	$('#cert_iframe_fieldset').append('<legend>Create Cert/Key Configuration</legend>');
    	$('#cert_iframe_fieldset').append('<iframe src="/content/if_ssl_create.php" scrolling="no" width="700px" height="600" frameborder="0"></iframe>');    	
    });
});