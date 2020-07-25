<?php
require_once(__DIR__ . '/utility/chaniqLogger.php');

function check_login($username, $password, $logger){
    if (!($username && $password))
        return 0;
    // Call Python to check Username and password

    $cmd = '/usr/bin/python2 /var/www/chaniq/py/check_login.py '. escapeshellarg($username) .' '. escapeshellarg($password); 
    #file_put_contents(__DIR__ . "/log/chaniq-php.log", "Python CMD string: " . $cmd . "\n", FILE_APPEND);
    $logger->info("Python CMD string: " . $cmd);
    $output = shell_exec($cmd);

    return $output;
}

// Given DB Table Name, Colume Name, Username, and Password, return one correspondig value
function get_one_db_val($table_id, $col_id, $user, $pass, $logger){
    if (!($table_id && $col_id && $user && $pass))
        return "0";
    // Call Python to check Username and password
    $cmd = '/usr/bin/python2 /var/www/chaniq/py/get_one_db_val.py '. escapeshellarg($table_id) .' '. escapeshellarg($col_id) .' '. escapeshellarg($user) .' '. escapeshellarg($pass);
    #file_put_contents(__DIR__ . "/log/chaniq-php.log", "Python CMD string: " . $cmd . "\n", FILE_APPEND);
    $logger->info("Python CMD string: " . $cmd);
    $output = shell_exec($cmd);
    
    return $output;
}

if(isset($_POST['btnLogin'])){
    $authOut = check_login($_POST['username'], $_POST['password'], $logger);

    if($authOut == 1){
        if (session_id() != ''){
            session_unset();
            session_destroy();
            #file_put_contents(__DIR__ . "/log/chaniq-php.log", "login.php - redirection to login page!!\n", FILE_APPEND);
            $logger->info("login.php - redirection to login page!!");
            return;
        }
        session_start();
        $_SESSION['username'] = $_POST['username'];
        
        # Return string value from DB is in utf-8 format. We need to remove non-printable string for correct string comparison
        # For this use, preg_replace() - Ref: https://stackoverflow.com/questions/1176904/php-how-to-remove-all-non-printable-characters-in-a-string/28970891
        $role = preg_replace('/[\x00-\x1F\x7F]/u', '', get_one_db_val('users', 'role', $_POST['username'], $_POST['password'], $logger) );
        
        $_SESSION['role'] = $role;
        $_SESSION['loggedin'] = true;
        $_SESSION['sessID'] = session_id();
        #file_put_contents(__DIR__ . "/log/chaniq-php.log", "login.php - User is authenticated. Redirection to index page!!\n", FILE_APPEND);
        $logger->info("login.php - User is authenticated. Redirection to index page!!");
        header('Location: index.php');
    }
    elseif ($authOut == 'ERR' || $authOut == 0){
        #file_put_contents(__DIR__ . "/log/chaniq-php.log", "Login authen result: " . $authOut . "\n", FILE_APPEND);
        $logger->info("Login authen result: " . $authOut);
        header('Location: login.php');
    }
    else {
        header('Location: login.php');
    }

}

if(isset($_GET['action'])){
    session_start();
    #file_put_contents(__DIR__ . "/log/chaniq-php.log", "Session has been deleted through logout()\n", FILE_APPEND);
    #file_put_contents(__DIR__ . "/log/chaniq-php.log", "Session Info before destroy - username: " . $_SESSION['username'] . " Role: " . $_SESSION['role'] .  " Logged-IN: " . $_SESSION['loggedin'] . " Session ID: " . $_SESSION['sessID'] . "\n", FILE_APPEND);
    $logger->info("Session has been deleted through logout()");
    $logger->info("Session Info before destroy - username: " . $_SESSION['username'] . " Role: " . $_SESSION['role'] .  " Logged-IN: " . $_SESSION['loggedin'] . " Session ID: " . $_SESSION['sessID']);
    
    # Remove all session variables
    session_unset();
    #Now destory the session
    session_destroy();
    
    #file_put_contents(__DIR__ . "/log/chaniq-php.log", "login.php - Normal Logout process. Redirection to login page!!\n", FILE_APPEND);
    $logger->info("login.php - Normal Logout process. Redirection to login page!!");
    header('Location: login.php');
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
