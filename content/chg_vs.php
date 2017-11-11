<div>
    <!-- Admin Content - Visible if the logged-in user has admin role -->
    <?php
    if (!isadmin()){
        header('Location: index.php');
    }
    ?>
    <p> Change virtual server </p>
</div>


