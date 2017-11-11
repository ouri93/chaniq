<?php include('header.php'); ?>

<div id="content">
    <div id="sidebar">
       <?php include('sidebar.php'); ?>
    </div>
    <div id="maincontent">
        <!-- Content loading by a given parameter -->
        <?php include('content/contentswitch.php'); ?>
    </div>
</div>

<?php include('footer.php'); ?>