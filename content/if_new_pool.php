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
                 
        <script type="text/javascript" src="/js/pool_jquery.js"></script>
        <?php include('../utility/utility.php'); ?>
        <?php
            if (GetParentURLParameter('go') == 'new_pool')
                echo '<title>Create a new Pool</title>';
            elseif (GetParentURLParameter('go') == 'chg_pool')
                echo '<title>Change Pool configuration</title>';
            elseif (GetParentURLParameter('go') == 'del_pool')
                echo '<title>Delete Pools</title>';
        ?>
        
    </head>
    <body style="background-color: #ffffff;">
        <form class="inner-form">
            <?php
            if (GetParentURLParameter('go') == 'new_pool') {
                echo "<h1> Create a new Pool </h1>";
            }
            elseif (GetParentURLParameter('go') == 'chg_pool') {
                echo "<h1> Change Pool Configuration</h1>";
            }
            elseif (GetParentURLParameter('go') == 'del_pool') {
                echo "<h1> Delete Pools</h1>";
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
                    if (GetParentURLParameter('go') != 'del_pool') {
                        echo '<legend>Pool Properties</legend>';
                    }
                ?>
                <p>
                <table id="poolDataTable" class="form" border="1">
                    <tbody>
                        <tr>
                            <td>
                                <?php
                                if (GetParentURLParameter('go') == 'new_pool') {
                                    echo "<label>*Pool Name: </label><input type='text' name='p_vs_name' id='p_vs_name' required='required' />";
                                }
                                elseif (GetParentURLParameter('go') == 'chg_pool') {
                                    echo "<label>*Pool Name: </label><select name='chg_p_name_select' id='chg_p_name_select' required='required'><option value='none' selected='selected'>None</option></select>";
                                }
                                elseif (GetParentURLParameter('go') == 'del_pool') {
                                    echo "<label>*Partition:</label> </td><td><select id='partition_name_select' required='required'><option value='select' selected='selected'>Select...</option><option value='common' >Common</option>";
                                }
                                ?>                            
                            </td>
                                <?php
                                    if (GetParentURLParameter('go') == 'new_pool'){
                                     echo '<td> <label>VS Port: </label> <input type="text" name="p_vs_port" id="p_vs_port" onfocusout="portValidation("p_vs_port")" onkeypress="return event.charCode >= 48 && event.charCode <= 57" /> </td>';
                                    }
                                ?>
                            <td>
                            <?php
                            if (GetParentURLParameter('go') != 'del_pool'){
                                echo '<label>Pool Monitor: </label>';
                                echo '<select name="p_mon" id="p_mon"><option value="none">None</option></select>';
                            }
                            else {
                                echo "<label>*Pool Name: </label><select name='del_p_name_select' id='del_p_name_select' required='required'><option value='none' selected='selected'>None</option></select>";
                            }
                            ?>
                                
                            </td>
                            <?php 
                                if (GetParentURLParameter('go') == 'new_pool'){
                                    echo '<td> <label>Env.: </label> <select name="p_env" id="p_env" required="required">';
                                }
                            ?>
                                <?php
                                    if (GetParentURLParameter('go') == 'new_pool'){
                                        $iniarray = parse_ini_section_file();
                                        echo "<option value='select' selected='selected' >Select...</option>";
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
                            <?php
                                if (GetParentURLParameter('go') == 'new_pool'){
                                    echo '</select> </td>';
                                }
                            ?>
                        </tr>
                    </tbody>
                </table>
                </p>
                <?php if (GetParentURLParameter('go') != 'del_pool'){ ?>
                <p>
                <fieldset class="row2">
                    <legend>Pool Resources</legend>
                    <p>
                        <label>LB Method</label>
                        <select name="p_lbmethod" id="p_lbmethod" onchange="optEnDis('p_lbmethod')" required="required">
                        	<option value="none" selected="selected">none</option>
                            <option value="round-robin" >round-robin</option>
                            <option value="least-connections-member" selected="selected">least-connections-member</option>
                            <option value="least-connections-node" >least-connections-node</option>
                            <option value="ratio-member" >ratio-member</option>
                            <option value="ratio-node" >ratio-node</option>
                        </select>
                        <label>Priority Group</label>
                        <select name="p_prigroup" id="p_prigroup">
                        	<option selected="selected" value="disabled">disabled</option>
                        	<option value="Lessthan">Less than ...</option>
                        </select>
                        <label id="p_lpl_lessthan" name="p_lbl_lessthan" >Less than ...</label>
                        <input type="text" id="p_lessthan" name="p_lessthan" value="0" disabled="disabled" />
                        
                        <table id="dataTable" class="form" border="1">
                            <tbody>
                            <tr>
                            	<th id='pm_hdr_chkbox' />
                            	<th id='pm_hdr_name' > DNS Name: </th>
                            	<th id='pm_hdr_ip' > IP: </th>
                            	<th id='pm_hdr_port' > Port: </th>
                            	<th id='pm_hdr_ratio' > Ratio: </th>
                            	<th id='pm_hdr_mon' > Monitor: </th>
                            	<th id='pm_hdr_prigroup' > Priority Group: </th>
                            </tr>
                            <tr>
                                <td><input type="checkbox" required="required" name="pool_chk[]" checked="checked" /></td>                                
                                <td>
                                <?php
                                    if (GetParentURLParameter('go') == 'chg_pool'){
                                        echo '<input type="text" name="pool_membername[]" id="pool_membername" class="pool_membername" disabled />';
                                    }
                                    else {
                                        $pm_name_id = 'pool_membername';
                                        echo '<input type="text" name="pool_membername[]" id="pool_membername" class="pool_membername" onfocusout="dnsValidation($pm_name_id)" />';    
                                    }
                                ?>
                                </td>
                                <td>
                                <?php
                                    if (GetParentURLParameter('go') == 'chg_pool'){
                                        echo '<input type="text" name="pool_memberip[]" id="pool_memberip" class="pool_memberip" disabled />'; 
                                    }
                                    else {
                                        $pm_ip_id = 'pool_memberip';
                                        echo '<input type="text" name="pool_memberip[]" id="pool_memberip" class="pool_memberip" onfocusout="ipValidation($pm_ip_id)" />';    
                                    }
                                ?>                                
                                </td>
                                <td>
                                <?php
                                    if (GetParentURLParameter('go') == 'chg_pool'){
                                        echo '<input type="text" name="pool_memberport[]" id="pool_memberport" class="pool_memberport" disabled />';
                                    }
                                    else {
                                        $pm_port_id = 'pool_memberport';
                                        echo '<input type="text" name="pool_memberport[]" id="pool_memberport" class="pool_memberport" onfocusout="portValidation($pm_port_id)" onkeypress="return event.charCode >= 48 && event.charCode <= 57" />';    
                                    }
                                ?>                                 
                                </td>
                                <td>
                                	<input type="text" name="pool_memberratio[]" id="pool_memberratio" class="pool_memberratio" value="1" />
                                </td>
                                <td id="pm_td">
                					<select name="pm_mon[]" id="pm_mon" class="pm_mon" > 
                						<option selected="selected" value="inherit">Inherit</option>
            						</select>
                                </td>
                                <td>
                                	<input type="text" name="pm_pg_val[]" id="pri_group_val" class="pm_pg_val" value="0" disabled="disabled" />
                                </td>
							</tr>
                            </tbody>
                        </table>
                    </p>
                    <p></p>
                    <input type="button" value="Remove Member" onClick="deleteRow('dataTable')"  /> 

            		<?php
            		if (GetParentURLParameter('go') == 'new_pool')
                            echo '<input id="add_new_pm" type="button" value="Add Member" />';
                    elseif (GetParentURLParameter('go') == 'chg_pool')
                        echo '<input id="add_editable_new_pm" type="button" value="Add Member" />';
                    ?>

                </fieldset>
                </p>
                <?php } ?>
            </fieldset>
            <?php
                if (GetParentURLParameter('go') == 'new_pool') {
                    echo '<input id="btn_newPoolBuild" type="button" name="deploy_pool" value="Deploy Pool" />';
                }
                elseif (GetParentURLParameter('go') == 'chg_pool') {
                    echo '<input id="btn_chgPoolConfig" type="button" name="change_pool" value="Apply Changes" />';
                }
                elseif (GetParentURLParameter('go') == 'del_pool') {
                    echo '<input id="btn_delPool" type="button" name="delete_pool" value="Delete Pool" />';
                }
            ?>
            <p></p>
            <fieldset class="row1">        
                <legend>Evaluation Result and Review</legend>
                <div>
                    <p id="newPool_EvalReview">
        			</p>
                </div>
            </fieldset>        
        </form>
    </body>
</html>