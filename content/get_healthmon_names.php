<?php

    //if(isset($_POST)==TRUE && empty($_POST)==FALSE):
    // If you put variables to save data from POST, it wont work. I moved the part under get_healthmon_names()

    error_log(date("y-m-d H:i:s").": get_healthmon_names.php() - callBack function php has been called\n", 3, "/var/log/chaniqphp.log");
    
    // Call get_healthmon_names() by echo statement
    if (isset($_POST['jsonData'])){
        $monData = json_decode($_POST['jsonData']);
        file_put_contents("/var/log/chaniqphp.log", "get_healthmon_names() phpFile: " . $monData->phpFileName ."\n", FILE_APPEND);
        
        // Call the fuction get_healthmon_names()
        echo ($monData->phpFileName)($monData);
    }
    else{

        echo "Required POST Data is not defined!";
    }
    
    
    function get_healthmon_names($monData) {
        //'phpFileName' 'DevIP' 'MonType' 'MonPart'
        file_put_contents("/var/log/chaniqphp.log", "get_healthmon_names() called\n", FILE_APPEND);
            
        $phpFileName = $monData->phpFileName;
        $devIp = $monData->DevIP;
        $monType = $monData->MonType;
        $monPart = $monData->MonPart;
        
        file_put_contents("/var/log/chaniqphp.log", "get_healthmon_names() Device IP: " . $devIp . " Partition name: " .$monPart. " iRule or Data Group: " .$monType. "\n", FILE_APPEND);
        
        $cmd = '/usr/bin/python /var/www/chaniq/py/get_healthmon_names.py '. escapeshellarg($devIp) .' '. escapeshellarg($monType) .' '. escapeshellarg($monPart);

        file_put_contents("/var/log/chaniqphp.log", "Python CMD output: " . $cmd . "\n", FILE_APPEND);
        
        $output = shell_exec($cmd);
        file_put_contents("/var/log/chaniqphp.log", "After python call - get_healthmon_names.php() -> get_healthmon_names() function called!\n", FILE_APPEND);
        
        $rtnOutput = explode(":", $output);
        $json = json_encode($rtnOutput);
        
        echo $json;
        
    }
?>