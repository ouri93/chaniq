<div>
    <!-- Admin Content - Visible if the logged-in user has admin role -->
    <?php
    if (!isadmin()){
        header('Location: index.php');
    }
    ?>
    <form class="register">
        <fieldset  id='ir_iframe_fieldset' class="row1">
		<!-- IFrame content here -->
		<!-- Default Page content - iRule build -->
		<?php 
		if ( GetParentURLParameter('go') == 'new_irule') {
		  echo '<legend>Create iRules/Data Groups</legend>';    
		}
		else if ( GetParentURLParameter('go') == 'chg_irule') {
		    echo '<legend>Change iRules/Data Groups</legend>';
		}
		else if ( GetParentURLParameter('go') == 'del_irule') {
		    echo '<legend>Delete iRules/Data Groups</legend>';
		}
		?>
		<iframe src="/content/if_new_ir.php" width="720px" height="600" frameborder="0"></iframe>       	
        </fieldset>
    </form>
</div>
