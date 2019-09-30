<div id="sidebar">
     <div class="menu-item alpha">
         <h4><a href="?go=home">Home</a></h4>
         <p> Welcome to CHAN-IQ Configuration Tool</p>
     </div>
     <!-- Admin menu - Visible if the logged-in user has admin role -->
     <?php
     /* Include on this level affects all down php */
     include 'utility/utility.php';
     /* echo "User role: ".$_SESSION['role']; */
     if(isadmin()){     
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
         echo "<li><a href='?go=new_policies'>Policies</a></li>";
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
     }
     ?>             
     <div class="menu-item">
         <h4><a href="#">Monitor</a></h4>
         <ul> <!-- Expanding white area -->
             <li><a href="?go=mon_vs">VS</a></li>
             <li><a href="?go=mon_pool">Pool</a></li>
         </ul>
     </div>
         <!-- Admin menu - Visible if the logged-in user has admin role -->
         <?php
         /* echo "User role: ".$_SESSION['role']; */
         if(isadmin()){
             echo "<div class='menu-item'>";
             echo "<h4><a href='#'>Admin</a></h4>";
             echo "<ul>";
             echo "<li><a href='?go=admin_user'>User Management</a></li>";
             echo "<li><a href='?go=ltmadmin_pass'>LTM/GTM Admin</a></li>";
             echo "</ul>";
             echo "</div>";
         }
         ?>
     <div class="menu-item">
         <h4><a href="#">About</a></h4>
         <ul> <!-- Expanding white area -->
             <li><a href="?go=about">About</a></li>
         </ul>
     </div>
</div>