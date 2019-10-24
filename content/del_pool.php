<div>
    <!-- Admin Content - Visible if the logged-in user has admin role -->
    <?php
    if (!isadmin()){
        header('Location: index.php');
    }
    ?>
    <form class="register">
        <fieldset  id='pool_iframe_fieldset' class="row1">
		<!-- IFrame content here -->
		<!-- iFrame for Pool Build -->
		<legend>Delete Pools</legend>
		<iframe src="/content/if_new_pool.php" width="720px" height="600" frameborder="0"></iframe>
        </fieldset>
    </form>
</div>

