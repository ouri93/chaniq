<?php

    error_log(date("y-m-d H:i:s").": get_healthmon_settings() - callBack function php has been called\n", 3, "/var/log/chaniqphp.log");
    
    // Call get_pool_monitors() by echo statement
    echo $_POST['phpFile']();
    
    function get_healthmon_settings() {
        if(isset($_POST['DevIP']))
        {
            //$bigipIP = json_decode($_POST['DevIP']);
            $bigipIP = $_POST['DevIP'];
            $monType = $_POST['MonType'];
            $parMonType = $_POST['ParMonType'];
            //error_log(date("y-m-d H:i:s").": get_pool_monitors() - Device IP sent over POST\n", 3, "/var/log/chaniqphp.log");
            file_put_contents("/var/log/chaniqphp.log", "get_healthmon_settings() Device IP: " . $bigipIP . " Mon Type: " . $monType . " Parent Mon: " . $parMonType . "\n", FILE_APPEND);
        }

        $cmd = '/usr/bin/python /var/www/chaniq/py/get_healthmon_settings.py '. $bigipIP . ' ' . escapeshellarg($monType) . ' ' . escapeshellarg($parMonType);
        //echo "<br>Command:" .$cmd." <br>";
        error_log(date("y-m-d H:i:s").": get_healthmon_settings() - get_healthmon_settings() called\n", 3, "/var/log/chaniqphp.log");
        exec($cmd, $output);

        //$json = json_decode($output, true);
        
        file_put_contents("/var/log/chaniqphp.log", "Returned Exec() Output: " . $output[0] ."\n", FILE_APPEND);
        
        echo $output;
    }
?>