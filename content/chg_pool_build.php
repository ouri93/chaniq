<?php
session_start();
file_put_contents("/var/log/chaniqphp.log", "chg_pool_build.php UN: " .$_SESSION['username'] . " Role: " . $_SESSION['role'] . " LoggedIn: " . $_SESSION['loggedin'] . "\n", FILE_APPEND);
if ($_SESSION['loggedin'] != true){
    session_unset();
    session_destroy();
    file_put_contents("/var/log/chaniqphp.log", "chg_pool_build.php redirection to login page!!\n", FILE_APPEND);
    header('Location: ../login.php');
}
if ($_SESSION['role'] == 'guest'){
    header('Location: contentbase.php');
}

//if(isset($_POST)==TRUE && empty($_POST)==FALSE):
// If you put variables to save data from POST, it wont work. I moved the part under chg_pool_build()
error_log(date("y-m-d H:i:s").": chg_pool_build.php() - callBack function php has been called\n", 3, "/var/log/chaniqphp.log");
// Call chg_pool_build() by echo statement
if (isset($_POST['jsonPoolData'])){
    $poolData = json_decode($_POST['jsonPoolData']);
    file_put_contents("/var/log/chaniqphp.log", "chg_pool_build.php File: " . $poolData->PhpFileName ."\n", FILE_APPEND);
    
    // Call the fuction chg_pool_build()
    echo ($poolData->PhpFileName)($poolData);
}
else{
    
    echo "Ajax call failed as jsonPoolData POST data is not defined during AJAX call";
}

//'PhpFileName' 'DevIP' 'P_name' 'P_mon' 'P_LB' 'P_priGroup' 'P_lessthan' 'PM_names'
//'PM_ips' 'PM_ratios' 'PM_mons' 'PM_priGroup'
function chg_pool_build($poolData) {
    file_put_contents("/var/log/chaniqphp.log", "chg_pool_build() called\n", FILE_APPEND);
    
    $phpFileName = $poolData->PhpFileName;
    $pDevIp = $poolData->DevIP;
    $pName = $poolData->P_name;
    $pPart = $poolData->P_part;
    $pMon = $poolData->P_mon;
    $pLB = $poolData->P_LB;
    $pPriGroup = $poolData->P_priGroup;
    $pLessthan = $poolData->P_lessthan;
    $pmNames = $poolData->PM_names;
    $pmIPs = $poolData->PM_ips;
    //$pmPorts = $poolData->PM_ports;
    $pmRatios = $poolData->PM_ratios;
    $pmMons = $poolData->PM_mons;
    $pmPriGroup = $poolData->PM_priGroup;
    
    file_put_contents("/var/log/chaniqphp.log", "chg_pool_build() 
          Device IP: " . $pDevIp . 
        " Pool Name: " . $pName . 
        " Pool Mon: " . $pMon .  
        " Pool Partition: " . $pPart .
        " Pool LB: " . $pLB .
        " Pool Priority Group: " . $pPriGroup .
        " Pool Priority Lessthan: " . $pLessthan . 
        " Pool Member Names: " . $pmNames . 
        " Pool Member IPs: " . $pmIPs .
        " Pool Member Ratios: " . $pmRatios .
        " Pool Member Monitors: " . $pmMons .
        " Pool Member Priority Group: " . $pmPriGroup ."\n", FILE_APPEND);
    
    $cmd = '/usr/bin/python /var/www/chaniq/py/chg_pool_build.py '
        . escapeshellarg($pDevIp) .' '. escapeshellarg($pName) .' '. escapeshellarg($pPart) .' '
        . escapeshellarg($pMon) .' '. escapeshellarg($pLB) .' '. escapeshellarg($pPriGroup) .' '
        . escapeshellarg($pLessthan) .' '. escapeshellarg($pmNames).' '. escapeshellarg($pmIPs) .' '
        . escapeshellarg($pmRatios) .' '. escapeshellarg($pmMons) .' '. escapeshellarg($pmPriGroup);
    
        
    $output = shell_exec($cmd);
    error_log(date("y-m-d H:i:s").": After python call -chg_pool_build.php() chg_pool_build() function called!\n", 3, "/var/log/chaniqphp.log");
    
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