<?php
if ($_SESSION['loggedin'] != true){
    session_unset();
    session_destroy();
    header('Location: ../login.php');
}
if ($_SESSION['role'] == 'guest'){
    header('Location: contentbase.php');
}

?>
<div>
    <!-- Admin Content - Visible if the logged-in user has admin role -->
    <form class="register">
        <fieldset  id='mon_iframe_fieldset' class="row1">
		<!-- IFrame content here -->
		<!-- iFrame for Monitor Build -->
		<legend>Monitor Configuration</legend>
		<iframe src="/content/if_new_mon.php" width="720px" height="600" frameborder="0"></iframe>       	
        </fieldset>
    </form>
</div>

