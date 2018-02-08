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
		$('#prf_name').css('border-color', 'red');
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

// Initialize Profile Key and default value based on the profile type
// This function determins the supported profile options
function initPrfOptData(prfOptData, prfType) {
	
	var prfOptKeys =[]; 
	
	if (prfType == "DNS"){
		/*
		 * enableDnsExpress-DNS Express , enableDnsFirewall-DNS Security, enableGtm-GSLB, enableHardwareQueryValidation-Protocol Validation, enableHardwareResponseCache-Response Cache
		 * processRd-Process Recursion Desired, processXfr-Zone Transfer, unhandledQueryAction-Unhandled Query Actions, useLocalBind-Use BIND Server on BIG-IP
		 */
		var dnsPrfOptKeys = ['defaultsFrom', 'enableHardwareQueryValidation', 'enableHardwareResponseCache', 'enableDnsExpress', 'enableGtm', 'unhandledQueryAction', 'useLocalBind', 'processXfr','enableDnsFirewall', 'processRd']; 
	}
	else if (prfType == "Cookie"){
		/*
		 * 'defaultsFrom', 'method'- Cookie method(hash, insert, passive, rewrite), 'cookieName', 'httponly', 'secure', 'alwaysSend', 'expiration', 'overrideConnectionLimit'
		 */
		var dnsPrfOptKeys = ['defaultsFrom', 'method', 'cookieName', 'httponly', 'secure', 'alwaysSend', 'expiration', 'overrideConnectionLimit'];
	}
	else if (prfType == "DestAddrAffinity"){
		/* 
		 * Path: /mgmt/tm/ltm/persistence/dest-addr
		 * 'defaultsFrom', 'matchAcrossServices', 'matchAcrossVirtuals', 'matchAcrossPools','hashAlgorithm', 'timeout', 'mask', 'overrideConnectionLimit'
		 */
		var dnsPrfOptKeys = ['defaultsFrom', 'matchAcrossServices', 'matchAcrossVirtuals', 'matchAcrossPools','hashAlgorithm', 'timeout', 'mask', 'overrideConnectionLimit'];		
	}
	else if (prfType == "SrcAddrAffinity"){
		/* 
		 * Path: /mgmt/tm/ltm/persistence/source-addr
		 * 'defaultsFrom', 'matchAcrossServices', 'matchAcrossVirtuals', 'matchAcrossPools','hashAlgorithm', 'timeout', 'mask', 'mapProxies', 'overrideConnectionLimit'
		 */
		var dnsPrfOptKeys = ['defaultsFrom', 'matchAcrossServices', 'matchAcrossVirtuals', 'matchAcrossPools','hashAlgorithm', 'timeout', 'mask', 'mapProxies', 'overrideConnectionLimit'];	
	}
	else if (prfType == "Hash"){
		/*
		 * matchAcrossServices, matchAcrossVirtuals, matchAcrossPools, hashAlgorithm, hashOffset, hashLength, hashStartPattern, hashEndPattern, hashBufferLimit, timeout, rule, overrideConnectionLimit
		 */
		var dnsPrfOptKeys = ['defaultsFrom', 'matchAcrossServices', 'matchAcrossVirtuals', 'matchAcrossPools','hashAlgorithm', 'hashOffset', 'hashLength', 'hashStartPattern', 'hashEndPattern', 'hashBufferLimit', 'timeout', 'rule', 'mapProxies', 'overrideConnectionLimit'];
	}
	else if (prfType == "SSL"){
		/*
		 * matchAcrossServices, matchAcrossVirtuals, matchAcrossPools, timeout, overrideConnectionLimit
		 */
		var dnsPrfOptKeys = ['defaultsFrom', 'matchAcrossServices', 'matchAcrossVirtuals', 'matchAcrossPools', 'timeout', 'overrideConnectionLimit'];
	}
	else if (prfType == "Universal"){
		/*
		 * matchAcrossServices, matchAcrossVirtuals, matchAcrossPools, timeout, rule, overrideConnectionLimit
		 */
		var dnsPrfOptKeys = ['defaultsFrom', 'matchAcrossServices', 'matchAcrossVirtuals', 'matchAcrossPools','timeout', 'rule', 'overrideConnectionLimit'];
	}
	else if (prfType == "FastL4"){
		
	}
	else if (prfType == "TCP"){
		
	}
	else if (prfType == "UDP"){
		
	}
	else if (prfType == "CLIENTSSL"){
		
	}
	else if (prfType == "SERVERSSL"){
		
	}
	else if (prfType == "OneConnect"){
		
	}
	else if (prfType == "Stream"){
		
	}

	prfOptKeys = prfOptKeys.concat(dnsPrfOptKeys);
	
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

function setPrfOptData(prfOptData, prfType, parPrfName) {

	prfOptData['PrfType'] = prfType;
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
		prfOptData['rule'] = $('#persistIRule option:selected').val();
		prfOptData['overrideConnectionLimit'] = $('#uniConnLimit option:selected').val();
	}
}

