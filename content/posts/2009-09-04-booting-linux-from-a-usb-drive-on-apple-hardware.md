---
title: "Booting Linux from a USB Drive on Apple Hardware"
date: 2009-09-04
tags: 
  - "apple"
  - "instructional"
---

After hours of frustration and failure, I finally set up a USB bootable Linux distribution that worked on both a BIOS-based PC or EFI-based Apple system. Ten minutes later, I repeated the process with a second distribution.

I’ve been perusing this fine internet of hours all day, reviewing and attempting to complete step-by-step tutorials that were supposed to allow me to do this. Unfortunately, none of them would actually work on my MacBook Pro, as they promised they would. After finally acquiring a resolution, I decided to post my own step-by-step set of instructions that also claimed to work for a BIOS system or an EFI system. Hopefully it actually works for you as it did for me :).

 

## My System, My Recommendation, and My Disclaimer

The systems I was trying to get this work was in conjunction with my out dated, 2008, 2 GHz Intel Core Duo MacBook Pro with a measly 2GB of 667 MHz DDR2 SDRAM. I dual boot between OS X Leopard and Windows 7 using Boot Camp. I plug into a 24” Samsung display and use a Bluetooth Logitech MX 5500 keyboard and mouse set at my desk. Using Slax, all of this was compatible and _immediately_ recognized!! I had absolutely no problems with hardware, so I highly recommend using Slax as your portable Linux distribution. I had success with DSL after initial frustrations (the track pad is not recognized, so I was forced to plug a USB mouse in), and it’s simply not as clean or power of a system as Slax is.

Doing all of this in no way effected positively or negatively the booting, reliability or functionality of OS X Leopard or Windows 7 on my system or Windows XP on any of the BIOS-based systems I ran this on. However, as always, proceed at your own risk.

I recommend the 4GB flash drive from Amazon below, as it is cheap and reliable. Though you don't need a full 4GB flash drive, if you ever want to throw a larger distribution of Linux onto the flash drive at any time, or if you'd like to use the drive for other storage at a later date, this is a good size and a great price.  Also ... it's hard to find a smaller drive than 4GB these days!

 

## Setting Up an EFI System

Boot into Mac OS and follow these steps:

1. Download and install [rEFIt](http://refit.sourceforge.net/ "SourceForge - rEFIt Project").
2. Restart your computer.

Complicated, huh? The initial restart after installing rEFIt will not show a boot loader, but all following restarts will display a boot loader if multiple bootable systems are attached to your Apple computer or other EFI-based system.

rEFIt will essentially overtake Boot Camp. Before installing rEFIt on my system, when I wanted to boot into Windows 7 I had to hold down the Alt-Option key when booting. Once rEFIt is installed, the boot menu is shown whenever the computer is booted. After a given number of seconds, it will boot into the default operating system, which is usually OS X.

 

## Setting Up a BIOS System

Your BIOS must support the ability to boot from a USB drive. Follow these instructions on a BIOS-based (any standard Windows-based) computer:

1. Restart your computer.
2. At some point your computer will inform you that you can press some key to enter the BIOS setup (probably some key like F8, F12, or Del). Hold that key down. If you miss it, restart and try again.
3. Unfortunately, every computer is different in the BIOS menu setup. Do not change anything you are unfamiliar.
4. You may need to enable the ability to boot from a USB drive.
5. You will most likely need to change the boot sequence, moving your USB drive higher than your standard HDD.
6. Make sure that you save your changes to the BIOS before restarting.

 

## Setting Up Your USB Drive

NOTE: Generally speaking, the instructions given on a portable Linux distribution’s website will tell you to run some bootinst.bat file that will configure your USB drive to boot properly. This will work for most BIOS-based systems, and may work with some distributions on some EFI systems, but it generally would not work for me. The solution given below, theoretically, works on all systems.

In a Windows environment (it’s just easiest that way, trust me), follow these steps:

1. Download and extract [Syslinux](http://syslinux.zytor.com/wiki/index.php/Download "Download Syslinux"). Since we’re in Windows, it’d be most beneficial to download the zip file. Extract it to a convenient location like C:\\Syslinux.
2. Download your favorite portable Linux distribution. It has been verified that this works with [DSL](http://www.damnsmalllinux.org/ "Download DSL") (I can’t spell it out ... My Mom reads this!), [DSL-N](http://www.damnsmalllinux.org/dsl-n/ "Download DSL-N"), and [Slax](http://www.slax.org/get_slax.php "Get Slax!").
3. Plug your USB drive into your computer.
4. Backup any data on the USB drive you wish to keep! Right-click on the USB drive and select “Format.” Format the drive to either FAT-16 or FAT-32. I recommend FAT-32. A quick format will be fine.
5. Extract the contents of your favorite portable Linux distribution onto your USB drive using [your favorite decompression program](http://www.7-zip.org/download.html "Download 7-Zip").
6. In Windows XP, click Start then Run, type “cmd,” then press Enter.
7. In Windows Vista or Windows 7, click Start and simply type “cmd.” Click on the Command Prompt icon to launch it.
8. From the Command Prompt, navigate to the win32 folder of where you extracted Syslinux. So, in my case, type “cd C:\\Syslinux\\win32\\”.
9. From the win32 folder of Syslinux, type “syslinux.exe -ma :” where is replaced with the drive letter of your USB drive. Most commonly this will be E or F (it does need to be followed by a colon), but you can verify this by checking in My Computer.
10. Assuming you don’t receive any errors, your USB drive should now be set up for booting.

 

## Conclusion

In theory, you should now be able restart your system and it will notice that you have a bootable USB drive in the computer (assuming, of course, that you do). If rEFIt opens, use the arrow keys to navigate to your USB drive and press Enter. If your on a BIOS system, you may need to press a key (if it tells you to press a key for the boot menu), but most likely it will pop up with a message telling you to press any key to boot Linux. If you don’t press any key, it may continue into your standard operating system, so you’ll want to strike that Enter key.

I hope this works as well for all of you as it did for me! It’s always handy to have a portable, friendly, and compatible version of Linux in your slacks that you can whip out and use anytime, on any computer.
