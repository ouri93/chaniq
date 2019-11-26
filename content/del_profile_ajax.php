<?php

    error_log(date("y-m-d H:i:s").": del_profile_ajax() - callBack function php has been called\n", 3, "/var/log/chaniqphp.log");
    
    // Call del_profile_ajax() by echo statement
    echo $_POST['method']();
    
    /**
     * Given the IP address of active LTM, profile Type, profile name, and partition, delete the specified profile from BIG-IP
     * Supported Profile types:
     *               "TCP",  "UDP",  "FastL4",  "PERSIST",  "Cookie",  "DestAddrAffinity",  "SrcAddrAffinity",
     *               "Hash",  "SSL",  "Universal",  "HTTP:reverse",  "HTTP:explicit",  "HTTP:transparent",  "HTTP:dnsresolver",
     *               "HTTP",  "DNS",  "CLIENTSSL",  "SERVERSSL",  "OneConnect",  "Stream",  "IRULE",  "SNATPOOL",  "POLICY",  "CERT",  "KEY"    
     *
     */
    
    // Data format: {method:'jsonDATA', DevIP:ltmIP, LoadTypeName:prfType, Partition:partition, PrfName:prfName}
    function del_profile_ajax() {
        if(isset($_POST['DevIP']))
        {
            //$bigipIP = json_decode($_POST['DevIP']);
            $bigipIP = $_POST['DevIP'];
            $prfType = $_POST['LoadTypeName'];
            $partition = $_POST['Partition'];
            $prfName = $_POST['PrfName'];
            //error_log(date("y-m-d H:i:s").": del_profile_ajax() - Device IP sent over POST\n", 3, "/var/log/chaniqphp.log");
            file_put_contents("/var/log/chaniqphp.log", "del_profile_ajax() Device IP: " . $bigipIP."\n", FILE_APPEND);
        }
        
        $cmd = '/usr/bin/python /var/www/chaniq/py/del_profile_ajax.py ' .$bigipIP. ' ' .escapeshellarg($prfType). ' ' .escapeshellarg($partition). ' ' .escapeshellarg($prfName);
        error_log(date("y-m-d H:i:s").": del_profile_ajax() - get_names() called. Dev IP: " . $bigipIP. " Profile Type: " . $prfType . "\n", 3, "/var/log/chaniqphp.log");
        $output = shell_exec($cmd);

        if($output == null) error_log(date("y-m-d H:i:s").": Output returned NULL\n", 3, "/var/log/chaniqphp.log");
        
        error_log(date("y-m-d H:i:s").": After python call - del_profile_ajax.php() function is called!\n", 3, "/var/log/chaniqphp.log");
        
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