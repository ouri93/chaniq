/* 
 * Javascript and JQuery for SSL Cert and Key management
 */
function getCertImportHtml(impType){
	// Update html code by SSL Cert/Key type - Key, Certificate, PKCS12
	// Bit 0 - Cert/Key Name (0000 0001), Bit 1 - Source (Paste, File Upload) (0000 0010), Bit 2 - Source (File Upload) (0000 0100) 
	// Bit 3 - Security Type(Normal, Password) (0000 1000), Bit 4 - Password (0001 0000)
	// Key - 0000 1011(11), Certificate - 0000 0011(3), PKCS12 - 0001 1101(29)
	var strHtml = '';
	var importCode = 0;
	switch (impType)
	{
	case 'Key':
		importCode = 11;
		break;
	case 'Certificate':
		importCode = 3;
		break;
	case 'PKCS 12 (IIS)':
		importCode = 29;
		break;
	}
	
	//alert("Chosen import Code: " + importCode);
	var tmpLabel ='';
	if (impType == "PKCS 12 (IIS)")	tmpLabel = "Certificate";
	else tmpLabel = impType;
	
	switch(true)
	{
	case (((importCode >> 0) & 1) == 1):
		if(((importCode >> 0) & 1) == 1) {
			strHtml += "<tr id='r1'><td width='132px' ><label>*" + tmpLabel + " Name</label></td><td><input type='text' id='crtConfName' required='required' /> <p>** DO NOT include extenstion! **</p></td></tr>";
		}
	case (((importCode >> 1) & 1) == 1):
		if(((importCode >> 1) & 1) == 1) {
			strHtml += "<tr id='r2'><td width='132px' ><label>*" + impType + " Source</label></td><td id='crtTdRadioBtn' ><label>Upload File</label><input type='radio' id='crtConfUploadFile' name='crtImportSource' checked /><label>Paste Text</label><input type='radio' id='crtConfPasteText' name='crtImportSource' > <br><br><input type='file' id='crtConfSource' /></td></tr>";
		}
	case (((importCode >> 2) & 1) == 1):
		if(((importCode >> 2) & 1) == 1) {
			strHtml += "<tr id='r3'><td width='132px' ><label>*" + tmpLabel + " Source</label></td><td><input type='file' id='crtConfSource' /></td></tr>";
		}
	case (((importCode >> 4) & 1) == 1):
		if(((importCode >> 4) & 1) == 1) { 	
			strHtml += "<tr id='r5'><td width='132px' ><label>Password</label></td><td><input type='password' id='crtConfPKCSPw' /></td></tr>";
		}
	case (((importCode >> 3) & 1) == 1):
		if(((importCode >> 3) & 1) == 1) {
			var tmp;
			if (impType == "Key") tmp = "*Security Type";
			if (impType == "PKCS 12 (IIS)")	tmp = "Key Security";
			strHtml += "<tr id='r4'><td width='132px' ><label>" + tmp + "</label></td><td><select id='crtSecType'><option selected='selected' value='Normal'>Normal</option><option value='Password' >Password</option></select> </td></tr>";
		}
	default:
		break;
	}
	
	return strHtml;
	
}

