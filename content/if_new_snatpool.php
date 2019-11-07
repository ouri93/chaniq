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
                 
        <script type="text/javascript" src="/js/snatpool_jquery.js"></script>
        <?php include('../utility/utility.php'); ?>
        <?php
        if (GetParentURLParameter('go') == 'new_snatpool' ){
            echo '<title>Create a new Snatpool</title>';
        }
        else if (GetParentURLParameter('go') == 'del_snatpool' ){
            echo '<title>Delete a Snatpool</title>';
        }
        ?>
    </head>
    <body style="background-color: #ffffff;">
        <form class="inner-form">
        <?php
        if (GetParentURLParameter('go') == 'new_snatpool' ){
            echo '<h1> Create a new Snatpool </h1>';
        }
        else if (GetParentURLParameter('go') == 'del_snatpool' ){
            echo '<h1> Delete a Snatpool </h1>';
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
    	        <?php
                if (GetParentURLParameter('go') == 'new_snatpool' ){
                    echo '<legend>Snatpool Configuration</legend>';
                }
                else if (GetParentURLParameter('go') == 'del_snatpool' ){
                    echo '<legend>Delete Snatpools</legend>';
                }
                ?>
                <p>
                <table class="form" border="1">
                    <tbody id="snatDataTbody" >
                    	<?php if (GetParentURLParameter('go') != 'new_snatpool') echo '<!--'; ?>
                        <tr>
                            <td> <label>Snatpool Name: </label> </td>
                            <td> <input type="text" name="snat_name" id="snat_name" /></td>
                        </tr>
                        <tr> 
                        	<td> <label> Member List </label></td>
                        	<td> <label>&nbsp;&nbsp;* IP Address:</label> <input type='text' id='snat_ipaddr' /> <br>
                        		<p><input type='button' id='snat_add' value='Add' style="width:50px; float: left;" />&nbsp;&nbsp;&nbsp;&nbsp;<br><br></p>
                        		<select size='8' width='450px' style='width:450px' id='snat_address_list' ></select><br><br>
                        		<p><input type='button' id='snat_edit' value='Edit' style="width:80px; float: left;" />&nbsp;&nbsp;&nbsp;&nbsp;<input type='button' id='snat_del' value='Delete' style="width:80px; float: left;" />&nbsp;&nbsp;</p>
                        	</td> 
                        </tr>
                        <?php if (GetParentURLParameter('go') != 'new_snatpool') echo '-->'; ?>
                        
                        <?php if (GetParentURLParameter('go') != 'del_snatpool') echo '<!--'; ?>
                    	<tr>
                            <td>
                                <label> Select a Snatpool: </label>
                            </td>
                            <td>
                                <select id="select_snatpool_name" >
                                    <option value="select">Select...</option>
                                </select>
                            </td>
                            <td>
                                <label> Partition: </label>
                            </td>
                            <td>
                                <select id="select_del_snatpool_part" >
                                    <option value="Common">Common</option>
                                </select>
                            </td>
                        </tr>
                        <?php if (GetParentURLParameter('go') != 'del_snatpool') echo '-->'; ?>
                    </tbody>
                </table>
                </p>
            </fieldset>
            <?php
            if (GetParentURLParameter('go') == 'new_snatpool' ){
                echo '<input id="snat_build" type="button" name="snat_build" value="Deploy Snatpool" />';
            }
            else if (GetParentURLParameter('go') == 'del_snatpool' ){
                echo '<input id="del_snatpool" type="button" name="del_snatpool" value="Delete Snatpool" />';
            }
            ?>
            <p></p>
            <fieldset class="row1">        
                <legend>Evaluation Result and Review</legend>
                <div>
                    <p id="newSnat_EvalReview">
        			</p>
                </div>
            </fieldset>        
        </form>
    </body>
</html>