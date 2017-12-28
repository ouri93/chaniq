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
    	            		<td>Issuer Type:</td><td><select id='create_type_select' required='required' ><option value='select' selected='selected' >Select...</option><option value='self' >Self</option><option value='ca' >Certificate Authority</option></input></td>
    	            	</tr>
    			        <!--  Conditional HTML code here  --> 
            	        </tbody>
                    </table>
                </p>
            	<p align="right">
	            	<input id="crt_btn_build" type="button" name="crt_btn_build" value="Deploy Cert/Key" />
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