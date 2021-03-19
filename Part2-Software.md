## Part 2 - Software

### Install operating system

- To get the operating system onto the SD card, we will use the [Pi imager](https://www.raspberrypi.org/software/).
- There, we select *Choose OS -> Other general purpose OS -> Ubuntu -> Ubuntu Server 20.XX.x LTS (RPi 3/4/400)*.
- And then choose your SD card.
- Then press "Write".
- The process took me about 6 minutes.



### Get the IP of the Raspberry

- After the SD card is in the Pi and it is turned on, it should appear on your router's user interface after a few seconds.

- At my Fritz!Box you can find the IP under *Home Networks -> Mesh -> Other connected or registered home network devices*.

- There you should give the device a static IP, so that you don't have any problems later when mounting e.g. in fstab.

![router](https://user-images.githubusercontent.com/56551925/111346906-f9ce9a00-867e-11eb-8b17-d3e45a9af534.png)

  

### Access the Pi via SSH

- To get access to the Raspberry Pi via SSH, we open a terminal on the PC and type: `ssh ubuntu@ubuntu` or `ssh ubuntu@"IP_of_your_pi"`.

- the default password is `ubuntu` but the password should be urgently replaced with a strong password, otherwise an attacker will have access to all data stored on the NAS.

- After that you will be logged out and have to log in again with your new password.

  

### First steps on a new OS

#### Hints and tips

- Use `tab` in terminal for auto-complete.

- Exit nano with `Ctrl+x` and confirm changes with `y`.

- Select a text section in nano: `Alt+A+M` and then move with the `arrow` keys.
  `Ctrl+arrow` key then selects the whole paragraph at once.

- Cut selected text in nano: `Ctrl+K`

  

#### Update the Raspberry Pi

```shell
sudo apt-get update
```

```shell
sudo at-get full-upgrade
```


  If errors occur here, just rebooting will help.

  

#### Make SSH more secure

Note: Since the NAS will only be accessible from the home network anyway, this is not absolutely necessary. This measure helps to make attacks on port 22 useless, but with a portscan you can also find out the actually used port. Therefore, a strong password is more important for every user. More help would be provided by [fail2ban](https://linuxize.com/post/install-configure-fail2ban-on-ubuntu-20-04/) and access via [certificate](https://www.digitalocean.com/community/tutorials/how-to-configure-ssh-key-based-authentication-on-a-linux-server).

- For this we need to change the default SSH port and disable root login. This is done in the SSH configuration file under */etc/ssh/sshd_config*:

```shell
sudo nano /etc/ssh/sshd_config
```

- Here we have to remove the "#" in line `#Port 22` and change "22" to any other port (e.g. 2846).
- Also, in the line `#PermitRootLogin prohibit-password,` the "#" should be removed and *"prohibit-password"* should be replaced by *" no"*.
- This should look like this:

```shell
Port 2846
#AddressFamily any
#ListenAddress 0.0.0.0
#ListenAddress ::

#HostKey /etc/ssh/ssh_host_rsa_key
[...]

# Authentication:

#LoginGraceTime 2m
PermitRootLogin no

```

- To make the changes take effect immediately, we restart ssh:

```shell
sudo /etc/init.d/ssh restart
```



#### Allow selected port in the firewall

Since we changed the default port of SSH, `sudo ufw allow OpenSSH` won't work anymore. Therefore, we need to use the following command to allow the newly selected port:

```shell
sudo ufw allow 1636
```

- Now the port must be specified when logging in via SSH: `ssh ubuntu@ubuntu -p 2846`



#### Change hostname

Since I have installed several Ubuntu servers and want to recognize my NAS better in the home network afterwards, the hostname will be changed.
Note: After that the RPi is no longer reachable via ssh under `ssh ubuntu@ubuntu -p 2846` but under `ssh ubuntu@rpi-nas -p 2846`.

- With `hostnamectl` we can display the current hostname:

```shell
$ hostnamectl
   Static hostname: ubuntu
         Icon name: computer
        Machine ID: e5e5d4e8666c456488d91bc2735712d0
           Boot ID: 1fdeecd84e8f48c499c520978bc60358
  Operating System: Ubuntu 20.04.2 LTS
            Kernel: Linux 5.4.0-1029-raspi
      Architecture: arm64
```

- With the `set-hostname` option we can set a new hostname:

```shell
sudo hostnamectl set-hostname rpi-nas
```

- Then we have to add the line `127.0.0.1 rpi-nas` to the `/etc/hosts` file:

```
sudo nano /etc/hosts
```

​		It should then look something like this:

```shell
127.0.0.1 rpi-nas

# The following lines are desirable for IPv6 capable hosts
::1 ip6-localhost ip6-loopback
fe00::0 ip6-localnet

```

- The last thing to do is to change a value in the cloud.cfg file:

```shell
sudo nano /etc/cloud/cloud.cfg
```

- Search here for `preserve_hostname: ` and change the value to `true`
- To make sure everything worked, we run `hostnamectl` again.

```shell
$ hostnamectl
   Static hostname: rpi-nas
         Icon name: computer
        Machine ID: e5e5d4e8666c456488d91bc2735712d0
           Boot ID: 1fdeecd84e8f48c499c520978bc60358
  Operating System: Ubuntu 20.04.2 LTS
            Kernel: Linux 5.4.0-1029-raspi
      Architecture: arm64
```



#### Add non-root user

The last thing we do is to add a default, non-root user, which we will work with from now on.

- To do this: 

```shell
sudo adduser config
```

- Add the user to the sudo group:

```shell
sudo usermod -a -G sudo config 
```

- Now we switch to the new user and run a command that requires root right to make sure everything worked:

```shell
sudo su - config
sudo apt-get update
```



### Python scripts to cool the NAS

#### Cooling the Raspberry Pi

- First, you need to install some packages:

```shell
sudo apt-get install python3-pip
sudo pip3 install Rpi.GPIO
pip3 install gpiozero
pip3 install pigpio
sudo apt-get install rpi.gpio-common
sudo apt-get install python3-rpi.gpio
```

- Then the group `gpio` must be created, the current user (config) must be added and the group must get rights for the GPIOs:

```shell
sudo groupadd gpio					# Add the group 
sudo usermod -a -G gpio $USER		# Add the current user to the new group
sudo grep gpio /etc/group			# Assure that everything is working
sudo chown root:gpio /dev/gpiomem	# Change the gpio owner to root
sudo chmod g+rw /dev/gpiomem		# Add read and write permissions 
```

- Alternatively, the current user may also own `gpiomem`:

```shell
sudo chown root:$USER /dev/gpiomem
```

- Now we create another folder where the python scripts will be placed, and also the python script itself. The code that needs to be inserted is found on GitHub:

```shell
mkdir code
cd code
mkdir python
cd python
nano cooling_pi.py	# now paste the code from GitHub
sudo chmod u+x cooling_pi.py	# Make the script executable
```

- To ensure that the Pi is reliably cooled after each reboot, we add the following line to the crontab.
  To log any errors that occur, we also create a log file:

```shell
cd log/
touch cron_user.log
crontab -e
	@reboot python3 /home/config/code/python/cooling_pi.py > /home/config/log/cron_user.log 2>&1	# Insert this line.
```



#### Cooling the HDDs

- To be able to read out the temperatures of the hard disks, hddtemp must be installed:

```shell
sudo apt-get install hddtemp
```

- The following line can be used to read out the temperature for a hard disk:

```shell
for i in /dev/sdX ; do sudo hddtemp sata:$i; done
```

- For the script we create a new folder for shell scripts in the directory ./code. There we will create a script for each disk (code on GitHub) 
  Since the readout requires root rights, but the python script is executed by a non-root user, the owner of the shell scripts must be changed to root, as well as the file rights must be adjusted.

```shell
cd code/
mkdir shell
cd shell/
nano sda_temp.sh		# For HDD1
nano sdb_temp.sh		# For HDD2
sudo chown root:root sda_temp.sh sdb_temp.sh		# Change the owner
sudo chmod 755 sda_temp.sh sdb_temp.sh		# Assign the relevant file permissions
sudo visudo		# To avoid the need to enter a password.
	config ALL=(ALL) NOPASSWD: /home/config/code/shell/sda_temp.sh		# Insert those two lines
	config ALL=(ALL) NOPASSWD: /home/config/code/shell/sdb_temp.sh
```

- Now we create the python script and add it to the crontab.

```shell
cd code/python/ 
nano cooling_hdd.py		# now paste the code from GitHub
sudo chmod u+x cooling_hdd.py		#  Make the script executable
crontab -e
	@reboot python3 /home/config/code/python/cooling_hdd.py > /home/config/log/cron_user.log 2>&1		# Insert this line.
```



### Create Software Raid

Now it finally comes to create the raid using mdadm.

- First, let's display the available disks to check that everything is working fine.

```shell
sudo lshw -short
H/W path      Device     Class      Description
===============================================
                         system     Raspberry Pi 4 Model B Rev 1.4
/0                       bus        Motherboard
/0/1                     processor  cpu
/0/2                     processor  cpu
/0/3                     processor  cpu
/0/4                     processor  cpu
/0/5                     memory     7811MiB System memory		# 8 GB RAM
/0/0                     bridge     Broadcom Inc. and subsidiaries
/0/0/0                   bus        VL805 USB 3.0 Host Controller
/0/0/0/0      usb1       bus        xHCI Host Controller
/0/0/0/0/1               bus        USB2.0 Hub
/0/0/0/1      usb2       bus        xHCI Host Controller
/0/0/0/1/1               storage    ASM105x
/0/0/0/1/2               storage    ASM105x
/0/6          scsi0      storage    
/0/6/0.0.0    /dev/sda   disk       4TB ASM105x			# HDD1
/0/6/0.0.0/1  /dev/sda1  volume     3726GiB EXT4 volume
/0/7          scsi1      storage    
/0/7/0.0.0    /dev/sdb   disk       4TB ASM105x			# HDD2
/0/7/0.0.0/1  /dev/sdb1  volume     3726GiB EXT4 volume
/1            wlan0      network    Wireless interface
/2            eth0       network    Ethernet interface
```

- If the hard disks are not partitioned yet, we will do that first. Note that for disks larger than 2TB, GPT must be used instead of MBR as the partition table, since MBR can only handle partitions < 2TB and the disk will otherwise contain several small partitions instead of one large one.
- To create a partition using the entire hard disk, you can simply enter 0% 100%. Otherwise the start and end block must be specified.

```shell
sudo parted /dev/sda mklabel gpt		# Create partition table
sudo parted -a optimal -- /dev/sda mkpart primary 0% 100%
sudo parted /dev/sda set 1 raid on		# Mark partition as RAID
```

​	Of course must be repeated for the second drive (sdb).

- **Now the RAID can be created.** 
  We create a RAID1, so the disks are mirrored.

```shell
sudo mdadm --create /dev/md0 --auto md --level=1 --raid-devices=2 /dev/sda1 /dev/sdb1
```

- The question "Continue creating array?" must be answered with "y".

- Now we create an ext4 partition on the raid array and mount it.

```sh
sudo mkfs.ext4 /dev/md0
sudo mkdir /mnt/nas
sudo nano /etc/fstab
	/dev/md0                /mnt/nas        ext4            defaults        0       2		# Insert this line
sudo mount -a
```

- The last thing to do is to update mdadm.conf and initramfs. The second one takes a while.

```shell
sudo su -c "/usr/share/mdadm/mkconf > /etc/mdadm/mdadm.conf“
sudo update-initramfs -u -k all
```

- Whether everything went well can be checked with these two commands:

```shell
cat /proc/mdstat 
Personalities : [linear] [multipath] [raid0] [raid1] [raid6] [raid5] [raid4] [raid10] 
md0 : active raid1 sdb[1] sda[0]
      3906886464 blocks super 1.2 [2/2] [UU]
      [>....................]  resync =  1.9% (75295680/3906886464) finish=3092.5min speed=20649K/sec
      bitmap: 30/30 pages [120KB], 65536KB chunk
```


​		Here you can also see if a hard disk is failed or synchronized.

```shell
sudo mdadm --detail /dev/md0
/dev/md0:
           Version : 1.2
     Creation Time : Wed Feb  3 09:26:57 2021
        Raid Level : raid1
        Array Size : 3906886464 (3725.90 GiB 4000.65 GB)
     Used Dev Size : 3906886464 (3725.90 GiB 4000.65 GB)
      Raid Devices : 2
     Total Devices : 2
       Persistence : Superblock is persistent

     Intent Bitmap : Internal

       Update Time : Wed Feb  3 10:31:45 2021
             State : clean, resyncing 
    Active Devices : 2
   Working Devices : 2
    Failed Devices : 0
     Spare Devices : 0

Consistency Policy : bitmap

     Resync Status : 1% complete

              Name : ubuntu:0  (local to host ubuntu)
              UUID : ab3d8d90:b05e8253:5f8e750d:7ae67fea
            Events : 1235

    Number   Major   Minor   RaidDevice State
       0       8        0        0      active sync   /dev/sda 
       1       8       16        1      active sync   /dev/sdb
```



### Block UAS

In the beginning, I often had problems with my hard drives being kicked out. On the one hand, this was due to the lack of a USB hub, but on the other hand, it was also due to UAS. That is why we will block it.
In addition, we deactivate the sleep mode of the hard drives, so that they do not switch off at some point and are then no longer accessible.

```shell
lsusb -t		# check, if your adapter uses UAS:
/:  Bus 04.Port 1: Dev 1, Class=root_hub, Driver=xhci_hcd/4p, 5000M
    |__ Port 2: Dev 2, If 0, Class=Mass Storage, Driver=uas, 5000M		# <- UAS
```

```shell
sudo lsusb
Bus 001 Device 002: ID 8087:0024 Intel Corp. Integrated Rate Matching Hub
Bus 001 Device 001: ID 1d6b:0002 Linux Foundation 2.0 root hub
Bus 004 Device 002: ID 174c:55aa ASMedia Technology Inc. Name: ASM1051E SATA 6Gb/s bridge, ASM1053E SATA 6Gb/s bridge, ASM1153 SATA 3Gb/s bridge, ASM1153E SATA 6Gb/s bridge
```

```shell
sudo nano /boot/firmware/cmdline.txt 
	usb-storage.quirks=174c:55aa:u		# Insert this line.
sudo update-initramfs -u		# Update initramfs so that the changes take effect.
```

```shell
sudo hdparm -S0 /dev/sda		#Disable sleep
```



### Setup Samba

#### Create users

```shell
sudo apt-get install samba samba-common		# install samba
```

- I have created a **total of 7 users** on my end. The distribution as follows: **User1, User2, User3, User4** for all **family members**. In addition, I have set up a **public share (family)**. This is where files and photos are stored to which **everyone has access**. Then there is a share **User2Work**. This share is for the **business data** of user 2, which is also mounted **only** on the **business laptop**.

- There is also the user **nas**. This is **generally** used for **writing**, because otherwise **conflicts with user rights** could arise, for example, if User1 wants to change a file created by User2.

- With the **first command** a normal Ubuntu user named **User1 is created**. However, since this user does **not need** a **home** directory, **nor** does he need to **log in** to the NAS via ssh as we do, we **disable** this with the options `--no-create-home` and `--disabled-login`. Also questions about residence, department, etc. can be **skipped**.
  The second command sets a ***(strong!)*** **password** for this user. Note that anyone who has this password can also have access to all files stored under this user.

```shell
sudo adduser --no-create-home --disabled-login --shell /bin/false user1
sudo smbpasswd -a user1
```

- These steps are now **repeat**ed for **all 7 users**.



#### Create folders for the users

- Of course, no folder is created for nas, since this user is only used for writing. Besides that, a separate folder is created for each of the other 6 users.
- In order for nas to be used for writing, this user must also be specified as the owner at the end.

```shell
cd /mnt/nas/
sudo mkdir shares
cd shares/
sudo mkdir {user1,user2,user2work,user3,user4,family}
sudo chown -R nas: /mnt/nas/shares/
```



#### Set up shares

- To do this, we edit the `smb.conf` file.

- For the normal users, the example of user1 can be used. Make sure that everywhere user1 *(also in the path to the folder)* is aligned with the real name.

- The example from the family can be used for all public shares.

  Just add it at the end of the file.

- In addition, the line `map to guest = bad user` must be changed to `map to guest = never`, so that Windows10 users can also use the share without errors. Otherwise "network errors" might occur.

```shell
sudo nano /etc/samba/smb.conf

# user1
[user1]		# The name of the share.
comment = User1		# This comment appears e.g. in Explorer.
path = /mnt/nas/shares/user		# This is the folder for all files of User1.
write list = user1
valid users = user1
force user = nas
read only = no
browsable = yes

# family
[family]
comment = Family
path = /mnt/nas/shares/family
write list = user1,user2,user3,user4		# Enter all users who should have access here.
valid users = family,user1,user2,user3,user4		# In addition, of course, family must be added here.
force user = nas
read only = no
browsable = yes
```

**Note at this point: Whoever has the ubuntu or config passwords also has access to all files stored on the entire NAS.**

#### Last step

- The last thing to do is to restart Samba and allow it in the firewall

```shell
sudo service smbd restart
sudo allow smb on ufw
```

