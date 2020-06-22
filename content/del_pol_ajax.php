<?phprequire_once(__DIR__ . '/../utility/chaniqLogger.php');

session_start();
#file_put_contents("/var/log/chaniqphp.log", "del_pol_ajax.php UN: " .$_SESSION['username'] . " Role: " . $_SESSION['role'] . " LoggedIn: " . $_SESSION['loggedin'] . "\n", FILE_APPEND);
$logger->info("del_pol_ajax.php UN: " .$_SESSION['username'] . " Role: " . $_SESSION['role'] . " LoggedIn: " . $_SESSION['loggedin']);
if ($_SESSION['loggedin'] != true){
    session_unset();
    session_destroy();
    #file_put_contents("/var/log/chaniqphp.log", "del_pol_ajax.php redirection to login page!!\n", FILE_APPEND);
    $logger->info("del_pol_ajax.php redirection to login page!!");
    header('Location: ../login.php');
}
//Admin Content - Visible if the logged-in user has admin role
if ($_SESSION['role'] == 'guest'){
    header('Location: contentbase.php');
}

//if(isset($_POST)==TRUE && empty($_POST)==FALSE):
// If you put variables to save data from POST, it wont work. I moved the part under del_pol_ajax()
#error_log(date("y-m-d H:i:s").": del_pol_ajax.php() - callBack function php has been called\n", 3, "/var/log/chaniqphp.log");
$logger->info("del_pol_ajax.php() - callBack function php has been called");
// Call del_pol_ajax() by echo statement
if (isset($_POST['jsonData'])){
    $jsonParam = json_decode($_POST['jsonData']);
    if ($jsonParam->polType == 'draft'){
        $polData = json_decode($_POST['dftPolData']);
    }
    else if ($jsonParam->polType == 'published'){
        $polData = json_decode($_POST['pubPolData']);
    }
    #file_put_contents("/var/log/chaniqphp.log", "del_pol_ajax.php File: " . $jsonParam->PhpFileName ."\n", FILE_APPEND);
    $logger->info("del_pol_ajax.php File: " . $jsonParam->PhpFileName);
    
    // Call the fuction del_pol_ajax()
    echo ($jsonParam->PhpFileName)($jsonParam, $polData, $logger);
}
else{
    
    echo "Required Post parameter is missing";
}

//'PhpFileName':'del_pol_ajax', 'DevIP':arr[1], 'polType':'draft|published'
function del_pol_ajax($jsonParam, $polData, $logger) {
    #file_put_contents("/var/log/chaniqphp.log", "del_pol_ajax() called\n", FILE_APPEND);
    $logger->info("del_pol_ajax() called");
    
    $devIP = $jsonParam->DevIP;
    $polType = $jsonParam->polType;

    #file_put_contents("/var/log/chaniqphp.log", "del_pol_ajax() Device IP: " . $devIP . "\nPolicy Status: " . $polType . "\n", FILE_APPEND);
    $logger->info("del_pol_ajax() Device IP: " . $devIP . "\nPolicy Status: " . $polType);
    
    // JSON encoded data passed to Python must be loaded by json.loads() in Python code 
    // e.g. parsedData = json.loads(dftPolData) then use parsedData[idx] format to access data
    // Ref: https://stackoverflow.com/questions/46866730/sending-array-from-php-to-python-and-then-parse-in-python/46866791
    $PolData = json_encode($polData);
    
    $cmd = '/usr/bin/python /var/www/chaniq/py/del_pol_ajax.py ' . escapeshellarg($devIP) . ' ' . escapeshellarg($PolData) . ' ' . escapeshellarg($polType);
        
    $output = shell_exec($cmd);
    #error_log(date("y-m-d H:i:s").": After python call -del_pol_ajax.php() del_pol_ajax() function called!\n", 3, "/var/log/chaniqphp.log");
    $logger->info("After python call -del_pol_ajax.php() del_pol_ajax() function called!");
    
    /*
    $outputdata = json_decode($output, true);
    ksort($outputdata);
    */
    
    echo $output;
}
?>