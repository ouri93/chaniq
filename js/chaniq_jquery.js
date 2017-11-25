/* 
 * Javascript for moving items between two list boxes
 */
/*
 * Original example found here: http://www.jquerybyexample.net/2012/05/how-to-move-items-between-listbox-using.html
 * Modified by Esau Silva to support 'Move ALL items to left/right' and add better stylingon on Jan 28, 2016.
 * 
 */

function getPoolMonAjax(phpFileName, bigipName, bigipIP) {
  	return $.ajax({
  		url: 'content/get_pool_monitors.php',
   		type: 'POST',
   		data: {method: phpFileName, DevName: bigipName, DevIP: bigipIP}
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

function buildNewPoolAjax(phpFileName, arr, pVsName, pVsPort, pMon, pEnv, pLBMethod, pPriGroup, pPriGroupLessThan, pmPoolMemberName, pmPoolMemberIp, pmPoolMemberPort, pmPoolMemberMon, pmPriGroup)
{

	alert("buildNewPoolAjax()");
	//alert(arr[1] + ":"+ pVsName + ":"+ pVsPort + ":"+ pMon + ":"+ pEnv + ":" + pLBMethod + ":"+ pPriGroup + ":"+ pPriGroupLessThan + ":" + pmPoolMemberName + ":"+ pmPoolMemberIp +":" + pmPoolMemberPort + ":" + pmPoolMemberMon + ":" + pmPriGroup);
  	return $.ajax({
  		url: 'content/new_pool_build.php',
   		type: 'POST',
   		dataType: 'JSON',
   		//data: {phpFile: phpFileName, DevIP: arr[1], PVsName: pVsName, PVsPort: pVsPort, PMon: pMon, PEnv: pEnv, PLBMethod: pLBMethod, PPriGroup: pPriGroup, PPriGroupLessThan: pPriGroupLessThan, PmPoolMemberNmae: pmPoolMemberName, PmPoolMemberIp: pmPoolMemberIp, PmPoolMemberPort: pmPoolMemberPort, PmPoolMemberMon: pmPoolMemberMon, PmPrigroup: pmPriGroup }
   		data: {phpFile: phpFileName, DevIP: arr[1], PVsName: pVsName, PVsPort: pVsPort, PMon: pMon, PEnv: pEnv, PLBMethod: pLBMethod }
   	});
	//return "String line1\n String line2\n";
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
    	var arr = bigipNameAndIP.split(":");
    	//alert("Name: " + arr[0] + " IP: " + arr[1]);
    	
    	// Call Ajax to get all available Pool monitors from the device
    	
    	ajaxOut = getPoolMonAjax("get_pool_monitors", arr[0], arr[1]);
    	ajaxOut.done(PprocessData);
    	$('#pm_mon').trigger('click');

    });
    
    $('#pm_mon').one('click', function() {
    //$('#pm_td').on('click', 'select', function() {
    	//alert("Select has been changed");
    	var bigipNameAndIP = $('#ltmSelBox').val();
    	var arr = bigipNameAndIP.split(":");
    	//alert("Name: " + arr[0] + " IP: " + arr[1]);
    	
    	// Call Ajax to get all available Pool monitors from the device
    	
    	ajaxOut = getPoolMonAjax("get_pool_monitors", arr[0], arr[1]);
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
    	if (pPriGroup != "disabled") {
    		var pmPriGroup = document.getElementsByClassName('pm_pg_val');
    	}

    	//alert(bigipNameAndIP + ":" + arr[1] + ":"+ pVsName + ":"+ pVsPort + ":"+ pMon + ":"+ pEnv + ":" + pLBMethod + ":"+ pPriGroup + ":"+ pPriGroupLessThan + ":" + pmPoolMemberName[0].value + ":"+ pmPoolMemberIp[0].value +":" + pmPoolMemberPort[0].value + ":" + pmPoolMemberMon[0].value + ":" + pmPriGroup[0].value + ":" + pmPoolMemberName[1].value + ":" + pmPoolMemberIp[1].value + ":"+ pmPoolMemberPort[1].value + ":"+ pmPoolMemberMon[1].value + ":" + pmPriGroup[1].value);
    	ajaxOut = buildNewPoolAjax('new_pool_build', arr, pVsName, pVsPort, pMon, pEnv, pLBMethod, pPriGroup, pPriGroupLessThan, pmPoolMemberName, pmPoolMemberIp, pmPoolMemberPort, pmPoolMemberMon, pmPriGroup);
    	//$('#newPool_EvalReview').html(ajaxOut);
    	
    	//alert(bigipNameAndIP + " " + arr[1] + " "+ pVsName + " "+ pVsPort + " "+ pMon + " "+ pLBMethod + " "+ pPriGroup + " "+ pmPoolMemberName[0].value + " "+ pmPoolMemberName[1].value + " " + pmPoolMemberIp + " "+ pmPoolMemberPort + " "+ pmPriGroup + " ");
    	
    });
});