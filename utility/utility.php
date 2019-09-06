<?php
function echoTest() {
    return "Echo Test";
}

/**
 * Determine if the logged-in user has admin role
 * 
 * @param None
 * @return Boolean TRUE if logged-in user is admin. Otherwise return FALSE
 */
function isadmin(){
    if($_SESSION['role']=='admin'){
        return true;
    }
    else
        return false;
}

/** 
 * Given an ini section name, return whole data of the section
 * 
 * @param String $secname Name of INI Section
 * @return String The name of ini section name
 * 
 */
function parse_ini_section_file (){
    $iniarray = parse_ini_file('/var/www/chaniq/config/chaniq.ini', TRUE);
    /* Error handling code */
    /* print_r($secdata); */
    return $iniarray;
}

/** 
 * Given an ini data name, return the value of the data
 * 
 * @param String $secname Name of INI Section 
 * @param String $inidata Name of INI data 
 */
function parse_ini_sec_val ($secname, $inidata){
    $iniarray = parse_ini_section_file();
    return print($iniarray[$secname][$inidata]);
}

/** 
 * Given an ini section name, return all values of the section (Key is not included)
 * 
 * @param String $parasecname Name of INI Section name
 * @return Array One dimension array of all values of the section
 *      
 */
function parse_ini_sec_vals ($parmsecname){
    $iniarray = parse_ini_section_file();
    $rtnarray = [];
    $cnt = 0;
    foreach ($iniarray as $section => $values){
        $myx = (string)$section; // Conversion Array to string
        //echo "Section Name: " . $section;
        if ($myx == $parmsecname ){
            foreach ($values as $key=>$value){
                $rtnarray[$cnt++] = (string)$value;
                //echo $rtnarray[$cnt];
            }
        }
    }
    return $rtnarray;
}

/**
 * Given an ini section name, return all keys of the section (Value is not included)
 *
 * @param String $parasecname Name of INI Section name
 * @return Array One dimension array of all keys of the section
 *
 */
function parse_ini_key_vals ($parmsecname){
    $iniarray = parse_ini_section_file();
    $rtnarray = [];
    $cnt = 0;
    foreach ($iniarray as $section => $values){
        $myx = (string)$section; // Conversion Array to string
        if ($myx == $parmsecname ){
            foreach ($values as $key=>$value){
                $rtnarray[$cnt++] = (string)$key;
            }
        }
    }
    return $rtnarray;
}

/** 
 * Given an ini section name, return all keys and values of the section
 * 
 * @param String $parasecname Name of INI Section name
 * @param String $valtype Constant type name of the Value - SUBNET(used with finding a list of subnets and VIPs), VALUE (used with finding mgmt IP address)
 *               Format1: Key = val1,val2,...,valn,  Format2: Key = val
 * @return Array Array of all keys and values of the section. Format Key1 => ( key2 =>val1, val2,...)
 *      
 */
function parse_ini_sec_keyvals ($parmsecname, $valtype){
    $iniarray = parse_ini_section_file();
    $rtnarray = [];
    $cnt = 0;
    if(empty($parmsecname)) return null;
    foreach ($iniarray as $section => $values){
        $myx = (string)$section; // Conversion Array to string
        //echo "Section Name: " . $section;
        if ($myx == $parmsecname ){
            foreach ($values as $key=>$value){
                if ($valtype == "SUBNET"){
                    $val_list = explode(",", $value);
                    $rtnarray[$key] = $val_list;
                }
                elseif ($valtype == "VALUE"){
                    $rtnarray[$key] = $value;
                }
                //echo "Key: " .$key."  Value: ".$value;
            }
        }
    }
    //echo print_r($rtnarray);
    return $rtnarray;
}

/** 
 * 
 * Given an VIP IP and its pool members' IP, return corresponding device group section name
 * 
 * @param String $vip IPv4 expression of VIP IP
 * @param Array  $poo_memberip Associate array of Pool members' IP (format {0, x.x.x.x, 1, x.y.z.a })
 * @param String $env_name Name of Environment (PRD, STG, QA, DEV)
 * @return String LTM Device Group Section name
 *      
 */
