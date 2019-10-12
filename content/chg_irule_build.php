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
        $irDgName = $irData->IrDgName;
        $irEnv = $irData->IrEnv;
        $irType = $irData->IrType;
        $irCode = $irData->IrCode;
        $irDgType = $irData->IrDgType;
        $irDgData =  $irData->IrDgData;
        
        file_put_contents("/var/log/chaniqphp.log", "new_irule_build() Device IP: " . $irDevIp . " iRule/DataGroup name: " .$irDgName. " Env: " .$irEnv." Config Type: " .$irType." Irule Code: " .$irCode." DataGroup Type: " .$irDgType." DG Data: " .$irDgData . "\n", FILE_APPEND);
        
        $cmd = '/usr/bin/python /var/www/chaniq/py/new_irule_build.py '. escapeshellarg($irDevIp) .' '. escapeshellarg($irDgName) .' '. escapeshellarg($irEnv) .' '. escapeshellarg($irType) .' '. escapeshellarg($irCode) .' '. escapeshellarg($irDgType) .' '. escapeshellarg($irDgData);

        file_put_contents("/var/log/chaniqphp.log", "Python CMD output: " . $cmd . "\n", FILE_APPEND);
        
        $output = shell_exec($cmd);
        file_put_contents("/var/log/chaniqphp.log", "After python call - new_irule_build.php() -> new_irule_build() function called!\n", FILE_APPEND);
        
        $outputdata = json_decode($output, true);
        
        if (!ksort($outputdata)){
            file_put_contents("/var/log/chaniqphp.log", "Ksort returned False!\n", FILE_APPEND);
        };
        
        $rtnOutput = [];
        
        foreach ($outputdata as $key => $value){
            file_put_contents("/var/log/chaniqphp.log", "shell_exec() Return - Key: " . $key . " Value: " . $value . "\n", FILE_APPEND);
            array_push($rtnOutput, (string)$value);
        }
        
        foreach ($rtnOutput as $value){
            file_put_contents("/var/log/chaniqphp.log", "String Returned: " . $value . "\n", FILE_APPEND);
        }
        
        $json = json_encode($rtnOutput);
        
        echo $json;
    }
?>