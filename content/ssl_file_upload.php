<?php

    $target_dir = "/var/www/chaniq/log/tmp/";
    $target_file = $target_dir . basename($_FILES["file"]["name"]);
    $uploadOk = 1;
    $allowedFileType = strtolower(pathinfo($target_file,PATHINFO_EXTENSION));

    // Check if file already exists
    if (file_exists($target_file)) {
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
    
    // Allow certain file formats
    if($allowedFileType != "txt" && $allowedFileType != "crt" && $allowedFileType != "cer" && $allowedFileType != "key" && $allowedFileType != "p12" && $allowedFileType != "pfx" ) {
        echo "Error: Allowed File formats: txt, crt, cer, key, p12 & pfx.<br>";
        $uploadOk = 0;
    }
        
    if ($uploadOk == 0) {
        echo 'File Upload failed: ' . $_FILES['file']['error'] . '<br>';
    }
    else {
        move_uploaded_file($_FILES['file']['tmp_name'], '/var/www/chaniq/log/tmp/' . $_FILES['file']['name']);
        echo 'Success';
    }
?>