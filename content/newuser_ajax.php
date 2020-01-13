<?php
if ($_SESSION['loggedin'] != true){
    session_unset();
    session_destroy();
    file_put_contents("/var/log/chaniqphp.log", "newuser_ajax.php redirection to login page!!\n", FILE_APPEND);
    header('Location: ../login.php');
}
//Admin Content - Visible if the logged-in user has admin role
if ($_SESSION['role'] == 'guest'){
    header('Location: contentbase.php');
}

include('../utility/utility.php');

//if(isset($_POST)==TRUE && empty($_POST)==FALSE):
// If you put variables to save data from POST, it wont work. I moved the part under newuser_ajax()
error_log(date("y-m-d H:i:s").": newuser_ajax.php() - callBack function php has been called\n", 3, "/var/log/chaniqphp.log");
// Call newuser_ajax() by echo statement
if (isset($_POST['jsonPassData'])){
    $passData = json_decode($_POST['jsonPassData']);
    file_put_contents("/var/log/chaniqphp.log", "newuser_ajax.php File: " . $passData->PhpFileName ."\n", FILE_APPEND);
    
    // Call the fuction newuser_ajax()
    echo ($passData->PhpFileName)($passData);
}
else{
    
    echo "Required Post parameter is missing";
}

//'PhpFileName':'', 'Username', 'UserRole', 'Pass1':'' 
function newuser_ajax($passData) {
    file_put_contents("/var/log/chaniqphp.log", "newuser_ajax() called\n", FILE_APPEND);
    
    $un = $passData->UserName;
    $userrole = $passData->UserRole;
    $pass1 = $passData->Pass1;
    $db_ip = parse_ini_sec_val('DB_CONFIG', "DB_IP");

    file_put_contents("/var/log/chaniqphp.log", "newuser_ajax() DB IP: " . $db_ip . "\n", FILE_APPEND);
    
    $cmd = '/usr/bin/python /var/www/chaniq/py/newuser_ajax.py ' . escapeshellarg($db_ip) .' '. escapeshellarg($un) .' '. escapeshellarg($userrole) .' '. escapeshellarg($pass1);
    
        
    $output = shell_exec($cmd);
    error_log(date("y-m-d H:i:s").": After python call -newuser_ajax.php() newuser_ajax() function called!\n", 3, "/var/log/chaniqphp.log");
    
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