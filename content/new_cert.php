<div>
    <!-- Admin Content - Visible if the logged-in user has admin role -->
    <?php
    if (!isadmin()){
        header('Location: index.php');
    }
    ?>
    <form class="register">
        <h1> Create SSL Certificates/Keys </h1>
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
            <p>
            	<div>
            		<input type="button" id="cert_create_btn" value="Create" />
            		<input type="button" id="cert_import_btn" value="Import" />
            	</div>
            </p>
        </fieldset>
        <fieldset  id='cert_iframe_fieldset' class="row1">
		<!-- IFrame content here -->       	
        </fieldset>
    </form>
</div>
