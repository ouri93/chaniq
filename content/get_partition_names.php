<?php
require_once(__DIR__ . '/../utility/chaniqLogger.php');
    session_start();
    #file_put_contents("/var/log/chaniqphp.log", "get_partition_names.php UN: " .$_SESSION['username'] . " Role: " . $_SESSION['role'] . " LoggedIn: " . $_SESSION['loggedin'] . "\n", FILE_APPEND);
    $logger->info("get_partition_names.php UN: " .$_SESSION['username'] . " Role: " . $_SESSION['role'] . " LoggedIn: " . $_SESSION['loggedin']);
    if ($_SESSION['loggedin'] != true){
        session_unset();
        session_destroy();
        #file_put_contents("/var/log/chaniqphp.log", "get_partition_names.php redirection to login page!!\n", FILE_APPEND);
        $logger->info("get_partition_names.php redirection to login page!!");
        header('Location: ../login.php');
    }
    //Admin Content - Visible if the logged-in user has admin role
    if ($_SESSION['role'] == 'guest'){
        header('Location: contentbase.php');
    }

    #error_log(date("y-m-d H:i:s").": get_partition_names() - callBack function php has been called\n", 3, "/var/log/chaniqphp.log");
    $logger->info("get_partition_names() - callBack function php has been called");
    
    // Call get_pool_names() by echo statement
    if (isset($_POST['jsonData'])){
        $jsonData = json_decode($_POST['jsonData']);
        #file_put_contents("/var/log/chaniqphp.log", "get_partition_names.php File: " . $jsonData->phpFileName ."\n", FILE_APPEND);
        $logger->info("get_partition_names.php File: " . $jsonData->phpFileName);
        
        // Call the fuction chg_pool_build()
        echo ($jsonData->phpFileName)($jsonData, $logger);
    }
    else
        echo "Requried POST parameter is missing!";
    
    /**
     * Given the name of active LTM, get the list of pool names from the given active ltm
     *
     * @param String $active_ltm The name of active LTM device
     * @return Array
     *
     */
    function get_partition_names($jsonData, $logger) {
        $active_ltm = $jsonData->DevIP;
        #file_put_contents("/var/log/chaniqphp.log", "get_partition_names() Device IP: " . $active_ltm . "\n", FILE_APPEND);
        $logger->info("get_partition_names() Device IP: " . $active_ltm);
        
        $cmd = '/usr/bin/python2 /var/www/chaniq/py/get_partition_names.py '.$active_ltm;
        //echo "<br>Command:" .$cmd." <br>";
        #error_log(date("y-m-d H:i:s").": get_partition_names() called\n", 3, "/var/log/chaniqphp.log");
        $logger->info("get_partition_names() called");
        // Return format - Null (''), partition1:, part1:part2:
        $output = shell_exec($cmd);
        #file_put_contents("/var/log/chaniqphp.log", "Partition names: " . $output . "\n", FILE_APPEND);
        $logger->info("Partition names: " . $output);
       
        $json = json_encode($output);
        echo $json;
    }
?>