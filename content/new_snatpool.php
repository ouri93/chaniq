<div>
    <!-- Admin Content - Visible if the logged-in user has admin role -->
    <?php
    if (!isadmin()){
        header('Location: index.php');
    }
    ?>
    <form class="register">
        <h1> Create a new Snatpool </h1>
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
            <legend>Snatpool Configuration</legend>
            <p>
            <table id="snatDataTable" class="form" border="1">
                <tbody>
                    <tr>
                        <td> <label>Snatpool Name: </label> </td>
                        <td> <input type="text" name="snat_name" id="snat_name" /></td>
                    </tr>
                    <tr> 
                    	<td> <label> Member List </label></td>
                    	<td> <label>&nbsp;&nbsp;* IP Address:</label> <input type='text' id='snat_ipaddr' /> <br>
                    		<p><input type='button' id='snat_add' value='Add' style="width:50px; float: left;" />&nbsp;&nbsp;&nbsp;&nbsp;<br><br></p>
                    		<select size='8' width='450px' style='width:450px' id='snat_address_list' ></select><br><br>
                    		<p><input type='button' id='snat_del' value='Delete' style="width:80px; float: left;" />&nbsp;&nbsp;<input type='button' id='snat_edit' value='Edit' style="width:80px; float: left;" />&nbsp;&nbsp;&nbsp;&nbsp;</p>
                    	</td> 
                    </tr>
                    <!-- 
                    <tr>
                    	<td><input type='button' id='snat_add' value='Add' />&nbsp;&nbsp;&nbsp;&nbsp;</td>
                    </tr>
					<tr> 
						<td> <select size='8' width='680px' style='width:680px' id='snat_address_list' ></select> </td> 
					</tr>
					<tr>
						<td><input type='button' id='snat_del' value='Delete' />&nbsp;&nbsp;<input type='button' id='snat_edit' value='Edit' />&nbsp;&nbsp;&nbsp;&nbsp;</td> 
                    </tr>
                     -->
                </tbody>
            </table>
            </p>
        </fieldset>
        <input id="snat_build" type="button" name="snat_build" value="Deploy Snatpool" />
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
