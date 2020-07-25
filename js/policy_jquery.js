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

function addRow(tableID) {
	var table = document.getElementById(tableID);
	var rowCount = table.rows.length;
	if(rowCount < 10){							// limit the user from creating fields more than your limits
		var row = table.insertRow(rowCount);
		var colCount = table.rows[0].cells.length;
		for(var i=0; i<colCount; i++) {
			var newcell = row.insertCell(i);
			newcell.innerHTML = table.rows[0].cells[i].innerHTML;
		}
	}else{
		 alert("Maximum number of pool members are 10.");
			   
	}
}

function deleteRow(tableID) {
	var table = document.getElementById(tableID);
	var rowCount = table.rows.length;
	for(var i=0; i<rowCount; i++) {
		var row = table.rows[i];
		var chkbox = row.cells[0].childNodes[0];
		if(null != chkbox && true == chkbox.checked) {
			if(rowCount <= 1) { 						// limit the user from removing all the fields
				alert("Cannot Remove all pool members.");
				break;
			}
			table.deleteRow(i);
			rowCount--;
			i--;
		}
	}
}

//Old Table Row cleanup - Delete existing all rows except first row
function deleteAllRows(tableID) {
	var table = document.getElementById(tableID);
	var rowCount = table.rows.length;
	
	for(var x=rowCount-1; x>1; x--) {
		table.deleteRow(x);
	}
}

// Delete a row by name
function deleteRowByName(tableID, name) {
	var table = document.getElementById(tableID);
	var rowCount = table.rows.length;
	for(var i=1; i<rowCount; i++) {
		var row = table.rows[i];
		var chkbox = row.cells[0].childNodes[0];
		if(null != chkbox && true == chkbox.checked) {
			var col1 = '#' + tableID + ' tbody tr:eq(' + i + ') td:eq(1)';
			var rowName = $(col1).children().val();
			if(rowName == name){
				table.deleteRow(i);
				rowCount--;
				i--;
			}
		}
	}
}

// Check if there is checked rows at least one
function hasCheckedRow(tableID) {
	var table = document.getElementById(tableID);
	var rowCount = table.rows.length;
	if (rowCount == 1 && table.rows[1].cells[1].firstChild.value == ""){
		return "false";
	}
	
	var numOfChecked = 0;
	for(var i=1; i<rowCount; i++) {
		var row = table.rows[i];
		var chkbox = row.cells[0].childNodes[0];
		if(null != chkbox && true == chkbox.checked)
			numOfChecked++;
	}
	//alert("Number of checked box: " + numOfChecked);
	if (numOfChecked >= 1) return "true";
	else return "false";
}



//Add a new table row to display content information
function addPolRow(tableID) {
	var table = document.getElementById(tableID);
	var rowCount = table.rows.length;

	var row = table.insertRow(rowCount);
	var colCount = table.rows[1].cells.length;
	for(var i=0; i<colCount; i++) {
		var newcell = row.insertCell(i);
		newcell.innerHTML = table.rows[1].cells[i].innerHTML;
	}
}

// Process Draft and published policy names returned from BIG-IP
function loadPolNamesProcess(response_in){
	//Return Data Format: 'polType':'draft|published', 'name':'', 'partition':''
	var numOfPols = Object.keys(response_in).length;
	
	if (numOfPols == 0) { alert("No Policy exists"); return; }
	var col1='';
	var col2='';

	var dftIdx = 1;
	var pubIdx = 1;
	$.each(response_in, function(index){
		
		if (response_in[index].polType == 'FAIL'){
			var strResult = '';
			strResult = strResult + "<b>Loading Policy Names has failed!</b><br>";
			strResult = strResult + "Error Detail: " + response_in[index].partition + "<br>";
			$('#delPol_EvalReview').append(strResult);
			return;
		}
		else if (response_in[index].polType == 'draft'){
			if(dftIdx != 1 ) {
				addPolRow('dftDataTable');
			}
			
			col1 = '#dftDataTable tbody tr:eq(' + dftIdx + ') td:eq(1)';
			col2 = '#dftDataTable tbody tr:eq(' + dftIdx + ') td:eq(2)';
			
			$(col1).children().val(response_in[index].name);
			$(col2).children().val(response_in[index].partition);

			dftIdx = dftIdx + 1;
		}
		else if (response_in[index].polType == 'published'){
			if(pubIdx != 1) {
				addPolRow('pubDataTable');
			}
			
			col1 = '#pubDataTable tbody tr:eq(' + pubIdx + ') td:eq(1)';
			col2 = '#pubDataTable tbody tr:eq(' + pubIdx + ') td:eq(2)';
			
			$(col1).children().val(response_in[index].name);
			$(col2).children().val(response_in[index].partition);

			pubIdx = pubIdx + 1;
		}
	});
	
	return;
}

// Process the result data of deleting policies from BIG-IP
function delPolProcess(response_in){
	//'name':'', 'polType':'draft|published', 'result':'', 'message':''
	var strResult = '';
	
	$.each(response_in, function(index){
		if (response_in[index].result == "SUCCESS"){
			strResult += "<b>" + response_in[index].name + " has been deleted successfully</b><br>";
			strResult += response_in[index].message + "<br>";
			if (response_in[index].polType == 'draft'){
				deleteRowByName('dftDataTable', response_in[index].name);	
			}
			else if (response_in[index].polType == 'published'){
				deleteRowByName('pubDataTable', response_in[index].name);	
			}
		}
		else{
			strResult += "<b>" + response_in[index].name + " deletion has failed</b><br>";
			strResult += response_in[index].message + "<br>";			
		}
	});
	
	$('#delPol_EvalReview').append(strResult);
	return;

}

