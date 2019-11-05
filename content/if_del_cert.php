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
                 
        <script type="text/javascript" src="/js/cert_jquery.js"></script>
        <?php include('../utility/utility.php'); ?>
        <title>Delete Certs and Keys</title>
    </head>
    <body style="background-color: #ffffff;">
        <form class="inner-form">
        	<h1> Delete Certs and Keys </h1>
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
                <legend>Certs and Keys</legend>
                <p>
                    <table id="dataTable" class="form" border="1">
                        <tbody>
                        <tr>
                        	<th id='certkey_chkbox' />
                        	<th id='certkey_name' > Name: </th>
                        	<th id='certkey_CN' > Common Name: </th>
                        	<th id='certkey_exp' > Expiration: </th>
                        	<th id='certkey_part' > Partition: </th>
                        </tr>
                        <tr>
                            <td><input type="checkbox" required="required" name="certkey_chkbox[]" /></td>                                
                            <td><input type="text" name="certkey_name[]" id="certkey_name" class="certkey_name" disabled/></td>
                            <td><input type="text" name="certkey_CN[]" id="certkey_CN" class="certkey_CN" disabled /></td>
                            <td><input type="text" name="certkey_exp[]" id="certkey_exp" class="certkey_exp" disabled /></td>
                            <td><input type="text" name="certkey_part[]" id="certkey_part" class="certkey_part" disabled /></td>
						</tr>
                        </tbody>
                    </table>
                </p>
            </fieldset>
            </p>
            </fieldset>
            <input id="btn_delCertkey" type="button" name="delete_certkey" value="Delete Cert/Key" />
            <p></p>
            <fieldset class="row1">        
                <legend>Evaluation Result and Review</legend>
                <div>
                    <p id="delCert_EvalReview">
        			</p>
                </div>
            </fieldset>        
        </form>
    </body>
</html>