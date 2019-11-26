<?php

    error_log(date("y-m-d H:i:s").": get_vs_config() - callBack function php has been called\n", 3, "/var/log/chaniqphp.log");
    
    // Call get_vs_config() by echo statement
    echo $_POST['method']();
    
    /**
     * Given the name of active LTM, get the list of pool names from the given active ltm
     *
     * @param String $active_ltm The name of active LTM device
     * @return Array
     *
     */
    function get_vsconfig($active_ltm, $vsname, $vspart)
    {
        $cmd = '/usr/bin/python /var/www/chaniq/py/get_vs_config.py '. $active_ltm . ' ' . $vsname .' '. $vspart;
        //echo "<br>Command:" .$cmd." <br>";
        error_log(date("y-m-d H:i:s").": get_vs_config() - get_vsconfig() called\n", 3, "/var/log/chaniqphp.log");
        $output = shell_exec($cmd);

        return $output;
    }
    
    function get_vs_config() {
        if(isset($_POST['DevIP']))
        {
            //$bigipIP = json_decode($_POST['DevIP']);
            $bigipIP = $_POST['DevIP'];
            $vsname = $_POST['VsName'];
            $vspart = $_POST['VsPart'];
            //error_log(date("y-m-d H:i:s").": get_vs_config() - Device IP sent over POST\n", 3, "/var/log/chaniqphp.log");
            file_put_contents("/var/log/chaniqphp.log", "get_vs_config() Device IP: " . $bigipIP . "\nVS Name: " .$vsname. "\nVS Partition: " .$vspart. "\n", FILE_APPEND);
        }
        
        //$echoOut = echoTest();
        //file_put_contents("/var/log/chaniqphp.log", "get_vs_config() EchoTest: " . $echoOut, FILE_APPEND);
        $vsConfigs = get_vsconfig($bigipIP, $vsname, $vspart);
        file_put_contents("/var/log/chaniqphp.log", "get_vs_config() - Return data from BIG-IP\n", FILE_APPEND);
        //$json = json_encode($vsConfigs);
        echo $vsConfigs;
    }
?>