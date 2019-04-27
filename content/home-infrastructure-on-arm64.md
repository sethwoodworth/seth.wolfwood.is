Title: Home Network Infrastructure on ARM64 SBC
Date: 2019-03-30 12:12
Tags: arm64 'Single-Board Computer' FOSS OpenWRT
# Home Infrastructure Part 1: Espressobin v7

I've been running DD-WRT on my router / WAP, a Linksys 1900ACS v2 for a few years.
It's a fine router, but I'd been seeing some stability issues with the temperature sensor after setting up HomeAssistant's DD-WRT integration for detecting which devices are currently active on the home network.

I've been reading about single-board computers lately, alternatives to the Raspberry Pi.
Back in Highschool I was fascinated by the PC/104 micro computer form-factor.
The MIT Media Lab's wearable computer team used PC/104 boards for a few of their [wearable computing platforms](https://web.archive.org/web/20190330020156/https://www.media.mit.edu/wearables/history.html), and I've been interested in small computers running linux ever since.

The Espressobin is a router SBC with a built-in 3-port switch.
They run a Marvell Armada 3700LP dual-core ARM Cortex A53 processor that runs upto 1.2Ghz.
It has three 1GB ethernet ports, a MiniPCIe slot, and 1 or 2Gb of DDR4 ram.
It consumes around 1W of power when running at 1Ghz.

