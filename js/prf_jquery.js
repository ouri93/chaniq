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

function validateInput(prfOptData) {
	$('#prf_name').css('border-color', '#E1E1E1');
	//alert("DNS REsolver: " + prfOptData['dnsResolver']); 
	if(prfOptData['name'] == '') {
		if (GetParentURLParameter('go') == 'new_profile' ) {
			$('#prf_name').css('border-color', 'red');	
		}
		else $('#chg_svc_prf_name_select').css('border-color', 'red');
		return false;
	}
	if (prfOptData['dnsResolver'] == 'select'){
		$('#newprf_EvalReview').html("** DNS Resolver is required!<br>");
		return false;
	}
	return true;
}

function getMaskByCIDR(strPfxLength) {
	var pfxLength = parseInt(strPfxLength);
	var mask=[];
	for(i=0;i<4;i++) {
	    var n = Math.min(pfxLength, 8);
	    mask.push(256 - Math.pow(2, 8-n));
	    pfxLength -= n;
	}
	return mask.join('.');
}

function getCIDRByMask(strCIDR) {
	var maskNodes = strCIDR.match(/(\d+)/g);
	var cidr = 0;
	for(var i in maskNodes)
	{
	  cidr += (((maskNodes[i] >>> 0).toString(2)).match(/1/g) || []).length;
	}
	return cidr;
}

// Retrieve partition names from a given BIG-IP
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
		$('#' + selID).append("<option value='select' selected='selected'>Select...</option><option value='common' >Common</option>");

		$('#del_svc_prf_name_select option').each(function(index) {
			$(this).remove();
		});
		$('#del_svc_prf_name_select').append("<option value='none' selected='selected'>None</option>");

		
		//var partNames = "Part2:Part3:".split(":");
		var partNames = response_in.split(":");
		
		// Empty array - Return 1
		var numOfPart = partNames.length; 
		if (numOfPart <= 1) return;
		else{
			var i=0;
			for (;i < numOfPart-1;i++){
				strResult += "<option value='" + partNames[i].toLowerCase() + "'>" + partNames[i] + "</option>";
			}
			
			$('#' + selID).append(strResult);	
		}
		//alert("Return output: " + strResult);
		
	});
}