function find_ini_section($vip, $pool_memberip, $env_name){
    $section_name = "";
    $cnt = 0;
    switch ($env_name){
        // Search PRD_F5_SUBNETS section
        case "PRD":
            $sec_data = parse_ini_sec_keyvals("PRD_F5_SUBNETS", "SUBNET");
        case "STG":
            $sec_data = parse_ini_sec_keyvals("STG_F5_SUBNETS", "SUBNET");
            break;
        // Search LAB_F5_SUBNETS section
        case "QA":
            $sec_data = parse_ini_sec_keyvals("QA_F5_SUBNETS", "SUBNET");
        case "DEV":
            $sec_data = parse_ini_sec_keyvals("DEV_F5_SUBNETS", "SUBNET");
            break;
        case "STANDALONE":
            $sec_data = parse_ini_sec_keyvals("STANDALONE_F5_SUBNETS", "SUBNET");
            break;
        default:
            error_log(date("y-m-d H:i:s").": find_ini_section() - No matching Environment name found\n", 3, "/var/log/chaniqphp.log");
    }
    
    foreach ($pool_memberip as $pkey => $pval){
        $cnt = 0;
        //echo "pool member key: ".$pkey." pool member val:".$pval;
        //echo "<br></br>";
        foreach($sec_data as $key => $value){
            foreach($value as $vkey => $vvalue){
                //echo "PRD Count:".$cnt." Given IP:".$pval." vkey: ".$vkey." vvalue: ".$vvalue;
                //echo "<br></br>";
                if (cidr_match($pval, $vvalue)) {
                    error_log(date("y-m-d H:i:s").": find_ini_section() - CIDR-Mathcing found!".$key."\n", 3, "/var/log/chaniqphp.log");
                    return $section_name = $key;
                }
                $cnt++;
            }
        }
    }
    
    if (empty($section_name)){
        error_log( date("y-m-d H:i:s").": find_ini_section() - No Section found from INI\n", 3, "/var/log/chaniqphp.log");
        return $section_name;
    }
    else {
        return $section_name;
    }
    
}


/** 
 * Given an IPv4 IP address and CIDR expression, determine if the given IP is within the range of CIDR
 * 
 * @param String $name IPv4 IP address expression (e.g. 1.2.3.4)
 * @param String $cidr CIDR IPv4 IP address expression (e.g. 192.168.168.0/24)
 * @return Boolean TRUE if matching and FALSE if not matching.
 *  Test Cases
 *  cidr_match("1.2.3.4", "0.0.0.0/0") -> True
 *  cidr_match("127.0.0.1", "127.0.0.1/32") -> True
 *  cidr_match("127.0.0.1", "127.0.0.2/32") -> False
 *  cidr_match("127.0.0.1", "127.0.0.0/30") -> True
 *      
 */
function cidr_match($ip, $cidr)
{
    //echo "IP: ".$ip." CIDR: ".$cidr;
    list($subnet, $mask) = explode('/', $cidr);
    //echo "subnet: ".$subnet." mask: ".$mask;
    if ((ip2long($ip) & ~((1 << (32 - $mask)) - 1) ) == ip2long($subnet))
    { 
        //echo "Returning true from cidr_match";
        return true;
    }
    //echo "Returning false from cidr_match";
    return false;
}

/**
 * Given an Device Section name of INI, find the active ltm device name
 *
 * @param String $section_name INI Section Name of LTM Device group
 * @return String Active LTM device name
 *
 */
function find_active_ltm($section_name, $env_name){
    // Find Device Group name
    // $device_group format: section_name =>{(DNS_Name1, IP1), (DNS_Name2, IP2), ... }
    //echo "Param section name: " . $section_name;
    $device_group_members = parse_ini_sec_keyvals($section_name, "VALUE");
    //print_r($device_group_members);
    // If Env is "STANDARD", we assume there is only one ltm. Otherwise (PRD, STG, QA, DEV) we assume LTM device is HA pair
    if ($env_name == "STANDALONE"){
        foreach ($device_group_members as $dgkey => $dgval){
            error_log( date("y-m-d H:i:s").": find_active_ltm() - Key: " .$dgkey. " Value: " .$dgval."\n", 3, "/var/log/chaniqphp.log");
            return $dgval;
        }
            
    }
    else {
        // Check which device of a pair is an active LTM
        foreach ($device_group_members as $dgkey => $dgval){
            echo "<br> Key: " . $dgkey . "Value: " . $dgval . "<br>";
            $cmd = '/usr/bin/python /var/www/chaniq/py/get_tcpprofiles.py '.$dgkey. ' ' .$dgval;
            exec($cmd, $output);
            if ($output) return $dgval;
        }
    }

    // Failed in finding active ltm
    return "0.0.0.0";
    //return $active_ltm;
}

