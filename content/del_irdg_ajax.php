<?php
require_once(__DIR__ . '/../utility/chaniqLogger.php');

    session_start();
    #file_put_contents("/var/log/chaniqphp.log", "del_irdg_ajax.php UN: " .$_SESSION['username'] . " Role: " . $_SESSION['role'] . " LoggedIn: " . $_SESSION['loggedin'] . "\n", FILE_APPEND);
    $logger->info("del_irdg_ajax.php UN: " .$_SESSION['username'] . " Role: " . $_SESSION['role'] . " LoggedIn: " . $_SESSION['loggedin']);
    if ($_SESSION['loggedin'] != true){
        session_unset();
        session_destroy();
        #file_put_contents("/var/log/chaniqphp.log", "del_irdg_ajax.php redirection to login page!!\n", FILE_APPEND);
        $logger->info("del_irdg_ajax.php redirection to login page!!");
        header('Location: ../login.php');
    }
    //Admin Content - Visible if the logged-in user has admin role
    if ($_SESSION['role'] == 'guest'){
        header('Location: contentbase.php');
    }


    //if(isset($_POST)==TRUE && empty($_POST)==FALSE):
    // If you put variables to save data from POST, it wont work. I moved the part under del_irdg_ajax()

    #error_log(date("y-m-d H:i:s").": del_irdg_ajax.php() - callBack function php has been called\n", 3, "/var/log/chaniqphp.log");
    $logger->info("del_irdg_ajax.php() - callBack function php has been called");
    
    // Call del_irdg_ajax() by echo statement
    if (isset($_POST['jsonData'])){
        $irData = json_decode($_POST['jsonData']);
        #file_put_contents("/var/log/chaniqphp.log", "del_irdg_ajax() phpFile: " . $irData->phpFileName ."\n", FILE_APPEND);
        $logger->info("del_irdg_ajax() phpFile: " . $irData->phpFileName);
        
        // Call the fuction del_irdg_ajax()
        echo ($irData->phpFileName)($irData, $logger);
    }
    else{

        echo "Required POST Data is not defined!";
    }
    
    
    function del_irdg_ajax($irData, $logger) {
        //'phpFileName':'', 'DevIP':'', 'IrDgName':'', 'IrType':'', 'IrDgType':''
        #file_put_contents("/var/log/chaniqphp.log", "del_irdg_ajax() called\n", FILE_APPEND);
        $logger->info("del_irdg_ajax() called");
            
        $phpFileName = $irData->phpFileName;
        $irDevIp = $irData->DevIP;
        $irDgName = $irData->IrDgName;
        $irOrDg = $irData->IrType;
        $dgType = $irData->IrDgType;
        
        #file_put_contents("/var/log/chaniqphp.log", "del_irdg_ajax() Device IP: " . $irDevIp . " iRule/DataGroup name: " .$irDgName. " Config Type: " .$irOrDg. " DataGroup Type: " .$dgType. "\n", FILE_APPEND);
        $logger->info("del_irdg_ajax() Device IP: " . $irDevIp . " iRule/DataGroup name: " .$irDgName. " Config Type: " .$irOrDg. " DataGroup Type: " .$dgType);
        
        $cmd = '/usr/bin/python2 /var/www/chaniq/py/del_irdg_ajax.py '. escapeshellarg($irDevIp) .' '. escapeshellarg($irDgName) .' '. escapeshellarg($irOrDg) .' '. escapeshellarg($dgType);

        #file_put_contents("/var/log/chaniqphp.log", "Python CMD output: " . $cmd . "\n", FILE_APPEND);
        $logger->info("Python CMD output: " . $cmd);
        
        $output = shell_exec($cmd);
        #file_put_contents("/var/log/chaniqphp.log", "After python call - del_irdg_ajax.php() -> del_irdg_ajax() function called!\n", FILE_APPEND);
        $logger->info("After python call - del_irdg_ajax.php() -> del_irdg_ajax() function called!");
        
        $outputdata = json_decode($output, true);
        
        if (!ksort($outputdata)){
            #file_put_contents("/var/log/chaniqphp.log", "Ksort returned False!\n", FILE_APPEND);
            $logger->info("Ksort returned False!");
        };
        
        $rtnOutput = [];
        
        foreach ($outputdata as $key => $value){
            #file_put_contents("/var/log/chaniqphp.log", "shell_exec() Return - Key: " . $key . " Value: " . $value . "\n", FILE_APPEND);
            $logger->info("shell_exec() Return - Key: " . $key . " Value: " . $value);
            array_push($rtnOutput, (string)$value);
        }
        
        foreach ($rtnOutput as $value){
            #file_put_contents("/var/log/chaniqphp.log", "String Returned: " . $value . "\n", FILE_APPEND);
            $logger->info("String Returned: " . $value);
        }
        
        $json = json_encode($rtnOutput);
        
        echo $json;
    }
?>