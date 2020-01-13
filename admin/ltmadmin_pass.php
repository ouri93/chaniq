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
<div id="ltmadmin_pass">
    <form class="register">
        <fieldset  id='vs_iframe_fieldset' class="row1">
		<!-- IFrame content here -->
		<legend>LTM/GTM Admin password Management</legend>
		<iframe src="/admin/if_adminpw.php" width="720px" height="600" frameborder="0"></iframe>       	
        </fieldset>
    </form>
</div>
