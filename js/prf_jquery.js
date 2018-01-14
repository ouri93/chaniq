function prfNameProcessData(response_in) {
	var strResult = '';
	//Remove existing profile types and then add new ones
	$('#svc_prf_type_select option').each(function(index) {
		if (index != 0) $(this).remove();
	});
	
	$.each(response_in, function(index) {
		if (response_in[index] != "none")
			strResult += "<option value='" + response_in[index] + "'>" + response_in[index] + "</option>";
	});
	
	//alert("Return output: " + strResult);
	$('#svc_prf_type_select').append(strResult);
}

$(function () {
	// Default Page Load action - Load parent profile names
	var nameAndIp = window.parent.document.getElementById('ltmSelBox').value;
	var prfType = window.parent.document.getElementById('selectedPrfType').value;
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
	
	//Dynamically add profile names
	$('#svc_prf_type_select').on('change', function() {
		alert("Chosen Parent Name: " + $('#svc_prf_type_select').val());
	});
	
	//Load the chosen profile configuration
	$('#tr_svc_prf_type').on('change','#svc_prf_type_select', function() {
		
	});
	
	$('#prf_btn_build').on('click', function(){
		//Retrieve the element data of the parent window
		var nameAndIp = window.parent.document.getElementById('ltmSelBox').value;
		var arr = nameAndIp.split(":");
	});
	
});