<?php
if ($_SESSION['loggedin'] != true){
    file_put_contents("/var/log/chaniqphp.log", "footer.php - Un-authenticated user - Redirect to login page\n", FILE_APPEND);
    session_unset();
    session_destroy();
    header('Location: login.php');
}
?>
    <div id="footer"><p style="text-align: center;padding-top:5px">
        Since 2017 | Copyleft(<img src="./images/copyleft.png">) | Email: chaniqhelper at gmail dot com
        </p>
    </div>

    </body>
</html>
