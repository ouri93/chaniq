$(function () {
	
	//Load parent profile names
	$('#svc_prf_type_select').on('click', function() {
		var nameAndIp = window.parent.document.getElementById('ltmSelBox').value;
		var arr = nameAndIp.split(":");
		alert("Device IP: " + arr[1]);
		
		
	});
	
	//Load parent profile names
	$('#tr_svc_prf_type').on('change','#svc_prf_type_select', function() {
		
	});
	
	$('#prf_btn_build').on('click', function(){
		//Retrieve the element data of the parent window
		var nameAndIp = window.parent.document.getElementById('ltmSelBox').value;
		var arr = nameAndIp.split(":");
	});
	
});