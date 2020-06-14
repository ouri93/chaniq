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

function getPoolMonAjax(phpFileName, bigipName, bigipIP, monType) {
  	return $.ajax({
  		url: '/content/get_pool_monitors.php',
   		type: 'POST',
   		data: {method: phpFileName, DevName: bigipName, DevIP: bigipIP, LoadTypeName: monType}
   	});
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
	var configMode = GetParentURLParameter('go');
	
	var monType = '';
	if (configMode == 'new_monitor')
		monType = $('#m_type').val();
	//else if(configMode == 'chg_monitor'){
	else {
		monType = $('#chg_m_type').val();
		$('#m_desc').val(response_in['description']);
		if (response_in['defaultsFrom'] != ''){
			var parMonName = response_in['defaultsFrom'].split('/');
			$('#chg_m_type_parent').append('<option value='+ parMonName[2] + ' text=' + parMonName[2] + '>' + parMonName[2] + '</option>');
		}
	}
	
	if (configMode != 'del_monitor') setMonHtml(monType, response_in);
}

function getMonSettingsAjax(phpFileName, bigipName, bigipIP, monType, parMonType)
{
	//alert("getMonSettingsAjax - phpFileName: " + phpFileName + " Dev name: " + bigipName + " Dev IP: " + bigipIP + " Mon Type: " + monType + " Parent Monitor: " + parMonType);
	return $.ajax({ 
		url: '/content/get_healthmon_settings.php',
		type: 'POST',
		dataType: 'JSON',
		data: {phpFile: phpFileName, DevIP:bigipIP, MonType: monType, ParMonType:parMonType},
		error: function(jqXHR, textStatus, errorThrown){
			alert("Ajax call for retrieving monitor settings has failed!");
            console.log('jqXHR:');
            console.log(jqXHR);
            console.log('textStatus:');
            console.log(textStatus);
            console.log('errorThrown:');
            console.log(errorThrown);
		}
	});
}

