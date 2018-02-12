<?php

    //if(isset($_POST)==TRUE && empty($_POST)==FALSE):
    // If you put variables to save data from POST, it wont work. I moved the part under new_certkey_build()

    error_log(date("y-m-d H:i:s").": new_Profile_build.php() - callBack function php has been called\n", 3, "/var/log/chaniqphp.log");
    
    // Call new_Profile_build() by echo statement
    if (isset($_POST['newProfileBuild'])){
        $profileData = json_decode($_POST['newProfileBuild']);
        file_put_contents("/var/log/chaniqphp.log", "new_Profile_build() phpFile: " . $profileData->phpFileName ."\n", FILE_APPEND);
        
        // Call the fuction new_Profile_build()
        echo ($profileData->phpFileName)($profileData);
    }
    else{

        echo "AJAX call failed";
    }
    
    //'phpFileName', 'DevIP', 'name', 'proxyType', 'defaultsFrom', 'basicAuthRealm', 'fallbackHost', 'fallbackStatusCodes', 'headerErase'
    //'headerInsert','requestChunking', 'responseChunkimg','insertXforwardedFor', 'serverAgentName', 'dnsResolver'
    function new_Profile_build($profileData) {
        file_put_contents("/var/log/chaniqphp.log", "new_Profile_build() called\n", FILE_APPEND);
        $cmd = '';
        
        $phpFileName = $profileData->phpFileName;
        $prfDevIp = $profileData->DevIP;
        $prfName = $profileData->name;
        $prfType = $profileData->PrfType;
        
        if ($prfType == 'DNS'){
            $prfDftFrom = $profileData->defaultsFrom;
            $prfHwValid = $profileData->enableHardwareQueryValidation;
            $prfHwRespCache = $profileData->enableHardwareResponseCache;
            $prfDnsExp = $profileData->enableDnsExpress;
            $prfGtm = $profileData->enableGtm;
            $prfUnhandledAct = $profileData->unhandledQueryAction;
            $prfUseBind = $profileData->useLocalBind;
            $prfZoneXfr = $profileData->processXfr;
            $prfDnsSecurity = $profileData->enableDnsFirewall;
            $prfRecursion = $profileData->processRd;

            file_put_contents("/var/log/chaniqphp.log", "new_DnsProfile_build() Device IP: " . $prfDevIp . " Profile Name: " .$prfName. " Defaults-From: " .$prfDftFrom." HW Query Validation: " .$prfHwValid." HW Response Cache: " .$prfHwRespCache." DNS Express: " .$prfDnsExp. " GSLB: " .$prfGtm. " Unhandled Query Action: " .$prfUnhandledAct." Use BIND: " .$prfUseBind." Zone Transfer: " .$prfZoneXfr."\n", FILE_APPEND);
            $cmd = '/usr/bin/python /var/www/chaniq/py/new_DnsProfile_build.py '. escapeshellarg($prfDevIp) .' '. escapeshellarg($prfName) .' '. escapeshellarg($prfDftFrom) .' '. escapeshellarg($prfHwValid) .' '. escapeshellarg($prfHwRespCache) .' '. escapeshellarg($prfDnsExp) .' '. escapeshellarg($prfGtm) .' '. escapeshellarg($prfUnhandledAct) .' '. escapeshellarg($prfUseBind) .' '. escapeshellarg($prfZoneXfr).' '. escapeshellarg($prfDnsSecurity) .' '. escapeshellarg($prfRecursion);
        }
        else if ($prfType == 'Cookie'){
            $prfPara1 = $profileData->defaultsFrom;
            $prfPara2 = $profileData->method;
            $prfPara3 = $profileData->cookieName;
            $prfPara4 = $profileData->httponly;
            $prfPara5 = $profileData->secure;
            $prfPara6 = $profileData->alwaysSend;
            $prfPara7 = $profileData->expiration;
            $prfPara8 = $profileData->overrideConnectionLimit;
            
            file_put_contents("/var/log/chaniqphp.log", "new_cookieProfile_build() Device IP: " . $prfDevIp . " Profile Name: " .$prfName. " Defaults-From: " .$prfPara1." Cookie Method: " .$prfPara2." Cookie Name: " .$prfPara3." Http Only: " .$prfPara4. " Secure Attribute: " .$prfPara5. " Always Send Cookie: " .$prfPara6." Expiration: " .$prfPara7." Override Connection Limit: " .$prfPara8."\n", FILE_APPEND);
            $cmd = '/usr/bin/python /var/www/chaniq/py/new_cookieProfile_build.py '. escapeshellarg($prfDevIp) .' '. escapeshellarg($prfName) .' '. escapeshellarg($prfPara1) .' '. escapeshellarg($prfPara2) .' '. escapeshellarg($prfPara3) .' '. escapeshellarg($prfPara4) .' '. escapeshellarg($prfPara5) .' '. escapeshellarg($prfPara6) .' '. escapeshellarg($prfPara7).' '. escapeshellarg($prfPara8);
        }
        else if ($prfType == 'DestAddrAffinity'){
            $prfPara1 = $profileData->defaultsFrom;
            $prfPara2 = $profileData->matchAcrossServices;
            $prfPara3 = $profileData->matchAcrossVirtuals;
            $prfPara4 = $profileData->matchAcrossPools;
            $prfPara5 = $profileData->hashAlgorithm;
            $prfPara6 = $profileData->timeout;
            $prfPara7 = $profileData->mask;
            $prfPara8 = $profileData->overrideConnectionLimit;
            
            file_put_contents("/var/log/chaniqphp.log", "new_dstAffProfile_build() Device IP: " . $prfDevIp . " Profile Name: " .$prfName. " Defaults-From: " .$prfPara1." Match Across Services: " .$prfPara2." Match Across VSs: " .$prfPara3." Match Across Pools: " .$prfPara4. " Hash Algo.: " .$prfPara5. " Timeout: " .$prfPara6." Prefix Length: " .$prfPara7." Override Connection Limit: " .$prfPara8."\n", FILE_APPEND);
            $cmd = '/usr/bin/python /var/www/chaniq/py/new_dstAffProfile_build.py '. escapeshellarg($prfDevIp) .' '. escapeshellarg($prfName) .' '. escapeshellarg($prfPara1) .' '. escapeshellarg($prfPara2) .' '. escapeshellarg($prfPara3) .' '. escapeshellarg($prfPara4) .' '. escapeshellarg($prfPara5) .' '. escapeshellarg($prfPara6) .' '. escapeshellarg($prfPara7).' '. escapeshellarg($prfPara8);
        }
        else if ($prfType == 'SrcAddrAffinity'){
            $prfPara1 = $profileData->defaultsFrom;
            $prfPara2 = $profileData->matchAcrossServices;
            $prfPara3 = $profileData->matchAcrossVirtuals;
            $prfPara4 = $profileData->matchAcrossPools;
            $prfPara5 = $profileData->hashAlgorithm;
            $prfPara6 = $profileData->timeout;
            $prfPara7 = $profileData->mask;
            $prfPara8 = $profileData->mapProxies;
            $prfPara9 = $profileData->overrideConnectionLimit;
            
            file_put_contents("/var/log/chaniqphp.log", "new_srcAffProfile_build() Device IP: " . $prfDevIp . " Profile Name: " .$prfName. " Defaults-From: " .$prfPara1." Match Across Services: " .$prfPara2." Match Across VSs: " .$prfPara3." Match Across Pools: " .$prfPara4. " Hash Algo.: " .$prfPara5. " Timeout: " .$prfPara6." Prefix Length: " .$prfPara7. " Map Proxies:" .$prfPara8." Override Connection Limit: " .$prfPara9."\n", FILE_APPEND);
            $cmd = '/usr/bin/python /var/www/chaniq/py/new_srcAffProfile_build.py '. escapeshellarg($prfDevIp) .' '. escapeshellarg($prfName) .' '. escapeshellarg($prfPara1) .' '. escapeshellarg($prfPara2) .' '. escapeshellarg($prfPara3) .' '. escapeshellarg($prfPara4) .' '. escapeshellarg($prfPara5) .' '. escapeshellarg($prfPara6) .' '. escapeshellarg($prfPara7).' '. escapeshellarg($prfPara8).' '. escapeshellarg($prfPara9);
        }
        else if ($prfType == 'Hash'){
            $prfPara1 = $profileData->defaultsFrom;
            $prfPara2 = $profileData->matchAcrossServices;
            $prfPara3 = $profileData->matchAcrossVirtuals;
            $prfPara4 = $profileData->matchAcrossPools;
            $prfPara5 = $profileData->hashAlgorithm;
            $prfPara6 = $profileData->hashOffset;
            $prfPara7 = $profileData->hashLength;
            $prfPara8 = $profileData->hashStartPattern;
            $prfPara9 = $profileData->hashEndPattern;
            $prfPara10 = $profileData->hashBufferLimit;
            $prfPara11 = $profileData->timeout;
            $prfPara12 = $profileData->rule;
            $prfPara13 = $profileData->overrideConnectionLimit;
            
            file_put_contents("/var/log/chaniqphp.log", "new_hashProfile_build() Device IP: " . $prfDevIp . " Profile Name: " .$prfName. " Defaults-From: " .$prfPara1." Match Across Services: " .$prfPara2." Match Across VSs: " .$prfPara3." Match Across Pools: " .$prfPara4. " Hash Algo: " .$prfPara5. " Hash Offset: " .$prfPara6. " Hash Length: " .$prfPara7. " Hash Start Pattern: " .$prfPara8. " Hash End Pattern: " .$prfPara9. " Hash Buffer Limit: " .$prfPara10." Timeout: " .$prfPara11." Rule: " .$prfPara12. " Override Connection Limit: " .$prfPara13."\n", FILE_APPEND);
            $cmd = '/usr/bin/python /var/www/chaniq/py/new_hashProfile_build.py '. escapeshellarg($prfDevIp) .' '. escapeshellarg($prfName) .' '. escapeshellarg($prfPara1) .' '. escapeshellarg($prfPara2) .' '. escapeshellarg($prfPara3) .' '. escapeshellarg($prfPara4) .' '. escapeshellarg($prfPara5) .' '. escapeshellarg($prfPara6) .' '. escapeshellarg($prfPara7).' '. escapeshellarg($prfPara8).' '. escapeshellarg($prfPara9).' '. escapeshellarg($prfPara10).' '. escapeshellarg($prfPara11).' '. escapeshellarg($prfPara12).' '. escapeshellarg($prfPara13);
        }
        else if ($prfType == 'SSL'){
            $prfPara1 = $profileData->defaultsFrom;
            $prfPara2 = $profileData->matchAcrossServices;
            $prfPara3 = $profileData->matchAcrossVirtuals;
            $prfPara4 = $profileData->matchAcrossPools;
            $prfPara5 = $profileData->timeout;
            $prfPara6 = $profileData->overrideConnectionLimit;
            
            file_put_contents("/var/log/chaniqphp.log", "new_sslProfile_build() Device IP: " . $prfDevIp . " Profile Name: " .$prfName. " Defaults-From: " .$prfPara1." Match Across Services: " .$prfPara2." Match Across VSs: " .$prfPara3." Match Across Pools: " .$prfPara4. " Timeout: " .$prfPara5. " Override Connection Limit: " .$prfPara6."\n", FILE_APPEND);
            $cmd = '/usr/bin/python /var/www/chaniq/py/new_sslProfile_build.py '. escapeshellarg($prfDevIp) .' '. escapeshellarg($prfName) .' '. escapeshellarg($prfPara1) .' '. escapeshellarg($prfPara2) .' '. escapeshellarg($prfPara3) .' '. escapeshellarg($prfPara4) .' '. escapeshellarg($prfPara5) .' '. escapeshellarg($prfPara6);
            
        }
        else if ($prfType == 'Universal'){
            $prfPara1 = $profileData->defaultsFrom;
            $prfPara2 = $profileData->matchAcrossServices;
            $prfPara3 = $profileData->matchAcrossVirtuals;
            $prfPara4 = $profileData->matchAcrossPools;
            $prfPara5 = $profileData->timeout;
            $prfPara6 = $profileData->rule;
            $prfPara7 = $profileData->overrideConnectionLimit;
            
            file_put_contents("/var/log/chaniqphp.log", "new_uniProfile_build() Device IP: " . $prfDevIp . " Profile Name: " .$prfName. " Defaults-From: " .$prfPara1." Match Across Services: " .$prfPara2." Match Across VSs: " .$prfPara3." Match Across Pools: " .$prfPara4. " Timeout: " .$prfPara5. " Rule: " .$prfPara6. " Override Connection Limit: " .$prfPara7."\n", FILE_APPEND);
            $cmd = '/usr/bin/python /var/www/chaniq/py/new_uniProfile_build.py '. escapeshellarg($prfDevIp) .' '. escapeshellarg($prfName) .' '. escapeshellarg($prfPara1) .' '. escapeshellarg($prfPara2) .' '. escapeshellarg($prfPara3) .' '. escapeshellarg($prfPara4) .' '. escapeshellarg($prfPara5) .' '. escapeshellarg($prfPara6) .' '. escapeshellarg($prfPara7);
            
        }
        else if ($prfType == 'OneConnect'){
            $prfPara1 = $profileData->defaultsFrom;
            $prfPara2 = $profileData->sourceMask;
            $prfPara3 = $profileData->maxSize;
            $prfPara4 = $profileData->maxAge;
            $prfPara5 = $profileData->maxReuse;
            $prfPara6 = $profileData->idleTimeoutOverride;
            $prfPara7 = $profileData->limitType;
            
            file_put_contents("/var/log/chaniqphp.log", "new_ocProfile_build() Device IP: " . $prfDevIp . " Profile Name: " .$prfName. " Defaults-From: " .$prfPara1." Source Prefix Length: " .$prfPara2." Maximum Size: " .$prfPara3." Maximum Age: " .$prfPara4. " Maximum Reuse: " .$prfPara5. " Idle Timeout Override: " .$prfPara6. " Limit Type: " .$prfPara7."\n", FILE_APPEND);
            $cmd = '/usr/bin/python /var/www/chaniq/py/new_ocProfile_build.py '. escapeshellarg($prfDevIp) .' '. escapeshellarg($prfName) .' '. escapeshellarg($prfPara1) .' '. escapeshellarg($prfPara2) .' '. escapeshellarg($prfPara3) .' '. escapeshellarg($prfPara4) .' '. escapeshellarg($prfPara5) .' '. escapeshellarg($prfPara6) .' '. escapeshellarg($prfPara7);
            
        }
        else if ($prfType == 'Stream'){
            $prfPara1 = $profileData->defaultsFrom;
            $prfPara2 = $profileData->source;
            $prfPara3 = $profileData->tmTarget;
            
            file_put_contents("/var/log/chaniqphp.log", "new_streamProfile_build() Device IP: " . $prfDevIp . " Profile Name: " .$prfName. " Defaults-From: " .$prfPara1." Source: " .$prfPara2." Target: " .$prfPara3."\n", FILE_APPEND);
            $cmd = '/usr/bin/python /var/www/chaniq/py/new_streamProfile_build.py '. escapeshellarg($prfDevIp) .' '. escapeshellarg($prfName) .' '. escapeshellarg($prfPara1) .' '. escapeshellarg($prfPara2) .' '. escapeshellarg($prfPara3);
            
        }
        
        $output = shell_exec($cmd);
        error_log(date("y-m-d H:i:s").": After python call - new_Profile_build.php() new_Profile_build() function called!\n", 3, "/var/log/chaniqphp.log");

        file_put_contents("/var/log/chaniqphp.log", "String Returned: " . $output , FILE_APPEND);
        
        if ($output == ''){
            $rtnOutput = ["Python shell_exec() returns null"];
            echo json_encode($rtnOutput);
        }
        else {
            $outputdata = json_decode($output, true);
            ksort($outputdata);
            
            $rtnOutput = [];
            
            foreach ($outputdata as $key => $value){
                file_put_contents("/var/log/chaniqphp.log", "shell_exec() Return - Key: " . $key . " Value: " . $value , FILE_APPEND);
                array_push($rtnOutput, (string)$value);
            }
            
            foreach ($rtnOutput as $value){
                file_put_contents("/var/log/chaniqphp.log", "String Returned: " . $value , FILE_APPEND);
            }
            
            $json = json_encode($rtnOutput);
            
            echo $json;
        }
    }
?>