<div>
    <!-- Admin Content - Visible if the logged-in user has admin role -->
    <?php
    if (!isadmin()){
        header('Location: index.php');
    }
    ?>
    <form action="index.php?go=deploy_pool_simulate" class="register" method="POST">
        <h1> Create a new Pool </h1>
        <fieldset class="row1">
            <legend>Select a target LTM</legend>
            <?php
                // Load all BIG-IP devices name and IP
                $allBigips = load_all_bigips();
                $allBigipNames = array();

                $i=0;
                foreach($allBigips as $name => $ip){
                    $allBigipNames[$i] = $name . ":" . $ip;
                    $i += 1;
                }
                asort($allBigipNames);
            ?>
            <p>
                <div class="ltmDeviceList">
                	<?php 
                	dynamic_select($allBigipNames, "ltmSelBox", "", "");
                	?>
                </div>
            </p>
        </fieldset>
        <fieldset class="row1">
            <legend>Pool Properties</legend>
            <p>
                <label>Name: </label>
                <input type="text" name="p_name" id="p_name" required="required" />
                <label>Description: </label>
                <input type="text" name="p_desc" id="p_desc" />
                <label>Pool Monitor: </label>
                <select name="p_mon" id="p_mon" > </select>
            </p>
            <p>
            <fieldset class="row2">
                <legend>Pool Resources</legend>
                <p>
                    <label>LB Method</label>
                    <select name="p_lbmethod" id="p_lbmethod" onchange="optEnDis('p_lbmethod')" required="required">
                    	<option selected="selected">none</option>
                        <option>round-robin</option>
                        <option selected="selected">least-connections-member</option>
                        <option>least-connections-node</option>
                        <option>ratio-member</option>
                        <option >ratio-node</option>
                    </select>
                    <label>Priority Group</label>
                    <select name="p_prigroup" id="p_prigroup" onchange="p_pglessthan('p_prigroup')">
                    	<option selected="selected" value="disabled">disabled</option>
                    	<option value="Lessthan">Less than ...</option>
                    </select>
                    <label id="p_lpl_lessthan" name="p_lbl_lessthan" >Less than ...</label>
                    <input type="text" id="p_lessthan" name="p_lessthan" disabled="disabled" />
                    
                    <table id="dataTable" class="form" border="1">
                        <tbody>
                            <tr>
                                <td><input type="checkbox" required="required" name="pool_chk[]" checked="checked" /></td>                                
                                <td>
                                    <label>DNS Name: </label>                                
                                    <input type="text" name="pool_membername[]" id="pool_membername" onfocusout="dnsValidation('pool_membername')" />
                                </td>
                                <td>
                                    <label>IP: </label>
                                    <input type="text" name="pool_memberip[]" id="pool_memberip" onfocusout="ipValidation('pool_memberip')" />
                                </td>
                                <td>
                                    <label>Port: </label>
                                    <input type="text" name="pool_memberport[]" id="pool_memberport" onfocusout="portValidation('pool_memberport')" onkeypress='return event.charCode >= 48 && event.charCode <= 57' />
                                </td>
                                <td>
                					<label>Monitor: </label>
                					<select name="pm_mon" id="pm_mon" > 
                						<option selected="selected">Inherit</option>
            						</select>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </p>
                <p></p>
                <input type="button" value="Remove Member" onClick="deleteRow('dataTable')"  /> 
                <input type="button" value="Add Member" onClick="addRow('dataTable')" /> 
            </fieldset>
            </p>
        </fieldset>
        <input type="submit" name="deploy_pool_simulate" value="Simulate & Review" />        
    </form>
</div>
