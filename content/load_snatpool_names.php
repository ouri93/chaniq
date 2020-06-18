<?php
require_once(__DIR__ . '/../utility/chaniqLogger.php');
session_start();
#file_put_contents("/var/log/chaniqphp.log", "load_snatpool_names.php UN: " .$_SESSION['username'] . " Role: " . $_SESSION['role'] . " LoggedIn: " . $_SESSION['loggedin'] . "\n", FILE_APPEND);
$logger->info("load_snatpool_names.php UN: " .$_SESSION['username'] . " Role: " . $_SESSION['role'] . " LoggedIn: " . $_SESSION['loggedin']);
if ($_SESSION['loggedin'] != true){
    session_unset();
    session_destroy();
    #file_put_contents("/var/log/chaniqphp.log", "load_snatpool_names.php redirection to login page!!\n", FILE_APPEND);
    $logger->info("load_snatpool_names.php redirection to login page!!");
    header('Location: ../login.php');
}
//Admin Content - Visible if the logged-in user has admin role
if ($_SESSION['role'] == 'guest'){
    header('Location: contentbase.php');
}

//if(isset($_POST)==TRUE && empty($_POST)==FALSE):
// If you put variables to save data from POST, it wont work. I moved the part under load_snatpool_names()

#error_log(date("y-m-d H:i:s").": load_snatpool_names.php() - callBack function php has been called\n", 3, "/var/log/chaniqphp.log");
$logger->info("load_snatpool_names.php() - callBack function php has been called");

// Call load_snatpool_names() by echo statement
if (isset($_POST['jsonData'])){
    $snatData = json_decode($_POST['jsonData']);
    #file_put_contents("/var/log/chaniqphp.log", "load_snatpool_names() phpFile: " . $snatData->PhpFileName ."\n", FILE_APPEND);
    $logger->info("load_snatpool_names() phpFile: " . $snatData->PhpFileName);
    
    // Call the fuction load_snatpool_names()
    echo ($snatData->PhpFileName)($snatData, $logger);
}
else{
    
    echo "Required POST Data is not defined!";
}

function load_snatpool_names($snatData, $logger) {
    #file_put_contents("/var/log/chaniqphp.log", "load_snatpool_names() called\n", FILE_APPEND);
    $logger->info("load_snatpool_names() called");
    
    $phpFileName = $snatData->PhpFileName;
    $DevIp = $snatData->DevIP;
    
    #file_put_contents("/var/log/chaniqphp.log", "load_snatpool_names() Device IP: " . $DevIp . "\n", FILE_APPEND);
    $logger->info("load_snatpool_names() Device IP: " . $DevIp);
    
    $cmd = '/usr/bin/python /var/www/chaniq/py/load_snatpool_names.py '. escapeshellarg($DevIp);
    
    $output = shell_exec($cmd);
    #error_log(date("y-m-d H:i:s").": After python call -load_snatpool_names.php() load_snatpool_names() function called!\n", 3, "/var/log/chaniqphp.log");
    $logger->info("After python call -load_snatpool_names.php() load_snatpool_names() function called!");
    
    $outputdata = json_decode($output, true);
    ksort($outputdata);
    
    foreach ($outputdata as $value){
        #file_put_contents("/var/log/chaniqphp.log", "String Returned: " . $value , FILE_APPEND);
        $logger->info("String Returned: " . $value);
    }
    
    $json = json_encode($outputdata);
    
    echo $json;
}
?>