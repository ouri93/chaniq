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
			strHtml += "<tr id='r1'><td width='132px' ><label>*" + tmpLabel + " Name</label></td><td><input type='text' id='crtConfName' required='required' /></td></tr>";
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

function buildCertKeyAjax(phpFileName, certkeyData){
	
	return $.ajax({
		url: 'content/new_certkey_build.php',
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
    
    $('#create_cert_type').on('change','#create_type_select', function (e) {
    	var creType = $('#create_type_select').val();
    	alert("Selected Creation type: " + creType);
    	
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
    	
    	sslImpData['phpFileName'] = 'if_ssl_import_build';
    	sslImpData['sslImpType'] = impType;
    	sslImpData['sslImpName'] = $('#crtConfName').val();
    	
    	if ( (impType == "Key" || impType == "Certificate") && $('#crtConfPasteText').prop('checked') ){
    		sslImpData['sslKeySource'] = 'PASTE';
    		sslImpData['sslKeySourceData'] = $('#crtPasteTextarea').val();
    	}
    	else{
    		sslImpData['sslKeySource'] = 'UPLOAD';
    	}
    	
    	if ( impType == "Key" || impType == "PKCS 12 (IIS)" )
    		sslImpData['sslSecType'] = secType;
    	else
    		sslImpData['sslSecType'] = '';
    	
    	if ( (impType == "Key" || impType == "PKCS 12 (IIS)") && (secType == "Password") )
    		sslImpData['sslSecTypeData'] = $('#crtSecTypePw').val();
    	
    	if ( impType == "PKCS 12 (IIS)" )
    		sslImpData['sslPKCSPw'] = $('#crtConfPKCSPw').val();
    	
    	alert("Device IP: " + sslImpData['sslDevIP'] + "Import Type: " + sslImpData['sslImpType'] + "SSL Name: " + sslImpData['sslImpName'] + " Key Source: " + sslImpData['sslKeySource']+ " Key SourceData: " + sslImpData['sslKeySourceData'] + " Secu Type: " + sslImpData['sslSecType']+ " Secu Data: " + sslImpData['sslSecTypeData']+ " PKCS Only PW: " + sslImpData['sslPKCSPw']);
    	
    	
    	// Upload a file to the Web Server (/var/www/chaniq/log/tmp) crtConfSource
    	if (sslImpData['sslKeySource'] == 'UPLOAD'){
    		var file_data = $('#crtConfSource').prop('files')[0];
    		var form_data = new FormData();
    		form_data.append('file', file_data);
    		
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
        	
        	var output;
        	$.each(sslImpData, function(index) {	
        	    output = output + sslImpData[index] + "\n";
        	});
        	alert("Data: " + output);
        	
        	
        	ajaxOut = buildCertKeyAjax("new_certkey_build", sslImpData);
        	ajaxOut.done(buildCertKeyProcessData);
    			
    	}
    	
    });
});