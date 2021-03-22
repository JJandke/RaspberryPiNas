# Raspberry Pi 4 NAS out of an old power amplifier

A Raspberry Pi 4 as NAS server with two WD red 4TB out of an old 19" power amplifier case.

------



![BeforeAfterCase](https://user-images.githubusercontent.com/56551925/111883854-1a1f9100-89be-11eb-9ec6-4a5eba319a4f.jpg)


![BeforeAfter](https://user-images.githubusercontent.com/56551925/111883862-21df3580-89be-11eb-9e3b-cf0f6020e6c0.jpg)


### Story:

I had played around with the NAS feature of my router in the past, but quickly reached its limits. Since then, I was looking for a NAS solution for my whole family. Best to build it myself. I already had a few Raspberry Pis at home and when the PI 4B came out, this was the perfect moment to get this project started.

Around the same time, a power amp at my school broke. Since I am involved in sound engineering there, it was no problem to get hold of it. So, I had a case in which all components would fit.



### This project is divided into two parts.

In **part 1** we take care of the **hardware**, i.e. the cabling of the individual devices and especially also the installation in the power amp case.

In **part 2** we will install the **operating** system and **set up** the **NAS.**

If you are **only** interested in the **software** part and setting up the NAS with Ubuntu Server, you can jump straight to the **second** **part**.

**Attention!** Working on mains voltage is life threatening and should only be done by qualified personnel. Some steps shown here should only be done if you know exactly what you are doing. Furthermore, a multiple socket, as shown here, should never be used for permanent installations.



### Specs:

- ​	Raspberry Pi 4

- ​	8 GB DDR3 SDRAM

- ​	Gigabit Ethernet

- ​	4 TB RAID 1 Storage

   

### What you need:

*Note: For a pure Raspberry Pi 4 NAS without amp case, we only need those articles in bold.*

- ​	**Raspberry Pi 4B** (I recommend the 8GB RAM version, as it is not much more expensive compared to other NAS solutions)
- ​	**Power supply** (PSU) for the Pi (5V, 3A, 45W, UBS-C, surge- and overload protection)
- ​	**Micro SD card** (32GB)
- ​	**Active cooling case** for the Pi
- ​	**USB 3 Hub** (This turned out later)
- ​	**Active USB-SATA adapter**
- ​	**Hard drives** (4TB WD red)
- ​	Power supply for the case fans (24V, 4.5A)
- ​	2 relay board (to switch the two case fans and the fan on the Raspberry Pi)
- ​	Ethernet feedthrough (To connect an Ethernet cable to the case, as it would be with a real server)
- ​	Ethernet patch cable (20cm)
- ​	Switch (250V, 10A, for the Case)
- ​	Fuse (4.5A)
- ​	MC 7805 (Fixed voltage regulator)
- ​	Capacitors (2200µF, 10 µF, 100nF – more details later)
- ​	Diode (1N4001)
- ​	Jumper cables

![Components_lr](https://user-images.githubusercontent.com/56551925/111883871-315e7e80-89be-11eb-8808-b6d4dbe8cb20.jpg)

We'll continue with the hardware in part 1.
If you are only interested in setting up and configuring the server on a Raspberry Pi, you can immediately jump to part 2.
