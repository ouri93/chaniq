<?php
session_start();
if ($_SESSION['loggedin'] != true){
    session_unset();
    session_destroy();
    header('Location: ../login.php');
}
//Admin Content - Visible if the logged-in user has admin role
if ($_SESSION['role'] == 'guest'){
    header('Location: contentbase.php');
}
?>
<div>
    <form action="index.php?go=new_vs_findltm" class="register" method="POST">
        <h1> Create a new Virtual Server </h1>
        <fieldset class="row1">
            <legend>Virtual Server</legend>
            <p>
                <label>DNS Name: </label>
                <input type="text" name="vs_dnsname" id="vs_dnsname" onfocusout="dnsValidation('vs_dnsname')" required="required" />
                <label>Dest. IP: </label>
                <input type="text" name="vs_dest" id="vs_dest" onfocusout="ipValidation('vs_dest')" required="required" />
                <label>Service Port: </label>
                <input type="text" name="vs_port" id="vs_port" onfocusout="portValidation('vs_port')" onkeypress='return event.charCode >= 48 && event.charCode <= 57' required="required" />
            </p>
            <p>
                <label>Description: </label>
                <input type="text" name="vs_desc" maxlength="128" required="required" />
                <label>Env.: </label>
                <select name="vs_env" required="required"> 
                <?php
                $iniarray = parse_ini_section_file();

                foreach ($iniarray as $section => $values){
                    $myx = (string)$section;
                    //$myxval = (string)$values;
                    if ($myx == "LTM_GTM_ENVIRONMENT"){
                        foreach ($values as $key=>$value){
                            echo "<option> " . $value ."</option>";
                        }
                    }
                }
                ?>
                </select>
                <label>VS Type: </label>
                <select name="vs_type" required="required">
                    <option>Standard</option>
                    <option>Forwarding (IP)</option>
                </select>
            </p>
            <p>
            <fieldset class="row2">
                <legend>Pool Members</legend>
                <table id="dataTable" class="form" border="1">
                    <tbody>
                        <tr>
                            <td><input type="checkbox" required="required" name="pool_chk[]" checked="checked" /></td>                                
                            <td>
                                <label>DNS Name: </label>                                
                                <input type="text" name="pool_membername[]" id="pool_membername" onfocusout="dnsValidation('pool_membername')" />
                            </td>
                            <td>
                                <label>IP: </label>
                                <input type="text" name="pool_memberip[]" id="pool_memberip" onfocusout="ipValidation('pool_memberip')" />
                            </td>
                            <td>
                                <label>Port: </label>
                                <input type="text" name="pool_memberport[]" id="pool_memberport" onfocusout="portValidation('pool_memberport')" onkeypress='return event.charCode >= 48 && event.charCode <= 57' />
                            </td>
                        </tr>
                    </tbody>
                </table>
                <p></p>
                <input type="button" value="Remove Member" onClick="deleteRow('dataTable')"  /> 
                <input type="button" value="Add Member" onClick="addRow('dataTable')" /> 
            </fieldset>
            </p>
        </fieldset>
        <input type="submit" name="new_vs_findltm" value="Find LTM" />        
    </form>
    <?php
    //parse_ini_sec_keyvals("PRD_F5_SUBNETS");
    //$tmparray = ["10.213.16.5"];
    //$section_name = find_ini_section("1.2.3.4", $tmparray, "PRD");
    //echo "Found section Name: " . $section_name;
    /* test code end */
    //$section_name = find_ini_section($vs_dest, $pool_memberip, $vs_env);
    //$active_ltm = find_active_ltm($section_name);
    //$dgval = find_active_ltm($section_name);
    //echo "IP address: " .$dgval;
    //$output = exec("/usr/bin/python2 /var/www/chaniq/utility/get_ltm.py $dgval");
    //echo "Found Active LTM: " . $output;
    ?>
</div>