---
title: "DD-WRT Guest Wireless"
date: 2013-03-23
tags: 
  - "instructional"
---

If you've done any amount of work with routers, you know that it doesn't take long to start craving consistency. And more advanced functionality that the cheap home interfaces simply don't grant you. This is the point where you usually break down and start research things like Tomato, OpenWrt, and DD-WRT, just to name a few of the more popular alternatives.

These alternate firmwares don't just provide a consistent administrative experience across all compatible models and brands, they also turn a cheap home router into a flexible and competitive enterprise router.

# My Setup

DD-WRT is my personal firmware of choice. Powerful, flexible, and stable. One thing that I demand in a router is the ability to broadcast a secondary SSID for my guest's to be able to access wireless internet in my home without also having access to my entire network of computers and devices.

Gladly, because my router's firmware was extremely slow and buggy, I flashed my [Cisco E2500 router](http://www.linksys.com/en-apac/products/routers/E2500) with ["mini" DD-WRT firmware](http://www.dd-wrt.com/phpBB2/download.php?id=21930) (the E2500 [also supports the "big" firmware](http://www.dd-wrt.com/wiki/index.php/Linksys_E2500)). But after reviewing getting the two wireless networks setup on my router, it was brought to my attention that there are no good tutorials for how exactly you are to do this using DD-WRT. The tutorial provided on their own website, in fact, does not work. So, I find that it falls upon me to put out my particular configuration for two mutually exclusive wireless networks from a single router, both networks having access to the WAN port (that is, internet access). There are, of course, multiple ways to do this. Feel free to leave alternative suggestions in the comments.

# Create Two Wireless Networks

First, create your wireless networks by clicking clicking on "Wireless" and then "Basic Settings". We'll setup security in a moment. After you've configured your private wireless network setup, click "Add" under "Virtual Interfaces" to add the "wl0.1 SSID". Give your guest network a separate SSID, and select "Enable" for "AP Isolation".

Now click "Save" and "Apply Settings".

![ssid](/assets/ssid.png)

# Setup Wireless Security

Navigate over to the "Wireless Security" tab. After you've setup the wireless security for your private network, setup similar security for your guest SSID. I would advise against leaving your guest wireless completely open, but since you're going to be giving out this password to your guests, it should probably be a little simpler than your private network's key.

Now click "Save" and "Apply Settings".

![security](/assets/security.png)

# Create Bridge

At this point, you have two wireless networks broadcasting on two separate SSIDs. Both networks should have internet access, but you'll also notice both networks dish out IPs in the same subnet, and both networks are clearly able to see each other. While you may like and trust your guests, that doesn't mean you necessarily want them to have access to all your network devices. To separate the network routing, we need to create a bridge and place the guest network into a different subnet.

Click on "Setup" and then on the "Networking" tab. Under "Create Bridge" click "Add" to add a new bridge. Give the bridge a name, and modify the IP address of the bridge to be in a different subnet than your private network. For example, my private network grants IPs in the subnet 192.168.1.0/24, so my guest network in the image below is setup to grant IPs in the subnet 192.168.2.0/24.

Now click "Save" and "Apply Settings". Though the page may refresh right away, you may need to wait about a minute before the bridge is available to use in the next few steps.

![create-bridge](/assets/create-bridge.png)

# Assign Guest Network to Bridge

Under "Assign to Bridge" click "Add". Select the new bridge you've created from the first drop-down, and pair it with the "wl0.1" interface.

Now click "Save" and "Apply Settings".

![assign-bridge](/assets/assign-bridge.png)

# Create DHCP Server for Guest Network

We're almost there! We've created a bridge in an alternate subnet, but the alternate subnet doesn't have a DHCP server, so our guests currently cannot access the guest SSID (unless they assign themselves a static IP). Scroll to the bottom of the "Networking" page and under "Multiple DHCP Server" click "Add". Ensure your newly created bridge name is selected from the first drop-down menu.

Now click "Save" and "Apply Settings". Congratulations, we now have a working, separate guest network! Unfortunately, while users can connect to the network and DHCP is running, guest users aren't able to access the internet quite yet.

![bridge-dhcp](/assets/bridge-dhcp.png)

# Create Firewall Rules for Guest Network

Navigate to the "Administration" tab and click on "Commands". We need to add three rules to our firewall settings before our private network is completely secure and our guest network has internet access. Add these three rules (one per line) to the "Commands" text field, then click "Save Firewall" to ensure the rules execute even after the router is rebooted.

```bash
iptables -t nat -I POSTROUTING -o `get_wanface` -j SNAT --to `nvram get wan_ipaddr` iptables -I FORWARD -i br1 -m state --state NEW -j ACCEPT iptables -I FORWARD -i br1 -o br0 -m state --state NEW -j DROP
```

![firewall](/assets/firewall.png)

# Improve Guest Security

Pete Runyan commented with a few more ways to nail down the security of the guest network. For one, your guests likely assume that their device on the guest network is not accessible from other devices on the same network, so you'll want to add the firewall rules below to make that true. It's also probably unnecessary (depending on your needs) to allow users on the guest network SSH, Telnet, or GUI access to the router. Append these firewall rules to harden the security of all of your networks!

```bash
iptables -I FORWARD -i br0 -o br1 -m state --state NEW -j DROP iptables -I INPUT -i br1 -p tcp --dport telnet -j REJECT --reject-with tcp-reset iptables -I INPUT -i br1 -p tcp --dport ssh -j REJECT --reject-with tcp-reset iptables -I INPUT -i br1 -p tcp --dport www -j REJECT --reject-with tcp-reset iptables -I INPUT -i br1 -p tcp --dport https -j REJECT --reject-with tcp-reset
```

# Conclusion

You should now have two working SSIDs: a private one for your home network, and a guest network for your visitors. Both networks should have internet access. The private network will function the same as a LAN and single wireless network did before, with the wireless network having full access to the LAN connections. The guest network, on the other hand, is separated from the private network. Additionally, each individual device on the guest network is separate from another, so guests cannot see each other.

If you've gotten to this point and something is not working, or your guest network does not have internet access, don't be alarmed. DD-WRT is a always evolving, and it's entirely possible bridge settings or firewall rules for the latest build have changed. If this tutorial does not produce the desired result, please leave a comment below. I'll try to always keep the tutorial updated with instructions for the latest DD-WRT build.

<div class="admonition important">


If you are using DD-WRT and experiencing issues with NAT loopback (accessing your public IP address from within your network), I have a tutorial to help resolve that issue [here](http://alexlaird.com/2013/04/dd-wrt-nat-loopback-issue/).

</div>
