<?php
if ($_SESSION['loggedin'] != true){
    session_unset();
    session_destroy();
    header('Location: ../login.php');
}
//Admin Content - Visible if the logged-in user has admin role
if ($_SESSION['role'] == 'guest'){
    header('Location: contentbase.php');
}
?>
<div>

    <?php
    echo "<nav>";
    echo "<ul class='nav'>";
    
        echo "<li id='li_prf_svc'><a href='#'>Services</a>";
            echo "<ul id='ul_prf_selected'>";
                echo "<li value='HTTP'><a href='#'>HTTP</a></li>";
                echo "<li value='DNS'><a href='#'>DNS</a></li>";
            echo "</ul>";
        echo "</li>";
        
        echo "<li id='li_prf_persist'><a href='#'>Persistence</a>";
            echo "<ul id='ul_prf_selected'>";
                echo "<li value='Cookie'><a href='#'>Cookie</a></li>";
                echo "<li value='DestAddrAffinity'><a href='#'>Destination Address Affinity</a></li>";
                echo "<li value='SrcAddrAffinity'><a href='#'>Source Address Affinity</a></li>";
                echo "<li value='Hash'><a href='#'>Hash</a></li>";
                echo "<li value='SSL'><a href='#'>SSL</a></li>";
                echo "<li value='Universal'><a href='#'>Universal</a></li>";
            echo "</ul>";
        echo "</li>";
        
        echo "<li id='li_prf_prto'><a href='#'>Protocol</a>";
            echo "<ul id='ul_prf_selected'>";
                echo "<li value='FastL4'><a href='#'>Fast L4</a></li>";
                echo "<li value='TCP'><a href='#'>TCP</a></li>";
                echo "<li value='UDP'><a href='#'>UDP</a></li>";
            echo "</ul>";
        echo "</li>";
        
        echo "<li id='li_prf_ssl'><a href='#'>SSL</a>";
            echo "<ul id='ul_prf_selected'>";
                echo "<li value='CLIENTSSL'><a href='#'>Client</a></li>";
                echo "<li value='SERVERSSL'><a href='#'>Server</a></li>";
            echo "</ul>";
        echo "</li>";

        echo "<li id='li_prf_other'><a href='#'>Other</a>";
            echo "<ul id='ul_prf_selected'>";
            echo "<li value='OneConnect'><a href='#'>OneConnect</a></li>";
            echo "<li value='Stream'><a href='#'>Stream</a></li>";
        echo "</li>";        

    echo "</ul>";
    echo "</nav>";

       
    ?>
	<form class="register">
        <fieldset  id='prf_iframe_fieldset' class="row1">
        <!-- 
        Set Default Profile values - HTTP Reverse proxy type Profile
        All other profile build events are initiated through Top Profile List menu
        Handler: On_click event of 'ul_prf_selected li' 
        Jquery file: /js/chaniq_jquery.js  
        -->
        <input type='hidden' id='selectedPrfProxyType' value='reverse' />
        <input type='hidden' id='selectedPrfType' value='HTTP' />
		<!-- IFrame content here -->
		<!-- Default Page content - HTTP Profile -->
		<legend>HTTP Profile Configuration</legend>
		<iframe src="/content/if_prf_svc_http.php" width="1105px" height="87%" frameborder="0"></iframe>       	
        </fieldset>
    </form>
</div>