function prfNameProcessData(response_in) {
	var strResult = '';
	//Remove existing profile types and then add new ones
	$('#svc_prf_type_select option').each(function(index) {
		if (index != 0) $(this).remove();
	});
	
	$.each(response_in, function(index) {
		if (response_in[index] != "none"){
			strResult += "<option value='" + response_in[index] + "'>" + response_in[index] + "</option>";
		}
	});
	
	//alert("Return output: " + strResult);
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

function getHttpSettingsProcessData(response_in){
	//alert("Data: " + response_in);
	var responseArray = response_in.split('|');

	/* Debugging */
	/*
	var strResult = '';
	$.each(responseArray, function(index) {
		strResult += responseArray[index] + "<br>";
	});
	
	$('#newprf_EvalReview').html(strResult);
	*/
	
	$('#httpBasicAuth').val(responseArray[2]);
	$('#httpFallbackHost').val(responseArray[3]);
	$('#httpFallbackErrorCodes').val(responseArray[4]);
	$('#httpReqHdrErase').val(responseArray[5]);
	$('#httpReqHdrInsert').val(responseArray[6]);
	$('#httpReqChunk option[value="' + responseArray[7] + '"]').attr('selected', 'selected');
	$('#httpRespChunk option[value="' + responseArray[8] + '"]').attr('selected', 'selected');
	$('#httpXFF option:selected').val(responseArray[9]);
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
	alert('First Data: ' + responseArray[0] + 'Profile Type: ' + prfType);
	/* Debugging */
	/*
	var strResult = '';
	$.each(responseArray, function(index) {
		strResult += responseArray[index] + "<br>";
	});
	
	$('#newprf_EvalReview').html(strResult);
	*/
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
		$('#ckExp').val(responseArray[6]);
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
		$('#persistIRule option[value="' + responseArray[5] + '"]').attr('selected', 'selected');
		$('#uniConnLimit option[value="' + responseArray[6] + '"]').attr('selected', 'selected');

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
	
	//alert("Return output: " + strResult);
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
		strHtml += "<tr id='r6'><td width='132px' ><label>Expiration</label></td><td><input type='text' id='ckExp' value='0'><br><p> Note: 0 - Session Cookie. To specify specific expiration period, use D:H:M:S format.</p></td></tr>";
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
		strHtml += "<tr id='r5'><td width='132px' ><label>Hash Length</label></td><td><input type='text' id='hsLen' value='0'/></td></tr>";
		strHtml += "<tr id='r5'><td width='132px' ><label>Hash Start Pattern</label></td><td><input type='text' id='hsSPtn' value=''/></td></tr>";
		strHtml += "<tr id='r5'><td width='132px' ><label>Hash End Pattern</label></td><td><input type='text' id='hsEPtn' value=''/></td></tr>";
		strHtml += "<tr id='r5'><td width='132px' ><label>Hash Buffer Limit</label></td><td><input type='text' id='hsBfLimit' value='0'/></td></tr>";
		strHtml += "<tr id='r5'><td width='132px' ><label>Timeout</label></td><td><input type='text' id='hsTimeout' value='180'/></td></tr>";
		strHtml += "<tr id='r7'><td width='132px' ><label>Rule</label></td><td><select id='persistIRule' ><option value='none' selected>Select...</option></select></td></tr>";
		strHtml += "<tr id='r8'><td width='132px' ><label>Override Connection Limit</label></td><td><select id='hsConnLimit' ><option value='disabled' selected>Disabled</option><option value='enabled'>Enabled</option></select></td></tr>";
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
		strHtml += "<tr id='r5'><td width='132px' ><label>Rule</label></td><td><select id='persistIRule' ><option value='none' selected>Select...</option></select></td></tr>";
		strHtml += "<tr id='r6'><td width='132px' ><label>Override Connection Limit</label></td><td><select id='uniConnLimit' ><option value='disabled' selected>Disabled</option><option value='enabled'>Enabled</option></select></td></tr>";
		
	}
	return strHtml;
}

