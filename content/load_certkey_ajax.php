<?php
//if(isset($_POST)==TRUE && empty($_POST)==FALSE):
// If you put variables to save data from POST, it wont work. I moved the part under load_certkey_ajax()
error_log(date("y-m-d H:i:s").": load_certkey_ajax.php() - callBack function php has been called\n", 3, "/var/log/chaniqphp.log");
// Call load_certkey_ajax() by echo statement
if (isset($_POST['jsonData'])){
    $jsonParam = json_decode($_POST['jsonData']);
    file_put_contents("/var/log/chaniqphp.log", "load_certkey_ajax.php File: " . $jsonParam->PhpFileName ."\n", FILE_APPEND);
    
    // Call the fuction load_certkey_ajax()
    echo ($jsonParam->PhpFileName)($jsonParam);
}
else{
    
    echo "Required Post parameter is missing";
}

//'PhpFileName':'', 'DevIP':'', 'P_name':'', 'P_part':'' 
function load_certkey_ajax($jsonParam) {
    file_put_contents("/var/log/chaniqphp.log", "load_certkey_ajax() called\n", FILE_APPEND);
    
    $devIP = $jsonParam->DevIP;

    file_put_contents("/var/log/chaniqphp.log", "load_certkey_ajax() 
          Device IP: " . $devIP . "\n", FILE_APPEND);
    
    $cmd = '/usr/bin/python /var/www/chaniq/py/load_certkey_ajax.py ' . escapeshellarg($devIP);
        
    $output = shell_exec($cmd);
    error_log(date("y-m-d H:i:s").": After python call -load_certkey_ajax.php() load_certkey_ajax() function called!\n", 3, "/var/log/chaniqphp.log");
    
    /*
    $outputdata = json_decode($output, true);
    ksort($outputdata);
    */
    
    echo $output;
}
?>