/** 
 * Given the name of active LTM, get the list of tcp profile of the active ltm
 * get_profiles() replaces this function
 * 
 * @param String $active_ltm The name of active LTM device
 * @return Array 
 *
 */
function get_tcpprofiles($active_ltm)
{
    echo "<br>Calling get_tcpprofiles.py: ".$active_ltm;
    $cmd = '/usr/bin/python /var/www/chaniq/py/get_tcpprofiles.py '.$active_ltm;
    echo "<br>Command:" .$cmd." <br>";
    exec($cmd, $output);

    //foreach ($output as $key => $value) {
    //    echo "Value in Util: Key: ".$key. " Value: " .$value;
    //}
    //echo "Value in Util: " . $output['0'];
    $rtn_out = explode(":", $output['0']);
    echo "<br>";
    return $rtn_out;
}

/**
 * Given the name of active LTM, get the list of HTTP profile of the active ltm
 *
 * @param String $active_ltm The name of active LTM device
 * @param String $pf_type The name of a profile type. 
 *               1 - TCP Profile
 *               2 - Persistence Profile
 *               3 - HTTP Profile
 *               4 - Client SSL Profile
 *               5 - Server SSL Profile
 * @return Array
 *
 */
function get_profiles($active_ltm, $pf_type)
{
    //echo "<br>Calling get_profiles.py: ".$active_ltm;
    $cmd = '/usr/bin/python /var/www/chaniq/py/get_profiles.py '.$active_ltm.' ' .$pf_type;
    //echo "<br>Command:" .$cmd." <br>";
    exec($cmd, $output);

    //echo "<br>Output: " .$output[0];
    $rtn_out = explode(":", $output['0']);
    return $rtn_out;
}

/**
 * Given the name of active LTM, get the list of health monitors of the active ltm
 *
 * @param String $active_ltm The name of active LTM device
 * @param String $mon_type The name of a monitor type.
 *               1. TCP
 *               2. HTTP and HTTPS
 *               3. UDP
 *               4. TCP Half_open
 *               5. Gateway ICMP
 *               6. External
 * @return Array
 *
 */
function get_healthmon($active_ltm, $mon_type)
{
    $cmd = '/usr/bin/python /var/www/chaniq/py/get_healthmon.py '.$active_ltm.' ' .$mon_type;
    //echo "<br>Command:" .$cmd." <br>";
    error_log(date("y-m-d H:i:s").": get_healthmon() - get_healthmon() called\n", 3, "/var/log/chaniqphp.log");
    exec($cmd, $output);
    
    //echo "<br>Output: " .$output[0];
    $rtn_out = explode(":", $output['0']);
    return $rtn_out;
}

/**
 * Given a name of array of Select-Option value, Element Name, default Lable and Value name, generate Select HTML code
 * Ref: https://www.tutdepot.com/dynamic-select-menu-with-php/
 *
 * @param Array $opt_arry The array of dynamic option value
 * @param String $element_name Name used for Label and Select
 * @param String $label Name for Label Title
 * @param String $init_value Default Option value
 * @return String HTML code for Select
 *
 */
function dynamic_select($opt_array, $element_name, $label = '', $init_value = '') {
    $menu = '';
    if ($label != '') $menu .= '
    	<label for="'.$element_name.'">'.$label.'</label>';
    $menu .= '
    	<select name="'.$element_name.'" id="'.$element_name.'">';
    if (empty($_REQUEST[$element_name])) {
        $curr_val = $init_value;
    } else {
        $curr_val = $_REQUEST[$element_name];
    }
/*     foreach ($opt_array as $key => $value) {
        $menu .= '
			<option value="'.$key.'"';
        if ($key == $curr_val) $menu .= ' selected="selected"';
        $menu .= '>'.$value.'</option>';
    } */
    foreach ($opt_array as $key => $value) {
        $menu .= '
			<option ';
        if ($value == $curr_val) $menu .= ' selected="selected"';
        $menu .= '>'.$value.'</option>';
    }
    $menu .= '
    	</select>';
    echo $menu;
    return $menu;
}

