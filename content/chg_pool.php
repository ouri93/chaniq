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
    <form class="register">
        <fieldset  id='pool_iframe_fieldset' class="row1">
		<!-- IFrame content here -->
		<!-- iFrame for Pool Build -->
		<legend>Change Pool Configuration</legend>
		<iframe src="/content/if_new_pool.php" width="1105px" height="92%" frameborder="0"></iframe>
        </fieldset>
    </form>
</div>

