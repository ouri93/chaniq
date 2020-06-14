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
			//newcell.innerHTML = table.rows[0].cells[i].innerHTML;
			/*
			if (GetParentURLParameter('go') == 'chg_pool' && (1<= i <= 3)){
				strHtml = (table.rows[1].cells[i].innerHTML).replace('disabled', 'enabled');
				newcell.innerHTML = strHtml;
			}
			else
				newcell.innerHTML = table.rows[1].cells[i].innerHTML;
			*/
			newcell.innerHTML = table.rows[1].cells[i].innerHTML;
		}
	}else{
		 alert("Maximum number of pool members are 10.");
			   
	}
}

function addNewPoolMemberRow(tableID){
	var table = document.getElementById(tableID);
	var rowCount = table.rows.length;
	if(rowCount < 10){							// limit the user from creating fields more than your limits
		var row = table.insertRow(rowCount);
		var colCount = table.rows[0].cells.length;
		for(var i=0; i<colCount; i++) {
			var newcell = row.insertCell(i);
			if( 1 <= i <=3 ){
				strHtml = (table.rows[rowCount].cells[i].innerHTML).replace('disabled', 'enabled');
				newcell.innerHTML = strHtml;
			}
			else
				newcell.innerHTML = table.rows[rowCount].cells[i].innerHTML;
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
			//if(rowCount <= 1) { 						// limit the user from removing all row
			if(rowCount <= 2) { 						// limit the user from removing all rows and Header
				alert("Cannot Remove all pool members.");
				break;
			}
			table.deleteRow(i);
			rowCount--;
			i--;
		}
	}
}

// Old Table Row cleanup - Delete existing all rows except first row
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

function iterAssArray(assArray){
	var allKeyVal = '< Associate Array Key-Value List >\n\n';
	$.each(assArray, function(key, value) {
		allKeyVal += key + ":" + value + "\n";
	});
	return allKeyVal;
}

