<?php
session_start();
if ($_SESSION['loggedin'] != true){
    session_unset();
    session_destroy();
    header('Location: ../login.php');
}
//Admin Content - Visible if the logged-in user has admin role
if ($_SESSION['role'] == 'guest'){
    header('Location: contentbase.php');
}
include_once('../utility/utility.php');

?>
<html>
    <head>
        <meta charset="UTF-8">
        <link rel="stylesheet" href="/css/style.css" type="text/css" media="screen" />
        <!-- 
        For Produciton 
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js" </script>
        <script> window.jQuery || document.write("<script src='/js/jquery-3.2.1.min.js'><\/script>");  
        -->

        <!-- For Development --> 
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.js" </script>
        <script> window.jQuery || document.write("<script src='/js/jquery-3.2.1.js'><\/script>"); </script>  
                 
        <script type="text/javascript" src="/js/ssl_jquery.js"></script>
        <title>SSL Cert and Key Management</title>
    </head>
    <body style="background-color: #ffffff;">
        <form class="inner-form">
            <fieldset class="row1">
                <p>
                	<table id="crtConfTable" class="form" border="1">
    	            	<tbody id="crtConfTable_tbody">
    	            	<tr id='create_cert_type' >
    	            		<td width='132px' ><label>*Issuer:</label></td><td><select id='create_type_select' required='required' ><option value='select' selected='selected' >Select...</option><option value='Self' >Self</option><option value='Certificate Authority' >Certificate Authority</option></input></td>
    	            	</tr>
    			        <!--  Conditional HTML code here  --> 
            	        </tbody>
                    </table>
                </p>
                <p>*: Required field</p>
            	<p align="right">
	            	<input id="crt_create_btn_build" type="button" style="width:130px" name="crt_create_btn_build" value="Deploy Cert/Key" />
            	</p>
            	<p></p>
            </fieldset>
            <fieldset class="row1">        
                <legend>Evaluation Result and Review</legend>
                <div>
                    <p id="newcrt_EvalReview">
        			</p>
                </div>
	        </fieldset>        
        </form>
    </body>
</html>