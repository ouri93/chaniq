<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
    <head>
        <title>Dynamic Form Processing with PHP | Tech Stream</title>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
        <link rel="stylesheet" type="text/css" href="../css/style.css"/>
		<script type="text/javascript" src="../js/script.js"></script> 
    </head>
    <body>  
<div>
    <form action="" class="register">
        <h1> Create new Virtual Server </h1>
        <fieldset class="row1">
            <legend>Virtual Server</legend>
            <?php if(isset($_POST)==TRUE && empty($_POST)==FALSE):
            $vs_dnsname = $_POST['vs_dnsname'];
            $vs_dest = $_POST['vs_dest'];
            $vs_port = $_POST['vs_port'];
            $vs_desc = $_POST['vs_desc'];
            $vs_env = $_POST['vs_env'];
            $vs_tcpprofile = $_POST['vs_tcpprofile'];
            $vs_httpprofile = $_POST['vs_httpprofile'];
            $vs_poolmon = $_POST['vs_poolmon'];
            $vs_persistence = $_POST['vs_persistence'];
            $vs_sslclient = $_POST['vs_sslclient'];			
            $vs_sslserver = $_POST['vs_sslserver'];
            $vs_redirect = $_POST['vs_redirect'];					
            $pool_chk = $_POST['pool_chk'];	
            $pool_membername = $_POST['pool_membername'];			
            $pool_memberip = $_POST['pool_memberip'];
            $pool_memberport = $_POST['pool_memberport'];					
            $pool_membermon = $_POST['pool_membermon'];
            ?>
            <p>
                <label>DNS Name</label>
                <input type="text" name="vs_dnsname" readonly="readonly" value="<?php echo $vs_dnsname ?>" />
                <label>Dest. IP</label>
                <input type="text" name="vs_dest" readonly="readonly" value="<?php echo $vs_dest ?>" />
                <label>Service Port</label>
                <input type="text" name="vs_port" readonly="readonly" value="<?php echo $vs_port ?>" />
            </p>
            <p>
                <label>Description</label>
                <input type="text" name="vs_desc" readonly="readonly" value="<?php echo $vs_desc ?>" />
                <label>Env.</label>
                <select name="vs_env" readonly="readonly" value="<?php echo $vs_env ?>" > 
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
                <select name="vs_tcpprofile" readonly="readonly" value="<?php echo $vs_tcpprofile ?>" >
                    <option>Auto</option>
                    <option>tcp</option>
                </select>
            </p>
            <p>
                <label>HTTP Profile</label>
                <select name="vs_httpprofile" readonly="readonly" value="<?php echo $vs_httpprofile ?>" >
                    <option>Auto</option>
                    <option>http</option>
                </select>
                <label>Pool Monitor</label>
                <select name="vs_poolmon" readonly="readonly" value="<?php echo $vs_poolmon ?>" >
                    <option>tcp</option>
                    <option>custom</option>
                </select>
                <label>Persistence</label>
                <select name="vs_persistence" readonly="readonly" value="<?php echo $vs_persistence ?>" >
                    <option>source affinity</option>
                    <option>dest affininity</option>
                </select>
            </p>
            <p>
                <label>Client SSL Profile</label>
                <select name="vs_sslclient" readonly="readonly" value="<?php echo $vs_sslclient ?>" >
                    <option>Auto</option>
                    <option>clientssl</option>
                </select>
                <label>Server SSL Profile</label>
                <select name="vs_sslserver" readonly="readonly" value="<?php echo $vs_sslserver ?>" >
                    <option>Auto</option>
                    <option>serverssl</option>
                </select>
                <label>Redirection</label>
                <select name="vs_redirect" readonly="readonly" value="<?php echo $vs_redirect ?>" >
                    <option>NO</option>
                    <option>YES</option>
                </select>
            </p>
            <p>
            <fieldset>
                <legend>Pool Members</legend>
                <table id="dataTable" class="form" border="1">
                    <tbody>
                        <?php foreach($pool_membername as $a => $b){ ?>
                        <tr>
                            <p>
                                <td>
                                    <?php echo $a+1; ?>
                                </td>
                                <td>
                                    <label>DNS Name</label>                                
                                    <input type="text" name="pool_membername[$a]" readonly="readonly" value="<?php echo $pool_membername[$a]; ?>" />
                                </td>
                                <td>
                                    <label>IP </label>
                                    <input type="text" name="pool_memberip[]" readonly="readonly" value="<?php echo $pool_memberip[$a]; ?>" />
                                </td>
                                <td>
                                    <label>Port</label>
                                    <input type="text" name="pool_memberport[]" readonly="readonly" value="<?php echo $pool_memberport[$a]; ?>" />
                                </td>
                                <td>
                                    <label>Monitor</label>
                                    <select name="pool_membermon" readonly="readonly[]" value="<?php echo $pool_membermon[$a]; ?>" >
                                        <option>Auto</option>
                                        <option>Custom</option>
                                    </select>
                                </td>
                            </p>
                        </tr>
                        <?php } ?>
                    </tbody>
                </table>
                <div class="clear"></div>
            </fieldset>
                <?php else: ?>
                <fieldset>
                    <legend>Sorry</legend>
                    <p>Something went wrong. Please try again</p>
                </fieldset>
            </p>
        </fieldset>
        <?php endif; ?>
        <div class="clear"></div>
    </form>
</div>

</body>
</html>