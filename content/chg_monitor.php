<div>
    <!-- Admin Content - Visible if the logged-in user has admin role -->
    <?php
    if(!isadmin()){
        /* echo 'username: '.$_SESSION['role']; */
        header('Location: index.php');
    }
    ?>
    <p> Change Monitor </p>
</div>