//Retrieve profile names of a given Profile type from a given BIG-IP
function loadProfileNames(ltmIP, prfType, selID){
	
	ajxOut = $.ajax({
		url: '/content/get_profile_names.php',
		type: 'POST',
		dataType: 'JSON',
		data: {method:'get_profile_names', DevIP:ltmIP, LoadTypeName:prfType},
		error: function(jqXHR, textStatus, errorThrown){
			alert("Ajax call to retrieve Profile names (loadProfileNames) has failed!");
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
		
		var flag=0;

		// BIG-IP 12.1.2 Builtin profile list
		var builtinProfiles = ["http", "http-explicit", "http-transparent", "dns", "cookie", "dest_addr", "hash", "msrdp", "sip_info", "source_addr", "ssl", "universal", "fastL4", "apm-forwarding-fastL4", "apm-forwarding-client-tcp", "apm-forwarding-server-tcp", "tcp", "udp", "clientssl", "serverssl", "oneconnect", "stream"];
		$.each(response_in, function(index) {
			if (response_in[index] == "none"){
				$('#' + selID).append("<option value='none' selected='selected'>None</option>");
				flag = 1;
			}
			else if (builtinProfiles.includes(response_in[index])== false ){
				strResult += "<option value='" + response_in[index] + "'>" + response_in[index] + "</option>";
			}
		});
		
		// From Python get_profiles.py, some profiles add "none" some don't.. No consistencey. This is simple workaround. 
		if(flag == 0)$('#' + selID).append("<option value='none' selected='selected'>None</option>");
		
		$('#' + selID).append(strResult);	

	});
}

// Delete a given profile name of a given partition
function deleteProfile(devIP, prfType, partition, prfName){
	alert("LTM: " + devIP + "\nProfile Type: " + prfType + "\nPartition: " + partition + "\nProfile Name: " + prfName);
	ajxOut = $.ajax({
		url: '/content/del_profile_ajax.php',
		type: 'POST',
		dataType: 'JSON',
		data: {method:'del_profile_ajax', DevIP:devIP, LoadTypeName:prfType, Partition:partition, PrfName:prfName},
		error: function(jqXHR, textStatus, errorThrown){
			alert("Ajax call to delete a given profile (deleteProfile) has failed!");
            console.log('jqXHR:');
            console.log(jqXHR);
            console.log('textStatus:');
            console.log(textStatus);
            console.log('errorThrown:');
            console.log(errorThrown);
		}
	});
	ajxOut.done(function (response_in){
		
		/* Debugging */

		var strResult = '***** Profile deletion result *****<br>';
		$.each(response_in, function(index) {
			strResult += response_in[index] + "<br>";
		});
		
		$('#newprf_EvalReview').html(strResult);
	});
}


// Initialize Profile Key and default value based on the profile type
// This function determins the supported profile options
function initPrfOptData(prfOptData, prfType) {
	
	var prfOptKeys =[]; 
	
	if (prfType == "DNS"){
		/*
		 * enableDnsExpress-DNS Express , enableDnsFirewall-DNS Security, enableGtm-GSLB, enableHardwareQueryValidation-Protocol Validation, enableHardwareResponseCache-Response Cache
		 * processRd-Process Recursion Desired, processXfr-Zone Transfer, unhandledQueryAction-Unhandled Query Actions, useLocalBind-Use BIND Server on BIG-IP
		 */
		var tmpPrfOptKeys = ['defaultsFrom', 'enableHardwareQueryValidation', 'enableHardwareResponseCache', 'enableDnsExpress', 'enableGtm', 'unhandledQueryAction', 'useLocalBind', 'processXfr','enableDnsFirewall', 'processRd']; 
	}
	else if (prfType == "Cookie"){
		/*
		 * 'defaultsFrom', 'method'- Cookie method(hash, insert, passive, rewrite), 'cookieName', 'httponly', 'secure', 'alwaysSend', 'expiration', 'overrideConnectionLimit'
		 */
		var tmpPrfOptKeys = ['defaultsFrom', 'method', 'cookieName', 'httponly', 'secure', 'alwaysSend', 'expiration', 'overrideConnectionLimit'];
	}
	else if (prfType == "DestAddrAffinity"){
		/* 
		 * Path: /mgmt/tm/ltm/persistence/dest-addr
		 * 'defaultsFrom', 'matchAcrossServices', 'matchAcrossVirtuals', 'matchAcrossPools','hashAlgorithm', 'timeout', 'mask', 'overrideConnectionLimit'
		 */
		var tmpPrfOptKeys = ['defaultsFrom', 'matchAcrossServices', 'matchAcrossVirtuals', 'matchAcrossPools','hashAlgorithm', 'timeout', 'mask', 'overrideConnectionLimit'];		
	}
	else if (prfType == "SrcAddrAffinity"){
		/* 
		 * Path: /mgmt/tm/ltm/persistence/source-addr
		 * 'defaultsFrom', 'matchAcrossServices', 'matchAcrossVirtuals', 'matchAcrossPools','hashAlgorithm', 'timeout', 'mask', 'mapProxies', 'overrideConnectionLimit'
		 */
		var tmpPrfOptKeys = ['defaultsFrom', 'matchAcrossServices', 'matchAcrossVirtuals', 'matchAcrossPools','hashAlgorithm', 'timeout', 'mask', 'mapProxies', 'overrideConnectionLimit'];	
	}
	else if (prfType == "Hash"){
		/*
		 * matchAcrossServices, matchAcrossVirtuals, matchAcrossPools, hashAlgorithm, hashOffset, hashLength, hashStartPattern, hashEndPattern, hashBufferLimit, timeout, rule, overrideConnectionLimit
		 */
		var tmpPrfOptKeys = ['defaultsFrom', 'matchAcrossServices', 'matchAcrossVirtuals', 'matchAcrossPools','hashAlgorithm', 'hashOffset', 'hashLength', 'hashStartPattern', 'hashEndPattern', 'hashBufferLimit', 'timeout', 'rule', 'mapProxies', 'overrideConnectionLimit'];
	}
	else if (prfType == "SSL"){
		/*
		 * matchAcrossServices, matchAcrossVirtuals, matchAcrossPools, timeout, overrideConnectionLimit
		 */
		var tmpPrfOptKeys = ['defaultsFrom', 'matchAcrossServices', 'matchAcrossVirtuals', 'matchAcrossPools', 'timeout', 'overrideConnectionLimit'];
	}
	else if (prfType == "Universal"){
		/*
		 * matchAcrossServices, matchAcrossVirtuals, matchAcrossPools, timeout, rule, overrideConnectionLimit
		 */
		var tmpPrfOptKeys = ['defaultsFrom', 'matchAcrossServices', 'matchAcrossVirtuals', 'matchAcrossPools','timeout', 'rule', 'overrideConnectionLimit'];
	}
	else if (prfType == "FastL4"){
		/*
		 * resetOnTimeout, reassembleFragments, idleTimeout, tcpHandshakeTimeout, tcpTimestampMode, tcpWscaleMode, looseInitialization, looseClose, tcpCloseTimeout, keepAliveInterval
		 */
		var tmpPrfOptKeys = ['defaultsFrom', 'resetOnTimeout', 'reassembleFragments', 'idleTimeout', 'tcpHandshakeTimeout', 'tcpTimestampMode', 'tcpWscaleMode', 'looseInitialization', 'looseClose', 'tcpCloseTimeout', 'keepAliveInterval'];
	}
	else if (prfType == "TCP"){
		/*
		 * 'resetOnTimeout', 'resetOnTimeout', 'proxyBufferHigh', 'proxyBufferLow', 'receiveWindowSize', 'sendBufferSize', 'ackOnPush', 'nagle', 'initCwnd', 'slowStart', 'selectiveAcks'
		 */
		var tmpPrfOptKeys = ['defaultsFrom', 'resetOnTimeout', 'proxyBufferHigh', 'proxyBufferLow', 'receiveWindowSize', 'sendBufferSize', 'ackOnPush', 'nagle', 'initCwnd', 'slowStart', 'selectiveAcks'];
		
	}
	else if (prfType == "UDP"){
		/*
		 * 'proxyMss', 'idleTimeout', 'ipTosToClient', 'linkQosToClient', 'datagramLoadBalancing', 'allowNoPayload', 'ipDfMode', 'ipTtlV4', 'ipTtlV6', 'ipDfMode'
		 */
		var tmpPrfOptKeys = ['defaultsFrom', 'proxyMss', 'idleTimeout', 'ipTosToClient', 'linkQosToClient', 'datagramLoadBalancing', 'allowNoPayload', 'ipDfMode', 'ipTtlV4', 'ipTtlV6', 'ipDfMode'];
		
	}
	else if (prfType == "CLIENTSSL"){
		/*
		 * 'certKeyChain', 'ciphers', 'proxySsl', 'proxySslPassthrough', 'renegotiation', 'renegotiatePeriod', 'renegotiateSize', 'renegotiateMaxRecordDelay', 'secureRenegotiation', 'maxRenegotiationsPerMinute', 'serverName', 'sniDefault', 'sniRequire'
		 */
		var tmpPrfOptKeys = ['defaultsFrom', 'cert', 'key', 'chain', 'ciphers', 'proxySsl', 'proxySslPassthrough', 'renegotiation', 'renegotiatePeriod', 'renegotiateSize', 'renegotiateMaxRecordDelay', 'secureRenegotiation', 'maxRenegotiationsPerMinute', 'serverName', 'sniDefault', 'sniRequire'];

	}
	else if (prfType == "SERVERSSL"){
		/*
		 * 'cert', 'key', 'chain', 'ciphers', 'proxySsl', 'proxySslPassthrough', 'renegotiation', 'renegotiatePeriod', 'renegotiateSize', 'secureRenegotiation', 'serverName', 'sniDefault', 'sniRequire'
		 */
		var tmpPrfOptKeys = ['defaultsFrom','cert', 'key', 'chain', 'ciphers', 'proxySsl', 'proxySslPassthrough', 'renegotiation', 'renegotiatePeriod', 'renegotiateSize', 'secureRenegotiation', 'serverName', 'sniDefault', 'sniRequire'];
	}
	else if (prfType == "OneConnect"){
		/*
		 * 'sourceMask', 'maxSize', 'maxAge', 'maxReuse', 'idleTimeoutOverride', 'limitType'
		 */
		var tmpPrfOptKeys = ['defaultsFrom', 'sourceMask', 'maxSize', 'maxAge', 'maxReuse', 'idleTimeoutOverride', 'limitType'];
	}
	else if (prfType == "Stream"){
		/*
		 * 'source', 'tmTarget'
		 */
		var tmpPrfOptKeys = ['defaultsFrom', 'source', 'tmTarget'];
	}

	prfOptKeys = prfOptKeys.concat(tmpPrfOptKeys);
	
	for(var i=0; i<prfOptKeys.length;i++){
		prfOptData[prfOptKeys[i]] = '';
	}
}

function initHttpPrfOptData(prfOptData, prfType, pxyMode ) {
	
	var prfOptKeys =[]; 
	
	if (pxyMode == "reverse"){
		var httpPrfOptKeys = ['proxyType', 'defaultsFrom', 'basicAuthRealm', 'fallbackHost', 'fallbackStatusCodes', 'headerErase', 'headerInsert', 'requestChunking', 'responseChunking', 'insertXforwardedFor', 'serverAgentName']; 
		prfOptKeys = prfOptKeys.concat(httpPrfOptKeys);
	}
	else if (pxyMode == "explicit") {
		var httpPrfOptKeys = ['proxyType', 'defaultsFrom', 'basicAuthRealm', 'fallbackHost', 'fallbackStatusCodes', 'headerErase', 'headerInsert', 'requestChunking', 'responseChunking', 'insertXforwardedFor', 'serverAgentName', 'dnsResolver']; 
		prfOptKeys = prfOptKeys.concat(httpPrfOptKeys);
	}
	else if (pxyMode == "transparent") {
		var httpPrfOptKeys = ['proxyType', 'defaultsFrom', 'basicAuthRealm', 'fallbackHost', 'fallbackStatusCodes', 'headerErase', 'headerInsert', 'requestChunking', 'responseChunking', 'insertXforwardedFor', 'serverAgentName']; 
		prfOptKeys = prfOptKeys.concat(httpPrfOptKeys);
	}
	for(var i=0; i<prfOptKeys.length;i++){
		prfOptData[prfOptKeys[i]] = '';
	}
}

function setHttpPrfOptData(prfOptData, prfType, pxyMode, parPrfName ) {
	
	prfOptData['proxyType'] = $('#svc_prf_proxymode_select').val();
	prfOptData['defaultsFrom'] = '/Common/' + parPrfName;
	prfOptData['basicAuthRealm'] = $('#httpBasicAuth').val();
	prfOptData['fallbackHost'] = $('#httpFallbackHost').val();
	prfOptData['fallbackStatusCodes'] = $('#httpFallbackErrorCodes').val();
	prfOptData['headerErase'] = $('#httpReqHdrErase').val();
	prfOptData['headerInsert'] = $('#httpReqHdrInsert').val();
	prfOptData['requestChunking'] = $('#httpReqChunk option:selected').val();
	prfOptData['responseChunking'] = $('#httpRespChunk option:selected').val();
	prfOptData['insertXforwardedFor'] = $('#httpXFF').val();
	prfOptData['serverAgentName'] = $('#httpAgentName').val();
	if (pxyMode == 'explicit'){
		prfOptData['dnsResolver'] = $('#httpDnsResolver').val();
	}
	
}
// Retrieve input profile data from Web interface and save the data onto prfOptData dictionary
function setPrfOptData(prfOptData, prfType, parPrfName) {

	prfOptData['LoadTypeName'] = prfType;
	prfOptData['defaultsFrom'] = '/Common/' + parPrfName;
	
	if(prfType == 'DNS'){
		//'defaultsFrom', 'enableHardwareQueryValidation', 'enableHardwareResponseCache', 'enableDnsExpress', 'enableGtm', 'unhandledQueryAction'
		//'useLocalBind', 'processXfr','enableDnsFirewall', 'processRd'
		prfOptData['enableHardwareQueryValidation'] = $('#dnsHwPrtoValid').val();
		prfOptData['enableHardwareResponseCache'] = $('#dnsHwRespCache').val();
		prfOptData['enableDnsExpress'] = $('#dnsExp').val();
		prfOptData['enableGtm'] = $('#dnsGtm').val();
		prfOptData['unhandledQueryAction'] = $('#dnsUnhandledQueryAct').val();
		prfOptData['useLocalBind'] = $('#dnsUseBind option:selected').val();
		prfOptData['processXfr'] = $('#dnsZoneXfr option:selected').val();
		prfOptData['enableDnsFirewall'] = $('#dnsSecurity').val();
		prfOptData['processRd'] = $('#dnsRd').val();
	}
	else if(prfType == "Cookie") {
		//'defaultsFrom', 'method'- Cookie method(hash, insert, passive, rewrite), 'cookieName', 'httponly', 'secure', 'alwaysSend', 'expiration', 'overrideConnectionLimit'
		prfOptData['method'] = $('#ckMethod option:selected').val();
		prfOptData['cookieName'] = $('#ckName').val();
		prfOptData['httponly'] = $('#ckHttpOnly option:selected').val();
		prfOptData['secure'] = $('#ckSecure option:selected').val();
		if ($('#ckAlzSend').prop('checked') == true) prfOptData['alwaysSend'] = 'enabled';
		else prfOptData['alwaysSend'] = 'disabled';
		prfOptData['expiration'] = $('#ckExp').val();
		prfOptData['overrideConnectionLimit'] = $('#ckConnLimit option:selected').val();
		
	}
	else if(prfType == 'DestAddrAffinity'){
		// 'defaultsFrom', 'matchAcrossServices', 'matchAcrossVirtuals', 'matchAcrossPools','hashAlgorithm', 'timeout', 'mask', 'overrideConnectionLimit'
		prfOptData['matchAcrossServices'] = $('#dstXSvc option:selected').val();
		prfOptData['matchAcrossVirtuals'] = $('#dstXVs option:selected').val();
		prfOptData['matchAcrossPools'] = $('#dstXP option:selected').val();
		prfOptData['hashAlgorithm'] = $('#dstHash option:selected').val();
		if ($('#dstTimeout').val() == '0') prfOptData['timeout'] = 'indefinite';
		else prfOptData['timeout'] = $('#dstTimeout').val(); 
		if ($('#dstMask').val() == '0')	prfOptData['mask'] = 'none';
		else prfOptData['mask'] = getMaskByCIDR($('#dstMask').val());
		prfOptData['overrideConnectionLimit'] = $('#dstConnLimit option:selected').val();
	}
	else if(prfType == 'SrcAddrAffinity'){
		// 'defaultsFrom', 'matchAcrossServices', 'matchAcrossVirtuals', 'matchAcrossPools','hashAlgorithm', 'timeout', 'mask', 'mapProxies', 'overrideConnectionLimit'
		prfOptData['matchAcrossServices'] = $('#srcXSvc option:selected').val();
		prfOptData['matchAcrossVirtuals'] = $('#srcXVs option:selected').val();
		prfOptData['matchAcrossPools'] = $('#srcXP option:selected').val();
		prfOptData['hashAlgorithm'] = $('#srcHash option:selected').val();
		if ($('#srcTimeout').val() == '0') prfOptData['timeout'] = 'indefinite';
		else prfOptData['timeout'] = $('#srcTimeout').val(); 
		if ($('#srcMask').val() == '0')	prfOptData['mask'] = 'none';
		else prfOptData['mask'] = getMaskByCIDR($('#srcMask').val());
		prfOptData['mapProxies'] = $('#srcMapPrxy option:selected').val();
		prfOptData['overrideConnectionLimit'] = $('#srcConnLimit option:selected').val();
	}
	else if(prfType == 'Hash'){
		// 'defaultsFrom', 'matchAcrossServices', 'matchAcrossVirtuals', 'matchAcrossPools', 'hashAlgorithm', 'hashOffset', 'hashLength', 'hashStartPattern', 'hashEndPattern', 'hashBufferLimit', 'timeout', 'rule', 'overrideConnectionLimit'
		prfOptData['matchAcrossServices'] = $('#hsXSvc option:selected').val();
		prfOptData['matchAcrossVirtuals'] = $('#hsXVs option:selected').val();
		prfOptData['matchAcrossPools'] = $('#hsXP option:selected').val();
		prfOptData['hashAlgorithm'] = $('#hsHash option:selected').val();
		prfOptData['hashOffset'] = $('#hsOffset').val();
		prfOptData['hashLength'] = $('#hsLen').val();
		prfOptData['hashStartPattern'] = $('#hsSPtn').val();
		prfOptData['hashEndPattern'] = $('#hsEPtn').val();
		prfOptData['hashBufferLimit'] = $('#hsBfLimit').val();
		if ($('#hsTimeout').val() == '0') prfOptData['timeout'] = 'indefinite';
		else prfOptData['timeout'] = $('#hsTimeout').val();
		prfOptData['rule'] = $('#persistIRule option:selected').val();
		prfOptData['overrideConnectionLimit'] = $('#hsConnLimit option:selected').val();
	}
	else if(prfType == 'SSL'){
		// 'defaultsFrom', 'matchAcrossServices', 'matchAcrossVirtuals', 'matchAcrossPools', 'timeout', 'overrideConnectionLimit'
		prfOptData['matchAcrossServices'] = $('#sslXSvc option:selected').val();
		prfOptData['matchAcrossVirtuals'] = $('#sslXVs option:selected').val();
		prfOptData['matchAcrossPools'] = $('#sslXP option:selected').val();
		if ($('#sslTimeout').val() == '0') prfOptData['timeout'] = 'indefinite';
		else prfOptData['timeout'] = $('#sslTimeout').val();
		prfOptData['overrideConnectionLimit'] = $('#sslConnLimit option:selected').val();
	}
	else if(prfType == 'Universal'){
		// 'defaultsFrom', 'matchAcrossServices', 'matchAcrossVirtuals', 'matchAcrossPools', 'timeout', 'rule', 'overrideConnectionLimit'
		prfOptData['matchAcrossServices'] = $('#uniXSvc option:selected').val();
		prfOptData['matchAcrossVirtuals'] = $('#uniXVs option:selected').val();
		prfOptData['matchAcrossPools'] = $('#uniXP option:selected').val();
		if ($('#uniTimeout').val() == '0') prfOptData['timeout'] = 'indefinite';
		else prfOptData['timeout'] = $('#uniTimeout').val();
		
		if($('#persistIRule option:selected').val() == 'select'){
			prfOptData['rule']='';
		}
		else
			prfOptData['rule'] = '/Common/' + $('#persistIRule option:selected').val();
		prfOptData['overrideConnectionLimit'] = $('#uniConnLimit option:selected').val();
	}
	else if (prfType == "FastL4"){
		// defaultsFrom, resetOnTimeout, reassembleFragments, idleTimeout, tcpHandshakeTimeout, tcpTimestampMode, tcpWscaleMode, looseInitialization, looseClose, tcpCloseTimeout, keepAliveInterval
		//               f4ResetTO, f4RzmbFrgmt, prfIdleTimeout, f4TcpHSTO, f4TcpTSMode, f4TcpWsMode, f4LsInit, f4LsCls, f4TcpClsTO, f4KeepIntvl	
		prfOptData['resetOnTimeout'] = $('#f4ResetTO option:selected').val();
		prfOptData['reassembleFragments'] = $('#f4RzmbFrgmt option:selected').val();
		if ($('#prfIdleTimeout option:selected').val() == 'specify') prfOptData['idleTimeout'] = $('#prfIdleTimeoutSpecify').val();
		else prfOptData['idleTimeout'] = $('#prfIdleTimeout option:selected').val();
		if ($('#f4TcpHSTO option:selected').val() == 'specify') prfOptData['tcpHandshakeTimeout'] = $('#f4TcpHSTOSpecify').val();
		else prfOptData['tcpHandshakeTimeout'] = $('#f4TcpHSTO option:selected').val();
		prfOptData['tcpTimestampMode'] = $('#f4TcpTSMode option:selected').val();
		prfOptData['tcpWscaleMode'] = $('#f4TcpWsMode option:selected').val();
		prfOptData['looseInitialization'] = $('#f4LsInit option:selected').val();
		prfOptData['looseClose'] = $('#f4LsCls option:selected').val();
		if ($('#f4TcpClsTO option:selected').val() == 'specify') prfOptData['tcpCloseTimeout'] = $('#f4TcpClsTOSpecify').val();
		else prfOptData['tcpCloseTimeout'] = $('#f4TcpClsTO option:selected').val();
		if ($('#f4KeepIntvl option:selected').val() == 'specify') prfOptData['keepAliveInterval'] = $('#f4KeepIntvlSpecify').val();
		else prfOptData['keepAliveInterval'] = $('#f4KeepIntvl option:selected').val();
	}
	else if (prfType == "TCP"){
		// defaultsFrom, 'resetOnTimeout', 'proxyBufferHigh', 'proxyBufferLow', 'receiveWindowSize', 'sendBufferSize', 'ackOnPush', 'nagle', 'initCwnd', 'slowStart', 'selectiveAcks'
		//                tcpRstOnTO, tcpPxyBfHigh, tcpPxyBfLow, tcpRcvWin, tcpSndBfSz, tcpAckOnPush, tcpNagle, tcpInitCwnd, tcpSlowStart, tcpSltvAcks
		prfOptData['resetOnTimeout'] = $('#tcpRstOnTO option:selected').val();
		prfOptData['proxyBufferHigh'] = $('#tcpPxyBfHigh').val();
		prfOptData['proxyBufferLow'] = $('#tcpPxyBfLow').val();
		prfOptData['receiveWindowSize'] = $('#tcpRcvWin').val();
		prfOptData['sendBufferSize'] = $('#tcpSndBfSz').val();
		prfOptData['ackOnPush'] = $('#tcpAckOnPush option:selected').val();
		prfOptData['nagle'] = $('#tcpNagle option:selected').val();
		prfOptData['initCwnd'] = $('#tcpInitCwnd').val();
		prfOptData['slowStart'] = $('#tcpSlowStart option:selected').val();
		prfOptData['selectiveAcks'] = $('#tcpSltvAcks option:selected').val();
	}
	else if (prfType == "UDP"){
		// defaultsFrom, 'proxyMss', 'idleTimeout', 'ipTosToClient', 'linkQosToClient', 'datagramLoadBalancing', 'allowNoPayload', 'ipTtlMode', 'ipTtlV4', 'ipTtlV6', 'ipDfMode'
		//                udpPxyMss, prfIdleTimeout, udpIpToS, udpLkQoS, udpDGLB, udpNoPayload, udpTtlMode, udpTtlV4, udpTtlV6, udpDfMode
		prfOptData['proxyMss'] = $('#udpPxyMss option:selected').val();
		if ($('#prfIdleTimeout option:selected').val() == 'specify') prfOptData['idleTimeout'] = $('#prfIdleTimeoutSpecify').val();
		else prfOptData['idleTimeout'] = $('#prfIdleTimeout option:selected').val();
		if ($('#udpIpToS option:selected').val() == 'specify') prfOptData['ipTosToClient'] = $('#udpIpToSSpecify').val();
		else prfOptData['ipTosToClient'] = $('#udpIpToS option:selected').val();
		if ($('#udpLkQoS option:selected').val() == 'specify') prfOptData['linkQosToClient'] = $('#udpLkQoSSpecify').val();
		else prfOptData['linkQosToClient'] = $('#udpLkQoS option:selected').val();
		prfOptData['datagramLoadBalancing'] = $('#udpDGLB option:selected').val();
		prfOptData['allowNoPayload'] = $('#udpNoPayload option:selected').val();
		prfOptData['ipTtlMode'] = $('#udpTtlMode option:selected').val();
		prfOptData['ipTtlV4'] = $('#udpTtlV4').val();
		prfOptData['ipTtlV6'] = $('#udpTtlV6').val();
		prfOptData['ipDfMode'] = $('#udpDfMode option:selected').val();
	}
	else if (prfType == "CLIENTSSL"){
		// defaultsFrom, 'certificate', 'key', 'cert', 'key', 'chain', 'ciphers', 'proxySsl', 'proxySslPassthrough', 'renegotiation', 'renegotiatePeriod', 'renegotiateSize', 'renegotiateMaxRecordDelay', 'secureRenegotiation', 'maxRenegotiationsPerMinute', 'serverName', 'sniDefault', 'sniRequire'
		//                clisslCert, clisslKey, clisslKeyChain, clisslCiphers, clisslPxySsl, clisslPxySslPassTh, clisslRego, prfRegoPeriod, prfRegoSize, clisslRegoMaxRcdDly, clisslSecRego, clisslMxRegoPerMin, clisslSrvName, clisslSniDft, clisslSNIRqr
		prfOptData['cert'] = $('#clisslCert option:selected').val();
		prfOptData['key'] = $('#clisslKey option:selected').val();
		prfOptData['chain'] = $('#clisslKeyChain option:selected').val();
		prfOptData['ciphers'] = $('#clisslCiphers').val();
		prfOptData['proxySsl'] = $('#clisslPxySsl option:selected').val();
		prfOptData['proxySslPassthrough'] = $('#clisslPxySslPassTh option:selected').val();
		prfOptData['renegotiation'] = $('#clisslRego option:selected').val();
		if ($('#prfRegoPeriod option:selected').val() == 'specify') prfOptData['renegotiatePeriod'] = $('#prfRegoPeriodSpecify').val();
		else prfOptData['renegotiatePeriod'] = $('#prfRegoPeriod option:selected').val();
		if ($('#prfRegoSize option:selected').val() == 'specify') prfOptData['renegotiateSize'] = $('#prfRegoSizeSpecify').val();
		else prfOptData['renegotiateSize'] = $('#prfRegoSize option:selected').val();
		if ($('#clisslRegoMaxRcdDly option:selected').val() == 'specify') prfOptData['renegotiateMaxRecordDelay'] = $('#clisslRegoMaxRcdDlySpecify').val();
		else prfOptData['renegotiateMaxRecordDelay'] = $('#clisslRegoMaxRcdDly option:selected').val();
		prfOptData['secureRenegotiation'] = $('#clisslSecRego option:selected').val();
		prfOptData['maxRenegotiationsPerMinute'] = $('#clisslMxRegoPerMin').val();
		prfOptData['serverName'] = $('#clisslSrvName').val();
		prfOptData['sniDefault'] = $('#clisslSniDft option:selected').val();
		prfOptData['sniRequire'] = $('#clisslSNIRqr option:selected').val();
	}
	else if (prfType == "SERVERSSL"){
		// defaultsFrom, 'cert', 'key', 'chain', 'ciphers', 'proxySsl', 'proxySslPassthrough', 'renegotiation', 'renegotiatePeriod', 'renegotiateSize', 'secureRenegotiation', 'serverName', 'sniDefault', 'sniRequire'
		//                srvsslCert, srvsslKey, srvsslChain, srvsslCiphers, srvsslPxySsl, srvsslPxySslPassTh, srvsslRego, prfRegoPeriod, prfRegoSize, srvsslSecRego, srvsslSrvName, srvsslSniDft, srvsslSNIRqr
		prfOptData['cert'] = $('#srvsslCert option:selected').val();
		prfOptData['key'] = $('#srvsslKey option:selected').val();
		prfOptData['chain'] = $('#srvsslChain option:selected').val();
		prfOptData['ciphers'] = $('#srvsslCiphers').val();
		prfOptData['proxySsl'] = $('#srvsslPxySsl option:selected').val();
		prfOptData['proxySslPassthrough'] = $('#srvsslPxySslPassTh option:selected').val();
		prfOptData['renegotiation'] = $('#srvsslRego option:selected').val();
		if ($('#prfRegoPeriod option:selected').val() == 'specify') prfOptData['renegotiatePeriod'] = $('#prfRegoPeriodSpecify').val();
		else prfOptData['renegotiatePeriod'] = $('#prfRegoPeriod option:selected').val();
		if ($('#prfRegoSize option:selected').val() == 'specify') prfOptData['renegotiateSize'] = $('#prfRegoSizeSpecify').val();
		else prfOptData['renegotiateSize'] = $('#prfRegoSize option:selected').val();
		prfOptData['secureRenegotiation'] = $('#srvsslSecRego option:selected').val();
		prfOptData['serverName'] = $('#srvsslSrvName').val();
		prfOptData['sniDefault'] = $('#srvsslSniDft option:selected').val();
		prfOptData['sniRequire'] = $('#srvsslSNIRqr option:selected').val();
		
	}
	else if(prfType == 'OneConnect'){
		// 'defaultsFrom', 'sourceMask', 'maxSize', 'maxAge', 'maxReuse', 'idleTimeoutOverride, 'limitType'
		if ($('#ocMask').val() == '0') prfOptData['sourceMask'] = 'any';
		else prfOptData['sourceMask'] = getMaskByCIDR($('#ocMask').val());
		prfOptData['maxSize'] = $('#ocMaxSize').val();
		prfOptData['maxAge'] = $('#ocMaxAge').val();
		prfOptData['maxReuse'] = $('#ocMaxReuse').val();
		if ($('#prfIdleTimeout option:selected').val() == 'specify') prfOptData['idleTimeoutOverride'] = $('#prfIdleTimeoutSpecify').val();
		else prfOptData['idleTimeoutOverride'] = $('#prfIdleTimeout option:selected').val();
		prfOptData['limitType'] = $('#ocLimitType option:selected').val();
	}
	else if(prfType == 'Stream'){
		// 'defaultsFrom', 'source', 'tmTarget'
		prfOptData['source'] = $('#strmSrc').val();
		prfOptData['tmTarget'] = $('#strmTgt').val();
	}
}

function prfNameProcessData(response_in) {
	var strResult = '';

	if (GetParentURLParameter('go')=='chg_profile'){
		$('#chg_svc_prf_name_select option').each(function(index) {
			if (index != 0) $(this).remove();
		});
	}
	
	//Remove existing profile types and then add new ones
	$('#svc_prf_type_select option').each(function(index) {
		if (index != 0) $(this).remove();
	});
	
	//chg_svc_prf_name_select

	$.each(response_in, function(index) {
		if (response_in[index] != "none"){
			strResult += "<option value='" + response_in[index] + "'>" + response_in[index] + "</option>";
		}
	});
	
	//alert("Return output: " + strResult);
	if (GetParentURLParameter('go')=='chg_profile'){
		$('#chg_svc_prf_name_select').append(strResult);
	}
	
	$('#svc_prf_type_select').append(strResult);
}

function iruleNameProcessData(response_in) {
	var strResult = '';
	//Remove existing profile types and then add new ones
	$('#persistIRule option').each(function(index) {
		if (index != 0) $(this).remove();
	});
	
	$.each(response_in, function(index) {
		if (response_in[index] != "none"){
			strResult += "<option value='" + response_in[index] + "'>" + response_in[index] + "</option>";
		}
	});
	
	//alert("Return output: " + strResult);
	$('#persistIRule').append(strResult);
}

function certNameProcessData(response_in) {
	var strResult = '';
	//Remove existing profile types and then add new ones
	$('#clisslCert option').each(function(index) {
		if (index != 0) $(this).remove();
	});
	$('#clisslKeyChain option').each(function(index) {
		if (index != 0) $(this).remove();
	});
	
	
	$.each(response_in, function(index) {
		if (response_in[index] != "none"){
			strResult += "<option value='" + response_in[index] + "'>" + response_in[index] + "</option>";
		}
	});
	
	//alert("Return output: " + strResult);
	$('#clisslCert').append(strResult);
	$('#clisslKeyChain').append(strResult);
}

function keyNameProcessData(response_in) {
	var strResult = '';
	//Remove existing profile types and then add new ones
	$('#clisslKey option').each(function(index) {
		if (index != 0) $(this).remove();
	});
	
	$.each(response_in, function(index) {
		if (response_in[index] != "none"){
			strResult += "<option value='" + response_in[index] + "'>" + response_in[index] + "</option>";
		}
	});
	
	//alert("Return output: " + strResult);
	$('#clisslKey').append(strResult);
}

function getHttpSettingsProcessData(response_in){
	//alert("Data: " + response_in);
	var responseArray = response_in.split('|');
	
	var prfMode = GetParentURLParameter('go');
	
	/* Debugging */

	var strResult = 'Debugging Info - Loading Http profile settings';
	$.each(responseArray, function(index) {
		strResult += responseArray[index] + "<br>";
	});
	
	$('#newprf_EvalReview').html(strResult);

	// String parsing - '/Common/parent_prf_name'
	var parPrfName = responseArray[1].split("/");
	
	// BugID 09152019-1031pm
    // Mode - Change Profile mode
    // Symptom: When a Parent profile name is changed where a user already chose a Profile name, all other profile settings are successfully loaded. 
	//          However the chosen Parent profile name is changed back to the original parent profile name
	// Sol: In Profile change mode, if Profile is not in 'initial' state (Parent Profile name is 'select') and the returned parent profile name is not
	// equal to '', then keep the current parent profile name
	
	// If the defaultsFrom property value of a profile is null, that means the profile is F5 Built-in profile.
	var orgParPrfName = $('#svc_prf_type_select').val();
	
	if (prfMode == 'chg_profile')
	{
		$('#svc_prf_proxymode_select option[value="' + responseArray[0] + '"]').attr('selected', 'selected');

		if (orgParPrfName == 'select') {
			if (responseArray[1] == '') {
				responseArray[1] = 'select';
				$('#svc_prf_type_select option[value="' + responseArray[1] + '"]').prop('selected', 'selected');
			}
			else {
					$('#svc_prf_type_select option[value="' + parPrfName[2] + '"]').prop('selected', 'selected');
			}
		}
		else {
			if (responseArray[1] == '') {
				$('#svc_prf_type_select option[value="' + responseArray[1] + '"]').prop('selected', 'selected');
			}
			else{
				$('#svc_prf_type_select option[value="' + orgParPrfName + '"]').prop('selected', 'selected');	
			} 
		}

	}
	
	$('#httpBasicAuth').val(responseArray[2]);
	$('#httpFallbackHost').val(responseArray[3]);
	$('#httpFallbackErrorCodes').val(responseArray[4]);
	$('#httpReqHdrErase').val(responseArray[5]);
	$('#httpReqHdrInsert').val(responseArray[6]);
	$('#httpReqChunk option[value="' + responseArray[7] + '"]').attr('selected', 'selected');
	$('#httpRespChunk option[value="' + responseArray[8] + '"]').attr('selected', 'selected');
	//$('#httpXFF option:selected').val(responseArray[9]);
	$('#httpXFF option[value="' + responseArray[9] + '"]').attr('selected', 'selected');
	$('#httpAgentName').val(responseArray[10]);
	if(responseArray[11] != ''){
		$('#httpDnsResolver option[value="' + responseArray[11] + '"]').attr('selected', 'selected');
	}
}

function getPrfSettingsProcessData(response_in){
	var responseArray = response_in.split('|');

	/* Debugging */
	/*
	var strResult = '';
	$.each(responseArray, function(index) {
		strResult += responseArray[index] + "<br>";
	});
	
	$('#newprf_EvalReview').html(strResult);
	*/
	
	$('#dnsHwPrtoValid option[value="' + responseArray[1] + '"]').attr('selected', 'selected');
	$('#dnsHwRespCache option[value="' + responseArray[2] + '"]').attr('selected', 'selected');
	$('#dnsExp option[value="' + responseArray[3] + '"]').attr('selected', 'selected');
	$('#dnsGtm option[value="' + responseArray[4] + '"]').attr('selected', 'selected');
	$('#dnsUnhandledQueryAct option[value="' + responseArray[5] + '"]').attr('selected', 'selected');
	$('#dnsUseBind option[value="' + responseArray[6] + '"]').attr('selected', 'selected');
	$('#dnsZoneXfr option[value="' + responseArray[7] + '"]').attr('selected', 'selected');
	$('#dnsSecurity option[value="' + responseArray[8] + '"]').attr('selected', 'selected');
	$('#dnsRd option[value="' + responseArray[9] + '"]').attr('selected', 'selected');
	
}

function processGetProfileData(response_in, prfType){
	var responseArray = response_in.split('|');
	//alert('First Data: ' + responseArray[0] + 'Profile Type: ' + prfType);

	var prfMode = GetParentURLParameter('go');
	var parPrfName = '';
	
	/* Debugging */

	var strResult = 'Debugging Info - Loading ' + prfType + ' profile settings\n';
	$.each(responseArray, function(index) {
		strResult += responseArray[index] + "<br>";
	});
	$('#newprf_EvalReview').html(strResult);

	// String parsing - '/Common/parent_prf_name'
	parPrfName = responseArray[0].split("/");

	$('#svc_prf_type_select').prop('disabled', false);
	// If Profile mode is 'chg_profile", you must set Parent Profile name loaded from BIG-IP
	// If Profile mode is 'new_profile", Parent Profile name stays intact.
	
	// BugID 09152019-1031pm
    // Mode - Change Profile mode
    // Symptom: When a Parent profile name is changed where a user already chose a Profile name, all other profile settings are successfully loaded. 
	//          However the chosen Parent profile name is changed back to the original parent profile name
	// Sol: In Profile change mode, if Profile is not in 'initial' state (Parent Profile name is 'select') and the returned parent profile name is not
	// equal to '', then keep the current parent profile name
	
	// If the defaultsFrom property value of a profile is null, that means the profile is F5 Built-in profile.
	var orgParPrfName = $('#svc_prf_type_select').val();
	
	if (prfMode == 'chg_profile')
	{
		if (orgParPrfName == 'select') {
			if (responseArray[0] == '') {
				responseArray[0] = 'select';
				$('#svc_prf_type_select option[value="' + responseArray[0] + '"]').prop('selected', 'selected');
				$('#svc_prf_type_select').prop('disabled', true);
			}
			else {
				$('#svc_prf_type_select').prop('disabled', false);
				$('#svc_prf_type_select option[value="' + parPrfName[2] + '"]').prop('selected', 'selected');
			}
		}
		else {
			if (responseArray[0] == '') {
				$('#svc_prf_type_select option[value="' + responseArray[0] + '"]').prop('selected', 'selected');
				$('#svc_prf_type_select').prop('disabled', true);
			}
			else{
				$('#svc_prf_type_select').prop('disabled', false);
				$('#svc_prf_type_select option[value="' + orgParPrfName + '"]').prop('selected', 'selected');	
			} 
		}

	}

	alert("Profile Type: " + prfMode + "\nParent Profile name: " + parPrfName + "\nresponseArrya[0] value: " + responseArray[0] );
	if(prfType == 'DNS'){
		$('#dnsHwPrtoValid option[value="' + responseArray[1] + '"]').attr('selected', 'selected');
		$('#dnsHwRespCache option[value="' + responseArray[2] + '"]').attr('selected', 'selected');
		$('#dnsExp option[value="' + responseArray[3] + '"]').attr('selected', 'selected');
		$('#dnsGtm option[value="' + responseArray[4] + '"]').attr('selected', 'selected');
		$('#dnsUnhandledQueryAct option[value="' + responseArray[5] + '"]').attr('selected', 'selected');
		$('#dnsUseBind option[value="' + responseArray[6] + '"]').attr('selected', 'selected');
		$('#dnsZoneXfr option[value="' + responseArray[7] + '"]').attr('selected', 'selected');
		$('#dnsSecurity option[value="' + responseArray[8] + '"]').attr('selected', 'selected');
		$('#dnsRd option[value="' + responseArray[9] + '"]').attr('selected', 'selected');
	}
	else if(prfType == 'Cookie'){
		$('#ckMethod option[value="' + responseArray[1] + '"]').attr('selected', 'selected');
		$('#ckName').val(responseArray[2]);
		$('#ckHttpOnly option[value="' + responseArray[3] + '"]').attr('selected', 'selected');
		$('#ckSecure option[value="' + responseArray[4] + '"]').attr('selected', 'selected');
		if (responseArray[5] == 'enabled') $('#ckAlzSend').prop('checked', true);	
		else  $('#ckAlzSend').prop('checked', false);
		// If cookie expiration is '' (session cookie), replace the '' with '0'
		if (responseArray[6] == '') $('#ckExp').val('0')
		else $('#ckExp').val(responseArray[6]);
		$('#ckConnLimit option[value="' + responseArray[7] + '"]').attr('selected', 'selected');
	}
	else if(prfType == 'DestAddrAffinity'){
		$('#dstXSvc option[value="' + responseArray[1] + '"]').attr('selected', 'selected');
		$('#dstXVs option[value="' + responseArray[2] + '"]').attr('selected', 'selected');
		$('#dstXP option[value="' + responseArray[3] + '"]').attr('selected', 'selected');
		$('#dstHash option[value="' + responseArray[4] + '"]').attr('selected', 'selected');
		if(responseArray[5] == 'indefinite') $('#dstTimeout').val('0');
		else  $('#dstTimeout').val(responseArray[5]);
		if(responseArray[6] == 'none') $('#dstMask').val('0'); 
		else $('#dstMask').val(getCIDRByMask(responseArray[6]));
		$('#dstConnLimit option[value="' + responseArray[7] + '"]').attr('selected', 'selected');
	}
	else if(prfType == 'SrcAddrAffinity'){
		$('#srcXSvc option[value="' + responseArray[1] + '"]').attr('selected', 'selected');
		$('#srcXVs option[value="' + responseArray[2] + '"]').attr('selected', 'selected');
		$('#srcXP option[value="' + responseArray[3] + '"]').attr('selected', 'selected');
		$('#srcHash option[value="' + responseArray[4] + '"]').attr('selected', 'selected');
		if(responseArray[5] == 'indefinite') $('#srcTimeout').val('0');
		else  $('#srcTimeout').val(responseArray[5]);
		if(responseArray[6] == 'none') $('#srcMask').val('0'); 
		else $('#srcMask').val(getCIDRByMask(responseArray[6]));
		$('#srcMapPrxy option[value="' + responseArray[7] + '"]').attr('selected', 'selected');
		$('#srcConnLimit option[value="' + responseArray[8] + '"]').attr('selected', 'selected');
	}
	else if(prfType == 'Hash'){
		$('#hsXSvc option[value="' + responseArray[1] + '"]').attr('selected', 'selected');
		$('#hsXVs option[value="' + responseArray[2] + '"]').attr('selected', 'selected');
		$('#hsXP option[value="' + responseArray[3] + '"]').attr('selected', 'selected');
		$('#hsHash option[value="' + responseArray[4] + '"]').attr('selected', 'selected');
		$('#hsOffset').val(responseArray[5]);
		$('#hsLen').val(responseArray[6]);
		$('#hsSPtn').val(responseArray[7]);
		$('#hsEPtn').val(responseArray[8]);
		$('#hsBfLimit').val(responseArray[9]);
		if(responseArray[10] == 'indefinite') $('#hsTimeout').val('0');
		else  $('#hsTimeout').val(responseArray[10]);
		$('#persistIRule option[value="' + responseArray[11] + '"]').attr('selected', 'selected');
		$('#hsConnLimit option[value="' + responseArray[12] + '"]').attr('selected', 'selected');
	}
	else if(prfType == 'SSL'){
		$('#sslXSvc option[value="' + responseArray[1] + '"]').attr('selected', 'selected');
		$('#sslXVs option[value="' + responseArray[2] + '"]').attr('selected', 'selected');
		$('#sslXP option[value="' + responseArray[3] + '"]').attr('selected', 'selected');
		if(responseArray[4] == 'indefinite') $('#sslTimeout').val('0');
		else  $('#sslTimeout').val(responseArray[4]);
		$('#sslConnLimit option[value="' + responseArray[5] + '"]').attr('selected', 'selected');
	}
	else if(prfType == 'Universal'){
		$('#uniXSvc option[value="' + responseArray[1] + '"]').attr('selected', 'selected');
		$('#uniXVs option[value="' + responseArray[2] + '"]').attr('selected', 'selected');
		$('#uniXP option[value="' + responseArray[3] + '"]').attr('selected', 'selected');
		if(responseArray[4] == 'indefinite') $('#uniTimeout').val('0');
		else  $('#uniTimeout').val(responseArray[4]);
		if (responseArray[5] == ''){
			$('#persistIRule option[value="select"]').attr('selected', 'selected');
		}
		else{
			var prfiRuleName = responseArray[5].split("/");
			$('#persistIRule option[value="' + prfiRuleName[2] + '"]').attr('selected', 'selected');
		}
			
		$('#uniConnLimit option[value="' + responseArray[6] + '"]').attr('selected', 'selected');
	}
	else if (prfType == "FastL4"){
		$('#f4ResetTO option[value="' + responseArray[1] + '"]').attr('selected', 'selected');
		$('#f4RzmbFrgmt option[value="' + responseArray[2] + '"]').attr('selected', 'selected');
		if(responseArray[3] == 'immediate' || responseArray[3] == 'indefinite') $('#prfIdleTimeout option[value="' + responseArray[3] + '"]').attr('selected', 'selected');
		else{
			$('#prfIdleTimeout option[value="specify"]').attr('selected', 'selected');
			$('#prfIdleTimeoutSpecify').prop('disabled', false);
			$('#prfIdleTimeoutSpecify').val(responseArray[3]);
		}

		if(responseArray[4] == 'disabled' || responseArray[4] == 'indefinite') $('#f4TcpHSTO option[value="' + responseArray[4] + '"]').attr('selected', 'selected');
		else{
			$('#f4TcpHSTO option[value="specify"]').attr('selected', 'selected');
			$('#f4TcpHSTOSpecify').prop('disabled', false);
			$('#f4TcpHSTOSpecify').val(responseArray[4]);
		}

		$('#f4TcpTSMode option[value="' + responseArray[5] + '"]').attr('selected', 'selected');
		$('#f4TcpWsMode option[value="' + responseArray[6] + '"]').attr('selected', 'selected');
		$('#f4LsInit option[value="' + responseArray[7] + '"]').attr('selected', 'selected');
		$('#f4LsCls option[value="' + responseArray[8] + '"]').attr('selected', 'selected');

		if(responseArray[9] == 'immediate' || responseArray[9] == 'indefinite') $('#f4TcpClsTO option[value="' + responseArray[9] + '"]').attr('selected', 'selected');
		else{
			$('#f4TcpClsTO option[value="specify"]').attr('selected', 'selected');
			$('#f4TcpClsTOSpecify').prop('disabled', false);
			$('#f4TcpClsTOSpecify').val(responseArray[9]);
		}

		if(responseArray[10] == 'disabled') $('#f4KeepIntvl option[value="' + responseArray[10] + '"]').attr('selected', 'selected');
		else{
			$('#f4KeepIntvl option[value="specify"]').attr('selected', 'selected');
			$('#f4KeepIntvlSpecify').prop('disabled', false);
			$('#f4KeepIntvlSpecify').val(responseArray[10]);
		}		
	}
	else if (prfType == "TCP"){
		$('#tcpRstOnTO option[value="' + responseArray[1] + '"]').attr('selected', 'selected');
		$('#tcpPxyBfHigh').val(responseArray[2]);
		$('#tcpPxyBfLow').val(responseArray[3]);
		$('#tcpRcvWin').val(responseArray[4]);
		$('#tcpSndBfSz').val(responseArray[5]);
		$('#tcpAckOnPush option[value="' + responseArray[6] + '"]').attr('selected', 'selected');
		$('#tcpNagle option[value="' + responseArray[7] + '"]').attr('selected', 'selected');
		$('#tcpInitCwnd').val(responseArray[8]);
		$('#tcpSlowStart option[value="' + responseArray[9] + '"]').attr('selected', 'selected');
		$('#tcpSltvAcks option[value="' + responseArray[10] + '"]').attr('selected', 'selected');
	}
	else if (prfType == "UDP"){
		$('#udpPxyMss option[value="' + responseArray[1] + '"]').attr('selected', 'selected');
		if(responseArray[2] == 'immediate' || responseArray[2] == 'indefinite') $('#prfIdleTimeout option[value="' + responseArray[2] + '"]').attr('selected', 'selected');
		else{
			$('#prfIdleTimeout option[value="specify"]').attr('selected', 'selected');
			$('#prfIdleTimeoutSpecify').prop('disabled', false);
			$('#prfIdleTimeoutSpecify').val(responseArray[2]);
		}
		if(responseArray[3] == 'pass-through' || responseArray[3] == 'mimic') $('#udpIpToS option[value="' + responseArray[3] + '"]').attr('selected', 'selected');
		else{
			$('#udpIpToS option[value="specify"]').attr('selected', 'selected');
			$('#udpIpToSSpecify').prop('disabled', false);
			$('#udpIpToSSpecify').val(responseArray[3]);
		}
		if(responseArray[4] == 'pass-through') $('#udpLkQoS option[value="' + responseArray[4] + '"]').attr('selected', 'selected');
		else{
			$('#udpLkQoS option[value="specify"]').attr('selected', 'selected');
			$('#udpLkQoSSpecify').prop('disabled', false);
			$('#udpLkQoSSpecify').val(responseArray[4]);
		}		
		$('#udpDGLB option[value="' + responseArray[5] + '"]').attr('selected', 'selected');
		$('#udpNoPayload option[value="' + responseArray[6] + '"]').attr('selected', 'selected');
		$('#udpTtlMode option[value="' + responseArray[7] + '"]').attr('selected', 'selected');
		$('#udpTtlV4').val(responseArray[8]);
		$('#udpTtlV6').val(responseArray[9]);
		$('#udpDfMode option[value="' + responseArray[10] + '"]').attr('selected', 'selected');
		
	}
	else if (prfType == "CLIENTSSL"){
		$('#clisslCert option[value="' + responseArray[1] + '"]').attr('selected', 'selected');
		$('#clisslKey option[value="' + responseArray[2] + '"]').attr('selected', 'selected');
		$('#clisslKeyChain option[value="' + responseArray[3] + '"]').attr('selected', 'selected');
		$('#clisslCiphers').val(responseArray[4]);
		$('#clisslPxySsl option[value="' + responseArray[5] + '"]').attr('selected', 'selected');
		$('#clisslPxySslPassTh option[value="' + responseArray[6] + '"]').attr('selected', 'selected');
		$('#clisslRego option[value="' + responseArray[7] + '"]').attr('selected', 'selected');
		if(responseArray[8] == 'indefinite') $('#prfRegoPeriod option[value="' + responseArray[8] + '"]').attr('selected', 'selected');
		else{
			$('#prfRegoPeriod option[value="specify"]').attr('selected', 'selected');
			$('#prfRegoPeriodSpecify').prop('disabled', false);
			$('#prfRegoPeriodSpecify').val(responseArray[8]);
		}
		if(responseArray[9] == 'indefinite') $('#prfRegoSize option[value="' + responseArray[9] + '"]').attr('selected', 'selected');
		else{
			$('#prfRegoSize option[value="specify"]').attr('selected', 'selected');
			$('#prfRegoSizeSpecify').prop('disabled', false);
			$('#prfRegoSizeSpecify').val(responseArray[9]);
		}
		if(responseArray[10] == 'indefinite') $('#clisslRegoMaxRcdDly option[value="' + responseArray[10] + '"]').attr('selected', 'selected');
		else{
			$('#clisslRegoMaxRcdDly option[value="specify"]').attr('selected', 'selected');
			$('#clisslRegoMaxRcdDlySpecify').prop('disabled', false);
			$('#clisslRegoMaxRcdDlySpecify').val(responseArray[10]);
		}
		
		$('#clisslSecRego option[value="' + responseArray[11] + '"]').attr('selected', 'selected');
		$('#clisslMxRegoPerMin').val(responseArray[12]);
		$('#clisslSrvName').val(responseArray[13]);
		$('#clisslSniDft option[value="' + responseArray[14] + '"]').attr('selected', 'selected');
		$('#clisslSNIRqr option[value="' + responseArray[15] + '"]').attr('selected', 'selected');
	}
	else if (prfType == "SERVERSSL"){
		$('#srvsslCert option[value="' + responseArray[1] + '"]').attr('selected', 'selected');
		$('#srvsslKey option[value="' + responseArray[2] + '"]').attr('selected', 'selected');
		$('#srvsslChain option[value="' + responseArray[3] + '"]').attr('selected', 'selected');
		$('#srvsslCiphers').val(responseArray[4]);
		$('#srvsslPxySsl option[value="' + responseArray[5] + '"]').attr('selected', 'selected');
		$('#srvsslPxySslPassTh option[value="' + responseArray[6] + '"]').attr('selected', 'selected');
		$('#srvsslRego option[value="' + responseArray[7] + '"]').attr('selected', 'selected');
		if(responseArray[8] == 'indefinite') $('#prfRegoPeriod option[value="' + responseArray[8] + '"]').attr('selected', 'selected');
		else{
			$('#prfRegoPeriod option[value="specify"]').attr('selected', 'selected');
			$('#prfRegoPeriodSpecify').prop('disabled', false);
			$('#prfRegoPeriodSpecify').val(responseArray[8]);
		}
		if(responseArray[9] == 'indefinite') $('#prfRegoSize option[value="' + responseArray[9] + '"]').attr('selected', 'selected');
		else{
			$('#prfRegoSize option[value="specify"]').attr('selected', 'selected');
			$('#prfRegoSizeSpecify').prop('disabled', false);
			$('#prfRegoSizeSpecify').val(responseArray[9]);
		}
		
		$('#srvsslSecRego option[value="' + responseArray[10] + '"]').attr('selected', 'selected');
		$('#srvsslSrvName').val(responseArray[11]);
		$('#srvsslSniDft option[value="' + responseArray[12] + '"]').attr('selected', 'selected');
		$('#srvsslSNIRqr option[value="' + responseArray[13] + '"]').attr('selected', 'selected');
		
	}
	else if(prfType == 'OneConnect'){
		if(responseArray[1] == 'any') $('#ocMask').val('0'); 
		else $('#ocMask').val(getCIDRByMask(responseArray[1]));
		$('#ocMaxSize').val(responseArray[2]);
		$('#ocMaxAge').val(responseArray[3]);
		$('#ocMaxReuse').val(responseArray[4]);
		if(responseArray[5] == 'disabled' || responseArray[5] == 'indefinite') $('#prfIdleTimeout option[value="' + responseArray[5] + '"]').attr('selected', 'selected');
		else{
			$('#prfIdleTimeout option[value="specify"]').attr('selected', 'selected');
			$('#prfIdleTimeoutSpecify').prop('disabled', false);
			$('#prfIdleTimeoutSpecify').val(responseArray[5]);
		}
		$('#ocLimitType option[value="' + responseArray[6] + '"]').attr('selected', 'selected');
	}
	else if(prfType == 'Stream'){
		$('#strmSrc').val(responseArray[1]);
		$('#strmTgt').val(responseArray[2]);		
	}
}


function newProfileBuildProcessData(response_in) {
	var strResult = '';
	$.each(response_in, function(index) {
		if(index == 0) 
			strResult = "<b>" + response_in[index] + "</b><br>";
		else
			strResult += response_in[index] + "<br>";
	});
	
	//alert("Return output: " + strResult);
	$('#newprf_EvalReview').html(strResult);	
}

function processBuildProfileData(response_in, prfType) {
	var strResult = '';

	$.each(response_in, function(index) {
		if(index == 0) 
			strResult = "<b>" + response_in[index] + "</b><br>";
		else
			strResult += response_in[index] + "<br>";
	});
	
	$('#newprf_EvalReview').html(strResult);	
}

function getPrfHtml(prfType, parPrfName){
	var strHtml = '';
	if(prfType == 'DNS'){
		//'defaultsFrom', 'enableHardwareQueryValidation', 'enableHardwareResponseCache', 'enableDnsExpress', 'enableGtm', 'unhandledQueryAction', 'useLocalBind', 'processXfr','enableDnsFirewall', 'processRd'
		strHtml += "<tr id='r1'><td width='132px' ><label>Hardware Acceleration(Protocol Validation)</label></td><td><select id='dnsHwPrtoValid' ><option value='yes' >Enabled</option><option value='no' selected>Disabled</option></select></td></tr>";
		strHtml += "<tr id='r2'><td width='132px' ><label>Hardware Acceleration(Response Cache)</label></td><td><select id='dnsHwRespCache' ><option value='yes' >Enabled</option><option value='no' selected>Disabled</option></select></td></tr>";
		strHtml += "<tr id='r3'><td width='132px' ><label>DNS Express</label></td><td><select id='dnsExp' ><option value='yes' selected >Enabled</option><option value='no'>Disabled</option></select></td></tr>";
		strHtml += "<tr id='r4'><td width='132px' ><label>GSLB</label></td><td><select id='dnsGtm' ><option value='yes' selected >Enabled</option><option value='no'>Disabled</option></select></td></tr>";
		strHtml += "<tr id='r5'><td width='132px' ><label>Unhandled Query Actions</label></td><td><select id='dnsUnhandledQueryAct' ><option value='allow' selected >Allow</option><option value='drop'>Drop</option><option value='reject'>Reject</option><option value='hint'>Hint</option><option value='noerror'>No Error</option></select></td></tr>";
		strHtml += "<tr id='r6'><td width='132px' ><label>Use BIND Server on BIG-IP</label></td><td><select id='dnsUseBind' ><option value='yes' selected >Enabled</option><option value='no'>Disabled</option></select></td></tr>";
		strHtml += "<tr id='r7'><td width='132px' ><label>Zone Transfer</label></td><td><select id='dnsZoneXfr' ><option value='yes' >Enabled</option><option value='no' selected>Disabled</option></select></td></tr>";
		strHtml += "<tr id='r8'><td width='132px' ><label>DNS Security</label></td><td><select id='dnsSecurity' ><option value='yes' >Enabled</option><option value='no' selected>Disabled</option></select></td></tr>";
		strHtml += "<tr id='r9'><td width='132px' ><label>Process Recursion Desired</label></td><td><select id='dnsRd' ><option value='yes' selected>Enabled</option><option value='no'>Disabled</option></select></td></tr>";
	}
	else if(prfType == 'Cookie') {
		//'defaultsFrom', 'method'- Cookie method(hash, insert, passive, rewrite), 'cookieName', 'httponly', 'secure', 'alwaysSend', 'expiration', 'overrideConnectionLimit'
		strHtml += "<tr id='r1'><td width='132px' ><label>Cookie Method</label></td><td><select id='ckMethod' ><option value='hash'>Cookie Hash</option><option value='insert' selected>HTTP Cookie Insert</option><option value='passive'>HTTP Cookie Passive</option><option value='rewrite'>HTTP Cookie Rewrite</option></select></td></tr>";
		strHtml += "<tr id='r2'><td width='132px' ><label>Cookie Name</label></td><td><input type='text' id='ckName' /><br><p>** Cookie name is requred if the method is Cookie Hash or Cookie Passive</p><td></tr>";
		strHtml += "<tr id='r3'><td width='132px' ><label>HTTPOnly Attribute</label></td><td><select id='ckHttpOnly' ><option value='enabled'>Enabled</option><option value='disabled' selected>Disabled</option></select></td></tr>";
		strHtml += "<tr id='r4'><td width='132px' ><label>Secure Attribute</label></td><td><select id='ckSecure' ><option value='enabled'>Enabled</option><option value='disabled' selected>Disabled</option></select></td></tr>";
		strHtml += "<tr id='r5'><td width='132px' ><label>Always Send Cookie</label></td><td><input type='checkbox' id='ckAlzSend' value='enabled'/></td></tr>";
		strHtml += "<tr id='r6'><td width='132px' ><label>Expiration</label></td><td><input type='text' id='ckExp' value='0' /><br><p> Note: 0 - Session Cookie. To specify specific expiration period, use D:H:M:S format.</p></td></tr>";
		strHtml += "<tr id='r7'><td width='132px' ><label>Override Connection Limit</label></td><td><select id='ckConnLimit' ><option value='enabled' selected>Enabled</option><option value='disabled'>Disabled</option></select></td></tr>";
		
	}
	else if(prfType == 'DestAddrAffinity') {
		//'defaultsFrom', 'matchAcrossServices', 'matchAcrossVirtuals', 'matchAcrossPools','hashAlgorithm', 'timeout', 'mask', 'overrideConnectionLimit'
		strHtml += "<tr id='r1'><td width='132px' ><label>Match Across Services</label></td><td><select id='dstXSvc' ><option value='enabled'>Enabled</option><option value='disabled' selected>Disabled</option></select></td></tr>";
		strHtml += "<tr id='r2'><td width='132px' ><label>Match Across Virtual Servers</label></td><td><select id='dstXVs' ><option value='enabled'>Enabled</option><option value='disabled' selected>Disabled</option></select></td></tr>";
		strHtml += "<tr id='r3'><td width='132px' ><label>Match Across Pools</label></td><td><select id='dstXP' ><option value='enabled'>Enabled</option><option value='disabled' selected>Disabled</option></select></td></tr>";
		strHtml += "<tr id='r4'><td width='132px' ><label>Hash Algorithm</label></td><td><select id='dstHash' ><option value='default' selected>Default</option><option value='carp'>CARP</option></select></td></tr>";
		strHtml += "<tr id='r5'><td width='132px' ><label>Timeout</label></td><td><input type='text' id='dstTimeout' value='180'/>seconds<br><p>* Use 0 for indefinite.</p></td></tr>";
		strHtml += "<tr id='r6'><td width='132px' ><label>Prefix Length</label></td><td><input type='text' id='dstMask' value='0'/><br><p>* CIDR number without '/'</p></td></tr>";
		strHtml += "<tr id='r7'><td width='132px' ><label>Override Connection Limit</label></td><td><select id='dstConnLimit' ><option value='disabled' selected>Disabled</option><option value='enabled'>Enabled</option></select></td></tr>";
	}
	else if(prfType == 'SrcAddrAffinity') {
		//'defaultsFrom', 'matchAcrossServices', 'matchAcrossVirtuals', 'matchAcrossPools','hashAlgorithm', 'timeout', 'mask', 'mapProxies', 'overrideConnectionLimit'
		strHtml += "<tr id='r1'><td width='132px' ><label>Match Across Services</label></td><td><select id='srcXSvc' ><option value='enabled'>Enabled</option><option value='disabled' selected>Disabled</option></select></td></tr>";
		strHtml += "<tr id='r2'><td width='132px' ><label>Match Across Virtual Servers</label></td><td><select id='srcXVs' ><option value='enabled'>Enabled</option><option value='disabled' selected>Disabled</option></select></td></tr>";
		strHtml += "<tr id='r3'><td width='132px' ><label>Match Across Pools</label></td><td><select id='srcXP' ><option value='enabled'>Enabled</option><option value='disabled' selected>Disabled</option></select></td></tr>";
		strHtml += "<tr id='r4'><td width='132px' ><label>Hash Algorithm</label></td><td><select id='srcHash' ><option value='default' selected>Default</option><option value='carp'>CARP</option></select></td></tr>";
		strHtml += "<tr id='r5'><td width='132px' ><label>Timeout</label></td><td><input type='text' id='srcTimeout' value='180'/>seconds<br><p>* Use 0 for indefinite.</p></td></tr>";
		strHtml += "<tr id='r6'><td width='132px' ><label>Prefix Length</label></td><td><input type='text' id='srcMask' value='0'/><br><p>* CIDR number without '/'</p></td></tr>";
		strHtml += "<tr id='r7'><td width='132px' ><label>Map Proxies</label></td><td><select id='srcMapPrxy' ><option value='enabled' selected>Enabled</option><option value='disabled'>Disabled</option></select></td></tr>";
		strHtml += "<tr id='r8'><td width='132px' ><label>Override Connection Limit</label></td><td><select id='srcConnLimit' ><option value='disabled' selected>Disabled</option><option value='enabled'>Enabled</option></select></td></tr>";
	}
	else if(prfType == 'Hash') {
		//defaultsFrom, matchAcrossServices, matchAcrossVirtuals, matchAcrossPools, hashAlgorithm, hashOffset, hashLength, hashStartPattern, hashEndPattern, hashBufferLimit, timeout, rule, overrideConnectionLimit
		strHtml += "<tr id='r1'><td width='132px' ><label>Match Across Services</label></td><td><select id='hsXSvc' ><option value='enabled'>Enabled</option><option value='disabled' selected>Disabled</option></select></td></tr>";
		strHtml += "<tr id='r2'><td width='132px' ><label>Match Across Virtual Servers</label></td><td><select id='hsXVs' ><option value='enabled'>Enabled</option><option value='disabled' selected>Disabled</option></select></td></tr>";
		strHtml += "<tr id='r3'><td width='132px' ><label>Match Across Pools</label></td><td><select id='hsXP' ><option value='enabled'>Enabled</option><option value='disabled' selected>Disabled</option></select></td></tr>";
		strHtml += "<tr id='r4'><td width='132px' ><label>Hash Algorithm</label></td><td><select id='hsHash' ><option value='default' selected>Default</option><option value='carp'>CARP</option></select></td></tr>";
		strHtml += "<tr id='r5'><td width='132px' ><label>Hash Offset</label></td><td><input type='text' id='hsOffset' value='0'/></td></tr>";
		strHtml += "<tr id='r6'><td width='132px' ><label>Hash Length</label></td><td><input type='text' id='hsLen' value='0'/></td></tr>";
		strHtml += "<tr id='r7'><td width='132px' ><label>Hash Start Pattern</label></td><td><input type='text' id='hsSPtn' value=''/></td></tr>";
		strHtml += "<tr id='r8'><td width='132px' ><label>Hash End Pattern</label></td><td><input type='text' id='hsEPtn' value=''/></td></tr>";
		strHtml += "<tr id='r9'><td width='132px' ><label>Hash Buffer Limit</label></td><td><input type='text' id='hsBfLimit' value='0'/></td></tr>";
		strHtml += "<tr id='r10'><td width='132px' ><label>Timeout</label></td><td><input type='text' id='hsTimeout' value='180'/></td></tr>";
		strHtml += "<tr id='r11'><td width='132px' ><label>Rule</label></td><td><select id='persistIRule' ><option value='none' selected>Select...</option></select></td></tr>";
		strHtml += "<tr id='r12'><td width='132px' ><label>Override Connection Limit</label></td><td><select id='hsConnLimit' ><option value='disabled' selected>Disabled</option><option value='enabled'>Enabled</option></select></td></tr>";
	}
	else if(prfType == 'SSL') {
		//defaultsFrom, matchAcrossServices, matchAcrossVirtuals, matchAcrossPools, timeout, overrideConnectionLimit
		strHtml += "<tr id='r1'><td width='132px' ><label>Match Across Services</label></td><td><select id='sslXSvc' ><option value='enabled'>Enabled</option><option value='disabled' selected>Disabled</option></select></td></tr>";
		strHtml += "<tr id='r2'><td width='132px' ><label>Match Across Virtual Servers</label></td><td><select id='sslXVs' ><option value='enabled'>Enabled</option><option value='disabled' selected>Disabled</option></select></td></tr>";
		strHtml += "<tr id='r3'><td width='132px' ><label>Match Across Pools</label></td><td><select id='sslXP' ><option value='enabled'>Enabled</option><option value='disabled' selected>Disabled</option></select></td></tr>";
		strHtml += "<tr id='r4'><td width='132px' ><label>Timeout</label></td><td><input type='text' id='sslTimeout' value='300'/></td></tr>";
		strHtml += "<tr id='r5'><td width='132px' ><label>Override Connection Limit</label></td><td><select id='sslConnLimit' ><option value='disabled' selected>Disabled</option><option value='enabled'>Enabled</option></select></td></tr>";
		
	}
	else if(prfType == 'Universal') {
		//defaultsFrom, matchAcrossServices, matchAcrossVirtuals, matchAcrossPools, timeout, rule, overrideConnectionLimit
		strHtml += "<tr id='r1'><td width='132px' ><label>Match Across Services</label></td><td><select id='uniXSvc' ><option value='enabled'>Enabled</option><option value='disabled' selected>Disabled</option></select></td></tr>";
		strHtml += "<tr id='r2'><td width='132px' ><label>Match Across Virtual Servers</label></td><td><select id='uniXVs' ><option value='enabled'>Enabled</option><option value='disabled' selected>Disabled</option></select></td></tr>";
		strHtml += "<tr id='r3'><td width='132px' ><label>Match Across Pools</label></td><td><select id='uniXP' ><option value='enabled'>Enabled</option><option value='disabled' selected>Disabled</option></select></td></tr>";
		strHtml += "<tr id='r4'><td width='132px' ><label>Timeout</label></td><td><input type='text' id='uniTimeout' value='180'/></td></tr>";
		strHtml += "<tr id='r5'><td width='132px' ><label>Rule</label></td><td><select id='persistIRule' ><option value='select' selected>Select...</option></select></td></tr>";
		strHtml += "<tr id='r6'><td width='132px' ><label>Override Connection Limit</label></td><td><select id='uniConnLimit' ><option value='disabled' selected>Disabled</option><option value='enabled'>Enabled</option></select></td></tr>";
		
	}
	else if (prfType == "FastL4"){
		//defaultsFrom, resetOnTimeout, reassembleFragments, idleTimeout, tcpHandshakeTimeout, tcpTimestampMode, tcpWscaleMode, looseInitialization, looseClose, tcpCloseTimeout, keepAliveInterval
		strHtml += "<tr id='r1'><td width='132px' ><label>Reset on Timeout</label></td><td><select id='f4ResetTO' ><option value='enabled' selected>Enabled</option><option value='disabled'>Disabled</option></select></td></tr>";
		strHtml += "<tr id='r2'><td width='132px' ><label>Reassemble IP Fragment</label></td><td><select id='f4RzmbFrgmt' ><option value='enabled'>Enabled</option><option value='disabled' selected>Disabled</option></select></td></tr>";
		strHtml += "<tr id='r3'><td width='132px' ><label>Idle Timeout</label></td><td><select id='prfIdleTimeout' ><option value='specify' selected>Specify</option><option value='immediate'>Immediate</option><option value='indefinite'>Indefinite</option></select><input type='text' id='prfIdleTimeoutSpecify' value='300'/> <label id='lblF4IdleTimeout'>Seconds</label></td></tr>";
		strHtml += "<tr id='r4'><td width='132px' ><label>TCP Handshake Timeout</label></td><td><select id='f4TcpHSTO' ><option value='specify' selected>Specify</option><option value='disabled'>Disabled</option><option value='indefinite'>Indefinite</option></select><input type='text' id='f4TcpHSTOSpecify' value='5' /> <label id='lblF4TcpHSTimeout'>Seconds</label></td></tr>";
		strHtml += "<tr id='r5'><td width='132px' ><label>TCP Timestamp Mode</label></td><td><select id='f4TcpTSMode' ><option value='preserve' selected>Preserve</option><option value='rewrite' selected>Rewrite</option><option value='strip'>Strip</option></select></td></tr>";
		strHtml += "<tr id='r6'><td width='132px' ><label>TCP Window Scale Mode</label></td><td><select id='f4TcpWsMode' ><option value='preserve' selected>Preserve</option><option value='strip'>Strip</option></select></td></tr>";
		strHtml += "<tr id='r7'><td width='132px' ><label>Loose Initiation</label></td><td><select id='f4LsInit' ><option value='disabled' selected>Disabled</option><option value='enabled'>Enabled</option></select></td></tr>";
		strHtml += "<tr id='r8'><td width='132px' ><label>Loose Close</label></td><td><select id='f4LsCls' ><option value='disabled' selected>Disabled</option><option value='enabled'>Enabled</option></select></td></tr>";
		strHtml += "<tr id='r9'><td width='132px' ><label>TCP Close Timeout</label></td><td><select id='f4TcpClsTO' ><option value='specify' selected>Specify</option><option value='immediate'>Immediate</option><option value='indefinite'>Indefinite</option></select><input type='text' id='f4TcpClsTOSpecify' value='5' /> <label id='lblF4TcpClsTimeout'>Seconds</label></td></tr>";
		strHtml += "<tr id='r10'><td width='132px' ><label>TCP Keep Alive Interval</label></td><td><select id='f4KeepIntvl' ><option value='disabled' selected>Disabled</option><option value='specify'>Specify</option></select><input type='text' id='f4KeepIntvlSpecify' disabled='disabled' /> <label id='lblF4KeepInterval'>Seconds</label></td></tr>";
	}
	else if (prfType == "TCP"){
		//defaultsFrom, 'resetOnTimeout', 'proxyBufferHigh', 'proxyBufferLow', 'receiveWindowSize', 'sendBufferSize', 'ackOnPush', 'nagle', 'initCwnd', 'slowStart', 'selectiveAcks'
		strHtml += "<tr id='r1'><td width='132px' ><label>Reset on Timeout</label></td><td><select id='tcpRstOnTO'><option value='disabled'>Disabled</option><option value='enabled' selected>Enabled</option></select></td></tr>";
		strHtml += "<tr id='r2'><td width='132px' ><label>Proxy Buffer High</label></td><td><input type='text' id='tcpPxyBfHigh' value='49152'/></td></tr>";
		strHtml += "<tr id='r3'><td width='132px' ><label>Proxy Buffer Low</label></td><td><input type='text' id='tcpPxyBfLow' value='32768'/></td></tr>";
		strHtml += "<tr id='r4'><td width='132px' ><label>Receive Window</label></td><td><input type='text' id='tcpRcvWin' value='65535'/></td></tr>";
		strHtml += "<tr id='r5'><td width='132px' ><label>Send Buffer</label></td><td><input type='text' id='tcpSndBfSz' value='65535'/></td></tr>";
		strHtml += "<tr id='r6'><td width='132px' ><label>Acknowledge on Push</label></td><td><select id='tcpAckOnPush'><option value='disabled'>Disabled</option><option value='enabled' selected>Enabled</option></select></td></tr>";
		strHtml += "<tr id='r7'><td width='132px' ><label>Nagle's Algorithm</label></td><td><select id='tcpNagle'><option value='disabled' selected>Disabled</option><option value='enabled'>Enabled</option></select></td></tr>";
		strHtml += "<tr id='r8'><td width='132px' ><label>Initial Congestion Window Size</label></td><td><input type='text' id='tcpInitCwnd' value='0'/></td></tr>";
		strHtml += "<tr id='r9'><td width='132px' ><label>Slow Start</label></td><td><select id='tcpSlowStart'><option value='disabled'>Disabled</option><option value='enabled' selected>Enabled</option></select></td></tr>";
		strHtml += "<tr id='r10'><td width='132px' ><label>Selective ACKs</label></td><td><select id='tcpSltvAcks'><option value='disabled'>Disabled</option><option value='enabled' selected>Enabled</option></select></td></tr>";
	}
	else if (prfType == "UDP"){
		//defaultsFrom, 'proxyMss', 'idleTimeout', 'ipTosToClient', 'linkQosToClient', 'datagramLoadBalancing', 'allowNoPayload', 'ipDfMode', 'ipTtlV4', 'ipTtlV6', 'ipDfMode'
		strHtml += "<tr id='r1'><td width='132px' ><label>Proxy Maximum Segment</label></td><td><select id='udpPxyMss'><option value='disabled' selected>Disabled</option><option value='enabled'>Enabled</option></select></td></tr>";
		strHtml += "<tr id='r2'><td width='132px' ><label>Idle Timeout</label></td><td><select id='prfIdleTimeout'><option value='immediate'>Immediate</option><option value='indefinite'>Indefinite</option><option value='specify' selected>Specify</option></select><input type='text' id='prfIdleTimeoutSpecify' value='60'/><label>Seconds</label></td></tr>";
		strHtml += "<tr id='r3'><td width='132px' ><label>IP ToS</label></td><td><select id='udpIpToS'><option value='pass-through'>Pass Through</option><option value='mimic'>Mimic</option><option value='specify' selected>Specify</option></select><input type='text' id='udpIpToSSpecify' value='0'/></td></tr>";
		strHtml += "<tr id='r4'><td width='132px' ><label>Link QoS</label></td><td><select id='udpLkQoS'><option value='pass-through'>Pass Through</option><option value='specify' selected>Specify</option></select><input type='text' id='udpLkQoSSpecify' value='0'/></td></tr>";
		strHtml += "<tr id='r5'><td width='132px' ><label>Datagram LB</label></td><td><select id='udpDGLB'><option value='enabled'>Enabled</option><option value='disabled' selected>Disabled</option></select></td></tr>";
		strHtml += "<tr id='r6'><td width='132px' ><label>Allow No Payload</label></td><td><select id='udpNoPayload'><option value='enabled'>Enabled</option><option value='disabled' selected>Disabled</option></td></tr>";
		strHtml += "<tr id='r7'><td width='132px' ><label>TTL Mode</label></td><td><select id='udpTtlMode'><option value='proxy' selected>Proxy</option><option value='preserve'>Preserve</option><option value='decrement'>Decrement</option><option value='set'>Set</option></td></tr>";
		strHtml += "<tr id='r8'><td width='132px' ><label>TTL IPv4</label></td><td><input type='text' id='udpTtlV4' value='255'/></td></tr>";
		strHtml += "<tr id='r9'><td width='132px' ><label>TTL IPv6</label></td><td><input type='text' id='udpTtlV6' value='64'/></td></tr>";
		strHtml += "<tr id='r10'><td width='132px' ><label>Don't Fragment Mode</label></td><td><select id='udpDfMode'><option value='pmtu' selected>PMTU</option><option value='preserve'>Preserve</option><option value='set'>Enable</option><option value='clear'>Disable</option></td></tr>";
		
	}
	else if (prfType == "CLIENTSSL"){
		//defaultsFrom, 'certKeyChain', 'ciphers', 'proxySsl', 'proxySslPassthrough', 'renegotiation', 'renegotiatePeriod', 'renegotiateSize', 'renegotiateMaxRecordDelay', 'secureRenegotiation', 'maxRenegotiationsPerMinute', 'serverName', 'sniDefault', 'sniRequire'
		strHtml += "<tr id='r1'><td width='132px' ><label>Certificate</label></td><td><select id='clisslCert'><option value='none' selected>None</option></select></td></tr>";
		strHtml += "<tr id='r2'><td width='132px' ><label>Key</label></td><td><select id='clisslKey'><option value='none' selected>None</option></select></td></tr>";
		strHtml += "<tr id='r3'><td width='132px' ><label>Certificate Key Chain</label></td><td><select id='clisslKeyChain'><option value='none' selected>None</option></select></td></tr>";
		strHtml += "<tr id='r4'><td width='132px' ><label>Ciphers</label></td><td><input type='text' id='clisslCiphers' value='DEFAULT'/></td></tr>";
		strHtml += "<tr id='r5'><td width='132px' ><label>Proxy SSL</label></td><td><select id='clisslPxySsl'><option value='disabled' selected>Disabled</option><option value='enabled'>Enabled</option></select></td></tr>";
		strHtml += "<tr id='r6'><td width='132px' ><label>Proxy SSL Passthrough</label></td><td><select id='clisslPxySslPassTh'><option value='disabled' selected>Disabled</option><option value='enabled'>Enabled</option></select></td></tr>";
		strHtml += "<tr id='r7'><td width='132px' ><label>Renegotiation</label></td><td><select id='clisslRego'><option value='disabled'>Disabled</option><option value='enabled' selected>Enabled</option></select></td></tr>";
		strHtml += "<tr id='r8'><td width='132px' ><label>Renegotiate Period</label></td><td><select id='prfRegoPeriod'><option value='indefinite' selected>Indefinite</option><option value='specify'>Specify</option></select><input type='text' id='prfRegoPeriodSpecify' disabled='disabled'/><label>Seconds</label></td></tr>";
		strHtml += "<tr id='r9'><td width='132px' ><label>Renegotiate Size</label></td><td><select id='prfRegoSize'><option value='indefinite' selected>Indefinite</option><option value='specify'>Specify</option></select><input type='text' id='prfRegoSizeSpecify' disabled='disabled'/><label>megabytes</label></td></tr>";
		strHtml += "<tr id='r10'><td width='132px' ><label>Renegotiate Max Record Delay</label></td><td><select id='clisslRegoMaxRcdDly'><option value='indefinite' selected>Indefinite</option><option value='specify'>Specify</option></select><input type='text' id='clisslRegoMaxRcdDlySpecify' disabled='disabled'/><label>Records</label></td></tr>";
		strHtml += "<tr id='r11'><td width='132px' ><label>Secure Renegotiation</label></td><td><select id='clisslSecRego'><option value='require' selected>Require</option><option value='request'>Request</option><option value='require-strict'>Require Strict</option></td></tr>";
		strHtml += "<tr id='r12'><td width='132px' ><label>Max Renegotiations</label></td><td><input type='text' id='clisslMxRegoPerMin' value='5' /><label>per minute</label></td></tr>";
		strHtml += "<tr id='r13'><td width='132px' ><label>Server Name</label></td><td><input type='text' id='clisslSrvName' /></td></tr>";
		strHtml += "<tr id='r14'><td width='132px' ><label>Default SSL Profile for SNI</label></td><td><select id='clisslSniDft'><option value='true'>Enabled</option><option value='false' selected>Disabled</option></select></td></tr>";
		strHtml += "<tr id='r15'><td width='132px' ><label>Require Peer SNI support</label></td><td><select id='clisslSNIRqr'><option value='true'>Enabled</option><option value='false' selected>Disabled</option></select></td></tr>";
	}
	else if (prfType == "SERVERSSL"){
		//defaultsFrom, 'cert', 'key', 'chain', 'ciphers', 'proxySsl', 'proxySslPassthrough', 'renegotiation', 'renegotiatePeriod', 'renegotiateSize', 'secureRenegotiation', 'serverName', 'sniDefault', 'sniRequire
		strHtml += "<tr id='r1'><td width='132px' ><label>Certificate</label></td><td><select id='srvsslCert'><option value='none' selected>None</option></select></td></tr>";
		strHtml += "<tr id='r2'><td width='132px' ><label>Key</label></td><td><select id='srvsslKey'><option value='none' selected>None</option></select></td></tr>";
		strHtml += "<tr id='r3'><td width='132px' ><label>Certificate Key Chain</label></td><td><select id='srvsslChain'><option value='none' selected>None</option></select></td></tr>";
		strHtml += "<tr id='r4'><td width='132px' ><label>Ciphers</label></td><td><input type='text' id='srvsslCiphers' value='DEFAULT'/></td></tr>";
		strHtml += "<tr id='r5'><td width='132px' ><label>Proxy SSL</label></td><td><select id='srvsslPxySsl'><option value='disabled' selected>Disabled</option><option value='enabled'>Enabled</option></select></td></tr>";
		strHtml += "<tr id='r6'><td width='132px' ><label>Proxy SSL Passthrough</label></td><td><select id='srvsslPxySslPassTh'><option value='disabled' selected>Disabled</option><option value='enabled'>Enabled</option></select></td></tr>";
		strHtml += "<tr id='r7'><td width='132px' ><label>Renegotiation</label></td><td><select id='srvsslRego'><option value='disabled'>Disabled</option><option value='enabled' selected>Enabled</option></select></td></tr>";
		strHtml += "<tr id='r8'><td width='132px' ><label>Renegotiate Period</label></td><td><select id='prfRegoPeriod'><option value='indefinite' selected>Indefinite</option><option value='specify'>Specify</option></select><input type='text' id='prfRegoPeriodSpecify' disabled='disabled'/><label>Seconds</label></td></tr>";
		strHtml += "<tr id='r9'><td width='132px' ><label>Renegotiate Size</label></td><td><select id='prfRegoSize'><option value='indefinite' selected>Indefinite</option><option value='specify'>Specify</option></select><input type='text' id='prfRegoSizeSpecify' disabled='disabled'/><label>megabytes</label></td></tr>";
		strHtml += "<tr id='r10'><td width='132px' ><label>Secure Renegotiation</label></td><td><select id='srvsslSecRego'><option value='require' selected>Require</option><option value='request'>Request</option><option value='require-strict'>Require Strict</option></td></tr>";
		strHtml += "<tr id='r11'><td width='132px' ><label>Server Name</label></td><td><input type='text' id='srvsslSrvName' /></td></tr>";
		strHtml += "<tr id='r12'><td width='132px' ><label>Default SSL Profile for SNI</label></td><td><select id='srvsslSniDft'><option value='true'>Enabled</option><option value='false' selected>Disabled</option></select></td></tr>";
		strHtml += "<tr id='r13'><td width='132px' ><label>Require Peer SNI support</label></td><td><select id='srvsslSNIRqr'><option value='true'>Enabled</option><option value='false' selected>Disabled</option></select></td></tr>";
	}
	else if(prfType == 'OneConnect') {
		//defaultsFrom, 'sourceMask', 'maxSize', 'maxAge', 'maxReuse', 'idleTimeoutOverride, 'limitType'
		strHtml += "<tr id='r1'><td width='132px' ><label>Source Prefix Length</label></td><td><input type='text' id='ocMask' value='0'/><br><p>* CIDR number without '/'</p></td></tr>";
		strHtml += "<tr id='r2'><td width='132px' ><label>Maximum Size</label></td><td><input type='text' id='ocMaxSize' value='10000' /></td></tr>";
		strHtml += "<tr id='r3'><td width='132px' ><label>Maximum Age</label></td><td><input type='text' id='ocMaxAge' value='86400' /></td></tr>";
		strHtml += "<tr id='r4'><td width='132px' ><label>Maximum Reuse</label></td><td><input type='text' id='ocMaxReuse' value='1000'/></td></tr>";
		//strHtml += "<tr id='r5'><td width='132px' ><label>Idle Timeout Override</label></td><td id='tdOcIdleTimeout'><select id='prfIdleTimeout' ><option value='specify'>Specify</option><option value='disabled' selected>Disabled</option><option value='indefinite'>Indefinite</option></select></td></tr>";
		strHtml += "<tr id='r5'><td width='132px' ><label>Idle Timeout Override</label></td><td id='tdOcIdleTimeout'><select id='prfIdleTimeout' ><option value='specify'>Specify</option><option value='disabled' selected>Disabled</option><option value='indefinite'>Indefinite</option></select><input type='text' id='prfIdleTimeoutSpecify' disabled='disabled' /> <label id='lblOcIdleTimeoutSpecify'>Seconds</label></td></tr>";
		strHtml += "<tr id='r6'><td width='132px' ><label>Limit Type</label></td><td><select id='ocLimitType' ><option value='none' selected>None</option><option value='idle'>Idle</option><option value='strict'>Strict</option></select></td></tr>";
	}
	else if(prfType == 'Stream') {
		//defaultsFrom, source, tmTarget
		strHtml += "<tr id='r1'><td width='132px' ><label>Source</label></td><td><input type='text' id='strmSrc' /></td></tr>";
		strHtml += "<tr id='r2'><td width='132px' ><label>Target</label></td><td><input type='text' id='strmTgt' /></td></tr>";

	}
	return strHtml;
}

function setPrfHtml(prfType, response_in){
	var strHtml = '';
	return strHtml;
}

// If a profile type is HTTP, build configuration html code accordingly (reverse, transparent, explicit)
// If Proxy mode is explicit, it requires DNS Resolver profile.
function getStrHttpHtml(pxyMode){
	// Default Page Load action - Load parent profile names
	var nameAndIp = $('#ltmSelBox option:selected').val();

	var dnsRzvs = [];
	// Get the list of DNS Resolver if HTTP proxy mode is 'explicit'. Wait for ajax transaction completed - async: false
	ajxOut = $.ajax({
		url: '/content/get_profile_names.php',
		type: 'POST',
		async: false,
		dataType: 'JSON',
		data: {method:'get_profile_names', DevIP:arr[1], LoadTypeName:prfType},
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
	ajxOut.done(function(response_in){
		var idx = 0;
		$.each(response_in, function(index) {
			if (response_in[index] != "none"){
				dnsRzvs[idx] = response_in[index];
				//alert("DNS Resolver Profile name: " + dnsRzvs[idx]);
				idx += 1;
			}
		});
	});
	
	//alert(iterArray(dnsRzvs));
	//'proxyType', 'defaultsFrom', 'basicAuthRealm', 'fallbackHost', 'fallbackStatusCodes', 'headerErase', 'headerInsert', 'insertXforwardedFor', 'serverAgentName'
	var strHtml = '';
	strHtml += "<tr id='r1'><td width='132px' ><label>Basic Auth Realm</label></td><td><input type='text' id='httpBasicAuth' /></td></tr>";
	strHtml += "<tr id='r2'><td width='132px' ><label>Fallback Host</label></td><td><input type='text' id='httpFallbackHost' /></td></tr>";
	strHtml += "<tr id='r3'><td width='132px' ><label>Fallback on Error Codes</label></td><td><input type='text' id='httpFallbackErrorCodes' /> e.g. '404 502 503' </td></tr>";
	strHtml += "<tr id='r4'><td width='132px' ><label>Request Header Erase</label></td><td><input type='text' id='httpReqHdrErase' /></td></tr>";
	strHtml += "<tr id='r5'><td width='132px' ><label>Request Header Insert</label></td><td><input type='text' id='httpReqHdrInsert' /></td></tr>";
	strHtml += "<tr id='r6'><td width='132px' ><label>Request Chunking</label></td><td><select id='httpReqChunk' ><option value='preserve' selected >Preserve</option><option value='selective' >Selective</option><option value='rechunk' >Rechunk</option></select></td></tr>";
	strHtml += "<tr id='r7'><td width='132px' ><label>Response Chunking</label></td><td><select id='httpRespChunk' ><option value='preserve' >Preserve</option><option value='selective' selected >Selective</option><option value='unchunk' >Unchunk</option><option value='rechunk' >Rechunk</option></select></td></tr>";
	strHtml += "<tr id='r8'><td width='132px' ><label>Insert X-Forwarded-For</label></td><td><select id='httpXFF' ><option value='disabled' selected >Disabled</option><option value='enabled'>Enabled</option></select></td></tr>";
	strHtml += "<tr id='r9'><td width='132px' ><label>Server Agent Name</label></td><td><input type='text' id='httpAgentName' /></td></tr>";
	if (pxyMode == "explicit"){
		strHtml += "<tr id='r10'><td width='132px' ><label>*DNS Resolver</label></td><td><select id='httpDnsResolver'><option value='select' selected>Select...</option>";
		$.each(dnsRzvs , function(index) {
			//alert("HTML Building - DNS Resolver Profile name: " + dnsRzvs[index]);
			strHtml += "<option value='" + dnsRzvs[index] +"'>" + dnsRzvs[index] + "</option>"; 
		});
		strHtml += "</select></td></tr>";
	}
	return strHtml;
}

//Read a page's GET URL variables and return them as an associate array
// e.g. URL: http://www.example.com/?me=myValue&name2=SomeOtherValue
//      Return: { "me": "myValue", "name2": "SomeOtherValue" }
function getUrlQryStrings() {
	var urlQryStrings = [], hash;
	var hashes = window.location.href.slice(window.location.href.indexOf('?') + 1).split('&');
    for(var i = 0; i < hashes.length; i++)
    {
        hash = hashes[i].split('=');
        urlQryStrings.push(hash[0]);
        urlQryStrings[hash[0]] = hash[1];
    }
    return urlQryStrings;
}

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

$(function () {
	$('#div_ltmchoice').on('change', function() {

		var nameAndIp = $('#ltmSelBox option:selected').val();
		if (nameAndIp == 'Select...') return;
		
		var arr = nameAndIp.split(":");
		//alert("Device IP: " + arr[1] + " Profile Type: " + prfType);
		
		if (GetParentURLParameter('go') == 'new_profile' | GetParentURLParameter('go') == 'chg_profile'){
			var prfType = window.parent.document.getElementById('selectedPrfType').value;
			if (prfType == 'HTTP')
				prfType = prfType + ":" + window.parent.document.getElementById('selectedPrfProxyType').value;
			
			// Retrieve DB IP address from INI file
			
			// Call Ajax to retrieve parent profile names
			ajxOut = $.ajax({
				url: '/content/get_profile_names.php',
				type: 'POST',
				dataType: 'JSON',
				data: {method:'get_profile_names', DevIP:arr[1], LoadTypeName:prfType},
				error: function(jqXHR, textStatus, errorThrown){
					alert("Ajax call to retrieve profile names has failed!");
		            console.log('jqXHR:');
		            console.log(jqXHR);
		            console.log('textStatus:');
		            console.log(textStatus);
		            console.log('errorThrown:');
		            console.log(errorThrown);
				}
			});
			ajxOut.done(prfNameProcessData);
		}
		else if (GetParentURLParameter('go') == 'del_profile'){
			loadPartitionNames(arr[1], 'prf_partition_name_select');
		}
	});
	
	$('#svc_prf_proxymode_select').on('change', function() {
		var nameAndIp = $('#ltmSelBox option:selected').val();
		var arr = nameAndIp.split(":");
		var pxyMode = $('#svc_prf_proxymode_select').val();
		var prfType = 'HTTP:'
		//alert("Proxy Mode: " + pxyMode);
		if (pxyMode == 'reverse')
			prfType += 'reverse';
		else if (pxyMode == 'explicit')
			prfType += 'explicit';
		else if (pxyMode == 'transparent')
			prfType += 'transparent';
		
		// Call Ajax to retrieve parent profile names
		ajxOut = $.ajax({
			url: '/content/get_profile_names.php',
			type: 'POST',
			dataType: 'JSON',
			data: {method:'get_profile_names', DevIP:arr[1], LoadTypeName:prfType},
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
		ajxOut.done(prfNameProcessData);
		//Clean up profile options tr except first three fixed tr
    	$('#prfConfTable_tbody tr').each(function(index) {
    		if (index > 2) $(this).remove();
    	});
	});
	
	//Dynamically add Parent profile names - Event hadnler for when a Parent Profile is selected
	$('#svc_prf_type_select').on('change', function() {

		//Profile name and parent profile name cannot be same
		if (GetParentURLParameter('go')=='chg_profile'){
			if (this.value == $('#chg_svc_prf_name_select').val()){
				// Update needed - If a current profile name and chosen parent profile name is same, revert the parent profile name back to original name 
				alert("Chosen profile name and Parent profile name can't be same!\nChosen Profile Name: " + $('#chg_svc_prf_name_select').val() + "\nParent Profile Name: " + this.value);
				return;
			}
		}
		
		//alert("Chosen Parent Name: " + $('#svc_prf_type_select').val());
		var nameAndIp = $('#ltmSelBox option:selected').val();
		var arr = nameAndIp.split(":");
		var pxyMode = $('#svc_prf_proxymode_select').val();
		var prfType = window.parent.document.getElementById('selectedPrfType').value;
		var parPrfName = $('#svc_prf_type_select').val();
		var prfMode = GetParentURLParameter('go');
		alert("Proxy Mode: " + pxyMode + "\nProfile Type: " + prfType + "\nParent Profile name: " + parPrfName + "\nProfile Mode: " + prfMode);
		var prfOptData = {'phpFileName':'', 'DevIP':'', 'name':''};

		// 1. Build configuration data structure according to the chosen profile name		
		if (prfType == "HTTP") initHttpPrfOptData(prfOptData, prfType, pxyMode);
		else initPrfOptData(prfOptData, prfType);
		
		
		// Profile Names: HTTP, DNS, Cookie, DestAddrAffinity, SrcAddrAffinity, Hash, SSL, Universal, FastL4, TCP, UDP, CLIENTSSL, SERVERSSL, OneConnect, Stream
		if (prfType == "HTTP"){
			//alert(iterAssArray(prfOptData));
			// 2. Build Dynamic configuration page according to the chosen profile name
			var strHtml = getStrHttpHtml(pxyMode);
	    	$('#prfConfTable_tbody tr').each(function(index) {
	    		if (index != 0 && index != 1 && index != 2) $(this).remove();
	    	});

			$('#prfConfTable_tbody').append(strHtml);
			// 3. Load the chosen profile configuration
			alert("Before ajax call of getHttpSettings.php. Dev IP: " + arr[1] + " Proxy Type: " + pxyMode + " Profile Type: " + prfType + " Parent Profile Name: " + parPrfName + "\n");
			ajaxOut = $.ajax({
	    		url:'/content/getHttpSettings.php',
	    		type: 'POST',
	    		data: {method:'getHttpSettings', DevIP:arr[1], ProxyType:pxyMode, LoadTypeName:prfType, PrfName:parPrfName, PrfMode:prfMode },
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
	    	ajaxOut.done(getHttpSettingsProcessData);
			
		}
		else {
			var strHtml = getPrfHtml(prfType, parPrfName);
	    	$('#prfConfTable_tbody tr').each(function(index) {
	    		if (index != 0 && index != 1) $(this).remove();
	    	});
			$('#prfConfTable_tbody').append(strHtml);

			if (prfType == 'Hash' || prfType == 'Universal'){
				// Get iRule list
				ajxOut = $.ajax({
					url: '/content/get_profile_names.php',
					type: 'POST',
					dataType: 'JSON',
					data: {method:'get_profile_names', DevIP:arr[1], LoadTypeName:'IRULE'},
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
				ajxOut.done(iruleNameProcessData);
			}
			else if (prfType == 'CLIENTSSL' || prfType == 'SERVERSSL') {
				// Get Cert and Key list
				ajxOut = $.ajax({
					url: '/content/get_profile_names.php',
					type: 'POST',
					async: false,
					dataType: 'JSON',
					data: {method:'get_profile_names', DevIP:arr[1], LoadTypeName:'CERT'},
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
				ajxOut.done(certNameProcessData);
				
				ajxOut2 = $.ajax({
					url: '/content/get_profile_names.php',
					type: 'POST',
					async: false,
					dataType: 'JSON',
					data: {method:'get_profile_names', DevIP:arr[1], LoadTypeName:'KEY'},
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
				ajxOut2.done(keyNameProcessData);
			}
			
			// 3. Load the chosen profile configuration
			ajaxOut = $.ajax({
	    		url:'/content/getPrfSettings.php',
	    		type: 'POST',
	    		data: {method:'getPrfSettings', DevIP:arr[1], LoadTypeName:prfType, ParPrfName:parPrfName, PrfMode:prfMode },
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
			ajaxOut.done(function(response_in){
				processGetProfileData(response_in, prfType);
			});			
		} 
	});
	

	// Event handler for handling the both of <select - option> and text value
	$('#prfConfTable_tbody').on('change' ,function(event) {
		//var selectedId = $('#prfConfTable_tbody').find('#prfIdleTimeout').attr('id');
		//alert("Caller ID Name: " + event.target.id);
		/*
		 * event.target.id: Retrieve the ID of the event caller. 'event' parameter must be passed through function parameter
		 */
		var callerID = event.target.id;
		if (callerID == 'prfIdleTimeout' || callerID == 'f4TcpHSTO' || callerID == 'f4TcpClsTO' || callerID == 'f4KeepIntvl' || callerID == 'udpIpToS' || callerID == 'udpLkQoS' || callerID == 'prfRegoPeriod' || callerID == 'prfRegoSize' || callerID == 'clisslRegoMaxRcdDly') {
			var selectedId = callerID;
			var selectedIdSpecify = selectedId + "Specify";
			if($('#' + selectedId + ' option:selected').val() == 'specify'){
				//alert("ID Name: " + selectedId);
				$('#' + selectedIdSpecify).prop('disabled', false);
			}
			else{
				//alert("ID Name value is not specify");
				$('#' + selectedIdSpecify).prop('disabled', true);
			}
			
		}
	});
	
	$('#prf_btn_build').on('click', function(){
		//Retrieve the element data of the parent window
		var nameAndIp = $('#ltmSelBox option:selected').val();
		var arr = nameAndIp.split(":");
		// prfName - User provided profile name
		var prfName = $('#prf_name').val();
		// pxyMode - HTTP profile only. HTTP proxy mode - reverse, explicit, transparent
		var pxyMode = $('#svc_prf_proxymode_select').val();
		// parPrfName - Parent Profile Name
		var parPrfName = $('#svc_prf_type_select').val();
		var prfType = window.parent.document.getElementById('selectedPrfType').value;
		//alert("Proxy Mode: " + pxyMode + " Profile Type: " + prfType + " Parent Profile name: " + parPrfName);
		// prfOptData has been extended with a Query string value of the Parent URL
		var prfOptData = {'phpFileName':'', 'DevIP':'', 'name':'', 'dplyOrChg':''};
		
		
		alert("prf_btn_build event in prf_jquery.js - Profile Type is: " + prfType + "\n");

		if (prfType == 'HTTP')
			prfOptData['phpFileName'] = 'new_httpProfile_build';
		else
			prfOptData['phpFileName'] = 'new_Profile_build';
		
		prfOptData['DevIP'] = arr[1];
		prfOptData['name'] = prfName;
		prfOptData['dplyOrChg'] = GetParentURLParameter('go');
		
		// 1. Build configuration data structure according to the chosen profile name		
		if (prfType == "HTTP") initHttpPrfOptData(prfOptData, prfType, pxyMode);
		else initPrfOptData(prfOptData, prfType);
		
		if (prfType == "HTTP"){
			// 2. Retrieve configuration data and save them according to the chosen profile name
			setHttpPrfOptData(prfOptData, prfType, pxyMode, parPrfName);
			//alert(iterAssArray(prfOptData));
			if( !validateInput(prfOptData)){
				alert("HTTP Profile name is required!");
				return;
			}

			// 3. Load the chosen profile configuration
			ajaxOut = $.ajax({
	    		url:'/content/new_httpProfile_build.php',
	    		type: 'POST',
	    		dataType: 'JSON',
	    		data: {'newProfileBuild': JSON.stringify(prfOptData)},
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
	    	ajaxOut.done(newProfileBuildProcessData);

		}
		else {
			// 2. Retrieve configuration data and save them according to the chosen profile name
			setPrfOptData(prfOptData, prfType, parPrfName);
			alert(iterAssArray(prfOptData));
			if( !validateInput(prfOptData)){
				alert("Profile name is required!");
				return;
			}

			// 3. Send the retrieved data to new_Profile_build.php where it calls a proper python file 
			// based on profile type name
			ajaxOut = $.ajax({
	    		url:'/content/new_Profile_build.php',
	    		type: 'POST',
	    		dataType: 'JSON',
	    		data: {'newProfileBuild': JSON.stringify(prfOptData)},
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
			ajaxOut.done(function(response_in){
				processBuildProfileData(response_in, prfType);
			});			
		}
	});
	
	// Event handler when a parent profile name is chosen
	$('#chg_svc_prf_name_select').on('change', function(){
		//Retrieve the element data of the parent window
		var nameAndIp = $('#ltmSelBox option:selected').val();
		var arr = nameAndIp.split(":");
		var prfType = window.parent.document.getElementById('selectedPrfType').value;
		// Load the corresponding Service profile configuration retrieved from BIG-IP
		// parPrfName is used for dual purpose - If Profile change mode is active, a chosen profile name is saved.
		// If Profile build mode is active ('new_profile'), parent profile name is saved
		var prfMode = GetParentURLParameter('go');
		var parPrfName;
		if (prfMode=='chg_profile'){
			// In Profile Change mode, variable 'parPrfName'(Parent Profile Name) is used to store a profile name
			parPrfName = this.value;
			if (parPrfName == 'none') return;
		}
		else if (prfMode=='new_profile'){
			parPrfName = $('#svc_prf_type_select').val();
		}
		
		var pxyMode = $('#svc_prf_proxymode_select').val();
		alert("Mode: " + prfMode + "\nChosen Profile Info: DevIP: " + arr[1] + "\nChosen or Parent Profile name: " + parPrfName + "\nProfile Type: " + prfType);

		var prfOptData = {'phpFileName':'', 'DevIP':'', 'name':''};

		//////////////////////// Beginning of Profile Data loading ////////////////////////
		// 1. Build configuration data structure according to the chosen profile name		
		if (prfType == "HTTP") initHttpPrfOptData(prfOptData, prfType, pxyMode);
		else initPrfOptData(prfOptData, prfType);
		
		// Profile Names: HTTP, DNS, Cookie, DestAddrAffinity, SrcAddrAffinity, Hash, SSL, Universal, FastL4, TCP, UDP, CLIENTSSL, SERVERSSL, OneConnect, Stream
		if (prfType == "HTTP"){
			//alert(iterAssArray(prfOptData));
			// 2. Build Dynamic configuration page according to the chosen profile name
			var strHtml = getStrHttpHtml(pxyMode);
	    	$('#prfConfTable_tbody tr').each(function(index) {
	    		if (index != 0 && index != 1 && index != 2) $(this).remove();
	    	});

			$('#prfConfTable_tbody').append(strHtml);
			// 3. Load the chosen profile configuration
			ajaxOut = $.ajax({
	    		url:'/content/getHttpSettings.php',
	    		type: 'POST',
	    		data: {method:'getHttpSettings', DevIP:arr[1], ProxyType:pxyMode, LoadTypeName:prfType, PrfName:parPrfName, PrfMode:prfMode },
	    		error: function(jqXHR, textStatus, errorThrown){
					alert("Ajax call for retrieving HTTP Profile config has failed!");
		            console.log('jqXHR:');
		            console.log(jqXHR);
		            console.log('textStatus:');
		            console.log(textStatus);
		            console.log('errorThrown:');
		            console.log(errorThrown);
				}
	    	}); 
	    	ajaxOut.done(getHttpSettingsProcessData);
			
		}
		else {
			var strHtml = getPrfHtml(prfType, parPrfName);
	    	$('#prfConfTable_tbody tr').each(function(index) {
	    		if (index != 0 && index != 1) $(this).remove();
	    	});
			$('#prfConfTable_tbody').append(strHtml);

			if (prfType == 'Hash' || prfType == 'Universal'){
				// Get iRule list
				ajxOut = $.ajax({
					url: '/content/get_profile_names.php',
					type: 'POST',
					dataType: 'JSON',
					data: {method:'get_profile_names', DevIP:arr[1], LoadTypeName:'IRULE'},
					error: function(jqXHR, textStatus, errorThrown){
						alert("Ajax call for " + prfType + " profile name loadig has failed!");
			            console.log('jqXHR:');
			            console.log(jqXHR);
			            console.log('textStatus:');
			            console.log(textStatus);
			            console.log('errorThrown:');
			            console.log(errorThrown);
					}
				});
				ajxOut.done(iruleNameProcessData);
			}
			else if (prfType == 'CLIENTSSL' || prfType == 'SERVERSSL') {
				// Get Cert and Key list
				ajxOut = $.ajax({
					url: '/content/get_profile_names.php',
					type: 'POST',
					async: false,
					dataType: 'JSON',
					data: {method:'get_profile_names', DevIP:arr[1], LoadTypeName:'CERT'},
					error: function(jqXHR, textStatus, errorThrown){
						alert("Ajax call for " + prfType + " profile Cert name loadig has failed!");
			            console.log('jqXHR:');
			            console.log(jqXHR);
			            console.log('textStatus:');
			            console.log(textStatus);
			            console.log('errorThrown:');
			            console.log(errorThrown);
					}
				});
				ajxOut.done(certNameProcessData);
				
				ajxOut2 = $.ajax({
					url: '/content/get_profile_names.php',
					type: 'POST',
					async: false,
					dataType: 'JSON',
					data: {method:'get_profile_names', DevIP:arr[1], LoadTypeName:'KEY'},
					error: function(jqXHR, textStatus, errorThrown){
						alert("Ajax call for " + prfType + " profile Key loading has failed!");
			            console.log('jqXHR:');
			            console.log(jqXHR);
			            console.log('textStatus:');
			            console.log(textStatus);
			            console.log('errorThrown:');
			            console.log(errorThrown);
					}
				});
				ajxOut2.done(keyNameProcessData);
			}
			
			// 3. Load the chosen profile configuration
			ajaxOut = $.ajax({
	    		url:'/content/getPrfSettings.php',
	    		type: 'POST',
	    		data: {method:'getPrfSettings', DevIP:arr[1], LoadTypeName:prfType, ParPrfName:parPrfName, PrfMode:prfMode },
	    		error: function(jqXHR, textStatus, errorThrown){
					alert("Ajax call for " + prfType + " profile setting loading has failed!");
		            console.log('jqXHR:');
		            console.log(jqXHR);
		            console.log('textStatus:');
		            console.log(textStatus);
		            console.log('errorThrown:');
		            console.log(errorThrown);
				}
	    	});
			ajaxOut.done(function(response_in){
				processGetProfileData(response_in, prfType);
			});			
		} 		
        //////////////////////// End of Profile Data Loading ////////////////////////
		
	});
	
	
	// Event handler for Profile change button click
	$('#prf_btn_change').on('click', function(){
		//Retrieve the element data of the parent window
		var nameAndIp = $('#ltmSelBox option:selected').val();
		var arr = nameAndIp.split(":");
		// prfName - Selected profile name
		var prfName = $('#chg_svc_prf_name_select').val();
		// pxyMode - HTTP profile only. HTTP proxy mode - reverse, explicit, transparent
		var pxyMode = $('#svc_prf_proxymode_select').val();
		// parPrfName - Parent Profile Name
		var parPrfName = $('#svc_prf_type_select').val();
		var prfType = window.parent.document.getElementById('selectedPrfType').value;
		//alert("Proxy Mode: " + pxyMode + " Profile Type: " + prfType + " Parent Profile name: " + parPrfName);
		// prfOptData has been extended with a Query string value of the Parent URL
		var prfOptData = {'phpFileName':'', 'DevIP':'', 'name':'', 'dplyOrChg':''};
		
		alert("prf_btn_change event in prf_jquery.js - Profile Type is: " + prfType + "\n");

		if (prfType == 'HTTP')
			prfOptData['phpFileName'] = 'new_httpProfile_build';
		else
			prfOptData['phpFileName'] = 'new_Profile_build';
		
		prfOptData['DevIP'] = arr[1];
		prfOptData['name'] = prfName;
		prfOptData['dplyOrChg'] = GetParentURLParameter('go');
		
		alert("Profile Name: " + prfName + "\nProxy Mode: " + pxyMode + "\nProfile Type: " + prfType + "\nParent Profile name: " + parPrfName + "\nDeploy or Change: " + prfOptData['dplyOrChg'] + "\n");

		// 1. Build configuration data structure according to the selected profile name		
		if (prfType == "HTTP") initHttpPrfOptData(prfOptData, prfType, pxyMode);
		else initPrfOptData(prfOptData, prfType);
		
		if (prfType == "HTTP"){
			// 2. Retrieve configuration data and save them according to the chosen profile name
			setHttpPrfOptData(prfOptData, prfType, pxyMode, parPrfName);
			//alert(iterAssArray(prfOptData));
			if( !validateInput(prfOptData)){
				alert("HTTP Profile name is required!");
				return;
			}

			// 3. Load the chosen profile configuration
			ajaxOut = $.ajax({
	    		url:'/content/new_httpProfile_build.php',
	    		type: 'POST',
	    		dataType: 'JSON',
	    		data: {'newProfileBuild': JSON.stringify(prfOptData)},
	    		error: function(jqXHR, textStatus, errorThrown){
					alert("Ajax call for HTTP Profile change has failed!");
		            console.log('jqXHR:');
		            console.log(jqXHR);
		            console.log('textStatus:');
		            console.log(textStatus);
		            console.log('errorThrown:');
		            console.log(errorThrown);
				}
	    	}); 
	    	ajaxOut.done(newProfileBuildProcessData);

		}
		else {
			// 2. Retrieve configuration data and save them according to the chosen profile name
			setPrfOptData(prfOptData, prfType, parPrfName);
			alert(iterAssArray(prfOptData));
			if( !validateInput(prfOptData)){
				alert("Profile name is required!");
				return;
			}

			// 3. Send the retrieved data to new_Profile_build.php where it calls a proper python file 
			// based on profile type name
			ajaxOut = $.ajax({
	    		url:'/content/new_Profile_build.php',
	    		type: 'POST',
	    		dataType: 'JSON',
	    		data: {'newProfileBuild': JSON.stringify(prfOptData)},
	    		error: function(jqXHR, textStatus, errorThrown){
					alert("Ajax call for " + prfType + " profile change has failed!");
		            console.log('jqXHR:');
		            console.log(jqXHR);
		            console.log('textStatus:');
		            console.log(textStatus);
		            console.log('errorThrown:');
		            console.log(errorThrown);
				}
	    	}); 
			ajaxOut.done(function(response_in){
				processBuildProfileData(response_in, prfType);
			});			
		}
	});
	
	// Change Event handler when a partition is selected
	$('#prf_partition_name_select').on('change', function(){
		if(this.value == 'select') return;
		
		// Reset Profile Name select option to default
		$('#del_svc_prf_name_select option').each(function(index) {
			$(this).remove();
		});
		$('#del_svc_prf_name_select').append("<option value='none' selected='selected'>None</option>");

		
		var nameAndIp = $('#ltmSelBox option:selected').val();
		var prfType = window.parent.document.getElementById('selectedPrfType').value;
		var arr = nameAndIp.split(":");
		
		loadProfileNames(arr[1], prfType, 'del_svc_prf_name_select');

	});
	
	// Click event handler when "Delete" buttion is clicked
	$('#prf_btn_delete').on('click', function(){
		if ($('#ltmSelBox').val() == 'select' || $('#prf_partition_name_select').val() == 'select' || $('#del_svc_prf_name_select').val() == 'none')
			alert("Required field is not fed!");
		
		// Builtin profile names are not listed from drop-down box
		var nameAndIp = $('#ltmSelBox option:selected').val();
		var arr = nameAndIp.split(":");
		var prfType = window.parent.document.getElementById('selectedPrfType').value;
		var partition = $('#prf_partition_name_select').val();
		var prfName = $('#del_svc_prf_name_select').val();
		
		deleteProfile(arr[1], prfType, partition, prfName);
		
		
		
	});
});