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

//Read the parent URL parameters and return a query parameter value against a given key
//e.g. URL: http://www.example.com/?go=chg_profile
//     GetParentURLParameter('go')
//     Return: chg_profile
function GetParentURLParameter(sParam)
{
   var parentURL = (window.location != window.parent.location)
    ? document.referrer
    : document.location.href;

   var parentQry = parentURL.slice(parentURL.indexOf('?')+1).split('&');
   //alert("Given URL: " + parentQry);
   for (var i = 0; i < parentQry.length; i++)
   {
       var sParameterName = parentQry[i].split('=');
       if (sParameterName[0] == sParam)
       {
           return sParameterName[1];
       }
   }
}

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

// Delete a row by name
function deleteRowByName(tableID, name) {
	var table = document.getElementById(tableID);
	var rowCount = table.rows.length;
	for(var i=1; i<rowCount; i++) {
		var row = table.rows[i];
		var chkbox = row.cells[0].childNodes[0];
		if(null != chkbox && true == chkbox.checked) {
			var col1 = '#dataTable tbody tr:eq(' + i + ') td:eq(1)';
			var rowName = $(col1).children().val();
			if(rowName == name){
				table.deleteRow(i);
				rowCount--;
				i--;
			}
		}
	}
}

// Check if there is checked rows at least one
function hasCheckedRow(tableID) {
	var table = document.getElementById(tableID);
	var rowCount = table.rows.length;
	if (rowCount == 1 && table.rows[1].cells[1].firstChild.value == ""){
		return "false";
	}
	
	var numOfChecked = 0;
	for(var i=1; i<rowCount; i++) {
		var row = table.rows[i];
		var chkbox = row.cells[0].childNodes[0];
		if(null != chkbox && true == chkbox.checked)
			numOfChecked++;
	}
	//alert("Number of checked box: " + numOfChecked);
	if (numOfChecked >= 1) return "true";
	else return "false";
}

// Add a new table row to display content information
function addCertRow(tableID) {
	var table = document.getElementById(tableID);
	var rowCount = table.rows.length;

	var row = table.insertRow(rowCount);
	var colCount = table.rows[1].cells.length;
	for(var i=0; i<colCount; i++) {
		var newcell = row.insertCell(i);
		newcell.innerHTML = table.rows[1].cells[i].innerHTML;
	}
}

