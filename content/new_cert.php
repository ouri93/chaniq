<div>
    <!-- Admin Content - Visible if the logged-in user has admin role -->
    <?php
    if (!isadmin()){
        header('Location: index.php');
    }
    ?>
    <form class="register">
        <fieldset  id='cert_iframe_base_fieldset' class="row1">
		<!-- IFrame content here -->
		<!-- Default Page content - HTTP Profile -->
		<legend>Certificate and Key Import and Creation</legend>
		<iframe src="/content/if_new_cert.php" width="720px" height="600" frameborder="0"></iframe>       	
        </fieldset>
    </form>
</div>
