
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

function isValidName(objip){
	document.getElementById(objip).style.borderColor="#E1E1E1";
	
	var val = document.getElementById(objip).value;
    if (val != ""){
    	document.getElementById(objip).style.borderColor="#E1E1E1";
        return true;
    }
    else {
        document.getElementById(objip).value = "";
        document.getElementById(objip).style.borderColor="red";
        return false;        
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


// Process snatpool names returned from BIG-IP
function loadSnatpoolNameProcess(response_in){
	var strResult = '';
	if (response_in.includes("FAIL")){
		strResult = "<b>Loading SNATPOOL names failed!</b><br>" + response_in[1] + "<br>";
		$('#newSnat_EvalReview').html(strResult);
		return;
	}
	
	var strNames = '';
	var strParts = '';
	$.each(response_in, function(index){
		if (index % 2 == 0)
			strNames += "<option value='" + response_in[index] + "'>" + response_in[index] + "</option>";
		else{
			if (response_in[index] != 'Common')
				strParts += "<option value='" + response_in[index] + "'>" + response_in[index] + "</option>";
		}
	});
	$('#select_snatpool_name').append(strNames);
	$('#select_del_snatpool_part').append(strParts);
}

// Process the result data returning from deleting a snatpool of BIG-IP
function delSnatpoolProcess(response_in){
	var strResult = '';
	if (response_in.includes("FAIL")){
		strResult = "<b>Deleting SNATPOOL has failed!</b><br>" + response_in[2] + "<br>";
		$('#newSnat_EvalReview').html(strResult);
		return;
	}
	
	$.each(response_in, function(index){
		if(index == 0){
			strResult = "<b>" + response_in[index] + "</b><br>";
		}
		strResult = strResult + response_in[index] + "<br>";
	});
	
	$('#newSnat_EvalReview').html(strResult);
}

//JQueury 
$(function () {
	$('#div_ltmchoice').on('change', function() {
		var nameAndIp = $('#ltmSelBox option:selected').val();
		if (nameAndIp == 'Select...'){
			// Reset Snatpool and Partition
			$('#select_snatpool_name').empty();
			$('#select_snatpool_name').append('<option value="select">Select...</option>');
			$('#select_del_snatpool_part').empty();
			$('#select_del_snatpool_part').append('<option value="common">Common</option>');
			return;
		}
		
		var nameAndIp = $('#ltmSelBox option:selected').val();
		var arr = nameAndIp.split(":");

		if (GetParentURLParameter('go') == 'del_snatpool'){
			// Call Ajax to retrieve snatpool names from a given BIG-IP
			var snatData = {'PhpFileName':'load_snatpool_names', 'DevIP':''};
			snatData['DevIP'] = arr[1];
			
			ajxOut = $.ajax({
				url: '/content/load_snatpool_names.php',
				type: 'POST',
				dataType: 'JSON',
				data: {'jsonData' : JSON.stringify(snatData)},
				error: function(jqXHR, textStatus, errorThrown){
					alert("Ajax call for loading snatpool names has failed!");
		            console.log('jqXHR:');
		            console.log(jqXHR);
		            console.log('textStatus:');
		            console.log(textStatus);
		            console.log('errorThrown:');
		            console.log(errorThrown);
				}
			});
			ajxOut.done(loadSnatpoolNameProcess);
		}
	});
	
	$('#snat_add').on('click', function() {
		// Validate input values
		if (!ipValidation('snat_ipaddr')){
			alert("Input validation failed!");
			return;
		}
		
    	//alert("Add button clicked!");
    	var snat_addr = $('#snat_ipaddr').val();
    	$('#snat_address_list').append('<option value="'+ snat_addr +'">' + snat_addr + '</option>');
    	$('#snat_add').focus();

	});
	
    $('#snat_edit').on('click', function() {
    	var snat_addr_to_edit = $('#snat_address_list option:selected').text();
    	$('#snat_ipaddr').val(snat_addr_to_edit);
    	
    	$('#snat_address_list option').each(function() {
    		//alert("Option Value: " + $(this).val());
    		if ($(this).val() == snat_addr_to_edit){
    			$(this).remove();
    		}
    	});
    });
    
    $('#snat_del').on('click', function() {
    	var snat_addr_to_delete = $('#snat_address_list option:selected').text();
    	
    	$('#snat_address_list option').each(function() {
    		if ($(this).val() == snat_addr_to_delete){
    			$(this).remove();
    		}
    	});
    });
	
	$('#snat_build').on('click', function() {
		if(!isValidName('snat_name')){
			alert("Required validation failed!");
			return;
		}
			
		// Gather input values
		var nameAndIp = $('#ltmSelBox option:selected').val();
		var arr = nameAndIp.split(":");
		var active_ltm = arr[1];
		
		var snat_name = $('#snat_name').val();
		
		
		var snatRecords = '';
		var len = $('#snat_address_list option').length;
    	$('#snat_address_list option').each(function(index) {
    		snatRecords += $(this).val();
    		if(index != (len-1))
    			snatRecords += ':';
    	});
    	//alert("Snat Addresses: " + snatRecords);
		
        // 1. Build Snatpool
    	var snatData = {'PhpFileName':'', 'DevIP':'', 'Snat_name':'', 'Snat_members':''};
    	snatData['PhpFileName'] = 'new_snatpool_build';
    	snatData['DevIP'] = arr[1];
    	snatData['Snat_name'] = snat_name;
    	snatData['Snat_members'] = snatRecords;

    	
    	ajxOut = $.ajax({
    		url: '/content/new_snatpool_build.php',
    		type: 'POST',
    		dataType: 'JSON',
    		data: {'jsonSnatData' : JSON.stringify(snatData)},
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
    		$('#newSnat_EvalReview').html(strResult);
    	});
    	ajxOut.fail(function(){
    		alert("Ajax call for Snatpool build failed!");
    		return;
    	});
	});

	//Event handler for when "Delete Snatpool" button is clicked
	$('#del_snatpool').on('click', function(){
		// Gather input values
		var nameAndIp = $('#ltmSelBox option:selected').val();
		var arr = nameAndIp.split(":");
		var active_ltm = arr[1];
		
		var snatname = $('#select_snatpool_name').val();
		var partname = $('#select_del_snatpool_part').val();
		if(snatname == 'select') {
			alert("Please select a Snatpool name to delete");
			return;
		}
		
    	var snatData = {'PhpFileName':'', 'DevIP':'', 'Name':'', 'Partition':''};
    	snatData['PhpFileName'] = 'del_snatpool_ajax';
    	snatData['DevIP'] = arr[1];
    	snatData['Name'] = snatname;
    	snatData['Partition'] = partname;
    	
    	ajxOut = $.ajax({
    		url: '/content/del_snatpool_ajax.php',
    		type: 'POST',
    		dataType: 'JSON',
    		data: {'jsonData' : JSON.stringify(snatData)},
    		error: function(jqXHR, textStatus, errorThrown){
    			alert("Ajax call to delete a snatpool has failed!");
                console.log('jqXHR:');
                console.log(jqXHR);
                console.log('textStatus:');
                console.log(textStatus);
                console.log('errorThrown:');
                console.log(errorThrown);
    		}
    	});
    	ajxOut.done(delSnatpoolProcess);
	});
	
});