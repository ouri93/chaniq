<div>
    <form action="index.php?go=new_vs_simulate" class="register" method="POST">
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
            </p>
            <p>
            <fieldset class="row2">
                <legend>Pool Members</legend>
                <table id="dataTable" class="form" border="1">
                    <tbody>
                        <tr>
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
                                <select name="pool_membermon[]" onclick="window.location='<? print($this_page); ?>.php?language='+this.value">
                                    <option>Auto</option>
                                    <option>Custom</option>
                                </select>
                            </td>
                        </tr>
                    </tbody>
                </table>
                <p></p>
                <input type="button" value="Remove Member" onClick="deleteRow('dataTable')"  /> 
                <input type="button" value="Add Member" onClick="addRow('dataTable')" /> 
            </fieldset>
            </p>
            <p>
                <label>TCP Profile</label>
                <select name="vs_tcpprofile" required="required">
                    <option>Auto</option>
                    <option>tcp</option>
                </select>
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
            </p>
            <p>
                <label>Persistence</label>
                <select name="vs_persistence" required="required">
                    <option>source affinity</option>
                    <option>dest affininity</option>
                </select>
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
            </p>
            <p>
                <label>Redirection</label>
                <select name="vs_redirect" required="required">
                    <option>NO</option>
                    <option>YES</option>
                </select>
            </p>
        </fieldset>
        <input type="submit" name="new_vs_simulate" value="Simulate & Review" />
    </form>
    <?php
    //parse_ini_sec_keyvals("PRD_F5_SUBNETS");
    $tmparray = ["10.213.16.5"];
    $section_name = find_ini_section("1.2.3.4", $tmparray, "PRD");
    $active_ltm = find_active_ltm($section_name);
    ?>
</div>