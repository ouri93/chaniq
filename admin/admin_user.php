<div id="admin-user">
    <!-- Admin Content - Visible if the logged-in user has admin role -->
    <?php
    if (!isadmin()){
        header('Location: index.php');
    }
    ?>
    <br>
    <p><b>User Administration</b></p><br><br>
    <p> CHAN-IQ Local users are managed through PHP MyAdmin SQL Database System.<br></p>
    <p> To add, delete, or modify local user, please log in PHP MyAdmin page.<br></p>
    <br>
</div>

