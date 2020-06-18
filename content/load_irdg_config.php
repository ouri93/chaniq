<?php
require_once(__DIR__ . '/../utility/chaniqLogger.php');
session_start();
#file_put_contents("/var/log/chaniqphp.log", "load_irdg_config.php UN: " .$_SESSION['username'] . " Role: " . $_SESSION['role'] . " LoggedIn: " . $_SESSION['loggedin'] . "\n", FILE_APPEND);
$logger->info("load_irdg_config.php UN: " .$_SESSION['username'] . " Role: " . $_SESSION['role'] . " LoggedIn: " . $_SESSION['loggedin']);
    if ($_SESSION['loggedin'] != true){
        session_unset();
        session_destroy();
        #file_put_contents("/var/log/chaniqphp.log", "load_irdg_config.php redirection to login page!!\n", FILE_APPEND);
        $logger->info("load_irdg_config.php redirection to login page!!");
        header('Location: ../login.php');
    }
    //Admin Content - Visible if the logged-in user has admin role
    if ($_SESSION['role'] == 'guest'){
        header('Location: contentbase.php');
    }

    //if(isset($_POST)==TRUE && empty($_POST)==FALSE):
    // If you put variables to save data from POST, it wont work. I moved the part under load_irdg_config()

    #error_log(date("y-m-d H:i:s").": load_irdg_config.php() - callBack function php has been called\n", 3, "/var/log/chaniqphp.log");
    $logger->info("load_irdg_config.php() - callBack function php has been called");
    
    // Call load_irdg_config() by echo statement
    if (isset($_POST['jsonIrData'])){
        $irData = json_decode($_POST['jsonIrData']);
        #file_put_contents("/var/log/chaniqphp.log", "load_irdg_config() phpFile: " . $irData->phpFileName ."\n", FILE_APPEND);
        $logger->info("load_irdg_config() phpFile: " . $irData->phpFileName);
        
        // Call the fuction load_irdg_config()
        echo ($irData->phpFileName)($irData, $logger);
    }
    else{

        echo "Required POST Data is not defined!";
    }
    
    
    function load_irdg_config($irData, $logger) {
        //'phpFileName' 'DevIP' 'IrType' 'IrDgPart'
        #file_put_contents("/var/log/chaniqphp.log", "load_irdg_config() called\n", FILE_APPEND);
        $logger->info("load_irdg_config() called");
        // 'phpFileName' 'DevIP' 'IrType' 'IrDgName'
        $phpFileName = $irData->phpFileName;
        $irDevIp = $irData->DevIP;
        $irType = $irData->IrType;
        $irDgName = $irData->IrDgName;
        
        #file_put_contents("/var/log/chaniqphp.log", "load_irdg_config() Device IP: " . $irDevIp . " iRule or DG name: " .$irDgName. " iRule or Data Group: " .$irType. "\n", FILE_APPEND);
        $logger->info("load_irdg_config() Device IP: " . $irDevIp . " iRule or DG name: " .$irDgName. " iRule or Data Group: " .$irType);
        
        $cmd = '/usr/bin/python /var/www/chaniq/py/load_irdg_config.py '. escapeshellarg($irDevIp) .' '. escapeshellarg($irType) .' '. escapeshellarg($irDgName);

        #file_put_contents("/var/log/chaniqphp.log", "Python CMD output: " . $cmd . "\n", FILE_APPEND);
        $logger->info("Python CMD output: " . $cmd);
        
        $output = shell_exec($cmd);
        #file_put_contents("/var/log/chaniqphp.log", "After python call - load_irdg_config.php() -> load_irdg_config() function called!\n", FILE_APPEND);
        $logger->info("After python call - load_irdg_config.php() -> load_irdg_config() function called!");
        
        /* Decode the returned JSON data and convert it into associative array (true) */
        $outputdata = json_decode($output, true);
        
        // Logging code
        if ($irType == "iRule"){
            #file_put_contents("/var/log/chaniqphp.log", "iRule Return Values at load_irdg_config()\n", FILE_APPEND);
            #file_put_contents("/var/log/chaniqphp.log", "Name: " . $outputdata['name'] . "\n", FILE_APPEND);
            #file_put_contents("/var/log/chaniqphp.log", "iRule Code: " . $outputdata['apiAnonymous'] . "\n", FILE_APPEND);
            $logger->info("iRule Return Values at load_irdg_config()");
            $logger->info("Name: " . $outputdata['name']);
            $logger->info("iRule Code: " . $outputdata['apiAnonymous']);
        }
        elseif ($irType == "Data Group") {
            #file_put_contents("/var/log/chaniqphp.log", "Data Group Return Values at load_irdg_config()\n", FILE_APPEND);
            #file_put_contents("/var/log/chaniqphp.log", "Name: " . $outputdata['name'] . "\n", FILE_APPEND);
            #file_put_contents("/var/log/chaniqphp.log", "Data Group Type: " . $outputdata['type'] . "\n", FILE_APPEND);
            $logger->info("Data Group Return Values at load_irdg_config()");
            $logger->info("Name: " . $outputdata['name']);
            $logger->info("Data Group Type: " . $outputdata['type']);
            foreach ($outputdata['records'] as $value) {
                #file_put_contents("/var/log/chaniqphp.log", "Data: " . $value["data"]. " Value: " .$value["name"]. "\n", FILE_APPEND);
                $logger->info("Data: " . $value["data"]. " Value: " .$value["name"]);
            }
            
        }
        
        $json = json_encode($outputdata);
        
        echo $output;
    }
?>