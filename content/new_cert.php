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
        <fieldset  id='cert_iframe_base_fieldset' class="row1">
		<!-- IFrame content here -->
		<!-- Default Page content - HTTP Profile -->
		<legend>Certificate and Key Import and Creation</legend>
		<!--  <iframe src="/content/if_new_cert.php" width="720px" height="600" frameborder="0"></iframe>  -->
		<iframe src="/content/if_new_cert.php" width="1105px" height="92%" frameborder="0"></iframe>
        </fieldset>
    </form>
</div>
