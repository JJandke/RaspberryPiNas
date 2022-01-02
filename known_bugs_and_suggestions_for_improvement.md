# Known bugs and suggestions for improvement

## A hard drive being ejected continuously

In the beginning, I had the problem that one hard disk kept ejecting. If it was previously present as `/dev/sda`, it now had a different identifier, for example `/dev/sdc`.
This makes it impossible for a softwareraid to exist.

- **One problem** may be a **chip** in the SATA-USB adapter that is **not supported** by the Raspberry Pi. A list of good and bad working chips can be found in this [german Raspberry Pi forum](https://forum-raspberrypi.de/forum/thread/47876-magische-usb-sata-adapter-und-wo-sie-zu-finden-sind/?l=2).

  The chip in the adapter can be found with `sudo lsusb`.

  You will get the ID built from **VendorID:ProductID** (here *174c:55aa*) and the chip name (here *ASM1053E*).

   ```shell
   sudo lsusb   
   Bus 002 Device 004: ID 174c:55aa ASMedia Technology Inc. Name: ASM1051E SATA 6Gb/s bridge, ASM1053E SATA 6Gb/s bridge, ASM1153 SATA 3Gb/s bridge, ASM1153E SATA 6Gb/s bridge
   Bus 002 Device 003: ID 174c:55aa ASMedia Technology Inc. Name: ASM1051E SATA 6Gb/s bridge, ASM1053E SATA 6Gb/s bridge, ASM1153 SATA 3Gb/s bridge, ASM1153E SATA 6Gb/s bridge
   ```

   If the chip used is known not to work with the Raspberry Pi, a SATA-USB adapter should be purchased that has a different chip. It is important that the adapter has a 12V power supply to support 3.5" hard drives.
  
  *Alternatively, an adapter without 12V connection can be converted to work as an active adapter with an additional 12V power supply. You can find a tutorial in [this video](https://youtu.be/bS5Wsu1iSsY). It is important that you solder the correct pins, otherwise you will destroy the hard drive and the adapter.*
  
- **In my case**, however, the actual problem was not with the chip but with a **broken adapter**. Whenever large amounts of data were written quickly, the hard drive was ejected. This problem only occurred on USB 3.0 ports. If the adapter was used on the USB 2 ports, there were no problems, since it could not be written faster. *In anyway, that's my guess. On the internet, after three months of googling and troubleshooting, I found many of the same error messages, but never due to the same cause as mine.*
  The corresponding **error message** in dmesg looked like this:

  ```shell
  [   26.655337] usb 2-1.3: reset SuperSpeed Gen 1 USB device number 4 using xhci_hcd
  [   26.675456] usb 2-1.3: device firmware changed
  [   26.676075] usb 2-1.3: USB disconnect, device number 4
  [   26.677875] sd 1:0:0:0: [sda] Synchronizing SCSI cache
  [   26.682735] blk_update_request: I/O error, dev sda, sector 4278068096 op 0x0:(READ) flags 0x4000 phys_seg 64 prio class 0
  [   26.693962] md/raid1:md0: sda: unrecoverable I/O read error for block 4277801856
  [   26.694100] sd 1:0:0:0: [sda] Synchronize Cache(10) failed: Result: hostbyte=DID_NO_CONNECT driverbyte=DRIVER_OK
  [   26.694455] blk_update_request: I/O error, dev sda, sector 4278069120 op 0x0:(READ) flags 0x0 phys_seg 16 prio class 0
  [   26.701599] md/raid1:md0: sda: unrecoverable I/O read error for block 4277801856
  [   26.791899] md: super_written gets error=10
  [   26.993210] md: md0: recovery interrupted.
  [   27.083098] usb 2-1.3: new SuperSpeed Gen 1 USB device number 5 using xhci_hcd
  [   27.085930] md: super_written gets error=10
  [   27.104118] usb 2-1.3: New USB device found, idVendor=174c, idProduct=55aa, bcdDevice= 1.00
  [   27.104127] usb 2-1.3: New USB device strings: Mfr=2, Product=3, SerialNumber=1
  [   27.104132] usb 2-1.3: Product: ASM105x
  [   27.104136] usb 2-1.3: Manufacturer: ASMedia
  [   27.104140] usb 2-1.3: SerialNumber:      WD-WCC7K0ZET7JE
  [   27.106951] usb 2-1.3: UAS is blacklisted for this device, using usb-storage instead
  [   27.106961] usb-storage 2-1.3:1.0: USB Mass Storage device detected
  [   27.110837] usb-storage 2-1.3:1.0: Quirks match for vid 174c pid 55aa: c00000
  [   27.110986] scsi host2: usb-storage 2-1.3:1.0
  [   27.159740] md: super_written gets error=10
  ```

  Finally, I found the affected adapter and replaced it. Even if `dmesg` is still spammed with the following line, the **hard disk remains mounted**. I am afraid that there might be an additional problem with the USB 3.0 connection of the Raspberry Pi. Since I don't have another Pi 4 available, it will take some time until I can confirm or exclude this problem.

  ```sh
  [12414.494229] usb 2-1.2: reset SuperSpeed Gen 1 USB device number 3 using xhci_hcd
  ```

  

- 

