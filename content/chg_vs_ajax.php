<?php
require_once(__DIR__ . '/../utility/chaniqLogger.php');

session_start();
#file_put_contents("/var/log/chaniqphp.log", "chg_vs_ajax.php UN: " .$_SESSION['username'] . " Role: " . $_SESSION['role'] . " LoggedIn: " . $_SESSION['loggedin'] . "\n", FILE_APPEND);
$logger->info("chg_vs_ajax.php UN: " .$_SESSION['username'] . " Role: " . $_SESSION['role'] . " LoggedIn: " . $_SESSION['loggedin']);

if ($_SESSION['loggedin'] != true){
    session_unset();
    session_destroy();
    #file_put_contents("/var/log/chaniqphp.log", "chg_vs_ajax.php redirection to login page!!\n", FILE_APPEND);
    $logger->info("chg_vs_ajax.php redirection to login page!!");
    header('Location: ../login.php');
}
//Admin Content - Visible if the logged-in user has admin role
if ($_SESSION['role'] == 'guest'){
    header('Location: contentbase.php');
}

//if(isset($_POST)==TRUE && empty($_POST)==FALSE):
// If you put variables to save data from POST, it wont work. I moved the part under chg_vs_ajax()

#error_log(date("y-m-d H:i:s").": chg_vs_ajax.php() - callBack function php has been called\n", 3, "/var/log/chaniqphp.log");
$logger->info("chg_vs_ajax.php() - callBack function php has been called");

// Call chg_vs_ajax() by echo statement
if (isset($_POST['jsonVsData'])){
    $vsData = json_decode($_POST['jsonVsData']);
    #file_put_contents("/var/log/chaniqphp.log", "chg_vs_ajax() phpFile: " . $vsData->PhpFileName ."\n", FILE_APPEND);
    $logger->info("chg_vs_ajax() phpFile: " . $vsData->PhpFileName);
    
    // Call the fuction chg_vs_ajax()
    echo ($vsData->PhpFileName)($vsData, $logger);
}
else{
    
    echo "Required Post parameter is missing";
}

//active_ltm, vs_dnsname, vs_dest, vs_port, vs_desc, vs_tcpprofile, vs_persistence, vs_type, vs_httpprofile, vs_sslclient, vs_sslserver, vs_irule, vs_snatpool, vs_policy
function chg_vs_ajax($vsData, $logger) {
    #file_put_contents("/var/log/chaniqphp.log", "chg_vs_ajax() called\n", FILE_APPEND);
    $logger->info("chg_vs_ajax() called");
    
    $phpFileName = $vsData->PhpFileName;
    $vsDevIp = $vsData->DevIP;
    $vs_dnsname = $vsData->Vs_name;
    $vs_dest = $vsData->Vs_dest;
    $vs_port = $vsData->Vs_port;
    $vs_desc = $vsData->Vs_desc;
    $vs_tcpprofile = $vsData->Vs_tcpprf;
    $vs_persistence = $vsData->Vs_persist;
    $vs_type = $vsData->Vs_type;
    $vs_httpprofile = $vsData->Vs_httpprf;
    $vs_sslclient = $vsData->Vs_clisslprf;
    $vs_sslserver = $vsData->Vs_srvsslprf;
    $vs_irule = $vsData->Vs_irule;
    $vs_snatpool = $vsData->Vs_snatpool;
    $vs_policy = $vsData->Vs_policy;
    $vs_poolname = $vsData->Vs_poolname;
    
    #file_put_contents("/var/log/chaniqphp.log", "chg_vs_ajax() Device IP: " . $vsDevIp . " VS Name: " .$vs_dnsname. " VS Port: " .$vs_port. " TCP Profile: " .$vs_tcpprofile.  " VS Persist: " .$vs_persistence. " VS Type: " .$vs_type. " VS iRule: " .$vs_irule. " VS Poolname: " .$vs_poolname."\n", FILE_APPEND);
    $logger->info("chg_vs_ajax() Device IP: " . $vsDevIp . " VS Name: " .$vs_dnsname. " VS Port: " .$vs_port. " TCP Profile: " .$vs_tcpprofile.  " VS Persist: " .$vs_persistence. " VS Type: " .$vs_type. " VS iRule: " .$vs_irule. " VS Poolname: " .$vs_poolname);
    
    $cmd = '/usr/bin/python /var/www/chaniq/py/chg_vs_ajax.py '. escapeshellarg($vsDevIp) .' '. escapeshellarg($vs_dnsname) .' '. escapeshellarg($vs_dest) .' '. escapeshellarg($vs_port) .' '. escapeshellarg($vs_desc) .' '. escapeshellarg($vs_tcpprofile).' '. escapeshellarg($vs_persistence) .' '.escapeshellarg($vs_type) .' '.escapeshellarg($vs_httpprofile) .' '.escapeshellarg($vs_sslclient) .' '.escapeshellarg($vs_sslserver) .' '. escapeshellarg($vs_irule) .' '.escapeshellarg($vs_snatpool) .' '.escapeshellarg($vs_policy) .' '.escapeshellarg($vs_poolname);
    
    $output = shell_exec($cmd);
    #error_log(date("y-m-d H:i:s").": After python call -chg_vs_ajax.php() chg_vs_ajax() function called!\n", 3, "/var/log/chaniqphp.log");
    $logger->info("After python call -chg_vs_ajax.php() chg_vs_ajax() function called!");
    
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