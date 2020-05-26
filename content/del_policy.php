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
    <form class="register">
        <fieldset  id='policy_iframe_fieldset' class="row1">
		<!-- IFrame content here -->
		<!-- Default Page content - HTTP Profile -->
		<legend>Policy Configuration</legend>
	    <iframe src="/content/if_del_policy.php" width="1105px" height="92%" frameborder="0" onload="this.contentDocument.body.scrollHeight +'px';" ></iframe>
        </fieldset>
    </form>
</div>