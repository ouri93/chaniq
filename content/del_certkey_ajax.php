<?php
require_once(__DIR__ . '/../utility/chaniqLogger.php');

session_start();
file_put_contents("/var/log/chaniqphp.log", "del_certkey_ajax.php UN: " .$_SESSION['username'] . " Role: " . $_SESSION['role'] . " LoggedIn: " . $_SESSION['loggedin'] . "\n", FILE_APPEND);
if ($_SESSION['loggedin'] != true){
    session_unset();
    session_destroy();
    #file_put_contents("/var/log/chaniqphp.log", "del_certkey_ajax.php redirection to login page!!\n", FILE_APPEND);
    $logger->info("del_certkey_ajax.php redirection to login page!!");
    header('Location: ../login.php');
}
//Admin Content - Visible if the logged-in user has admin role
if ($_SESSION['role'] == 'guest'){
    header('Location: contentbase.php');
}

//if(isset($_POST)==TRUE && empty($_POST)==FALSE):
// If you put variables to save data from POST, it wont work. I moved the part under del_certkey_ajax()
#error_log(date("y-m-d H:i:s").": del_certkey_ajax.php() - callBack function php has been called\n", 3, "/var/log/chaniqphp.log");
$logger->info("del_certkey_ajax.php() - callBack function php has been called");
// Call del_certkey_ajax() by echo statement
if (isset($_POST['jsonData'])){
    $jsonParam = json_decode($_POST['jsonData']);
    $certData = json_decode($_POST['certData']);
    #file_put_contents("/var/log/chaniqphp.log", "del_certkey_ajax.php File: " . $jsonParam->PhpFileName ."\n", FILE_APPEND);
    $logger->info("del_certkey_ajax.php File: " . $jsonParam->PhpFileName);
    
    // Call the fuction del_certkey_ajax()
    echo ($jsonParam->PhpFileName)($jsonParam, $certData, $logger);
}
else{
    
    echo "Required Post parameter is missing";
}

//'PhpFileName':'', 'DevIP':'', 'P_name':'', 'P_part':'' 
function del_certkey_ajax($jsonParam, $certData, $logger) {
    #file_put_contents("/var/log/chaniqphp.log", "del_certkey_ajax() called\n", FILE_APPEND);
    $logger->info("del_certkey_ajax() called");
    $devIP = $jsonParam->DevIP;

    #file_put_contents("/var/log/chaniqphp.log", "del_certkey_ajax() Device IP: " . $devIP . "\n", FILE_APPEND);
    $logger->info("del_certkey_ajax() Device IP: " . $devIP);
    
    // JSON encoded data passed to Python must be loaded by json.loads() in Python code 
    // e.g. parsedData = json.loads(certData) then use parsedData[idx] format to access data
    // Ref: https://stackoverflow.com/questions/46866730/sending-array-from-php-to-python-and-then-parse-in-python/46866791
    $CertData = json_encode($certData);
    
    $cmd = '/usr/bin/python /var/www/chaniq/py/del_certkey_ajax.py ' . escapeshellarg($devIP) . ' ' . escapeshellarg($CertData);
        
    $output = shell_exec($cmd);
    #error_log(date("y-m-d H:i:s").": After python call -del_certkey_ajax.php() del_certkey_ajax() function called!\n", 3, "/var/log/chaniqphp.log");
    $logger->info("After python call -del_certkey_ajax.php() del_certkey_ajax() function called!");
    
    /*
    $outputdata = json_decode($output, true);
    ksort($outputdata);
    */
    
    echo $output;
}
?>