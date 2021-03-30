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

- ​	**[Raspberry Pi 4B](https://www.amazon.de/Raspberry-Pi-Ersatzteil-Single-Board-102110421/dp/B0899VXM8F/)** (I recommend the 8GB RAM version, as it is not much more expensive compared to other NAS solutions)
- ​	**[Power supply](https://www.amazon.de/Voltcraft-CNPS-45-USB-C-LADEGER%C3%84T/dp/B07DC97TMM/ref=sr_1_13?__mk_de_DE=%C3%85M%C3%85%C5%BD%C3%95%C3%91&dchild=1&keywords=voltcraft+usb+c&qid=1617098220&sr=8-13)** (PSU) for the Pi (5V, 3A, 45W, UBS-C, surge- and overload protection)
- ​	**[Micro SD card](https://www.amazon.de/SanDisk-microSDHC-Speicherkarte-SD-Adapter-App-Leistung/dp/B08GY9NYRM/ref=sr_1_4?__mk_de_DE=%C3%85M%C3%85%C5%BD%C3%95%C3%91&dchild=1&keywords=sandisk+micro+sd&qid=1617098301&sr=8-4)** (32GB)
- ​	**[Active cooling case](https://www.amazon.de/Miuzei-Raspberry-Aluminium-K%C3%BChlventilator-W%C3%A4rmeleitklebeband/dp/B08FSP9VL6/ref=sr_1_36?__mk_de_DE=%C3%85M%C3%85%C5%BD%C3%95%C3%91&dchild=1&keywords=raspberry+pi+4+case&qid=1617098453&sr=8-36)** for the Pi
- ​	**[USB 3 Hub](https://www.amazon.de/dp/B01K7RR3W8/?coliid=I2D76GQUSANVR8&colid=19V8MGZC0S3K3&psc=1&ref_=lv_ov_lig_dp_it)** (This turned out later)
- ​	**[Active USB-SATA adapter](https://www.amazon.de/Inateck-Konverter-Adapter-Laufwerke-Netzteil/dp/B00N4JLNXM/ref=sr_1_5?__mk_de_DE=%C3%85M%C3%85%C5%BD%C3%95%C3%91&dchild=1&keywords=usb-sata+adapter+active&qid=1617099266&s=computers&sr=1-5)**
- ​	**[Hard drives](https://www.amazon.de/interne-NAS-Festplatte-Festplatte-NASware-Technologie-Cache/dp/B083XVY99B/ref=sr_1_4?__mk_de_DE=%C3%85M%C3%85%C5%BD%C3%95%C3%91&dchild=1&keywords=wd+red+4tb+64mb&qid=1617100376&s=computers&sr=1-4)** (4TB WD red)
- ​	[Power supply](https://www.amazon.de/Schaltnetzteil-Netzteil-MeanWell-LRS-100-24-Treiber/dp/B06XWR8RGJ/ref=sr_1_13?dchild=1&keywords=meanwell+24v&qid=1617100444&sr=8-13) for the case fans (24V, 4.5A)
- ​	[2 relay module](https://www.amazon.de/YXPCARS-Relais-Optokoppler-Arduino-Raspberry/dp/B08G1587VT/ref=sr_1_5?__mk_de_DE=%C3%85M%C3%85%C5%BD%C3%95%C3%91&dchild=1&keywords=2+relay+module&qid=1617100501&sr=8-5) (to switch the two case fans and the fan on the Raspberry Pi)
- ​	Ethernet feedthrough (To connect an Ethernet cable to the case, as it would be with a real server)
- ​	Ethernet patch cable (20cm)
- ​	Switch (250V, 10A, for the Case)
- ​	Fuse (4.5A)
- ​	MC 7805 (Fixed voltage regulator)
- ​	Capacitors (2200µF, 10 µF, 100nF – more details later)
- ​	Diode (1N4001)
- ​	Jumper cables

![Components_lr](https://user-images.githubusercontent.com/56551925/112286936-22145500-8c8c-11eb-85e4-9198a3d877bb.jpg)

We'll continue with the hardware in part 1.
If you are only interested in setting up and configuring the server on a Raspberry Pi, you can immediately jump to part 2.
