<?php
require_once(__DIR__ . '/../utility/chaniqLogger.php');

if ($_SESSION['loggedin'] != true){
    session_unset();
    session_destroy();
    header('Location: ../login.php');
}


/* 
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

?>
<div id="baseContent" class="div_vertical_scroll">
<p> About content </p>
</div>