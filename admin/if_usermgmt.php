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
        <!-- For Produciton 
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>
        <script> window.jQuery || document.write("<script src='/js/jquery-3.2.1.min.js'><\/script>"); </script>  
        -->
        
        <!-- For Development  -->
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.js"> </script>
        <script> window.jQuery || document.write("<script src='/js/jquery-3.2.1.js'><\/script>"); </script>  
        
        <script type="text/javascript" src="/admin/admin_jquery.js"></script>
    </head>
    <body style="background-color: #ffffff;">
        <form class="register admin" method="POST">
            <h1>CHAN-IQ User Management</h1>
            <p>You can create new CHAN-IQ users and reset CHAN-IQ users' password here.</p>
            <fieldset class="reset_pw"> 
            <legend> Create a new CHAN-IQ User</legend>
                <p>
                    <label> *Username </label>
                    <input type="email" id="unEmail" name="unEmail" placeholder="user_id@example.com" style="width: 200px;">* Email Address *</input>
                </p>
                <p>
                    <label> *User Role </label>
                    <select name="unRole" id="unRole" style="width: 200px;">
                        <option value="admin">Admin</option>
                        <option selected="selected" value="guest">Guest</option>
                    </select>
                </p>                
                <p>
                        <label> *Type password</label>
                        <input type="password" id="unPass1" name="unPass1" style="width: 200px;"></input>
                </p>
                <p>
                        <label> *Retype password</label>
                        <input type="password" id="unPass2" name="unPass2" style="width: 200px;"></input>
                        <p><b>** Minimum 8 characters. The password must include at least one uppercase, one lowercase, one number, and one special character **</b></p>
                </p>
                <p>
                        <input type="button" id="submit_unPass" name="submit_unPass" value="Submit"/>
                </p>
            </fieldset>
            <fieldset class="mod_pw"> 
                <legend> Modify CHAN-IQ User Role and Password</legend>
                    <p>
                        <label> *Username </label>
                        <input type="text" id="rst_unEmail" name="rst_unEmail" style="width: 200px;">* Built-in User ID or Email Address *</input>
                    </p>
                    <p>
                        <label> *User Role </label>
                        <select name="rst_unRole" id="rst_unRole" style="width: 200px;">
                            <option value="admin">Admin</option>
                            <option selected="selected" value="guest">Guest</option>
                        </select>
                    </p>                    
                    <p>
                            <label> *Type new password</label>
                            <input type="password" id="rst_unPass1" name="rst_unPass1" style="width: 200px;"></input>
                    </p>
                    <p>
                            <label> *Retype new password</label>
                            <input type="password" id="rst_unPass2" name="rst_unPass2" style="width: 200px;"></input>
                            <p><b>** Minimum 8 characters. The password must include at least one uppercase, one lowercase, one number, and one special character **</b></p>
                    </p>
                    <p>
                            <input type="button" id="submit_modUser" name="submit_modUser" value="Submit"/>
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