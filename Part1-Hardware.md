## Part 1 - The enclosure (not important for the NAS itself)

### Mounting the devices:

After opening the 19" case, and removing the actual PCB, I was also able to unscrew the front panel and get access to the **fans**. Of course, these had to be **cleaned** first. I decided to further disassemble the **front** panel and **spray paint** it completely **black**. In order for the paint to hold better, I had to sand it down a bit.

![Case](https://user-images.githubusercontent.com/56551925/111883898-623eb380-89be-11eb-8749-140fd528fdc3.jpg)




Then I had to think about the actual allocation of the devices in the case. This was only possible to a limited extent before, because I didn’t have any specifications of the power supplies for the USB-SATA adapters. I had originally wanted to take a black **multi-socket**, but the **plugs** there were **arranged** at an **45° angle**, so that the **power supplies** would then have been too high and would no longer have fit into the housing. Therefore, I had to search for a multi-socket with **straight plugs**.

Now that I knew what should go where, I could start attaching the parts. The **Ethernet feed through** I could simply **attach** to the place of a previous **speakOn** **port**, for this I only had to drill two holes for the screws. For the **relay**, the **24 V power supply** and the **Raspberry Pi**, I marked the **holes** and punched them so I could drill them with a 2.5 and **3mm** drill bit. I was able to immediately screw the 24V power supply to the bottom of the case. But since the **relay** module was **not insulated** at the bottom side of the PCB, I had to **mount it on spacers** and attach a small plastic sheet.

![Mounting](https://user-images.githubusercontent.com/56551925/111883909-6f5ba280-89be-11eb-9345-6a6ddf9a31aa.jpg)




I had long been wondering how I would **mount** the **Raspberry Pi**. In the end, the best **solution** was to **mark** the four **holes of the base plate**, with a scriber on the bottom of the amp, and then **screw** the **Raspberry Pi case to the power amp case** with longer screws. Since the fans were clean again in the meantime, I could screw them into the case as well.

In order not to damage the hard drives during assembling the NAS, I took two old ones to mark the proportions. Then the hard drives were fixed with metal brackets. To **allow air** to get under the hard drives and **reduce vibrations** at the same time, I packed **rubber spacers** between both, the metal brackets and the case bottom.

![Drives](https://user-images.githubusercontent.com/56551925/111883953-adf15d00-89be-11eb-98e4-7316923f7c14.jpg)


After all the important components were fixed, I could start the wiring.



### AC wiring:

I decided to use the screw terminals on the 24V power supply to be able to connect the multisocket there. So I had to remove the plug, and strip the three stranded wires. I crimped ferrules onto the stripped ends and then screwed them *(L2, N2, PE2)* to the AC input side of the terminal block on the 24V power supply.

- From the **incoming mains** cable, I was able to connect the **neutral** conductor *(N1)* directly to the **power supply**, using a wire end ferrule.
- The **phase** *(L1)*, I first connected to a 4.5A **fuse**. In my case, I was able to insulate the solder joints of the fuse holder well with heat shrink tubing and electrical tape.
- Then *L1* was **looped** to the **switch** *(250V, 10 A)*. There I used insulated cable lugs to be able to plug and unplug the switch easily. Next, the phase was **pulled** back to the **power supply**. Since I have an illuminated switch, I also had to connect the neutral *(N3)* to the switch.
- Because only two cable ends fit on the terminal strip of the 24V PSU, this neutral conductor *(N3)* had to be connected with a terminal plug.
- I also screwed the **protective conductor** *(PE2)* of the **multiple** socket to the **terminal strip** of the power supply.
- In order to be able to **connect** the **protective conductor** of the mains cable and the power supply *(PE3)* and the incoming cable *(PE1)* **with the housing**, I have sanded down an unpainted area again and screwed both protective conductors using a toothed ring.

After an isolation test, I was able to plug it in for the first test. Fortunately, nothing blew up in my face, nothing exploded, and everything behaved as it should.... except the switch… Wiring this power switch was a bit difficult, as it had an LED that was supposed to indicate if the switch was set to on or off.... but it was not quite clear in which positions what happened. So it took me a few tries before I knew the correct wiring, as the manufacturer did not include instructions.

Now that the AC part is done, I'll take care of the DC part.

![ACCircuitDiagram](https://user-images.githubusercontent.com/56551925/111884027-2526f100-89bf-11eb-8a93-77edce941b24.png)

![RPINAs00051](https://user-images.githubusercontent.com/56551925/111884042-396aee00-89bf-11eb-84e6-566a5e8d6e1e.jpg)

![ACWiring](https://user-images.githubusercontent.com/56551925/111884053-50a9db80-89bf-11eb-8a10-b0990ccb69a0.jpg)




### DC wiring:

This seems complicated because there are many cables, but it is **relatively simple**.

- To **reduce a few cables**, and to be able to connect the fans well, I **soldered** a board to which I can **plug** **both** **fans** on one side and the 24V is connected on the other side. GND goes directly to the power supply and +24V are switched via relay1. As it turned out later, the **fans vibrated** very strongly **at 24V**. At 20V, however, they ran quietly. **Therefore I soldered a 85 Ohm power resistor in front of each fan**. From the fan of the Raspberry PI you can also plug GND directly to a GPIO. I connected the +5V with a jumper cable to relay 2 and led it back again, so I didn't have to cut and solder a cable. This would make the fan more replaceable.

  ![RPINAs00096](https://user-images.githubusercontent.com/56551925/111884069-66b79c00-89bf-11eb-80dc-5876bbace17a.jpg)

- To **switch the relay**, we need to connect +5V (VCC) and GND (GND) from the Raspberry Pi as power supply to the relay module. We also need GPIO 04 (IN1) and GPIO 17 (In2) to switch the relays. The jumper has to be set between VCC and RVCC. Now the relay would theoretically already work, but the Raspi would **not** **be** **galvanically** **separated** from the relay module. 

  

- To **achieve** this by using the **optocouplers** on the PCB, the jumper must be **removed** and a voltage of +5V must be **connected** to RVCC and GND.

  Since I don't have a 5V voltage source in the case, I built myself a **voltage converter** with a **fixed voltage regulator** with the following schematic:

  *On the **In** Pin of the MC7805 **+24V** are applied. Also an electrolytic **capacitor** is connected between **+24V** and GND. The **middle** pin (GND) is also connected to **GND** and the Out pin is **connected** to RVCC on the relay board. **Between** the **out** pin and **GND** an electrolytic capacitor with 10µF and a **ceramic** **capacitor** with 100nF are connected. To **protect** the **MC7805** from a too **high** **voltage** **at** the **Out** pin, a 1N4001 **diode** is connected **between** **In** and **Out**. The capacitors smooth the voltage. The GND of the circuit is connected to GND on the relay board.*

  *Because 19V drops at the fixed voltage regulator, it can get very hot. Therefore I took an old heat sink, which was previously installed in the power amp, and attached the MC7805 to it. I used a fixed voltage regulator instead of a DC/DC converter, because I had one at home. In addition, the 5V are only needed for the switching operations of the relay. Therefore the heat sink is theoretically not necessary. But since I might need the 5V output for other stuff and it does look good, I decided to use it.*

  ![DCCircuitDiagram](https://user-images.githubusercontent.com/56551925/111884099-8b137880-89bf-11eb-94a4-36d9b9609c7a.png)



- Now all that's left to do is plug in the power supplies, **connect** the **hard drives to the Pi**, and create a **connection** with the 20cm patch cable between the Pi and the **Ethernet** **feedthrough**.

At this point it is important to add that it turned out later that you **need** an additional **active USB hub** between the **Raspberry Pi** and the **active SATA USB** **adapters**. When setting up the NAS, I struggled almost continuously with one of the disks being kicked out. `sudo dmesg` always returned errors that looked like this: `over current change #54`. There were other errors, but they were software related. After weeks of trying and researching I found someone with the same problem. His hard drives were also thrown out, although he also used active SATA USB adapters. Indeed. With an **active USB hub I didn't get these error** messages anymore. Interesting to know is that the active USB hub drew only 0.2A(DC) in IDLE and almost 1A(DC) in use. From this I conclude that the active adapters could not supply enough current. Now that the Raspberry Pi has been expanded with more USB3 ports, I'm also thinking of moving the operating system to an SSD, as these are more durable than SD cards.

![USBHub](https://user-images.githubusercontent.com/56551925/111884107-9666a400-89bf-11eb-9b5b-99c40f279004.jpg)



Of course, good **cable management** is important, so that cables do not unplug themselves and that it is easier to upgrade later.

To stop dust that would be sucked in by the fans, I sandwiched a strip of filter floss for servers between the chassis and the fans.

![Case2](https://user-images.githubusercontent.com/56551925/111884127-d168d780-89bf-11eb-96ea-d041c426a44a.jpg)



After flashing the Micro SD card (See Part 2) I was able to insert it into the Raspberry Pi and then attach the black painted front panel as well as the lid.

**About switching the fans:** Since the fans do not support PWM out of the box, it would be an idea to control the fans with MosFets instead of just a relay, to control their speed proportional to the temperature.

**Now we continue in part 2, since we have already done everything that has to do with hardware.**