function buildMonAjax(phpFileName, monData){
	return $.ajax({
		url: '/content/new_monitor_build.php',
		type: 'POST',
		dataType: 'JSON',
		data: {'jsonMonData': JSON.stringify(monData)},
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

function buildMonProcessData(response_in) {
	var strResult = '';
	$.each(response_in, function(index) {
		if(index == 0) 
			strResult = "<b>" + response_in[index] + "</b><br>";
		else
			strResult += response_in[index] + "<br>";
	});
	
	//alert("Return output: " + strResult);
	$('#newMon_EvalReview').html(strResult);
}

function chgMonProcessData(response_in) {
	var strResult = '';
	$.each(response_in, function(index) {
		if(index == 0) 
			strResult = "<b>" + response_in[index] + "</b><br>";
		else
			strResult += response_in[index] + "<br>";
	});
	
	//alert("Return output: " + strResult);
	$('#newMon_EvalReview').html(strResult);
}

// Process the return data of deleting Health monitors from BIG-IP
function delMonProcessData(response_in){
	var strResult = '';
	$.each(response_in, function(index) {
		if(index == 0) 
			strResult = "<b>" + response_in[index] + "</b><br>";
		else
			strResult += response_in[index] + "<br>";
	});
	
	//alert("Return output: " + strResult);
	$('#newMon_EvalReview').html(strResult);
}

function getMonHtml(devIp, monType)
{
	// Update html code by Monitor type - HTTP, HTTPS, TCP, UDP, TCP Half Open, ICMP, External
	// Bit 0 - Interval (0000 0001), Bit 1 - Timeout (0000 0010), Bit 2 - Send String (0000 0100), Bit 3 - Receive String (0000 1000)
	// Bit 4 - Username/Password (0001 0000), Bit 5 - Reverse (0010 0000), Bit 6 - Alias Service Port (0100 0000), Bit 7 - Cipher List (1000 0000) 
	// Big 8 - External Program and Arguments (0001 0000 0000)
	// HTTP - 0111 1111(127), HTTPS - 1111 1111(255), TCP and UDP - 0110 1111(111), TCP Half Open - 0100 0011(67), ICMP - 0000 0011(3), External - 0001 0100 0011(323)
	var strHtml = '';
	var htmlCode = 0;
	switch (monType)
	{
	case 'ICMP':
		htmlCode = 3;
		break;
	case 'TCP Half Open':
		htmlCode = 67;
		break;
	case 'TCP':
	case 'UDP':
		htmlCode = 111;
		break;
	case 'HTTP':
		htmlCode = 127;
		break;
	case 'HTTPS':
		htmlCode = 255;
		break;
	case 'External':
		htmlCode = 323;
		break;
	}
	//alert("Chosen HtmlCode: " + htmlCode);
	
	switch(true)
	{
	case (((htmlCode >> 0) & 1) == 1):
		if(((htmlCode >> 0) & 1) == 1) {
			strHtml += "<tr><td><label> Interval: </label></td><td><input type='text' id='monConfInterval' value='5' /> Seconds</td></tr>";
		}
	case (((htmlCode >> 1) & 1) == 1):
		if(((htmlCode >> 1) & 1) == 1) {
			strHtml += "<tr><td><label> Timeout: </label></td><td><input type='text' id='monConfTimeout' value='16' /> Seconds</td></tr>";
		}
	case (((htmlCode >> 2) & 1) == 1):
		if(((htmlCode >> 2) & 1) == 1) {
			strHtml += "<tr><td><label> Send String: </label></td><td><textarea id='monConfSndString' rows='5' cols='50'> </textarea> </td></tr>";
		}
	case (((htmlCode >> 3) & 1) == 1):
		if(((htmlCode >> 3) & 1) == 1) {
			strHtml += "<tr><td><label> Receive String: </label></td><td><textarea id='monConfRcvString' rows='5' cols='50'> </textarea> </td></tr>";
		}
	case (((htmlCode >> 4) & 1) == 1):
		if(((htmlCode >> 4) & 1) == 1) { 	
			strHtml += "<tr><td><label> User Name: </label></td><td><input type='text' id='monConfUN' /></td></tr>";
			strHtml += "<tr><td><label> Password: </label></td><td><input type='password' id='monConfPW' /> </td></tr>";
		}
	case (((htmlCode >> 5) & 1) == 1):
		if(((htmlCode >> 5) & 1) == 1) {
			strHtml += "<tr><td><label> Reverse: </label></td><td><label>Yes</label><input type='radio' id='monConfRvsYes' name='reverse' ><label>No</label><input type='radio' id='monConfRvsNo' name='reverse' checked /></td></tr>";
		}
	case (((htmlCode >> 6) & 1) == 1):
		if(((htmlCode >> 6) & 1) == 1) {
			strHtml += "<tr><td><label> Alias Service Port: </label></td><td><input type='text' id='monConfAliasPort' value='*'/></td></tr>";
		}
	case (((htmlCode >> 7) & 1) == 1):
		if(((htmlCode >> 7) & 1) == 1) {
			strHtml += "<tr><td><label> Cipher List: </label></td><td><input type='text' id='monConfCipher' value='DEFAULT:+SHA:+3DES:+kEDH' /></td></tr>";
		}
	case (((htmlCode >> 8) & 1) == 1):
		;
	default:
		break;
	}
	
	return strHtml;
}

function setMonHtml(monType, response_in)
{
	// Update html code by Monitor type - HTTP, HTTPS, TCP, UDP, TCP Half Open, ICMP, External
	// Bit 0 - Interval (0000 0001), Bit 1 - Timeout (0000 0010), Bit 2 - Send String (0000 0100), Bit 3 - Receive String (0000 1000)
	// Bit 4 - Username/Password (0001 0000), Bit 5 - Reverse (0010 0000), Bit 6 - Alias Service Port (0100 0000), Bit 7 - Cipher List (1000 0000) 
	// Big 8 - External Program and Arguments (0001 0000 0000)
	// HTTP - 0111 1111(127), HTTPS - 1111 1111(255), TCP and UDP - 0110 1111(111), TCP Half Open - 0100 0011(67), ICMP - 0000 0011(3), External - 0001 0100 0011(323)
	var strHtml = '';
	var htmlCode = 0;
	switch (monType)
	{
	case 'ICMP':
		htmlCode = 3;
		break;
	case 'TCP Half Open':
		htmlCode = 67;
		break;
	case 'TCP':
	case 'UDP':
		htmlCode = 111;
		break;
	case 'HTTP':
		htmlCode = 127;
		break;
	case 'HTTPS':
		htmlCode = 255;
		break;
	case 'External':
		htmlCode = 323;
		break;
	}
	//alert("Chosen HtmlCode: " + htmlCode);
	
	switch(true)
	{
	case (((htmlCode >> 0) & 1) == 1):
		if(((htmlCode >> 0) & 1) == 1) {
			$('#monConfInterval').val(response_in['interval']);
		}
	case (((htmlCode >> 1) & 1) == 1):
		if(((htmlCode >> 1) & 1) == 1) {
			$('#monConfTimeout').val(response_in['timeout']);
		}
	case (((htmlCode >> 2) & 1) == 1):
		if(((htmlCode >> 2) & 1) == 1) {
			$('#monConfSndString').val(response_in['send']);
		}
	case (((htmlCode >> 3) & 1) == 1):
		if(((htmlCode >> 3) & 1) == 1) {
			$('#monConfRcvString').val(response_in['recv']);
		}
	case (((htmlCode >> 4) & 1) == 1):
		if(((htmlCode >> 4) & 1) == 1) { 	
			$('#monConfUN').val(response_in['username']);
			$('#monConfPW').val(response_in['password']);
		}
	case (((htmlCode >> 5) & 1) == 1):
		if(((htmlCode >> 5) & 1) == 1) {
			if(response_in['reverse'] == "enabled"){
				//alert("Reverse enabled!");
				$('#monConfRvsYes').prop("checked", true);
			}
			else{
				//alert("Reverse disabled!");
				$('#monConfRvsNo').prop("checked", true);	
			}
		}
	case (((htmlCode >> 6) & 1) == 1):
		if(((htmlCode >> 6) & 1) == 1) {
			$('#monConfAliasPort').val(response_in['aliasPort']);
		}
	case (((htmlCode >> 7) & 1) == 1):
		if(((htmlCode >> 7) & 1) == 1) {
			$('#monConfCipher').val(response_in['cipherlist']);
		}
	case (((htmlCode >> 8) & 1) == 1):
		;
	default:
		break;
	}
	
	return strHtml;
}

// Process Health monitor names returned from BIG-IP
function HealthMonNamesProcess(response_in, monType){
	/* Debugging - Print out returned health monitor names
	var strResult = '';
	$.each(response_in, function(index) {
		if(index == 0) 
			strResult = "<b>" + response_in[index] + "</b><br>";
		else
			strResult += response_in[index] + "<br>";
	});
	
	$('#newMon_EvalReview').html(strResult);
	*/
	$.each(response_in, function(index) {
		var builtins={'HTTP':'http, http_head_f5', 'HTTPS':'https, https_443, https_head_f5', 'ICMP':'icmp', 'INBAND':'inband', 'REAL SERVER':'real_server', 'SNMP DCA':'snmp_dca', 'TCP':'tcp', 'TCP ECHO':'tch_echo', 'TCP Half Open':'tcp_half_open', 'UDP':'udp'};
		// Remove special character at the end such as whitespace at the beginning or end, newlines
		var strResponse = (response_in[index]).trim();

		if (builtins[monType].search(strResponse) == -1 )
   			$('#select_mon_name').append('<option> ' + response_in[index] + '</option>');
	});
}

$(function () {
	$('#div_ltmchoice').on('change', function() {
		var nameAndIp = $('#ltmSelBox option:selected').val();
		if (nameAndIp == 'Select...') return;

		var arr = nameAndIp.split(":");

	});
	
    // Evnet handler for Monitor type change - Once Parent Monitor data is retrived, the data is fed into Paraent Monitor
    $('#m_type').on('change', function() {
    	var bigipNameAndIP = $('#ltmSelBox').val();
    	// arr[0] - BIG-IP Device Name, arr[1] - BIG-IP Device IP address
    	var arr = bigipNameAndIP.split(":");
   		var monType = $('#m_type').val();
    	    	
		// Call Ajax to get all available Pool monitors from the device
		ajaxOut = getPoolMonAjax("get_pool_monitors", arr[0], arr[1], monType);
		ajaxOut.done(MonProcessData);
    	
    	// Update html code by Monitor type - HTTP, HTTPS, TCP, UDP, TCP Half Open, ICMP, External    	
    	var strMonitorHtml = getMonHtml(arr[1], monType);
       	
    	$('#monConfTable_tbody').empty();
    	$('#monConfTable_tbody').append(strMonitorHtml);

    });
    
    // Fill in the dynamic Monitor form
    $('#m_type_parent').on('change', function() {
    	var bigipNameAndIP = $('#ltmSelBox').val();
    	// arr[0] - BIG-IP Device Name, arr[1] - BIG-IP Device IP address
    	var arr = bigipNameAndIP.split(":");
    	var monType = $('#m_type').val();
    	var parMonType = $('#m_type_parent').val();
    	
    	//alert ("Parent Monitor: " + parMonType);
    	
    	// Call Ajax to get all available Pool monitors from the device
    	//alert("Calling get_healthmon_settings Ajax - Dev Name: " + arr[0] + " Dev IP: " + arr[1] + " Monitor Type: " + monType + "Parent Monitor: " + parMonType);
    	ajaxOut = getMonSettingsAjax("get_healthmon_settings", arr[0], arr[1], monType, parMonType);
    	ajaxOut.done(MonSettingsProcessData);
    });

    //Submit "Deploy Monitor"
    $('#btn_newMonBuild').click( function() {
    	//Dictionary Data fed from the form
    	var monData = {'phpFileName':'', 'DevIP':'', 'MonName':'', 'MDesc':'', 'MEnv':'', 'MMonType':'', 'MMonCode':'', 'MParMonType':'', 'interval':'', 'timeout':'', 'send':'', 'recv':'', 'username':'', 'password':'', 'reverse':'', 'aliasPort':'', 'cipherlist':''};
    	var bigipNameAndIP = $('#ltmSelBox').val()
    	var arr = bigipNameAndIP.split(":");
    	
    	monData['phpFileName'] = 'new_monitor_build';
    	monData['DevIP'] = arr[1];
    	monData['MonName'] = $('#m_name').val();
    	monData['MDesc'] = $('#m_desc').val();
    	monData['MEnv'] = $('#p_env').val();
    	monData['MMonType'] = $('#m_type').val();
    	monData['MParMonType'] = $('#m_type_parent').val();
    	
    	// Update html code by Monitor type - HTTP, HTTPS, TCP, UDP, TCP Half Open, ICMP, External
    	// Bit 0 - Interval (0000 0001), Bit 1 - Timeout (0000 0010), Bit 2 - Send String (0000 0100), Bit 3 - Receive String (0000 1000)
    	// Bit 4 - Username/Password (0001 0000), Bit 5 - Reverse (0010 0000), Bit 6 - Alias Service Port (0100 0000), Bit 7 - Cipher List (1000 0000) 
    	// Big 8 - External Program and Arguments (0001 0000 0000)
    	// HTTP - 0111 1111(127), HTTPS - 1111 1111(255), TCP and UDP - 0110 1111(111), TCP Half Open - 0100 0011(67), ICMP - 0000 0011(3), External - 0001 0100 0011(323)
    	var strHtml = '';
    	var htmlCode = 0;
    	switch ($('#m_type').val())
    	{
    	case 'ICMP':
    		htmlCode = 3;
    		break;
    	case 'TCP Half Open':
    		htmlCode = 67;
    		break;
    	case 'TCP':
    	case 'UDP':
    		htmlCode = 111;
    		break;
    	case 'HTTP':
    		htmlCode = 127;
    		break;
    	case 'HTTPS':
    		htmlCode = 255;
    		break;
    	case 'External':
    		htmlCode = 323;
    		break;
    	}
    	monData['MMonCode'] = htmlCode.toString();
    	//alert("Chosen HtmlCode: " + htmlCode);
    	
    	switch(true)
    	{
    	case (((htmlCode >> 0) & 1) == 1):
    		if(((htmlCode >> 0) & 1) == 1) {
    			monData['interval'] = $('#monConfInterval').val();
    		}
    	case (((htmlCode >> 1) & 1) == 1):
    		if(((htmlCode >> 1) & 1) == 1) {
    			monData['timeout']= $('#monConfTimeout').val();
    		}
    	case (((htmlCode >> 2) & 1) == 1):
    		if(((htmlCode >> 2) & 1) == 1) {
    			monData['send']= $('#monConfSndString').val();
    		}
    	case (((htmlCode >> 3) & 1) == 1):
    		if(((htmlCode >> 3) & 1) == 1) {
    			monData['recv']= $('#monConfRcvString').val();
    		}
    	case (((htmlCode >> 4) & 1) == 1):
    		if(((htmlCode >> 4) & 1) == 1) { 	
    			monData['username']= $('#monConfUN').val();
    			monData['password']= $('#monConfPW').val();
    		}
    	case (((htmlCode >> 5) & 1) == 1):
    		if(((htmlCode >> 5) & 1) == 1) {
    			if ($('#monConfRvsYes').prop("checked") )
    				monData['reverse'] = 'enabled';
    			else
    				monData['reverse'] = 'disabled';
    		}
    	case (((htmlCode >> 6) & 1) == 1):
    		if(((htmlCode >> 6) & 1) == 1) {
    			monData['aliasPort'] = $('#monConfAliasPort').val();
    		}
    	case (((htmlCode >> 7) & 1) == 1):
    		if(((htmlCode >> 7) & 1) == 1) {
    			monData['cipherlist'] = $('#monConfCipher').val();
    		}
    	case (((htmlCode >> 8) & 1) == 1):
    		;
    	default:
    		break;
    	}
    	
    	/*
    	var output;
    	$.each(monData, function(index) {	
    	    output = output + monData[index] + "\n";
    	});
    	alert("Data: " + output);
    	*/
    	
    	ajaxOut = buildMonAjax("new_monitor_build", monData);
    	ajaxOut.done(buildMonProcessData);
    });
    
    // Event handler for Monitor Type change
    $('#chg_m_type').on('change', function(){
    	if(this.value == 'select') return;

    	// Reset monitor name, Description, and parent monitor
    	$('#select_mon_name').empty();
    	$('#select_mon_name').append('<option value="select" selected="selected">Select...</option>');
    	$('#m_desc').val('');
    	$('#chg_m_type_parent').empty();

    	// Load monitor names
    	var monData = {'phpFileName':'', 'DevIP':'', 'MonType':'', 'MonPart':'' };
    	var bigipNameAndIP = $('#ltmSelBox').val();
    	// arr[0] - BIG-IP Device Name, arr[1] - BIG-IP Device IP address
    	var arr = bigipNameAndIP.split(":");
    	var monType = $('#chg_m_type').val();
    	
    	// Data feed to irData
    	monData['phpFileName'] = 'get_healthmon_names';
    	monData['DevIP'] = arr[1];
    	monData['MonType'] = monType;
    	monData['MonPart'] = 'Common';
    	
    	// Call Ajax to retrieve Health Monitor names
    	ajaxOut = $.ajax({
    		url: '/content/get_healthmon_names.php',
    		type: 'POST',
    		dataType: 'JSON',
    		data: {'jsonData': JSON.stringify(monData)},
    		error: function(jqXHR, textStatus, errorThrown){
    			alert("Ajax call for retrieving Health Monitor names has failed!");
                console.log('jqXHR:');
                console.log(jqXHR);
                console.log('textStatus:');
                console.log(textStatus);
                console.log('errorThrown:');
                console.log(errorThrown);
    		}
    	});
    	ajaxOut.done(function(response_in){
    		HealthMonNamesProcess(response_in, monType);
    	});
    	
    });
    
    // Event handler for when Monitor name has been changed
    $('#select_mon_name').on('change', function(){

    	if(this.value == 'select') return;
    	if($('#chg_m_type').val() == 'select') return;
    	
    	// Reset monitor Description and parent monitor
    	$('#m_desc').val('');
    	$('#chg_m_type_parent').empty();
    	
    	var bigipNameAndIP = $('#ltmSelBox').val();
    	// arr[0] - BIG-IP Device Name, arr[1] - BIG-IP Device IP address
    	var arr = bigipNameAndIP.split(":");
   		var monType = $('#chg_m_type').val();
   		// parMonType variable is used to store Health monitor name under chg_monitor configuration mode
   		var parMonType = this.value;
    	
   		// 1. Build health monitor form according to a given monitor name
    	// Update html code by Monitor type - HTTP, HTTPS, TCP, UDP, TCP Half Open, ICMP, External
   		if (GetParentURLParameter('go') != 'del_monitor'){
	    	var strMonitorHtml = getMonHtml(arr[1], monType);
	       	
	    	$('#monConfTable_tbody').empty();
	    	$('#monConfTable_tbody').append(strMonitorHtml);
   		}
   		
   		// 2. Read health monitor config from BIG-IP and feed the config data to the built form
    	//alert("getMonSettingsAjax - phpFileName: " + phpFileName + " Dev name: " + bigipName + " Dev IP: " + bigipIP + " Mon Type: " + monType + " Parent Monitor: " + parMonType);
    	ajaxOut = getMonSettingsAjax("get_healthmon_settings", arr[0], arr[1], monType, parMonType);
    	ajaxOut.done(MonSettingsProcessData);
    	
    });
    
    // Event handler for when 'Modify Monitor' button click event is fired
    $('#btn_chgMonBuild').on('click', function(){
    	//Dictionary Data fed from the form
    	var monData = {'phpFileName':'', 'DevIP':'', 'MonName':'', 'MDesc':'', 'MMonType':'', 'MMonCode':'', 'MParMonType':'', 'interval':'', 'timeout':'', 'send':'', 'recv':'', 'username':'', 'password':'', 'reverse':'', 'aliasPort':'', 'cipherlist':''};
    	var bigipNameAndIP = $('#ltmSelBox').val()
    	var arr = bigipNameAndIP.split(":");
    	
    	monData['phpFileName'] = 'chg_monitor_config';
    	monData['DevIP'] = arr[1];
    	monData['MonName'] = $('#select_mon_name').val();
    	monData['MDesc'] = $('#m_desc').val();
    	monData['MMonType'] = $('#chg_m_type').val();
    	monData['MParMonType'] = $('#chg_m_type_parent').val();
    	
    	// Client site process to avoid modifying builtin profiles
    	// BIG-IP 12.1.2 HF1 Builtin Monitor list
    	var builtins={'HTTP':'http, http_head_f5', 'HTTPS':'https, https_443, https_head_f5', 'ICMP':'icmp', 'INBAND':'inband', 'REAL SERVER':'real_server', 'SNMP DCA':'snmp_dca', 'TCP':'tcp', 'TCP ECHO':'tch_echo', 'TCP Half Open':'tcp_half_open', 'UDP':'udp'};
    	if (builtins[monData['MMonType']].search(monData['MonName']) >= 0){
    		alert("BuiltIn Monitor (" + monData['MonName'] + " ) is not editable!");
    		return;
    	}
    	// Update html code by Monitor type - HTTP, HTTPS, TCP, UDP, TCP Half Open, ICMP, External
    	// Bit 0 - Interval (0000 0001), Bit 1 - Timeout (0000 0010), Bit 2 - Send String (0000 0100), Bit 3 - Receive String (0000 1000)
    	// Bit 4 - Username/Password (0001 0000), Bit 5 - Reverse (0010 0000), Bit 6 - Alias Service Port (0100 0000), Bit 7 - Cipher List (1000 0000) 
    	// Big 8 - External Program and Arguments (0001 0000 0000)
    	// HTTP - 0111 1111(127), HTTPS - 1111 1111(255), TCP and UDP - 0110 1111(111), TCP Half Open - 0100 0011(67), ICMP - 0000 0011(3), External - 0001 0100 0011(323)
    	var strHtml = '';
    	var htmlCode = 0;
    	switch ($('#chg_m_type').val())
    	{
    	case 'ICMP':
    		htmlCode = 3;
    		break;
    	case 'TCP Half Open':
    		htmlCode = 67;
    		break;
    	case 'TCP':
    	case 'UDP':
    		htmlCode = 111;
    		break;
    	case 'HTTP':
    		htmlCode = 127;
    		break;
    	case 'HTTPS':
    		htmlCode = 255;
    		break;
    	case 'External':
    		htmlCode = 323;
    		break;
    	}
    	monData['MMonCode'] = htmlCode.toString();
    	//alert("Chosen HtmlCode: " + htmlCode);
    	
    	switch(true)
    	{
    	case (((htmlCode >> 0) & 1) == 1):
    		if(((htmlCode >> 0) & 1) == 1) {
    			monData['interval'] = $('#monConfInterval').val();
    		}
    	case (((htmlCode >> 1) & 1) == 1):
    		if(((htmlCode >> 1) & 1) == 1) {
    			monData['timeout']= $('#monConfTimeout').val();
    		}
    	case (((htmlCode >> 2) & 1) == 1):
    		if(((htmlCode >> 2) & 1) == 1) {
    			monData['send']= $('#monConfSndString').val();
    		}
    	case (((htmlCode >> 3) & 1) == 1):
    		if(((htmlCode >> 3) & 1) == 1) {
    			monData['recv']= $('#monConfRcvString').val();
    		}
    	case (((htmlCode >> 4) & 1) == 1):
    		if(((htmlCode >> 4) & 1) == 1) { 	
    			monData['username']= $('#monConfUN').val();
    			monData['password']= $('#monConfPW').val();
    		}
    	case (((htmlCode >> 5) & 1) == 1):
    		if(((htmlCode >> 5) & 1) == 1) {
    			if ($('#monConfRvsYes').prop("checked") )
    				monData['reverse'] = 'enabled';
    			else
    				monData['reverse'] = 'disabled';
    		}
    	case (((htmlCode >> 6) & 1) == 1):
    		if(((htmlCode >> 6) & 1) == 1) {
    			monData['aliasPort'] = $('#monConfAliasPort').val();
    		}
    	case (((htmlCode >> 7) & 1) == 1):
    		if(((htmlCode >> 7) & 1) == 1) {
    			monData['cipherlist'] = $('#monConfCipher').val();
    		}
    	case (((htmlCode >> 8) & 1) == 1):
    		;
    	default:
    		break;
    	}
    	
    	
    	var output ='';
    	$.each(monData, function(index) {	
    	    output = output + monData[index] + "\n";
    	});
    	//alert("Data: " + output);
    	
    	ajaxOut = $.ajax({
    		url: '/content/chg_monitor_config.php',
    		type: 'POST',
    		dataType: 'JSON',
    		data: {'jsonMonData': JSON.stringify(monData)},
    		error: function(jqXHR, textStatus, errorThrown){
    			alert("Ajax call for updating Health Monitor configruation has failed!");
                console.log('jqXHR:');
                console.log(jqXHR);
                console.log('textStatus:');
                console.log(textStatus);
                console.log('errorThrown:');
                console.log(errorThrown);
    		}
    	});
    	
    	ajaxOut.done(chgMonProcessData);
    });
    
    // Event handler when Delete Health monitor button clicked.
    $('#btn_delMonBuild').on('click', function(){
    	//Dictionary Data fed from the form
    	var monData = {'phpFileName':'', 'DevIP':'', 'MonName':'', 'MDesc':'', 'MMonType':'', 'MParMonType':''};
    	var bigipNameAndIP = $('#ltmSelBox').val()
    	var arr = bigipNameAndIP.split(":");
    	
    	monData['phpFileName'] = 'del_monitor_ajax';
    	monData['DevIP'] = arr[1];
    	monData['MonName'] = $('#select_mon_name').val();
    	monData['MDesc'] = $('#m_desc').val();
    	monData['MMonType'] = $('#chg_m_type').val();
    	monData['MParMonType'] = $('#chg_m_type_parent').val();
    	
    	// ajax call to delete a given health monitor
    	ajaxOut = $.ajax({
    		url: '/content/del_monitor_ajax.php',
    		type: 'POST',
    		dataType: 'JSON',
    		data: {'jsonData': JSON.stringify(monData)},
    		error: function(jqXHR, textStatus, errorThrown){
    			alert("Ajax call to delete a Health Monitor has failed!");
                console.log('jqXHR:');
                console.log(jqXHR);
                console.log('textStatus:');
                console.log(textStatus);
                console.log('errorThrown:');
                console.log(errorThrown);
    		}
    	});
    	
    	ajaxOut.done(delMonProcessData);
    });
    
});