<?php
require_once(__DIR__ . '/../utility/chaniqLogger.php');
    session_start();
    #file_put_contents("/var/log/chaniqphp.log", "get_profile_names.php UN: " .$_SESSION['username'] . " Role: " . $_SESSION['role'] . " LoggedIn: " . $_SESSION['loggedin'] . "\n", FILE_APPEND);
    $logger->info("get_profile_names.php UN: " .$_SESSION['username'] . " Role: " . $_SESSION['role'] . " LoggedIn: " . $_SESSION['loggedin']);
    if ($_SESSION['loggedin'] != true){
        session_unset();
        session_destroy();
        #file_put_contents("/var/log/chaniqphp.log", "get_profile_names.php redirection to login page!!\n", FILE_APPEND);
        $logger->info("get_profile_names.php redirection to login page!!");
        header('Location: ../login.php');
    }
    //Admin Content - Visible if the logged-in user has admin role
    if ($_SESSION['role'] == 'guest'){
        header('Location: contentbase.php');
    }

    #error_log(date("y-m-d H:i:s").": get_profile_names() - callBack function php has been called\n", 3, "/var/log/chaniqphp.log");
    $logger->info("get_profile_names() - callBack function php has been called");
    
    // Call get_profile_names() by echo statement
    echo $_POST['method']($logger);
    
    /**
     * Given the name of active LTM, get the list of health monitors of the active ltm
     *
     * @param String $active_ltm The name of active LTM device
     * @param String $prf_type The name of a monitor type.
     *               1. TCP
     *               2. HTTP and HTTPS
     *               3. UDP
     *               4. TCP Half_open
     *               5. Gateway ICMP
     *               6. External
     * @return Array
     *
     */
    function get_names($active_ltm, $prfType, $logger)
    {
        $cmd = '/usr/bin/python2 /var/www/chaniq/py/get_profiles.py '.$active_ltm.' ' . escapeshellarg($prfType);
        //echo "<br>Command:" .$cmd." <br>";
        #error_log(date("y-m-d H:i:s").": get_profile_names() - get_names() called. Dev IP: " . $active_ltm . " Profile Type: " . $prfType . "\n", 3, "/var/log/chaniqphp.log");
        $logger->info("get_profile_names() - get_names() called. Dev IP: " . $active_ltm . " Profile Type: " . $prfType);
        exec($cmd, $output);
        
        //echo "<br>Output: " .$output[0];
        $rtn_out = explode(":", $output['0']);
        return $rtn_out;
    }
    
    function get_profile_names($logger) {
        if(isset($_POST['DevIP']))
        {
            //$bigipIP = json_decode($_POST['DevIP']);
            $bigipIP = $_POST['DevIP'];
            $prfType = $_POST['LoadTypeName'];
            //error_log(date("y-m-d H:i:s").": get_profile_names() - Device IP sent over POST\n", 3, "/var/log/chaniqphp.log");
            #file_put_contents("/var/log/chaniqphp.log", "get_profile_names() Device IP: " . $bigipIP."\n", FILE_APPEND);
            $logger->info("get_profile_names() Device IP: " . $bigipIP);
        }
        
        //$echoOut = echoTest();
        //file_put_contents("/var/log/chaniqphp.log", "get_profile_names(): " . $echoOut, FILE_APPEND);
        $prfNames = get_names($bigipIP, $prfType, $logger);

        foreach ($prfNames as $value) {
            #file_put_contents("/var/log/chaniqphp.log", "Profile name: " . $value . "\n", FILE_APPEND);
            $logger->info("Profile name: " . $value);
        }
        $json = json_encode($prfNames);
        echo $json;
    }
?>