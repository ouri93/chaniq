<?php

    //if(isset($_POST)==TRUE && empty($_POST)==FALSE):
    // If you put variables to save data from POST, it wont work. I moved the part under del_irdg_ajax()

    error_log(date("y-m-d H:i:s").": del_irdg_ajax.php() - callBack function php has been called\n", 3, "/var/log/chaniqphp.log");
    
    // Call del_irdg_ajax() by echo statement
    if (isset($_POST['jsonData'])){
        $irData = json_decode($_POST['jsonData']);
        file_put_contents("/var/log/chaniqphp.log", "del_irdg_ajax() phpFile: " . $irData->phpFileName ."\n", FILE_APPEND);
        
        // Call the fuction del_irdg_ajax()
        echo ($irData->phpFileName)($irData);
    }
    else{

        echo "Required POST Data is not defined!";
    }
    
    
    function del_irdg_ajax($irData) {
        //'phpFileName':'', 'DevIP':'', 'IrDgName':'', 'IrType':'', 'IrDgType':''
        file_put_contents("/var/log/chaniqphp.log", "del_irdg_ajax() called\n", FILE_APPEND);
            
        $phpFileName = $irData->phpFileName;
        $irDevIp = $irData->DevIP;
        $irDgName = $irData->IrDgName;
        $irOrDg = $irData->IrType;
        $dgType = $irData->IrDgType;
        
        file_put_contents("/var/log/chaniqphp.log", "del_irdg_ajax() Device IP: " . $irDevIp . " iRule/DataGroup name: " .$irDgName. " Config Type: " .$irOrDg. " DataGroup Type: " .$dgType. "\n", FILE_APPEND);
        
        $cmd = '/usr/bin/python /var/www/chaniq/py/del_irdg_ajax.py '. escapeshellarg($irDevIp) .' '. escapeshellarg($irDgName) .' '. escapeshellarg($irOrDg) .' '. escapeshellarg($dgType);

        file_put_contents("/var/log/chaniqphp.log", "Python CMD output: " . $cmd . "\n", FILE_APPEND);
        
        $output = shell_exec($cmd);
        file_put_contents("/var/log/chaniqphp.log", "After python call - del_irdg_ajax.php() -> del_irdg_ajax() function called!\n", FILE_APPEND);
        
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