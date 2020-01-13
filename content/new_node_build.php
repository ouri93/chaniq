<?php
session_start();
file_put_contents("/var/log/chaniqphp.log", "new_node_build.php UN: " .$_SESSION['username'] . " Role: " . $_SESSION['role'] . " LoggedIn: " . $_SESSION['loggedin'] . "\n", FILE_APPEND);
if ($_SESSION['loggedin'] != true){
    session_unset();
    session_destroy();
    file_put_contents("/var/log/chaniqphp.log", "new_node_build.php redirection to login page!!\n", FILE_APPEND);
    header('Location: ../login.php');
}
//Admin Content - Visible if the logged-in user has admin role
if ($_SESSION['role'] == 'guest'){
    header('Location: contentbase.php');
}

//if(isset($_POST)==TRUE && empty($_POST)==FALSE):
// If you put variables to save data from POST, it wont work. I moved the part under new_node_build()

error_log(date("y-m-d H:i:s").": new_node_build.php() - callBack function php has been called\n", 3, "/var/log/chaniqphp.log");

// Call new_node_build() by echo statement
if (isset($_POST['jsonNodeData'])){
    $nodeData = json_decode($_POST['jsonNodeData']);
    file_put_contents("/var/log/chaniqphp.log", "new_node_build() phpFile: " . $nodeData->PhpFileName ."\n", FILE_APPEND);
    
    // Call the fuction new_node_build()
    echo ($nodeData->PhpFileName)($nodeData);
}
else{
    
    echo "AJAX call failed";
}


function new_node_build($nodeData) {
    file_put_contents("/var/log/chaniqphp.log", "new_node_build() called\n", FILE_APPEND);
    
    $phpFileName = $nodeData->PhpFileName;
    $nodeDevIp = $nodeData->DevIP;
    $nodeMbrNames = $nodeData->Pool_membernames;
    $nodeMbrIps = $nodeData->Pool_memberips;
    
    file_put_contents("/var/log/chaniqphp.log", "new_node_build() Device IP: " . $nodeDevIp . " Node names: " .$nodeMbrNames. " Node IPs: " .$nodeMbrIps."\n", FILE_APPEND);
    
    $cmd = '/usr/bin/python /var/www/chaniq/py/new_node_build.py '. escapeshellarg($nodeDevIp) .' '. escapeshellarg($nodeMbrNames) .' '. escapeshellarg($nodeMbrIps);
    
    $output = shell_exec($cmd);
    error_log(date("y-m-d H:i:s").": After python call -new_node_build.php() new_node_build() function called!\n", 3, "/var/log/chaniqphp.log");
    
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