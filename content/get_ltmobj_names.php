<?php
    session_start();
    file_put_contents("/var/log/chaniqphp.log", "get_ltmobj_names.php UN: " .$_SESSION['username'] . " Role: " . $_SESSION['role'] . " LoggedIn: " . $_SESSION['loggedin'] . "\n", FILE_APPEND);
    if ($_SESSION['loggedin'] != true){
        session_unset();
        session_destroy();
        file_put_contents("/var/log/chaniqphp.log", "get_ltmobj_names.php redirection to login page!!\n", FILE_APPEND);
        header('Location: ../login.php');
    }
    //Admin Content - Visible if the logged-in user has admin role
    if ($_SESSION['role'] == 'guest'){
        header('Location: contentbase.php');
    }

    error_log(date("y-m-d H:i:s").": get_ltmobj_names() - callBack function php has been called\n", 3, "/var/log/chaniqphp.log");
    
    // Call get_ltmobj_names() by echo statement
    echo $_POST['method']();
    
    /**
     * Given the name of active LTM, get the list of health monitors of the active ltm
     *
     * @param String $active_ltm The name of active LTM device
     * @param String $obj_type The name of a LTM object type.
     *               1. VS
     *               2. POOL
     * @return Array
     *
     */
    function get_names($active_ltm, $objType)
    {
        $cmd = '/usr/bin/python /var/www/chaniq/py/get_ltmobj_names.py '.$active_ltm.' ' . escapeshellarg($objType);
        //echo "<br>Command:" .$cmd." <br>";
        error_log(date("y-m-d H:i:s").": get_ltmobj_names() - get_names() called. Dev IP: " . $active_ltm . " Profile Type: " . $objType . "\n", 3, "/var/log/chaniqphp.log");
        exec($cmd, $output);
        
        //echo "<br>Output: " .$output[0];
        $rtn_out = explode(":", $output['0']);
        return $rtn_out;
    }
    
    function get_ltmobj_names() {
        if(isset($_POST['DevIP']))
        {
            $bigipIP = $_POST['DevIP'];
            $objType = $_POST['LoadTypeName'];
            file_put_contents("/var/log/chaniqphp.log", "get_ltmobj_names() Device IP: " . $bigipIP."\n", FILE_APPEND);
        }
        
        //$echoOut = echoTest();
        //file_put_contents("/var/log/chaniqphp.log", "get_ltmobj_names(): " . $echoOut, FILE_APPEND);
        $objNames = get_names($bigipIP, $objType);

        foreach ($objNames as $value) {
            file_put_contents("/var/log/chaniqphp.log", "Object name: " . $value . "\n", FILE_APPEND);
        }
        $json = json_encode($objNames);
        echo $json;
    }
?>