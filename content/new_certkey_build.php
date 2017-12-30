<?php

    //if(isset($_POST)==TRUE && empty($_POST)==FALSE):
    // If you put variables to save data from POST, it wont work. I moved the part under new_certkey_build()

    error_log(date("y-m-d H:i:s").": new_certkey_build.php() - callBack function php has been called\n", 3, "/var/log/chaniqphp.log");
    
    // Call new_certkey_build() by echo statement
    if (isset($_POST['jsonCertkeyData'])){
        $certkeyData = json_decode($_POST['jsonCertkeyData']);
        file_put_contents("/var/log/chaniqphp.log", "new_certkey_build() phpFile: " . $certkeyData->phpFileName ."\n", FILE_APPEND);
        
        // Call the fuction new_certkey_build()
        echo ($certkeyData->phpFileName)($certkeyData);
    }
    else{

        echo "AJAX call failed";
    }
    
    function new_certkey_build($certkeyData) {
        file_put_contents("/var/log/chaniqphp.log", "new_certkey_build() called\n", FILE_APPEND);
            
        $phpFileName = $certkeyData->phpFileName;
        $certkeyDevIp = $certkeyData->sslDevIP;
        $certkeyImpType = $certkeyData->sslImpType;
        $certkeyImpName = $certkeyData->sslImpName;
        $certkeyKeySource = $certkeyData->sslKeySource;
        $certkeyKeySourceData = $certkeyData->sslKeySourceData;
        $certkeySecType = $certkeyData->sslSecType;
        $certkeySecTypeData = $certkeyData->sslSecTypeData;
        $certkeyPKCSPw = $certkeyData->sslPKCSPw;
        
        file_put_contents("/var/log/chaniqphp.log", "new_certkey_build() Device IP: " . $certkeyDevIp . " Import Type: " .$certkeyImpType. " Import Name: " .$certkeyImpName." Key Source: " .$certkeyKeySource." KeySource Data: " .$certkeyKeySourceData." Security Type: " .$certkeySecType." Security Type Data: " .$certkeySecTypeData." PKCS Password: " .$certkeyPKCSPw."\n", FILE_APPEND);
        
        $cmd = '/usr/bin/python /var/www/chaniq/py/new_certkey_build.py '. escapeshellarg($certkeyDevIp) .' '. escapeshellarg($certkeyImpType) .' '. escapeshellarg($certkeyImpName) .' '. escapeshellarg($certkeyKeySource) .' '. escapeshellarg($certkeyKeySourceData) .' '. escapeshellarg($certkeySecType) .' '. escapeshellarg($certkeySecTypeData) .' '. escapeshellarg($certkeyPKCSPw);
        
        $output = shell_exec($cmd);
        error_log(date("y-m-d H:i:s").": After python call -new_certkey_build.php() new_certkey_build() function called!\n", 3, "/var/log/chaniqphp.log");
        
        $outputdata = json_decode($output, true);
        ksort($outputdata);
        
        $rtnOutput = [];
        
        foreach ($outputdata as $key => $value){
            file_put_contents("/var/log/chaniqphp.log", "shell_exec() Return - Key: " . $key . " Value: " . $value , FILE_APPEND);
            array_push($rtnOutput, (string)$value);
        }
        
        foreach ($rtnOutput as $value){
            file_put_contents("/var/log/chaniqphp.log", "String Returned: " . $value , FILE_APPEND);
        }
        
        $json = json_encode($rtnOutput);
        
        echo $json;
    }
?>