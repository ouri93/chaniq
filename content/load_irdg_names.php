<?php
require_once(__DIR__ . '/../utility/chaniqLogger.php');
    session_start();
    #file_put_contents("/var/log/chaniqphp.log", "load_irdg_names.php UN: " .$_SESSION['username'] . " Role: " . $_SESSION['role'] . " LoggedIn: " . $_SESSION['loggedin'] . "\n", FILE_APPEND);
    $logger->info("load_irdg_names.php UN: " .$_SESSION['username'] . " Role: " . $_SESSION['role'] . " LoggedIn: " . $_SESSION['loggedin']);
    if ($_SESSION['loggedin'] != true){
        session_unset();
        session_destroy();
        #file_put_contents("/var/log/chaniqphp.log", "load_irdg_names.php redirection to login page!!\n", FILE_APPEND);
        $logger->info("load_irdg_names.php redirection to login page!!");
        header('Location: ../login.php');
    }
    //Admin Content - Visible if the logged-in user has admin role
    if ($_SESSION['role'] == 'guest'){
        header('Location: contentbase.php');
    }

    //if(isset($_POST)==TRUE && empty($_POST)==FALSE):
    // If you put variables to save data from POST, it wont work. I moved the part under load_irdg_names()

    #error_log(date("y-m-d H:i:s").": load_irdg_names.php() - callBack function php has been called\n", 3, "/var/log/chaniqphp.log");
    $logger->info("load_irdg_names.php() - callBack function php has been called");
    
    // Call load_irdg_names() by echo statement
    if (isset($_POST['jsonIrData'])){
        $irData = json_decode($_POST['jsonIrData']);
        #file_put_contents("/var/log/chaniqphp.log", "load_irdg_names() phpFile: " . $irData->phpFileName ."\n", FILE_APPEND);
        $logger->info("load_irdg_names() phpFile: " . $irData->phpFileName);
        
        // Call the fuction load_irdg_names()
        echo ($irData->phpFileName)($irData, $logger);
    }
    else{

        echo "Required POST Data is not defined!";
    }
    
    
    function load_irdg_names($irData, $logger) {
        //'phpFileName' 'DevIP' 'IrType' 'IrDgPart'
        #file_put_contents("/var/log/chaniqphp.log", "load_irdg_names() called\n", FILE_APPEND);
        $logger->info("load_irdg_names() called");
            
        $phpFileName = $irData->phpFileName;
        $irDevIp = $irData->DevIP;
        $irType = $irData->IrType;
        $irDgPart = $irData->IrDgPart;
        
        #file_put_contents("/var/log/chaniqphp.log", "load_irdg_names() Device IP: " . $irDevIp . " Partition name: " .$irDgPart. " iRule or Data Group: " .$irType. "\n", FILE_APPEND);
        $logger->info("load_irdg_names() Device IP: " . $irDevIp . " Partition name: " .$irDgPart. " iRule or Data Group: " .$irType);
        
        $cmd = '/usr/bin/python /var/www/chaniq/py/load_irdg_names.py '. escapeshellarg($irDevIp) .' '. escapeshellarg($irType) .' '. escapeshellarg($irDgPart);

        #file_put_contents("/var/log/chaniqphp.log", "Python CMD output: " . $cmd . "\n", FILE_APPEND);
        $logger->info("Python CMD output: " . $cmd);
        
        $output = shell_exec($cmd);
        #file_put_contents("/var/log/chaniqphp.log", "After python call - load_irdg_names.php() -> load_irdg_names() function called!\n", FILE_APPEND);
        $logger->info("After python call - load_irdg_names.php() -> load_irdg_names() function called!");
        
        $outputdata = json_decode($output, true);
        
        $rtnOutput = explode("|", $outputdata);
        
        foreach ($rtnOutput as $value){
            #file_put_contents("/var/log/chaniqphp.log", "String Returned: " . $value . "\n", FILE_APPEND);
            $logger->info("String Returned: " . $value);
        }

        $json = json_encode($rtnOutput);
        
        echo $json;
    }
?>