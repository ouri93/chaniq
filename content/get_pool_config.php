<?php
session_start();
file_put_contents("/var/log/chaniqphp.log", "get_pool_config.php UN: " .$_SESSION['username'] . " Role: " . $_SESSION['role'] . " LoggedIn: " . $_SESSION['loggedin'] . "\n", FILE_APPEND);
if ($_SESSION['loggedin'] != true){
    session_unset();
    session_destroy();
    file_put_contents("/var/log/chaniqphp.log", "get_pool_config.php redirection to login page!!\n", FILE_APPEND);
    header('Location: ../login.php');
}
//Admin Content - Visible if the logged-in user has admin role
if ($_SESSION['role'] == 'guest'){
    header('Location: contentbase.php');
}


//if(isset($_POST)==TRUE && empty($_POST)==FALSE):
// If you put variables to save data from POST, it wont work. I moved the part under get_pool_config()
error_log(date("y-m-d H:i:s").": get_pool_config.php() - callBack function php has been called\n", 3, "/var/log/chaniqphp.log");
// Call get_pool_config() by echo statement
if (isset($_POST['jsonPoolData'])){
    $poolData = json_decode($_POST['jsonPoolData']);
    file_put_contents("/var/log/chaniqphp.log", "get_pool_config() phpFile: " . $poolData->PhpFileName ."\n", FILE_APPEND);
    
    // Call the fuction get_pool_config()
    echo ($poolData->PhpFileName)($poolData);
}
else{
    
    echo "AJAX call failed";
}
function get_pool_config($poolData) {
    file_put_contents("/var/log/chaniqphp.log", "get_pool_config() called\n", FILE_APPEND);
    
    // Data Format: {'PhpFileName':'', 'DevIP':'', 'PoolName':'', 'Partition':''}
    $phpFileName = $poolData->PhpFileName;
    $poolDevIp = $poolData->DevIP;
    $poolName = $poolData->PoolName;
    $poolPartition = $poolData->Partition;
    
    file_put_contents("/var/log/chaniqphp.log", "get_pool_config() \nDevice IP: " . $poolDevIp . "\nPool Name: " .$poolName. "\nPartition: " . $poolPartition . "\n", FILE_APPEND);
    
    $cmd = '/usr/bin/python /var/www/chaniq/py/get_pool_config.py '. escapeshellarg($poolDevIp) .' '. escapeshellarg($poolName) .' '. escapeshellarg($poolPartition);
    
    $output = shell_exec($cmd);
    error_log(date("y-m-d H:i:s").": After python call -get_pool_config.php() get_pool_config() function called!\n", 3, "/var/log/chaniqphp.log");
    error_log(date("y-m-d H:i:s").": Returned output: " . $output . "\n", 3, "/var/log/chaniqphp.log");
    
    $json = json_encode($output);
    echo $json;
}
?>