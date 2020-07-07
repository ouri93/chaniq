<?php
require_once(__DIR__ . '/../utility/chaniqLogger.php');
    session_start();
    #file_put_contents("/var/log/chaniqphp.log", "new_certkey_build.php UN: " .$_SESSION['username'] . " Role: " . $_SESSION['role'] . " LoggedIn: " . $_SESSION['loggedin'] . "\n", FILE_APPEND);
    $logger->info("new_certkey_build.php UN: " .$_SESSION['username'] . " Role: " . $_SESSION['role'] . " LoggedIn: " . $_SESSION['loggedin']);
    if ($_SESSION['loggedin'] != true){
        session_unset();
        session_destroy();
        #file_put_contents("/var/log/chaniqphp.log", "new_certkey_build.php redirection to login page!!\n", FILE_APPEND);
        $logger->info("new_certkey_build.php redirection to login page!!");
        header('Location: ../login.php');
    }
    //Admin Content - Visible if the logged-in user has admin role
    if ($_SESSION['role'] == 'guest'){
        header('Location: contentbase.php');
    }


    //if(isset($_POST)==TRUE && empty($_POST)==FALSE):
    // If you put variables to save data from POST, it wont work. I moved the part under new_certkey_build()

    #error_log(date("y-m-d H:i:s").": new_certkey_build.php() - callBack function php has been called\n", 3, "/var/log/chaniqphp.log");
    $logger->info("new_certkey_build.php() - callBack function php has been called");
    
    // Call new_certkey_build() by echo statement
    if (isset($_POST['jsonCertkeyData'])){
        $certkeyData = json_decode($_POST['jsonCertkeyData']);
        #file_put_contents("/var/log/chaniqphp.log", "new_certkey_build() phpFile: " . $certkeyData->phpFileName ."\n", FILE_APPEND);
        $logger->info("new_certkey_build() phpFile: " . $certkeyData->phpFileName);
        
        // Call the fuction new_certkey_build()
        echo ($certkeyData->phpFileName)($certkeyData, $logger);
    }
    else{

        echo "AJAX call failed";
    }
    
    function new_certkey_build($certkeyData, $logger) {
        #file_put_contents("/var/log/chaniqphp.log", "new_certkey_build() called\n", FILE_APPEND);
        $logger->info("new_certkey_build() called");
            
        $phpFileName = $certkeyData->phpFileName;
        $certkeyDevIp = $certkeyData->sslDevIP;
        $certkeyImpType = $certkeyData->sslImpType;
        $certkeyImpName = $certkeyData->sslImpName;
        $certkeyKeySource = $certkeyData->sslKeySource;
        $certkeyKeySourceData = $certkeyData->sslKeySourceData;
        $certkeySecType = $certkeyData->sslSecType;
        $certkeySecTypeData = $certkeyData->sslSecTypeData;
        $certkeyPKCSPw = $certkeyData->sslPKCSPw;
        
        #file_put_contents("/var/log/chaniqphp.log", "new_certkey_build() Device IP: " . $certkeyDevIp . " Import Type: " .$certkeyImpType. " Import Name: " .$certkeyImpName." Key Source: " .$certkeyKeySource." KeySource Data: " .$certkeyKeySourceData." Security Type: " .$certkeySecType." Security Type Data: " .$certkeySecTypeData." PKCS Password: " .$certkeyPKCSPw."\n", FILE_APPEND);
        $logger->info("new_certkey_build() Device IP: " . $certkeyDevIp . " Import Type: " .$certkeyImpType. " Import Name: " .$certkeyImpName." Key Source: " .$certkeyKeySource." KeySource Data: " .$certkeyKeySourceData." Security Type: " .$certkeySecType." Security Type Data: " .$certkeySecTypeData." PKCS Password: " .$certkeyPKCSPw);
        
        $cmd = '/usr/bin/python2 /var/www/chaniq/py/new_certkey_build.py '. escapeshellarg($certkeyDevIp) .' '. escapeshellarg($certkeyImpType) .' '. escapeshellarg($certkeyImpName) .' '. escapeshellarg($certkeyKeySource) .' '. escapeshellarg($certkeyKeySourceData) .' '. escapeshellarg($certkeySecType) .' '. escapeshellarg($certkeySecTypeData) .' '. escapeshellarg($certkeyPKCSPw);
        
        $output = shell_exec($cmd);
        #error_log(date("y-m-d H:i:s").": After python call -new_certkey_build.php() new_certkey_build() function called!\n", 3, "/var/log/chaniqphp.log");
        $logger->info("After python call -new_certkey_build.php() new_certkey_build() function called!");
        
        $outputdata = json_decode($output, true);
        ksort($outputdata);
        
        $rtnOutput = [];
        
        foreach ($outputdata as $key => $value){
            #file_put_contents("/var/log/chaniqphp.log", "shell_exec() Return - Key: " . $key . " Value: " . $value , FILE_APPEND);
            $logger->info("shell_exec() Return - Key: " . $key . " Value: " . $value);
            array_push($rtnOutput, (string)$value);
        }
        
        foreach ($rtnOutput as $value){
            #file_put_contents("/var/log/chaniqphp.log", "String Returned: " . $value , FILE_APPEND);
            $logger->info("String Returned: " . $value);
        }
        
        $json = json_encode($rtnOutput);
        
        echo $json;
    }
?>