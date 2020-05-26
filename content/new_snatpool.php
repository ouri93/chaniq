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
        <fieldset  id='snatpool_iframe_fieldset' class="row1">
		<!-- IFrame content here -->
		<!-- Default Page content - HTTP Profile -->
		<?php 
		if ( GetParentURLParameter('go') == 'new_snatpool'){
		  echo '<legend>Snatpool Configuration</legend>';
		}
		else if ( GetParentURLParameter('go') == 'del_snatpool'){
		    echo '<legend>Delete Snatpool</legend>';
		}
		?>
		<iframe src="/content/if_new_snatpool.php" width="1105px" height="92%" frameborder="0"></iframe>       	
        </fieldset>
    </form>
</div>