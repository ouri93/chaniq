<?php
if(isset($_GET['go'])) {
    switch ($_GET['go']) {
        case "home": include('content/contentbase.php'); break;
        //case "new_vs": include('content/new_vs_data.php'); break;
        case "new_vs": include('content/new_vs.php'); break;
        case "new_vs_findltm": include('content/new_vs_findltm.php'); break;
        case "new_vs_simulate": include('content/new_vs_simulate.php'); break;
        case "new_vs_build": include('content/new_vs_build.php'); break;
        case "new_pool": include('content/new_pool.php');break;
        case "deploy_pool_simulate": include('content/deploy_pool_simulate.php');break;
        case "deploy_pool": include('content/deploy_pool.php');break;
        case "new_profile": include('content/new_profile.php');break;
        case "new_cert": include('content/new_cert.php'); break;
        case "new_irule": include('content/new_irule.php');break;
        case "new_monitor": include('content/new_monitor.php');break;
        case "new_snatpool": include('content/new_snatpool.php');break;
        case "new_policies": include('content/new_policy.php');break;
        case "chg_vs": include('content/chg_vs.php'); break;
        case "chg_pool": include('content/chg_pool.php');break;
        case "chg_profile": include('content/chg_profile.php');break;
        case "chg_irule": include('content/new_irule.php');break;
        case "chg_monitor": include('content/chg_monitor.php');break;
        case "new_monitor": include('content/profile.php');break;
        case "del_vs": include('content/del_vs.php');break;
        case "del_profile": include('content/del_profile.php');break;
        case "del_pool": include('content/del_pool.php');break;
        case "del_cert": include('content/del_cert.php'); break;
        case "del_irule": include('content/new_irule.php');break;
        case "del_monitor": include('content/chg_monitor.php');break;
        case "del_snatpool": include('content/new_snatpool.php');break;
        case "del_policies": include('content/del_policy.php');break;
        case "admin_user": include('admin/admin_user.php');break;
        case "admpw_mgmt": include('admin/ltmadmin_pass.php');break;
        case "about": include('content/about.php'); break;
        default: include('content/contentbase.php');
    }
}
else{
    include('content/contentbase.php');
}
?>