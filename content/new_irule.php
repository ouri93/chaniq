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
include_once 'utility/utility.php';
?>
<div>
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
		<iframe src="/content/if_new_ir.php" width="1105px" height="92%" frameborder="0"></iframe>       	
        </fieldset>
    </form>
</div>
