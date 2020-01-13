<?php
session_start();
file_put_contents("/var/log/chaniqphp.log", "new_snatpool_build.php UN: " .$_SESSION['username'] . " Role: " . $_SESSION['role'] . " LoggedIn: " . $_SESSION['loggedin'] . "\n", FILE_APPEND);
if ($_SESSION['loggedin'] != true){
    session_unset();
    session_destroy();
    file_put_contents("/var/log/chaniqphp.log", "new_snatpool_build.php redirection to login page!!\n", FILE_APPEND);
    header('Location: ../login.php');
}
//Admin Content - Visible if the logged-in user has admin role
if ($_SESSION['role'] == 'guest'){
    header('Location: contentbase.php');
}

//if(isset($_POST)==TRUE && empty($_POST)==FALSE):
// If you put variables to save data from POST, it wont work. I moved the part under new_snatpool_build()

error_log(date("y-m-d H:i:s").": new_snatpool_build.php() - callBack function php has been called\n", 3, "/var/log/chaniqphp.log");

// Call new_snatpool_build() by echo statement
if (isset($_POST['jsonSnatData'])){
    $snatData = json_decode($_POST['jsonSnatData']);
    file_put_contents("/var/log/chaniqphp.log", "new_snatpool_build() phpFile: " . $snatData->PhpFileName ."\n", FILE_APPEND);
    
    // Call the fuction new_snatpool_build()
    echo ($snatData->PhpFileName)($snatData);
}
else{
    
    echo "AJAX call failed";
}

function new_snatpool_build($snatData) {
    file_put_contents("/var/log/chaniqphp.log", "new_snatpool_build() called\n", FILE_APPEND);
    
    $phpFileName = $snatData->PhpFileName;
    $DevIp = $snatData->DevIP;
    $snat_name = $snatData->Snat_name;
    $snat_members = $snatData->Snat_members;

    
    file_put_contents("/var/log/chaniqphp.log", "new_snatpool_build() Device IP: " . $DevIp . " Snatpool Name: " .$snat_name. " Snatpool members: " .$snat_members."\n", FILE_APPEND);
    
    $cmd = '/usr/bin/python /var/www/chaniq/py/new_snatpool_build.py '. escapeshellarg($DevIp) .' '. escapeshellarg($snat_name) .' '. escapeshellarg($snat_members);
    
    $output = shell_exec($cmd);
    error_log(date("y-m-d H:i:s").": After python call -new_snatpool_build.php() new_snatpool_build() function called!\n", 3, "/var/log/chaniqphp.log");
    
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