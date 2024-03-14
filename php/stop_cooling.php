<?php

$command = escapeshellcmd('/home/config/code/python/stop_external_cooling.py');
$output = shell_exec($command);
echo $output;

?>
