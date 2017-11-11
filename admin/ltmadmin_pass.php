<div id="ltmadmin_pass">
    <!-- Admin Content - Visible if the logged-in user has admin role -->
    <?php
    require 'db/connect.php';
    if (!isadmin()){
        header('Location: index.php');
    }
    
    if(isset($_POST['set_pass']) || isset($_POST['mod_pass'])){
        // Process LTM/GTM Admin password set
        $option = isset($_POST['set_module']) ? $_POST['mod_module'] : FALSE;
        if($option == "LTM"){
            $selected = "LTM";
        }
        else $selected = "GTM";

        //echo "Selected option: " . $selected;

        // Set LTM/GTM admin password
        if( (isset($_POST['set_pass'])) && ( strcmp($_POST['setpass1'], $_POST['setpass2']) == 0 ) && (!empty($_POST['setpass1'])) && (!empty($_POST['setpass2'])) ){
            $hashed_password = password_hash($_POST['setpass1'], PASSWORD_DEFAULT);
            $result = mysqli_query($con, 'update bigip_pass set pass="'.$hashed_password.'" where module="'.$selected.'"');
            //echo "Query result: ".$result;
            echo "<script type='text/javascript'>alert('Password has been successfully reset!');</script>";
        }
        // Modify LMT/GTM admin password
        elseif( (isset($_POST['mod_pass'])) && ( strcmp($_POST['modpass2'], $_POST['modpass3']) == 0 ) && (!empty($_POST['modpass2'])) && (!empty($_POST['modpass3']))){
            $hashed_password = password_hash($_POST['modpass2'], PASSWORD_DEFAULT);
            $result = mysqli_query($con, 'select pass from bigip_pass where module="'.$selected.'"');
            $pass_temp =  mysqli_fetch_object($result);
            $db_hashed_password = $pass_temp->pass;
            
            //echo 'Hashed PW: '.$db_hashed_password;
            //Check if current password is matching
            if(password_verify($_POST['modpass1'], $db_hashed_password)){
                $result2 = mysqli_query($con, 'update bigip_pass set pass="'.$hashed_password.'" where module="'.$selected.'"');
                //echo "Query result: ".$result2;
                echo "<script type='text/javascript'>alert('Password has been successfully modified!');</script>";
            }
            else{
                echo "<script type='text/javascript'>alert('Current password not correct!');</script>";
            }
        }
        else{
            echo "<script type='text/javascript'>alert('New password not matching or empty!');</script>";
        }
    }
    ?>
    <form class="register" method="POST">
        <h1>Set LTM/GTM admin password Management</h1>
        <fieldset class="admin_pass"> 
            <legend> Set LTM/GTM password</legend>
                <p>
                    <label> BIG-IP Type </label>
                    <select name="set_module">
                        <option>LTM</option>
                        <option>GTM</option>
                    </select>
                </p>
                <p>
                        <label> Type password</label>
                        <input type="password" name="setpass1"></input>
                </p>
                <p>
                        <label> Retype password</label>
                        <input type="password" name="setpass2"></input>
                </p>
                <p>
                        <input type="submit" name="set_pass" value="Submit"/>
                </p>
            </fieldset>
        <fieldset class="admin_pass"> 
            <legend> Modify LTM/GTM password</legend>
                <p>
                    <label> BIG-IP Type </label>
                    <select name="mod_module">
                        <option>LTM</option>
                        <option>GTM</option>
                    </select>
                </p>
                <p>
                        <label> Type current password</label>
                        <input type="password" name="modpass1"></input>
                </p>
                <p>
                        <label> Type new password</label>
                        <input type="password" name="modpass2"></input>
                </p>
                <p>
                        <label> Retype new password</label>
                        <input type="password" name="modpass3"></input>
                </p>
                <p>
                        <input type="submit" name="mod_pass" value="Submit"/>
                </p>
            </fieldset>    </form>
</div>
