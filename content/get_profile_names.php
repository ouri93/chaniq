<?php

    error_log(date("y-m-d H:i:s").": get_profile_names() - callBack function php has been called\n", 3, "/var/log/chaniqphp.log");
    
    // Call get_profile_names() by echo statement
    echo $_POST['method']();
    
    /**
     * Given the name of active LTM, get the list of health monitors of the active ltm
     *
     * @param String $active_ltm The name of active LTM device
     * @param String $prf_type The name of a monitor type.
     *               1. TCP
     *               2. HTTP and HTTPS
     *               3. UDP
     *               4. TCP Half_open
     *               5. Gateway ICMP
     *               6. External
     * @return Array
     *
     */
    function get_names($active_ltm, $prfType)
    {
        $cmd = '/usr/bin/python /var/www/chaniq/py/get_profiles.py '.$active_ltm.' ' . escapeshellarg($prfType);
        //echo "<br>Command:" .$cmd." <br>";
        error_log(date("y-m-d H:i:s").": get_profile_names() - get_names() called. Dev IP: " . $active_ltm . " Profile Type: " . $prfType . "\n", 3, "/var/log/chaniqphp.log");
        exec($cmd, $output);
        
        //echo "<br>Output: " .$output[0];
        $rtn_out = explode(":", $output['0']);
        return $rtn_out;
    }
    
    function get_profile_names() {
        if(isset($_POST['DevIP']))
        {
            //$bigipIP = json_decode($_POST['DevIP']);
            $bigipIP = $_POST['DevIP'];
            $prfType = $_POST['PrfType'];
            //error_log(date("y-m-d H:i:s").": get_profile_names() - Device IP sent over POST\n", 3, "/var/log/chaniqphp.log");
            file_put_contents("/var/log/chaniqphp.log", "get_profile_names() Device IP: " . $bigipIP."\n", FILE_APPEND);
        }
        
        //$echoOut = echoTest();
        //file_put_contents("/var/log/chaniqphp.log", "get_profile_names(): " . $echoOut, FILE_APPEND);
        $prfNames = get_names($bigipIP, $prfType);

        foreach ($prfNames as $value) {
            file_put_contents("/var/log/chaniqphp.log", "Profile name: " . $value . "\n", FILE_APPEND);
        }
        $json = json_encode($prfNames);
        echo $json;
    }
?>