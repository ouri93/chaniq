<?php

    //if(isset($_POST)==TRUE && empty($_POST)==FALSE):
    // If you put variables to save data from POST, it wont work. I moved the part under load_irdg_names()

    error_log(date("y-m-d H:i:s").": load_irdg_names.php() - callBack function php has been called\n", 3, "/var/log/chaniqphp.log");
    
    // Call load_irdg_names() by echo statement
    if (isset($_POST['jsonIrData'])){
        $irData = json_decode($_POST['jsonIrData']);
        file_put_contents("/var/log/chaniqphp.log", "load_irdg_names() phpFile: " . $irData->phpFileName ."\n", FILE_APPEND);
        
        // Call the fuction load_irdg_names()
        echo ($irData->phpFileName)($irData);
    }
    else{

        echo "Required POST Data is not defined!";
    }
    
    
    function load_irdg_names($irData) {
        //'phpFileName' 'DevIP' 'IrType' 'IrDgPart'
        file_put_contents("/var/log/chaniqphp.log", "load_irdg_names() called\n", FILE_APPEND);
            
        $phpFileName = $irData->phpFileName;
        $irDevIp = $irData->DevIP;
        $irType = $irData->IrType;
        $irDgPart = $irData->IrDgPart;
        
        file_put_contents("/var/log/chaniqphp.log", "load_irdg_names() Device IP: " . $irDevIp . " Partition name: " .$irDgPart. " iRule or Data Group: " .$irType. "\n", FILE_APPEND);
        
        $cmd = '/usr/bin/python /var/www/chaniq/py/load_irdg_names.py '. escapeshellarg($irDevIp) .' '. escapeshellarg($irType) .' '. escapeshellarg($irDgPart);

        file_put_contents("/var/log/chaniqphp.log", "Python CMD output: " . $cmd . "\n", FILE_APPEND);
        
        $output = shell_exec($cmd);
        file_put_contents("/var/log/chaniqphp.log", "After python call - load_irdg_names.php() -> load_irdg_names() function called!\n", FILE_APPEND);
        
        $outputdata = json_decode($output, true);
        
        $rtnOutput = explode("|", $outputdata);
        
        foreach ($rtnOutput as $value){
            file_put_contents("/var/log/chaniqphp.log", "String Returned: " . $value . "\n", FILE_APPEND);
        }

        $json = json_encode($rtnOutput);
        
        echo $json;
    }
?>