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
                 
        <script type="text/javascript" src="/js/mon_jquery.js"></script>
        <?php include('../utility/utility.php'); ?>
        <title>Create a new Pool</title>
    </head>
    <body style="background-color: #ffffff;">
        <form class="inner-form">
            <h1> Create a new Pool </h1>
            <fieldset class="row1">
                <legend>Select a target LTM</legend>
                <?php
                    // Load all BIG-IP devices name and IP
                    $allBigips = load_all_bigips();
                    $allBigipNames = array();
    
                    $allBigipNames[0] = 'Select...';
                    $i=1;
                    foreach($allBigips as $name => $ip){
                        $allBigipNames[$i] = $name . ":" . $ip;
                        $i += 1;
                    }
                    asort($allBigipNames);
                ?>
                <p>
                    <div id='div_ltmchoice' class="ltmDeviceList">
                    	<?php 
                    	dynamic_select($allBigipNames, "ltmSelBox", "", "Select...");
                    	?>
                    </div>
                </p>
            </fieldset>
            <fieldset class="row1">
                <legend>Monitor Properties</legend>
                <p>
                <table id="monDataTable" class="form" border="1">
                    <tbody>
                        <tr>
                            <td>
                                <label>Monitor Name: </label>
                                <input type="text" name="m_name" id="m_name" required="required" />
                            </td>
                            <td>
                                <label>Monitor Description: </label>
                                <input type="text" name="m_desc" id="m_desc" />
                            </td>
                            <td>
                                <label>Env.: </label>
                                <select name="p_env" id="p_env" required="required"> 
                                <?php
                                    $iniarray = parse_ini_section_file();
                    
                                    foreach ($iniarray as $section => $values){
                                        $myx = (string)$section;
                                        if ($myx == "LTM_GTM_ENVIRONMENT"){
                                            foreach ($values as $key=>$value){
                                                echo "<option> " . $value ."</option>";
                                            }
                                        }
                                    }
                                ?>
                            </select>
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <label>Monitor Type: </label>
                                <select name="m_type" id="m_type" required="required" />
                                	<option selected="selected">Select...</option>
                                	<option>HTTP</option>
                                	<option>HTTPS</option>
                                	<option>TCP</option>
                                	<option>TCP Half Open</option>
                                	<!-- <option>ICMP</option>  -->
                                	<!-- <option>External</option> -->
                                	<option>UDP</option>
                            </td>
                            <td>
                                <label>Parent Monitor: </label>
                                <select name="m_type_parent" id="m_type_parent" required="required" />
                            </td>
    
                        </tr>
                    </tbody>
                </table>
                </p>
                <p>
                <fieldset class="row2">
                    <legend>Monitor Configuration</legend>
                    <p>
                    	<table id="monConfTable" class="form" border="1">
                    		<tbody id="monConfTable_tbody">
    						<!--  Conditional HTML code here  --> 
                    		</tbody>
                    	</table>
                    </p>
                </fieldset>
                </p>
            </fieldset>
            <input id="btn_newMonBuild" type="button" name="deploy_mon" value="Deploy Monitor" />
            <p></p>
            <fieldset class="row1">        
                <legend>Evaluation Result and Review</legend>
                <div>
                    <p id="newMon_EvalReview">
        			</p>
                </div>
            </fieldset>        
        </form>
    </body>
</html>