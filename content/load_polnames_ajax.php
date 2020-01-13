<?php
session_start();
file_put_contents("/var/log/chaniqphp.log", "load_polnames_ajax.php UN: " .$_SESSION['username'] . " Role: " . $_SESSION['role'] . " LoggedIn: " . $_SESSION['loggedin'] . "\n", FILE_APPEND);
if ($_SESSION['loggedin'] != true){
    session_unset();
    session_destroy();file_put_contents("/var/log/chaniqphp.log", "load_polnames_ajax.php redirection to login page!!\n", FILE_APPEND);        
    header('Location: ../login.php');
}
//Admin Content - Visible if the logged-in user has admin role
if ($_SESSION['role'] == 'guest'){
    header('Location: contentbase.php');
}

//if(isset($_POST)==TRUE && empty($_POST)==FALSE):
// If you put variables to save data from POST, it wont work. I moved the part under load_polnames_ajax()
error_log(date("y-m-d H:i:s").": load_polnames_ajax.php() - callBack function php has been called\n", 3, "/var/log/chaniqphp.log");
// Call load_polnames_ajax() by echo statement
if (isset($_POST['jsonData'])){
    $jsonParam = json_decode($_POST['jsonData']);
    file_put_contents("/var/log/chaniqphp.log", "load_polnames_ajax.php File: " . $jsonParam->PhpFileName ."\n", FILE_APPEND);
    
    // Call the fuction load_polnames_ajax()
    echo ($jsonParam->PhpFileName)($jsonParam);
}
else{
    
    echo "Required Post parameter is missing";
}

//'PhpFileName':'', 'DevIP':'', 'P_name':'', 'P_part':'' 
function load_polnames_ajax($jsonParam) {
    file_put_contents("/var/log/chaniqphp.log", "load_polnames_ajax() called\n", FILE_APPEND);
    
    $devIP = $jsonParam->DevIP;

    file_put_contents("/var/log/chaniqphp.log", "load_polnames_ajax() 
          Device IP: " . $devIP . "\n", FILE_APPEND);
    
    $cmd = '/usr/bin/python /var/www/chaniq/py/load_polnames_ajax.py ' . escapeshellarg($devIP);
        
    $output = shell_exec($cmd);
    error_log(date("y-m-d H:i:s").": After python call -load_polnames_ajax.php() load_polnames_ajax() function called!\n", 3, "/var/log/chaniqphp.log");
    
    /*
    $outputdata = json_decode($output, true);
    ksort($outputdata);
    */
    
    echo $output;
}
?>