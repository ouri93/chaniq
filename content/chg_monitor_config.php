<?php
    session_start();
    file_put_contents("/var/log/chaniqphp.log", "chg_monitor_config.php UN: " .$_SESSION['username'] . " Role: " . $_SESSION['role'] . " LoggedIn: " . $_SESSION['loggedin'] . "\n", FILE_APPEND);
    if ($_SESSION['loggedin'] != true){
        session_unset();
        session_destroy();
        file_put_contents("/var/log/chaniqphp.log", "chg_monitor_config.php redirection to login page!!\n", FILE_APPEND);
        header('Location: ../login.php');
    }
    if ($_SESSION['role'] == 'guest'){
        header('Location: contentbase.php');
    }

    //if(isset($_POST)==TRUE && empty($_POST)==FALSE):
    // If you put variables to save data from POST, it wont work. I moved the part under chg_monitor_config()

    error_log(date("y-m-d H:i:s").": chg_monitor_config.php() - callBack function php has been called\n", 3, "/var/log/chaniqphp.log");
    //file_put_contents("/var/log/chaniqphp.log", "POST param phpFileName: " . $phpFileName . " devIP: " .$devIp ."VS name: ". $pVsName . "VsPort: " . $pVsPort . "Pool Mon: " . $pMon , FILE_APPEND);
    
    // Call chg_monitor_config() by echo statement
    if (isset($_POST['jsonMonData'])){
        $monData = json_decode($_POST['jsonMonData']);
        file_put_contents("/var/log/chaniqphp.log", "chg_monitor_config() phpFile: " . $monData->phpFileName ."\n", FILE_APPEND);
        
        // Call the fuction chg_monitor_config()
        echo ($monData->phpFileName)($monData);
    }
    else{

        echo "Ajax call failed as jsonPoolData POST data is not defined during AJAX call";
    }
    
    
    function chg_monitor_config($monData) {
        file_put_contents("/var/log/chaniqphp.log", "chg_monitor_config() called\n", FILE_APPEND);

        $phpFileName = $monData->phpFileName;
        $mDevIp = $monData->DevIP;
        $monName = $monData->MonName;
        $mDesc = $monData->MDesc;
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

        
        
        
        //file_put_contents("/var/log/chaniqphp.log", "chg_monitor_config() Device IP: " . $mDevIp . " Desc: " .$mDesc. " Reverse: " .$mReverse." Alias Port: " .$mAliasPort." Cipherlist: " .$mCipherlist."\n", FILE_APPEND);
        
        $cmd = '/usr/bin/python /var/www/chaniq/py/chg_monitor_config.py '. escapeshellarg($mDevIp) .' '. escapeshellarg($monName) .' '. escapeshellarg($mDesc) .' '. escapeshellarg($mMonType) .' '. $mMonCode .' '. escapeshellarg($mParMonType) .' '. escapeshellarg($mInterval) .' '. escapeshellarg($mTimeout) .' '. escapeshellarg($mSend) .' '. escapeshellarg($mRecv) .' '. escapeshellarg($mUsername) .' '. escapeshellarg($mPassword) .' '. escapeshellarg($mReverse) .' '. escapeshellarg($mAliasPort) .' '. escapeshellarg($mCipherlist);
        
        $output = shell_exec($cmd);
        error_log(date("y-m-d H:i:s").": After python call -chg_monitor_config.php() chg_monitor_config() function called!\n", 3, "/var/log/chaniqphp.log");
        
        $outputdata = json_decode($output, true);
        ksort($outputdata);
        
        $rtnOutput = [];
        
        foreach ($outputdata as $key => $value){
            file_put_contents("/var/log/chaniqphp.log", "shell_exec() Return - Key: " . $key . " Value: " . $value ."\n" , FILE_APPEND);
            array_push($rtnOutput, (string)$value);
        }
        
        foreach ($rtnOutput as $value){
            file_put_contents("/var/log/chaniqphp.log", "String Returned: " . $value ."\n", FILE_APPEND);
        }
        
        $json = json_encode($rtnOutput);
        
        echo $json;
    }
?>