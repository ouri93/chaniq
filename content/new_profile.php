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
        
        echo "<li id='li_prf_persist'><a href='#'>Persistence</a></li>";
        
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
        <fieldset  id='prf_iframe_fieldset' class="row1">
		<!-- IFrame content here -->       	
        </fieldset>
    </form>
</div>

