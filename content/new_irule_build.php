<?php

    //if(isset($_POST)==TRUE && empty($_POST)==FALSE):
    // If you put variables to save data from POST, it wont work. I moved the part under new_irule_build()

    error_log(date("y-m-d H:i:s").": new_irule_build.php() - callBack function php has been called\n", 3, "/var/log/chaniqphp.log");
    
    // Call new_irule_build() by echo statement
    if (isset($_POST['jsonIrData'])){
        $irData = json_decode($_POST['jsonIrData']);
        file_put_contents("/var/log/chaniqphp.log", "new_irule_build() phpFile: " . $irData->phpFileName ."\n", FILE_APPEND);
        
        // Call the fuction new_irule_build()
        echo ($irData->phpFileName)($irData);
    }
    else{

        echo "AJAX call failed";
    }
    
    
    function new_irule_build($irData) {
        file_put_contents("/var/log/chaniqphp.log", "new_irule_build() called\n", FILE_APPEND);
            
        $phpFileName = $irData->phpFileName;
        $irDevIp = $irData->DevIP;
        $irVsName = $irData->IrVsName;
        $irVsPort = $irData->IrVsPort;
        $irEnv = $irData->IrEnv;
        $irType = $irData->IrType;
        $irCode = $irData->IrCode;
        $irDgType = $irData->IrDgType;
        $irDgData =  $irData->IrDgData;
        
        file_put_contents("/var/log/chaniqphp.log", "new_irule_build() Device IP: " . $irDevIp . " VS name: " .$irVsName. " Port: " .$irVsPort." Env: " .$irEnv." Irule Type: " .$irType." Irule Code: " .$irCode." DG Type: " .$irDgType." DG Data: " .$irDgData."\n", FILE_APPEND);
        
        $cmd = '/usr/bin/python /var/www/chaniq/py/new_irule_build.py '. escapeshellarg($irDevIp) .' '. escapeshellarg($irVsName) .' '. escapeshellarg($irVsPort) .' '. $irEnv .' '. escapeshellarg($irType) .' '. escapeshellarg($irCode) .' '. escapeshellarg($irDgType) .' '. escapeshellarg($irDgData);
        
        $output = shell_exec($cmd);
        error_log(date("y-m-d H:i:s").": After python call -new_irule_build.php() new_irule_build() function called!\n", 3, "/var/log/chaniqphp.log");
        
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