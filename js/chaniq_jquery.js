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
   		data: {method: phpFileName, DevName: bigipName, DevIP: bigipIP, MonType: monType}
   	});
}

function PprocessData(response_in)
{
   	var response = JSON.parse(response_in);
   	//alert("In ProcessData" + response[0]);

   	$.each(response, function(index){
   		$('#p_mon').append('<option value=' + response[index] + ' text=' + response[index] + '>' + response[index] + '</option>');
   	});
}

function PMprocessData(response_in)
{
   	var response = JSON.parse(response_in);
   	//alert("In ProcessData" + response[0]);

   	$.each(response, function(index){
   		$('#pm_mon').append('<option value=' + response[index] + ' text=' + response[index] + '>' + response[index] + '</option>');
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

function buildNewPoolAjax(phpFileName, arr, pVsName, pVsPort, pMon, pEnv, pLBMethod, pPriGroup, pPriGroupLessThan, pmPoolMemberName, pmPoolMemberIp, pmPoolMemberPort, pmPoolMemberMon, pmPriGroup)
{

	//alert(arr[1] + ":"+ pVsName + ":"+ pVsPort + ":"+ pMon + ":"+ pEnv + ":" + pLBMethod + ":"+ pPriGroup + ":"+ pPriGroupLessThan + ":" + pmPoolMemberName + ":"+ pmPoolMemberIp +":" + pmPoolMemberPort + ":" + pmPoolMemberMon + ":" + pmPriGroup);
  	return $.ajax({
  		url: 'content/new_pool_build.php',
   		type: 'POST',
   		dataType: 'JSON',
   		data: {phpFile: phpFileName, DevIP: arr[1], PVsName: pVsName, PVsPort: pVsPort, PMon: pMon, PEnv: pEnv, PLBMethod: pLBMethod, PPriGroup: pPriGroup, PPriGroupLessThan: pPriGroupLessThan, PmPoolMemberNmae: pmPoolMemberName, PmPoolMemberIp: pmPoolMemberIp, PmPoolMemberPort: pmPoolMemberPort, PmPoolMemberMon: pmPoolMemberMon, PmPrigroup: pmPriGroup }
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

function buildMonAjax(phpFileName, monData){
	return $.ajax({
		url: 'content/new_monitor_build.php',
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

function buildIrAjax(phpFileName, irData) {
	//alert(monData['interval'] + ":" + monData['send']);
	return $.ajax({
		url: 'content/new_irule_build.php',
		type: 'POST',
		dataType: 'JSON',
		data: {'jsonIrData': JSON.stringify(irData)},
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
    $('#btnRight').click(function (e) {
        var selectedOpts = $('#lstBox1 option:selected');
        if (selectedOpts.length == 0) {
            alert("Nothing to move.");
            e.preventDefault();
        }

        $('#lstBox2').append($(selectedOpts).clone());
        $(selectedOpts).remove();
        e.preventDefault();
    });

    $('#btnLeft').click(function (e) {
        var selectedOpts = $('#lstBox2 option:selected');
        if (selectedOpts.length == 0) {
            alert("Nothing to move.");
            e.preventDefault();
        }

        $('#lstBox1').append($(selectedOpts).clone());
        $(selectedOpts).remove();
        e.preventDefault();
    });
    
    /* Ajax Ref: https://www.youtube.com/watch?v=G9jz9mdblgs 
     * if you specify change() event, it won't fire as there is no option value initially.
     * Here we use .one() method which guarantee to be executed only once with the specified event.
     * Once Pool monitors are gathered from BIG-IP, add them to select and 
     * call Pool member monitor click event to add them there.
     * */
    $('#p_mon').one('click', function() {
    	//alert("Select has been changed");
    	var bigipNameAndIP = $('#ltmSelBox').val()
    	// arr[0] - BIG-IP Device Name, arr[1] - BIG-IP Device IP address
    	var arr = bigipNameAndIP.split(":");
    	
    	// Call Ajax to get all available Pool monitors from the device
    	ajaxOut = getPoolMonAjax("get_pool_monitors", arr[0], arr[1], "ALL");
    	ajaxOut.done(PprocessData);
    	$('#pm_mon').trigger('click');

    });
    
    $('#pm_mon').one('click', function() {
    //$('#pm_td').on('click', 'select', function() {
    	//alert("Select has been changed");
    	var bigipNameAndIP = $('#ltmSelBox').val();
    	// arr[0] - BIG-IP Device Name, arr[1] - BIG-IP Device IP address
    	var arr = bigipNameAndIP.split(":");
    	
    	// Call Ajax to get all available Pool monitors from the device
    	ajaxOut = getPoolMonAjax("get_pool_monitors", arr[0], arr[1], "ALL");
    	ajaxOut.done(PMprocessData);
    	//$('#pm_td').off('click');

    });

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
    	var pmPoolMemberMon = document.getElementsByClassName('pm_mon');
    	var pmPriGroup = document.getElementsByClassName('pm_pg_val');
    	
    	var arrayLen = pmPoolMemberName.length;
    	
    	// Build parameter data format for array type - e.g. pool_membername is the string array. Change the array to a single string using ":" as a delimiter.
    	// Array = [srv1.xyz.com, srv2.xyz.com, srv3.xyz.com] => "srv1.xyz.com:srv2.xyz.com:srv3.xyz.com"
    	
    	//alert("Array Length: " + arrayLen);
    	var strPmPoolMemberName = '';
    	var strPmPoolMemberIp = '';
    	var strPmPoolMemberPort = '';
    	var strPmPoolMemberMon = '';
    	var strPmPriGroup = '';
    	
    	for(i=0;i<arrayLen;i++){
    		strPmPoolMemberName += pmPoolMemberName[i].value + ":";
    		strPmPoolMemberIp += pmPoolMemberIp[i].value + ":";
    		strPmPoolMemberPort += pmPoolMemberPort[i].value + ":";
    		strPmPoolMemberMon += pmPoolMemberMon[i].value + ":";
    		strPmPriGroup += pmPriGroup[i].value + ":";
    	}
    	//alert(bigipNameAndIP + ":" + arr[1] + ":"+ pVsName + ":"+ pVsPort + ":"+ pMon + ":"+ pEnv + ":" + pLBMethod + ":"+ pPriGroup + ":"+ pPriGroupLessThan + ":" + strPmPoolMemberName + ":" + strPmPoolMemberIp + ":" + strPmPoolMemberPort + ":" + strPmPoolMemberMon + ":" + strPmPriGroup);

    	ajaxOut = buildNewPoolAjax('new_pool_build', arr, pVsName, pVsPort, pMon, pEnv, pLBMethod, pPriGroup, pPriGroupLessThan, strPmPoolMemberName, strPmPoolMemberIp, strPmPoolMemberPort, strPmPoolMemberMon, strPmPriGroup);
    	ajaxOut.done(poolBuildProcessData);
    	
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
    	var monData = {'phpFileName':'', 'DevIP':'', 'MVsName':'', 'MVsPort':'', 'MDesc':'', 'MEnv':'', 'MMonType':'', 'MMonCode':'', 'MParMonType':'', 'interval':'', 'timeout':'', 'send':'', 'recv':'', 'username':'', 'password':'', 'reverse':'', 'aliasPort':'', 'cipherlist':''};
    	var bigipNameAndIP = $('#ltmSelBox').val()
    	var arr = bigipNameAndIP.split(":");
    	
    	monData['phpFileName'] = 'new_monitor_build';
    	monData['DevIP'] = arr[1];
    	monData['MVsName'] = $('#m_vs_name').val();
    	monData['MVsPort'] = $('#m_vs_port').val();
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
    		$('#ir_td_dg_type').append("<label> DG Type: </label><select name='ir_dg_type_select' id='ir_dg_type_select' required='required' ><option selected='selected'>Select...</option><option>Address</option><option>String</option><option>Integer</option></select>");
    	}
    });
    
    // Event delegation to ir_td_dg_type
    $('#ir_td_dg_type').on('change', function() {
    	var ir_dg_type = $('#ir_dg_type_select').val();
		$('#irConfTable_tbody').empty();
    	if (ir_dg_type == "Address"){
    		$('#irConfTable_tbody').append("<tr> <td> <label>Address:</label> <input type='text' id='ir_dg_name' />(*required) </td> </tr><tr> <td> <label>Value&nbsp;&nbsp;&nbsp;&nbsp;:</label> <input type='text' id='ir_dg_value' /> </td> </tr><tr><td><input type='button' id='ir_add_btn' value='Add' />&nbsp;&nbsp;&nbsp;&nbsp;</td></tr> <tr> <td> <select size='8' width='680px' style='width:680px' id='dg_select_records' ></select> </td> </tr> <tr> <td><input type='button' id='ir_dg_del' value='Delete' />&nbsp;&nbsp;<input type='button' id='ir_dg_edit' value='Edit' />&nbsp;&nbsp;&nbsp;&nbsp;</td> </tr>");
    	}
    	else if (ir_dg_type == "String"){
    		$('#irConfTable_tbody').append("<tr> <td> <label>String:</label> <input type='text' id='ir_dg_name' />(*required) </td> </tr><tr> <td> <label>Value:</label> <input type='text' id='ir_dg_value' /> </td> </tr><tr><td><input type='button' id='ir_add_btn' value='Add' />&nbsp;&nbsp;&nbsp;&nbsp;</td></tr> <tr> <td> <select size='8' width='680px' style='width:680px' id='dg_select_records' ></select> </td> </tr> <tr> <td><input type='button' id='ir_dg_del' value='Delete' />&nbsp;&nbsp;<input type='button' id='ir_dg_edit' value='Edit' />&nbsp;&nbsp;&nbsp;&nbsp;</td> </tr>");
    	}
    	else if (ir_dg_type == "Integer"){
    		$('#irConfTable_tbody').append("<tr> <td> <label>Integer:</label> <input type='text' id='ir_dg_name' />(*required) </td> </tr><tr> <td> <label>Value&nbsp;&nbsp;&nbsp;:</label> <input type='text' id='ir_dg_value' /> </td> </tr><tr><td><input type='button' id='ir_add_btn' value='Add' />&nbsp;&nbsp;&nbsp;&nbsp;</td></tr> <tr> <td> <select size='8' width='680px' style='width:680px' id='dg_select_records' ></select> </td> </tr> <tr> <td><input type='button' id='ir_dg_del' value='Delete' />&nbsp;&nbsp;<input type='button' id='ir_dg_edit' value='Edit' />&nbsp;&nbsp;&nbsp;&nbsp;</td> </tr>");
    	}
    });
    
    // Event delegation to irConfTable_tbody 
    $('#irConfTable_tbody').on('click', '#ir_add_btn', function() {
    	
    	//alert("Add button clicked!");
    	var dg_name = $('#ir_dg_name').val();
    	var dg_val = $('#ir_dg_value').val();
    	if (dg_name != ''){
    		$('#dg_select_records').append('<option value="'+ dg_name + ':' + dg_val +'">' + dg_name + ':' + dg_val + '</option>');
    		$('#ir_dg_name').val('');
    		$('#ir_dg_value').val('');
    		$('#ir_dg_name').focus();
    	}
    	else
    		$('#ir_dg_name').focus();
    });
    $('#irConfTable_tbody').on('click', '#ir_dg_edit', function() {
    	//alert("Edit button clicked! - ");
    	var dg_record = $('#dg_select_records option:selected').text();
    	//alert("selected Value: " + dg_record);
    	var arr = dg_record.split(":");
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
    	var irData = {'phpFileName':'', 'DevIP':'', 'IrVsName':'', 'IrVsPort':'', 'IrEnv':'', 'IrType':'', 'IrCode':'', 'IrDgType':'', 'IrDgData':''};
    	var bigipNameAndIP = $('#ltmSelBox').val()
    	var arr = bigipNameAndIP.split(":");
    	
    	var irType = $('#ir_type').val();
    	
    	// Data feed to irData
    	irData['phpFileName'] = 'new_irule_build';
    	irData['DevIP'] = arr[1];
    	irData['IrVsName'] = $('#ir_vs_name').val();
    	irData['IrVsPort'] = $('#ir_vs_port').val();
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
    	
    	/*
    	var output;
    	$.each(irData, function(index) {	
    	    output = output + irData[index] + "\n";
    	});
    	alert("Data: " + output);
    	*/
    	
    	ajaxOut = buildIrAjax("new_irule_build", irData);
    	ajaxOut.done(buildIrProcessData);
    });
    
    $('#cert_import_btn').on('click', function() {
    	//alert("Cert Import button clicked!");
    	$('#cert_iframe_fieldset').empty();
    	$('#cert_iframe_fieldset').append('<legend>Import Cert/Key Configuration</legend>');
    	$('#cert_iframe_fieldset').append('<iframe src="/content/if_ssl_import.php" width="725px" height="600" frameborder="0"></iframe>');
    });

    $('#cert_create_btn').on('click', function() {
    	//alert("Cert Create button clicked!");
    	$('#cert_iframe_fieldset').empty();
    	$('#cert_iframe_fieldset').append('<legend>Create Cert/Key Configuration</legend>');
    	$('#cert_iframe_fieldset').append('<iframe src="/content/if_ssl_create.php" width="725px" height="600" frameborder="0"></iframe>');    	
    });
    
    // Profile Submenu event handlers
    $('#ul_prf_selected li').on('click', function() {
    	prfSelected = $(this).text();
    	$('#prf_iframe_fieldset').empty();
    	alert($(this).text());
    	
    	if (prfSelected == 'HTTP'){
    		$('#prf_iframe_fieldset').append('<legend>HTTP Profile Configuration</legend>');
    		$('#prf_iframe_fieldset').append('<iframe src="/content/if_prf_svc_http.php" width="725px" height="600" frameborder="0"></iframe>');
    	}
    	else if (prfSelected == 'DNS'){
    		$('#prf_iframe_fieldset').append('<legend>DNS Profile Configuration</legend>');
    		$('#prf_iframe_fieldset').append('<iframe src="/content/if_prf_svc_dns.php" width="725px" height="600" frameborder="0"></iframe>');
    	}
    	else if (prfSelected == 'Cookie'){
    		$('#prf_iframe_fieldset').append('<legend>Cookie Persistence Profile Configuration</legend>');
    		$('#prf_iframe_fieldset').append('<iframe src="/content/if_prf_persist_cookie.php" width="725px" height="600" frameborder="0"></iframe>');
    	}
    	else if (prfSelected == 'Destination Address Affinity'){
    		$('#prf_iframe_fieldset').append('<legend>Destination Address Affinity Persistence Profile Configuration</legend>');
    		$('#prf_iframe_fieldset').append('<iframe src="/content/if_prf_persist_dest.php" width="725px" height="600" frameborder="0"></iframe>');
    	}
    	else if (prfSelected == 'Source Address Affinity'){
    		$('#prf_iframe_fieldset').append('<legend>Source Address Affinity Persistence Profile Configuration</legend>');
    		$('#prf_iframe_fieldset').append('<iframe src="/content/if_prf_persist_src.php" width="725px" height="600" frameborder="0"></iframe>');
    	}
    	else if (prfSelected == 'Hash'){
    		$('#prf_iframe_fieldset').append('<legend>Hash Persistence Profile Configuration</legend>');
    		$('#prf_iframe_fieldset').append('<iframe src="/content/if_prf_persist_hash.php" width="725px" height="600" frameborder="0"></iframe>');
    	}
    	else if (prfSelected == 'SSL'){
    		$('#prf_iframe_fieldset').append('<legend>SSL Persistence Profile Configuration</legend>');
    		$('#prf_iframe_fieldset').append('<iframe src="/content/if_prf_persist_ssl.php" width="725px" height="600" frameborder="0"></iframe>');
    	}
    	else if (prfSelected == 'Universal'){
    		$('#prf_iframe_fieldset').append('<legend>Universal Persistence Profile Configuration</legend>');
    		$('#prf_iframe_fieldset').append('<iframe src="/content/if_prf_persist_univ.php" width="725px" height="600" frameborder="0"></iframe>');
    	}      	
    	else if (prfSelected == 'Fast L4'){
    		$('#prf_iframe_fieldset').append('<legend>FastL4 Profile Configuration</legend>');
    		$('#prf_iframe_fieldset').append('<iframe src="/content/if_prf_prot_fastl4.php" width="725px" height="600" frameborder="0"></iframe>');
    	}
    	else if (prfSelected == 'TCP'){
    		$('#prf_iframe_fieldset').append('<legend>TCP Profile Configuration</legend>');
    		$('#prf_iframe_fieldset').append('<iframe src="/content/if_prf_prot_tcp.php" width="725px" height="600" frameborder="0"></iframe>');
    	}
    	else if (prfSelected == 'UDP'){
    		$('#prf_iframe_fieldset').append('<legend>UDP Profile Configuration</legend>');
    		$('#prf_iframe_fieldset').append('<iframe src="/content/if_prf_prot_udp.php" width="725px" height="600" frameborder="0"></iframe>');
    	}
    	else if (prfSelected == 'Client'){
    		$('#prf_iframe_fieldset').append('<legend>Client SSL Profile Configuration</legend>');
    		$('#prf_iframe_fieldset').append('<iframe src="/content/if_prf_ssl_client.php" width="725px" height="600" frameborder="0"></iframe>');
    	}
    	else if (prfSelected == 'Server'){
    		$('#prf_iframe_fieldset').append('<legend>Server SSL Profile Configuration</legend>');
    		$('#prf_iframe_fieldset').append('<iframe src="/content/if_prf_ssl_server.php" width="725px" height="600" frameborder="0"></iframe>');
    	}
    	else if (prfSelected == 'OneConnect'){
    		$('#prf_iframe_fieldset').append('<legend>OneConnect Profile Configuration</legend>');
    		$('#prf_iframe_fieldset').append('<iframe src="/content/if_prf_other_oneconnect.php" width="725px" height="600" frameborder="0"></iframe>');
    	}
    });
    
});