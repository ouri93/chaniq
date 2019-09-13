<?php

    //if(isset($_POST)==TRUE && empty($_POST)==FALSE):
    // If you put variables to save data from POST, it wont work. I moved the part under new_certkey_build()

    error_log(date("y-m-d H:i:s").": new_Profile_build.php() - callBack function php has been called\n", 3, "/var/log/chaniqphp.log");
    
    // Call new_Profile_build() by echo statement
    if (isset($_POST['newProfileBuild'])){
        $profileData = json_decode($_POST['newProfileBuild']);
        file_put_contents("/var/log/chaniqphp.log", "In new_Profile_build.php calling new_Profile_build() fucntion: " . $profileData->phpFileName ."\n", FILE_APPEND);
        
        // Call the fuction new_Profile_build()
        echo ($profileData->phpFileName)($profileData);
    }
    else{

        echo "Failed to call main funciton new_Profile_build()";
    }
    
    //'phpFileName', 'DevIP', 'name', 'dplyOrChg', 'proxyType', 'defaultsFrom', 'basicAuthRealm', 'fallbackHost', 'fallbackStatusCodes', 'headerErase'
    //'headerInsert','requestChunking', 'responseChunkimg','insertXforwardedFor', 'serverAgentName', 'dnsResolver'
    function new_Profile_build($profileData) {
        $cmd = '';
        
        $phpFileName = $profileData->phpFileName;
        $prfDevIp = $profileData->DevIP;
        $prfName = $profileData->name;
        $prfDplyOrChg = $profileData->dplyOrChg;
        //$prfType = $profileData->PrfType;
        $prfType = $profileData->LoadTypeName;
        file_put_contents("/var/log/chaniqphp.log", "new_Profile_build() called. \nDevice IP: " . $prfDevIp . "\nDeploy or Change: " . $prfDplyOrChg . "\nProfile Type:" . $prfType . "\nPhp Filename: " . $phpFileName . "\n", FILE_APPEND);
        
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

            file_put_contents("/var/log/chaniqphp.log", "new_DnsProfile_build() \nDevice IP: " . $prfDevIp . " \nProfile Name: " .$prfName. "\nProfile Deploy or Change: " .$prfDplyOrChg . "\nDefaults-From: " .$prfDftFrom."\nHW Query Validation: " .$prfHwValid."\nHW Response Cache: " .$prfHwRespCache."\nDNS Express: " .$prfDnsExp. "\nGSLB: " .$prfGtm. "\nUnhandled Query Action: " .$prfUnhandledAct."\nUse BIND: " .$prfUseBind."\nZone Transfer: " .$prfZoneXfr."\n", FILE_APPEND);
            $cmd = '/usr/bin/python /var/www/chaniq/py/new_DnsProfile_build.py '. escapeshellarg($prfDevIp) .' '. escapeshellarg($prfName) .' '. escapeshellarg($prfDplyOrChg) .' '. escapeshellarg($prfDftFrom) .' '. escapeshellarg($prfHwValid) .' '. escapeshellarg($prfHwRespCache) .' '. escapeshellarg($prfDnsExp) .' '. escapeshellarg($prfGtm) .' '. escapeshellarg($prfUnhandledAct) .' '. escapeshellarg($prfUseBind) .' '. escapeshellarg($prfZoneXfr).' '. escapeshellarg($prfDnsSecurity) .' '. escapeshellarg($prfRecursion);
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
            
            file_put_contents("/var/log/chaniqphp.log", "new_cookieProfile_build() \nDevice IP: " . $prfDevIp . " \nProfile Name: " .$prfName. "\nProfile Deploy or Change: " .$prfDplyOrChg . "\nDefaults-From: " .$prfPara1."\nCookie Method: " .$prfPara2."\nCookie Name: " .$prfPara3."\nHttp Only: " .$prfPara4. "\nSecure Attribute: " .$prfPara5. "\nAlways Send Cookie: " .$prfPara6."\nExpiration: " .$prfPara7."\nOverride Connection Limit: " .$prfPara8."\n", FILE_APPEND);
            $cmd = '/usr/bin/python /var/www/chaniq/py/new_cookieProfile_build.py '. escapeshellarg($prfDevIp) .' '. escapeshellarg($prfName) .' '. escapeshellarg($prfDplyOrChg) .' '. escapeshellarg($prfPara1) .' '. escapeshellarg($prfPara2) .' '. escapeshellarg($prfPara3) .' '. escapeshellarg($prfPara4) .' '. escapeshellarg($prfPara5) .' '. escapeshellarg($prfPara6) .' '. escapeshellarg($prfPara7).' '. escapeshellarg($prfPara8);
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
            
            file_put_contents("/var/log/chaniqphp.log", "new_dstAffProfile_build() \nDevice IP: " . $prfDevIp . " \nProfile Name: " .$prfName. "\nProfile Deploy or Change: " .$prfDplyOrChg . "\nDefaults-From: " .$prfPara1."\nMatch Across Services: " .$prfPara2."\nMatch Across VSs: " .$prfPara3."\nMatch Across Pools: " .$prfPara4. "\nHash Algo.: " .$prfPara5. "\nTimeout: " .$prfPara6."\nPrefix Length: " .$prfPara7."\nOverride Connection Limit: " .$prfPara8."\n", FILE_APPEND);
            $cmd = '/usr/bin/python /var/www/chaniq/py/new_dstAffProfile_build.py '. escapeshellarg($prfDevIp) .' '. escapeshellarg($prfName) .' '. escapeshellarg($prfDplyOrChg) .' '. escapeshellarg($prfPara1) .' '. escapeshellarg($prfPara2) .' '. escapeshellarg($prfPara3) .' '. escapeshellarg($prfPara4) .' '. escapeshellarg($prfPara5) .' '. escapeshellarg($prfPara6) .' '. escapeshellarg($prfPara7).' '. escapeshellarg($prfPara8);
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
            
            file_put_contents("/var/log/chaniqphp.log", "new_srcAffProfile_build() \nDevice IP: " . $prfDevIp . " \nProfile Name: " .$prfName. "\nProfile Deploy or Change: " .$prfDplyOrChg . "\nDefaults-From: " .$prfPara1."\nMatch Across Services: " .$prfPara2."\nMatch Across VSs: " .$prfPara3."\nMatch Across Pools: " .$prfPara4. "\nHash Algo.: " .$prfPara5. "\nTimeout: " .$prfPara6."\nPrefix Length: " .$prfPara7. "\nMap Proxies:" .$prfPara8."\nOverride Connection Limit: " .$prfPara9."\n", FILE_APPEND);
            $cmd = '/usr/bin/python /var/www/chaniq/py/new_srcAffProfile_build.py '. escapeshellarg($prfDevIp) .' '. escapeshellarg($prfName) .' '. escapeshellarg($prfDplyOrChg) .' '. escapeshellarg($prfPara1) .' '. escapeshellarg($prfPara2) .' '. escapeshellarg($prfPara3) .' '. escapeshellarg($prfPara4) .' '. escapeshellarg($prfPara5) .' '. escapeshellarg($prfPara6) .' '. escapeshellarg($prfPara7).' '. escapeshellarg($prfPara8).' '. escapeshellarg($prfPara9);
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
            
            file_put_contents("/var/log/chaniqphp.log", "new_hashProfile_build() \nDevice IP: " . $prfDevIp . " \nProfile Name: " .$prfName. "\nProfile Deploy or Change: " .$prfDplyOrChg . "\nDefaults-From: " .$prfPara1."\nMatch Across Services: " .$prfPara2."\nMatch Across VSs: " .$prfPara3."\nMatch Across Pools: " .$prfPara4. "\nHash Algo: " .$prfPara5. "\nHash Offset: " .$prfPara6. "\nHash Length: " .$prfPara7. "\nHash Start Pattern: " .$prfPara8. "\nHash End Pattern: " .$prfPara9. "\nHash Buffer Limit: " .$prfPara10."\nTimeout: " .$prfPara11."\nRule: " .$prfPara12. "\nOverride Connection Limit: " .$prfPara13."\n", FILE_APPEND);
            $cmd = '/usr/bin/python /var/www/chaniq/py/new_hashProfile_build.py '. escapeshellarg($prfDevIp) .' '. escapeshellarg($prfName) .' '. escapeshellarg($prfDplyOrChg) .' '. escapeshellarg($prfPara1) .' '. escapeshellarg($prfPara2) .' '. escapeshellarg($prfPara3) .' '. escapeshellarg($prfPara4) .' '. escapeshellarg($prfPara5) .' '. escapeshellarg($prfPara6) .' '. escapeshellarg($prfPara7).' '. escapeshellarg($prfPara8).' '. escapeshellarg($prfPara9).' '. escapeshellarg($prfPara10).' '. escapeshellarg($prfPara11).' '. escapeshellarg($prfPara12).' '. escapeshellarg($prfPara13);
        }
        else if ($prfType == 'SSL'){
            $prfPara1 = $profileData->defaultsFrom;
            $prfPara2 = $profileData->matchAcrossServices;
            $prfPara3 = $profileData->matchAcrossVirtuals;
            $prfPara4 = $profileData->matchAcrossPools;
            $prfPara5 = $profileData->timeout;
            $prfPara6 = $profileData->overrideConnectionLimit;
            
            file_put_contents("/var/log/chaniqphp.log", "new_sslProfile_build() \nDevice IP: " . $prfDevIp . " \nProfile Name: " .$prfName. "\nProfile Deploy or Change: " .$prfDplyOrChg . "\nDefaults-From: " .$prfPara1."\nMatch Across Services: " .$prfPara2."\nMatch Across VSs: " .$prfPara3."\nMatch Across Pools: " .$prfPara4. "\nTimeout: " .$prfPara5. "\nOverride Connection Limit: " .$prfPara6."\n", FILE_APPEND);
            $cmd = '/usr/bin/python /var/www/chaniq/py/new_sslProfile_build.py '. escapeshellarg($prfDevIp) .' '. escapeshellarg($prfName) .' '. escapeshellarg($prfDplyOrChg) .' '. escapeshellarg($prfPara1) .' '. escapeshellarg($prfPara2) .' '. escapeshellarg($prfPara3) .' '. escapeshellarg($prfPara4) .' '. escapeshellarg($prfPara5) .' '. escapeshellarg($prfPara6);
            
        }
        else if ($prfType == 'Universal'){
            $prfPara1 = $profileData->defaultsFrom;
            $prfPara2 = $profileData->matchAcrossServices;
            $prfPara3 = $profileData->matchAcrossVirtuals;
            $prfPara4 = $profileData->matchAcrossPools;
            $prfPara5 = $profileData->timeout;
            $prfPara6 = $profileData->rule;
            $prfPara7 = $profileData->overrideConnectionLimit;
            
            file_put_contents("/var/log/chaniqphp.log", "new_uniProfile_build() \nDevice IP: " . $prfDevIp . " \nProfile Name: " .$prfName. "\nProfile Deploy or Change: " .$prfDplyOrChg . "\nDefaults-From: " .$prfPara1."\nMatch Across Services: " .$prfPara2."\nMatch Across VSs: " .$prfPara3."\nMatch Across Pools: " .$prfPara4. "\nTimeout: " .$prfPara5. "\nRule: " .$prfPara6. "\nOverride Connection Limit: " .$prfPara7."\n", FILE_APPEND);
            $cmd = '/usr/bin/python /var/www/chaniq/py/new_uniProfile_build.py '. escapeshellarg($prfDevIp) .' '. escapeshellarg($prfName) .' '. escapeshellarg($prfDplyOrChg) .' '. escapeshellarg($prfPara1) .' '. escapeshellarg($prfPara2) .' '. escapeshellarg($prfPara3) .' '. escapeshellarg($prfPara4) .' '. escapeshellarg($prfPara5) .' '. escapeshellarg($prfPara6) .' '. escapeshellarg($prfPara7);
            
        }
        else if ($prfType == 'FastL4'){
            $prfPara1 = $profileData->defaultsFrom;
            $prfPara2 = $profileData->resetOnTimeout;
            $prfPara3 = $profileData->reassembleFragments;
            $prfPara4 = $profileData->idleTimeout;
            $prfPara5 = $profileData->tcpHandshakeTimeout;
            $prfPara6 = $profileData->tcpTimestampMode;
            $prfPara7 = $profileData->tcpWscaleMode;
            $prfPara8 = $profileData->looseInitialization;
            $prfPara9 = $profileData->looseClose;
            $prfPara10 = $profileData->tcpCloseTimeout;
            $prfPara11 = $profileData->keepAliveInterval;

            file_put_contents("/var/log/chaniqphp.log", "new_f4Profile_build() \nDevice IP: " . $prfDevIp . " \nProfile Name: " .$prfName. "\nProfile Deploy or Change: " .$prfDplyOrChg . "\nDefaults-From: " .$prfPara1."\nReset on Timeout: " .$prfPara2."\nReassemble IP Fragment: " .$prfPara3."\nIdle Timeout: " .$prfPara4. "\nTCP Handshake Timeout: " .$prfPara5. "\nTCP Timestamp Mode: " .$prfPara6. "\nTCP Window Scale Mode: " .$prfPara7. "\nLoose Initiation: " .$prfPara8. "\nLoose Close: " .$prfPara9."\nTCP Close Timeout: " .$prfPara10."\nTCP Keep Alive Interval: " .$prfPara11."\n", FILE_APPEND);
            $cmd = '/usr/bin/python /var/www/chaniq/py/new_f4Profile_build.py '. escapeshellarg($prfDevIp) .' '. escapeshellarg($prfName) .' '. escapeshellarg($prfDplyOrChg) .' '. escapeshellarg($prfPara1) .' '. escapeshellarg($prfPara2) .' '. escapeshellarg($prfPara3) .' '. escapeshellarg($prfPara4) .' '. escapeshellarg($prfPara5) .' '. escapeshellarg($prfPara6) .' '. escapeshellarg($prfPara7).' '. escapeshellarg($prfPara8).' '. escapeshellarg($prfPara9).' '. escapeshellarg($prfPara10).' '. escapeshellarg($prfPara11);
            
        }
        else if ($prfType == 'TCP'){
            $prfPara1 = $profileData->defaultsFrom;
            $prfPara2 = $profileData->resetOnTimeout;
            $prfPara3 = $profileData->proxyBufferHigh;
            $prfPara4 = $profileData->proxyBufferLow;
            $prfPara5 = $profileData->receiveWindowSize;
            $prfPara6 = $profileData->sendBufferSize;
            $prfPara7 = $profileData->ackOnPush;
            $prfPara8 = $profileData->nagle;
            $prfPara9 = $profileData->initCwnd;
            $prfPara10 = $profileData->slowStart;
            $prfPara11 = $profileData->selectiveAcks;
            
            file_put_contents("/var/log/chaniqphp.log", "new_tcpProfile_build() \nDevice IP: " . $prfDevIp . " \nProfile Name: " .$prfName. "\nProfile Deploy or Change: " .$prfDplyOrChg . "\nDefaults-From: " .$prfPara1."\nReset on Timeout: " .$prfPara2."\nProxy Buffer High: " .$prfPara3."\nProxy Buffer Low: " .$prfPara4. "\nReceive Window: " .$prfPara5. "\nSend Buffer: " .$prfPara6. "\nAcknowledge on Push: " .$prfPara7. "\nNagle's Algorithm: " .$prfPara8. "\nInitial Congestion Window Size: " .$prfPara9."\nSlow Start: " .$prfPara10."\nSelective ACKs: " .$prfPara11."\n", FILE_APPEND);
            $cmd = '/usr/bin/python /var/www/chaniq/py/new_tcpProfile_build.py '. escapeshellarg($prfDevIp) .' '. escapeshellarg($prfName) .' '. escapeshellarg($prfDplyOrChg) .' '. escapeshellarg($prfPara1) .' '. escapeshellarg($prfPara2) .' '. escapeshellarg($prfPara3) .' '. escapeshellarg($prfPara4) .' '. escapeshellarg($prfPara5) .' '. escapeshellarg($prfPara6) .' '. escapeshellarg($prfPara7).' '. escapeshellarg($prfPara8).' '. escapeshellarg($prfPara9).' '. escapeshellarg($prfPara10).' '. escapeshellarg($prfPara11);
            
        }
        else if ($prfType == 'UDP'){
            $prfPara1 = $profileData->defaultsFrom;
            $prfPara2 = $profileData->proxyMss;
            $prfPara3 = $profileData->idleTimeout;
            $prfPara4 = $profileData->ipTosToClient;
            $prfPara5 = $profileData->linkQosToClient;
            $prfPara6 = $profileData->datagramLoadBalancing;
            $prfPara7 = $profileData->allowNoPayload;
            $prfPara8 = $profileData->ipTtlMode;
            $prfPara9 = $profileData->ipTtlV4;
            $prfPara10 = $profileData->ipTtlV6;
            $prfPara11 = $profileData->ipDfMode;
            
            file_put_contents("/var/log/chaniqphp.log", "new_udpProfile_build() \nDevice IP: " . $prfDevIp . " \nProfile Name: " .$prfName. "\nProfile Deploy or Change: " .$prfDplyOrChg . "\nDefaults-From: " .$prfPara1."\nProxy Maximum Segment: " .$prfPara2."\nIdle Timeout: " .$prfPara3."\nIP ToS: " .$prfPara4. "\nLink QoS: " .$prfPara5. "\nDatagram LB: " .$prfPara6. "\nAllow No Pyaload: " .$prfPara7. "\nTTL Mode: " .$prfPara8. "\nTTL IPv4: " .$prfPara9."\nTTL IPv6: " .$prfPara10."\nDon't Fragment Mode: " .$prfPara11."\n", FILE_APPEND);
            $cmd = '/usr/bin/python /var/www/chaniq/py/new_udpProfile_build.py '. escapeshellarg($prfDevIp) .' '. escapeshellarg($prfName) .' '. escapeshellarg($prfDplyOrChg) .' '. escapeshellarg($prfPara1) .' '. escapeshellarg($prfPara2) .' '. escapeshellarg($prfPara3) .' '. escapeshellarg($prfPara4) .' '. escapeshellarg($prfPara5) .' '. escapeshellarg($prfPara6) .' '. escapeshellarg($prfPara7).' '. escapeshellarg($prfPara8).' '. escapeshellarg($prfPara9).' '. escapeshellarg($prfPara10).' '. escapeshellarg($prfPara11);
            
        }
        else if ($prfType == 'CLIENTSSL'){
            $prfPara1 = $profileData->defaultsFrom;
            $prfPara2 = $profileData->cert;
            $prfPara3 = $profileData->key;
            $prfPara4 = $profileData->chain;
            $prfPara5 = $profileData->ciphers;
            $prfPara6 = $profileData->proxySsl;
            $prfPara7 = $profileData->proxySslPassthrough;
            $prfPara8 = $profileData->renegotiation;
            $prfPara9 = $profileData->renegotiatePeriod;
            $prfPara10 = $profileData->renegotiateSize;
            $prfPara11 = $profileData->renegotiateMaxRecordDelay;
            $prfPara12 = $profileData->secureRenegotiation;
            $prfPara13 = $profileData->maxRenegotiationsPerMinute;
            $prfPara14 = $profileData->serverName;
            $prfPara15 = $profileData->sniDefault;
            $prfPara16 = $profileData->sniRequire;
            
            file_put_contents("/var/log/chaniqphp.log", "new_clisslProfile_build() \nDevice IP: " . $prfDevIp . " \nProfile Name: " .$prfName. "\nProfile Deploy or Change: " .$prfDplyOrChg . "\nDefaults-From: " .$prfPara1."\nCertificate: " .$prfPara2."\nKey: " .$prfPara3."\nChain: " .$prfPara4. "\nCiphers: " .$prfPara5. "\nproxy SSL: " .$prfPara6. "\nProxsy SSL Pass-through: " .$prfPara7. "\nRenegotiation: " .$prfPara8. "\nRenegotiate Period: " .$prfPara9."\nRenegotiate Size: " .$prfPara10."\nRenegotiate Max Record Delay: " .$prfPara11."\nSecure Renegotiation: " .$prfPara12."\nMax Renegotiations: " .$prfPara13."\nServer Name: " .$prfPara14."\nDefault SSL Profile for SNI: " .$prfPara15."\nRequire Peer SNI support: " .$prfPara16."\n", FILE_APPEND);
            $cmd = '/usr/bin/python /var/www/chaniq/py/new_clisslProfile_build.py '. escapeshellarg($prfDevIp) .' '. escapeshellarg($prfName) .' '. escapeshellarg($prfDplyOrChg) .' '. escapeshellarg($prfPara1) .' '. escapeshellarg($prfPara2) .' '. escapeshellarg($prfPara3) .' '. escapeshellarg($prfPara4) .' '. escapeshellarg($prfPara5) .' '. escapeshellarg($prfPara6) .' '. escapeshellarg($prfPara7).' '. escapeshellarg($prfPara8).' '. escapeshellarg($prfPara9).' '. escapeshellarg($prfPara10).' '. escapeshellarg($prfPara11).' '. escapeshellarg($prfPara12).' '. escapeshellarg($prfPara13).' '. escapeshellarg($prfPara14).' '. escapeshellarg($prfPara15).' '. escapeshellarg($prfPara16);
            
        }
        else if ($prfType == 'SERVERSSL'){
            $prfPara1 = $profileData->defaultsFrom;
            $prfPara2 = $profileData->cert;
            $prfPara3 = $profileData->key;
            $prfPara4 = $profileData->chain;
            $prfPara5 = $profileData->ciphers;
            $prfPara6 = $profileData->proxySsl;
            $prfPara7 = $profileData->proxySslPassthrough;
            $prfPara8 = $profileData->renegotiation;
            $prfPara9 = $profileData->renegotiatePeriod;
            $prfPara10 = $profileData->renegotiateSize;
            $prfPara11 = $profileData->secureRenegotiation;
            $prfPara12 = $profileData->serverName;
            $prfPara13 = $profileData->sniDefault;
            $prfPara14 = $profileData->sniRequire;
            
            file_put_contents("/var/log/chaniqphp.log", "new_srvsslProfile_build() \nDevice IP: " . $prfDevIp . " \nProfile Name: " .$prfName. "\nProfile Deploy or Change: " .$prfDplyOrChg . "\nDefaults-From: " .$prfPara1."\nCertificate: " .$prfPara2."\nKey: " .$prfPara3."\nChain: " .$prfPara4. "\nCiphers: " .$prfPara5. "\nproxy SSL: " .$prfPara6. "\nProxsy SSL Pass-through: " .$prfPara7. "\nRenegotiation: " .$prfPara8. "\nRenegotiate Period: " .$prfPara9."\nRenegotiate Size: " .$prfPara10."\nSecure Renegotiation: " .$prfPara11."\nServer Name: " .$prfPara12."\nDefault SSL Profile for SNI: " .$prfPara13."\nRequire Peer SNI support: " .$prfPara14."\n", FILE_APPEND);
            $cmd = '/usr/bin/python /var/www/chaniq/py/new_srvsslProfile_build.py '. escapeshellarg($prfDevIp) .' '. escapeshellarg($prfName) .' '. escapeshellarg($prfDplyOrChg) .' '. escapeshellarg($prfPara1) .' '. escapeshellarg($prfPara2) .' '. escapeshellarg($prfPara3) .' '. escapeshellarg($prfPara4) .' '. escapeshellarg($prfPara5) .' '. escapeshellarg($prfPara6) .' '. escapeshellarg($prfPara7).' '. escapeshellarg($prfPara8).' '. escapeshellarg($prfPara9).' '. escapeshellarg($prfPara10).' '. escapeshellarg($prfPara11).' '. escapeshellarg($prfPara12).' '. escapeshellarg($prfPara13).' '. escapeshellarg($prfPara14);
        }
        else if ($prfType == 'OneConnect'){
            $prfPara1 = $profileData->defaultsFrom;
            $prfPara2 = $profileData->sourceMask;
            $prfPara3 = $profileData->maxSize;
            $prfPara4 = $profileData->maxAge;
            $prfPara5 = $profileData->maxReuse;
            $prfPara6 = $profileData->idleTimeoutOverride;
            $prfPara7 = $profileData->limitType;
            
            file_put_contents("/var/log/chaniqphp.log", "new_ocProfile_build() \nDevice IP: " . $prfDevIp . " \nProfile Name: " .$prfName. "\nProfile Deploy or Change: " .$prfDplyOrChg . "\nDefaults-From: " .$prfPara1."\nSource Prefix Length: " .$prfPara2."\nMaximum Size: " .$prfPara3."\nMaximum Age: " .$prfPara4. "\nMaximum Reuse: " .$prfPara5. "\nIdle Timeout Override: " .$prfPara6. "\nLimit Type: " .$prfPara7."\n", FILE_APPEND);
            $cmd = '/usr/bin/python /var/www/chaniq/py/new_ocProfile_build.py '. escapeshellarg($prfDevIp) .' '. escapeshellarg($prfName) .' '. escapeshellarg($prfDplyOrChg) .' '. escapeshellarg($prfPara1) .' '. escapeshellarg($prfPara2) .' '. escapeshellarg($prfPara3) .' '. escapeshellarg($prfPara4) .' '. escapeshellarg($prfPara5) .' '. escapeshellarg($prfPara6) .' '. escapeshellarg($prfPara7);
            
        }
        else if ($prfType == 'Stream'){
            $prfPara1 = $profileData->defaultsFrom;
            $prfPara2 = $profileData->source;
            $prfPara3 = $profileData->tmTarget;
            
            file_put_contents("/var/log/chaniqphp.log", "new_streamProfile_build() \nDevice IP: " . $prfDevIp . " \nProfile Name: " .$prfName. "\nProfile Deploy or Change: " .$prfDplyOrChg . "\nDefaults-From: " .$prfPara1."\nSource: " .$prfPara2."\nTarget: " .$prfPara3."\n", FILE_APPEND);
            $cmd = '/usr/bin/python /var/www/chaniq/py/new_streamProfile_build.py '. escapeshellarg($prfDevIp) .' '. escapeshellarg($prfName) .' '. escapeshellarg($prfDplyOrChg) .' '. escapeshellarg($prfPara1) .' '. escapeshellarg($prfPara2) .' '. escapeshellarg($prfPara3);
            
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
                file_put_contents("/var/log/chaniqphp.log", "shell_exec() Return - Key: " . $key . " Value: " . $value . "\n", FILE_APPEND);
                array_push($rtnOutput, (string)$value);
            }
            
            foreach ($rtnOutput as $value){
                file_put_contents("/var/log/chaniqphp.log", "String Returned: " . $value  . "\n", FILE_APPEND);
            }
            
            $json = json_encode($rtnOutput);
            
            echo $json;
        }
    }
?>