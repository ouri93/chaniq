<div>
     <form action="index.php?go=new_vs_build" class="register" method="POST">
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
            $vs_tcpprofile = $_POST['vs_tcpprofile'];
            $vs_poolmon = $_POST['vs_poolmon'];
            $vs_persistence = $_POST['vs_persistence'];
            $vs_redirect = $_POST['vs_redirect'];					
            if ($vs_type == "Standard"){
                $vs_httpprofile = $_POST['vs_httpprofile'];
                $vs_sslclient = $_POST['vs_sslclient'];			
                $vs_sslserver = $_POST['vs_sslserver'];
            }
            $pool_membername = $_POST['pool_membername'];			
            $pool_memberip = $_POST['pool_memberip'];
            $pool_memberport = $_POST['pool_memberport'];					
            $pool_membermon = $_POST['pool_membermon'];
            $active_ltm = $_POST['active_ltm'];
            $vs_irule = $_POST['vs_irule'];
            $vs_snatpool = $_POST['vs_snatpool'];
            $vs_policy = $_POST['vs_policy'];
            
            // Evaluation & Review process - Function calls
            // 0. Determine target ltm device (active unit) - Use $active_ltm pased by POSTBACK
            // 1. Build Node objects and check object conflict - Pre-checked when they were built
            // 2. Build Pool object and check object conflict check
            // 3. Build Virtual server and pool name conflict check
            // 4. Build configuration file and save
            
            // 0. Determine target ltm device (active unit)
            // 1. Build Node objects and check object conflict
            //$eval_result = "Add evaluation text here!!.<br> First line.<br> Second line.<br> Third line.<br>";
            $outputdata = check_object_conflict($active_ltm, $vs_env, $vs_dnsname, $vs_dest, $vs_port,  $pool_membername, $pool_memberip, $pool_memberport);
            
            // Start output buffer and save all echo output int to the variable $evalout
            ob_start();
            for ($i=1;$i<=sizeof($outputdata);$i++){
                echo $outputdata[$i] . "<br>";
            }
            $eval_result = ob_get_contents();
            ob_end_clean();
            
            $isConfigConflict = check_config_conflict($outputdata[sizeof($outputdata)]);
            
            // Configuration conflict identified - Stop further processing
            if(!$isConfigConflict) {
                $eval_result = $eval_result . "Continue further processing";
            }
            else {
                $eval_result = $eval_result . "Stop further processing";
            }
            
            // If no configuration conflict is identified, proceed with building Virtual Server configuration
            // How to show VS Building Confiuration? 
            // Save the output to a file for the future reference.
            
            
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
                <label>TCP Profile: </label>
                <input type="text" name="vs_tcpprofile" readonly="readonly" value="<?php echo $vs_tcpprofile ?>" />
                <label>Persistence: </label>
                <input type="text" name="vs_persistence" readonly="readonly" value="<?php echo $vs_persistence ?>" />
                <label>Redirection: </label>
                <input type="text" name="vs_redirect" readonly="readonly" value="<?php echo $vs_redirect ?>" />
            </p>
            <p>
                <label>iRule: </label>
                <input type="text" name="vs_irule" readonly="readonly" value="<?php echo $vs_irule ?>" />
                <label>SNAT Pool: </label>
                <input type="text" name="vs_snatpool" readonly="readonly" value="<?php echo $vs_snatpool ?>" />
                <label>Policy: </label>
                <input type="text" name="vs_policy" readonly="readonly" value="<?php echo $vs_policy ?>" />
            </p>                         
            <?php if($vs_type == "Standard"){
                echo "<p>";
                echo "<label>HTTP Profile: </label>";
                echo "<input type='text' name='vs_httpprofile' readonly='readonly' value={$vs_httpprofile} />";
                echo "<label>Client SSL Profile: </label>";
                echo "<input type='text' name='vs_sslclient' readonly='readonly' value={$vs_sslclient} />";
                echo "<label>Server SSL Profile: </label>";
                echo "<input type='text' name='vs_sslserver' readonly='readonly' value={$vs_sslserver} />";
                echo "</p>";
            }
            
            ?>            
            <p>
            <fieldset>
                <legend>Pool Members</legend>
                <p>
                    <label>Pool Monitor: </label>
                    <input type="text"  name="vs_poolmon" readonly="readonly" value="<?php echo "$vs_poolmon"; ?>" />
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
                                <label>Monitor: </label>
                                <input type="text" name="pool_membermon[]" readonly="readonly" value="<?php echo $pool_membermon[$a] ?>" />                                    
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
        <p></p>
        <h1> Evaluation Result and Review </h1>
        <fieldset class="row1">        
            <legend>Evaluation Result</legend>
            <p>
                <table id="evalTable" class="form" border="0">
                    <tr>
                        <td><?php echo $eval_result; ?> </td>
                    </tr>
                </table>
            </p>
        </fieldset>
        <!-- Fieldset for evaluation result -->
        <input type="hidden" name="eval_result" value="<?php echo $eval_result;  ?>" >
        <input type="submit" name="new_vs_build" value="Build VS" <?php if ($isConfigConflict) { echo "disabled"; } ?> >    
    </form>
</div>