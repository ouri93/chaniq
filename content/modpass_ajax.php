<?php
require_once(__DIR__ . '/../utility/chaniqLogger.php');
session_start();
#file_put_contents("/var/log/chaniqphp.log", "modpass_ajax.php UN: " .$_SESSION['username'] . " Role: " . $_SESSION['role'] . " LoggedIn: " . $_SESSION['loggedin'] . "\n", FILE_APPEND);
$logger->info("modpass_ajax.php UN: " .$_SESSION['username'] . " Role: " . $_SESSION['role'] . " LoggedIn: " . $_SESSION['loggedin']);
if ($_SESSION['loggedin'] != true){
    session_unset();
    session_destroy();
    #file_put_contents("/var/log/chaniqphp.log", "modpass_ajax.php redirection to login page!!\n", FILE_APPEND);
    $logger->info("modpass_ajax.php redirection to login page!!");
    header('Location: ../login.php');
}
//Admin Content - Visible if the logged-in user has admin role
if ($_SESSION['role'] == 'guest'){
    header('Location: contentbase.php');
}

include('../utility/utility.php');

//if(isset($_POST)==TRUE && empty($_POST)==FALSE):
// If you put variables to save data from POST, it wont work. I moved the part under modpass_ajax()
#error_log(date("y-m-d H:i:s").": modpass_ajax.php() - callBack function php has been called\n", 3, "/var/log/chaniqphp.log");
$logger->info("modpass_ajax.php() - callBack function php has been called");
// Call modpass_ajax() by echo statement
if (isset($_POST['jsonPassData'])){
    $passData = json_decode($_POST['jsonPassData']);
    #file_put_contents("/var/log/chaniqphp.log", "modpass_ajax.php File: " . $passData->PhpFileName ."\n", FILE_APPEND);
    $logger->info("modpass_ajax.php File: " . $passData->PhpFileName);
    
    // Call the fuction modpass_ajax()
    echo ($passData->PhpFileName)($passData, $logger);
}
else{
    
    echo "Required Post parameter is missing";
}

//'PhpFileName':'', 'Pass1':'', 'BigipType':'' 
function modpass_ajax($passData, $logger) {
    #file_put_contents("/var/log/chaniqphp.log", "modpass_ajax() called\n", FILE_APPEND);
    $logger->info("modpass_ajax() called");
    
    $curpass = $passData->CurPass;
    $newpass = $passData->NewPass;
    $bigip_type = $passData->BigipType;
    $db_ip = parse_ini_sec_val('DB_CONFIG', "DB_IP");

    #file_put_contents("/var/log/chaniqphp.log", "modpass_ajax() DB IP: " . $db_ip . "\n", FILE_APPEND);
    $logger->info("modpass_ajax() DB IP: " . $db_ip);
    
    $cmd = '/usr/bin/python /var/www/chaniq/py/modpass_ajax.py ' . escapeshellarg($db_ip) .' '. escapeshellarg($curpass) .' '. escapeshellarg($newpass) .' '. escapeshellarg($bigip_type);
    
        
    $output = shell_exec($cmd);
    #error_log(date("y-m-d H:i:s").": After python call -modpass_ajax.php() modpass_ajax() function called!\n", 3, "/var/log/chaniqphp.log");
    $logger->info("After python call -modpass_ajax.php() modpass_ajax() function called!");
    
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