function getCertCreateHtml(creType){
	var strHtml = '';
	strHtml += "<tr id='r1'><td width='132px' ><label>*Certificate Name</label></td><td><input type='text' id='crtCreConfName' required='required' /></td></tr>";
	strHtml += "<tr id='r2'><td width='132px' ><label>*Common Nmae</label></td><td><input type='text' id='crtCreConfCN' required='required' /></td></tr>";
	strHtml += "<tr id='r3'><td width='132px' ><label>Division</label></td><td><input type='text' id='crtCreConfDVZ' /></td></tr>";
	strHtml += "<tr id='r4'><td width='132px' ><label>Organization</label></td><td><input type='text' id='crtCreConfOG' /></td></tr>";
	strHtml += "<tr id='r5'><td width='132px' ><label>Locality</label></td><td><input type='text' id='crtCreConfLOC' /></td></tr>";
	strHtml += "<tr id='r6'><td width='132px' ><label>State Or Province</label></td><td><input type='text' id='crtCreConfState' /></td></tr>";
	strHtml += "<tr id='r7'><td width='132px' ><label>Country</label></td><td><select id='crtCreConfCountry' ><option value='United States:US' selected='selected'>United States:US</option><option value='Republic of South Korea:KR' >Republic of South Korea:KR</option></select></td></tr>";
	strHtml += "<tr id='r8'><td width='132px' ><label>E-mail Address</label></td><td><input type='email' id='crtCreConfEmail' placeholder='john@xyz.com' /></td></tr>";
	strHtml += "<tr id='r9'><td width='132px' ><label>Subject Alternative Name</label></td><td><input type='text' id='crtCreConfSAN' /></td></tr>";
	if (creType == 'Self'){
		strHtml += "<tr id='r10'><td width='132px' ><label>*Lifetime</label></td><td><input type='text' id='crtCreConfLifetime' value='365' />&nbsp;days</td></tr>";
	}
	if (creType == 'Certificate Authority'){
		strHtml += "<tr id='r11'><td width='132px' ><label>Challenge Password</label></td><td><input type='password' id='crtCreConfChPW' /></td></tr>";
		strHtml += "<tr id='r12'><td width='132px' ><label>Confirm Password</label></td><td><input type='password' id='crtCreConfChPW2' /></td></tr>";
	}
	strHtml += "<tr> <td style='padding:4px; color:#555; font-size:12pt;'><b> Key Properties</b></td><td></td></tr>";
	strHtml += "<tr id='r13'><td width='132px' ><label>*Key Type (Only RSA is supported)</label></td><td><select id='crtCreConfKeyType' ><option value='RSA' selected='selected'>RSA</option><option value='DSA'>DSA</option><option value='ECDSA' >ECDSA</option></select></td></tr>";
	strHtml += "<tr id='r14'><td width='132px' ><label>*Size</label></td><td><select id='crtCreConfKeySize' ><option value='512'>512</option><option value='1024'>1024</option><option value='2048' selected='selected' >2048</option><option value='4096' >4096</option></select>&nbsp;bits</td></tr>";
	return strHtml;
}

