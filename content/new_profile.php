<div>
    <?php
    if (!isadmin()){
        header('Location: index.php');
    }
    
    echo "<nav>";
    echo "<ul class='nav'>";
    
        echo "<li id='li_prf_svc'><a href='#'>Services</a>";
            echo "<ul id='ul_prf_selected'>";
                echo "<li><a href='#'>HTTP</a></li>";
                echo "<li><a href='#'>DNS</a></li>";
            echo "</ul>";
        echo "</li>";
        
        echo "<li id='li_prf_persist'><a href='#'>Persistence</a>";
            echo "<ul id='ul_prf_selected'>";
                echo "<li><a href='#'>Cookie</a></li>";
                echo "<li><a href='#'>Destination Address Affinity</a></li>";
                echo "<li><a href='#'>Source Address Affinity</a></li>";
                echo "<li><a href='#'>Hash</a></li>";
                echo "<li><a href='#'>SSL</a></li>";
                echo "<li><a href='#'>Universal</a></li>";
            echo "</ul>";
        echo "</li>";
        
        echo "<li id='li_prf_prto'><a href='#'>Protocol</a>";
            echo "<ul id='ul_prf_selected'>";
                echo "<li><a href='#'>Fast L4</a></li>";
                echo "<li><a href='#'>TCP</a></li>";
                echo "<li><a href='#'>UDP</a></li>";
            echo "</ul>";
        echo "</li>";
        
        echo "<li id='li_prf_ssl'><a href='#'>SSL</a>";
            echo "<ul id='ul_prf_selected'>";
                echo "<li><a href='#'>Client</a></li>";
                echo "<li><a href='#'>Server</a></li>";
            echo "</ul>";
        echo "</li>";

        echo "<li id='li_prf_other'><a href='#'>Other</a>";
            echo "<ul id='ul_prf_selected'>";
            echo "<li><a href='#'>OneConnect</a></li>";
        echo "</li>";        

    echo "</ul>";
    echo "</nav>";

       
    ?>
	<form class="register">
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
	
        <fieldset  id='prf_iframe_fieldset' class="row1">
		<!-- IFrame content here -->
		<!-- Default Page content - HTTP Profile -->
		<legend>HTTP Profile Configuration</legend>
		<iframe src="/content/if_prf_svc_http.php" width="725px" height="600" frameborder="0"></iframe>       	
        </fieldset>
    </form>
</div>

