<?php

    error_log(date("y-m-d H:i:s").": get_partition_names() - callBack function php has been called\n", 3, "/var/log/chaniqphp.log");
    
    // Call get_pool_names() by echo statement
    if (isset($_POST['jsonData'])){
        $jsonData = json_decode($_POST['jsonData']);
        file_put_contents("/var/log/chaniqphp.log", "get_partition_names.php File: " . $jsonData->phpFileName ."\n", FILE_APPEND);
        
        // Call the fuction chg_pool_build()
        echo ($jsonData->phpFileName)($jsonData);
    }
    else
        echo "Requried POST parameter is missing!";
    
    /**
     * Given the name of active LTM, get the list of pool names from the given active ltm
     *
     * @param String $active_ltm The name of active LTM device
     * @return Array
     *
     */
    function get_partition_names($jsonData) {
        $active_ltm = $jsonData->DevIP;
        file_put_contents("/var/log/chaniqphp.log", "get_partition_names() Device IP: " . $active_ltm . "\n", FILE_APPEND);
        
        $cmd = '/usr/bin/python /var/www/chaniq/py/get_partition_names.py '.$active_ltm;
        //echo "<br>Command:" .$cmd." <br>";
        error_log(date("y-m-d H:i:s").": get_partition_names() called\n", 3, "/var/log/chaniqphp.log");
        // Return format - Null (''), partition1:, part1:part2:
        $output = shell_exec($cmd);
        file_put_contents("/var/log/chaniqphp.log", "Partition names: " . $output . "\n", FILE_APPEND);
       
        $json = json_encode($output);
        echo $json;
    }
?>