I read a [blogpost about building a home router](https://blog.tjll.net/building-my-perfect-router/)
with an Espressobin.
The author, who wrote their post in April 02018, had [trouble getting PCIe wifi cards working](https://blog.tjll.net/building-my-perfect-router/#what-about-wifi).
I've seen some indications that this was a software configuration issue involving incorrect PCIe timing.
Given that the Espressobin wiki [now has a page detailing how to configure a PCIe card](https://web.archive.org/web/20190330024526/http://wiki.espressobin.net/tiki-index.php?page=Configuring+Realtek+RTL8191SE+mini+PCIe+WiFi+card)
I suspect this issue has been resolved.
Regardless, my ISP uplink terminates in my basement, so I don't really need a wireless AP in my basement.
I need an edge router that connects to a switch in the basement, where the house's ethernet cables terminate.
I can always add a wifi card later.
In the meantime, I can use my existing Linksys as a WAP.

## OpenWRT
After evaluating the status of the DD-WRT and OpenWRT projects,
I decided I liked the package management system of OpenWRT.
Also OpenWRT build instructions exist on the Espressobin wiki,
and the 18.06 release of OpenWRT has builds for the Marvell cortex a53.


### U-Boot
The first step is connecting to the bootloader via serial and poking around.

The Espressobin uses U-Boot, the [Universal Boot Loader](https://www.denx.de/wiki/U-Boot).
I'd heard of uboot before, but never learned what it was, or knowingly interacted with it.
In the README of uboot, the software is described thusly:

> U-Boot, a boot loader for Embedded boards based on PowerPC, ARM, MIPS and several other
> processors, which can be installed in a boot ROM and used to
> initialize and test the hardware or to download and run application code.

You connect to the uboot console via the usb port, which does usb to serial.
The [Espressobin linux instructions for connecting to uboot](https://web.archive.org/web/20190330002612/http://wiki.espressobin.net/tiki-index.php?page=Serial+connection+-+Linux)
via serial suggest using [C-Kermit](http://www.kermitproject.org/) or Minicom.
Both disappointed me for one reason or another.
It's been several years since I've connected to a serial connection and I'd completely forgot that I could just use `screen`.

    sudo screen /dev/ttyUSB0 115200

I prefer `tmux` these days, but I'd used screen for a few years,
and remember how to use the scrollback pager,
the major feature I was missing in Kermit/Minicom (which may exist, but I didn't find them).

I had some trouble getting the wiki documentation uboot instructions to work.
I believe the instructions were written for the Espressobin v5,
and the v7 had just become available and not all documentation was yet updated.

I ended up working from [this thread](https://web.archive.org/web/20190329233806/http://espressobin.net/forums/topic/will-openwrt-18-06-mvebu-cortexa53-work-on-espressobin/) on the espressobin forums.
This [Polish article on running OpenWRT v18.06.0](https://web.archive.org/web/20190329234307/http://gdr.geekhood.net/gdrwpl/18-08-01_openwrt_oficjalnie_na_espressobin.html) on the Espressobin was also incredibly helpful.
The post was written in January 02018 so I assume the author, GDK (a fellow [vimmer](http://gdr.geekhood.net/.vimrc), was using the espressobin v5 at that point.
The uboot configuration I ended up using is stored in [this file](https://github.com/sethwoodworth/openwrt-for-espressobin-v7/blob/4f63436434b1a1aa2ebe874ba2d0148e4239d1d1/extra/printenv.2019-03-04),
which is the output of the uboot `printenv` command.
At this point I still had some doubt that this configuration would work on the v7 version of the board.
But it appears that the differences between the v5 and v7 boards is likely encapsulated in the 
[device tree file](https://github.com/sethwoodworth/openwrt-for-espressobin-v7/blob/4f63436434b1a1aa2ebe874ba2d0148e4239d1d1/extra/armada-3720-community-v7.dtb).

### OpenWRT
The Espressobin v5, the previous revision of the device, required compiling OpenWRT 17.10,
as described on the [Espressobin wiki](https://web.archive.org/web/20190329231702/http://wiki.espressobin.net/tiki-index.php?page=Build+From+Source+-+OpenWrt).

I ended up trying to compile the [openwrt_18.06.1_release](https://github.com/MarvellEmbeddedProcessors/openwrt-dd/tree/openwrt_18.06.1_release) of openwrt-dd from Marvell's source repo.
I'd compared the difference between Marvell's branch and the [upstream openwrt](https://github.com:openwrt/openwrt.git) and learned a ton from the changes [Derek0425 (JIA)](https://github.com/Derek0425) had made on top of the upstream OpenWRT.

In the process of trying to compile OpenWRT, I ran into an issue where my version of glibc on Debian Buster was 2.28, and the compilation expected a version of glibc where in `lib/fseterr.c` had a flag of `_IO_ERR_SEEN`.
Luckily I wasn't the first with this problem, and was able to find a patch on the [OpenWRT-Devel mailing list](https://web.archive.org/web/20190329232642/https://www.mail-archive.com/openwrt-devel@lists.openwrt.org/msg43023.html).
The patch had me add [this file](https://github.com/sethwoodworth/openwrt-dd/blob/f73dfd2a4ea3601bfe2fb4fef512b47550725b81/tools/bison/patches/110-glibc-change-work-around.patch).
At build time, `bison` applied this directory of patches before compiling.

Another step of compiling OpenWRT and the OpenWRT kernel involved running `make menuconfig`.
I haven't compiled a kernel requiring menuconfig since I'd first tried installing RedHat 6 on a surplus eMachine in a computer class in Highschool.

But ultimately I found that I could use the off-the-shelf OpenWRT 18.06.02 build for the processor and board, named `mvebu-cortexa53-globalscale-espressobin`.
Slightly disappointing that I didn't end up compiling OpenWRT myself, but I learned a lot in the process.

I copied the image to an SD card, booted it up and had the LUCI interface to OpenWRT running.
I didn't use `dd` to create the boot sd-card.
It turns out that `dd` uses a fixed block size while copying disks, which can be much slower than other equivalents.
I had thought that `dd` was needed to be able to write disks, but it turns out you can copy directly from an image file to the `/dev/` device (not the partition).
In this case, I did:

    sudo zcat openwrt-18.06.0-mvebu-cortexa53-globalscale-espressobin-ext4-sdcard.img.gz > /dev/mmcblk0

Also worth noting, the Espressobin case doesn't have a slot for the MicroSD card.
I had to use a set of clippers to remove part of the grill under the USB port to allow for swapping the SD card without disassembling the case.

### Built-in Switch confusion and success
The Espressobin has a built-in three port switch.
On the front of the device, the three ports are labeled WAN, LAN 1 & LAN 2.
There is a slight physical separation between the WAN and LAN ports.
This may seem like a tangent, but it explains some of my stubborness when getting over the next hurdle.

Now I had OpenWRT running, booting from an SD card and running the LUCI web interface.
I have Verizon FIOS at home, and I'd had a patch cord from the fiber endpoint to a switch,
through a cable running upstairs to my Linksys WRT1200AC.
I connected my new OpenWRT router's WAN to one of the Linksys' lan ports, and my laptop to one of the Espressobin's LAN ports.

Confusingly, the router wasn't getting a DHCP address from the Linksys.
Nor could I connect to the router over the ethernet connection to my laptop.
I set a static IP on the Router's LAN port and still couldn't connect from my laptop.
I _could_ run `mtr` and trace to the static IP, but the path went over my laptop's wifi connection through the existing router to what was labeled the WAN port of the Espressobin.
I banged my head against this problem during a few short bursts in the evening after work with little progress.
Eventually I ran across a [thread on the armbian forums](https://web.archive.org/web/20190330012846/https://forum.armbian.com/topic/4089-espressobin-support-development-efforts/?page=24&tab=comments)
on the Espressobin, discussing first how the bridging of the WAN and LAN ports means that the WAN/LAN distinction is arbitrary.
This thread discusses how the order of the ports is reversed!

Since the distinction is arbitrary anyway, I didn't try to swap the ports back around by recompiling.
After swapping the WAN and LAN cables, OpenWRT got a DHCP IP as expected from the Linksys, and from my ISP when I plugged it in directly.

## Conclusion & Next Steps

I've been using the Espressobin for about a month.
I haven't done any cross-lan speed tests worth mentioning,
but outward-bound speed tests say I'm getting ~76 Mbps of download,
which is 100%+ of my current 75/75 Mbps plan with my ISP.

I haven't resolved the issues with the existing WAP,
There was a sale on the TP-Link Archer a7 this week,
which is well supported by OpenWRT.
I ordered it, and will get it flashed and attached to my network when it arrives.

My next post will document my next SBC project: a Network Attached Storage NanoPi-m4 running OpenMediaVault.

