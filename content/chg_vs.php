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
    <!-- Admin Content - Visible if the logged-in user has admin role -->
    <form class="register">
        <fieldset  id='vs_iframe_fieldset' class="row1">
		<!-- IFrame content here -->
		<!-- Default Page content - HTTP Profile -->
		<legend>Virtual Server Modification</legend>
		<iframe src="/content/if_chg_vs.php" width="1105px" height="92%" frameborder="0"></iframe>       	
        </fieldset>
    </form>
</div>