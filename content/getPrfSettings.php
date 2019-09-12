<?php

    error_log(date("y-m-d H:i:s").": getPrfSettings() - callBack function php has been called\n", 3, "/var/log/chaniqphp.log");
    
    // Call getPrfSettings() by echo statement
    echo $_POST['method']();
    
    /**
     * Given the name of active LTM, and Profile Name, retrieve the profile setting and return to php
     *
     * @param String $active_ltm The name of active LTM device
     * @param String $prfType The name of Profile Type
     * @param String $parParName The name of Parent Profile name
     * @return Array
     *
     */
    function getSettings($active_ltm, $prfType, $parPrfName, $prfMode)
    {
        $cmd = '/usr/bin/python /var/www/chaniq/py/getPrfSettings.py '.$active_ltm.' ' . escapeshellarg($prfType) .' '.escapeshellarg($parPrfName).' '.escapeshellarg($prfMode);
        //echo "<br>Command:" .$cmd." <br>";
        error_log(date("y-m-d H:i:s").": getPrfSettings.php getSettings() called\n", 3, "/var/log/chaniqphp.log");
        exec($cmd, $output);
        
        //$rtn_out = explode(":", $output['0']);
        //return $rtn_out;
        return $output[0];
    }
    //DevIP:arr[1], PrfType:prfType, ParPrfName: parPrfName 
    function getPrfSettings() {
        if(isset($_POST['DevIP']))
        {
            //$bigipIP = json_decode($_POST['DevIP']);
            $bigipIP = $_POST['DevIP'];
            $prfType = $_POST['LoadTypeName'];
            $parPrfName = $_POST['ParPrfName'];
            $prfMode = $_POST['PrfMode'];
            
            //error_log(date("y-m-d H:i:s").": getPrfSettings() - Device IP sent over POST\n", 3, "/var/log/chaniqphp.log");
            file_put_contents("/var/log/chaniqphp.log", "getPrfSettings.php getPrfSettings() Device IP: " . $bigipIP . "\nProfile Type: " . $prfType . "\nParent Profile name: " . $parPrfName . "\nProfile Build-Change: " . $prfMode . "\n", FILE_APPEND);
        }
        
        $prfSettings = getSettings($bigipIP, $prfType, $parPrfName, $prfMode);

        //file_put_contents("/var/log/chaniqphp.log", $prfType . "(" . $parPrfName . ") Profile Settings: " . $prfSettings . "\n", FILE_APPEND);
        return $prfSettings;
    }
?>