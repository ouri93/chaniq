<?php

    //if(isset($_POST)==TRUE && empty($_POST)==FALSE):
    // If you put variables to save data from POST, it wont work. I moved the part under new_monitor_build()

    error_log(date("y-m-d H:i:s").": new_monitor_build.php() - callBack function php has been called\n", 3, "/var/log/chaniqphp.log");
    //file_put_contents("/var/log/chaniqphp.log", "POST param phpFileName: " . $phpFileName . " devIP: " .$devIp ."VS name: ". $pVsName . "VsPort: " . $pVsPort . "Pool Mon: " . $pMon , FILE_APPEND);
    
    // Call new_monitor_build() by echo statement
    file_put_contents("/var/log/chaniqphp.log", "new_monitor_build() phpFile: " . $_POST['phpFile'], FILE_APPEND);
    //echo $_POST['phpFile']();
    
    
    function new_monitor_build() {
        /*
        $phpFileName = $_POST['phpFile'];
        $devIp = $_POST['DevIP'];
        $pVsName = $_POST['PVsName'];
        $pVsPort = $_POST['PVsPort'];
        $pMon = $_POST['PMon'];
        $pEnv = $_POST['PEnv'];
        $pLBMethod = $_POST['PLBMethod'];
        $pPriGroup = $_POST['PPriGroup'];
        $pPriGroupLessThan = $_POST['PPriGroupLessThan'];
        $pmPoolMemberName = $_POST['PmPoolMemberNmae'];
        $pmPoolMemberIp = $_POST['PmPoolMemberIp'];
        $pmPoolMemberPort = $_POST['PmPoolMemberPort'];
        $pmPoolMemberMon = $_POST['PmPoolMemberMon'];
        $pmPriGroup = $_POST['PmPrigroup'];
        
        file_put_contents("/var/log/chaniqphp.log", "new_monitor_build() Device IP: " . $devIp, FILE_APPEND);
        
        $cmd = '/usr/bin/python /var/www/chaniq/py/new_monitor_build.py '.$devIp.' '. $pVsName.' '. $pVsPort.' '. $pEnv.' '. $pMon.' '. $pLBMethod.' '. $pPriGroup.' '. $pPriGroupLessThan.' '. $pmPoolMemberName .' '. $pmPoolMemberIp .' '. $pmPoolMemberPort .' '. $pmPoolMemberMon .' '. $pmPriGroup;
        //$cmd = '/usr/bin/python /var/www/chaniq/py/new_monitor_build.py '.$devIp.' '. $pVsName.' '. $pVsPort.' '. $pEnv.' '. $pMon.' '. $pLBMethod;
        
        $output = shell_exec($cmd);
        error_log(date("y-m-d H:i:s").": After python call -new_monitor_build.php() new_monitor_build() function called!\n", 3, "/var/log/chaniqphp.log");
        
        $outputdata = json_decode($output, true);
        ksort($outputdata);
        
        $rtnOutput = [];
        
        foreach ($outputdata as $key => $value){
            file_put_contents("/var/log/chaniqphp.log", "shell_exec() Return - Key: " . $key . " Value: " . $value , FILE_APPEND);
            array_push($rtnOutput, (string)$value);
        }
        
        foreach ($rtnOutput as $value){
            file_put_contents("/var/log/chaniqphp.log", "Strint Return: " . $value , FILE_APPEND);
        }
        
        $json = json_encode($rtnOutput);
        
        echo $json;
        */
    }
?>