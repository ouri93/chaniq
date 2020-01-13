<?php
    session_start();
    file_put_contents("/var/log/chaniqphp.log", "new_pool_build.php UN: " .$_SESSION['username'] . " Role: " . $_SESSION['role'] . " LoggedIn: " . $_SESSION['loggedin'] . "\n", FILE_APPEND);
    if ($_SESSION['loggedin'] != true){
        session_unset();
        session_destroy();
        file_put_contents("/var/log/chaniqphp.log", "new_pool_build.php redirection to login page!!\n", FILE_APPEND);
        header('Location: ../login.php');
    }
    //Admin Content - Visible if the logged-in user has admin role
    if ($_SESSION['role'] == 'guest'){
        header('Location: contentbase.php');
    }

    //if(isset($_POST)==TRUE && empty($_POST)==FALSE):
    // If you put variables to save data from POST, it wont work. I moved the part under new_pool_build()

    error_log(date("y-m-d H:i:s").": new_pool_build.php() - callBack function php has been called\n", 3, "/var/log/chaniqphp.log");
    //file_put_contents("/var/log/chaniqphp.log", "POST param phpFileName: " . $phpFileName . " devIP: " .$devIp ."VS name: ". $pVsName . "VsPort: " . $pVsPort . "Pool Mon: " . $pMon , FILE_APPEND);
    
    // Call new_pool_build() by echo statement
    echo $_POST['phpFile']();
    
    function new_pool_build() {
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
        $pmPoolMemberRatio = $_POST['PmPoolMemberRatio'];
        $pmPoolMemberMon = $_POST['PmPoolMemberMon'];
        $pmPriGroup = $_POST['PmPrigroup'];
        
        file_put_contents("/var/log/chaniqphp.log", "new_pool_build() Device IP: " . $devIp . "\n", FILE_APPEND);
        /*
        if(isset($_POST['DevIp']))
        {
            $bigipIP = $_POST['DevIP'];
            file_put_contents("/var/log/chaniqphp.log", "new_pool_build() Device IP: " . $bigipIP, FILE_APPEND);
        }
        else{
            file_put_contents("/var/log/chaniqphp.log", "Device IP is not found: " . $bigipIP, FILE_APPEND);
            return "Error: Device IP address is not determined!";
        }
        */
        
        $cmd = '/usr/bin/python /var/www/chaniq/py/new_pool_build.py '.$devIp.' '. $pVsName.' '. $pVsPort.' '. $pEnv.' '. $pMon.' '. $pLBMethod.' '. $pPriGroup.' '. $pPriGroupLessThan.' '. $pmPoolMemberName .' '. $pmPoolMemberIp .' '. $pmPoolMemberPort .' '. $pmPoolMemberRatio . ' '. $pmPoolMemberMon .' '. $pmPriGroup;
        //$cmd = '/usr/bin/python /var/www/chaniq/py/new_pool_build.py '.$devIp.' '. $pVsName.' '. $pVsPort.' '. $pEnv.' '. $pMon.' '. $pLBMethod;
        
        $output = shell_exec($cmd);
        error_log(date("y-m-d H:i:s").": After python call -new_pool_build.php() new_pool_build() function called!\n", 3, "/var/log/chaniqphp.log");
        
        $outputdata = json_decode($output, true);
        ksort($outputdata);
        
        $rtnOutput = [];
        
        foreach ($outputdata as $key => $value){
            file_put_contents("/var/log/chaniqphp.log", "shell_exec() Return - Key: " . $key . " Value: " . $value . "\n", FILE_APPEND);
            array_push($rtnOutput, (string)$value);
        }
        
        foreach ($rtnOutput as $value){
            file_put_contents("/var/log/chaniqphp.log", "Strint Return: " . $value . "\n" , FILE_APPEND);
        }
        
        $json = json_encode($rtnOutput);
        
        echo $json;
    }
?>