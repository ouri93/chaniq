<div>
    <!-- Admin Content - Visible if the logged-in user has admin role -->
    <?php
    if (!isadmin()){
        header('Location: index.php');
    }
    ?>
    <form action="index.php?go=new_pool" class="register" method="POST">
        <h1> Create a new Pool </h1>
        <fieldset class="row1">
            <legend>Select Target LTMs</legend>
            <?php
                // Load all BIG-IP devices name and IP
                $allBigips = load_all_bigips();
                $allBigipNames = array();

                $i=0;
                foreach($allBigips as $name => $ip){
                    $allBigipNames[$i] = $name;
                    $i += 1;
                }
            ?>
            <p>
                <div class="subject-info-box-1">
                	<?php 
                	dynamic_multi_select($allBigipNames, "lstBox1", "Availabe", "", "lstBox1")
                	?>
                	<!-- 
                	<label> Avalable</label>
                	<select multiple="multiple" id="lstBox1" class="lstBox1">
                		<option value="toc-f5c1ext1-web.net.umb.com">toc-f5c1ext1-web.net.umb.com</option>
                		<option value="toc-f5c1ext3-secweb.net.umb.com">toc-f5c1ext1-web.net.umb.com</option>
                		<option value="toc-f5c1ext5-vweb.net.umb.com">toc-f5c1ext1-web.net.umb.com</option>
                	</select>
                	 -->
                </div>
                <div class="subject-info-arrows text-center">
                	<br><br>
                	<input type="button" id="btnRight" value=">"  /><br /><br/> 
                	<input type="button" id="btnLeft" value="<" />
                </div>
                <div class="subject-info-box-2">
                	<label>Selected</label>
                	<select multiple="multiple" id="lstBox2" class="lstBox2">
                	</select>
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
                <input type="text" name="p_mon" id="p_mon"  />
            </p>
            <p>
            <fieldset class="row2">
                <legend>Pool Resources</legend>
                <label>LB Method</label>
                <select name="p_lbmethod" id="p_lbmethod" onchange="optEnDis('p_lbmethod')" required="required">
                	<option selected="selected">none</option>
                    <option>round-robin</option>
                    <option>least-connections-member</option>
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
                                <input type="text" name="pool_membermon[]" id="pool_membermon" onfocusout="portValidation('pool_membermon')" onkeypress='return event.charCode >= 48 && event.charCode <= 57' />
                            </td>
                        </tr>
                    </tbody>
                </table>
                <p></p>
                <input type="button" value="Remove Member" onClick="deleteRow('dataTable')"  /> 
                <input type="button" value="Add Member" onClick="addRow('dataTable')" /> 
            </fieldset>
            </p>
        </fieldset>
        <input type="submit" name="new_vs_findltm" value="Find LTM" />        
    </form>
</div>
