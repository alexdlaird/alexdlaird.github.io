---
title: "DD-WRT NAT Loopback Issue"
date: 2013-04-23
tags: 
  - "instructional"
---

NAT loopback is what your router performs when you try to access your external IP address from within your LAN. For instance, say your router forwards port 80 to a web server on your LAN. From an outside network, you could simply visit your external IP address from a browser to access the web server. Internally, if NAT loopback is disabled or blocked, you would not be able to access this the same way.

There are any number of valid reasons why you'd want to allow NAT loopback on your network. If you're like me, you simply want internal and external access to operate in the same way. NAT loopback is needed to accomplish this, and it is simple and safe. Don't be fooled by the plethora of forum posts crying that NAT loopback is disabled on routers purposefully, that it opens up dangerous security holes, or that it will destroy your network and ultimately your livelihood as you know it. Like the vast majority of scare tactic-based content on the internet, it's false. Your router will not stab you in your sleep if you allow NAT loopback ... although it may emit higher levels of radiation, lace your lipstick and food with carcinogens (compliments of the government, of course), and kill Brad Pitt. Again. Coincidentally, the posts never specify _why_ the claims might be true, lack credible sources, and are rarely found outside of back alley forums. We're still talking about NAT loopback, right? The internet has made us so gullible ...

The primary reason for the security concern is that some consumer routers appear to intentionally disable NAT loopback by default, and there is no way around this with stock firmware. However, this is not an intentional barrier, it's just a constraint of limited stock firmware. Nothing new there. The simplest solution to this is, as usual, to [flash DD-WRT to your router](http://www.dd-wrt.com/wiki/index.php/Installation). Then, follow this tutorial to allow NAT loopback.

# Implementation

Before proceeding, ensure NAT loopback actually doesn't work with your version of DD-WRT. Different versions of DD-WRT implement NAT with slight variances, so it's possible your version of DD-WRT may not actually need the special rules below.

To check if NAT loopback is working on your router, you'll need your external IP address. If you don't know your external IP address, just [Google "what is my ip"](https://www.google.com/search?q=what+is+my+ip). Now, open a Command Prompt and ping your external IP address. If the command times out, NAT loopback is not working.

In the DD-WRT Control Panel, navigate to the “Administration” tab and click on “Commands”. Add the following rules, then click “Save Firewall” to ensure the rules execute even after the router is rebooted.

```bash
insmod ipt_mark insmod xt_mark iptables -t mangle -A PREROUTING -i ! `get_wanface` -d `nvram get wan_ipaddr` \\\\ -j MARK --set-mark 0xd001 iptables -t nat -A POSTROUTING -m mark --mark 0xd001 -j MASQUERADE
```

# Conclusion

That's it! Now, try pinging your external IP again from the Command Line. This time you should receive packets.

DD-WRT is a always evolving. The developers have stated that they aren't planning on fixing this issue, but if this procedure doesn't work for you, leave a comment below and I'll check to see if something has changed in the latest version of DD-WRT. I’ll try to always keep the tutorial updated with instructions for the latest DD-WRT build.

Also, if you previously followed [my DD-WRT Guest Wireless tutorial](http://alexlaird.com/2013/03/dd-wrt-guest-wireless/), this fix should work for both interfaces.
