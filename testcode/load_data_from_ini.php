<div>
    <form>
        <fieldset>
            <!-- <legend> VS <?php echo "$_POST[$vs_count]"; ?> </legend> -->
            <legend> VS 1 </legend>
            VS Name: <input type="text"> &nbsp;&nbsp; VS Dest. IP: <input type="text"><br>
            VS Service Port: <input type="text"> &nbsp;&nbsp; Environment: 
            <select> 
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
            </select><br>
            Pool Monitor: <input type="text"> &nbsp;&nbsp; HTTP Profile: <input type="text"><br>
            Persistence: <input type="text"> &nbsp;&nbsp; Client SSL Prfile: <input type="text"><br>
            Server SSL Profile: <input type="text"> &nbsp;&nbsp; Redirection: <input type="text"><br>
            Description: <input type="text"><br>
            Pool Name: <input type="text"> &nbsp;&nbsp; Pool IP: <input type="text"> &nbsp;&nbsp; Pool Service Port: <input type="text"> &nbsp;&nbsp; Pool Monitor: <input type="text"> &nbsp;&nbsp;<input type="button" value="Add Pool Member"><br>
        </fieldset>
        <input type="button" value="Add Virtual Server">
    </form>
</div>