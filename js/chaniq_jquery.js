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
	//alert(monData['interval'] + ":" + monData['send']);
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

});