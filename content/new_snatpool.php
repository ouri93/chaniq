<div>
    <!-- Admin Content - Visible if the logged-in user has admin role -->
    <?php
    if (!isadmin()){
        header('Location: index.php');
    }
    ?>
    <form class="register">
        <fieldset  id='snatpool_iframe_fieldset' class="row1">
		<!-- IFrame content here -->
		<!-- Default Page content - HTTP Profile -->
		<legend>Snatpool Configuration</legend>
		<iframe src="/content/if_new_snatpool.php" width="720px" height="600" frameborder="0"></iframe>       	
        </fieldset>
    </form>
</div>