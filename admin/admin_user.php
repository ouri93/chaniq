<div id="admin-user">
    <!-- Admin Content - Visible if the logged-in user has admin role -->
    <?php
    if (!isadmin()){
        header('Location: index.php');
    }
    ?>
    <form class="register">
        <fieldset  id='vs_iframe_fieldset' class="row1">
		<!-- IFrame content here -->
		<legend>CHAN-IQ User Management</legend>
		<iframe src="/admin/if_usermgmt.php" width="720px" height="600" frameborder="0"></iframe>       	
        </fieldset>
    </form>
</div>