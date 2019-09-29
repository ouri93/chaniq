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
    function get_vsconfig($active_ltm, $vsname)
    {
        $cmd = '/usr/bin/python /var/www/chaniq/py/get_vs_config.py '. $active_ltm . ' ' . $vsname;
        //echo "<br>Command:" .$cmd." <br>";
        error_log(date("y-m-d H:i:s").": get_vs_config() - get_vsconfig() called\n", 3, "/var/log/chaniqphp.log");
        exec($cmd, $output);
        
        //echo "<br>Output: " .$output[0];
        $rtn_out = explode(":", $output['0']);
        return $rtn_out;
    }
    
    function get_vs_config() {
        if(isset($_POST['DevIP']))
        {
            //$bigipIP = json_decode($_POST['DevIP']);
            $bigipIP = $_POST['DevIP'];
            $vsname = $_POST['VsName'];
            //error_log(date("y-m-d H:i:s").": get_vs_config() - Device IP sent over POST\n", 3, "/var/log/chaniqphp.log");
            file_put_contents("/var/log/chaniqphp.log", "get_vs_config() Device IP: " . $bigipIP . "\n", FILE_APPEND);
        }
        
        //$echoOut = echoTest();
        //file_put_contents("/var/log/chaniqphp.log", "get_vs_config() EchoTest: " . $echoOut, FILE_APPEND);
        $vsConfigs = get_vsconfig($bigipIP, $vsname);

        foreach ($vsConfigs as $value) {
            file_put_contents("/var/log/chaniqphp.log", "Config names: " . $value . "\n", FILE_APPEND);
        }
        $json = json_encode($vsConfigs);
        echo $json;
    }
?>