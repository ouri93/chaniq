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
                 
        <script type="text/javascript" src="/js/ir_jquery.js"></script>
        <?php
        if (GetParentURLParameter('go') == 'new_irule' ) {
            echo '<title>Create iRules/Data Groups</title>';    
        }
        else if(GetParentURLParameter('go') == 'chg_irule' ) {
            echo '<title>Change iRules/Data Groups</title>';
        }
        else if(GetParentURLParameter('go') == 'del_irule' ) {
            echo '<title>Delete iRules/Data Groups</title>';
        }
        ?>
    </head>
    <body style="background-color: #ffffff;">
        <form class="inner-form">
        	<?php
        	if (GetParentURLParameter('go') == 'new_irule' ) {
        	   echo '<h1> Create iRules/Data Groups </h1>';
        	}
        	else if(GetParentURLParameter('go') == 'chg_irule' ) {
        	   echo '<h1> Change iRules/Data Groups </h1>';
        	}
        	else if(GetParentURLParameter('go') == 'del_irule' ) {
        	    echo '<h1> Delete iRules/Data Groups </h1>';
        	}
        	?>
            
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
                <legend>iRule/Data Group Selection</legend>
                <p>
                <table id="iruleDataTable" class="form" border="1">
                    <tbody>
                        <tr>
                            <td>
                            <?php
                            if (GetParentURLParameter('go') == 'new_irule' ) {
                                echo '<label>* iRule/Data Group Name: </label>';
                                echo '<input type="text" name="ir_name" id="ir_name" required="required" />';
                            }
                            else{
                                echo '<label>* Select Type: </label>';
                                echo '<select name="chg_ir_type" id="chg_ir_type" required="required" />';
                                echo '<option value="select" selected="selected">Select...</option>';
                                echo '<option value="iRule">iRule</option>';
                                echo '<option value="Data Group"> Data Group</option>';
                            }
                            ?>
                            
                            </td>
                            <td>
                            <?php
                            if (GetParentURLParameter('go') == 'new_irule' ) {
                                echo '<label>Env.: </label>';
                                echo '<select name="ir_env" id="ir_env" required="required">';
                            
                                $iniarray = parse_ini_section_file();
                
                                foreach ($iniarray as $section => $values){
                                    $myx = (string)$section;
                                    if ($myx == "LTM_GTM_ENVIRONMENT"){
                                        foreach ($values as $key=>$value){
                                            echo "<option> " . $value ."</option>";
                                        }
                                    }
                                }
                            }
                            ?>
                            </select>
                            </td>
                        </tr>
                        <tr id='ir_dg_tr_select' >
                            <td>
                            <?php
                                if (GetParentURLParameter('go') == 'new_irule' ) {
                                    echo '<label>* Select Type: </label>';
                                    echo '<select name="ir_type" id="ir_type" required="required" />';
                                	echo '<option selected="selected">Select...</option>';
                                	echo '<option value="iRule">iRule</option>';
                                	echo '<option value="Data Group"> Data Group</option>';
                                }
                                else{
                                    echo '<label>* Select iRule/Data Group Name: </label>';
                                    echo '<select name="select_ir_dg_name" id="select_ir_dg_name" required="required" />';
                                    echo '<option value="select" selected="selected">Select...</option>';
                                }
                        	?>
                            </td>
                            <td id="ir_td_dg_type" name="ir_td_dg_type">
    
                            </td>
                        </tr>
                    </tbody>
                </table>
                </p>
                <p>
                <?php
                if (GetParentURLParameter('go') == 'del_irule' ) { echo "<!--"; } ?>
                <fieldset class="row2">
                    <legend>Configuration</legend>
                    <p>
                    	<table id="irConfTable" class="form" border="1">
                    	<thead align="left" id='ir_confTable_thead' >
                    		
                    	</thead>
                    	<tbody id="irConfTable_tbody">
                    	</tbody>
                    	</table>
                    </p>
                </fieldset>
                <?php if (GetParentURLParameter('go') == 'del_irule' ) { echo "-->"; } ?>
                </p>
            </fieldset>
            <?php
            if (GetParentURLParameter('go') == 'new_irule' ){
                echo '<input id="ir_btn_build" type="button" name="ir_btn_build" value="Deploy iRule/DG" />';
            }
            else if (GetParentURLParameter('go') == 'chg_irule' ) {
                echo '<input id="chg_ir_btn_build" type="button" name="chg_ir_btn_build" value="Change iRule/DG" />';
            }
            else if (GetParentURLParameter('go') == 'del_irule' ) {
                echo '<input id="del_ir_btn_build" type="button" name="del_ir_btn_build" value="Delete iRule/DG" />';
            }
            ?>
            <p></p>
            <fieldset class="row1">        
                <legend>Evaluation Result and Review</legend>
                <div>
                    <p id="newIr_EvalReview">
        			</p>
                </div>
            </fieldset>        
        </form>
    </body>
</html>