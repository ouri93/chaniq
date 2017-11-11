<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
    <head>
        <title>Dynamic Form Processing with PHP | Tech Stream</title>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
        <link rel="stylesheet" type="text/css" href="../css/style.css"/>
		<script type="text/javascript" src="../js/script.js"></script> 
    </head>
    <body>  
<div>
    <form action="new_vs_process.php" class="register" method="POST">
        <h1> Create new Virtual Server </h1>
        <fieldset class="row1">
            <legend>Virtual Server</legend>
            <p>
                <label>DNS Name</label>
                <input type="text" name="vs_dnsname" required="required" />
                <label>Dest. IP</label>
                <input type="text" name="vs_dest" required="required" />
                <label>Service Port</label>
                <input type="text" name="vs_port" required="required" />
            </p>
            <p>
                <label>Description</label>
                <input type="text" name="vs_desc" required="required" />
                <label>Env.</label>
                <select name="vs_env" required="required"> 
                <?php
                include "../utility/utility.php";
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
                <label>TCP Profile</label>
                <select name="vs_tcpprofile" required="required">
                    <option>Auto</option>
                    <option>tcp</option>
                </select>
            </p>
            <p>
                <label>HTTP Profile</label>
                <select name="vs_httpprofile" required="required">
                    <option>Auto</option>
                    <option>http</option>
                </select>
                <label>Pool Monitor</label>
                <select name="vs_poolmon" required="required">
                    <option>tcp</option>
                    <option>custom</option>
                </select>
                <label>Persistence</label>
                <select name="vs_persistence" required="required">
                    <option>source affinity</option>
                    <option>dest affininity</option>
                </select>
            </p>
            <p>
                <label>Client SSL Profile</label>
                <select name="vs_sslclient" required="required">
                    <option>Auto</option>
                    <option>clientssl</option>
                </select>
                <label>Server SSL Profile</label>
                <select name="vs_sslserver" required="required">
                    <option>Auto</option>
                    <option>serverssl</option>
                </select>
                <label>Redirection</label>
                <select name="vs_redirect" required="required">
                    <option>NO</option>
                    <option>YES</option>
                </select>
            </p>
            <p>
            <fieldset class="row2">
                <legend>Pool Members</legend>
                <table id="dataTable" class="form" border="1">
                    <tbody>
                        <tr>
                            <p>
                                <td><input type="checkbox" required="required" name="pool_chk[]" checked="checked" /></td>                                
                                <td>
                                    <label>DNS Name</label>                                
                                    <input type="text" name="pool_membername[]"/>
                                </td>
                                <td>
                                    <label>IP </label>
                                    <input type="text" name="pool_memberip[]"/>
                                </td>
                                <td>
                                    <label>Port</label>
                                    <input type="text" name="pool_memberport[]"/>
                                </td>
                                <td>
                                    <label>Monitor</label>
                                    <select name="pool_membermon[]">
                                        <option>Auto</option>
                                        <option>Custom</option>
                                    </select>
                                </td>
                            </p>
                        </tr>
                    </tbody>
                </table>
                <p></p>
                <input type="button" value="Add Member" onClick="addRow('dataTable')" /> 
                <input type="button" value="Remove Member" onClick="deleteRow('dataTable')"  /> 
            </fieldset>
            </p>
        </fieldset>
    </form>
</div>

</body>
</html>