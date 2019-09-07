<?php

    error_log(date("y-m-d H:i:s").": getHttpSettings() - callBack function php has been called\n", 3, "/var/log/chaniqphp.log");
    
    // Call getHttpSettings() by echo statement
    echo $_POST['method']();
    
    /**
     * Given the name of active LTM, HTTP proxy Mode, and Profile Name, retrieve the profile setting and return to php
     *
     * @param String $active_ltm The name of active LTM device
     * @param String $proxyType The name of a proxy mode. Used only in Profile Build mode! 
     * @param String $prfType The name of Profile Type
     * @param String $prfName The chosen parent profile name in profile build mode.
     *                        The chosen profile name in Profile change mode.
     * @param String $prfMode Profile modes - Profile Build or Profile Change
     * @return Array
     *
     */
    function getSettings($active_ltm, $proxyType, $prfType, $prfName, $prfMode)
    {
        $cmd = '/usr/bin/python /var/www/chaniq/py/getHttpSettings.py '.$active_ltm.' ' . escapeshellarg($proxyType) .' '.escapeshellarg($prfType) .' '.escapeshellarg($prfName).' '.escapeshellarg($prfMode);
        //echo "<br>Command:" .$cmd." <br>";
        error_log(date("y-m-d H:i:s").": getSettings() called\n", 3, "/var/log/chaniqphp.log");
        exec($cmd, $output);
        
        //$rtn_out = explode(":", $output['0']);
        //return $rtn_out;
        return $output[0];
    }
    //DevIP:arr[1], ProxyType:pxyMode, PrfType:prfType, PrfName:prfName 
    function getHttpSettings() {
        if(isset($_POST['DevIP']))
        {
            //$bigipIP = json_decode($_POST['DevIP']);
            $bigipIP = $_POST['DevIP'];
            $proxyType = $_POST['ProxyType'];
            $prfType = $_POST['PrfType'];
            $prfName = $_POST['PrfName'];
            $prfMode = $_POST['PrfMode'];
            
            //error_log(date("y-m-d H:i:s").": getHttpSettings() - Device IP sent over POST\n", 3, "/var/log/chaniqphp.log");
            file_put_contents("/var/log/chaniqphp.log", "getHttpSettings() \nDevice IP: " . $bigipIP . "\nProxy Type: " . $proxyType . "\nProfile Type: " . $prfType . "\nChosen or Parent Profile Name: " . $prfName . "\nProfile Mode: " . $prfMode . "\n", FILE_APPEND);
        }
        
        $httpSettings = getSettings($bigipIP, $proxyType, $prfType, $prfName, $prfMode);

        file_put_contents("/var/log/chaniqphp.log", "HTTP Settings: " . $httpSettings . "\n", FILE_APPEND);
        return $httpSettings;
    }
?>