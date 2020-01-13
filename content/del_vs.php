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
        <fieldset  id='vs_iframe_fieldset' class="row1">
		<!-- IFrame content here -->
		<!-- Default Page content - HTTP Profile -->
		<legend>Virtual Server Deletion</legend>
		<iframe src="/content/if_del_vs.php" width="720px" height="600" frameborder="0"></iframe>       	
        </fieldset>
    </form>
</div>