function setPrfHtml(prfType, response_in){
	var strHtml = '';
	return strHtml;
}

function getStrHttpHtml(pxyMode){
	// Default Page Load action - Load parent profile names
	var nameAndIp = window.parent.document.getElementById('ltmSelBox').value;
	var prfType = window.parent.document.getElementById('selectedPrfType').value;
	if (prfType == 'HTTP')
		prfType = prfType + ":dnsresolver";

	var arr = nameAndIp.split(":");
	var dnsRzvs = [];
	// Get the list of DNS Resolver if HTTP proxy mode is 'explicit'. Wait for ajax transaction completed - async: false
	ajxOut = $.ajax({
		url: '/content/get_profile_names.php',
		type: 'POST',
		async: false,
		dataType: 'JSON',
		data: {method:'get_profile_names', DevIP:arr[1], PrfType:prfType},
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
	strHtml += "<tr id='r3'><td width='132px' ><label>Fallback on Error Codes</label></td><td><input type='text' id='httpFallbackErrorCodes' /></td></tr>";
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

$(function () {
	// Default Page Load action - Load parent profile names
	var nameAndIp = window.parent.document.getElementById('ltmSelBox').value;
	var prfType = window.parent.document.getElementById('selectedPrfType').value;
	if (prfType == 'HTTP')
		prfType = prfType + ":" + window.parent.document.getElementById('selectedPrfProxyType').value;

	var arr = nameAndIp.split(":");
	//alert("Device IP: " + arr[1] + " Profile Type: " + prfType);
	
	// Call Ajax to retrieve parent profile names
	ajxOut = $.ajax({
		url: '/content/get_profile_names.php',
		type: 'POST',
		dataType: 'JSON',
		data: {method:'get_profile_names', DevIP:arr[1], PrfType:prfType},
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
	
	$('#svc_prf_proxymode_select').on('change', function() {
		var nameAndIp = window.parent.document.getElementById('ltmSelBox').value;
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
			data: {method:'get_profile_names', DevIP:arr[1], PrfType:prfType},
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
	
	//Dynamically add Parent profile names
	$('#svc_prf_type_select').on('change', function() {
		//alert("Chosen Parent Name: " + $('#svc_prf_type_select').val());
		var nameAndIp = window.parent.document.getElementById('ltmSelBox').value;
		var arr = nameAndIp.split(":");
		var pxyMode = $('#svc_prf_proxymode_select').val();
		var prfType = window.parent.document.getElementById('selectedPrfType').value;
		var parPrfName = $('#svc_prf_type_select').val();
		//alert("Proxy Mode: " + pxyMode + " Profile Type: " + prfType + " Parent Profile name: " + parPrfName);
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
			ajaxOut = $.ajax({
	    		url:'/content/getHttpSettings.php',
	    		type: 'POST',
	    		data: {method:'getHttpSettings', DevIP:arr[1], ProxyType:pxyMode, PrfType:prfType, PrfName:parPrfName },
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
					data: {method:'get_profile_names', DevIP:arr[1], PrfType:'IRULE'},
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
			
			// 3. Load the chosen profile configuration
			ajaxOut = $.ajax({
	    		url:'/content/getPrfSettings.php',
	    		type: 'POST',
	    		data: {method:'getPrfSettings', DevIP:arr[1], PrfType:prfType, ParPrfName:parPrfName },
	    		error: function(jqXHR, textStatus, errorThrown){
					alert("Ajax call failed!");
		            console.log('jqXHR:');
		            console.log(jqXHR);
		            console.log('textStatus:');
		            console.log(textStatus);
		            console.log('errorThrown:');
		            console.log(errorThrown);
				},
	    	});
			ajaxOut.done(function(response_in){
				processGetProfileData(response_in, prfType);
			});			
		} 
		/*
		else if (prfType == "DNS"){
			//alert(iterAssArray(prfOptData));
			// 2. Build Dynamic configuration page according to the chosen profile name
			var strHtml = getPrfHtml(prfType, parPrfName);
	    	$('#prfConfTable_tbody tr').each(function(index) {
	    		if (index != 0 && index != 1) $(this).remove();
	    	});
			$('#prfConfTable_tbody').append(strHtml);
			// 3. Load the chosen profile configuration
			ajaxOut = $.ajax({
	    		url:'/content/getPrfSettings.php',
	    		type: 'POST',
	    		data: {method:'getPrfSettings', DevIP:arr[1], PrfType:prfType, ParPrfName:parPrfName },
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
		else if (prfType == "Cookie"){
			var strHtml = getPrfHtml(prfType, parPrfName);
	    	$('#prfConfTable_tbody tr').each(function(index) {
	    		if (index != 0 && index != 1) $(this).remove();
	    	});
			$('#prfConfTable_tbody').append(strHtml);
			// 3. Load the chosen profile configuration
			ajaxOut = $.ajax({
	    		url:'/content/getPrfSettings.php',
	    		type: 'POST',
	    		data: {method:'getPrfSettings', DevIP:arr[1], PrfType:prfType, ParPrfName:parPrfName },
	    		error: function(jqXHR, textStatus, errorThrown){
					alert("Ajax call failed!");
		            console.log('jqXHR:');
		            console.log(jqXHR);
		            console.log('textStatus:');
		            console.log(textStatus);
		            console.log('errorThrown:');
		            console.log(errorThrown);
				},
	    	});
			ajaxOut.done(function(response_in){
				processGetProfileData(response_in, prfType);
			});

		}
		else if (prfType == "DestAddrAffinity"){
			
		}
		else if (prfType == "SrcAddrAffinity"){
			
		}
		else if (prfType == "Hash"){
			
		}
		else if (prfType == "SSL"){
			
		}
		else if (prfType == "Universal"){
			
		}
		else if (prfType == "FastL4"){
			
		}
		else if (prfType == "TCP"){
			
		}
		else if (prfType == "UDP"){
			
		}
		else if (prfType == "CLIENTSSL"){
			
		}
		else if (prfType == "SERVERSSL"){
			
		}
		else if (prfType == "OneConnect"){
			
		}
		else if (prfType == "Stream"){
			
		}
		*/
	});
	
	$('#prf_btn_build').on('click', function(){
		//Retrieve the element data of the parent window
		var nameAndIp = window.parent.document.getElementById('ltmSelBox').value;
		var arr = nameAndIp.split(":");
		// prfName - User provided profile name
		var prfName = $('#prf_name').val();
		// pxyMode - HTTP profile only. HTTP proxy mode - reverse, explicit, transparent
		var pxyMode = $('#svc_prf_proxymode_select').val();
		// parPrfName - Parent Profile Name
		var parPrfName = $('#svc_prf_type_select').val();
		var prfType = window.parent.document.getElementById('selectedPrfType').value;
		//alert("Proxy Mode: " + pxyMode + " Profile Type: " + prfType + " Parent Profile name: " + parPrfName);
		var prfOptData = {'phpFileName':'', 'DevIP':'', 'name':''};
		if (prfType == 'HTTP')
			prfOptData['phpFileName'] = 'new_httpProfile_build';
		else
			prfOptData['phpFileName'] = 'new_Profile_build';
		
		prfOptData['DevIP'] = arr[1];
		prfOptData['name'] = prfName;
		
		// 1. Build configuration data structure according to the chosen profile name		
		if (prfType == "HTTP") initHttpPrfOptData(prfOptData, prfType, pxyMode);
		else initPrfOptData(prfOptData, prfType);
		
		if (prfType == "HTTP"){
			// 2. Retrieve configuration data and save them according to the chosen profile name
			setHttpPrfOptData(prfOptData, prfType, pxyMode, parPrfName);
			//alert(iterAssArray(prfOptData));
			if( !validateInput(prfOptData)) return;

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
			//alert(iterAssArray(prfOptData));
			if( !validateInput(prfOptData)) return;

			// 3. Load the chosen profile configuration
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
		/*
		else if (prfType == "DNS"){
			// 2. Retrieve configuration data and save them according to the chosen profile name
			setPrfOptData(prfOptData, prfType, parPrfName);
			//alert(iterAssArray(prfOptData));
			if( !validateInput(prfOptData)) return;

			// 3. Load the chosen profile configuration
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
	    	ajaxOut.done(newProfileBuildProcessData);

		}
		else if (prfType == "Cookie"){
			// 2. Retrieve configuration data and save them according to the chosen profile name
			setPrfOptData(prfOptData, prfType, parPrfName);
			//alert(iterAssArray(prfOptData));
			if( !validateInput(prfOptData)) return;

			// 3. Load the chosen profile configuration
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
		*/		
	});
	
});