function iterArray(aArray){
	var allVals = '< Array Value List >\n\n';
	$.each(aArray, function(index) {
		allVals += aArray[index] + "\n";
	});
	return allVals;
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

function loadObjNames(ltmIP, objType, selID){
	var callingUrl = '';
	//alert("loadObjNames called - selID: " + selID + " objType: " + objType);
	callingUrl = 'get_ltmobj_names';
	
	ajxOut = $.ajax({
		url: '/content/' + callingUrl + '.php',
		type: 'POST',
		dataType: 'JSON',
		data: {method:callingUrl, DevIP:ltmIP, LoadTypeName:objType},
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
			loadObjNamesProcessData(response_in, selID);
	});
}

function loadObjNamesProcessData(response_in, selID) {
	var strResult = '';
	//alert("loadObjNameProcessData called - selID: " + selID);
	//Remove existing profile types and then add new ones
	$('#' + selID + ' option').each(function(index) {
		if (index != 0) $(this).remove();
	});
	
	$.each(response_in, function(index) {
		if (response_in[index] != "none"){
			strResult += "<option value='" + response_in[index] + "'>" + response_in[index] + "</option>";
		}
	});
	
	//alert("Return output: " + strResult);
	$('#' + selID).append(strResult);
}

// Function to process Pool configuration data returned by Ajax call
function poolConfigProcessData(response_in) {
	// pool_name|pool_partition|pool_monitor|pool_LB|pool_lessthan@pm_name|pm_ip|pm_port|pm_ratio|pm_mon|pm_pri_group@pm_name|pm_ip|pm_port|pm_ratio|pm_mon|pm_pri_group...
	var responseArray = response_in.split('@');
	var strResult = "<b>" + 'Debugging for loading Pool configuration' + "</b><br>";

	//alert ("Length of array: " + responseArray.length);
	var numOfPoolMembers = responseArray.length - 1;

	strResult += "Pool configuration: " + responseArray[0] + "<br>";

	var pPrpt = responseArray[0].split('|');
	
	if (numOfPoolMembers != 0){
		var pmSettings = new Array(numOfPoolMembers);
		for (i=0; i<numOfPoolMembers;i++){
			pmSettings[i] = responseArray[i+1].split("|");
			//alert(iterArray(pmSettings[i]));
			strResult += (i+1) + "th Pool member configuration: " + pmSettings[i] + "<br>";	
		} 
		
	}				
			
	// Update Pool properties
	// Pool ID: chg_p_name_select, partition, p_mon, p_lbmethod, p_prigroup, p_lessthan
	$('#p_mon option[value="' + pPrpt[2] + '"]').prop('selected', true);
	//$('#p_mon option[value="https"]').prop('selected', 'selected');
	//$('#p_mon').val(pPrpt[2]);
	$('#p_lbmethod option[value="' + pPrpt[3] + '"]').prop('selected', 'selected');
	if ( pPrpt[4] == '0' ) $('#p_prigroup option[value="disabled"]').prop('selected', 'selected');
	else $('#p_prigroup option[value="Lessthan"]').prop('selected', 'selected');
	$('#p_lessthan').val(pPrpt[4]);

	// Update pool members properties
	// Pool Member ID: pool_membername, pool_memberip, pool_memberport, pool_memberratio, pm_mon, pri_group_val
	
	// By default, there is one pool member row
	if (numOfPoolMembers >= 1){
		// Delete all existing rows except the first row and reset the first row
		deleteAllRows('dataTable');
		
		// Disable pool member properties - Pool member name, IP and port
		$('#dataTable tbody tr:eq(1) td:eq(1)').children().prop("disabled", true);
		$('#dataTable tbody tr:eq(1) td:eq(2)').children().prop("disabled", true);
		$('#dataTable tbody tr:eq(1) td:eq(3)').children().prop("disabled", true);

		for (rowIndex=1;rowIndex<numOfPoolMembers;rowIndex++){
			addRow('dataTable');
		}
		for(rowIndex=1;rowIndex<=numOfPoolMembers;rowIndex++){
			//alert("Number of row: " + $('#dataTable tbody tr').length + "\nNumber of col: " + $('#dataTable tbody td').length );
			var pm_prpt = responseArray[rowIndex].split('|');
			
			//var a = $('#dataTable tbody tr:eq(1) td:eq(1)').children().each(function() { alert($(this).val('name1')); });
			// Update cell fields of Pool members table by using index
			$('#dataTable tbody tr:eq(' + rowIndex + ') td:eq(1)').children().val(pm_prpt[0]);
			$('#dataTable tbody tr:eq(' + rowIndex + ') td:eq(2)').children().val(pm_prpt[1]);
			$('#dataTable tbody tr:eq(' + rowIndex + ') td:eq(3)').children().val(pm_prpt[2]);
			$('#dataTable tbody tr:eq(' + rowIndex + ') td:eq(4)').children().val(pm_prpt[3]);
			if (pm_prpt[4] != 'default')
				$('#dataTable tbody tr:eq(' + rowIndex + ') td:eq(5)').children().val(pm_prpt[4]);
			else
				$('#dataTable tbody tr:eq(' + rowIndex + ') td:eq(5)').children().val('inherit');
			$('#dataTable tbody tr:eq(' + rowIndex + ') td:eq(6)').children().val(pm_prpt[5]);
			
		}
	}
	// No pool memebrs - Reset all fileds of the first row and allow Pool name, IP, and port configuration
	else{
		deleteAllRows('dataTable');

		// Set the first row fields with default value and allow pool member properties
		$('#dataTable tbody tr:eq(1) td:eq(1)').children().val("");
		$('#dataTable tbody tr:eq(1) td:eq(1)').children().prop("disabled", false);
		$('#dataTable tbody tr:eq(1) td:eq(2)').children().val("");
		$('#dataTable tbody tr:eq(1) td:eq(2)').children().prop("disabled", false);
		$('#dataTable tbody tr:eq(1) td:eq(3)').children().val("");
		$('#dataTable tbody tr:eq(1) td:eq(3)').children().prop("disabled", false);
		$('#dataTable tbody tr:eq(1) td:eq(4)').children().val("1");
		$('#dataTable tbody tr:eq(1) td:eq(5)').children().val("inherit");
		$('#dataTable tbody tr:eq(1) td:eq(6)').children().val("0");
	}
	
	//strResult += responseArray[0] + "  " + responseArray[1] + "  " + responseArray[2]; 
/*
	$.each(response_in, function(index) {
		if(index == 0) 
			strResult = "<b>" + response_in[index] + "</b><br>";
		else
			strResult += response_in[index] + "<br>";
	});
*/	
	$('#newPool_EvalReview').html(strResult);	
}

// Display Pool modification result returned from Python
function showPoolChangeResult(response_in){
	var strResult = '';
	
	$.each(response_in, function(index) {
		if(index == 0) 
			strResult = "<b>" + response_in[index] + "</b><br>";
		else
			strResult += response_in[index] + "<br>";
	});
	
	$('#newPool_EvalReview').append(strResult);
	
}

//Display Pool deletion result returned from BIG-IP
function poolDeleteProcessData(response_in){
	var strResult = '';
	
	$.each(response_in, function(index) {
		if(index == 0) 
			strResult = "<b>" + response_in[index] + "</b><br>";
		else
			strResult += response_in[index] + "<br>";
	});
	
	$('#newPool_EvalReview').append(strResult);
	
}

function isMinNumOfPoolMbr(){
	minPoolMbr = parseInt($('#vs_poolmbrnum option:selected').val());
	if (minPoolMbr > 0) return true;
	else return false;
}

function isValidInputs(){
	if (dnsValidation('vs_dnsname') && ipValidation('vs_dest') && portValidation('vs_port') && dnsValidation('vs_poolname') && isMinNumOfPoolMbr())
		return true;
	else return false;
}

/* 
 * Javascript for moving items between two list boxes
 */
/*
 * Original example found here: http://www.jquerybyexample.net/2012/05/how-to-move-items-between-listbox-using.html
 * Modified by Esau Silva to support 'Move ALL items to left/right' and add better stylingon on Jan 28, 2016.
 * 
 */

function getPoolMonAjax(phpFileName, bigipName, bigipIP, monType) {
  	return $.ajax({
  		url: 'content/get_pool_monitors.php',
   		type: 'POST',
   		data: {method: phpFileName, DevName: bigipName, DevIP: bigipIP, LoadTypeName: monType}
   	});
}

function PprocessData(response_in)
{
	/*
   	var response = JSON.parse(response_in);
   	alert("Pool Monitor ProcessData" + response[0]);
	
	$.each(response, function(index){
   		$('#p_mon').append('<option value=' + response[index] + ' text=' + response[index] + '>' + response[index] + '</option>');
   	});	
	*/
	var strResult = '';
	
	//Remove existing monitors and then add new ones
	$('#p_mon option').each(function(index) {
		if (index != 0) $(this).remove();
	});
	
	$.each(response_in, function(index) {
		if (response_in[index] != "none"){
			strResult += "<option value='" + response_in[index] + "'>" + response_in[index] + "</option>";
		}
	});
	
	//alert("Return output: " + strResult);
	$('#p_mon').append(strResult);
	
   	
}

function PMprocessData(response_in)
{
	/*
   	var response = JSON.parse(response_in);
   	alert("Pool Member monitor ProcessData" + response[0]);

   	$.each(response, function(index){
   		$('#pm_mon').append('<option value=' + response[index] + ' text=' + response[index] + '>' + response[index] + '</option>');
   	});
   	*/
	var strResult = '';
	
	//Remove existing pool member monitors and then add new ones
	$('#pm_mon option').each(function(index) {
		if (index != 0) $(this).remove();
	});
	
	$.each(response_in, function(index) {
		if (response_in[index] != "none"){
			strResult += "<option value='" + response_in[index] + "'>" + response_in[index] + "</option>";
		}
	});
	
	//alert("Return output: " + strResult);
	$('#pm_mon').append(strResult);
}

function MonProcessData(response_in)
{
   	var response = JSON.parse(response_in);
   	//alert("In ProcessData" + response[0]);

   	// Empty the existing options from the dropdown, then populate new options
   	$('#m_type_parent').empty();
   	$('#m_type_parent').append('<option selected="selected" value="Select..." > Select... </option>');
   	$.each(response, function(index){
		$('#m_type_parent').append('<option value=' + response[index] + ' text=' + response[index] + '>' + response[index] + '</option>');
   	});
}

function MonSettingsProcessData(response_in)
{
	//alert("Print Return data:  Interval: " + response_in['interval']);
	//alert("Print Return data:  send: " + response_in['send']);
	var monType = $('#m_type').val();
	setMonHtml(monType, response_in);
}

function getMonSettingsAjax(phpFileName, bigipName, bigipIP, monType, parMonType)
{
	//alert("getMonSettingsAjax - phpFileName: " + phpFileName + " Dev name: " + bigipName + " Dev IP: " + bigipIP + " Mon Type: " + monType + " Parent Monitor: " + parMonType);
	return $.ajax({ 
		url: 'content/get_healthmon_settings.php',
		type: 'POST',
		dataType: 'JSON',
		data: {phpFile: phpFileName, DevIP:bigipIP, MonType: monType, ParMonType:parMonType},
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
}

function buildNewPoolAjax(phpFileName, arr, pVsName, pVsPort, pMon, pEnv, pLBMethod, pPriGroup, pPriGroupLessThan, pmPoolMemberName, pmPoolMemberIp, pmPoolMemberPort, pmPoolMemberRatio, pmPoolMemberMon, pmPriGroup)
{

	//alert(arr[1] + ":"+ pVsName + ":"+ pVsPort + ":"+ pMon + ":"+ pEnv + ":" + pLBMethod + ":"+ pPriGroup + ":"+ pPriGroupLessThan + ":" + pmPoolMemberName + ":"+ pmPoolMemberIp +":" + pmPoolMemberPort + ":" + pmPoolMemberMon + ":" + pmPriGroup);
  	return $.ajax({
  		url: '/content/new_pool_build.php',
   		type: 'POST',
   		dataType: 'JSON',
   		data: {phpFile: phpFileName, DevIP: arr[1], PVsName: pVsName, PVsPort: pVsPort, PMon: pMon, PEnv: pEnv, PLBMethod: pLBMethod, PPriGroup: pPriGroup, PPriGroupLessThan: pPriGroupLessThan, PmPoolMemberNmae: pmPoolMemberName, PmPoolMemberIp: pmPoolMemberIp, PmPoolMemberPort: pmPoolMemberPort, PmPoolMemberRatio: pmPoolMemberRatio, PmPoolMemberMon: pmPoolMemberMon, PmPrigroup: pmPriGroup }
   		//data: {phpFile: phpFileName, DevIP: arr[1], PVsName: pVsName, PVsPort: pVsPort, PMon: pMon, PEnv: pEnv, PLBMethod: pLBMethod }
   	});
}

function poolBuildProcessData(response_in)
{
	//alert("poolBuildProcessData called!");
	
	var strResult = '';
	$.each(response_in, function(index) {
		strResult += response_in[index] + "<br>";
	});
	
	$('#newPool_EvalReview').html(strResult);
	
} 

function prfPoolNameProcessData(response_in) {
	var strResult = '';
	//Remove existing profile types and then add new ones
	if (GetParentURLParameter('go') == 'chg_pool'){
		$('#chg_p_name_select option').each(function(index) {
			if (index != 0) $(this).remove();
		});
	}
	else if (GetParentURLParameter('go') == 'del_pool'){
		$('#del_p_name_select option').each(function(index) {
			if (index != 0) $(this).remove();
		});
	}
	
	$.each(response_in, function(index) {
		if (response_in[index] != "none"){
			strResult += "<option value='" + response_in[index] + "'>" + response_in[index] + "</option>";
		}
	});
	
	//alert("Return output: " + strResult);
	
	if (GetParentURLParameter('go') == 'chg_pool')
		$('#chg_p_name_select').append(strResult);
	else if (GetParentURLParameter('go') == 'del_pool')
		$('#del_p_name_select').append(strResult);
}

//Retrieve partition names from a given BIG-IP
function loadPartitionNames(ltmIP, selID){
	
	var paramData = {'phpFileName':'get_partition_names', 'DevIP':'' };
	
	paramData['DevIP'] = ltmIP;

	ajxOut = $.ajax({
		url: '/content/get_partition_names.php',
		type: 'POST',
		dataType: 'JSON',
		data: {'jsonData' : JSON.stringify(paramData)},
		error: function(jqXHR, textStatus, errorThrown){
			alert("Ajax call to retrieve Partition names (loadPartitionNames) has failed!");
            console.log('jqXHR:');
            console.log(jqXHR);
            console.log('textStatus:');
            console.log(textStatus);
            console.log('errorThrown:');
            console.log(errorThrown);
		}
	});
	ajxOut.done(function (response_in) {
		var strResult = '';
		//Reset all options and rebuild default option values
		$('#' + selID + ' option').each(function(index) {
			$(this).remove();
		});
		$('#' + selID).append("<option value='select' selected='selected'>Select...</option><option value='Common' >Common</option>");

		$('#del_p_name_select option').each(function(index) {
			$(this).remove();
		});
		$('#del_p_name_select').append("<option value='none' selected='selected'>None</option>");

		
		//var partNames = "Part2:Part3:".split(":");
		var partNames = response_in.split(":");
		
		// Empty array - Return 1
		var numOfPart = partNames.length; 
		if (numOfPart <= 1) return;
		else{
			var i=0;
			for (;i < numOfPart-1;i++){
				strResult += "<option value='" + partNames[i] + "'>" + partNames[i] + "</option>";
			}
			
			$('#' + selID).append(strResult);	
		}
		//alert("Return output: " + strResult);
		
	});
}

//JQueury 
$(function () {
	$('#div_ltmchoice').on('change', function() {
		var nameAndIp = $('#ltmSelBox option:selected').val();
		if (nameAndIp == 'Select...') return;
		
		//$('body').fadeOut();
		
		var arr = nameAndIp.split(":");
		
		if (GetParentURLParameter('go') == 'del_pool'){
			loadPartitionNames(arr[1], 'partition_name_select');
		}
		//if (GetParentURLParameter('go') == 'new_pool' | GetParentURLParameter('go') == 'chg_pool'){
		else {
			// Call Ajax to retrieve pool names from a given LTM
			ajxOut = $.ajax({
				url: '/content/get_pool_names.php',
				type: 'POST',
				dataType: 'JSON',
				data: {method:'get_pool_names', DevIP:arr[1], Partition:'Common'},
				error: function(jqXHR, textStatus, errorThrown){
					alert("Ajax call for retrieving pool names has failed!");
		            console.log('jqXHR:');
		            console.log(jqXHR);
		            console.log('textStatus:');
		            console.log(textStatus);
		            console.log('errorThrown:');
		            console.log(errorThrown);
				}
			});
			ajxOut.done(prfPoolNameProcessData);
	
	    	// Call Ajax to get all available Pool monitors from the device
	    	ajaxOut = $.ajax({
	    		url: '/content/get_pool_monitors.php',
	    		type: 'POST',
	    		dataType: 'JSON',
	    		data: {method: 'get_pool_monitors', DevIP: arr[1], LoadTypeName:'ALL'},
				error: function(jqXHR, textStatus, errorThrown){
					alert("Ajax call for Pool monitor retrieval has failed!");
		            console.log('jqXHR:');
		            console.log(jqXHR);
		            console.log('textStatus:');
		            console.log(textStatus);
		            console.log('errorThrown:');
		            console.log(errorThrown);
				}
	    	});
	    	//ajaxOut = getPoolMonAjax("get_pool_monitors", arr[0], arr[1], "ALL");
	    	ajaxOut.done(PprocessData);
	    	$('#pm_mon').trigger('click');
	    	
	    	
	    	// Call Ajax to get all available Pool monitors from the device
	    	//ajaxOut = getPoolMonAjax("get_pool_monitors", arr[0], arr[1], "ALL");
	    	ajaxOut = $.ajax({
	    		url: '/content/get_pool_monitors.php',
	    		type: 'POST',
	    		dataType: 'JSON',
	    		data: {method: 'get_pool_monitors', DevIP: arr[1], LoadTypeName:'ALL'},
				error: function(jqXHR, textStatus, errorThrown){
					alert("Ajax call for Pool Member monitor retrieval has failed!");
		            console.log('jqXHR:');
		            console.log(jqXHR);
		            console.log('textStatus:');
		            console.log(textStatus);
		            console.log('errorThrown:');
		            console.log(errorThrown);
				}
	    	});    	
	    	ajaxOut.done(PMprocessData);
	    	//$('#pm_td').off('click');
		}

	});

    /* Ajax Ref: https://www.youtube.com/watch?v=G9jz9mdblgs 
     * if you specify change() event, it won't fire as there is no option value initially.
     * Here we use .one() method which guarantee to be executed only once with the specified event.
     * Once Pool monitors are gathered from BIG-IP, add them to select and 
     * call Pool member monitor click event to add them there.
     * */
/*	
    $('#p_mon').one('click', function() {
    	//alert("Select has been changed");
    	var bigipNameAndIP = $('#ltmSelBox').val()
    	// arr[0] - BIG-IP Device Name, arr[1] - BIG-IP Device IP address
    	var arr = bigipNameAndIP.split(":");
    	
    	// Call Ajax to get all available Pool monitors from the device
    	ajaxOut = $.ajax({
    		url: '/content/get_pool_monitors.php',
    		type: 'POST',
    		dataType: 'JSON',
    		data: {method: 'get_pool_monitors', DevIP: arr[1], LoadTypeName:'ALL'},
			error: function(jqXHR, textStatus, errorThrown){
				alert("Ajax call for Pool monitor retrieval has failed!");
	            console.log('jqXHR:');
	            console.log(jqXHR);
	            console.log('textStatus:');
	            console.log(textStatus);
	            console.log('errorThrown:');
	            console.log(errorThrown);
			}
    	});
    	//ajaxOut = getPoolMonAjax("get_pool_monitors", arr[0], arr[1], "ALL");
    	ajaxOut.done(PprocessData);
    	$('#pm_mon').trigger('click');

    });
*/    
/*
    $('#pm_mon').one('click', function() {
    //$('#pm_td').on('click', 'select', function() {
    	//alert("Select has been changed");
    	var bigipNameAndIP = $('#ltmSelBox').val();
    	// arr[0] - BIG-IP Device Name, arr[1] - BIG-IP Device IP address
    	var arr = bigipNameAndIP.split(":");
    	
    	// Call Ajax to get all available Pool monitors from the device
    	//ajaxOut = getPoolMonAjax("get_pool_monitors", arr[0], arr[1], "ALL");
    	ajaxOut = $.ajax({
    		url: '/content/get_pool_monitors.php',
    		type: 'POST',
    		dataType: 'JSON',
    		data: {method: 'get_pool_monitors', DevIP: arr[1], LoadTypeName:'ALL'},
			error: function(jqXHR, textStatus, errorThrown){
				alert("Ajax call for Pool Member monitor retrieval has failed!");
	            console.log('jqXHR:');
	            console.log(jqXHR);
	            console.log('textStatus:');
	            console.log(textStatus);
	            console.log('errorThrown:');
	            console.log(errorThrown);
			}
    	});    	
    	ajaxOut.done(PMprocessData);
    	//$('#pm_td').off('click');

    });
*/
    $('#p_prigroup').change(function() {
    	var priGroupChoice = $('#p_prigroup').val();
    	//alert("priGroupChoice: " + priGroupChoice);
    	if (priGroupChoice == "Lessthan"){
    		//alert("Less than selected!");
    		$('#p_lessthan').attr("disabled", false);
    		$('#pri_group_val').attr("disabled", false);
    	}
    	else{
    		$('#p_lessthan').attr("disabled", true);
    		$('#pri_group_val').attr("disabled", true);
    		$('#p_lessthan').val("0");
    		$('#pri_group_val').val("0");
    	}
    });	

    // Add new pool member with Deploy Deply Pool mode
    $('#add_new_pm').on('click', function() {
    	var table = document.getElementById('dataTable');
    	var rowCount = table.rows.length;
    	if(rowCount < 10){							// limit the user from creating fields more than your limits
    		var row = table.insertRow(rowCount);
    		var colCount = table.rows[0].cells.length;
    		for(var i=0; i<colCount; i++) {
    			var newcell = row.insertCell(i);
    			newcell.innerHTML = table.rows[1].cells[i].innerHTML;
    		}
    	}else{
    		 alert("Maximum number of pool members are 10.");
    			   
    	}    	
    });
    
    // Add new pool members with Change pool mode
    $('#add_editable_new_pm').on('click', function() {
    	var table = document.getElementById('dataTable');
    	var rowCount = table.rows.length;
    	if(rowCount < 10){							// limit the user from creating fields more than your limits
    		var row = table.insertRow(rowCount);
    		var colCount = table.rows[0].cells.length;
    		for(var i=0; i<colCount; i++) {
    			var newcell = row.insertCell(i);
    			if( 1 <= i <=3 ){
    				strHtml = (table.rows[1].cells[i].innerHTML).replace('disabled', 'enabled');
    				newcell.innerHTML = strHtml;
    			}
    			else
    				newcell.innerHTML = table.rows[1].cells[i].innerHTML;
    		}
    	}else{
    		 alert("Maximum number of pool members are 10.");
    			   
    	}
    });
    
    // Async jQuery for new Pool building
    $('#btn_newPoolBuild').on('click', function() {
    	var bigipNameAndIP = $('#ltmSelBox').val()
    	var arr = bigipNameAndIP.split(":");
    	var pVsName = $('#p_vs_name').val();
    	var pVsPort = $('#p_vs_port').val();
    	var pMon = $('#p_mon').val();
    	var pEnv = $('#p_env').val();
    	var pLBMethod = $('#p_lbmethod').val();
    	var pPriGroup = $('#p_prigroup').val();
    	var pPriGroupLessThan = "0";
    	if (pPriGroup != "disabled") {
    		pPriGroupLessThan = $('#p_lessthan').val();
    	}
    	
    	// Collect pool member data
    	var table = document.getElementById('dataTable');
    	var rowCount = table.rows.length;
    	var colCount = table.rows[0].cells.length;

    	var pmPoolMemberName = document.getElementsByClassName('pool_membername');
    	var pmPoolMemberIp = document.getElementsByClassName('pool_memberip');
    	var pmPoolMemberPort = document.getElementsByClassName('pool_memberport');
    	var pmPoolMemberRatio = document.getElementsByClassName('pool_memberratio');
    	var pmPoolMemberMon = document.getElementsByClassName('pm_mon');
    	var pmPriGroup = document.getElementsByClassName('pm_pg_val');
    	
    	var arrayLen = pmPoolMemberName.length;
    	
    	// Build parameter data format for array type - e.g. pool_membername is the string array. Change the array to a single string using ":" as a delimiter.
    	// Array = [srv1.xyz.com, srv2.xyz.com, srv3.xyz.com] => "srv1.xyz.com:srv2.xyz.com:srv3.xyz.com"
    	
    	//alert("Array Length: " + arrayLen);
    	var strPmPoolMemberName = '';
    	var strPmPoolMemberIp = '';
    	var strPmPoolMemberPort = '';
    	var strPmPoolMemberRatio = '';
    	var strPmPoolMemberMon = '';
    	var strPmPriGroup = '';
    	
    	for(i=0;i<arrayLen;i++){
    		strPmPoolMemberName += pmPoolMemberName[i].value + ":";
    		strPmPoolMemberIp += pmPoolMemberIp[i].value + ":";
    		strPmPoolMemberPort += pmPoolMemberPort[i].value + ":";
    		strPmPoolMemberRatio += pmPoolMemberRatio[i].value + ":";
    		strPmPoolMemberMon += pmPoolMemberMon[i].value + ":";
    		strPmPriGroup += pmPriGroup[i].value + ":";
    	}
    	//alert(bigipNameAndIP + ":" + arr[1] + ":"+ pVsName + ":"+ pVsPort + ":"+ pMon + ":"+ pEnv + ":" + pLBMethod + ":"+ pPriGroup + ":"+ pPriGroupLessThan + ":" + strPmPoolMemberName + ":" + strPmPoolMemberIp + ":" + strPmPoolMemberPort + ":" + strPmPoolMemberMon + ":" + strPmPriGroup);

    	ajaxOut = buildNewPoolAjax('new_pool_build', arr, pVsName, pVsPort, pMon, pEnv, pLBMethod, pPriGroup, pPriGroupLessThan, strPmPoolMemberName, strPmPoolMemberIp, strPmPoolMemberPort, strPmPoolMemberRatio, strPmPoolMemberMon, strPmPriGroup);
    	ajaxOut.done(poolBuildProcessData);
    	
    });
    
    // In Pool Change mode - Handling Pool name change event
    $('#chg_p_name_select').on('change', function(){
    	var bigipNameAndIP = $('#ltmSelBox').val()
    	var arr = bigipNameAndIP.split(":");
    	var pName = $('#chg_p_name_select').val();
    	
    	if (pName == 'none') return;
    	
    	var poolData = {'PhpFileName':'', 'DevIP':'', 'PoolName':'', 'Partition':''};
    	
    	poolData['PhpFileName'] = 'get_pool_config';
    	poolData['DevIP'] = arr[1];
    	poolData['PoolName'] = pName;
    	poolData['Partition'] = 'Common';
    	
		// Ajax call to retrieve pool configuration from BIG-IP
		ajxOut = $.ajax({
			url: '/content/get_pool_config.php',
			type: 'POST',
			dataType: 'JSON',
			data: {'jsonPoolData' : JSON.stringify(poolData)},
			error: function(jqXHR, textStatus, errorThrown){
				alert("Ajax call for retrieving pool configuration has failed!");
	            console.log('jqXHR:');
	            console.log(jqXHR);
	            console.log('textStatus:');
	            console.log(textStatus);
	            console.log('errorThrown:');
	            console.log(errorThrown);
			}
		});
		ajxOut.done(poolConfigProcessData);
    });
    
    // Update modified pool configuration
	$('#btn_chgPoolConfig').on('click', function(){
    	var bigipNameAndIP = $('#ltmSelBox').val()
    	var arr = bigipNameAndIP.split(":");
    	var pName = $('#chg_p_name_select').val();
    	var pPart = 'Common';
    	//var pPort = $('#p_vs_port').val();
    	var pMon = $('#p_mon').val();
    	//var pEnv = $('#p_env').val();
    	var pLBMethod = $('#p_lbmethod').val();
    	var pPriGroup = $('#p_prigroup').val();
    	var pPriGroupLessThan = '0';
    	if (pPriGroup != "disabled") {
    		pPriGroupLessThan = $('#p_lessthan').val();
    	}
    	
    	// Collect pool member data
    	var table = document.getElementById('dataTable');
    	var rowCount = table.rows.length;
    	var colCount = table.rows[0].cells.length;

    	var pmPoolMemberName = document.getElementsByClassName('pool_membername');
    	var pmPoolMemberIp = document.getElementsByClassName('pool_memberip');
    	var pmPoolMemberPort = document.getElementsByClassName('pool_memberport');
    	var pmPoolMemberRatio = document.getElementsByClassName('pool_memberratio');
    	var pmPoolMemberMon = document.getElementsByClassName('pm_mon');
    	var pmPriGroup = document.getElementsByClassName('pm_pg_val');
    	
    	var arrayLen = pmPoolMemberName.length;
    	
    	// Build parameter data format for array type - e.g. pool_membername is the string array. Change the array to a single string using ":" as a delimiter.
    	// Array = [srv1.xyz.com, srv2.xyz.com, srv3.xyz.com] => "srv1.xyz.com:srv2.xyz.com:srv3.xyz.com"
    	
    	//alert("Array Length: " + arrayLen);
    	var strPmPoolMemberName = '';
    	var strPmPoolMemberIp = '';
    	//var strPmPoolMemberPort = '';
    	var strPmPoolMemberRatio = '';
    	var strPmPoolMemberMon = '';
    	var strPmPriGroup = '';
    	
    	for(i=0;i<arrayLen;i++){
    		// pool member name format should be 'poolmember_name:port'
    		strPmPoolMemberName += pmPoolMemberName[i].value + ":" + pmPoolMemberPort[i].value + "|";
    		strPmPoolMemberIp += pmPoolMemberIp[i].value + "|";
    		//strPmPoolMemberPort += pmPoolMemberPort[i].value + "|";
    		strPmPoolMemberRatio += pmPoolMemberRatio[i].value + "|";
    		strPmPoolMemberMon += pmPoolMemberMon[i].value + "|";
    		strPmPriGroup += pmPriGroup[i].value + "|";
    	}
    	//'PhpFileName' 'DevIP' 'P_name' 'P_part' 'P_mon' 'P_LB' 'P_priGroup' 'P_lessthan' 'PM_names'  
    	//'PM_ips' 'PM_ports' 'PM_ratios' 'PM_mons' 'PM_priGroup'
    	var poolData = {'PhpFileName':'', 'DevIP':'', 'P_name':'', 'P_part':'', 'P_mon':'','P_LB':'', 'P_priGroup':'', 'P_lessthan':'', 'PM_names':'', 'PM_ips':'', 'PM_ratios':'', 'PM_mons':'', 'PM_priGroup':''};
    	poolData['PhpFileName'] = 'chg_pool_build';
    	poolData['DevIP'] = arr[1];
    	poolData['P_name'] = pName;
    	poolData['P_part'] = pPart;
    	poolData['P_mon'] =pMon;
    	poolData['P_LB'] = pLBMethod;
    	poolData['P_priGroup'] = pPriGroup;
    	poolData['P_lessthan'] = pPriGroupLessThan;
    	poolData['PM_names'] = strPmPoolMemberName;
    	poolData['PM_ips'] = strPmPoolMemberIp;
    	//poolData['PM_ports'] = strPmPoolMemberPort;
    	poolData['PM_ratios'] = strPmPoolMemberRatio;
    	poolData['PM_mons'] = strPmPoolMemberMon;
    	poolData['PM_priGroup'] = strPmPriGroup;
    	
    	ajxOut = $.ajax({
    		url: '/content/chg_pool_build.php',
    		type: 'POST',
    		dataType: 'JSON',
    		async: false,
    		data: {'jsonPoolData' : JSON.stringify(poolData)},
    		error: function(jqXHR, textStatus, errorThrown){
    			alert("Ajax call to modify pool configuration has failed!");
                console.log('jqXHR:');
                console.log(jqXHR);
                console.log('textStatus:');
                console.log(textStatus);
                console.log('errorThrown:');
                console.log(errorThrown);
    		}
    	});
    	ajxOut.done(showPoolChangeResult);
	});	
	
	//Event handler for when Partition selection is made
	$('#partition_name_select').on('change', function(){
		
		// Reset Pool Name select option to default
		$('#del_p_name_select option').each(function(index) {
			$(this).remove();
		});
		$('#del_p_name_select').append("<option value='none' selected='selected'>None</option>");

		if(this.value == 'select') return;
		
		var nameAndIp = $('#ltmSelBox option:selected').val();
		var arr = nameAndIp.split(":");
		var partName = this.value;
		
		// Load the pool names of a given partition
		// Call Ajax to retrieve pool names from a given LTM
		ajxOut = $.ajax({
			url: '/content/get_pool_names.php',
			type: 'POST',
			dataType: 'JSON',
			data: {method:'get_pool_names', DevIP:arr[1], Partition:partName},
			error: function(jqXHR, textStatus, errorThrown){
				alert("Ajax call for retrieving pool names has failed!");
	            console.log('jqXHR:');
	            console.log(jqXHR);
	            console.log('textStatus:');
	            console.log(textStatus);
	            console.log('errorThrown:');
	            console.log(errorThrown);
			}
		});
		ajxOut.done(prfPoolNameProcessData);
	});
	
	//Event handler for when Delete Pool button click event is fired
	$('#btn_delPool').on('click', function(){
		
		if ( ($('#del_p_name_select').val() == 'none') || ($('#partition_name_select').val() == 'select')) 
			alert("Please chose a partition and/or pool name to delete!");
		
		// Builtin profile names are not listed from drop-down box
		var nameAndIp = $('#ltmSelBox option:selected').val();
		var arr = nameAndIp.split(":");
		var partition = $('#partition_name_select').val();
		var poolName = $('#del_p_name_select').val();
		
		// Call Ajax to delete a given pool from a given LTM
		var poolData = {'PhpFileName':'del_pool_ajax', 'DevIP':'', 'P_name':'', 'P_part':'' };
		poolData['DevIP'] = arr[1];
		poolData['P_name'] = poolName;
		poolData['P_part'] = partition;
		ajxOut = $.ajax({
			url: '/content/del_pool_ajax.php',
			type: 'POST',
			dataType: 'JSON',
			data: {'jsonPoolData' : JSON.stringify(poolData)},
			error: function(jqXHR, textStatus, errorThrown){
				alert("Ajax call for deleting a given pool has failed!");
	            console.log('jqXHR:');
	            console.log(jqXHR);
	            console.log('textStatus:');
	            console.log(textStatus);
	            console.log('errorThrown:');
	            console.log(errorThrown);
			}
		});
		ajxOut.done(poolDeleteProcessData);
	});
});