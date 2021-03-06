<?php
require_once(__DIR__ . '/../utility/chaniqLogger.php');
    session_start();
    #file_put_contents("/var/log/chaniqphp.log", "update_irdg_config.php UN: " .$_SESSION['username'] . " Role: " . $_SESSION['role'] . " LoggedIn: " . $_SESSION['loggedin'] . "\n", FILE_APPEND);
    $logger->info("update_irdg_config.php UN: " .$_SESSION['username'] . " Role: " . $_SESSION['role'] . " LoggedIn: " . $_SESSION['loggedin']);
    if ($_SESSION['loggedin'] != true){
        session_unset();
        session_destroy();
        #file_put_contents("/var/log/chaniqphp.log", "update_irdg_config.php redirection to login page!!\n", FILE_APPEND);
        $logger->info("update_irdg_config.php redirection to login page!!");
        header('Location: ../login.php');
    }
    //Admin Content - Visible if the logged-in user has admin role
    if ($_SESSION['role'] == 'guest'){
        header('Location: contentbase.php');
    }


    //if(isset($_POST)==TRUE && empty($_POST)==FALSE):
    // If you put variables to save data from POST, it wont work. I moved the part under update_irdg_config()

    #error_log(date("y-m-d H:i:s").": update_irdg_config.php() - callBack function php has been called\n", 3, "/var/log/chaniqphp.log");
    $logger->info("update_irdg_config.php() - callBack function php has been called");
    
    // Call update_irdg_config() by echo statement
    if (isset($_POST['jsonIrData'])){
        $irData = json_decode($_POST['jsonIrData']);
        #file_put_contents("/var/log/chaniqphp.log", "update_irdg_config() phpFile: " . $irData->phpFileName ."\n", FILE_APPEND);
        $logger->info("update_irdg_config() phpFile: " . $irData->phpFileName);
        
        // Call the fuction update_irdg_config()
        echo ($irData->phpFileName)($irData, $logger);
    }
    else{

        echo "Required POST Data is not defined!";
    }
    
    
    function update_irdg_config($irData, $logger) {
        //'phpFileName' 'DevIP' 'IrDgName' 'IrType' 'IrCode' 'IrDgType' 'IrDgData'
        #file_put_contents("/var/log/chaniqphp.log", "update_irdg_config() called\n", FILE_APPEND);
        $logger->info("update_irdg_config() called");
            
        $phpFileName = $irData->phpFileName;
        $irDevIp = $irData->DevIP;
        $irDgName = $irData->IrDgName;
        $irType = $irData->IrType;
        $irCode = $irData->IrCode;
        $irDgType = $irData->IrDgType;
        $irDgData =  $irData->IrDgData;
        
        #file_put_contents("/var/log/chaniqphp.log", "update_irdg_config() Device IP: " . $irDevIp . " iRule/DataGroup name: " .$irDgName. " Config Type: " .$irType." Irule Code: " .$irCode." DataGroup Type: " .$irDgType." DG Data: " .$irDgData . "\n", FILE_APPEND);
        $logger->info("update_irdg_config() Device IP: " . $irDevIp . " iRule/DataGroup name: " .$irDgName. " Config Type: " .$irType." Irule Code: " .$irCode." DataGroup Type: " .$irDgType." DG Data: " .$irDgData);
        
        $cmd = '/usr/bin/python /var/www/chaniq/py/update_irdg_config.py '. escapeshellarg($irDevIp) .' '. escapeshellarg($irDgName) .' '. escapeshellarg($irType) .' '. escapeshellarg($irCode) .' '. escapeshellarg($irDgType) .' '. escapeshellarg($irDgData);

        #file_put_contents("/var/log/chaniqphp.log", "Python CMD output: " . $cmd . "\n", FILE_APPEND);
        $logger->info("Python CMD output: " . $cmd);
        
        $output = shell_exec($cmd);
        #file_put_contents("/var/log/chaniqphp.log", "After python call - update_irdg_config.php() -> update_irdg_config() function called!\n", FILE_APPEND);
        $logger->info("After python call - update_irdg_config.php() -> update_irdg_config() function called!");
        
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