function buildCertKeyAjax(phpFileName, certkeyData){
	
	return $.ajax({
		url: '/content/new_certkey_build.php',
		type: 'POST',
		dataType: 'JSON',
		data: {'jsonCertkeyData': JSON.stringify(certkeyData)},
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

function buildCertKeyProcessData(response_in) {
	var strResult = '';
	$.each(response_in, function(index) {
		if(index == 0) 
			strResult = "<b>" + response_in[index] + "</b><br>";
		else
			strResult += response_in[index] + "<br>";
	});
	
	//alert("Return output: " + strResult);
	$('#newcrt_EvalReview').html(strResult);
}

$(function () {
	// SSL Key/Cert import
	$('#import_cert_type').on('change','#imp_type_select', function (e) {
    	var impType = $('#imp_type_select').val();
    	//alert("Selected Import type: " + impType);
    	var strCertImpHtml = getCertImportHtml(impType);
    	//alert("Created HTML code: " + strCertImpHtml);
    	
    	$('#crtConfTable_tbody tr').each(function(index) {
    		if (index != 0) $(this).remove();
    	});

    	$('#crtConfTable_tbody').append(strCertImpHtml);
    });
    
    // SSL Key/Cert creation
    $('#create_cert_type').on('change','#create_type_select', function (e) {
    	var creType = $('#create_type_select').val();
    	alert("Selected Creation type: " + creType);
    	var strCertCreHtml = getCertCreateHtml(creType);
    	alert("Created HTML code: " + strCertCreHtml);
    	
    	$('#crtConfTable_tbody tr').each(function(index) {
    		if (index != 0 && index != 1) $(this).remove();
    	});
		
    	$('#crtConfTable_tbody').append(strCertCreHtml);
    });
    
    // If File Upload radio buttion is chosen
    $('#crtConfTable_tbody').on('change', '#crtConfUploadFile', function(){
    	//alert("Radion buttion changed");
    	$('#crtPasteTextarea').remove();
    	$('#crtTdRadioBtn').append("<input type='file' id='crtConfSource' />");
    });
    
    // If Paste Text radio buttion is chosen
    $('#crtConfTable_tbody').on('change', '#crtConfPasteText', function(){
    	//alert("Radion buttion changed");
    	$('#crtConfSource').remove();
    	$('#crtTdRadioBtn').append("<textarea id='crtPasteTextarea' rows='8' cols='75' />");
    });

    // File Explorer to search Cert and Key file
    $('#crtConfTable_tbody').on('change', '#crtConfSource', function(){
    	var crtConfFileName = $('#crtConfSource').val();
    	alert("Chosen file name and path: " + crtConfFileName);
    	    	
    });
    $('#crtConfTable_tbody').on('change', '#crtSecType', function(){
    	var chosenSecType = $('#crtSecType').val();
    	if (chosenSecType == 'Password'){
    		var tmpLabel = 'Password';
    		if ( $('#imp_type_select').val() == 'PKCS 12 (IIS)')
    			tmpLabel = 'Key Password';

    		$('#crtConfTable_tbody').append("<tr id='crtSecTypeTd'><td><label>" + tmpLabel + "</label></td><td><input type='password' id='crtSecTypePw' /></td></tr>");
    	}
    	else if (chosenSecType == 'Normal'){
    		$('#crtSecTypeTd').remove();
    	}
    });
    
    $('#crt_btn_build').on('click', function() {
    	var sslImpData = {'phpFileName':'', 'sslDevIP':'', 'sslImpType':'', 'sslImpName':'', 'sslKeySource':'', 'sslKeySourceData':'', 'sslSecType':'', 'sslSecTypeData':'', 'sslPKCSPw':''};
    	//Retrieve the element data of the parent window
    	var nameAndIp = window.parent.document.getElementById('ltmSelBox').value;
    	var arr = nameAndIp.split(":");
    	
    	// Data gathering
    	sslImpData['sslDevIP'] = arr[1];
    	var impType = $('#imp_type_select').val();
    	var secType = $('#crtSecType').val();
    	var uploadStatus = '';
    	
    	sslImpData['phpFileName'] = 'new_certkey_build';
    	sslImpData['sslImpType'] = impType;
    	sslImpData['sslImpName'] = $('#crtConfName').val();
    	
    	// Set Cert/Key/PKCS12 Source type - UPLOAD, PASTE
    	// Cert/Key Paste option is chosen
    	if ( (impType == "Key" || impType == "Certificate") && $('#crtConfPasteText').prop('checked') ){
    		sslImpData['sslKeySource'] = 'PASTE';
    		sslImpData['sslKeySourceData'] = $('#crtPasteTextarea').val();
    		uploadStatus = 'Success';
    	}
    	// Cert/Key Upload option is chosen
    	else if ( (impType == "Key" || impType == "Certificate") && $('#crtConfUploadFile').prop('checked') ){ 
    		sslImpData['sslKeySource'] = 'UPLOAD';
    		uploadStatus = 'Success';
    	}
    	// PKCS12 option is chosen - UPLOAD
    	else{
    		sslImpData['sslKeySource'] = 'UPLOAD';
    	}
    	
    	// Set Cert/Key Securty Type - Key Security: Normal / Password
    	if ( impType == "Key" || impType == "PKCS 12 (IIS)" )
    		sslImpData['sslSecType'] = secType;
    	else
    		sslImpData['sslSecType'] = '';
    	
    	// Set Password if Key Security type is 'Password'
    	if ( (impType == "Key" || impType == "PKCS 12 (IIS)") && (secType == "Password") )
    		sslImpData['sslSecTypeData'] = $('#crtSecTypePw').val();
    	
    	// PKCS12 only - Set PKCS12 export password
    	if ( impType == "PKCS 12 (IIS)" )
    		sslImpData['sslPKCSPw'] = $('#crtConfPKCSPw').val();
    	
    	alert("Device IP: " + sslImpData['sslDevIP'] + "Import Type: " + sslImpData['sslImpType'] + "SSL Name: " + sslImpData['sslImpName'] + " Key Source: " + sslImpData['sslKeySource']+ " Key SourceData: " + sslImpData['sslKeySourceData'] + " Secu Type: " + sslImpData['sslSecType']+ " Secu Data: " + sslImpData['sslSecTypeData']+ " PKCS Only PW: " + sslImpData['sslPKCSPw']);
    	
    	
    	// Upload a file to the Web Server (/var/www/chaniq/log/tmp) crtConfSource
    	if (sslImpData['sslKeySource'] == 'UPLOAD'){
    		var file_data = $('#crtConfSource').prop('files')[0];
    		var form_data = new FormData();
    		form_data.append('file', file_data);
    		form_data.append('sslImpType', sslImpData['sslImpType']);
    		form_data.append('sslImpName', sslImpData['sslImpName']);
    		
    		/* Print all File FormData() Key and Value paires
    		for (var pair of form_data.entries()) {
    			console.log(pair[0] + ', ' + pair[1]);
    		}
    		*/
    		
    		// Note. async is set to "False" so that we can process further steps in order
    		$.ajax({
    			url: '/content/ssl_file_upload.php',
    			dataType: 'text',
    			cache: false,
    			contentType: false,
    			processData: false,
    			data: form_data,
    			type: 'post',
    			async: false,
    			success: function(php_script_response) {
    				uploadStatus = php_script_response;
    				//alert("Upload result: " + uploadStatus);
    			}
    		});
    		sslImpData['sslKeySourceData'] = $('#crtConfSource').val().split('\\').pop();
    	}

    	// If file upload is successful, build cert and key on the F5
    	if ( uploadStatus != 'Success'){
    		$('#newcrt_EvalReview').html(uploadStatus);
    	}
    	else {
        	
    		/*
        	var output;
        	$.each(sslImpData, function(index) {	
        	    output = output + sslImpData[index] + "\n";
        	});
        	alert("Data: " + output);
        	*/
        	
        	ajaxOut = buildCertKeyAjax("new_certkey_build", sslImpData);
        	ajaxOut.done(buildCertKeyProcessData);
    			
    	}
    	
    });

    $('#crtConfTable_tbody').on('change', '#crtCreConfKeyType', function(){
    	var keyType = $('#crtCreConfKeyType').val();
    	if (keyType == 'ECDSA'){
    	   	$('#r14').remove();
    	   	$('#crtConfTable_tbody').append("<tr id='r14'><td width='132px' ><label>*Curve Name</label></td><td><select id='crtCreConfKeySize' ><option value='prime256v1' selected='selected' >prime256v1</option><option value='secp384r1'>secp384r1</option><option value='secp521r1' >secp521r1</option></td></tr>");
    	}
    	else if (keyType == 'RSA' || keyType == 'DSA') {
    		$('#r14').remove();
    		$('#crtConfTable_tbody').append("<tr id='r14'><td width='132px' ><label>*Size</label></td><td><select id='crtCreConfKeySize' ><option value='512'>512</option><option value='1024'>1024</option><option value='2048' selected='selected' >2048</option><option value='4096' >4096</option></select></td></tr>");
    	}
    	    	
    });

    // F5 Python SDK 2.3.3 doesn't support CSR creation.
    // CSR creation is supported from Python SDK 3.0.8 or later
    $('#crt_create_btn_build').on('click', function() {
    	alert("Current F5 Python SDK Version (2.3.3) does not support CSR creation.\nCRS creation with Python SDK is supported from Python SDK 3.0.8 or later.")
    	
    });
    
   
});