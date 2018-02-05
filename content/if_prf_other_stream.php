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
                 
        <script type="text/javascript" src="/js/prf_jquery.js"></script>
        <title>Create Stream Profile</title>
    </head>
    <body style="background-color: #ffffff;">
        <form class="inner-form">
            <fieldset class="row1">
                <p>
                	<table id="prfConfTable" class="form" border="1">
    	            	<tbody id="prfConfTable_tbody">
    	            	<tr> <td width='132px'><label>*Name:</label> </td><td><input type='text' id='prf_name' required='required' /></td></tr>
    	            	<tr id='tr_svc_prf_type' >
    	            		<td width='132px' ><label>*Parent Profile:</label></td><td><select id='svc_prf_type_select' required='required' ><option id='noDelete' value='select' selected='selected' >Select...</option></select></td>
    	            	</tr>
    			        <!--  Conditional HTML code here  --> 
            	        </tbody>
                    </table>
                </p>
                <p>*: Required field</p>
                <p align="right">
    	            <input id="prf_btn_build" type="button" style="width:130px" name="prf_btn_build" value="Build" />
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