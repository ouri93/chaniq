<?php

//if(isset($_POST)==TRUE && empty($_POST)==FALSE):
// If you put variables to save data from POST, it wont work. I moved the part under del_snatpool_ajax()

error_log(date("y-m-d H:i:s").": del_snatpool_ajax.php() - callBack function php has been called\n", 3, "/var/log/chaniqphp.log");

// Call del_snatpool_ajax() by echo statement
if (isset($_POST['jsonData'])){
    $snatData = json_decode($_POST['jsonData']);
    file_put_contents("/var/log/chaniqphp.log", "del_snatpool_ajax() phpFile: " . $snatData->PhpFileName ."\n", FILE_APPEND);
    
    // Call the fuction del_snatpool_ajax()
    echo ($snatData->PhpFileName)($snatData);
}
else{
    
    echo "Required POST Data is not defined!";
}

//'PhpFileName':'', 'DevIP':'', 'Name':'', 'Partition':''
function del_snatpool_ajax($snatData) {
    file_put_contents("/var/log/chaniqphp.log", "del_snatpool_ajax() called\n", FILE_APPEND);
    
    $phpFileName = $snatData->PhpFileName;
    $DevIp = $snatData->DevIP;
    $snatpoolName = $snatData->Name;
    $snatPartName = $snatData->Partition;
    
    file_put_contents("/var/log/chaniqphp.log", "del_snatpool_ajax() Device IP: " . $DevIp . " Snatpool name: " . $snatpoolName. " Snatpool Partition: " .$snatPartName. "\n", FILE_APPEND);
    
    $cmd = '/usr/bin/python /var/www/chaniq/py/del_snatpool_ajax.py ' .escapeshellarg($DevIp). ' ' .escapeshellarg($snatpoolName). ' ' .escapeshellarg($snatPartName);
    
    $output = shell_exec($cmd);
    error_log(date("y-m-d H:i:s").": After python call -del_snatpool_ajax.php() del_snatpool_ajax() function called!\n", 3, "/var/log/chaniqphp.log");
    
    $outputdata = json_decode($output, true);
    ksort($outputdata);
    
    foreach ($outputdata as $value){
        file_put_contents("/var/log/chaniqphp.log", "String Returned: " . $value , FILE_APPEND);
    }
    
    $json = json_encode($outputdata);
    
    echo $json;
}
?>