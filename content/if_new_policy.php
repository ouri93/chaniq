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
        <!-- For Produciton 
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>
        <script> window.jQuery || document.write("<script src='/js/jquery-3.2.1.min.js'><\/script>"); </script>  
        -->
        
        <!-- For Development  -->
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.js"> </script>
        <script> window.jQuery || document.write("<script src='/js/jquery-3.2.1.js'><\/script>"); </script>  
                 
        <script type="text/javascript" src="/js/policy_jquery.js"></script>
        <title>Create a new Policy</title>
    </head>
    <body style="background-color: #ffffff;">
        <form class="inner-form">
            <h1> Create a new Policy </h1>
            <fieldset class="row1">
                <legend>Select a target LTM</legend>
                <?php
                    // Load all BIG-IP devices name and IP
                    $allBigips = load_all_bigips();
                    $allBigipNames = array();
    
                    $allBigipNames[0] = 'Select...';
                    $i=1;
                    foreach($allBigips as $name => $ip){
                        $allBigipNames[$i] = $name . ":" . $ip;
                        $i += 1;
                    }
                    asort($allBigipNames);
                ?>
                <p>
                    <div id='div_ltmchoice' class="ltmDeviceList">
                    	<?php 
                    	dynamic_select($allBigipNames, "ltmSelBox", "", "Select...");
                    	?>
                    </div>
                </p>
            </fieldset>
            <fieldset class="row1">
                <legend>Policy Building Configuration</legend>
                <p>
                <table class="form" border="1">
                    <tbody id="polDataTbody" >
                        <tr>
                            <td style="width:120px"> <label>*Policy Name: </label> </td>
                            <td> <input type="text" name="pol_name" id="pol_name" /></td>
                        </tr>
                        <tr>
                        	<td> <label>Policy Description: </label> </td>
                            <td> <input type="text" name="pol_desc" id="pol_desc" /></td>
                        </tr>
                        <tr>
                        	<td> <label>Strategy: </label> </td>
                            <td><label>Execute</label><select style='width:60px;height:20px;' id='pol_strategy'><option value='all-match'>all</option><option value='first-match' selected>first</option><option value='best-match'>best</option></select><label>matching rule</label></td>
                        </tr>
                    </tbody>
                </table>
                </p>
            </fieldset>
            <fieldset class="row1">
                <legend>Policy Rule Configuration</legend>
                <p>
                <table class="form" border="1">
                    <tbody id="polDataTbody2" >
                    	<tr><th style="width:20px"><input type="checkbox" id="rule_chkbox_all" checked/></th style="width:80px"><th>ID</th><th style="width:200px">Name</th><th>Description</th></tr>
                        <tr>
                        	<td></td>
                        	<td>col1</td>
                        	<td>col2</td>
                        	<td>col3</td>
                        </tr>
                    </tbody>
                </table>
                </p>
           		<input id="rule_delete" type="button" name="rule_delete" value="Delete" style="width:50px; float: left;" />
            </fieldset>

           	<p></p>
            <fieldset class="row1">                
                <legend>Rule Creation</legend>
                <table class="form" border="1">
                	<tbody id="polDataTbody3">
                	   	<tr>
                            <td style="width:120px"> <label>*Rule Name: </label> </td>
                            <td> <input type="text" name="rule_name" id="rule_name" /></td>
                        </tr>
                        <tr>
                        	<td> <label>Rule Description: </label> </td>
                            <td> <input type="text" name="rule_desc" id="rule_desc" /></td>
                        </tr>
                	</tbody>
                </table>
                <p></p>
                <table class="form" border="1">
                	<tr id='row_title'>
                		<td><label>Match all of the following conditions:</label></td>
                	</tr>
                	<tr id='row0'>
                		<td><p>All traffic<input type='button' id='rulecon_add1' style="width:15px; font-weight:900; float: right;" value='+' /></p></td>
                	</tr>
                </table>
                <p></p>                
                <table class="form" border="1">
                	<tr id='row_title'>
                		<td><label>Do the following when the traffic is matched:</label></td>
                	</tr>
                	<tr id='row0'>
                		<td><p>Ignore<input type='button' id='ruleact_add1' style="width:15px; font-weight:900; float: right;" value='+' /></p></td>
                	</tr>
                </table>                
                <p></p>
                <input id="rule_add" type="button" name="rule_add" value="Add Rule" style="width:70px; float: right;" />
                <p></p>
            </fieldset>
            <p>*: Required field</p>
            <input id="pol_build" type="button" name="pol_build" value="Deploy Policy" style="width:100px; float: right;" />
            <p></p>
            <fieldset class="row1">        
                <legend>Evaluation Result and Review</legend>
                <div>
                    <p id="newPol_EvalReview">
        			</p>
                </div>
            </fieldset>        
        </form>
    </body>
</html>