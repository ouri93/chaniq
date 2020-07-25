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
                 
        <script type="text/javascript" src="/js/mon_jquery.js"></script>
        <?php
        if (GetParentURLParameter('go') == 'new_monitor' ){
            echo '<title>Create a Health Monitor</title>';
        }
        else if (GetParentURLParameter('go') == 'chg_monitor' ){
            echo '<title>Modify a Health Monitor</title>';
        }
        else if (GetParentURLParameter('go') == 'del_monitor' ){
            echo '<title>Delete a Health Monitor</title>';
        }
        ?>
    </head>
    <body style="background-color: #ffffff;">
        <form class="inner-form">
        	<?php
        	if (GetParentURLParameter('go') == 'new_monitor' )
        	    echo '<title>Create new Health Monitors</title>';
    	    else if (GetParentURLParameter('go') == 'chg_monitor' )
        	    echo '<title>Modify Health Monitors</title>';
    	    else if (GetParentURLParameter('go') == 'del_monitor' )
        	    echo '<title>Delete Health Monitors</title>';
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
                <legend>Monitor Properties</legend>
                <p>
                <table id="monDataTable" class="form" border="1">
                    <tbody>
                        <tr>
                            <td>
                                <?php
                                if (GetParentURLParameter('go') == 'new_monitor' ){
        	                        echo '<label>Monitor Name: </label>';
                                    echo '<input type="text" name="m_name" id="m_name" required="required" />';
                                }
                                else{
                                    echo '<label>Monitor Type: </label>';
                                    echo '<select name="chg_m_type" id="chg_m_type" required="required" />';
                                    echo '<option selected="selected">Select...</option>';
                                    echo '<option>HTTP</option>';
                                    echo '<option>HTTPS</option>';
                                    echo '<option>TCP</option>';
                                    echo '<option>TCP Half Open</option>';
                                    echo '<option>UDP</option>';
                                }
                                ?>
                            </td>
                            <td>
                                <?php
                                    if (GetParentURLParameter('go') == 'new_monitor' ){
                                        echo '<label>Monitor Description: </label>';
                                        echo '<input type="text" name="m_desc" id="m_desc" />';
                                    }
                                    else{
                                        echo '<label>Monitor Name: </label>';
                                        echo '<select name="select_mon_name" id="select_mon_name" required="required" />';
                                        echo '<option value="select" selected="selected">Select...</option>';
                                    }
                                ?>
                                
                            </td>
                            <td>
                                <?php
                                if (GetParentURLParameter('go') == 'new_monitor' ){
                                    echo '<label>Env.: </label>';
                                    echo '<select name="p_env" id="p_env" required="required">';

                                    $iniarray = parse_ini_section_file();
                    
                                    foreach ($iniarray as $section => $values){
                                        $myx = (string)$section;
                                        if ($myx == "LTM_GTM_ENVIRONMENT"){
                                            foreach ($values as $key=>$value){
                                                echo "<option> " . $value ."</option>";
                                            }
                                        }
                                    }
                                    echo '</select>';
                                }
                                ?>
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <?php
                                if (GetParentURLParameter('go') == 'new_monitor' ){
                                    echo '<label>Monitor Type: </label>';
                                    echo '<select name="m_type" id="m_type" required="required" />';
                                    echo '<option selected="selected">Select...</option>';
                                    echo '<option>HTTP</option>';
                                    echo '<option>HTTPS</option>';
                                    echo '<option>TCP</option>';
                                    echo '<option>TCP Half Open</option>';
                                    echo '<option>UDP</option>';
                                }
                                else {
                                    echo '<label>Monitor Description: </label>';
                                    echo '<input type="text" name="m_desc" id="m_desc" />';
                                }
                                ?>
                            </td>
                            <td>
                            	<label>Parent Monitor: </label>
                                <?php
                                    if (GetParentURLParameter('go') == 'new_monitor' ){
                                        echo '<select name="m_type_parent" id="m_type_parent" required="required" />';
                                    }
                                    else{
                                        echo '<select name="chg_m_type_parent" id="chg_m_type_parent" required="required" disabled style="background-color: #E6E3E3;" />';
                                    }
                                ?>
                            </td>
                        </tr>
                    </tbody>
                </table>
                </p>
                <?php if (GetParentURLParameter('go') == 'del_monitor') echo '<!--'; ?>
                <p>
                <fieldset class="row2">
                    <legend>Monitor Configuration</legend>
                    <p>
                    	<table id="monConfTable" class="form" border="1">
                    		<tbody id="monConfTable_tbody">
                    		</tbody>
                    	</table>
                    </p>
                </fieldset>
                </p>
                <?php if (GetParentURLParameter('go') == 'del_monitor') echo '-->'; ?>
            </fieldset>
            <?php
                if (GetParentURLParameter('go') == 'new_monitor' )
                    echo '<input id="btn_newMonBuild" type="button" name="deploy_mon" value="Deploy Monitor" />';       
                else if (GetParentURLParameter('go') == 'chg_monitor' )
                    echo '<input id="btn_chgMonBuild" type="button" name="change_mon" value="Modify Monitor" />';
                else if (GetParentURLParameter('go') == 'del_monitor' )
                    echo '<input id="btn_delMonBuild" type="button" name="delete_mon" value="Delete Monitor" />';
            ?>
            
            <p></p>
            <fieldset class="row1">        
                <legend>Evaluation Result and Review</legend>
                <div>
                    <p id="newMon_EvalReview">
        			</p>
                </div>
            </fieldset>        
        </form>
    </body>
</html>