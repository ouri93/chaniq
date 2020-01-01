/* 
 * Javascript for managing BIG-IP LTM/GTM Admin passwords
 */
//Read the parent URL parameters and return a query parameter value against a given key
//e.g. URL: http://www.example.com/?go=chg_profile
//     GetParentURLParameter('go')
//     Return: chg_profile
function GetParentURLParameter(sParam)
{
   var parentURL = window.top.location.href;

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

/*
 * Source: https://www.w3resource.com/javascript/form/email-validation.php
 * Input: Your Input
 * Return: If your input is eligible email address format, return 'true'. Otherwise return 'false' 
*/
function ValidateEmail(mail) 
{
 if (/^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/.test(mail))
  {
    return (true)
  }
    return (false)
}

$(function () {
	$('#submit_setpass').on('click', function() {
		var param = GetParentURLParameter('go');
		
		// Regex Strong Password check - Use Regexp.test(str)
		// Return - True if matching to regex. Otherwise return False
		// at least 1 lowercase, uppercase, number, and special character. Password must be eight characters or longer
		var strongRegex = new RegExp("^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#\$%\^&\*])(?=.{8,})");
		
		var pass1 = $('#setpass1').val();
		var pass2 = $('#setpass2').val();
		
		if ( pass1 == "" || pass2 == "" ){
			alert("Password is not set!\nPlease type the password you want to set");
			return;
		}
		if ( pass1 != pass2 || (pass1).length != (pass2).length ){
			alert("Password is not matching!");
			return;
		}
		
		if ( param == 'admpw_mgmt' && strongRegex.test(pass1) ){
			//alert("It\'s Strong password and ready to save the password");
	    	
			var passData = {'PhpFileName':'', 'Pass1':''};
	    	
			passData['PhpFileName'] = 'resetpass_ajax';
			passData['BigipType'] = $('#set_module option:selected').val();
			passData['Pass1'] = pass1;
	    	
			//alert("Filename: " + passData['PhpFileName'] + " BIGIP Type: " + passData['BigipType'] + " Password: " + passData['Pass1'] );
			// ajax call to save password
			ajxOut = $.ajax({
				url: '/content/resetpass_ajax.php',
				type: 'POST',
				dataType: 'JSON',
				async: false,
				data: {'jsonPassData' : JSON.stringify(passData)},
				error: function(jqXHR, textStatus, errorThrown){
					alert("Ajax call to reset password has failed!");
		            console.log('jqXHR:');
		            console.log(jqXHR);
		            console.log('textStatus:');
		            console.log(textStatus);
		            console.log('errorThrown:');
		            console.log(errorThrown);
				}
			});
	    	ajxOut.done(function (response_in) {
	    		//alert("Response: " + response_in);
	    		var strResult = '';

	    		$.each(response_in, function(index) {
	    			if(index == 0) 
	    				strResult = "<b>" + response_in[index] + "</b><br>";
	    			else
	    				strResult += response_in[index] + "<br>";
	    		});
	
	    		$('#admin_ResultReview').html(strResult);
	    	});
	    	$('#setpass1').val('');
	    	$('#setpass2').val('');
		}
		else{
			alert("Your password doesn't meet password requirement");
			return;
		}
	});

	$('#submit_modpass').on('click', function() {
		var param = GetParentURLParameter('go');
		
		// Regex Strong Password check - Use Regexp.test(str)
		// Return - True if matching to regex. Otherwise return False
		// at least 1 lowercase, uppercase, number, and special character. Password must be eight characters or longer
		var strongRegex = new RegExp("^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#\$%\^&\*])(?=.{8,})");
		
		var pass1 = $('#modpass1').val();
		var pass2 = $('#modpass2').val();
		var pass3 = $('#modpass3').val();
		
		if ( pass1 == "" || pass2 == "" || pass3 == "" ){
			alert("Password is not set!\nPlease type the password you want to set");
			return;
		}
		if ( pass2 != pass3 || (pass2).length != (pass3).length ){
			alert("Password is not matching!");
			return;
		}
		
		if ( param == 'admpw_mgmt' && strongRegex.test(pass1) && strongRegex.test(pass2) ){
			//alert("It\'s Strong password and ready to save the password");
	    	
			var passData = {'PhpFileName':'', 'CurPass':'', 'NewPass':''};
	    	
			passData['PhpFileName'] = 'modpass_ajax';
			passData['BigipType'] = $('#mod_module option:selected').val();
			passData['CurPass'] = pass1;
			passData['NewPass'] = pass2;
	    	
			//alert("Filename: " + passData['PhpFileName'] + " BIGIP Type: " + passData['BigipType'] + " Password: " + passData['Pass1'] );
			// ajax call to save password
			ajxOut = $.ajax({
				url: '/content/modpass_ajax.php',
				type: 'POST',
				dataType: 'JSON',
				async: false,
				data: {'jsonPassData' : JSON.stringify(passData)},
				error: function(jqXHR, textStatus, errorThrown){
					alert("Ajax call to modify password has failed!");
		            console.log('jqXHR:');
		            console.log(jqXHR);
		            console.log('textStatus:');
		            console.log(textStatus);
		            console.log('errorThrown:');
		            console.log(errorThrown);
				}
			});
	    	ajxOut.done(function (response_in) {
	    		//alert("Response: " + response_in);
	    		var strResult = '';

	    		$.each(response_in, function(index) {
	    			if(index == 0) 
	    				strResult = "<b>" + response_in[index] + "</b><br>";
	    			else
	    				strResult += response_in[index] + "<br>";
	    		});
	
	    		$('#admin_ResultReview').html(strResult);
	    	});
	    	$('#modpass1').val('');
	    	$('#modpass2').val('');
	    	$('#modpass3').val('');
		}
		else{
			alert("Your password doesn't meet password requirement");
			return;
		}

	});
	
	$('#submit_unPass').on('click', function() {
		var param = GetParentURLParameter('go');
		
		// Regex Strong Password check - Use Regexp.test(str)
		// Return - True if matching to regex. Otherwise return False
		// at least 1 lowercase, uppercase, number, and special character. Password must be eight characters or longer
		var strongRegex = new RegExp("^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#\$%\^&\*])(?=.{8,})");
		
		var unEmail = $('#unEmail').val();
		var role = $('#unRole option:selected').val();
		var pass1 = $('#unPass1').val();
		var pass2 = $('#unPass2').val();

		if ( !(ValidateEmail(unEmail)) ){
			alert("Username must be a valid email address");
			return;
		}

		if ( pass1 == "" || pass2 == "" ){
			alert("Password is not set!\nPlease type the password you want to set");
			return;
		}
		if ( pass1 != pass2 || (pass1).length != (pass2).length ){
			alert("Password is not matching!");
			return;
		}
		
		if ( param == 'admin_user' && strongRegex.test(pass1) ){
			//alert("It\'s Strong password and ready to save the password");
	    	
			var passData = {'PhpFileName':'', 'UserName':'', 'UserRole':'', 'Pass1':''};
	    	
			passData['PhpFileName'] = 'newuser_ajax';
			passData['UserName'] = unEmail;
			passData['UserRole'] = role;
			passData['Pass1'] = pass1;
	    	
			//alert("Filename: " + passData['PhpFileName'] + " User Role: " + passData['UserRole'] + " Password: " + passData['Pass1'] );
			// ajax call to create a new user
			ajxOut = $.ajax({
				url: '/content/newuser_ajax.php',
				type: 'POST',
				dataType: 'JSON',
				async: false,
				data: {'jsonPassData' : JSON.stringify(passData)},
				error: function(jqXHR, textStatus, errorThrown){
					alert("Ajax call to create a new user has failed!");
		            console.log('jqXHR:');
		            console.log(jqXHR);
		            console.log('textStatus:');
		            console.log(textStatus);
		            console.log('errorThrown:');
		            console.log(errorThrown);
				}
			});
	    	ajxOut.done(function (response_in) {
	    		//alert("Response: " + response_in);
	    		var strResult = '';

	    		$.each(response_in, function(index) {
	    			if(index == 0) 
	    				strResult = "<b>" + response_in[index] + "</b><br>";
	    			else
	    				strResult += response_in[index] + "<br>";
	    		});
	
	    		$('#admin_ResultReview').html(strResult);
	    	});
	    	$('#unEmail').val('');
	    	$('#unPass1').val('');
	    	$('#unPass2').val('');
		}
		else{
			alert("Your password doesn't meet password requirement");
			return;
		}
	});
	
	$('#submit_modUser').on('click', function() {
		var param = GetParentURLParameter('go');

		// Regex Strong Password check - Use Regexp.test(str)
		// Return - True if matching to regex. Otherwise return False
		// at least 1 lowercase, uppercase, number, and special character. Password must be eight characters or longer
		var strongRegex = new RegExp("^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#\$%\^&\*])(?=.{8,})");
		
		var username = $('#rst_unEmail').val();
		var role = $('#rst_unRole option:selected').val();
		var pass2 = $('#rst_unPass1').val();
		var pass3 = $('#rst_unPass2').val();
		
		if (username == 'admin' && role == 'guest'){
			alert("Admin user's role must be admin");
			return;
		}
		if ( username != 'admin' && !(ValidateEmail(username)) ) {
			alert("Username must be email address except admin built-in user");
			return;
		}
		if ( pass2 == "" || pass3 == "" ){
			alert("Password is not set!\nPlease type the password you want to set");
			return;
		}
		if ( pass2 != pass3 || (pass2).length != (pass3).length ){
			alert("Password is not matching!");
			return;
		}
		
		if ( param == 'admin_user' && strongRegex.test(pass2) && strongRegex.test(pass3) ){
			//alert("It\'s Strong password and ready to save the password");
	    	
			var passData = {'PhpFileName':'', 'UserName':'', 'UserRole':'', 'NewPass':''};
	    	
			passData['PhpFileName'] = 'resetuserpw_ajax';
			passData['UserName'] = username;
			passData['UserRole'] = role;
			passData['NewPass'] = pass2;
			
			//alert("Filename: " + passData['PhpFileName'] + " BIGIP Type: " + passData['BigipType'] + " Password: " + passData['Pass1'] );
			// ajax call to save password
			ajxOut = $.ajax({
				url: '/content/resetuserpw_ajax.php',
				type: 'POST',
				dataType: 'JSON',
				async: false,
				data: {'jsonPassData' : JSON.stringify(passData)},
				error: function(jqXHR, textStatus, errorThrown){
					alert("Ajax call to reset CHAN-IQ User's role and password has failed!");
		            console.log('jqXHR:');
		            console.log(jqXHR);
		            console.log('textStatus:');
		            console.log(textStatus);
		            console.log('errorThrown:');
		            console.log(errorThrown);
				}
			});
	    	ajxOut.done(function (response_in) {
	    		//alert("Response: " + response_in);
	    		var strResult = '';

	    		$.each(response_in, function(index) {
	    			if(index == 0) 
	    				strResult = "<b>" + response_in[index] + "</b><br>";
	    			else
	    				strResult += response_in[index] + "<br>";
	    		});
	
	    		$('#admin_ResultReview').html(strResult);
	    	});
	    	$('#rst_unEmail').val('');
	    	$('#rst_unCurrent').val('');
	    	$('#rst_unPass1').val('');
	    	$('#rst_unPass2').val('');
		}
		else{
			alert("Your password doesn't meet password requirement");
			return;
		}

	});	
});