//Old Table Row cleanup - Delete existing all rows except first row
function deleteAllRows(tableID) {
	var table = document.getElementById(tableID);
	var rowCount = table.rows.length;
	
	for(var x=rowCount-1; x>1; x--) {
		table.deleteRow(x);
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

// Process certs and keys data returned from BIG-IP
// response_in array index starts from 1
function loadCertkeyProcess(response_in){
	//'name':'', 'commonName':'', 'expiration':'', 'partition':''
	var numOfCerts = Object.keys(response_in).length;
	
	if (numOfCerts == 0) { alert("No certs exist"); return; }
	$.each(response_in, function(index){
		var col1 = '#dataTable tbody tr:eq(' + index + ') td:eq(1)';
		var col2 = '#dataTable tbody tr:eq(' + index + ') td:eq(2)';
		var col3 = '#dataTable tbody tr:eq(' + index + ') td:eq(3)';
		var col4 = '#dataTable tbody tr:eq(' + index + ') td:eq(4)';

		// Cert name is retrieved without extension (.crt)
		//$(col1).children().val((response_in[index].name).split('.')[0]); <= Issue with cert/key names including dot('.')
		var strSz = (response_in[index].name).length;
		// Remove last 4 characters which is ".crt"
		$(col1).children().val((response_in[index].name).substr(0,strSz - 4));
		$(col2).children().val(response_in[index].commonName);
		$(col3).children().val(response_in[index].expiration);
		$(col4).children().val(response_in[index].partition);

		if(numOfCerts.toString() != index ) addCertRow('dataTable');
		//alert('Name: ' + response_in[index].name + ' CN: ' + response_in[index].commonName + ' Expiration: ' + response_in[index].expiration + ' Partition: ' + response_in[index].partition + '\n');
	});
	
}

// Process the result data of deleting certs and keys from BIG-IP
function delCertkeyProcess(response_in){
	//'name':'', 'result':'', 'message':''
	var numOfCerts = Object.keys(response_in).length;
	var strResult = '';
	
	$.each(response_in, function(index){
		if (response_in[index].result == "SUCCESS"){
			strResult += "<b>" + response_in[index].name + " has been deleted successfully</b><br>";
			strResult += response_in[index].message + "<br>";
			deleteRowByName('dataTable', response_in[index].name);
		}
		else{
			strResult += "<b>" + response_in[index].name + " deletion has failed</b><br>";
			strResult += response_in[index].message + "<br>";			
		}
	});
	
	$('#delCert_EvalReview').append(strResult);
	
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
		if (nameAndIp == 'Select...'){
			// Reset all fields
			deleteAllRows('dataTable');
			
			$('#dataTable tbody tr:eq(1) td:eq(1)').children().val("");
			$('#dataTable tbody tr:eq(1) td:eq(2)').children().val("");
			$('#dataTable tbody tr:eq(1) td:eq(3)').children().val("");
			$('#dataTable tbody tr:eq(1) td:eq(4)').children().val("");
			return;
		}
		
		var arr = nameAndIp.split(":");
		
		// Only for deleting cert and key
		if(GetParentURLParameter('go') == 'del_cert'){
			// Load Certs and Keys from a given BIG-IP
			var paramData = {'PhpFileName':'load_certkey_ajax', 'DevIP':''};
			paramData['DevIP'] = arr[1];
			ajxOut = $.ajax({
				url: '/content/load_certkey_ajax.php',
				type: 'POST',
				dataType: 'JSON',
				data: {'jsonData' : JSON.stringify(paramData)},
				error: function(jqXHR, textStatus, errorThrown){
					alert("Ajax call to load certs and keys has failed!");
		            console.log('jqXHR:');
		            console.log(jqXHR);
		            console.log('textStatus:');
		            console.log(textStatus);
		            console.log('errorThrown:');
		            console.log(errorThrown);
				}
			});
			ajxOut.done(loadCertkeyProcess);
		}
	});

    $('#cert_import_btn').on('click', function() {
    	//alert("Cert Import button clicked!");
    	$('#cert_iframe_fieldset').empty();
    	$('#cert_iframe_fieldset').append('<legend>Import Cert/Key Configuration</legend>');
    	//$('#cert_iframe_fieldset').append('<iframe src="/content/if_ssl_import.php" scrolling="no" width="700px" height="600" frameborder="0"></iframe>');
    	$('#cert_iframe_fieldset').append('<iframe src="/content/if_ssl_import.php" scrolling="no" width="1050px" height="75%" frameborder="0"></iframe>');
    });

    $('#cert_create_btn').on('click', function() {
    	//alert("Cert Create button clicked!");
    	$('#cert_iframe_fieldset').empty();
    	$('#cert_iframe_fieldset').append('<legend>Create Cert/Key Configuration</legend>');
    	//$('#cert_iframe_fieldset').append('<iframe src="/content/if_ssl_create.php" scrolling="no" width="700px" height="600" frameborder="0"></iframe>');    	
    	$('#cert_iframe_fieldset').append('<iframe src="/content/if_ssl_create.php" scrolling="yes" width="1050px" height="75%" frameborder="0"></iframe>');
    });
    
    // Event handler when 'Delete Cert/Key" button is clicked
    $('#btn_delCertkey').on('click', function(){
    	if (hasCheckedRow('dataTable') == 'false') {
    		alert("Please select a cert/certs to delete");
    		return;
    	}
    	//else alert("Moving forward");
    	
    	var nameAndIp = $('#ltmSelBox option:selected').val();
    	var arr = nameAndIp.split(":");
    	
    	var paramData = {'PhpFileName':'del_certkey_ajax', 'DevIP':arr[1]};
    	// certData - Array data of {name1, cn1, exp1, part1, name2, cn2, exp2, part2, ... }
    	var certData = [];
    	
    	var table = document.getElementById('dataTable');
    	var rowCount = table.rows.length;
    	
    	// Selected cert data collection
    	for(var i=1;i<rowCount;i++){
    		var row = table.rows[i];
    		var chkbox = row.cells[0].childNodes[0];
    		if(null != chkbox && true == chkbox.checked) {
    			for(colIdx=1;colIdx<=4;colIdx++){
	    			var col1 = '#dataTable tbody tr:eq(' + i + ') td:eq(' + colIdx + ')';
	    			certData.push($(col1).children().val())
    			}
    		}
    	}
    	
    	// Call ajax to pass the chosen cert info to BIG-IP and delete them from BIG-IP
		ajxOut = $.ajax({
			url: '/content/del_certkey_ajax.php',
			type: 'POST',
			dataType: 'JSON',
			data: {'jsonData' : JSON.stringify(paramData), 'certData': JSON.stringify(certData)},
			error: function(jqXHR, textStatus, errorThrown){
				alert("Ajax call to delete certs and keys has failed!");
	            console.log('jqXHR:');
	            console.log(jqXHR);
	            console.log('textStatus:');
	            console.log(textStatus);
	            console.log('errorThrown:');
	            console.log(errorThrown);
			}
		});
		ajxOut.done(delCertkeyProcess);
    	
    });
});