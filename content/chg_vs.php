<div>
    <!-- Admin Content - Visible if the logged-in user has admin role -->
    <?php
    if (!isadmin()){
        header('Location: index.php');
    }
    ?>
    <form class="register">
        <fieldset  id='vs_iframe_fieldset' class="row1">
		<!-- IFrame content here -->
		<!-- Default Page content - HTTP Profile -->
		<legend>Virtual Server Modification</legend>
		<iframe src="/content/if_chg_vs.php" width="720px" height="600" frameborder="0"></iframe>       	
        </fieldset>
    </form>
</div>