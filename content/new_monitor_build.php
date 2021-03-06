<?php
require_once(__DIR__ . '/../utility/chaniqLogger.php');
    session_start();
    #file_put_contents("/var/log/chaniqphp.log", "new_monitor_build.php UN: " .$_SESSION['username'] . " Role: " . $_SESSION['role'] . " LoggedIn: " . $_SESSION['loggedin'] . "\n", FILE_APPEND);
    $logger->info("new_monitor_build.php UN: " .$_SESSION['username'] . " Role: " . $_SESSION['role'] . " LoggedIn: " . $_SESSION['loggedin']);
        if ($_SESSION['loggedin'] != true){
            session_unset();
            session_destroy();
            #file_put_contents("/var/log/chaniqphp.log", "new_monitor_build.php redirection to login page!!\n", FILE_APPEND);
            $logger->info("new_monitor_build.php redirection to login page!!");
            header('Location: ../login.php');
        }
        //Admin Content - Visible if the logged-in user has admin role
        if ($_SESSION['role'] == 'guest'){
            header('Location: contentbase.php');
        }

    //if(isset($_POST)==TRUE && empty($_POST)==FALSE):
    // If you put variables to save data from POST, it wont work. I moved the part under new_monitor_build()

    #error_log(date("y-m-d H:i:s").": new_monitor_build.php() - callBack function php has been called\n", 3, "/var/log/chaniqphp.log");
    $logger->info("new_monitor_build.php() - callBack function php has been called");
    //file_put_contents("/var/log/chaniqphp.log", "POST param phpFileName: " . $phpFileName . " devIP: " .$devIp ."VS name: ". $pVsName . "VsPort: " . $pVsPort . "Pool Mon: " . $pMon , FILE_APPEND);
    
    // Call new_monitor_build() by echo statement
    if (isset($_POST['jsonMonData'])){
        $monData = json_decode($_POST['jsonMonData']);
        #file_put_contents("/var/log/chaniqphp.log", "new_monitor_build() phpFile: " . $monData->phpFileName ."\n", FILE_APPEND);
        $logger->info("new_monitor_build() phpFile: " . $monData->phpFileName);
        
        // Call the fuction new_monitor_build()
        echo ($monData->phpFileName)($monData, $logger);
    }
    else{

        echo "AJAX call failed";
    }
    
    
    function new_monitor_build($monData, $logger) {
        #file_put_contents("/var/log/chaniqphp.log", "new_monitor_build() called\n", FILE_APPEND);
        $logger->info("new_monitor_build() called");

        $phpFileName = $monData->phpFileName;
        $mDevIp = $monData->DevIP;
        $monName = $monData->MonName;
        $mDesc = $monData->MDesc;
        $mEnv = $monData->MEnv;
        $mMonType = $monData->MMonType;
        $mMonCode = $monData->MMonCode;
        $mParMonType = $monData->MParMonType;
        $mInterval =  $monData->interval;
        $mTimeout =  $monData->timeout;
        $mSend =  $monData->send;
        $mRecv =  $monData->recv;
        $mUsername =  $monData->username;
        $mPassword =  $monData->password;
        $mReverse =  $monData->reverse;
        $mAliasPort =  $monData->aliasPort;
        $mCipherlist =  $monData->cipherlist;

        
        
        
        #file_put_contents("/var/log/chaniqphp.log", "new_monitor_build() Device IP: " . $mDevIp . " Desc: " .$mDesc. " Reverse: " .$mReverse." Alias Port: " .$mAliasPort." Cipherlist: " .$mCipherlist."\n", FILE_APPEND);
        $logger->info("new_monitor_build() Device IP: " . $mDevIp . " Desc: " .$mDesc. " Reverse: " .$mReverse." Alias Port: " .$mAliasPort." Cipherlist: " .$mCipherlist);
        
        $cmd = '/usr/bin/python /var/www/chaniq/py/new_monitor_build.py '. escapeshellarg($mDevIp) .' '. escapeshellarg($monName) .' '. escapeshellarg($mDesc) .' '. $mEnv .' '. escapeshellarg($mMonType) .' '. $mMonCode .' '. escapeshellarg($mParMonType) .' '. escapeshellarg($mInterval) .' '. escapeshellarg($mTimeout) .' '. escapeshellarg($mSend) .' '. escapeshellarg($mRecv) .' '. escapeshellarg($mUsername) .' '. escapeshellarg($mPassword) .' '. escapeshellarg($mReverse) .' '. escapeshellarg($mAliasPort) .' '. escapeshellarg($mCipherlist);
        
        $output = shell_exec($cmd);
        #error_log(date("y-m-d H:i:s").": After python call -new_monitor_build.php() new_monitor_build() function called!\n", 3, "/var/log/chaniqphp.log");
        $logger->info("After python call -new_monitor_build.php() new_monitor_build() function called!");
        
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