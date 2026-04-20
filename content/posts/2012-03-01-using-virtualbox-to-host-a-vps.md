---
title: "Using VirtualBox to Host a VPS"
date: 2012-03-01
tags: 
  - "instructional"
  - "servers"
---

Oracle's VM VirtualBox is a virtualization program that allows you to run another operating system from within your native operating system. Though it is most commonly used to run fully functional operating systems such as Linux or OS X from within Windows 7 (or vice versa), it can also be used to host a Virtual Private Server (VPS).

This post does nothing to compare benchmarks between more efficient (and recommended) VPS environments such as VMware or Linux-VServer, and I would not recommend using VirtualBox as a VPS in a production environment. However, it is useful in many situations, and I'll let you be the judge of when this should or should not be done. It is certainly acceptable for personal and developmental purposes. And hosting a VPS through something like VirtualBox that is extremely simply to setup and use allows you to easily experiment with configurations and operating systems, or even jump between multiple VPSs on the same computer.

This tutorial assumes you have a rudimentary knowledge of server software and operating systems. I'm going to be explaining virtualization to you, not the details of the server installation and configuration.

 

# Setting Up VirtualBox

First, some definitions. When I refer to the _host_ operating system, that is the primary operating system that your computer boots into. When I refer to the _guest_ operating system, that is the virtualized system that is run from within VirtualBox_._ There will also be references to IP address and ports on the _host_ and _guest_. They follow the same theme. Now that we've got that of the way ...

You can pick up VirtualBox for free from [their website here](https://www.virtualbox.org/ "VirtualBox"). Download and run the installer for your _host_ operating system. Congratulations. VirtualBox is now ready to run. Unfortunately, it doesn't have a _guest_ operating system installed or configured yet, so it doesn't do much for you. But before we actually install one of those, let's create a virtual environment for it and configure some VirtualBox settings.

In VirtualBox, click New to create an environment where we install a _guest_ operating system. I'm assuming you're a civilized human being and installing a Linux server operating system, so select Linux, then select the version of operating system you're using. If the exact version isn't in the VirtualBox list, select the parent Linux distribution (for instance, for CentOS you'd select Fedora).

Ideally, you should grant at least half of your host system's memory to the guest operating system. You should dedicate at least 8GB to the guests hard drive space. Luckily, since this is a virtual environment, you can select to dynamically allocate this space, so the virtual hard drive will only consume space on your host's hard drive as it is needed. Finish up the wizard, and the guest environment will be created.

Now, to make that guest environment accessible to our host computer. Right-click on the newly created environment and select "Settings". Click on "Network" in the list on the left, and click on "Adapter 2". Enable this adapter and, from "Attached to:" select "Bridged Adapter". This will cause the guest environment to resolve DHCP IP information directly from the host operating system, which means we can now forward some host ports directly to the guest operating system.

Go back to the "Adapter 1" tab, make sure this adapter is "Attached to: NAT", and click "Advanced". Click on "Port Forwarding" and add a new TCP forward. Let's call it "SSH". Specify 22 for the host and guest ports. This will forward the host machines port 22 to the guest machines port 22—they don't have to be the same, they just have to match other configurations on the host and guest side of things. It's also worth adding an "HTTP" forward for port 80 as well as any other the forwards for ports controlling any other services you'd like accessible from the guest environment.

 

# Server Operating System

If you haven't already, now's the time to choose what operating system you're going to use for your guest environment. I recommend Ubuntu Server if you're used to Ubuntu or Debian environments, and CentOS is another wildly popular one, though it's not my cup of tea. Whatever operating system you choose, download the ISO for it's installation and open up VirtualBox again.

Right-click on your guest environment and select "Settings". From the list on the left select "Storage", and point your virtual disc drive to the ISO you just downloaded. Once this is done, you can simply start the guest environment and it will boot with that disc "in the drive", so you can install that operating system in the guest environment.

If you're installing Ubuntu Server, selecting OpenSSH during the install process as well as LAMP and any other services you'd like available will make things much easier for you. However, as I said above, this tutorial assumes you have a rudimentary knowledge of server operating systems, so I'm not going to go into the details of installing those services. But to prove that our port forwards worked, you should at least install OpenSSH (during installation or as soon as you boot into the environment), and if you are able to SSH to your host computer on port 22 and access the guest environment, then everything worked the way it should have.

 

# Launching Server When Computer is Booted

It may be useful to launch this virtual server when the computer boots. To do this, create a BAT file with the following command:

_VBoxManage startvm "VM Name" --type headless_

Place a shortcut to this BAT file in the Startup folder of a (or all) user accounts and you're good to go. The server will launch and run in the background, allowing you to SSH into the server to control it from a terminal.

For maintenance purposes, you may also want to create a second BAT file for stopping the server (since it's running in the background with no visible window). To do so, create a BAT file with the following command:

_VBoxManage controlvm "VM Name" poweroff_

 

# Access from External IP

Login to your router and go the Port Forwarding section. Add a new port 22 forward, and forward that port to the IP address of the _host_. Do the same for port 80 and any other ports you added during the configuration above. Now, by typing in the external IP address of your network, you can SSH into the _guest_ operating system through port 22, and you can utilize other services available to other ports.

There's a lot more than can be done from here (using DNS to propagate to your external IP address, mail servers, etc.), but this tutorial has gotten you to the point where you can use tutorials for non-virtualized environments tutorials to accomplish those goals now. Good luck with your endeavors!
