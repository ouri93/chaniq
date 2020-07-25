<?php
require_once(__DIR__ . '/../utility/chaniqLogger.php');

    session_start();
    #file_put_contents("/var/log/chaniqphp.log", "del_monitor_ajax.php UN: " .$_SESSION['username'] . " Role: " . $_SESSION['role'] . " LoggedIn: " . $_SESSION['loggedin'] . "\n", FILE_APPEND);
    $logger->info("del_monitor_ajax.php UN: " .$_SESSION['username'] . " Role: " . $_SESSION['role'] . " LoggedIn: " . $_SESSION['loggedin']);
    if ($_SESSION['loggedin'] != true){
        session_unset();
        session_destroy();
        #file_put_contents("/var/log/chaniqphp.log", "del_monitor_ajax.php redirection to login page!!\n", FILE_APPEND);
        $logger->info("del_monitor_ajax.php redirection to login page!!");
        header('Location: ../login.php');
    }
    //Admin Content - Visible if the logged-in user has admin role
    if ($_SESSION['role'] == 'guest'){
        header('Location: contentbase.php');
    }


    //if(isset($_POST)==TRUE && empty($_POST)==FALSE):
    // If you put variables to save data from POST, it wont work. I moved the part under del_monitor_ajax()

    #error_log(date("y-m-d H:i:s").": del_monitor_ajax.php() - callBack function php has been called\n", 3, "/var/log/chaniqphp.log");
    $logger->info("del_monitor_ajax.php() - callBack function php has been called");
    //file_put_contents("/var/log/chaniqphp.log", "POST param phpFileName: " . $phpFileName . " devIP: " .$devIp ."VS name: ". $pVsName . "VsPort: " . $pVsPort . "Pool Mon: " . $pMon , FILE_APPEND);
    
    // Call del_monitor_ajax() by echo statement
    if (isset($_POST['jsonData'])){
        $monData = json_decode($_POST['jsonData']);
        #file_put_contents("/var/log/chaniqphp.log", "del_monitor_ajax() phpFile: " . $monData->phpFileName ."\n", FILE_APPEND);
        $logger->info("del_monitor_ajax() phpFile: " . $monData->phpFileName);
        
        // Call the fuction del_monitor_ajax()
        echo ($monData->phpFileName)($monData, $logger);
    }
    else{

        echo "Required POST Data is not defined!";
    }
    
    
    //'phpFileName':'', 'DevIP':'', 'MonName':'', 'MDesc':'', 'MMonType':'', 'MParMonType':''
    function del_monitor_ajax($monData, $logger) {
        #file_put_contents("/var/log/chaniqphp.log", "del_monitor_ajax() called\n", FILE_APPEND);
        $logger->info("del_monitor_ajax() called");

        $phpFileName = $monData->phpFileName;
        $mDevIp = $monData->DevIP;
        $monName = $monData->MonName;
        $mDesc = $monData->MDesc;
        $mMonType = $monData->MMonType;
        $mParMonType = $monData->MParMonType;

        //file_put_contents("/var/log/chaniqphp.log", "del_monitor_ajax() Device IP: " . $mDevIp . " Desc: " .$mDesc. " Reverse: " .$mReverse." Alias Port: " .$mAliasPort." Cipherlist: " .$mCipherlist."\n", FILE_APPEND);
        
        $cmd = '/usr/bin/python2 /var/www/chaniq/py/del_monitor_ajax.py '. escapeshellarg($mDevIp) .' '. escapeshellarg($monName) .' '. escapeshellarg($mDesc) .' '. escapeshellarg($mMonType) .' '. escapeshellarg($mParMonType);
        
        $output = shell_exec($cmd);
        #error_log(date("y-m-d H:i:s").": After python call -del_monitor_ajax.php() del_monitor_ajax() function called!\n", 3, "/var/log/chaniqphp.log");
        $logger->info("After python call -del_monitor_ajax.php() del_monitor_ajax() function called!");
        
        $outputdata = json_decode($output, true);
        ksort($outputdata);
        
        $rtnOutput = [];
        
        foreach ($outputdata as $key => $value){
            #file_put_contents("/var/log/chaniqphp.log", "shell_exec() Return - Key: " . $key . " Value: " . $value ."\n" , FILE_APPEND);
            $logger->info("shell_exec() Return - Key: " . $key . " Value: " . $value);
            array_push($rtnOutput, (string)$value);
        }
        
        foreach ($rtnOutput as $value){
            #file_put_contents("/var/log/chaniqphp.log", "String Returned: " . $value ."\n", FILE_APPEND);
            $logger->info("String Returned: " . $value);
        }
        
        $json = json_encode($rtnOutput);
        
        echo $json;
    }
?>