/* 
 * Javascript for moving items between two list boxes
 */
/*
 * Original example found here: http://www.jquerybyexample.net/2012/05/how-to-move-items-between-listbox-using.html
 * Modified by Esau Silva to support 'Move ALL items to left/right' and add better stylingon on Jan 28, 2016.
 * 
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

// Process iRule/Data Group names returned from BIG-IP
function irdgNameLoadingProcess(response_in){
	// Add retrieved iRule or Data Group nmae to select_ir_dg_name option list
	var strHtml = '';
	$('#select_ir_dg_name').empty();
	$('#select_ir_dg_name').append('<option value="select" selected="selected">Select...</option>');
	
	// Builtin iRule list - BIG-IP 12.1.2
	var builtins = ['_sys_APM_ExchangeSupport_OA_BasicAuth', '_sys_APM_ExchangeSupport_OA_NtlmAuth', '_sys_APM_ExchangeSupport_helper', 
		'_sys_APM_ExchangeSupport_main', '_sys_APM_Office365_SAML_BasicAuth', '_sys_APM_activesync', '_sys_auth_krbdelegate', '_sys_auth_ldap', 
		'_sys_auth_radius', '_sys_auth_ssl_cc_ldap', '_sys_auth_ssl_crldp', '_sys_auth_ssl_ocsp', '_sys_auth_tacacs', '_sys_https_redirect'];
	$.each(response_in, function(index) {
		strHtml = '';
		if (builtins.indexOf(response_in[index]) == -1){
			strHtml = "<option>" + response_in[index] + "</option>";
		}
		$('#select_ir_dg_name').append(strHtml);
	});
}

//Process iRule/Data Group configuration returned from BIG-IP
function irdgConfigLoadingProcess(response_in){
	// Return Data format
	// iRule - {'IrDgType':'iRule', 'name':'name_of_iRule', 'apiAnonymous':'iRule_code' }
	// Data Group - {'IrDgType':'Data Group', 'name':'name_of_datagroup', 'type':'integer|string|address', 'records':[{'data':'data_val1', 'name':'name_val1'}, {'data':'data_val2', 'name':'name_val2'},... }
	//var result = JSON.parse(response_in);
	
	var irOrDg = '';
	
	// Pre-processing before you handle data such as building data group type input form
	$.each(response_in, function(index){
		if (index == 'IrOrDg') irOrDg = response_in[index];
		// Call delegated 'change' event of 'ir_td_dg_type' to build Data Group Type form
		if (index == 'type'){
			$('#ir_dg_type_select').find('option[value=' + response_in[index] + ']').attr('selected', true);
			if(GetParentURLParameter('go') != 'del_irule')
				$('#ir_td_dg_type').trigger('change');
		}
	});
	
	$.each(response_in, function(index){
		// index: key value, response_in[index]: data value
		// e.g. index='name', response_in[index] = name_of_iRule
		if (irOrDg == 'iRule' && index == 'apiAnonymous'){
			$('#irConfCode').val(response_in[index]);
		}
		else if (irOrDg == 'Data Group'){
			if(index == 'records') {
				for(i=0;i<response_in['records'].length;i++){
			    	var dg_name = response_in['records'][i]['name'];
			    	var dg_val = response_in['records'][i]['data'];
			    	if (dg_name != '' && dg_val != '')
			    		$('#dg_select_records').append('<option value="'+ dg_name + ':=' + dg_val +'">' + dg_name + ':=' + dg_val + '</option>');
		    		else if (dg_name != '' && dg_val == '')
		    			$('#dg_select_records').append('<option value="'+ dg_name + '">' + dg_name + '</option>');
		    		else
		    			alert("Data Group Data name is required!");
			    	
		    		$('#ir_dg_name').val('');
		    		$('#ir_dg_value').val('');
		    		$('#ir_dg_name').focus();
				}
			}
			
		}
	});
	//alert("IrDgType: " + result['IrDgType']);

}


//Process iRule/Data Group configuration udate result from BIG-IP
function irdgConfigUpdateProcess(response_in){
	// Add retrieved iRule or Data Group configuration change result to select_ir_dg_name option list
	var strResult = '';
	$.each(response_in, function(index) {
		if(index == 0) 
			strResult = "<b>" + response_in[index] + "</b><br>";
		else
			strResult += response_in[index] + "<br>";
	});
	
	$('#newIr_EvalReview').html(strResult);
}

//Process iRule/Data Group deletion result returnning from BIG-IP
function delIrdgProcess(response_in){
	// Add retrieved iRule or Data Group configuration change result to select_ir_dg_name option list
	var strResult = '';
	$.each(response_in, function(index) {
		if(index == 0) 
			strResult = "<b>" + response_in[index] + "</b><br>";
		else
			strResult += response_in[index] + "<br>";
	});
	
	$('#newIr_EvalReview').html(strResult);
}


function buildIrAjax(phpFileName, irData) {
	return $.ajax({
		url: '/content/new_irule_build.php',
		type: 'POST',
		dataType: 'JSON',
		data: {'jsonIrData': JSON.stringify(irData)},
		error: function(jqXHR, textStatus, errorThrown){
			alert("buildIrAjax Ajax call failed!");
            console.log('jqXHR:');
            console.log(jqXHR);
            console.log('textStatus:');
            console.log(textStatus);
            console.log('errorThrown:');
            console.log(errorThrown);
		}
	});	
}

function buildIrProcessData(response_in) {
	var strResult = '';
	$.each(response_in, function(index) {
		if(index == 0) 
			strResult = "<b>" + response_in[index] + "</b><br>";
		else
			strResult += response_in[index] + "<br>";
	});
	
	//alert("Return output: " + strResult);
	$('#newIr_EvalReview').html(strResult);
}

$(function () {
	$('#div_ltmchoice').on('change', function() {
		var nameAndIp = $('#ltmSelBox option:selected').val();
		if (nameAndIp == 'Select...') return;

		var arr = nameAndIp.split(":");

	});
	
    // Generate proper configuration form
    // For iRule, generate iRule code form. For Data Group, generate Data Group type and corresponding configuration form.
    $('#ir_type').on('change', function() {
    	var ir_type = $('#ir_type').val();
    	if (ir_type == "iRule") {
    		$('#ir_td_dg_type').empty();
    		$('#ir_confTable_thead').empty();
    		$('#ir_confTable_thead').append("<th style='font-weight:normal' >iRule Code</th>");
        	$('#irConfTable_tbody').empty();
    		$('#irConfTable_tbody').append("<tr><td><textarea id='irConfCode' rows='10' cols='90'> </textarea> </td></tr>");
    	}
    	else if (ir_type == "Data Group"){
    		$('#ir_td_dg_type').empty();
    		$('#ir_confTable_thead').empty();
    		$('#ir_confTable_thead').append("<th style='font-weight:normal'>Data Group Configuration</th>");
    		$('#irConfTable_tbody').empty();
    		$('#ir_td_dg_type').append("<label> DG Type: </label><select name='ir_dg_type_select' id='ir_dg_type_select' required='required' ><option selected='selected'>Select...</option><option value='ip'>Address</option><option value='string'>String</option><option value='integer'>Integer</option></select>");
    	}
    });
    
    // Event delegation to ir_td_dg_type
    $('#ir_td_dg_type').on('change', function() {
    	
    	var ir_dg_type = $('#ir_dg_type_select').val();
    	//alert("ir_td_dg_type event delegation is called! Data Group Type: " + ir_dg_type);
    	$('#irConfTable_tbody').empty();
    	if (ir_dg_type == "ip"){
    		$('#irConfTable_tbody').append("<tr> <td> <label>Address:</label> <input type='text' id='ir_dg_name' />(Use CIDR format or IP *required) </td> </tr><tr> <td> <label>Value&nbsp;&nbsp;&nbsp;&nbsp;:</label> <input type='text' id='ir_dg_value' /> </td> </tr><tr><td><input type='button' id='ir_add_btn' value='Add' />&nbsp;&nbsp;&nbsp;&nbsp;</td></tr> <tr> <td> <select size='8' width='680px' style='width:680px' id='dg_select_records' ></select> </td> </tr> <tr> <td><input type='button' id='ir_dg_del' value='Delete' />&nbsp;&nbsp;<input type='button' id='ir_dg_edit' value='Edit' />&nbsp;&nbsp;&nbsp;&nbsp;</td> </tr>");
    	}
    	else if (ir_dg_type == "string"){
    		$('#irConfTable_tbody').append("<tr> <td> <label>String:</label> <input type='text' id='ir_dg_name' />(*required) </td> </tr><tr> <td> <label>Value:</label> <input type='text' id='ir_dg_value' /> </td> </tr><tr><td><input type='button' id='ir_add_btn' value='Add' />&nbsp;&nbsp;&nbsp;&nbsp;</td></tr> <tr> <td> <select size='8' width='680px' style='width:680px' id='dg_select_records' ></select> </td> </tr> <tr> <td><input type='button' id='ir_dg_del' value='Delete' />&nbsp;&nbsp;<input type='button' id='ir_dg_edit' value='Edit' />&nbsp;&nbsp;&nbsp;&nbsp;</td> </tr>");
    	}
    	else if (ir_dg_type == "integer"){
    		$('#irConfTable_tbody').append("<tr> <td> <label>Integer:</label> <input type='text' id='ir_dg_name' />(*required) </td> </tr><tr> <td> <label>Value&nbsp;&nbsp;&nbsp;:</label> <input type='text' id='ir_dg_value' /> </td> </tr><tr><td><input type='button' id='ir_add_btn' value='Add' />&nbsp;&nbsp;&nbsp;&nbsp;</td></tr> <tr> <td> <select size='8' width='680px' style='width:680px' id='dg_select_records' ></select> </td> </tr> <tr> <td><input type='button' id='ir_dg_del' value='Delete' />&nbsp;&nbsp;<input type='button' id='ir_dg_edit' value='Edit' />&nbsp;&nbsp;&nbsp;&nbsp;</td> </tr>");
    	}
    });
    
    // Event delegation to irConfTable_tbody 
    $('#irConfTable_tbody').on('click', '#ir_add_btn', function() {
    	
    	//alert("Add button clicked!");
    	var dg_name = $('#ir_dg_name').val();
    	var dg_val = $('#ir_dg_value').val();
    	
    	if (dg_name != '' && dg_val != '')
    		$('#dg_select_records').append('<option value="'+ dg_name + ':=' + dg_val +'">' + dg_name + ':=' + dg_val + '</option>');
		else if (dg_name != '' && dg_val == '')
			$('#dg_select_records').append('<option value="'+ dg_name + '">' + dg_name + '</option>');
		else
    		$('#ir_dg_name').focus();
    	
		$('#ir_dg_name').val('');
		$('#ir_dg_value').val('');
		$('#ir_dg_name').focus();

    });
    $('#irConfTable_tbody').on('click', '#ir_dg_edit', function() {
    	//alert("Edit button clicked! - ");
    	var dg_record = $('#dg_select_records option:selected').text();
    	//alert("selected Value: " + dg_record);
    	var arr = dg_record.split(":=");
    	var dg_name = arr[0];
    	var dg_value = arr[1];
        //alert("Name: " + arr[0] + " Value: " + arr[1]);
    	$('#ir_dg_name').val(dg_name);
    	$('#ir_dg_value').val(dg_value);
    	
    	$('#dg_select_records option').each(function() {
    		//alert("Option Value: " + $(this).val());
    		if ($(this).val() == dg_record){
    			$(this).remove();
    			//alert("Removed!");
    		}
    	});
    });
    
    $('#irConfTable_tbody').on('click', '#ir_dg_del', function() {
    	//alert("Delete button clicked! - " + this.id );
    	var dg_record = $('#dg_select_records option:selected').text();
    	
    	$('#dg_select_records option').each(function() {
    		//alert("Option Value: " + $(this).val());
    		if ($(this).val() == dg_record){
    			$(this).remove();
    			//alert("Removed!");
    		}
    	});
    	
    	//$("#dg_select_records option[value='"+dg_record+"']").remove();
    	
    });
    
    $('#ir_btn_build').on('click', function() {
    	//Dictionary Data fed from the form
    	var irData = {'phpFileName':'', 'DevIP':'', 'IrDgName':'', 'IrEnv':'', 'IrType':'', 'IrCode':'', 'IrDgType':'', 'IrDgData':''};
    	var bigipNameAndIP = $('#ltmSelBox option:selected').val();
    	//var bigipNameAndIP = $('#ltmSelBox').val()
    	var arr = bigipNameAndIP.split(":");
    	
    	var irType = $('#ir_type').val();
    	
    	// Data feed to irData
    	irData['phpFileName'] = 'new_irule_build';
    	irData['DevIP'] = arr[1];
    	irData['IrDgName'] = $('#ir_name').val();
    	irData['IrEnv'] = $('#ir_env').val();
    	irData['IrType'] = irType;
    	if (irType == 'iRule'){
    		irData['IrCode'] = $('#irConfCode').val();
    	}
    	if (irType == 'Data Group'){
    		var irRecords = '';
    		irData['IrDgType'] = $('#ir_dg_type_select').val();
    		var len = $('#dg_select_records option').length;
        	$('#dg_select_records option').each(function(index) {
        		irRecords += $(this).val();
        		//alert("Option Length: " + len + " index: " + index);
        		if(index != (len-1))
        			irRecords += ',';
        		//alert("Record: " + irRecords);
        	});
        	irData['IrDgData'] = irRecords;
    	}
    	
    	
    	var output = '';
    	$.each(irData, function(index) {	
    	    output = output + irData[index] + "\n";
    	});
    	alert("Data: " + output);
    	
    	
    	ajaxOut = buildIrAjax("new_irule_build", irData);
    	ajaxOut.done(buildIrProcessData);
    });
    
    $('#chg_ir_type').on('change', function(){
    	var ir_type = $('#chg_ir_type').val();
    	//alert("irType Val: " + ir_type);
    	if (ir_type == 'select'){
	   		$('#select_ir_dg_name').empty();
	   		$('#select_ir_dg_name').append("<option selected='selected'>Select...</option>")
	   		$('#ir_td_dg_type').empty();
	   		$('#ir_confTable_thead').empty();
	   		$('#irConfTable_tbody').empty();
    		return;
    	}
    	
    	if (ir_type == "iRule") {
    		$('#ir_td_dg_type').empty();
    		if (GetParentURLParameter('go') != 'del_irule'){
	    		$('#ir_confTable_thead').empty();
	    		$('#ir_confTable_thead').append("<th style='font-weight:normal' >iRule Code</th>");
	        	$('#irConfTable_tbody').empty();
	    		$('#irConfTable_tbody').append("<tr><td><textarea id='irConfCode' rows='10' cols='90'> </textarea> </td></tr>");
	   		}
    	}
    	else if (ir_type == "Data Group"){
    		$('#ir_td_dg_type').empty();
    		if (GetParentURLParameter('go') != 'del_irule'){
	    		$('#ir_confTable_thead').empty();
	    		$('#ir_confTable_thead').append("<th style='font-weight:normal'>Data Group Configuration</th>");
	    		$('#irConfTable_tbody').empty();
    		}
    		if (GetParentURLParameter('go') == 'new_irule')
    			$('#ir_td_dg_type').append("<label> DG Type: </label><select name='ir_dg_type_select' id='ir_dg_type_select' required='required' ><option selected='selected'>Select...</option><option>Address</option><option>String</option><option>Integer</option></select>");
    		else{
    			$('#ir_td_dg_type').append("<label> DG Type: </label><select name='ir_dg_type_select' id='ir_dg_type_select' disabled style='background-color: #E6E3E3;' required='required' ><option selected='selected'>Select...</option><option value='ip'>Address</option><option value='string'>String</option><option value='integer'>Integer</option></select>");
    			//$('#ir_td_dg_type').append("<label> DG Type: </label><select name='ir_dg_type_select' id='ir_dg_type_select' required='required' ><option selected='selected'>Select...</option><option value='ip'>Address</option><option value='string'>String</option><option value='integer'>Integer</option></select>");
    		}
    		
    	}
    	
    	// Loading existing iRule or Data Group names
    	// IrType - iRule or Data Group, IrDgPart - Partition name
    	var irData = {'phpFileName':'', 'DevIP':'', 'IrType':'', 'IrDgPart':'' };
    	var bigipNameAndIP = $('#ltmSelBox option:selected').val();
    	//var bigipNameAndIP = $('#ltmSelBox').val()
    	var arr = bigipNameAndIP.split(":");
    	
    	var irType = $('#chg_ir_type').val();
    	
    	// Data feed to irData
    	irData['phpFileName'] = 'load_irdg_names';
    	irData['DevIP'] = arr[1];
    	irData['IrType'] = irType;
    	irData['IrDgPart'] = 'Common';
    	
    	// Call Ajax to retrieve iRule or Data Group names
    	ajaxOut = $.ajax({
    		url: '/content/load_irdg_names.php',
    		type: 'POST',
    		dataType: 'JSON',
    		data: {'jsonIrData': JSON.stringify(irData)},
    		error: function(jqXHR, textStatus, errorThrown){
    			alert("Ajax call for retrieving iRule or Data Group names has failed!");
                console.log('jqXHR:');
                console.log(jqXHR);
                console.log('textStatus:');
                console.log(textStatus);
                console.log('errorThrown:');
                console.log(errorThrown);
    		}
    	});
    	ajaxOut.done(irdgNameLoadingProcess);
    });
    
   $('#select_ir_dg_name').on('change', function(){
	   	// Loading existing iRule or Data Group configuration
	   	// IrType - iRule or Data Group, IrDgPart - Partition name ("Common" all the time)
	   	var irData = {'phpFileName':'', 'DevIP':'', 'IrType':'', 'IrDgName':'', 'IrDgConfigMode':'' };
	   	var bigipNameAndIP = $('#ltmSelBox option:selected').val();
	   	//var bigipNameAndIP = $('#ltmSelBox').val()
	   	var arr = bigipNameAndIP.split(":");
	   	var irType = $('#chg_ir_type').val();

	   	// Reset selector and option value
	   	if($('#select_ir_dg_name').val() == 'select'){
	    	if (irType == "iRule") {
	    		$('#ir_td_dg_type').empty();
	    		if (GetParentURLParameter('go') != 'del_irule'){
		    		$('#ir_confTable_thead').empty();
		    		$('#ir_confTable_thead').append("<th style='font-weight:normal' >iRule Code</th>");
		        	$('#irConfTable_tbody').empty();
		    		$('#irConfTable_tbody').append("<tr><td><textarea id='irConfCode' rows='10' cols='90'> </textarea> </td></tr>");
	    		}
	    	}
	    	else if (irType == "Data Group"){
	    		$('#ir_td_dg_type').empty();
	    		if (GetParentURLParameter('go') != 'del_irule'){
		    		$('#ir_confTable_thead').empty();
		    		$('#ir_confTable_thead').append("<th style='font-weight:normal'>Data Group Configuration</th>");
		    		$('#irConfTable_tbody').empty();
	    		}
	    		if (GetParentURLParameter('go') == 'new_irule')
	    			$('#ir_td_dg_type').append("<label> DG Type: </label><select name='ir_dg_type_select' id='ir_dg_type_select' required='required' ><option selected='selected'>Select...</option><option>Address</option><option>String</option><option>Integer</option></select>");
	    		else if (GetParentURLParameter('go') == 'chg_irule') {
	    			$('#ir_td_dg_type').append("<label> DG Type: </label><select name='ir_dg_type_select' id='ir_dg_type_select' disabled style='background-color: #E6E3E3;' required='required' ><option selected='selected'>Select...</option><option value='ip'>Address</option><option value='string'>String</option><option value='integer'>Integer</option></select>");
	    			//$('#ir_td_dg_type').append("<label> DG Type: </label><select name='ir_dg_type_select' id='ir_dg_type_select' required='required' ><option selected='selected'>Select...</option><option value='ip'>Address</option><option value='string'>String</option><option value='integer'>Integer</option></select>");
	    		}
	    	}
	   		return;
	   	}
	   	
	   	// Data feed to irData
	   	irData['phpFileName'] = 'load_irdg_config';
	   	irData['DevIP'] = arr[1];
	   	irData['IrType'] = $('#chg_ir_type').val();
	   	irData['IrDgName'] = this.value;
	   	
	   	alert("iRule or Data Group: " + irData['IrType'] + "\nName: " + irData['IrDgName'] );
    	// Call Ajax to retrieve iRule or Data Group configuration
    	ajaxOut = $.ajax({
    		url: '/content/load_irdg_config.php',
    		type: 'POST',
    		dataType: 'JSON',
    		data: {'jsonIrData': JSON.stringify(irData)},
    		error: function(jqXHR, textStatus, errorThrown){
    			alert("Ajax call for retrieving iRule or Data Group configuration has failed!");
                console.log('jqXHR:');
                console.log(jqXHR);
                console.log('textStatus:');
                console.log(textStatus);
                console.log('errorThrown:');
                console.log(errorThrown);
    		}
    	});
    	ajaxOut.done(irdgConfigLoadingProcess);
   });
   
   // iRule/Data Group modification button click event handler
   $('#chg_ir_btn_build').on('click', function(){
   	//Dictionary Data fed from the form
   	var irData = {'phpFileName':'', 'DevIP':'', 'IrDgName':'', 'IrType':'', 'IrCode':'', 'IrDgType':'', 'IrDgData':''};
   	var bigipNameAndIP = $('#ltmSelBox option:selected').val();
   	var arr = bigipNameAndIP.split(":");
   	
   	var irType = $('#chg_ir_type').val();
   	
   	// Data feed to irData
   	irData['phpFileName'] = 'update_irdg_config';
   	irData['DevIP'] = arr[1];
   	irData['IrDgName'] = $('#select_ir_dg_name').val();
   	irData['IrType'] = irType;
   	if (irType == 'iRule'){
   		irData['IrCode'] = $('#irConfCode').val();
   	}
   	if (irType == 'Data Group'){
   		var irRecords = '';
   		irData['IrDgType'] = $('#ir_dg_type_select').val();
   		var len = $('#dg_select_records option').length;
       	$('#dg_select_records option').each(function(index) {
       		irRecords += $(this).val();
       		//alert("Option Length: " + len + " index: " + index);
       		if(index != (len-1))
       			irRecords += ',';
       		//alert("Record: " + irRecords);
       	});
       	irData['IrDgData'] = irRecords;
   	}
   	
   	
   	var output = '';
   	$.each(irData, function(index) {	
   	    output = output + irData[index] + "\n";
   	});
   	alert("Configuration Data\n" + output);
   	
	// Call Ajax to update iRule or Data Group configuration
	ajaxOut = $.ajax({
		url: '/content/update_irdg_config.php',
		type: 'POST',
		dataType: 'JSON',
		data: {'jsonIrData': JSON.stringify(irData)},
		error: function(jqXHR, textStatus, errorThrown){
			alert("Ajax call to update iRule or Data Group configuration has failed!");
            console.log('jqXHR:');
            console.log(jqXHR);
            console.log('textStatus:');
            console.log(textStatus);
            console.log('errorThrown:');
            console.log(errorThrown);
		}
	});
	ajaxOut.done(irdgConfigUpdateProcess);
   	
   	
   });
   
   // Event handler for when 'Delete iRule/DG' button is clicked.
   $('#del_ir_btn_build').on('click', function(){
	   	//Dictionary Data fed from the form
	   	var irData = {'phpFileName':'', 'DevIP':'', 'IrDgName':'', 'IrType':'', 'IrDgType':''};
	   	var bigipNameAndIP = $('#ltmSelBox option:selected').val();
	   	var arr = bigipNameAndIP.split(":");
	   	
	   	// Data feed to irData
	   	irData['phpFileName'] = 'del_irdg_ajax';
	   	irData['DevIP'] = arr[1];
	   	// 'IrType' - iRule or Data Group
	   	irData['IrType'] = $('#chg_ir_type').val();
	   	// 'IrDgName' - Actual iRule or Data Group Name
	   	irData['IrDgName'] = $('#select_ir_dg_name').val();
	   	
	   	if (irData['IrType'] == 'Data Group'){
		   	// 'IrDgType' - Data Group Data Type ip | string | integer
		   	irData['IrDgType'] = $('#ir_dg_type_select').val();
	   	}
	   	
	   	//alert("Dev IP: " + irData['DevIP'] + "\niRule/DG: " + irData['IrType'] + "\niRule/DG Name: " + irData['IrDgName'] + "\nData Group Type: " + irData['IrDgType']);
		// Call Ajax to delete a chosen iRule or Data Group
		ajaxOut = $.ajax({
			url: '/content/del_irdg_ajax.php',
			type: 'POST',
			dataType: 'JSON',
			data: {'jsonData': JSON.stringify(irData)},
			error: function(jqXHR, textStatus, errorThrown){
				alert("Ajax call to delete iRule or Data Group has failed!");
	            console.log('jqXHR:');
	            console.log(jqXHR);
	            console.log('textStatus:');
	            console.log(textStatus);
	            console.log('errorThrown:');
	            console.log(errorThrown);
			}
		});
		ajaxOut.done(delIrdgProcess);
   });
   
});