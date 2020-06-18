<?php
require_once(__DIR__ . '/utility/chaniqLogger.php');

if ($_SESSION['loggedin'] != true){
    $logger->info("sidebar.php - Unauthen user - Redirect to login page.");
    #file_put_contents("/var/log/chaniqphp.log", "sidebar.php - Unauthen user - Redirect to login page\n", FILE_APPEND);
    session_unset();
    session_destroy();
    header('Location: login.php');
}
?>
<div id="sidebar">
     <div class="menu-item alpha">
         <h4><a href="?go=home">Home</a></h4>
         <p> Welcome to CHAN-IQ Configuration Tool</p>
     </div>
     <!-- Admin menu - Visible if the logged-in user has admin role -->
     <?php
     $role = $_SESSION['role'];
     if($role == 'admin'){
         echo "<div class='menu-item'>";
             echo "<h4><a href='#'>Deploy</a></h4>";
             echo "<ul> <!-- Expanding white area -->";
             echo "<li><a href='?go=new_vs'>VS</a></li>";
             echo "<li><a href='?go=new_profile'>Profile</a></li>";
             echo "<li><a href='?go=new_pool'>Pool</a></li>";
             echo "<li><a href='?go=new_cert'>Cert</a></li>";
             echo "<li><a href='?go=new_irule'>iRule</a></li>";
             echo "<li><a href='?go=new_monitor'>Monitor</a></li>";
             echo "<li><a href='?go=new_snatpool'>Snatpool</a></li>";
             #echo "<li><a href='?go=new_policies'>Policies</a></li>";
             echo "</ul>";
         echo "</div>";
         echo "<div class='menu-item'>";
             echo "<h4><a href='#'>Change</a></h4>";
             echo "<ul> <!-- Expanding white area -->";
                 echo "<li><a href='?go=chg_vs'>VS</a></li>";
                 echo "<li><a href='?go=chg_profile'>Profile</a></li>";
                 echo "<li><a href='?go=chg_pool'>Pool</a></li>";
                 echo "<li><a href='?go=chg_irule'>iRule</a></li>";
                 echo "<li><a href='?go=chg_monitor'>Monitor</a></li>";
             echo "</ul>";
         echo "</div>";
         echo "<div class='menu-item'>";
         echo "<h4><a href='#'>Delete</a></h4>";
         echo "<ul> <!-- Expanding white area -->";
         echo "<li><a href='?go=del_vs'>VS</a></li>";
         echo "<li><a href='?go=del_profile'>Profile</a></li>";
         echo "<li><a href='?go=del_pool'>Pool</a></li>";
         echo "<li><a href='?go=del_cert'>Cert</a></li>";
         echo "<li><a href='?go=del_irule'>iRule</a></li>";
         echo "<li><a href='?go=del_monitor'>Monitor</a></li>";
         echo "<li><a href='?go=del_snatpool'>Snatpool</a></li>";
         echo "<li><a href='?go=del_policies'>Policies</a></li>";
         echo "</ul>";
         echo "</div>";

         echo "<div class='menu-item'>";
         echo "<h4><a href='#'>Admin</a></h4>";
         echo "<ul>";
         echo "<li><a href='?go=admin_user'>User Management</a></li>";
         echo "<li><a href='?go=admpw_mgmt'>LTM/GTM Admin</a></li>";
         echo "</ul>";
         echo "</div>";
     }
     if ( $role == 'admin' || $role == 'guest' ){
         echo "<div class='menu-item'>";
         echo "<h4><a href='#'>About</a></h4>";
         echo "<ul> <!-- Expanding white area -->";
         echo "<li><a href='?go=about'>About</a></li>";
         echo "</ul>";
         echo "</div>";
     }
     else{
         $logger->info("sidebar.php - Undefined user role - Redirect to login page");
         #file_put_contents("/var/log/chaniqphp.log", "sidebar.php - Undefined user role - Redirect to login page\n", FILE_APPEND);
         session_unset();
         session_destroy();
         header('Location: login.php');
     }

     ?>
</div>