<?php
require_once(__DIR__ . '/../utility/chaniqLogger.php');
    session_start();
    #file_put_contents("/var/log/chaniqphp.log", "get_healthmon_settings.php UN: " .$_SESSION['username'] . " Role: " . $_SESSION['role'] . " LoggedIn: " . $_SESSION['loggedin'] . "\n", FILE_APPEND);
    $logger->info("get_healthmon_settings.php UN: " .$_SESSION['username'] . " Role: " . $_SESSION['role'] . " LoggedIn: " . $_SESSION['loggedin']);
    if ($_SESSION['loggedin'] != true){
        session_unset();
        session_destroy();
        #file_put_contents("/var/log/chaniqphp.log", "get_healthmon_settings.php redirection to login page!!\n", FILE_APPEND);
        $logger->info("get_healthmon_settings.php redirection to login page!!");
        header('Location: ../login.php');
    }
    //Admin Content - Visible if the logged-in user has admin role
    if ($_SESSION['role'] == 'guest'){
        header('Location: contentbase.php');
    }


    #error_log(date("y-m-d H:i:s").": get_healthmon_settings() - callBack function php has been called\n", 3, "/var/log/chaniqphp.log");
    $logger->info("get_healthmon_settings() - callBack function php has been called");
    
    // Call get_pool_monitors() by echo statement
    echo $_POST['phpFile']($logger);
    
    function get_healthmon_settings($logger) {
        if(isset($_POST['DevIP']))
        {
            //$bigipIP = json_decode($_POST['DevIP']);
            $bigipIP = $_POST['DevIP'];
            $monType = $_POST['MonType'];
            $parMonType = $_POST['ParMonType'];
            //error_log(date("y-m-d H:i:s").": get_pool_monitors() - Device IP sent over POST\n", 3, "/var/log/chaniqphp.log");
            #file_put_contents("/var/log/chaniqphp.log", "get_healthmon_settings() Device IP: " . $bigipIP . " Mon Type: " . $monType . " Parent Mon: " . $parMonType . "\n", FILE_APPEND);
            $logger->info("get_healthmon_settings() Device IP: " . $bigipIP . " Mon Type: " . $monType . " Parent Mon: " . $parMonType);
        }

        $cmd = '/usr/bin/python /var/www/chaniq/py/get_healthmon_settings.py '. $bigipIP . ' ' . escapeshellarg($monType) . ' ' . escapeshellarg($parMonType);
        //echo "<br>Command:" .$cmd." <br>";
        #error_log(date("y-m-d H:i:s").": get_healthmon_settings() - get_healthmon_settings() called\n", 3, "/var/log/chaniqphp.log");
        $logger->info("get_healthmon_settings() - get_healthmon_settings() called");
        exec($cmd, $output);

        #file_put_contents("/var/log/chaniqphp.log", "Output: " . $output[0] ."\n", FILE_APPEND);
        $logger->info("Output: " . $output[0]);
  
        //return '[{"Name":"BIG-IP", "Version":"12.1.2" }]';
        return $output[0];
    }
?>