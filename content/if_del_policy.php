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
                 
        <script type="text/javascript" src="/js/policy_jquery.js"></script>
        <title>Delete Draft/Published Policies</title>
    </head>
    <body style="background-color: #ffffff;">
        <form class="inner-form">
        	<h1> Delete Draft/Published Policies </h1>
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
            <fieldset class="row2">
                <legend>Draft Policies</legend>
                <p>
                    <table id="dftDataTable" class="form" border="1">
                        <tbody>
                        <tr>
                        	<th id='delpoldft_chkbox' />
                        	<th id='delpoldft_name' > Name: </th>
                        	<th id='delpoldft_part' > Partition: </th>
                        </tr>
                        <tr>
                            <td><input type="checkbox" required="required" name="delpoldft_chkbox[]" /></td>                                
                            <td><input type="text" name="delpoldft_name[]" id="delpoldft_name" class="delpoldft_name" disabled/></td>
                            <td><input type="text" name="delpoldft_part[]" id="delpoldft_part" class="delpoldft_part" disabled /></td>
						</tr>
                        </tbody>
                    </table>
                </p>
            </fieldset>
            <input id="btn_delpoldft" type="button" name="delete_delpoldft" value="Delete Policies" />
            <p></p>
            <fieldset class="row2">
                <legend>Published Policies</legend>
                <p>
                    <table id="pubDataTable" class="form" border="1">
                        <tbody>
                        <tr>
                        	<th id='delpolpub_chkbox' />
                        	<th id='delpolpub_name' > Name: </th>
                        	<th id='delpolpub_part' > Partition: </th>
                        </tr>
                        <tr>
                            <td><input type="checkbox" required="required" name="delpolpub_chkbox[]" /></td>                                
                            <td><input type="text" name="delpolpub_name[]" id="delpolpub_name" class="delpolpub_name" disabled/></td>
                            <td><input type="text" name="delpolpub_part[]" id="delpolpub_part" class="delpolpub_part" disabled /></td>
						</tr>
                        </tbody>
                    </table>
                </p>
            </fieldset>
            <input id="btn_delpolpub" type="button" name="delete_delpolpub" value="Delete Policies" />
            <p></p>
            <fieldset class="row1">        
                <legend>Evaluation Result and Review</legend>
                <div>
                    <p id="delPol_EvalReview">
        			</p>
                </div>
            </fieldset>        
        </form>
    </body>
</html>