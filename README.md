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

- ​	**[Raspberry Pi 4B](https://www.amazon.com/dp/B0899VXM8F/)** (I recommend the 8GB RAM version, as it is not much more expensive compared to other NAS solutions)
- ​	**[Power supply](https://www.amazon.de/dp/B07DC97TMM/)** (PSU) for the Pi (5V, 3A, 45W, UBS-C, surge- and overload protection)
- ​	**[Micro SD card](https://www.amazon.com/dp/B08GY9NYRM/)** (32GB)
- ​	**[Active cooling case](https://www.amazon.com/dp/B08FSP9VL6/)** for the Pi
- ​	**[USB 3 Hub](https://www.amazon.com/dp/B01K7RR3W8/)** (This turned out later)
- ​	**[Active USB-SATA adapter](https://www.amazon.de/dp/B00N4JLNXM/)**
- ​	**[Hard drives](https://www.amazon.com/dp/B083XVY99B/)** (4TB WD red)
- ​	[24V Power supply](https://www.amazon.de/dp/B06XWR8RGJ/) for the case fans (24V, 4.5A)
- ​	[2 relay module](https://www.amazon.de/dp/B08G1587VT/) (to switch the two case fans and the fan on the Raspberry Pi)
- ​	[Ethernet feedthrough](https://www.amazon.com/dp/B002BEWOYI/) (To connect an Ethernet cable to the case, as it would be with a real server)
- ​	[Ethernet patch cable](https://www.amazon.de/dp/B018M6PR10/) (25cm)
- ​	[Switch](https://www.amazon.de/dp/B07TTJWMT3/) (250V, 10A, for the Case)
- ​	[Fuse](https://www.amazon.de/dp/B001C6JSAY/) [(4.5A)](https://www.amazon.com/dp/B076F223W5/)
- ​	MC 7805 (Fixed voltage regulator)
- ​	Capacitors (2200µF, 10 µF, 100nF – more details later)
- ​	Diode (1N4001)
- ​	[Jumper cables](https://www.amazon.com/dp/B01EV70C78/)

![Components_lr](https://user-images.githubusercontent.com/56551925/112286936-22145500-8c8c-11eb-85e4-9198a3d877bb.jpg)

We'll continue with the hardware in part 1.
If you are only interested in setting up and configuring the server on a Raspberry Pi, you can immediately jump to part 2.
