<div>
    <!-- Admin Content - Visible if the logged-in user has admin role -->
    <?php
    if (!isadmin()){
        header('Location: index.php');
    }
    ?>
    <form class="register">
        <h1> Create a new Monitor </h1>
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
            <legend>Monitor Properties</legend>
            <p>
            <table id="monDataTable" class="form" border="1">
                <tbody>
                    <tr>
                        <td>
                            <label>VS DNS Name: </label>
                            <input type="text" name="m_vs_name" id="m_vs_name" required="required" />
                        </td>
                        <td>
                            <label>VS Port Number: </label>
                            <input type="text" name="m_vs_port" id="m_vs_port" />
                        </td>
                        <td>
                            <label>Monitor Description: </label>
                            <input type="text" name="m_desc" id="m_desc" />
                        </td>
                        <td>
                            <label>Env.: </label>
                            <select name="p_env" id="p_env" required="required"> 
                            <?php
                                $iniarray = parse_ini_section_file();
                
                                foreach ($iniarray as $section => $values){
                                    $myx = (string)$section;
                                    if ($myx == "LTM_GTM_ENVIRONMENT"){
                                        foreach ($values as $key=>$value){
                                            echo "<option> " . $value ."</option>";
                                        }
                                    }
                                }
                            ?>
                        </select>
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <label>Monitor Type: </label>
                            <select name="m_type" id="m_type" required="required" />
                        </td>
                        <td>
                            <label>Parent Monitor: </label>
                            <select name="m_type_parent" id="m_type_parent" />
                        </td>

                    </tr>
                </tbody>
            </table>
            </p>
            <p>
            <fieldset class="row2">
                <legend>Monitor Configuration</legend>
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
                    <select name="p_prigroup" id="p_prigroup">
                    	<option selected="selected" value="disabled">disabled</option>
                    	<option value="Lessthan">Less than ...</option>
                    </select>
                    <label id="p_lpl_lessthan" name="p_lbl_lessthan" >Less than ...</label>
                    <input type="text" id="p_lessthan" name="p_lessthan" value="0" disabled="disabled" />
                    
                    <table id="dataTable" class="form" border="1">
                        <tbody>
                            <tr>
                                <td><input type="checkbox" required="required" name="pool_chk[]" checked="checked" /></td>                                
                                <td>
                                    <label>DNS Name: </label>                                
                                    <input type="text" name="pool_membername[]" id="pool_membername" class="pool_membername" onfocusout="dnsValidation('pool_membername')" />
                                </td>
                                <td>
                                    <label>IP: </label>
                                    <input type="text" name="pool_memberip[]" id="pool_memberip" class="pool_memberip" onfocusout="ipValidation('pool_memberip')" />
                                </td>
                                <td>
                                    <label>Port: </label>
                                    <input type="text" name="pool_memberport[]" id="pool_memberport" class="pool_memberport" onfocusout="portValidation('pool_memberport')" onkeypress='return event.charCode >= 48 && event.charCode <= 57' />
                                </td>
                                <td id="pm_td">
                					<label>Monitor: </label>
                					<select name="pm_mon[]" id="pm_mon" class="pm_mon" > 
                						<option selected="selected">Inherit</option>
            						</select>
                                </td>
                                <td>
                                	<label>Priority Group</label>
                                	<input type="text" name="pm_pg_val[]" id="pri_group_val" class="pm_pg_val" value="0" disabled="disabled" />
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
        <input id="btn_newMonBuild" type="button" name="deploy_mon" value="Deploy Monitor" />
        <p></p>
        <fieldset class="row1">        
            <legend>Evaluation Result and Review</legend>
            <div>
                <p id="newMon_EvalReview">
    			</p>
            </div>
        </fieldset>        
    </form>
</div>

