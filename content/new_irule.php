<div>
    <!-- Admin Content - Visible if the logged-in user has admin role -->
    <?php
    if (!isadmin()){
        header('Location: index.php');
    }
    ?>
    <form class="register">
        <h1> Create a new iRule or Data Group </h1>
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
            <legend>iRule/Data Group Selection</legend>
            <p>
            <table id="iruleDataTable" class="form" border="1">
                <tbody>
                    <tr>
                        <td>
                            <label>VS DNS Name: </label>
                            <input type="text" name="ir_vs_name" id="ir_vs_name" onfocusout="dnsValidation('ir_vs_name')" required="required" />
                        </td>
                        <td>
                            <label>VS Port Number: </label>
                            <input type="text" name="ir_vs_port" id="ir_vs_port" onfocusout="portValidation('ir_vs_port')" onkeypress='return event.charCode >= 48 && event.charCode <= 57' />
                        </td>
                        <td>
                            <label>Env.: </label>
                            <select name="ir_env" id="ir_env" required="required"> 
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
                    <tr id='ir_dg_tr_select' >
                        <td>
                            <label>Select Type: </label>
                            <select name="ir_type" id="ir_type" required="required" />
                            	<option selected="selected">Select...</option>
                            	<option>iRule</option>
                            	<option>Data Group</option>
                        </td>
                        <td id="ir_td_dg_type" name="ir_td_dg_type">

                        </td>
                    </tr>
                </tbody>
            </table>
            </p>
            <p>
            <fieldset class="row2">
                <legend>Configuration</legend>
                <p>
                	<table id="irConfTable" class="form" border="1">
                	<thead align="left" id='ir_confTable_thead' >
                		
                	</thead>
                	<tbody id="irConfTable_tbody">
					<!--  Conditional HTML code here  --> 
                	</tbody>
                	</table>
                </p>
            </fieldset>
            </p>
        </fieldset>
        <input id="ir_btn_build" type="button" name="ir_btn_build" value="Deploy iRule/DG" />
        <p></p>
        <fieldset class="row1">        
            <legend>Evaluation Result and Review</legend>
            <div>
                <p id="newIr_EvalReview">
    			</p>
            </div>
        </fieldset>        
    </form>
</div>