/**
 * Given a name of array of Select-Option value, Element Name, default Lable and Value name, generate Select HTML code
 * Ref: https://www.tutdepot.com/dynamic-select-menu-with-php/
 *
 * @param Array $opt_arry The array of dynamic option value
 * @param String $element_name Name used for Label and Select
 * @param String $label Name for Label Title
 * @param String $init_value Default Option value
 * @return String HTML code for Select
 *
 */
function dynamic_multi_select($opt_array, $element_name, $label = '', $init_value = '') {
    $menu = '';
    if ($label != '') $menu .= '
    	<label for="'.$element_name.'">'.$label.'</label>';
    $menu .= '
    	<select multiple="multiple" name="'.$element_name.'" id="'.$element_name.'">';
    if (empty($_REQUEST[$element_name])) {
        $curr_val = $init_value;
    } else {
        $curr_val = $_REQUEST[$element_name];
    }
    /*     foreach ($opt_array as $key => $value) {
     $menu .= '
     <option value="'.$key.'"';
     if ($key == $curr_val) $menu .= ' selected="selected"';
     $menu .= '>'.$value.'</option>';
     } */
    foreach ($opt_array as $key => $value) {
        $menu .= '
			<option ';
        if ($value == $curr_val) $menu .= ' selected="selected"';
        $menu .= '>'.$value.'</option>';
    }
    $menu .= '
    	</select>';
    echo $menu;
    return $menu;
}

/**
 * Given the output of configuration conflict, return the result of the conflict
 *
 * @param String $conflictOutput The result string of the configuraion conflict
 * @return Bool true or false
 *
 */

function check_config_conflict($conflictOutput) {
    if ($conflictOutput == "** Configuration conflict **") {
        return true;        
    }
    if ($conflictOutput == "** No configuration conflict **") {
        return false;
    }
}

/**
 * Given array of chosen parameters, check object colflict
  *
 * @param String $active_ltm The IP address of active LTM
 * @param String $vs_env Name of environment name
 * @param String $vs_dnsname Name of Virtual server DNS name
 * @param String $vs_dest Virtual IP address of Virtual server
 * @param String $vs_port Port number of Virtual server
 * @param Array $vs_poolmembername Array of pool members' name
 * @param Array $vs_poolmemberip Array of pool members' IP
 * @param Array $vs_poolmemberport Array of pool members' port 
 * @return String Empty string or found conflicts
 *
 */

function check_object_conflict($active_ltm, $vs_env, $vs_dnsname, $vs_dest, $vs_port, $vs_poolmembername, $pool_memberip, $pool_memberport) {
    /* Integer $REQ_TYPE Constant request type value - 100: VS, 200:Pool, 201:pool memebr, 300: profiles, 400: Persistence, 500: Node */
    $evalout = '';
    // Node Name and IP conflict check
    // echo 'arry: ' .escapeshellarg(json_encode($vs_poolmembername));
    
    $cmd = '/usr/bin/python /var/www/chaniq/py/check_object_conflict.py '.$active_ltm.' ' .$vs_env.' ' .$vs_dnsname.' '.$vs_dest.' '.$vs_port.' '. escapeshellarg(json_encode($vs_poolmembername)).' '. escapeshellarg(json_encode($pool_memberip)).' '. escapeshellarg(json_encode($pool_memberport));
    
    //exec($cmd, $output);
    $output = shell_exec($cmd);
    //echo "Type of return value: " .gettype($output) ."<br>";
    //echo "Output: " .$output ."<br>";
    $outputdata = json_decode($output, true);
    //Print returned dictionary
    //var_dump($outputdata);

    return $outputdata;
}

