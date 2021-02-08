#!/bin/bash
for i in /dev/sdb ; do sudo hddtemp sata:$i; done