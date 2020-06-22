<?php
require_once(__DIR__ . '/../utility/chaniqLogger.php');
session_start();
#file_put_contents("/var/log/chaniqphp.log", "new_ssl_build() UN: " .$_SESSION['username'] . " Role: " . $_SESSION['role'] . " LoggedIn: " . $_SESSION['loggedin'] . "\n", FILE_APPEND);
$logger->info("new_ssl_build() UN: " .$_SESSION['username'] . " Role: " . $_SESSION['role'] . " LoggedIn: " . $_SESSION['loggedin']);
if ($_SESSION['loggedin'] != true){
    session_unset();
    session_destroy();
    #file_put_contents("/var/log/chaniqphp.log", "new_ssl_build.php redirection to login page!!\n", FILE_APPEND);
    $logger->info("new_ssl_build.php redirection to login page!!");
    header('Location: ../login.php');
}
//Admin Content - Visible if the logged-in user has admin role
if ($_SESSION['role'] == 'guest'){
    header('Location: contentbase.php');
}

//if(isset($_POST)==TRUE && empty($_POST)==FALSE):
// If you put variables to save data from POST, it wont work. I moved the part under new_ssl_build()

#error_log(date("y-m-d H:i:s").": new_ssl_build.php - callBack function php has been called\n", 3, "/var/log/chaniqphp.log");
$logger->info("new_ssl_build.php - callBack function php has been called");

// Call new_ssl_build() by echo statement
if (isset($_POST['jsonData'])){
    $sslData = json_decode($_POST['jsonData']);
    #file_put_contents("/var/log/chaniqphp.log", "new_ssl_build() phpFile: " . $sslData->phpFileName ."\n", FILE_APPEND);
    $logger->info("new_ssl_build() phpFile: " . $sslData->phpFileName);
    
    // Call the fuction new_ssl_build()
    echo ($sslData->phpFileName)($sslData, $logger);
}
else{
    
    echo "AJAX call failed";
}

// 'phpFileName':'', 'sslDevIP':'', 'issuerType':'', 'sslName':'', 'sslCN':'', 'sslSelfLifetime':'', 'sslCAChallengePW':'', 'sslDvz':'', 
// 'sslOG':'', 'sslLoc':'', 'sslState':'', 'sslCountry':'', 'sslEmail':'', 'sslSAN':'', 'sslKeyType':'', 'sslKeySize':''
function new_ssl_build($sslData, $logger) {
    #file_put_contents("/var/log/chaniqphp.log", "new_ssl_build() called\n", FILE_APPEND);
    $logger->info("new_ssl_build() called");
    $phpFileName = $sslData->phpFileName;
    $sslDevIP = $sslData->sslDevIP;
    $issuerType = $sslData->issuerType;
    $sslName = $sslData->sslName;
    $sslCN = $sslData->sslCN;
    $sslSelfLifetime = $sslData->sslSelfLifetime;
    $sslCAChallengePW = $sslData->sslCAChallengePW;
    $sslDvz = $sslData->sslDvz;
    $sslOG = $sslData->sslOG;
    $sslLoc = $sslData->sslLoc;
    $sslState = $sslData->sslState;
    $sslCountry = $sslData->sslCountry;
    $sslEmail = $sslData->sslEmail;
    $sslSAN = $sslData->sslSAN;
    $sslKeyType = $sslData->sslKeyType;
    $sslKeySize = $sslData->sslKeySize;

    
    #file_put_contents("/var/log/chaniqphp.log", "new_ssl_build() Device IP: " . $sslDevIP . " SSL Type: " .$issuerType. " SSL CN: " .$sslCN. " SSL PW: " .$sslCAChallengePW. " SSL Division: " .$sslDvz.  " SSL Locality: " .$sslLoc. " SSL Organization: " .$sslOG. " SSL State: " .$sslState. " SSL Key Type: " .$sslKeyType."\n", FILE_APPEND);
    $logger->info("new_ssl_build() Device IP: " . $sslDevIP . " SSL Type: " .$issuerType. " SSL CN: " .$sslCN. " SSL PW: " .$sslCAChallengePW. " SSL Division: " .$sslDvz.  " SSL Locality: " .$sslLoc. " SSL Organization: " .$sslOG. " SSL State: " .$sslState. " SSL Key Type: " .$sslKeyType);
    
    $cmd = '/usr/bin/python /var/www/chaniq/py/new_ssl_build.py '. escapeshellarg($sslDevIP) .' '. escapeshellarg($issuerType) .' '. escapeshellarg($sslName) .' '. escapeshellarg($sslCN) .' '. escapeshellarg($sslSelfLifetime) .' '. escapeshellarg($sslCAChallengePW) .' '. escapeshellarg($sslDvz).' '. escapeshellarg($sslOG) .' '. escapeshellarg($sslLoc) .' '.escapeshellarg($sslState) .' '.escapeshellarg($sslCountry) .' '.escapeshellarg($sslEmail) .' '.escapeshellarg($sslSAN) .' '. escapeshellarg($sslKeyType) .' '.escapeshellarg($sslKeySize);
    
    $output = shell_exec($cmd);
    #error_log(date("y-m-d H:i:s").": After python call - new_ssl_build() function called!\n", 3, "/var/log/chaniqphp.log");
    $logger->info("After python call - new_ssl_build() function called!");
    
    $outputdata = json_decode($output, true);
    ksort($outputdata);
    
    $rtnOutput = [];
    
    foreach ($outputdata as $key => $value){
        #file_put_contents("/var/log/chaniqphp.log", "shell_exec() Return - Key: " . $key . " Value: " . $value . "\n" , FILE_APPEND);
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