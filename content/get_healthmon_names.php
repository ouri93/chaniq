<?php
require_once(__DIR__ . '/../utility/chaniqLogger.php');
    session_start();
    #file_put_contents("/var/log/chaniqphp.log", "get_healthmon_names.php UN: " .$_SESSION['username'] . " Role: " . $_SESSION['role'] . " LoggedIn: " . $_SESSION['loggedin'] . "\n", FILE_APPEND);
    $logger->info("get_healthmon_names.php UN: " .$_SESSION['username'] . " Role: " . $_SESSION['role'] . " LoggedIn: " . $_SESSION['loggedin']);
    if ($_SESSION['loggedin'] != true){
        session_unset();
        session_destroy();
        #file_put_contents("/var/log/chaniqphp.log", "get_healthmon_names.php redirection to login page!!\n", FILE_APPEND);
        $logger->info("get_healthmon_names.php redirection to login page!!");
        header('Location: ../login.php');
    }
    //Admin Content - Visible if the logged-in user has admin role
    if ($_SESSION['role'] == 'guest'){
        header('Location: contentbase.php');
    }


    //if(isset($_POST)==TRUE && empty($_POST)==FALSE):
    // If you put variables to save data from POST, it wont work. I moved the part under get_healthmon_names()

    #error_log(date("y-m-d H:i:s").": get_healthmon_names.php() - callBack function php has been called\n", 3, "/var/log/chaniqphp.log");
    $logger->info("get_healthmon_names.php() - callBack function php has been called");
    
    // Call get_healthmon_names() by echo statement
    if (isset($_POST['jsonData'])){
        $monData = json_decode($_POST['jsonData']);
        #file_put_contents("/var/log/chaniqphp.log", "get_healthmon_names() phpFile: " . $monData->phpFileName ."\n", FILE_APPEND);
        $logger->info("get_healthmon_names() phpFile: " . $monData->phpFileName);
        
        // Call the fuction get_healthmon_names()
        echo ($monData->phpFileName)($monData, $logger);
    }
    else{

        echo "Required POST Data is not defined!";
    }
    
    
    function get_healthmon_names($monData, $logger) {
        //'phpFileName' 'DevIP' 'MonType' 'MonPart'
        #file_put_contents("/var/log/chaniqphp.log", "get_healthmon_names() called\n", FILE_APPEND);
        $logger->info("get_healthmon_names() called");
            
        $phpFileName = $monData->phpFileName;
        $devIp = $monData->DevIP;
        $monType = $monData->MonType;
        $monPart = $monData->MonPart;
        
        #file_put_contents("/var/log/chaniqphp.log", "get_healthmon_names() Device IP: " . $devIp . " Partition name: " .$monPart. " iRule or Data Group: " .$monType. "\n", FILE_APPEND);
        $logger->info("get_healthmon_names() Device IP: " . $devIp . " Partition name: " .$monPart. " iRule or Data Group: " .$monType);
        
        $cmd = '/usr/bin/python /var/www/chaniq/py/get_healthmon_names.py '. escapeshellarg($devIp) .' '. escapeshellarg($monType) .' '. escapeshellarg($monPart);

        #file_put_contents("/var/log/chaniqphp.log", "Python CMD output: " . $cmd . "\n", FILE_APPEND);
        $logger->info("Python CMD output: " . $cmd);
        
        $output = shell_exec($cmd);
        #file_put_contents("/var/log/chaniqphp.log", "After python call - get_healthmon_names.php() -> get_healthmon_names() function called!\n", FILE_APPEND);
        $logger->info("After python call - get_healthmon_names.php() -> get_healthmon_names() function called!");
        
        $rtnOutput = explode(":", $output);
        $json = json_encode($rtnOutput);
        
        echo $json;
        
    }
?>