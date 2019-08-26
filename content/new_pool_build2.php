<?php

//if(isset($_POST)==TRUE && empty($_POST)==FALSE):
// If you put variables to save data from POST, it wont work. I moved the part under new_pool_build2()

error_log(date("y-m-d H:i:s").": new_pool_build2.php() - callBack function php has been called\n", 3, "/var/log/chaniqphp.log");

// Call new_pool_build2() by echo statement
if (isset($_POST['jsonPoolData'])){
    $poolData = json_decode($_POST['jsonPoolData']);
    file_put_contents("/var/log/chaniqphp.log", "new_pool_build2() phpFile: " . $poolData->PhpFileName ."\n", FILE_APPEND);
    
    // Call the fuction new_pool_build2()
    echo ($poolData->PhpFileName)($poolData);
}
else{
    
    echo "AJAX call failed";
}

function new_pool_build2($poolData) {
    file_put_contents("/var/log/chaniqphp.log", "new_pool_build2() called\n", FILE_APPEND);
    
    $phpFileName = $poolData->PhpFileName;
    $poolDevIp = $poolData->DevIP;
    $poolName = $poolData->Vs_poolname;
    $poolPort = $poolData->Vs_port;
    $poolEnv = $poolData->Vs_env;
    $poolMon = $poolData->Vs_poolmon;
    $poolMbrNames = $poolData->Pool_membernames;
    $poolMbrIps = $poolData->Pool_memberips;
    $poolMbrPorts = $poolData->Pool_memberports;
    $poolMbrMons = $poolData->Pool_membermons;
    
    file_put_contents("/var/log/chaniqphp.log", "new_pool_build2() Device IP: " . $poolDevIp . " Pool Name: " .$poolName. " Pool Port: " .$poolPort. " Pool Env: " .$poolEnv. " Pool Mon: " .$poolMon.  " Node names: " .$poolMbrNames. " Node IPs: " .$poolMbrIps. " Node Ports: " .$poolMbrPorts. " Node Mons: " .$poolMbrMons."\n", FILE_APPEND);
    
    $cmd = '/usr/bin/python /var/www/chaniq/py/new_pool_build2.py '. escapeshellarg($poolDevIp) .' '. escapeshellarg($poolName) .' '. escapeshellarg($poolPort) .' '. escapeshellarg($poolEnv) .' '. escapeshellarg($poolMon) .' '. escapeshellarg($poolMbrNames) .' '. escapeshellarg($poolMbrIps).' '. escapeshellarg($poolMbrPorts) .' '. escapeshellarg($poolMbrMons);
    
    $output = shell_exec($cmd);
    error_log(date("y-m-d H:i:s").": After python call -new_pool_build2.php() new_pool_build2() function called!\n", 3, "/var/log/chaniqphp.log");
    
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