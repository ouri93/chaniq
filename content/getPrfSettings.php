<?php
require_once(__DIR__ . '/../utility/chaniqLogger.php');
    session_start();
    #file_put_contents("/var/log/chaniqphp.log", "getPrfSettings.php UN: " .$_SESSION['username'] . " Role: " . $_SESSION['role'] . " LoggedIn: " . $_SESSION['loggedin'] . "\n", FILE_APPEND);
    $logger->info("getPrfSettings.php UN: " .$_SESSION['username'] . " Role: " . $_SESSION['role'] . " LoggedIn: " . $_SESSION['loggedin']);
    if ($_SESSION['loggedin'] != true){
        session_unset();
        session_destroy();
        #file_put_contents("/var/log/chaniqphp.log", "getPrfSettings.php redirection to login page!!\n", FILE_APPEND);
        $logger->info("getPrfSettings.php redirection to login page!!");
        header('Location: ../login.php');
    }
    //Admin Content - Visible if the logged-in user has admin role
    if ($_SESSION['role'] == 'guest'){
        header('Location: contentbase.php');
    }

    #error_log(date("y-m-d H:i:s").": getPrfSettings() - callBack function php has been called\n", 3, "/var/log/chaniqphp.log");
    $logger->info("getPrfSettings() - callBack function php has been called");
    
    // Call getPrfSettings() by echo statement
    echo $_POST['method']($logger);
    
    /**
     * Given the name of active LTM, and Profile Name, retrieve the profile setting and return to php
     *
     * @param String $active_ltm The name of active LTM device
     * @param String $prfType The name of Profile Type
     * @param String $parParName This variable used to dual purpose. In Profile Change mode it stores selected profile name
     *                                                               In Profile build mode, it stores selected parent profile name
     * @return Array
     *
     */
    function getSettings($active_ltm, $prfType, $parPrfName, $prfMode, $logger)
    {
        $cmd = '/usr/bin/python /var/www/chaniq/py/getPrfSettings.py '.$active_ltm.' ' . escapeshellarg($prfType) .' '.escapeshellarg($parPrfName).' '.escapeshellarg($prfMode);
        //echo "<br>Command:" .$cmd." <br>";
        #error_log(date("y-m-d H:i:s").": getPrfSettings.php getSettings() called\n", 3, "/var/log/chaniqphp.log");
        $logger->info("getPrfSettings.php getSettings() called");
        exec($cmd, $output);
        
        //$rtn_out = explode(":", $output['0']);
        //return $rtn_out;
        return $output[0];
    }
    //DevIP:arr[1], PrfType:prfType, ParPrfName: parPrfName 
    function getPrfSettings($logger) {
        if(isset($_POST['DevIP']))
        {
            //$bigipIP = json_decode($_POST['DevIP']);
            $bigipIP = $_POST['DevIP'];
            $prfType = $_POST['LoadTypeName'];
            $parPrfName = $_POST['ParPrfName'];
            $prfMode = $_POST['PrfMode'];
            
            //error_log(date("y-m-d H:i:s").": getPrfSettings() - Device IP sent over POST\n", 3, "/var/log/chaniqphp.log");
            #file_put_contents("/var/log/chaniqphp.log", "getPrfSettings.php getPrfSettings() \nDevice IP: " . $bigipIP . "\nProfile Type: " . $prfType . "\nParent Profile or Selected Profile name: " . $parPrfName . "\nProfile Build-Change: " . $prfMode . "\n", FILE_APPEND);
            $logger->info("getPrfSettings.php getPrfSettings() \nDevice IP: " . $bigipIP . "\nProfile Type: " . $prfType . "\nParent Profile or Selected Profile name: " . $parPrfName . "\nProfile Build-Change: " . $prfMode);
        }
        
        $prfSettings = getSettings($bigipIP, $prfType, $parPrfName, $prfMode, $logger);

        //file_put_contents("/var/log/chaniqphp.log", $prfType . "(" . $parPrfName . ") Profile Settings: " . $prfSettings . "\n", FILE_APPEND);
        return $prfSettings;
    }
?>