<?php
require_once(__DIR__ . '/../utility/chaniqLogger.php');

session_start();
#file_put_contents("/var/log/chaniqphp.log", "if_new_vs.php UN: " .$_SESSION['username'] . " Role: " . $_SESSION['role'] . " LoggedIn: " . $_SESSION['loggedin'] . "\n", FILE_APPEND);
$logger->info("if_new_vs.php UN: " .$_SESSION['username'] . " Role: " . $_SESSION['role'] . " LoggedIn: " . $_SESSION['loggedin']);
if ($_SESSION['loggedin'] != true){
    session_unset();
    session_destroy();
    #file_put_contents("/var/log/chaniqphp.log", "if_new_vs.php redirection to login page!!\n", FILE_APPEND);
    $logger->info("if_new_vs.php redirection to login page!!");
    header('Location: ../login.php');
}
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
                 
        <script type="text/javascript" src="/js/vs_jquery.js"></script>
        
        <title>Create a new Virtual Server</title>
    </head>
    <body style="background-color: #ffffff;">
        <form class="inner-form">
            <h1> Create a new Virtual Server </h1>
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
            <legend>Virtual Server</legend>
                <p>
                    <label>*DNS/VS Name: </label>
                    <input type="text" name="vs_dnsname" id="vs_dnsname" required="required" />
                    <label>*Dest. IP: </label>
                    <input type="text" name="vs_dest" id="vs_dest" onfocusout="ipValidation('vs_dest')" required="required" />
                    <label>*Service Port: </label>
                    <input type="text" name="vs_port" id="vs_port" onfocusout="portValidation('vs_port')" onkeypress='return event.charCode >= 48 && event.charCode <= 57' required="required" />
                </p>
                <p>
                    <label>Description: </label>
                    <input type="text" id="vs_desc" name="vs_desc" maxlength="128" />
                    <label>*Env.: </label>
                    <select id='vs_env' name="vs_env" required="required"> 
                    <?php
                    $iniarray = parse_ini_section_file();
    
                    foreach ($iniarray as $section => $values){
                        $myx = (string)$section;
                        //$myxval = (string)$values;
                        if ($myx == "LTM_GTM_ENVIRONMENT"){
                            foreach ($values as $key=>$value){
                                echo "<option> " . $value ."</option>";
                            }
                        }
                    }
                    ?>
                    </select>
                    <label>*VS Type: </label>
                    <select id="vs_type" name="vs_type" required="required">
                        <option>Standard</option>
                        <option>Forwarding (IP)</option>
                    </select>
                </p>
                <p>
                	<label> TCP Profile:</label>
                	<select id='vs_tcpprofile' name='vs_tcpprofile'><option value='none'>None</option></select>
                    <label> Persistence:</label>
                	<select id='vs_persist' name='vs_persist'><option value='none'>None</option></select>
                    <label>Redirection</label>
                    <select id='vs_redirect' name="vs_redirect" required="required">
                        <option>NO</option>
                        <option>YES</option>
                    </select>                
                </p>
				<p>
					<label> iRule:</label>
                	<select id='vs_irule' name='vs_irule'><option value='none'>None</option></select>
                    <label> SNAT Pool:</label>
                	<select id='vs_snatpool' name='vs_snatpool'><option value='none'>None</option></select>
                    <label> Policies:</label>
                	<select id='vs_policy' name='vs_policy'><option value='none'>None</option></select>
                   
				</p>
				<p>
					<label> HTTP Profile:</label>
                	<select id='vs_httpprf' name='vs_httpprf'><option value='none'>None</option></select>
                    <label> Client SSL Profile:</label>
                	<select id='vs_clisslprf' name='vs_clisslprf'><option value='none'>None</option></select>
                    <label> Server SSL Profile:</label>
                	<select id='vs_srvsslprf' name='vs_srvsslprf'><option value='none'>None</option></select>
				</p>
				<p>
					<label> Pool:</label>
					<select id='vs_pool_chosen' name='vs_pool_chosen'><option value='none' selected='selected'>None</option><option value='newPool'>New Pool</option></select>
					<!--  <input id="btn_createPool" type="button" style="width:130px" name="btn_createPool" value="Create a New Pool" />
					<label>Create a new pool?</label><input aligh='right' type='checkbox' id='chkbox_vs_new_pool' />  -->
				</p>
				</fieldset>
				<!-- 
                <fieldset class="row1">
                    <legend>Pool Configuration</legend>
                    <p>
                    <label>*DNS/Pool Name:</label>
                    <input type='text' id='vs_poolname' required />
                    <label>Pool Monitor:</label>
                    <select id='vs_poolmon' name='vs_poolmon'><option value='none' selected>None</option></select>
    				<label> Number of Pool Members:</label>
    				<select id='vs_poolmbrnum'>
    					<option value='0' selected>0</option>
    					<option value='1' >1</option>
    					<option value='2' >2</option>
    					<option value='3' >3</option>
    					<option value='4' >4</option>
    					<option value='5' >5</option>
    					<option value='6' >6</option>
    					<option value='7' >7</option>
    					<option value='8' >8</option>
    					<option value='9' >9</option>
    					<option value='10' >10</option>
    				</select>
                    </p>
                    <table id="dataTable" class="form" border="1">
                        <tbody id="poolmbrTbody">
                        </tbody>
                    </table> -->
                    <!-- 
                    <p></p>
                    <input type="button" value="Remove Member" onClick="deleteRow('dataTable')"  /> 
                    <input type="button" value="Add Member" onClick="addRow('dataTable')" /> 
                    <div class="clear"></div>
                     -->
                <!-- 
                </fieldset>
                -->
                <p>*: Required field</p>
    		</fieldset>
            
            <p align="right">
	            <input id="vs_btn_build" type="button" style="width:130px" name="vs_btn_build" value="Build" />
            </p>
            <p></p>
            <fieldset class="row1">        
                <legend>Evaluation Result and Review</legend>
                <div>
                    <p id="newvs_EvalReview">
        			</p>
                </div>
	        </fieldset>        
        </form>
    </body>
</html>