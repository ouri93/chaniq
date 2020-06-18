<?php
require_once(__DIR__ . '/../utility/chaniqLogger.php');
session_start();
#file_put_contents("/var/log/chaniqphp.log", "del_vs_ajax.php UN: " .$_SESSION['username'] . " Role: " . $_SESSION['role'] . " LoggedIn: " . $_SESSION['loggedin'] . "\n", FILE_APPEND);
$logger->info("del_vs_ajax.php UN: " .$_SESSION['username'] . " Role: " . $_SESSION['role'] . " LoggedIn: " . $_SESSION['loggedin']);
if ($_SESSION['loggedin'] != true){
    session_unset();
    session_destroy();
    #file_put_contents("/var/log/chaniqphp.log", "del_vs_ajax.php redirection to login page!!\n", FILE_APPEND);
    $logger->info("del_vs_ajax.php redirection to login page!!");
    header('Location: ../login.php');
}
//Admin Content - Visible if the logged-in user has admin role
if ($_SESSION['role'] == 'guest'){
    header('Location: contentbase.php');
}

//if(isset($_POST)==TRUE && empty($_POST)==FALSE):
// If you put variables to save data from POST, it wont work. I moved the part under del_vs_ajax()

#error_log(date("y-m-d H:i:s").": del_vs_ajax.php() - callBack function php has been called\n", 3, "/var/log/chaniqphp.log");
$logger->info("del_vs_ajax.php() - callBack function php has been called");

// Call del_vs_ajax() by echo statement
if (isset($_POST['jsonVsData'])){
    $vsData = json_decode($_POST['jsonVsData']);
    #file_put_contents("/var/log/chaniqphp.log", "del_vs_ajax() phpFile: " . $vsData->PhpFileName ."\n", FILE_APPEND);
    $logger->info("del_vs_ajax() phpFile: " . $vsData->PhpFileName);
    
    // Call the fuction del_vs_ajax()
    echo ($vsData->PhpFileName)($vsData, $logger);
}
else{
    
    echo "Required POST parameter is missing";
}

//'PhpFileName' 'DevIP' 'Vs_name' 'Partition'
function del_vs_ajax($vsData, $logger) {
    #file_put_contents("/var/log/chaniqphp.log", "del_vs_ajax() called\n", FILE_APPEND);
    $logger->info("del_vs_ajax() called");
    
    $phpFileName = $vsData->PhpFileName;
    $vsDevIp = $vsData->DevIP;
    $vs_name = $vsData->Vs_name;
    $partition = $vsData->Partition;
    
    #file_put_contents("/var/log/chaniqphp.log", "del_vs_ajax() Device IP: " . $vsDevIp . " VS Name: " .$vs_name. " Partition: " .$partition. "\n", FILE_APPEND);
    $logger->info("del_vs_ajax() Device IP: " . $vsDevIp . " VS Name: " .$vs_name. " Partition: " .$partition);
    
    $cmd = '/usr/bin/python /var/www/chaniq/py/del_vs_ajax.py '. escapeshellarg($vsDevIp) .' '. escapeshellarg($vs_name) .' '. escapeshellarg($partition);
    
    $output = shell_exec($cmd);
    #error_log(date("y-m-d H:i:s").": After python call -del_vs_ajax.php() del_vs_ajax() function called!\n", 3, "/var/log/chaniqphp.log");
    $logger->info("After python call -del_vs_ajax.php() del_vs_ajax() function called!");
    
    $outputdata = json_decode($output, true);
    ksort($outputdata);
    
    $rtnOutput = [];
    
    foreach ($outputdata as $key => $value){
        #file_put_contents("/var/log/chaniqphp.log", "shell_exec() Return - Key: " . $key . " Value: " . $value . "\n" , FILE_APPEND);
        $logger->info("shell_exec() Return - Key: " . $key . " Value: " . $value);
        array_push($rtnOutput, (string)$value);
    }
    
    foreach ($rtnOutput as $value){
        #file_put_contents("/var/log/chaniqphp.log", "String Returned: " . $value . "\n", FILE_APPEND);
        $logger->info("String Returned: " . $value);
    }
    
    $json = json_encode($rtnOutput);
    
    echo $json;
}
?>