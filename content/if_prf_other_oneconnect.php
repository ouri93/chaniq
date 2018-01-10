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
        <title>Create Service Profile</title>
    </head>
    <body style="background-color: #ffffff;">
        <form class="inner-form">
            <fieldset class="row1">
                <p>
                	<table id="prfConfTable" class="form" border="1">
    	            	<tbody id="prfConfTable_tbody">
    	            	<tr id='import_cert_type' >
    	            		<td width='132px' ><label>*Import Type:</label></td><td><select id='imp_type_select' required='required' ><option value='select' selected='selected' >Select...</option><option value='Key' >Key</option><option value='Certificate' >Certificate</option><option value='PKCS 12 (IIS)' >PKCS 12 (IIS)</option></input></td>
    	            	</tr>
    			        <!--  Conditional HTML code here  --> 
            	        </tbody>
                    </table>
                </p>
                <p>*: Required field</p>
                <p align="right">
    	            <input id="prf_btn_build" type="button" style="width:130px" name="prf_btn_build" value="Import Cert/Key" />
                </p>
                <p></p>
            </fieldset>
            <fieldset class="row1">        
                <legend>Evaluation Result and Review</legend>
                <div>
                    <p id="newprf_EvalReview">
        			</p>
                </div>
	        </fieldset>        
        </form>
    </body>
</html>