<?php

    error_log(date("y-m-d H:i:s").": get_pool_names() - callBack function php has been called\n", 3, "/var/log/chaniqphp.log");
    
    // Call get_pool_names() by echo statement
    echo $_POST['method']();
    
    /**
     * Given the name of active LTM, get the list of pool names from the given active ltm
     *
     * @param String $active_ltm The name of active LTM device
     * @return Array
     *
     */
    function get_poolNames($active_ltm)
    {
        $cmd = '/usr/bin/python /var/www/chaniq/py/get_pool_names.py '.$active_ltm;
        //echo "<br>Command:" .$cmd." <br>";
        error_log(date("y-m-d H:i:s").": get_poolNames() - get_poolNames() called\n", 3, "/var/log/chaniqphp.log");
        exec($cmd, $output);
        
        //echo "<br>Output: " .$output[0];
        $rtn_out = explode(":", $output['0']);
        return $rtn_out;
    }
    
    function get_pool_names() {
        if(isset($_POST['DevIP']))
        {
            //$bigipIP = json_decode($_POST['DevIP']);
            $bigipIP = $_POST['DevIP'];
            //error_log(date("y-m-d H:i:s").": get_pool_names() - Device IP sent over POST\n", 3, "/var/log/chaniqphp.log");
            file_put_contents("/var/log/chaniqphp.log", "get_pool_names() Device IP: " . $bigipIP, FILE_APPEND);
        }
        
        //$echoOut = echoTest();
        //file_put_contents("/var/log/chaniqphp.log", "get_pool_names() EchoTest: " . $echoOut, FILE_APPEND);
        $poolNames = get_poolNames($bigipIP);

        foreach ($poolNames as $value) {
            file_put_contents("/var/log/chaniqphp.log", "Pool names: " . $value . "\n", FILE_APPEND);
        }
        $json = json_encode($poolNames);
        echo $json;
    }
?>