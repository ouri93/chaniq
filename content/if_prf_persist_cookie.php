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
                 
        <script type="text/javascript" src="/js/prf_jquery.js"></script>
        <?php
        if (GetParentURLParameter('go') == 'new_profile')
            echo '<title>Create Cookie Persistence Profile</title>';
        elseif (GetParentURLParameter('go') == 'chg_profile')
            echo '<title>Change Cookie Persistence Profile</title>';
        elseif (GetParentURLParameter('go') == 'del_profile')
            echo '<title>Delete Cookie Persistence Profile</title>';
        ?>
        
    </head>
    <body style="background-color: #ffffff;">
        <form class="inner-form">
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
                <p>
                	<table id="prfConfTable" class="form" border="1">
    	            	<tbody id="prfConfTable_tbody">
    	            	<tr>
    	            		<?php
    	            		if (GetParentURLParameter('go') == 'new_profile') {
    	            		    echo "<td width='132px'><label>*Name:</label> </td><td><input type='text' id='prf_name' required='required' /></td>";
    	            		}
    	            		elseif (GetParentURLParameter('go') == 'chg_profile'){
    	            		    echo "<td width='132px'><label>*Name:</label> </td><td><select id='chg_svc_prf_name_select' required='required'> <option value='none' selected='selected'>None</option></td>";
    	            		}
    	            		elseif (GetParentURLParameter('go') == 'del_profile'){
    	            		    echo "<td width='132px'><label>*Partition:</label> </td><td><select id='prf_partition_name_select' required='required'><option value='select' selected='selected'>Select...</option><option value='common' >Common</option></td>";
    	            		    echo "<td width='132px'><label>*Name:</label> </td><td><select id='del_svc_prf_name_select' required='required'> <option value='none' selected='selected'>None</option></td>";
    	            		}
    	            		?> 
    	            	</tr>
    	            	<?php 
    	            	if (GetParentURLParameter('go') != 'del_profile'){
        	            	echo "<tr id='tr_svc_prf_type' >";
        	            	echo "<td width='132px' ><label>*Parent Profile:</label></td><td><select id='svc_prf_type_select' required='required' ><option id='noDelete' value='select' selected='selected' >Select...</option></select></td>";
        	            	echo "</tr>";
    	            	}
    	            	?>
            	        </tbody>
                    </table>
                </p>
                <p>*: Required field</p>
                <p align="right">
                    <?php
                	if (GetParentURLParameter('go') == 'new_profile') {
    	               echo '<input id="prf_btn_build" type="button" style="width:130px" name="prf_btn_build" value="Build" />';
                	}
                	elseif (GetParentURLParameter('go') == 'chg_profile'){
                	    echo '<input id="prf_btn_change" type="button" style="width:130px" name="prf_btn_change" value="Apply Changes" />';
                	}
                	elseif (GetParentURLParameter('go') == 'del_profile'){
                	    echo '<input id="prf_btn_delete" type="button" style="width:130px" name="prf_btn_delete" value="Delete" />';
                	}
    	            ?>
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