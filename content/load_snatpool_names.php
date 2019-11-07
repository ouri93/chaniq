<?php

//if(isset($_POST)==TRUE && empty($_POST)==FALSE):
// If you put variables to save data from POST, it wont work. I moved the part under load_snatpool_names()

error_log(date("y-m-d H:i:s").": load_snatpool_names.php() - callBack function php has been called\n", 3, "/var/log/chaniqphp.log");

// Call load_snatpool_names() by echo statement
if (isset($_POST['jsonData'])){
    $snatData = json_decode($_POST['jsonData']);
    file_put_contents("/var/log/chaniqphp.log", "load_snatpool_names() phpFile: " . $snatData->PhpFileName ."\n", FILE_APPEND);
    
    // Call the fuction load_snatpool_names()
    echo ($snatData->PhpFileName)($snatData);
}
else{
    
    echo "Required POST Data is not defined!";
}

function load_snatpool_names($snatData) {
    file_put_contents("/var/log/chaniqphp.log", "load_snatpool_names() called\n", FILE_APPEND);
    
    $phpFileName = $snatData->PhpFileName;
    $DevIp = $snatData->DevIP;
    
    file_put_contents("/var/log/chaniqphp.log", "load_snatpool_names() Device IP: " . $DevIp . "\n", FILE_APPEND);
    
    $cmd = '/usr/bin/python /var/www/chaniq/py/load_snatpool_names.py '. escapeshellarg($DevIp);
    
    $output = shell_exec($cmd);
    error_log(date("y-m-d H:i:s").": After python call -load_snatpool_names.php() load_snatpool_names() function called!\n", 3, "/var/log/chaniqphp.log");
    
    $outputdata = json_decode($output, true);
    ksort($outputdata);
    
    foreach ($outputdata as $value){
        file_put_contents("/var/log/chaniqphp.log", "String Returned: " . $value , FILE_APPEND);
    }
    
    $json = json_encode($outputdata);
    
    echo $json;
}
?>