<?php
require_once(__DIR__ . '/../utility/chaniqLogger.php');
    session_start();
    #file_put_contents("/var/log/chaniqphp.log", "get_pool_monitors.php UN: " .$_SESSION['username'] . " Role: " . $_SESSION['role'] . " LoggedIn: " . $_SESSION['loggedin'] . "\n", FILE_APPEND);
    $logger->info("get_pool_monitors.php UN: " .$_SESSION['username'] . " Role: " . $_SESSION['role'] . " LoggedIn: " . $_SESSION['loggedin']);
    if ($_SESSION['loggedin'] != true){
        session_unset();
        session_destroy();
        #file_put_contents("/var/log/chaniqphp.log", "get_pool_monitors.php redirection to login page!!\n", FILE_APPEND);
        $logger->info("get_pool_monitors.php redirection to login page!!");
        header('Location: ../login.php');
    }
    //Admin Content - Visible if the logged-in user has admin role
    if ($_SESSION['role'] == 'guest'){
        header('Location: contentbase.php');
    }

    #error_log(date("y-m-d H:i:s").": get_pool_monitors() - callBack function php has been called\n", 3, "/var/log/chaniqphp.log");
    $logger->info("get_pool_monitors() - callBack function php has been called");
    
    // Call get_pool_monitors() by echo statement
    echo $_POST['method']($logger);
    
    /**
     * Given the name of active LTM, get the list of health monitors of the active ltm
     *
     * @param String $active_ltm The name of active LTM device
     * @param String $mon_type The name of a monitor type.
     *               1. TCP
     *               2. HTTP and HTTPS
     *               3. UDP
     *               4. TCP Half_open
     *               5. Gateway ICMP
     *               6. External
     * @return Array
     *
     */
    function get_healthmon($active_ltm, $mon_type, $logger)
    {
        $cmd = '/usr/bin/python /var/www/chaniq/py/get_healthmon.py '.$active_ltm.' ' . escapeshellarg($mon_type);
        //echo "<br>Command:" .$cmd." <br>";
        #error_log(date("y-m-d H:i:s").": get_pool_monitors() - get_healthmon() called\n", 3, "/var/log/chaniqphp.log");
        $logger->info("get_pool_monitors() - get_healthmon() called");
        exec($cmd, $output);
        
        //echo "<br>Output: " .$output[0];
        $rtn_out = explode(":", $output['0']);
        return $rtn_out;
    }
    
    function get_pool_monitors($logger) {
        if(isset($_POST['DevIP']))
        {
            //$bigipIP = json_decode($_POST['DevIP']);
            $bigipIP = $_POST['DevIP'];
            $monType = $_POST['LoadTypeName'];
            //error_log(date("y-m-d H:i:s").": get_pool_monitors() - Device IP sent over POST\n", 3, "/var/log/chaniqphp.log");
            #file_put_contents("/var/log/chaniqphp.log", "get_pool_monitor() Device IP: " . $bigipIP, FILE_APPEND);
            $logger->info("get_pool_monitor() Device IP: " . $bigipIP);
        }
        
        //$echoOut = echoTest();
        //file_put_contents("/var/log/chaniqphp.log", "get_pool_monitor() EchoTest: " . $echoOut, FILE_APPEND);
        $poolMonitors = get_healthmon($bigipIP, $monType, $logger);

        foreach ($poolMonitors as $value) {
            #file_put_contents("/var/log/chaniqphp.log", "Pool monitors: " . $value . "\n", FILE_APPEND);
            $logger->info("Pool monitors: " . $value);
        }
        $json = json_encode($poolMonitors);
        echo $json;
    }
?>