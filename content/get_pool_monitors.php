<?php
    echo $_POST["method"]();
    
    function get_pool_monitors() {
        if(isset($_POST['bigipIP']))
        {
            $bigipIP = json_decode($_POST['bigipIP']);
        }
        $poolMonitors = get_healthmon($bigipIP, "ALL");
        $json = json_encode($poolMonitors);
        echo $json;
    }
?>