//JQueury 
$(function () {
	
	$('#div_ltmchoice').on('change', function() {
		var nameAndIp = $('#ltmSelBox option:selected').val();
		var arr = nameAndIp.split(":");
		
		if(GetParentURLParameter('go') == 'del_policies'){
			if (nameAndIp == 'Select...') {
				// Reset all fields
				deleteAllRows('dftDataTable');
				deleteAllRows('pubDataTable');
				$('#dftDataTable tbody tr:eq(1) td:eq(1)').children().val("");
				$('#dftDataTable tbody tr:eq(1) td:eq(2)').children().val("");
				$('#pubDataTable tbody tr:eq(1) td:eq(1)').children().val("");
				$('#pubDataTable tbody tr:eq(1) td:eq(2)').children().val("");
				return;
			}
		}
	
		// Load Draft and Published Policy Names and Partitions
		if(GetParentURLParameter('go') == 'del_policies'){
			var polData = {'PhpFileName':'load_polnames_ajax', 'DevIP':''};
			polData['DevIP'] = arr[1];
			ajxOut = $.ajax({
				url: '/content/load_polnames_ajax.php',
				type: 'POST',
				dataType: 'JSON',
				data: {'jsonData' : JSON.stringify(polData)},
				error: function(jqXHR, textStatus, errorThrown){
					alert("Ajax call to load policy names has failed!");
		            console.log('jqXHR:');
		            console.log(jqXHR);
		            console.log('textStatus:');
		            console.log(textStatus);
		            console.log('errorThrown:');
		            console.log(errorThrown);
				}
			});
			ajxOut.done(loadPolNamesProcess);
		}
	});
	
	// Event handler when "Delete Policies" button for Draft policies is clicked.
	$('#btn_delpoldft').on('click', function(){
		
    	if (hasCheckedRow('dftDataTable') == 'false') {
    		alert("Please select a Dfart Policy(ies) to delete");
    		return;
    	}
    	//else alert("Moving forward");
    	
    	var nameAndIp = $('#ltmSelBox option:selected').val();
    	var arr = nameAndIp.split(":");
    	
    	var paramData = {'PhpFileName':'del_pol_ajax', 'DevIP':arr[1], 'polType':'draft'};
    	// dftPolData - Array data of {name1, part1, name2, part2, ... }
    	var dftPolData = [];
    	
    	var table = document.getElementById('dftDataTable');
    	var rowCount = table.rows.length;
    	
    	// Selected Draft Policies data collection
    	for(var i=1;i<rowCount;i++){
    		var row = table.rows[i];
    		var chkbox = row.cells[0].childNodes[0];
    		if(null != chkbox && true == chkbox.checked) {
    			for(colIdx=1;colIdx<=2;colIdx++){
	    			var col1 = '#dftDataTable tbody tr:eq(' + i + ') td:eq(' + colIdx + ')';
	    			dftPolData.push($(col1).children().val())
    			}
    		}
    	}
    	// Call ajax to pass the chosen Draft Policy info to BIG-IP and delete them from BIG-IP
		ajxOut = $.ajax({
			url: '/content/del_pol_ajax.php',
			type: 'POST',
			dataType: 'JSON',
			data: {'jsonData' : JSON.stringify(paramData), 'dftPolData': JSON.stringify(dftPolData)},
			error: function(jqXHR, textStatus, errorThrown){
				alert("Ajax call to delete Draft Policy has failed!");
	            console.log('jqXHR:');
	            console.log(jqXHR);
	            console.log('textStatus:');
	            console.log(textStatus);
	            console.log('errorThrown:');
	            console.log(errorThrown);
			}
		});
		ajxOut.done(delPolProcess);
		
	});
	
	//Event handler when "Delete Policies" button for Published policies is clicked.
	$('#btn_delpolpub').on('click', function(){
    	if (hasCheckedRow('pubDataTable') == 'false') {
    		alert("Please select a Published Policy(ies) to delete");
    		return;
    	}
    	//else alert("Moving forward");
    	
    	var nameAndIp = $('#ltmSelBox option:selected').val();
    	var arr = nameAndIp.split(":");
    	
    	var paramData = {'PhpFileName':'del_pol_ajax', 'DevIP':arr[1], 'polType':'published'};
    	// pubPolData - Array data of {name1, part1, name2, part2, ... }
    	var pubPolData = [];
    	
    	var table = document.getElementById('pubDataTable');
    	var rowCount = table.rows.length;
    	
    	// Selected published policy data collection
    	for(var i=1;i<rowCount;i++){
    		var row = table.rows[i];
    		var chkbox = row.cells[0].childNodes[0];
    		if(null != chkbox && true == chkbox.checked) {
    			for(colIdx=1;colIdx<=2;colIdx++){
	    			var col1 = '#pubDataTable tbody tr:eq(' + i + ') td:eq(' + colIdx + ')';
	    			pubPolData.push($(col1).children().val())
    			}
    		}
    	}
    	// Call ajax to pass the chosen Draft Policy info to BIG-IP and delete them from BIG-IP
		ajxOut = $.ajax({
			url: '/content/del_pol_ajax.php',
			type: 'POST',
			dataType: 'JSON',
			data: {'jsonData' : JSON.stringify(paramData), 'pubPolData': JSON.stringify(pubPolData)},
			error: function(jqXHR, textStatus, errorThrown){
				alert("Ajax call to delete Published Policy has failed!");
	            console.log('jqXHR:');
	            console.log(jqXHR);
	            console.log('textStatus:');
	            console.log(textStatus);
	            console.log('errorThrown:');
	            console.log(errorThrown);
			}
		});
		ajxOut.done(delPolProcess);
	});
	
	
});