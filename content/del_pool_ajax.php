<?php
//if(isset($_POST)==TRUE && empty($_POST)==FALSE):
// If you put variables to save data from POST, it wont work. I moved the part under del_pool_ajax()
error_log(date("y-m-d H:i:s").": del_pool_ajax.php() - callBack function php has been called\n", 3, "/var/log/chaniqphp.log");
// Call del_pool_ajax() by echo statement
if (isset($_POST['jsonPoolData'])){
    $poolData = json_decode($_POST['jsonPoolData']);
    file_put_contents("/var/log/chaniqphp.log", "del_pool_ajax.php File: " . $poolData->PhpFileName ."\n", FILE_APPEND);
    
    // Call the fuction del_pool_ajax()
    echo ($poolData->PhpFileName)($poolData);
}
else{
    
    echo "Required Post parameter is missing";
}

//'PhpFileName':'', 'DevIP':'', 'P_name':'', 'P_part':'' 
function del_pool_ajax($poolData) {
    file_put_contents("/var/log/chaniqphp.log", "del_pool_ajax() called\n", FILE_APPEND);
    
    $pDevIp = $poolData->DevIP;
    $pName = $poolData->P_name;
    $pPart = $poolData->P_part;

    file_put_contents("/var/log/chaniqphp.log", "del_pool_ajax() 
          Device IP: " . $pDevIp . 
        " Pool Name: " . $pName . 
        " Pool Partition: " . $pPart . "\n", FILE_APPEND);
    
    $cmd = '/usr/bin/python /var/www/chaniq/py/del_pool_ajax.py '
        . escapeshellarg($pDevIp) .' '. escapeshellarg($pName) .' '. escapeshellarg($pPart);
    
        
    $output = shell_exec($cmd);
    error_log(date("y-m-d H:i:s").": After python call -del_pool_ajax.php() del_pool_ajax() function called!\n", 3, "/var/log/chaniqphp.log");
    
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