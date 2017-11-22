<html>
    <head>
        <meta charset="UTF-8">
        <link rel="stylesheet" href="./css/style.css" type="text/css" media="screen" />
        <script type="text/javascript" src="js/script.js"></script> 
        <!-- 
        For Produciton 
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js" </script>
        <script> window.jQuery || document.write("<script src='js/jquery-3.2.1.min.js'><\/script>");  
        -->

        <!-- For Development --> 
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.js" </script>
        <script> window.jQuery || document.write("<script src='js/jquery-3.2.1.js'><\/script>"); </script>  
                 
        <script type="text/javascript" src="js/chaniq_jquery.js"></script>
        <title>Chan-IQ - BIG-IP Management System</title>
    </head>
    <body>
        <div id="header">
            <div id="logo">
                <img src="./images/bigiq_top.png" >
            </div>
            <div id="navbar" align="right">
                <?php
                session_start();
                //echo 'user session: '.$_SESSION['username'];
                // If session variable 'username' is emtpry, redirect to login.php
                if (!isset($_SESSION['username'])){
                     header('Location: login.php');
                }
                else {
                    //echo 'User: '.$_SESSION['username'].'&nbsp;&nbsp;&nbsp;&nbsp;<a href="login.php?action=logout">Logout</a>&nbsp;&nbsp;';
                    echo 'User: '.$_SESSION['username'].' ( '.$_SESSION['role'].' )&nbsp;&nbsp;&nbsp;&nbsp;<a href="login.php?action=logout">Logout</a>&nbsp;&nbsp;';                    
                }
                ?>
            </div>
        </div>
