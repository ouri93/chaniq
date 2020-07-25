<?php
require_once(__DIR__ . '/../utility/chaniqLogger.php');
session_start();
#file_put_contents("/var/log/chaniqphp.log", "resetuserpw_ajax.php UN: " .$_SESSION['username'] . " Role: " . $_SESSION['role'] . " LoggedIn: " . $_SESSION['loggedin'] . "\n", FILE_APPEND);
$logger->info("resetuserpw_ajax.php UN: " .$_SESSION['username'] . " Role: " . $_SESSION['role'] . " LoggedIn: " . $_SESSION['loggedin']);
if ($_SESSION['loggedin'] != true){
    session_unset();
    session_destroy();
    #file_put_contents("/var/log/chaniqphp.log", "resetuserpw_ajax.php redirection to login page!!\n", FILE_APPEND);
    $logger->info("resetuserpw_ajax.php redirection to login page!!");
    header('Location: ../login.php');
}
//Admin Content - Visible if the logged-in user has admin role
if ($_SESSION['role'] == 'guest'){
    header('Location: contentbase.php');
}

include('../utility/utility.php');

//if(isset($_POST)==TRUE && empty($_POST)==FALSE):
// If you put variables to save data from POST, it wont work. I moved the part under resetuserpw_ajax()
#error_log(date("y-m-d H:i:s").": resetuserpw_ajax.php() - callBack function php has been called\n", 3, "/var/log/chaniqphp.log");
$logger->info("resetuserpw_ajax.php() - callBack function php has been called");
// Call resetuserpw_ajax() by echo statement
if (isset($_POST['jsonPassData'])){
    $passData = json_decode($_POST['jsonPassData']);
    #file_put_contents("/var/log/chaniqphp.log", "resetuserpw_ajax.php File: " . $passData->PhpFileName ."\n", FILE_APPEND);
    $logger->info("resetuserpw_ajax.php File: " . $passData->PhpFileName);
    
    // Call the fuction resetuserpw_ajax()
    echo ($passData->PhpFileName)($passData, $logger);
}
else{
    
    echo "Required Post parameter is missing";
}

//'PhpFileName':'', 'UserName':'', 'UserRole':'', 'CurPass':'', 'NewPass':''
function resetuserpw_ajax($passData, $logger) {
    #file_put_contents("/var/log/chaniqphp.log", "resetuserpw_ajax() called\n", FILE_APPEND);
    $logger->info("resetuserpw_ajax() called");
    
    $un = $passData->UserName;
    $role = $passData->UserRole;
    $newpass = $passData->NewPass;
    $db_ip = parse_ini_sec_val('DB_CONFIG', "DB_IP");

    #file_put_contents("/var/log/chaniqphp.log", "resetuserpw_ajax() DB IP: " . $db_ip . "\n", FILE_APPEND);
    $logger->info("resetuserpw_ajax() DB IP: " . $db_ip);
    
    $cmd = '/usr/bin/python2 /var/www/chaniq/py/resetuserpw_ajax.py ' . escapeshellarg($db_ip) .' '. escapeshellarg($un) .' '. escapeshellarg($role) .' '. escapeshellarg($newpass);
    
        
    $output = shell_exec($cmd);
    #error_log(date("y-m-d H:i:s").": After python call -resetuserpw_ajax.php() resetuserpw_ajax() function called!\n", 3, "/var/log/chaniqphp.log");
    $logger->info("After python call -resetuserpw_ajax.php() resetuserpw_ajax() function called!");
    
    $outputdata = json_decode($output, true);
    ksort($outputdata);
    
    $rtnOutput = [];
    
    foreach ($outputdata as $key => $value){
        #file_put_contents("/var/log/chaniqphp.log", "shell_exec() Return - Key: " . $key . " Value: " . $value . "\n" , FILE_APPEND);
        $logger->info("shell_exec() Return - Key: " . $key . " Value: " . $value);
        array_push($rtnOutput, (string)$value);
    }
    
    foreach ($rtnOutput as $value){
        #file_put_contents("/var/log/chaniqphp.log", "String Returned: " . $value . "\n" , FILE_APPEND);
        $logger->info("String Returned: " . $value);
    }
    
    $json = json_encode($rtnOutput);

    echo $json;
}
?>