function build_nodes($allPostData) {
    // Parsing variables
    $vs_dnsname = $allPostData['vs_dnsname'];
    $vs_dest = $allPostData['vs_dest'];
    $vs_port = $allPostData['vs_port'];
    $vs_desc = $allPostData['vs_desc'];
    $vs_env = $allPostData['vs_env'];
    $vs_tcpprofile = $allPostData['vs_tcpprofile'];
    $vs_poolmon = $allPostData['vs_poolmon'];
    $vs_persistence = $allPostData['vs_persistence'];
    $vs_redirect = $allPostData['vs_redirect'];
    $vs_type = $allPostData['vs_type'];
    if ($vs_type == "Standard"){
        $vs_httpprofile = $allPostData['vs_httpprofile'];
        $vs_sslclient = $allPostData['vs_sslclient'];
        $vs_sslserver = $allPostData['vs_sslserver'];
    }
    $pool_membername = $allPostData['pool_membername'];
    $pool_memberip = $allPostData['pool_memberip'];
    $pool_memberport = $allPostData['pool_memberport'];
    $pool_membermon = $allPostData['pool_membermon'];
    $active_ltm = $allPostData['active_ltm'];
    $eval_result = $allPostData['eval_result'];
    $active_ltm = $allPostData['active_ltm'];
    
    /*
    foreach ($pool_membername as $key => $value) {
        echo "key: " .$key . "    value: " .$value ."<br>";
    }
    */
    
    //1. Create nodes
    $cmd = '/usr/bin/python /var/www/chaniq/py/build_nodes.py '.$active_ltm.' '. escapeshellarg(json_encode($pool_membername)).' '. escapeshellarg(json_encode($pool_memberip));
        
    $output = shell_exec($cmd);
    //echo "Output: " .$output ."<br>";
    $outputdata = json_decode($output, true);
    
    return $outputdata;
    
}

/*
 * $active_ltm: string, LTM Device IP
 * $pool_membername: List of Pool member names
 * $pool_memberip: List of Pool member IP addresses
 */
function build_nodes2($active_ltm, $pool_membername, $pool_memberip) {

     foreach ($pool_membername as $key => $value) {
     echo "key: " .$key . "    value: " .$value ."<br>";
     }
    
    //1. Create nodes
    $cmd = '/usr/bin/python /var/www/chaniq/py/build_nodes.py '.$active_ltm.' '. escapeshellarg(json_encode($pool_membername)).' '. escapeshellarg(json_encode($pool_memberip));
    
    $output = shell_exec($cmd);
    //echo "Output: " .$output ."<br>";
    $outputdata = json_decode($output, true);
    
    return $outputdata;
    
}
function build_pools($allPostData) {
    // Parsing variables
    $vs_dnsname = $allPostData['vs_dnsname'];
    $vs_dest = $allPostData['vs_dest'];
    $vs_port = $allPostData['vs_port'];
    $vs_desc = $allPostData['vs_desc'];
    $vs_env = $allPostData['vs_env'];
    $vs_tcpprofile = $allPostData['vs_tcpprofile'];
    $vs_poolmon = $allPostData['vs_poolmon'];
    $vs_persistence = $allPostData['vs_persistence'];
    $vs_redirect = $allPostData['vs_redirect'];
    $vs_type = $allPostData['vs_type'];
    if ($vs_type == "Standard"){
        $vs_httpprofile = $allPostData['vs_httpprofile'];
        $vs_sslclient = $allPostData['vs_sslclient'];
        $vs_sslserver = $allPostData['vs_sslserver'];
    }
    $pool_membername = $allPostData['pool_membername'];
    $pool_memberip = $allPostData['pool_memberip'];
    $pool_memberport = $allPostData['pool_memberport'];
    $pool_membermon = $allPostData['pool_membermon'];
    $active_ltm = $allPostData['active_ltm'];
    $eval_result = $allPostData['eval_result'];
    $active_ltm = $allPostData['active_ltm'];
    
    //2. Create pool
    $cmd = '/usr/bin/python /var/www/chaniq/py/build_pools.py '.$active_ltm.' '. $vs_dnsname.' '. $vs_port.' '. $vs_env.' '. $vs_poolmon.' '. escapeshellarg(json_encode($pool_membername)).' '. escapeshellarg(json_encode($pool_memberip)).' '. escapeshellarg(json_encode($pool_memberport)).' '. escapeshellarg(json_encode($pool_membermon));
    
    $output = shell_exec($cmd);
    //echo "Output: " .$output ."<br>";
    $outputdata = json_decode($output, true);

    return $outputdata;
    
}

