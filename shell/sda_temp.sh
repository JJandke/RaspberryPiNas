#!/bin/bash
for i in /dev/sda ; do sudo hddtemp sata:$i; done