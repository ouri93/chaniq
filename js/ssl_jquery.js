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
	
	switch(true)
	{
	case (((importCode >> 0) & 1) == 1):
		if(((importCode >> 0) & 1) == 1) {
			var tmp;
			if (impType == "PKCS 12 (IIS)")	tmp = "Certificate";
			else tmp = impType;
			strHtml += "<tr id='r1'><td><label>" + tmp + " Name</label></td><td><input type='text' id='crtConfName' /></td></tr>";
		}
	case (((importCode >> 1) & 1) == 1):
		if(((importCode >> 1) & 1) == 1) {
			strHtml += "<tr id='r2'><td><label>" + impType + " Source</label></td><td id='crtTdRadioBtn'><label>Upload File</label><input type='radio' id='crtConfUploadFile' name='crtImportSource' checked /><label>Paste Text</label><input type='radio' id='crtConfPasteText' name='crtImportSource' > <br><input type='button' id='crtConfSource' value='Choose File' /></td></tr>";
		}
	case (((importCode >> 2) & 1) == 1):
		if(((importCode >> 2) & 1) == 1) {
			strHtml += "<tr id='r3'><td><label>" + impType + " Source</label></td><td><input type='button' id='crtConfSource' value='Choose File' /></td></tr>";
		}
	case (((importCode >> 3) & 1) == 1):
		if(((importCode >> 3) & 1) == 1) {
			var tmp;
			if (impType == "Key") tmp = "Security Type";
			if (impType == "PKCS 12 (IIS)")	tmp = "Key Security";
			strHtml += "<tr id='r4'><td><label>" + tmp + "</label></td><td><select id='crtSecType'><option selected='selected'>Normal</option><option>Password</option></select> </td></tr>";
		}
	case (((importCode >> 4) & 1) == 1):
		if(((importCode >> 4) & 1) == 1) { 	
			strHtml += "<tr id='r5'><td><label>Password</label></td><td><input type='password' id='crtConfPKCSPw' /></td></tr>";
		}
	default:
		break;
	}
	
	return strHtml;
	
}

$(function () {
    $('#import_cert_type').on('change','#imp_type_select', function (e) {
    	var impType = $('#imp_type_select').val();
    	//alert("Selected Import type: " + impType);
    	var strCertImpHtml = getCertImportHtml(impType);
    	alert("Created HTML code: " + strCertImpHtml);
    	
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
    	alert("Radion buttion changed");
    	$('#crtPasteTextarea').remove();
    	$('#crtTdRadioBtn').append("<input type='button' id='crtConfSource' value='Choose File' />");
    });
    
    // If Paste Text radio buttion is chosen
    $('#crtConfTable_tbody').on('change', '#crtConfPasteText', function(){
    	alert("Radion buttion changed");
    	$('#crtConfSource').remove();
    	$('#crtTdRadioBtn').append("<textarea id='crtPasteTextarea' rows='8' cols='80'> </textarea>");
    	
    	
    });
});