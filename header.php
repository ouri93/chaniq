<?php
require_once(__DIR__ . '/utility/chaniqLogger.php');

session_start();
if ($_SESSION['loggedin'] != true){
    $logger->info("header.php - Unauthen user - Redirect to login page");
    #file_put_contents("/var/www/chaniq/log/chaniq-php.log", "header.php - Unauthen user - Redirect to login page\n", FILE_APPEND);
    session_unset();
    session_destroy();
    header('Location: login.php');
}
?>
<html>
    <head>
        <meta charset="UTF-8">
        <link rel="stylesheet" href="./css/style.css" type="text/css" media="screen" />
        <script type="text/javascript" src="js/script.js"></script> 
        <!-- For Produciton 
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>
        <script> window.jQuery || document.write("<script src='/js/jquery-3.2.1.min.js'><\/script>"); </script>  
        -->
        
        <!-- For Development  -->
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.js"> </script>
        <script> window.jQuery || document.write("<script src='/js/jquery-3.2.1.js'><\/script>"); </script>  
                 
        <script type="text/javascript" src="js/chaniq_jquery.js"></script>
        <title>Chan-IQ - BIG-IP Management System</title>
        <style>
            .navbar_user
            {
                font-family: Calibri, Arial, Tahoma;
                font-size: 20px;
                font-weight: bold;
                color: #888888;
                font-weight:1000;
            }
        </style>
    </head>
    <body>
        <div id="header" >
            <div id="logo">
                <a href="index.php"><img src="./images/chaniq_top-180x50.png" ></a>
            </div>
            <div id="navbar" align="right" class="navbar_user" >
                <?php
                    echo 'User: '.$_SESSION['username'].' ( '.$_SESSION['role'].' )&nbsp;&nbsp;&nbsp;&nbsp;<a href="login.php?action=logout">Logout</a>&nbsp;&nbsp;';                    
                ?>
                
            </div>
        </div>
        
