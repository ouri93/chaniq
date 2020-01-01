<?php
include('../utility/utility.php');

//if(isset($_POST)==TRUE && empty($_POST)==FALSE):
// If you put variables to save data from POST, it wont work. I moved the part under resetuserpw_ajax()
error_log(date("y-m-d H:i:s").": resetuserpw_ajax.php() - callBack function php has been called\n", 3, "/var/log/chaniqphp.log");
// Call resetuserpw_ajax() by echo statement
if (isset($_POST['jsonPassData'])){
    $passData = json_decode($_POST['jsonPassData']);
    file_put_contents("/var/log/chaniqphp.log", "resetuserpw_ajax.php File: " . $passData->PhpFileName ."\n", FILE_APPEND);
    
    // Call the fuction resetuserpw_ajax()
    echo ($passData->PhpFileName)($passData);
}
else{
    
    echo "Required Post parameter is missing";
}

//'PhpFileName':'', 'UserName':'', 'UserRole':'', 'CurPass':'', 'NewPass':''
function resetuserpw_ajax($passData) {
    file_put_contents("/var/log/chaniqphp.log", "resetuserpw_ajax() called\n", FILE_APPEND);
    
    $un = $passData->UserName;
    $role = $passData->UserRole;
    $newpass = $passData->NewPass;
    $db_ip = parse_ini_sec_val('DB_CONFIG', "DB_IP");

    file_put_contents("/var/log/chaniqphp.log", "resetuserpw_ajax() DB IP: " . $db_ip . "\n", FILE_APPEND);
    
    $cmd = '/usr/bin/python /var/www/chaniq/py/resetuserpw_ajax.py ' . escapeshellarg($db_ip) .' '. escapeshellarg($un) .' '. escapeshellarg($role) .' '. escapeshellarg($newpass);
    
        
    $output = shell_exec($cmd);
    error_log(date("y-m-d H:i:s").": After python call -resetuserpw_ajax.php() resetuserpw_ajax() function called!\n", 3, "/var/log/chaniqphp.log");
    
    $outputdata = json_decode($output, true);
    ksort($outputdata);
    
    $rtnOutput = [];
    
    foreach ($outputdata as $key => $value){
        file_put_contents("/var/log/chaniqphp.log", "shell_exec() Return - Key: " . $key . " Value: " . $value . "\n" , FILE_APPEND);
        array_push($rtnOutput, (string)$value);
    }
    
    foreach ($rtnOutput as $value){
        file_put_contents("/var/log/chaniqphp.log", "String Returned: " . $value . "\n" , FILE_APPEND);
    }
    
    $json = json_encode($rtnOutput);

    echo $json;
}
?>