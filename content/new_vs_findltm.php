<div>
    <form action="index.php?go=new_vs_simulate" class="register" method="POST">
        <h1> Create new Virtual Server </h1>
        <fieldset class="row1">
            <legend>Virtual Server</legend>
            <?php if(isset($_POST)==TRUE && empty($_POST)==FALSE):
            $vs_dnsname = $_POST['vs_dnsname'];
            $vs_dest = $_POST['vs_dest'];
            $vs_port = $_POST['vs_port'];
            $vs_desc = $_POST['vs_desc'];
            $vs_env = $_POST['vs_env'];
            $vs_type = $_POST['vs_type'];
            $pool_chk = $_POST['pool_chk'];	
            $pool_membername = $_POST['pool_membername'];			
            $pool_memberip = $_POST['pool_memberip'];
            $pool_memberport = $_POST['pool_memberport'];					
            
            // Evaluation & Review process - Function calls
            // 0. Determine target ltm device (active unit)
            // 1. Build Node objects and check object conflict
            // 2. Build Pool object and check object conflict check
            // 3. Build Virtual server object and check object conflict check
            // 4. Build configuration file and save
            
            // 0. Determine target ltm device (active unit)
            /* test code begin */
            //$tmparray = ["10.213.16.5"];
            //$section_name = find_ini_section("1.2.3.4", $tmparray, "PRD");
            $section_name = find_ini_section($vs_dest, $pool_memberip, $vs_env);
            //echo "Found section Name: " . $section_name;
            /* test code end */
            //$section_name = find_ini_section($vs_dest, $pool_memberip, $vs_env);
            $active_ltm = find_active_ltm($section_name, $vs_env);
            //echo "Found Active LTM: " . $active_ltm;
            // Find tcp profiles used as select option values
            //$tcp_profiles = get_tcpprofiles($active_ltm);
            $tcp_profiles = get_profiles($active_ltm, "TCP");
            $persist_profiles = get_profiles($active_ltm, "PERSIST");
            $http_profiles = get_profiles($active_ltm, "HTTP");
            $clissl_profiles = get_profiles($active_ltm, "CLIENTSSL");
            $srvssl_profiles = get_profiles($active_ltm, "SERVERSSL");
            $pool_healthmons = get_healthmon($active_ltm, "ALL");
            
            $irules = get_profiles($active_ltm, "IRULE");
            $snatpools = get_profiles($active_ltm, "SNATPOOL");
            $policies = get_profiles($active_ltm, "POLICY");
            
            // 1. Build Node objects and check object conflict
            $eval_result = "Add evaluation text here!!.<br> First line.<br> Second line.<br> Third line.<br>";
            ?>
            <p>
                <label>Active LTM: </label>
                <input type="text" name="active_ltm" readonly="readonly" value="<?php echo $active_ltm ?>" />                
            </p>
            <p>
                <label>DNS Name: </label>
                <input type="text" name="vs_dnsname" readonly="readonly" value="<?php echo $vs_dnsname ?>" />
                <label>Dest. IP: </label>
                <input type="text" name="vs_dest" readonly="readonly" value="<?php echo $vs_dest ?>" />
                <label>Service Port: </label>
                <input type="text" name="vs_port" readonly="readonly" value="<?php echo $vs_port ?>" />
            </p>
            <p>
                <label>Description: </label>
                <input type="text" name="vs_desc" readonly="readonly" value="<?php echo $vs_desc ?>" />
                <label>Env.: </label>
                <input type="text" name="vs_env" readonly="readonly" value="<?php echo $vs_env ?>" />
                <label>VS Type: </label>
                <input type="text" name="vs_type" readonly="readonly" value="<?php echo $vs_type ?>" />
            </p>
            <p>
            <?php
                dynamic_select($tcp_profiles, "vs_tcpprofile", "TCP Profile", "tcp")
            ?>
            <?php
                dynamic_select($persist_profiles, "vs_persistence", "Persistence", "none")
            ?>                
                    
                <label>Redirection</label>
                <select name="vs_redirect" required="required">
                    <option>NO</option>
                    <option>YES</option>
                </select>                
            </p>
            <?php
                echo "<p>";
                dynamic_select($irules, "vs_irule", "iRule", "none");
                dynamic_select($snatpools, "vs_snatpool", "SNAT Pool", "none");
                dynamic_select($policies, "vs_policy", "Policy", "none");
                echo "</p>";
            ?>
            
            <?php if($vs_type == "Standard"){
                echo "<p>";
                dynamic_select($http_profiles, "vs_httpprofile", "HTTP Profile", "http");
                
                dynamic_select($clissl_profiles, "vs_sslclient", "Client SSL Profile", "clientssl");
                
                dynamic_select($srvssl_profiles, "vs_sslserver", "Server SSL Profile", "serverssl");

                echo "</p>";
            }
            
            ?>
            <p>
            <fieldset>
                <legend>Pool Members</legend>
                <p>
                <?php
                dynamic_select($pool_healthmons, "vs_poolmon", "Pool Monitor", "tcp");
                ?>

                </p>
                <table id="dataTable" class="form" border="1">
                    <tbody>
                        <?php foreach($pool_membername as $a => $b){ ?>
                        <tr>
                            <td>
                                <?php echo $a+1; ?>
                            </td>
                            <td>
                                <label>DNS Name: </label>                                
                                <input type="text" name="pool_membername[]" readonly="readonly" value="<?php echo $pool_membername[$a]; ?>" />
                            </td>
                            <td>
                                <label>IP: </label>
                                <input type="text" name="pool_memberip[]" readonly="readonly" value="<?php echo $pool_memberip[$a]; ?>" />
                            </td>
                            <td>
                                <label>Port: </label>
                                <input type="text" name="pool_memberport[]" readonly="readonly" value="<?php echo $pool_memberport[$a]; ?>" />
                            </td>
                            <td>
                            <?php 
                            array_push($pool_healthmons, "Inherit");
                            dynamic_select($pool_healthmons, "pool_membermon[]", "Pool Monitor", "Inherit");
                            ?>
                            </td>
                        </tr>
                        <?php } ?>
                    </tbody>
                </table>
                <div class="clear"></div>
            </fieldset>                
            </p>

            <?php else: ?>
            <fieldset>
                <legend>Sorry</legend>
                <p>Something went wrong. Please try again</p>
            </fieldset>
        </fieldset>
        <?php endif; ?>
        <div class="clear"></div>
        <!-- Fieldset for evaluation result -->
        <input type="submit" name="new_vs_simulate" value="Simulate & Review" />        
    </form>
</div>