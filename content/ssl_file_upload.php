<?php
require_once(__DIR__ . '/../utility/chaniqLogger.php');
    session_start();
    #file_put_contents("/var/log/chaniqphp.log", "ssl_file_upload.php.php UN: " .$_SESSION['username'] . " Role: " . $_SESSION['role'] . " LoggedIn: " . $_SESSION['loggedin'] . "\n", FILE_APPEND);
    $logger->info("ssl_file_upload.php.php UN: " .$_SESSION['username'] . " Role: " . $_SESSION['role'] . " LoggedIn: " . $_SESSION['loggedin']);
    if ($_SESSION['loggedin'] != true){
        session_unset();
        session_destroy();
        #file_put_contents("/var/log/chaniqphp.log", "ssl_file_upload.php redirection to login page!!\n", FILE_APPEND);
        $logger->info("ssl_file_upload.php redirection to login page!!");
        header('Location: ../login.php');
    }
    //Admin Content - Visible if the logged-in user has admin role
    if ($_SESSION['role'] == 'guest'){
        header('Location: contentbase.php');
    }

    $target_dir = "/var/www/chaniq/log/tmp/";
    $target_file = $target_dir . basename($_FILES["file"]["name"]);
    $uploadOk = 1;
    $fileExtention = strtolower(pathinfo($target_file,PATHINFO_EXTENSION));

    $sslImpType = $_POST['sslImpType'];
    $sslImpName = $_POST['sslImpName'];
    
    // Check if file already exists
    $newTargetFile = $target_dir . $sslImpName;
    if ( file_exists($target_file.'.key') || file_exists($target_file.'.crt') ) {
        echo "Error: File already exists.<br>";
        $uploadOk = 0;
    }
    // Check file size
    if ($_FILES["file"]["size"] == 0){
        echo "Error: File is not chosen.<br>";
        $uploadOk = 0;
    }
    if ($_FILES["file"]["size"] > 1024000) {
        echo "Error: File size should be less than 1MB.<br>";
        $uploadOk = 0;
    }
    
    // Allow certain file formats - txt, crt, cer, key, p12, pfx, pem, csr, der, crl
    if($fileExtention != "txt" && $fileExtention != "crt" && $fileExtention != "cer" && $fileExtention != "key" && $fileExtention != "p12" && $fileExtention != "pfx" && $fileExtention != "csr" && $fileExtention != "pem" && $fileExtention != "der" && $fileExtention != "crl") {
        echo "Error: Allowed File formats: txt, crt, cer, key, p12 & pfx.<br>";
        $uploadOk = 0;
    }
        
    if ($uploadOk == 0) {
        echo 'File Upload failed: ' . $_FILES['file']['error'] . '<br>';
    }
    else {
        if ($sslImpType == 'Key'){
            //move_uploaded_file($_FILES['file']['tmp_name'], '/var/www/chaniq/log/tmp/' . $_FILES['file']['name']);
            move_uploaded_file($_FILES['file']['tmp_name'], '/var/www/chaniq/log/tmp/' . $sslImpName . '.key');
        }
        else if ($sslImpType == 'Certificate'){
            move_uploaded_file($_FILES['file']['tmp_name'], '/var/www/chaniq/log/tmp/' . $sslImpName . '.crt');
        }
        else if ($sslImpType == 'PKCS 12 (IIS)'){
            move_uploaded_file($_FILES['file']['tmp_name'], '/var/www/chaniq/log/tmp/' . $sslImpName . '.pfx');
            //move_uploaded_file($_FILES['file']['tmp_name'], '/var/www/chaniq/log/tmp/' . $sslImpName . '.key');
        }
        echo 'Success';
    }
?>