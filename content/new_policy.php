<div>
    <!-- Admin Content - Visible if the logged-in user has admin role -->
    <?php
    if (!isadmin()){
        header('Location: index.php');
    }
    ?>
    <form class="register">
        <fieldset  id='policy_iframe_fieldset' class="row1">
		<!-- IFrame content here -->
		<!-- Default Page content - HTTP Profile -->
		<legend>Policy Configuration</legend>
		<iframe src="/content/if_new_policy.php" width="720px" height="600px" frameborder="0" onload="this.style.height=this.contentDocument.body.scrollHeight +'px';"></iframe>       	
        </fieldset>
    </form>
</div>