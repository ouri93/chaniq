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
			//newcell.innerHTML = table.rows[0].cells[i].innerHTML;
			newcell.innerHTML = table.rows[1].cells[i].innerHTML;
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
			if(rowCount <= 2) { 						// limit the user from removing all the rows and header row
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
	
	if (selID == 'vs_pool_chosen') strResult += "<option value='newPool'>New Pool</option>";
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
	
	if (loadType == 'POOL') callingUrl = 'get_pool_names';
	else if (loadType == 'ALL') callingUrl = 'get_pool_monitors';
	else callingUrl = 'get_profile_names';

	ajxOut = $.ajax({
		url: '/content/' + callingUrl + '.php',
		type: 'POST',
		dataType: 'JSON',
		data: {method:callingUrl, DevIP:ltmIP, LoadTypeName:loadType, Partition:'Common'},
		error: function(jqXHR, textStatus, errorThrown){
			alert("Ajax call to retrieve object option names (loadOptNames - " + callingUrl + ".php) has failed!");
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
			alert("Ajax call to retrieve object names (loadObjNames) failed!");
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

function loadVSConfig(ltmIP, vsName, vsPart){
	var callingUrl = '';
	callingUrl = 'get_vs_config';
	
	ajxOut = $.ajax({
		url: '/content/' + callingUrl + '.php',
		type: 'POST',
		dataType: 'JSON',
		data: {method:callingUrl, DevIP:ltmIP, VsName:vsName, VsPart:vsPart},
		error: function(jqXHR, textStatus, errorThrown){
			alert("Ajax call to load VS configuration has failed!");
            console.log('jqXHR:');
            console.log(jqXHR);
            console.log('textStatus:');
            console.log(textStatus);
            console.log('errorThrown:');
            console.log(errorThrown);
		}
	});
	ajxOut.done(function (response_in) {
			loadVSConfigProcessData(response_in);
	});
}

function loadVSConfigProcessData(response_in) {
	var strResult = '';

	//Fill in Virtual Server configuration data with the data given by BIG-IP
	// ID list: vs_desc, vs_dest, vs_port, vs_type, vs_tcpprofile, vs_persist, vs_irule, vs_snatpool, 
	//          vs_policy, vs_httpprf, vs_clisslprf, vs_srvsslprf, vs_poolname
	$.each(response_in, function(index) {
		var strKey = index;
		if ( index='vs_name' && response_in[index].search('FAIL') > -1 ){
			strResult = "<b>Retrieving Virtual Server properties has failed<b><br>";
			strResult = strResult + response_in[index];
			$('#newvs_EvalReview').append(strResult);
			return;
		}
		switch(strKey) {
		case 'vs_desc':
			$('#vs_desc').val(response_in[strKey]);
			break;
		case 'vs_dest':
			$('#vs_dest').val(response_in[strKey]);
			break;
		case 'vs_port':
			$('#vs_port').val(response_in[strKey]);
			break;
		case 'vs_type':
			$('#vs_type').val(response_in[strKey]);
			break;
		case 'vs_tcpprofile':
			$('#vs_tcpprofile').val(response_in[strKey]);
			break;			
		case 'vs_persist':
			$('#vs_persist').val(response_in[strKey]);
			break;			
		case 'vs_irule':
			$('#vs_irule').val(response_in[strKey]);
			break;			
		case 'vs_snatpool':
			$('#vs_snatpool').val(response_in[strKey]);
			break;			
		case 'vs_policy':
			$('#vs_policy').val(response_in[strKey]);
			break;			
		case 'vs_httpprf':
			$('#vs_httpprf').val(response_in[strKey]);
			break;			
		case 'vs_clisslprf':
			$('#vs_clisslprf').val(response_in[strKey]);
			break;			
		case 'vs_srvsslprf':
			$('#vs_srvsslprf').val(response_in[strKey]);
			break;			
		case 'vs_poolname':
			$('#chg_vs_pool_chosen').val(response_in[strKey]);
			break;
		}
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


function isMinNumOfPoolMbr(){
	minPoolMbr = parseInt($('#vs_poolmbrnum option:selected').val());
	if (minPoolMbr > 0) return true;
	else return false;
}

function isValidInputs(){
	//if (dnsValidation('vs_dnsname') && ipValidation('vs_dest') && portValidation('vs_port') ) {
	if (ipValidation('vs_dest') && portValidation('vs_port') ) {
		return true;
	}
/*	
	if ($('#chkbox_vs_new_pool').prop('checked')){
		if (dnsValidation('vs_dnsname') && ipValidation('vs_dest') && portValidation('vs_port') && dnsValidation('vs_poolname') && isMinNumOfPoolMbr() ) {
			alert('checkbox_vs_new_pool: checked');
			return true;
		}
		else {
			return false;
		}
	}
	else {
		if (dnsValidation('vs_dnsname') && ipValidation('vs_dest') && portValidation('vs_port')) {
			alert('checkbox_vs_new_pool: Not checked');
			return true;
		}
		else {
			return false;
		}
	}
*/
}

//JQueury 
$(function () {
	
	// Default - Disable new pool creation
	/*
	$('#vs_poolname').prop('disabled', true).css('opacity', 0.3);
	$('#vs_poolmon').prop('disabled', true).css('opacity', 0.3);
	$('#vs_poolmbrnum').prop('disabled', true).css('opacity', 0.3);
	*/
	$('#div_ltmchoice').on('change', function() {
		var nameAndIp = $('#ltmSelBox option:selected').val();
		if (nameAndIp == 'Select...') return;
		
		var arr = nameAndIp.split(":");
		loadOptNames(arr[1], 'TCP', 'vs_tcpprofile');
		loadOptNames(arr[1], 'PERSIST', 'vs_persist');
		loadOptNames(arr[1], 'IRULE', 'vs_irule');
		loadOptNames(arr[1], 'SNATPOOL', 'vs_snatpool');
		loadOptNames(arr[1], 'POLICY', 'vs_policy');
		loadOptNames(arr[1], 'HTTP', 'vs_httpprf');
		loadOptNames(arr[1], 'CLIENTSSL', 'vs_clisslprf');
		loadOptNames(arr[1], 'SERVERSSL', 'vs_srvsslprf');
		//loadOptNames(arr[1], 'ALL', 'vs_poolmon');
		//loadOptNames(arr[1], 'ALL', 'vs_poolmbrmon');
		loadOptNames(arr[1], 'POOL', 'vs_pool_chosen');

	});
	
	// Open a New Pool build iFrame window as a popup
/*	
	$('#btn_createPool').on('click', function() {
		var poolCreationPopup = window.open('/content/if_new_pool.php', '_blank', 'width=750, height=700, frameborder=0');
		
		// Referesh Pool list - Detecting the popup iFrame window and update Pool list with a new pool
		$(poolCreationPopup).on('beforeunload', function(){
			var nameAndIp = $('#ltmSelBox option:selected').val();
			if (nameAndIp == 'Select...') return;
			
			var arr = nameAndIp.split(":");
			loadOptNames(arr[1], 'POOL', 'vs_pool_chosen');
		});
	});
	
	$('#chkbox_vs_new_pool').change(function() {
		if(this.checked){
			// Disable pool choice selection box
			//alert("chkbox_vs_new_pool is checked!");
			$('#vs_pool_chosen').prop('disabled', true).css('opacity', 0.3);
			$('#vs_poolname').prop('disabled', false).css('opacity', 1.0);
			$('#vs_poolmon').prop('disabled', false).css('opacity', 1.0);
			$('#vs_poolmbrnum').prop('disabled', false).css('opacity', 1.0);
			
			// Open Pool creation iframe as a popup window
			window.open('/content/if_new_pool.php', '_blank', 'width=750, height=700, frameborder=0');
			//var win=window.open();
			//win.document.write('<iframe src="/content/if_new_pool.php" width="720px" height="600" frameborder="0"></iframe>');
		}
		else {
			// Disable pool and pool member creation elements
			//alert("chkbox_vs_new_pool is unchecked!");
			$('#vs_pool_chosen').prop('disabled', false).css('opacity', 1.0);
			$('#vs_poolname').prop('disabled', true).css('opacity', 0.3);
			$('#vs_poolmon').prop('disabled', true).css('opacity', 0.3);
			$('#vs_poolmbrnum').prop('disabled', true).css('opacity', 0.3);
		}
	});
*/	
	
	// If 'New Pool' is selected from Pool filed, pop up a New pool creation iFrame window.
	// When a new pool is created successfully, updte Pool list with the newly created pool.
	$('#vs_pool_chosen').on('change', function(){
		if ($('#vs_pool_chosen option:selected').val() == 'newPool'){
			var poolCreationPopup = window.open('/content/if_new_pool.php', '_blank', 'width=750, height=700, frameborder=0');
			
			// Referesh Pool list - Detecting the popup iFrame window and update Pool list with a new pool
			$(poolCreationPopup).on('beforeunload', function(){
				var nameAndIp = $('#ltmSelBox option:selected').val();
				if (nameAndIp == 'Select...') return;
				
				var arr = nameAndIp.split(":");
				loadOptNames(arr[1], 'POOL', 'vs_pool_chosen');
			});
		}
	});
	
	$('#vs_btn_build').on('click', function() {
		if(!isValidInputs()){
			alert("Required validation failed!");
			return;
		}
			
		/*
		var isNewPool = 0;
		if ($('#chkbox_vs_new_pool').prop('checked'))
			isNewPool = 1;
		*/
		
		// Gather input values		
		var nameAndIp = $('#ltmSelBox option:selected').val();
		var arr = nameAndIp.split(":");
		var active_ltm = arr[1];
		var vs_dnsname = $('#vs_dnsname').val();
		var vs_dest = $('#vs_dest').val();
        var vs_port = $('#vs_port').val();
        var vs_desc = $('#vs_desc').val();
        var vs_env = $('#vs_env option:selected').val();
        var vs_type = $('#vs_type option:selected').val();
        var vs_tcpprofile = $('#vs_tcpprofile option:selected').val();
        var vs_persistence = $('#vs_persist option:selected').val();
        var vs_redirect = $('#vs_redirect option:selected').val();
        var vs_irule = $('#vs_irule option:selected').val();
        var vs_snatpool = $('#vs_snatpool option:selected').val();
        var vs_policy = $('#vs_policy option:selected').val();
        var vs_httpprofile = $('#vs_httpprf option:selected').val();
        var vs_sslclient = $('#vs_clisslprf option:selected').val();
        var vs_sslserver = $('#vs_srvsslprf option:selected').val();
        
        var vs_poolname = $('#vs_pool_chosen option:selected').val();
                
/*
        var vs_poolname = $('#vs_poolname').val();
        var vs_poolmon = $('#vs_poolmon option:selected').val();
        var vs_poolmbrnum = parseInt($('#vs_poolmbrnum option:selected').val());
        var pool_membernames = '';
        var pool_memberips = '';
        var pool_memberports = '';
        var pool_membermons = '';

        var numOfRow = $('#dataTable tr').length;
        //alert("Length of TR: " + numOfRow);
        for(i=0; i<vs_poolmbrnum;i++){
        	if (i == numOfRow-1){
	        	pool_membernames += $('#pool_membername' + i).val();
	        	pool_memberips += $('#pool_memberip' + i).val();
	        	pool_memberports += $('#pool_memberport' + i).val();
	        	pool_membermons += $('#pool_membermon' + i).val();
        	}
        	else{
	        	pool_membernames += $('#pool_membername' + i).val() + ":";
	        	pool_memberips += $('#pool_memberip' + i).val() + ":";
	        	pool_memberports += $('#pool_memberport' + i).val() + ":";
	        	pool_membermons += $('#pool_membermon' + i).val() + ":";
        	}
        }
        
        //alert("Number of rows: " + $('#dataTable tr').length);

        // 1. Build node
    	var nodeData = {'PhpFileName':'', 'DevIP':'', 'Pool_membernames':'', 'Pool_memberips':''};
    	nodeData['PhpFileName'] = 'new_node_build';
    	nodeData['DevIP'] = arr[1];
    	nodeData['Pool_membernames'] = pool_membernames;
    	nodeData['Pool_memberips'] = pool_memberips;
    	
    	ajxOut = $.ajax({
    		url: '/content/new_node_build.php',
    		type: 'POST',
    		dataType: 'JSON',
    		async: false,
    		data: {'jsonNodeData' : JSON.stringify(nodeData)},
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
    		var strResult = '';
    		$.each(response_in, function(index) {
    			if(index == 0) 
    				strResult = "<b>" + response_in[index] + "</b><br>";
    			else
    				strResult += response_in[index] + "<br>";
    		});
    		
    		//alert("Return output: " + strResult);
    		$('#newvs_EvalReview').html(strResult);
    	});
    	ajxOut.fail(function(){
    		alert("Ajax call for Node build failed!");
    		return;
    	});

    	// 2. Build pool
    	var poolData = {'PhpFileName':'', 'DevIP':'', 'Vs_poolname':'', 'Vs_port':'', 'Vs_env':'', 'Vs_poolmon':'','Pool_membernames':'', 'Pool_memberips':'', 'Pool_memberports':'', 'Pool_membermons':''};
    	poolData['PhpFileName'] = 'new_pool_build2';
    	poolData['DevIP'] = arr[1];
    	poolData['Vs_poolname'] = vs_poolname;
    	poolData['Vs_port'] = vs_port;
    	poolData['Vs_env'] = vs_env;
    	poolData['Vs_poolmon'] =vs_poolmon;
    	poolData['Pool_membernames'] = pool_membernames;
    	poolData['Pool_memberips'] = pool_memberips;
    	poolData['Pool_memberports'] = pool_memberports;
    	poolData['Pool_membermons'] = pool_membermons;
    	
    	ajxOut = $.ajax({
    		url: '/content/new_pool_build2.php',
    		type: 'POST',
    		dataType: 'JSON',
    		async: false,
    		data: {'jsonPoolData' : JSON.stringify(poolData)},
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
    		var strResult = '';
    		$.each(response_in, function(index) {
    			if(index == 0) 
    				strResult = "<b>" + response_in[index] + "</b><br>";
    			else
    				strResult += response_in[index] + "<br>";
    		});
    		
    		//alert("Return output: " + strResult);
    		$('#newvs_EvalReview').append(strResult);
    	});
    	ajxOut.fail(function(){
    		alert("Ajax call for Node build failed!");
    		return;
    	});
*/
        // 3. Build Virtual Server
    	// active_ltm, vs_dnsname, vs_dest, vs_port, vs_desc, vs_env, vs_tcpprofile, vs_persistence, vs_redirect, vs_type, vs_httpprofile, vs_sslclient, vs_sslserver, vs_irule, vs_snatpool, vs_policy
    	var vsData = {'PhpFileName':'', 'DevIP':'', 'Vs_name':'', 'Vs_dest':'', 'Vs_port':'', 'Vs_desc':'', 'Vs_env':'', 'Vs_tcpprf':'','Vs_persist':'', 'Vs_redirect':'', 'Vs_type':'', 'Vs_httpprf':'', 'Vs_clisslprf':'', 'Vs_srvsslprf':'', 'Vs_irule':'', 'Vs_snatpool':'', 'Vs_policy':'', 'Vs_poolname':''};
    	vsData['PhpFileName'] = 'new_vs_build2';
    	vsData['DevIP'] = arr[1];
    	vsData['Vs_name'] = vs_dnsname;
    	vsData['Vs_dest'] = vs_dest;
    	vsData['Vs_port'] = vs_port;
    	vsData['Vs_desc'] = vs_desc;
    	vsData['Vs_env'] = vs_env;
    	vsData['Vs_tcpprf'] =vs_tcpprofile;
    	vsData['Vs_persist'] =vs_persistence;
    	vsData['Vs_redirect'] =vs_redirect;
    	vsData['Vs_type'] =vs_type;
    	vsData['Vs_httpprf'] =vs_httpprofile;
    	vsData['Vs_clisslprf'] = vs_sslclient;
    	vsData['Vs_srvsslprf'] = vs_sslserver;
    	vsData['Vs_irule'] = vs_irule;
    	vsData['Vs_snatpool'] = vs_snatpool;
    	vsData['Vs_policy'] = vs_policy;
    	
    	vsData['Vs_poolname'] = vs_poolname;
    	
    	ajxOut = $.ajax({
    		url: '/content/new_vs_build2.php',
    		type: 'POST',
    		dataType: 'JSON',
    		async: false,
    		data: {'jsonVsData' : JSON.stringify(vsData)},
    		error: function(jqXHR, textStatus, errorThrown){
    			alert("Ajax call to build requested virtual server has failed!");
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
    		$.each(response_in, function(index) {
    			if(index == 0) 
    				strResult = "<b>" + response_in[index] + "</b><br>";
    			else
    				strResult += response_in[index] + "<br>";
    		});
    		
    		//alert("Return output: " + strResult);
    		$('#newvs_EvalReview').append(strResult);
    	});
    	ajxOut.fail(function(){
    		alert("Ajax call for Node build failed!");
    		return;
    	});
	});

/*
	$('#vs_poolmbrnum').on('change', function() {
		var $numOfPoolmbr = parseInt($('#vs_poolmbrnum option:selected').val());
		//alert("Number of pool members: " + $numOfPoolmbr);
		var strResult = '';
		
		$('#poolmbrTbody').empty();

		var nameAndIp = $('#ltmSelBox option:selected').val();
		var arr = nameAndIp.split(":");
		
		for(i=0;i<$numOfPoolmbr;i++) {
			strResult += "<tr>";
			strResult += "<td><label>DNS Name: </label><input type='text' id='pool_membername" + i +"' /></td>";
			strResult += "<td><label>IP: </label><input type='text' id='pool_memberip" + i +"' /></td>";
			strResult += "<td><label>Port: </label><input type='text' id='pool_memberport" + i +"' /></td>";
			strResult += "<td><label>Monitor: </label><select id='pool_membermon" + i +"'><option value='inherit' selected>Inherit</option></select></td>";
			strResult += "</tr>"
		}
		$('#poolmbrTbody').append(strResult);
		
		for(i=0;i<$numOfPoolmbr;i++){
			loadOptNames(arr[1], 'ALL', "pool_membermon" + i);			
		}
	});
*/	
	///////////////////////////////// Virtual Server modification ///////////////////////////////
	$('#chg_div_ltmchoice').on('change', function() {
		var nameAndIp = $('#ltmSelBox option:selected').val();
		if (nameAndIp == 'Select...') return;
		
		var arr = nameAndIp.split(":");
		loadObjNames(arr[1], 'VS', 'chg_vs_sel_vs');

		loadOptNames(arr[1], 'TCP', 'vs_tcpprofile');
		loadOptNames(arr[1], 'PERSIST', 'vs_persist');
		loadOptNames(arr[1], 'IRULE', 'vs_irule');
		loadOptNames(arr[1], 'SNATPOOL', 'vs_snatpool');
		loadOptNames(arr[1], 'POLICY', 'vs_policy');
		loadOptNames(arr[1], 'HTTP', 'vs_httpprf');
		loadOptNames(arr[1], 'CLIENTSSL', 'vs_clisslprf');
		loadOptNames(arr[1], 'SERVERSSL', 'vs_srvsslprf');
		//loadOptNames(arr[1], 'ALL', 'vs_poolmon');
		//loadOptNames(arr[1], 'ALL', 'vs_poolmbrmon');
		
		loadOptNames(arr[1], 'POOL', 'chg_vs_pool_chosen');
	});
	
	$('#chg_vs_sel_vs').on('change', function() {
		var vsname_chosen = $('#chg_vs_sel_vs option:selected').val();
		//alert('Chosen VS name: ' + vsname_chosen);
		
		if (vsname_chosen == "select"){
			// Set default VS configuration
			$('#vs_dest').val('');
	        $('#vs_port').val('');
	        $('#vs_desc').val('');
	        $('#vs_type option[value="Standard"]').attr('selected', 'selected');
	        $('#vs_tcpprofile option[value="none"]').attr('selected', 'selected');
	        $('#vs_persist option[value="none"]').attr('selected', 'selected');
	        $('#vs_irule option[value="none"]').attr('selected', 'selected');
	        $('#vs_snatpool option[value="none"]').attr('selected', 'selected');
	        $('#vs_policy option[value="none"]').attr('selected', 'selected');
	        $('#vs_httpprf option[value="none"]').attr('selected', 'selected');
	        $('#vs_clisslprf option[value="none"]').attr('selected', 'selected');
	        $('#vs_srvsslprf option[value="none"]').attr('selected', 'selected');
	        $('#chg_vs_pool_chosen option[value="none"]').attr('selected', 'selected');
			return;
		}
		
		var nameAndIp = $('#ltmSelBox option:selected').val();
		var arr = nameAndIp.split(":");
		var active_ltm = arr[1];
		var vs_dnsname = vsname_chosen;

		// Load a chosen Virtual server configuration from BIG-IP
		loadVSConfig(active_ltm, vs_dnsname, "Common");
		
		/*
		var vs_dest;
        var vs_port;
        var vs_desc;
        var vs_type = $('#vs_type option:selected').val();
        var vs_tcpprofile = $('#vs_tcpprofile option:selected').val();
        var vs_persistence = $('#vs_persist option:selected').val();
        var vs_redirect = $('#vs_redirect option:selected').val();
        var vs_irule = $('#vs_irule option:selected').val();
        var vs_snatpool = $('#vs_snatpool option:selected').val();
        var vs_policy = $('#vs_policy option:selected').val();
        var vs_httpprofile = $('#vs_httpprf option:selected').val();
        var vs_sslclient = $('#vs_clisslprf option:selected').val();
        var vs_sslserver = $('#vs_srvsslprf option:selected').val();
        
        var vs_poolname = $('#vs_pool_chosen option:selected').val();
        */
		// Load the chosen VS configuration - Descritpion, Dest IP, Service Port, VS Type, TCP Profile, Persistence, iRule, SNAT Pool, Policies, HTTP Profile, Client SSL Profile, Server SSL profile, Pool name
		
	});
	
	$('#del_div_ltmchoice').on('change', function() {
		var nameAndIp = $('#ltmSelBox option:selected').val();
		if (nameAndIp == 'Select...') return;
		
		var arr = nameAndIp.split(":");
		loadObjNames(arr[1], 'VS', 'del_vs_sel_vs');

	});
	
	// Event handler for when Delete button is clicked
	$('#vs_btn_delete').on('click', function(){
		if($('#del_vs_sel_vs').val() == 'select'){
			alert("Please select a virtual server name to delete");
			return;
		}
		
		var nameAndIp = $('#ltmSelBox option:selected').val();
		var arr = nameAndIp.split(":");
		var active_ltm = arr[1];
		
		var vs_name = $('#del_vs_sel_vs').val();
		var partition = "Common";
		var vsData = {'PhpFileName':'', 'DevIP':'', 'Vs_name':'', 'Partition':''};
		
		vsData['PhpFileName'] = 'del_vs_ajax';
		vsData['DevIP'] = active_ltm;
		vsData['Vs_name'] = vs_name;
		vsData['Partition'] = partition;
		
    	ajxOut = $.ajax({
    		url: '/content/del_vs_ajax.php',
    		type: 'POST',
    		dataType: 'JSON',
    		data: {'jsonVsData' : JSON.stringify(vsData)},
    		error: function(jqXHR, textStatus, errorThrown){
    			alert("Ajax call to delete a virtual server has failed!");
                console.log('jqXHR:');
                console.log(jqXHR);
                console.log('textStatus:');
                console.log(textStatus);
                console.log('errorThrown:');
                console.log(errorThrown);
    		}
    	});
		
    	ajxOut.done(function (response_in){
    		var strResult = '';
    		$.each(response_in, function(index) {
    			if(index == 0) 
    				strResult = "<b>" + response_in[index] + "</b><br>";
    			else
    				strResult += response_in[index] + "<br>";
    		});
    		
    		//alert("Return output: " + strResult);
    		$('#newvs_EvalReview').html(strResult);    		
    	});
    	
    	// Update Virtual Server list after deletion
    	loadObjNames(arr[1], 'VS', 'del_vs_sel_vs');
	});
	
	// Event handler for when 'Modify VS' is clicked to update virtual server configuration
	$('#btn_vs_modify').on('click', function(){
		if($('#chg_vs_sel_vs').val() == 'select'){
			alert("Please choose a Virtual Server to modify");
			return;
		}
		
		// Gather input values		
		var nameAndIp = $('#ltmSelBox option:selected').val();
		var arr = nameAndIp.split(":");
		var active_ltm = arr[1];
		var vs_dnsname = $('#chg_vs_sel_vs').val();
		var vs_dest = $('#vs_dest').val();
        var vs_port = $('#vs_port').val();
        var vs_desc = $('#vs_desc').val();
        var vs_type = $('#vs_type option:selected').val();
        var vs_tcpprofile = $('#vs_tcpprofile option:selected').val();
        var vs_persistence = $('#vs_persist option:selected').val();
        var vs_irule = $('#vs_irule option:selected').val();
        var vs_snatpool = $('#vs_snatpool option:selected').val();
        var vs_policy = $('#vs_policy option:selected').val();
        var vs_httpprofile = $('#vs_httpprf option:selected').val();
        var vs_sslclient = $('#vs_clisslprf option:selected').val();
        var vs_sslserver = $('#vs_srvsslprf option:selected').val();
        var vs_poolname = $('#chg_vs_pool_chosen option:selected').val();
        
        // 2. Modify Virtual Server
    	// active_ltm, vs_dnsname, vs_dest, vs_port, vs_desc, vs_env, vs_tcpprofile, vs_persistence, vs_redirect, vs_type, vs_httpprofile, vs_sslclient, vs_sslserver, vs_irule, vs_snatpool, vs_policy
    	var vsData = {'PhpFileName':'', 'DevIP':'', 'Vs_name':'', 'Vs_dest':'', 'Vs_port':'', 'Vs_desc':'', 'Vs_tcpprf':'','Vs_persist':'', 'Vs_type':'', 'Vs_httpprf':'', 'Vs_clisslprf':'', 'Vs_srvsslprf':'', 'Vs_irule':'', 'Vs_snatpool':'', 'Vs_policy':'', 'Vs_poolname':''};
    	vsData['PhpFileName'] = 'chg_vs_ajax';
    	vsData['DevIP'] = arr[1];
    	vsData['Vs_name'] = vs_dnsname;
    	vsData['Vs_dest'] = vs_dest;
    	vsData['Vs_port'] = vs_port;
    	vsData['Vs_desc'] = vs_desc;
    	vsData['Vs_tcpprf'] =vs_tcpprofile;
    	vsData['Vs_persist'] =vs_persistence;
    	vsData['Vs_type'] =vs_type;
    	vsData['Vs_httpprf'] =vs_httpprofile;
    	vsData['Vs_clisslprf'] = vs_sslclient;
    	vsData['Vs_srvsslprf'] = vs_sslserver;
    	vsData['Vs_irule'] = vs_irule;
    	vsData['Vs_snatpool'] = vs_snatpool;
    	vsData['Vs_policy'] = vs_policy;
    	vsData['Vs_poolname'] = vs_poolname;
    	
    	ajxOut = $.ajax({
    		url: '/content/chg_vs_ajax.php',
    		type: 'POST',
    		dataType: 'JSON',
    		async: false,
    		data: {'jsonVsData' : JSON.stringify(vsData)},
    		error: function(jqXHR, textStatus, errorThrown){
    			alert("Ajax call to modify requested virtual server has failed!");
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
    		$.each(response_in, function(index) {
    			if(index == 0) 
    				strResult = "<b>" + response_in[index] + "</b><br>";
    			else
    				strResult += response_in[index] + "<br>";
    		});
    		
    		//alert("Return output: " + strResult);
    		$('#newvs_EvalReview').append(strResult);
    	});
    	
	});
	
});