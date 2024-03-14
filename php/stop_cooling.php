<?php

$command = escapeshellcmd('/home/config/code/python/stop_cooling.py');
$output = shell_exec($command);
echo $output;

?>
