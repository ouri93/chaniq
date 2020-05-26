<?php
session_start();
if ($_SESSION['loggedin'] != true){
    session_unset();
    session_destroy();
    header('Location: ../login.php');
}
//Admin Content - Visible if the logged-in user has admin role
if ($_SESSION['role'] == 'guest'){
    header('Location: ../content/contentbase.php');
}

include_once('../utility/utility.php');

?>
<html>
    <head>
        <meta charset="UTF-8">
        <link rel="stylesheet" href="/css/style.css" type="text/css" media="screen" />
        <!-- 
        For Produciton 
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js" </script>
        <script> window.jQuery || document.write("<script src='/js/jquery-3.2.1.min.js'><\/script>");  
        -->

        <!-- For Development --> 
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.js" </script>
        <script> window.jQuery || document.write("<script src='/js/jquery-3.2.1.js'><\/script>"); </script>  
                 
        <script type="text/javascript" src="/admin/admin_jquery.js"></script>
    </head>
    <body style="background-color: #ffffff;">
        <form class="register admin" method="POST">
            <h1>LTM/GTM admin password Management</h1>
            <p>Admin password set here will be used for all managed BIG-IP devices by CHAN-IQ.</p>
            <fieldset class="reset_pw"> 
            <legend> Save LTM/GTM admin password</legend>
                <p>
                    <label> BIG-IP Type </label>
                    <select name="set_module" id="set_module">
                        <option>LTM</option>
                        <option>GTM</option>
                    </select>
                </p>
                <p>
                        <label> Type password</label>
                        <input type="password" id="setpass1" name="setpass1"></input>
                </p>
                <p>
                        <label> Retype password</label>
                        <input type="password" id="setpass2" name="setpass2"></input>
                        <p><b>** Minimum 8 characters. The password must include at least one uppercase, one lowercase, one number, and one special character **</b></p>
                </p>
                <p>
                        <input type="button" id="submit_setpass" name="submit_setpass" value="Submit"/>
                </p>
            </fieldset>
            <fieldset class="mod_pw"> 
                <legend> Modify LTM/GTM admin password</legend>
                    <p>
                        <label> BIG-IP Type </label>
                        <select name="mod_module" id="mod_module">
                            <option>LTM</option>
                            <option>GTM</option>
                        </select>
                    </p>
                    <p>
                            <label> Type current password</label>
                            <input type="password" id="modpass1" name="modpass1"></input>
                    </p>
                    <p>
                            <label> Type new password</label>
                            <input type="password" id="modpass2" name="modpass2"></input>
                    </p>
                    <p>
                            <label> Retype new password</label>
                            <input type="password" id="modpass3" name="modpass3"></input>
                            <p><b>** Minimum 8 characters. The password must include at least one uppercase, one lowercase, one number, and one special character **</b></p>
                    </p>
                    <p>
                            <input type="button" id="submit_modpass" name="submit_modpass" value="Submit"/>
                    </p>
            </fieldset>
            <fieldset class="row1">        
                <legend>Result and Review</legend>
                <div>
                    <p id="admin_ResultReview">
        			</p>
                </div>
	        </fieldset>     
        </form>
    </body>
</html>