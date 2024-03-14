<?php

$command = escapeshellcmd('/home/config/code/python/start_cooling.py');
$output = shell_exec($command);
echo $output;

?>
