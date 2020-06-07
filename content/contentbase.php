<?php
if ($_SESSION['loggedin'] != true){
    session_unset();
    session_destroy();
    header('Location: ../login.php');
}
?>
<div id="baseContent">
		<h1> Welcome to the Chan-IQ</h1><br>
		<h2><ul> Introduction </ul></h2>
		<div id="baseContentBody">
			Chan-IQ has been started as my personal project to understand F5 Python SDK since Apr 5, 2017. In the beginning I just built Python codes and 
			over time those codes were unmanageable due to the number of codes. I felt the need of a centralized place to hold those Python codes. 
			Later I expanded the idea so that Chan-IQ could provide Graphical User Interfaces(GUI) for end users, store relevant data into DataBase system,
			and so on and so forth. <br><br>
			
			I named this project/website as "Chan-IQ" due to the partially functional similarities of F5 BIG-IQ system, where BIG-IQ system manages 
			multiple BIG-IP systems, deploys/modifys/delete configuration objects and so on. Compared to F5 BIG-IQ system, Chan-IQ has very limited 
			functionalities such as creating, modifying, deleting configuration objects. Gradually I might add more features and additional functions
			but there is no guaranteed timeline. For this reason, Chan-IQ can't be the replacement of BIG-IQ system but it would be beneficial for F5 admins
			whose daily works are tedious and repetitive creating, modifying, deleting configuratios objects.<br><br>
			
			
			
			 
			
		</div>
		<h2><ul> System Requirements </ul></h2>
		<h2><ul> How to up-to-date your code? </ul></h2>
		<h2><ul> Contribution </ul></h2>
		<h2><ul> License </ul></h2>
		<h2><ul> Need help? </ul></h2>
</div>