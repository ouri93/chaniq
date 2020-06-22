<?php
require_once(__DIR__ . '/../utility/chaniqLogger.php');
    session_start();
    #file_put_contents("/var/log/chaniqphp.log", "get_vs_config.php UN: " .$_SESSION['username'] . " Role: " . $_SESSION['role'] . " LoggedIn: " . $_SESSION['loggedin'] . "\n", FILE_APPEND);
    $logger->info("get_vs_config.php UN: " .$_SESSION['username'] . " Role: " . $_SESSION['role'] . " LoggedIn: " . $_SESSION['loggedin']);
    if ($_SESSION['loggedin'] != true){
        session_unset();
        session_destroy();
        #file_put_contents("/var/log/chaniqphp.log", "get_vs_config.php redirection to login page!!\n", FILE_APPEND);
        $logger->info("get_vs_config.php redirection to login page!!");
        header('Location: ../login.php');
    }
    //Admin Content - Visible if the logged-in user has admin role
    if ($_SESSION['role'] == 'guest'){
        header('Location: contentbase.php');
    }

    #error_log(date("y-m-d H:i:s").": get_vs_config() - callBack function php has been called\n", 3, "/var/log/chaniqphp.log");
    $logger->info("get_vs_config() - callBack function php has been called");
    
    // Call get_vs_config() by echo statement
    echo $_POST['method']($logger);
    
    /**
     * Given the name of active LTM, get the list of pool names from the given active ltm
     *
     * @param String $active_ltm The name of active LTM device
     * @return Array
     *
     */
    function get_vsconfig($active_ltm, $vsname, $vspart, $logger)
    {
        $cmd = '/usr/bin/python /var/www/chaniq/py/get_vs_config.py '. $active_ltm . ' ' . $vsname .' '. $vspart;
        //echo "<br>Command:" .$cmd." <br>";
        #error_log(date("y-m-d H:i:s").": get_vs_config() - get_vsconfig() called\n", 3, "/var/log/chaniqphp.log");
        $logger->info("get_vs_config() - get_vsconfig() called");
        $output = shell_exec($cmd);

        return $output;
    }
    
    function get_vs_config($logger) {
        if(isset($_POST['DevIP']))
        {
            //$bigipIP = json_decode($_POST['DevIP']);
            $bigipIP = $_POST['DevIP'];
            $vsname = $_POST['VsName'];
            $vspart = $_POST['VsPart'];
            //error_log(date("y-m-d H:i:s").": get_vs_config() - Device IP sent over POST\n", 3, "/var/log/chaniqphp.log");
            #file_put_contents("/var/log/chaniqphp.log", "get_vs_config() Device IP: " . $bigipIP . "\nVS Name: " .$vsname. "\nVS Partition: " .$vspart. "\n", FILE_APPEND);
            $logger->info("get_vs_config() Device IP: " . $bigipIP . "\nVS Name: " .$vsname. "\nVS Partition: " .$vspart);
        }
        
        //$echoOut = echoTest();
        //file_put_contents("/var/log/chaniqphp.log", "get_vs_config() EchoTest: " . $echoOut, FILE_APPEND);
        $vsConfigs = get_vsconfig($bigipIP, $vsname, $vspart, $logger);
        #file_put_contents("/var/log/chaniqphp.log", "get_vs_config() - Return data from BIG-IP\n", FILE_APPEND);
        $logger->info("get_vs_config() - Return data from BIG-IP");
        //$json = json_encode($vsConfigs);
        echo $vsConfigs;
    }
?>