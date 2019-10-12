<?php
session_start();
if(isset($_POST['btnLogin'])){
    require 'db/connect.php';
    $username = $_POST['username'];
    $password = $_POST['password'];
    $result = mysqli_query($con, 'select un, pw, role from users where un="'.$username.'" and pw="'.$password.'"');
    // Store the returned DB row object to $role
    $role = mysqli_fetch_object($result);
    if(mysqli_num_rows($result)==1){
        $_SESSION['username'] = $username;
        $_SESSION['role'] = $role->role;
        header('Location: index.php');
    }
    else{
        session_destroy();
        echo "Invalid username or passowrd";
    }
}
if(isset($_GET['logout'])){
    $_SESSION = array();
    session_unregister('username');
}
?>
<html>
    <head>
        <meta charset="UTF-8">
        <link rel="stylesheet" href="./css/style.css" type="text/css" media="screen" />        
        <title>CHAN-IQ Login</title>
    </head>
    <body>
        <div id="loginbody" style="text-align: center">
            <img src="./images/chaniq_login_image.png" style="padding: 40px;">
            <div id="loginpass">
                <form method="post">
                    <table style="align-self: center">
                        <tr>
                            <td>Username: </td>
                            <td><input type="text" name="username"></td>
                        </tr>
                        <tr>
                            <td>Password: </td>
                            <td><input type="password" name="password"></td>
                        </tr>
                        <tr>
                            <td>&nbsp;</td>
                            <td><input type="submit" name="btnLogin" value="Login"></td>
                        </tr>
                    </table>
                </form>
            </div>
        </div>
    </body>
</html>
