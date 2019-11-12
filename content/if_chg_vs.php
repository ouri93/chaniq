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
        <?php include('../utility/utility.php'); ?>
        <title>Create a new Virtual Server</title>
    </head>
    <body style="background-color: #ffffff;">
        <form class="inner-form">
            <h1> Modify a Virtual Server </h1>
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
                    <div id='chg_div_ltmchoice' class="chgltmDeviceList">
                    	<?php 
                    	dynamic_select($allBigipNames, "ltmSelBox", "", "Select...");
                    	?>
                    </div>
                </p>
            </fieldset>
			<fieldset class="row1">
				<legend> Select a Virtual Server</legend>
				<p>
					<label> Virtual Server:</label>
					<select id='chg_vs_sel_vs' name='chg_vs_sel_vs'><option value='select'>Select...</option></select>
				</p>
			</fieldset>            
            <fieldset class="row1">
            <legend>Virtual Server Configuration</legend>
                <p>
                    <label>Description: </label>
                    <input type="text" id="vs_desc" name="vs_desc" maxlength="128" required="required" />
                    <label>*Dest. IP: </label>
                    <input type="text" name="vs_dest" id="vs_dest" onfocusout="ipValidation('vs_dest')" required="required" />
                    <label>*Service Port: </label>
                    <input type="text" name="vs_port" id="vs_port" onfocusout="portValidation('vs_port')" onkeypress='return event.charCode >= 48 && event.charCode <= 57' required="required" />
                </p>
                <p>
                    <label>*VS Type: </label>
                    <select id="vs_type" name="vs_type" required="required">
                        <option>Standard</option>
                        <option>Forwarding (IP)</option>
                    </select>
                	<label> TCP Profile:</label>
                	<select id='vs_tcpprofile' name='vs_tcpprofile'><option value='none'>None</option></select>
                    <label> Persistence:</label>
                	<select id='vs_persist' name='vs_persist'><option value='none'>None</option></select>
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
					<select id='chg_vs_pool_chosen' name='chg_vs_pool_chosen'><option value='none' selected='selected'>None</option></select>
				</p>
				</fieldset>
                <p>*: Required field</p>
    		</fieldset>
            
            <p align="right">
	            <input id="btn_vs_modify" type="button" style="width:130px" name="btn_vs_modify" value="Update VS" />
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