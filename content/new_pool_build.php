<?php

//if(isset($_POST)==TRUE && empty($_POST)==FALSE):
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

    error_log(date("y-m-d H:i:s").": new_pool_build.php() - callBack function php has been called\n", 3, "/var/www/chaniq/log/chaniqphp.log");

    
    // Call new_pool_build() by echo statement
    echo $_POST['phpFile']();
    
    function new_pool_build() {
        error_log(date("y-m-d H:i:s").": new_pool_build.php() new_pool_build() function called!\n", 3, "/var/www/chaniq/log/chaniqphp.log");
        
        if(isset($_POST['devIp']))
        {
            //$bigipIP = json_decode($_POST['DevIP']);
            $bigipIP = $_POST['DevIP'];
            //error_log(date("y-m-d H:i:s").": get_pool_monitors() - Device IP sent over POST\n", 3, "/var/www/chaniq/log/chaniqphp.log");
            file_put_contents("/var/www/chaniq/log/chaniqphp.log", "new_pool_build() Device IP: " . $bigipIP, FILE_APPEND);
        }
        
        //.$active_ltm.$vs_dnsname. $vs_port. $vs_env. $vs_poolmon.$pool_membername.$pool_memberip.$pool_memberport.$pool_membermon));
        
        //$cmd = '/usr/bin/python /var/www/chaniq/py/new_pool_build.py '.$devIp.' '. $pVsName.' '. $pVsPort.' '. $pEnv.' '. $pMon.' '. $pLBMethod.' '. $pPriGroup.' '. $pPriGroupLessThan.' '. escapeshellarg(json_encode($pmPoolMemberName)).' '. escapeshellarg(json_encode($pmPoolMemberIp)).' '. escapeshellarg(json_encode($pmPoolMemberPort)).' '. escapeshellarg(json_encode($pmPoolMemberMon)).' '. escapeshellarg(json_encode($pmPriGroup));
        $cmd = '/usr/bin/python /var/www/chaniq/py/new_pool_build.py '.$devIp.' '. $pVsName.' '. $pVsPort.' '. $pEnv.' '. $pMon.' '. $pLBMethod;
        
        $output = shell_exec($cmd);
        error_log(date("y-m-d H:i:s").": After python call -new_pool_build.php() new_pool_build() function called!\n", 3, "/var/www/chaniq/log/chaniqphp.log");
        $outputdata = json_decode($output, true);
        
        echo $outputdata;
    }
?>