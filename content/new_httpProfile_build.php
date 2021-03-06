<?php
require_once(__DIR__ . '/../utility/chaniqLogger.php');
    session_start();
    #file_put_contents("/var/log/chaniqphp.log", "new_httpProfile_build.php UN: " .$_SESSION['username'] . " Role: " . $_SESSION['role'] . " LoggedIn: " . $_SESSION['loggedin'] . "\n", FILE_APPEND);
    $logger->info("new_httpProfile_build.php UN: " .$_SESSION['username'] . " Role: " . $_SESSION['role'] . " LoggedIn: " . $_SESSION['loggedin']);
    if ($_SESSION['loggedin'] != true){
        session_unset();
        session_destroy();
        #file_put_contents("/var/log/chaniqphp.log", "new_httpProfile_build.php redirection to login page!!\n", FILE_APPEND);
        $logger->info("new_httpProfile_build.php redirection to login page!!");
        header('Location: ../login.php');
    }
    //Admin Content - Visible if the logged-in user has admin role
    if ($_SESSION['role'] == 'guest'){
        header('Location: contentbase.php');
    }

    //if(isset($_POST)==TRUE && empty($_POST)==FALSE):
    // If you put variables to save data from POST, it wont work. I moved the part under new_certkey_build()

    #error_log(date("y-m-d H:i:s").": new_httpProfile_build.php() - callBack function php has been called\n", 3, "/var/log/chaniqphp.log");
    $logger->info("new_httpProfile_build.php() - callBack function php has been called");
    
    // Call new_httpProfile_build() by echo statement
    if (isset($_POST['newProfileBuild'])){
        $profileData = json_decode($_POST['newProfileBuild']);
        #file_put_contents("/var/log/chaniqphp.log", "new_httpProfile_build() phpFile: " . $profileData->phpFileName ."\n", FILE_APPEND);
        $logger->info("new_httpProfile_build() phpFile: " . $profileData->phpFileName);
        
        // Call the fuction new_httpProfile_build()
        echo ($profileData->phpFileName)($profileData, $logger);
    }
    else{

        echo "AJAX call failed due to missing POST data";
    }
    
    //'phpFileName', 'DevIP', 'name', 'proxyType', 'defaultsFrom', 'basicAuthRealm', 'fallbackHost', 'fallbackStatusCodes', 'headerErase'
    //'headerInsert','requestChunking', 'responseChunkimg','insertXforwardedFor', 'serverAgentName', 'dnsResolver'
    function new_httpProfile_build($profileData, $logger) {
        #file_put_contents("/var/log/chaniqphp.log", "new_httpProfile_build() called\n", FILE_APPEND);
        $logger->info("new_httpProfile_build() called");
            
        $phpFileName = $profileData->phpFileName;
        $prfDevIp = $profileData->DevIP;
        $prfName = $profileData->name;
        $prfDplyOrChg = $profileData->dplyOrChg;
        $prfPxyType = $profileData->proxyType;
        if ($prfPxyType == 'explicit') {
            $prfPxyType =  $prfPxyType . ":" . $profileData->dnsResolver;
            #file_put_contents("/var/log/chaniqphp.log", "Explicit Proxy Type: " . $prfPxyType . "\n" , FILE_APPEND);
            $logger->info("Explicit Proxy Type: " . $prfPxyType);
        }
        $prfDftFrom = $profileData->defaultsFrom;
        $prfBscAuthRealm = $profileData->basicAuthRealm;
        $prfFallbackHost = $profileData->fallbackHost;
        $prfFallbackStsCode = $profileData->fallbackStatusCodes;
        $prfReqChunking = $profileData->requestChunking;
        $prfRespChunking = $profileData->responseChunking;
        $prfHdrErase = $profileData->headerErase;
        $prfHdrInsert = $profileData->headerInsert;
        $prfInstXFF = $profileData->insertXforwardedFor;
        $prfSrvAgtName = $profileData->serverAgentName;
        $prfDnsResolver = '';
        
        #file_put_contents("/var/log/chaniqphp.log", "new_httpProfile_build() Device IP: " . $prfDevIp . " Profile Name: " .$prfName. " Deploy or Change: " . $prfDplyOrChg . " Proxy Type: " .$prfPxyType." Defaults-From: " .$prfDftFrom." Basic Auth Realm: " .$prfBscAuthRealm." Fallback Host: " .$prfFallbackHost." FallbackHost Status: " .$prfFallbackStsCode. " Request Chunking: " .$prfReqChunking. " Response Chunking: " .$prfRespChunking. " Insert XFF: " .$prfInstXFF." Server Agent Name: " .$prfSrvAgtName."\n", FILE_APPEND);
        $logger->info("new_httpProfile_build() Device IP: " . $prfDevIp . " Profile Name: " .$prfName. " Deploy or Change: " . $prfDplyOrChg . " Proxy Type: " .$prfPxyType." Defaults-From: " .$prfDftFrom." Basic Auth Realm: " .$prfBscAuthRealm." Fallback Host: " .$prfFallbackHost." FallbackHost Status: " .$prfFallbackStsCode. " Request Chunking: " .$prfReqChunking. " Response Chunking: " .$prfRespChunking. " Insert XFF: " .$prfInstXFF." Server Agent Name: " .$prfSrvAgtName);
        
        $cmd = '/usr/bin/python /var/www/chaniq/py/new_httpProfile_build.py '. escapeshellarg($prfDevIp) .' '. escapeshellarg($prfName) .' '. escapeshellarg($prfDplyOrChg) .' '. escapeshellarg($prfPxyType) .' '. escapeshellarg($prfDftFrom) .' '. escapeshellarg($prfBscAuthRealm) .' '. escapeshellarg($prfFallbackHost) .' '. escapeshellarg($prfFallbackStsCode) .' '. escapeshellarg($prfHdrErase) .' '. escapeshellarg($prfHdrInsert) .' '. escapeshellarg($prfReqChunking) . ' ' . escapeshellarg($prfRespChunking).' '. escapeshellarg($prfInstXFF) .' '. escapeshellarg($prfSrvAgtName);
        
        $output = shell_exec($cmd);
        #error_log(date("y-m-d H:i:s").": After python call - new_httpProfile_build.php() new_httpProfile_build() function called!\n", 3, "/var/log/chaniqphp.log");
        $logger->info("After python call - new_httpProfile_build.php() new_httpProfile_build() function called!");

        #file_put_contents("/var/log/chaniqphp.log", "String Returned: " . $output , FILE_APPEND);
        $logger->info("String Returned: " . $output);
        
        if ($output == ''){
            $rtnOutput = ["Python shell_exec() returns null"];
            echo json_encode($rtnOutput);
        }
        else {
            $outputdata = json_decode($output, true);
            ksort($outputdata);
            
            $rtnOutput = [];
            
            foreach ($outputdata as $key => $value){
                #file_put_contents("/var/log/chaniqphp.log", "shell_exec() Return - Key: " . $key . " Value: " . $value , FILE_APPEND);
                $logger->info("shell_exec() Return - Key: " . $key . " Value: " . $value);
                array_push($rtnOutput, (string)$value);
            }
            
            foreach ($rtnOutput as $value){
                #file_put_contents("/var/log/chaniqphp.log", "String Returned: " . $value , FILE_APPEND);
                $logger->info("String Returned: " . $value);
            }
            
            $json = json_encode($rtnOutput);
            
            echo $json;
        }
    }
?>