function build_vs_s($allPostData) {
    // Parsing variables
    $vs_dnsname = $allPostData['vs_dnsname'];
    $vs_dest = $allPostData['vs_dest'];
    $vs_port = $allPostData['vs_port'];
    $vs_desc = $allPostData['vs_desc'];
    $vs_env = $allPostData['vs_env'];
    $vs_tcpprofile = $allPostData['vs_tcpprofile'];
    $vs_poolmon = $allPostData['vs_poolmon'];
    $vs_persistence = $allPostData['vs_persistence'];
    $vs_redirect = $allPostData['vs_redirect'];
    $vs_type = $allPostData['vs_type'];
    if ($vs_type == "Standard"){
        $vs_httpprofile = $allPostData['vs_httpprofile'];
        $vs_sslclient = $allPostData['vs_sslclient'];
        $vs_sslserver = $allPostData['vs_sslserver'];
    }
    $pool_membername = $allPostData['pool_membername'];
    $pool_memberip = $allPostData['pool_memberip'];
    $pool_memberport = $allPostData['pool_memberport'];
    $pool_membermon = $allPostData['pool_membermon'];
    $vs_irule = $allPostData['vs_irule'];
    $vs_snatpool = $allPostData['vs_snatpool'];
    $vs_policy = $allPostData['vs_policy'];
    $active_ltm = $allPostData['active_ltm'];
    $eval_result = $allPostData['eval_result'];
    $active_ltm = $allPostData['active_ltm'];
    
    //3. Create VS
    // Use escapeshellarg() with $vs_desc variable so that if the variable includes space, the whole string description is considered as one variable
    // e.g. $vs_desc="Web Server" W/O escapeshellarg(), Web and Server are considered as two separate arguments
    $cmd = '/usr/bin/python /var/www/chaniq/py/build_vs_s.py '.$active_ltm.' '. $vs_dnsname.' '. $vs_dest.' '. $vs_port.' '. escapeshellarg($vs_desc) .' '. $vs_env .' '. $vs_tcpprofile.' '. $vs_persistence.' '. $vs_redirect.' '. $vs_type.' '. $vs_httpprofile.' '. $vs_sslclient.' '. $vs_sslserver.' '. $vs_irule.' '. $vs_snatpool.' '. $vs_policy;

    $output = shell_exec($cmd);
    //echo "Output: " .$output ."<br>";
    $outputdata = json_decode($output, true);
    
    return $outputdata;
    
}

// Load all BIG-IP names and IP addresses from chaniq.ini file
function load_all_bigips() {
    /*
     * PRD_DEVICE_GROUP, STG_DEVICE_GROUP, QA_DEVICE_GROUP, DEV_DEVICE_GROUP, STANDALONE_DEVICE_GROUP
     * Retrieve all BIG-IP devices from each device group
     */
    $devGroups = array("PRD_DEVICE_GROUP", "STG_DEVICE_GROUP", "QA_DEVICE_GROUP", "DEV_DEVICE_GROUP", "STANDALONE_DEVICE_GROUP");
    $rtnDevices = array();
    foreach ($devGroups as $devGroup){
        $devClstNames = parse_ini_key_vals($devGroup);
        foreach ($devClstNames as $devClstName) {
            $rtnDevices += parse_ini_sec_keyvals($devClstName, "VALUE");
        }
    }
    return $rtnDevices;
}

//Read the parent URL parameters and return a query parameter value against a given key
//e.g. URL: http://www.example.com/?go=chg_profile
//     GetParentURLParameter('go')
//     Return: chg_profile
function GetParentURLParameter($sParam)
{
    $parentURL = $_SERVER['HTTP_REFERER'];
    
    $parentQry = explode('?', $parentURL);
    //echo "In utility.php - GetParentURLParameter(): Query parameters: " . $parentQry[1] . "\r\n";
    
    parse_str($parentQry[1], $output);
    return $output[$sParam];
}

?>
