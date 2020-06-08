<?php
if ($_SESSION['loggedin'] != true){
    session_unset();
    session_destroy();
    header('Location: ../login.php');
}
?>
<div id="baseContent" class="div_vertical_scroll">
		<h1> Welcome to the Chan-IQ</h1><br>
		<h2><ul> Introduction </ul></h2>
		<div class="baseContentBody">
			<b>Chan-IQ</b> has been started as my personal project to understand F5 Python SDK since Apr 5, 2017. In the beginning I just practiced Python 
			programming using F5 Python SDK and over time those codes were unmanageable due to the number of codes. I felt the need of a centralized 
			place to hold those Python codes. Later I expanded the idea so that Chan-IQ could provide Graphical User Interfaces(GUI) for end users, 
			store relevant data into DataBase system, and so on and so forth. <br><br>
			
			I named this project/website as <b>Chan-IQ</b> due to the partially functional similarities of F5 BIG-IQ system, where BIG-IQ system manages 
			multiple BIG-IP systems, deploys/modifys/delete configuration objects and so on. Compared to F5 BIG-IQ system, Chan-IQ has very limited 
			functionalities such as creating, modifying, deleting configuration objects. Gradually I might add more features and additional functions
			but there is no guaranteed timeline. For this reason, Chan-IQ can't be the replacement of BIG-IQ system. However it would be beneficial 
			for F5 admins who do daily F5 tasks of tedious and repetitive creating, modifying, and deleting F5 configuratios objects.<br><br>
			
		</div>
		
		<h2><ul> How to install Chan-IQ? </ul></h2>
		<div class="baseContentBody">
			<b>Chan-IQ</b> is provided as a VM. All you need is to download <b>Chan-IQ</b> VM and configure the basic system setup.<br>
			You can download <b>Chan-IQ</b> VM <a href="">here.</a><br><br>
		</div>
		
		<h2><ul> System Requirements </ul></h2>
		<div class="baseContentBody">
			<b>Chan-IQ</b> has been built on Ubuntu 14.04(Upgraded to 18.04) with LAMP (Linux, Apache, MySQL, and PHP) package. Here are the required packages.<br><br>
			<ul>
				<li> F5 Python SDK (2.3.3) </li>
				<li> Python 2.7 or later </li>
				<li> LAMP (Linux, Apache, MySQL, and PHP) </li>
				<li> PhpMyAdmin </li>
				<li> Python mysql connector (python -m pip install mysql-connector) </li>
				<li> Python Cryptography package (pip install cryptography) </li>
			</ul>
			<br>
		</div>
		<h2><ul> How to up-to-date your code? </ul></h2>
		<div class="baseContentBody">
			<b>Chan-IQ</b> source code is managed through Git and you can download the latested code from Github.<br><br>
			<ul><li> <b>Chan-IQ</b> <a href="https://github.com/ouri93/chaniq">Git Repository</a></ul><br><br>
		</div>
		
		<h2><ul> Contribution </ul></h2>
		<div class="baseContentBody">
			Are you interested in Chan-IQ project and want to join ths project?<br>
			Thank you very much! Please send your email to <b><i>chaniqhelper at gmai dot com.</i></b><br><br>
		</div>
		
		<h2><ul> License </ul></h2>
			<div class="baseContentBody">
			<b>Chan-IQ</b> project follows <a href="https://github.com/ouri93/chaniq/blob/master/LICENSE">GNU General Public Licesne.</a><br><br>
			</div>
			
		<h2><ul> Need help? </ul></h2>
		
		<div class="baseContentBody">
			<b>Chan-IQ</b> project is my personal project and I didn't set any dedicated hours for this project. Whenever I have some extra time, I would
			update this project without any guaranteed timeline. However if you have any good ideas or need any help, shoot me an email to 
			<b><i>chaniqhelper at gmai dot com.</i></b><br><br>
		</div>
</div>