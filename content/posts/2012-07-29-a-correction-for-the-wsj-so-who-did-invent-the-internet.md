---
title: "A Correction for the WSJ: So, Who Did Invent the Internet?"
date: 2012-07-29
tags: 
  - "internet"
  - "politics"
---

Gordon Crovitz wrote an opinion piece for the Wall Street Journal titled _Who Really Invented the Internet?_ Fortunately, it's only an opinion piece, because there was little more than opinion, littered with plenty of misinformation, in the writing. You can read the article [here](http://online.wsj.com/article/SB10000872396390444464304577539063008406518.html).

Now, it's not like I look to the WSJ for the latest technology information (or, in this case, technology history). Far from it. And generally when a here's-the-truth-you-never-knew article starts with political propaganda, it's pretty safe to assume that whatever comes next is going to be absurd. The article's introduction could essentially be summarized as, "Obama said something that was true, but I'll be damned if I can't find a way to make it sound false!"

Even still, to those of us in the technology field, the "first computer" and "who invented the internet" discussions are highly revered and hotly debated, so when someone not in the industry starts boasting that they have a complete and final answer to these discussions, we just scoff. In Crovitz's defense, he seems to be confusing "internet" with "World Wide Web" and many other terms that merely relate to networking and computers. But that's about the extent I'd go to to defend him; he's a conservative author trying to make something out of nothing just because a liberal said it.

Due to the fact that I'm more than a little OCD, I wound up relating the history of internet technology through the ages to my Grandpa, who originally sent me the Crovitz article. Much of the details below are in response to specific parts of Crovitz's article, so, as painful as it may be, I recommend you [read that article first](http://online.wsj.com/article/SB10000872396390444464304577539063008406518.html). Alright, ready? Begin.

**Personal Computer**: The term "personal computer" was not coined until 1975 for the Altair 8800. However, it is disputed that Xerox created the first "personal computer", by whatever modern definition you use. IBM created the first electronic computer in 1953 (the IBM 701), Digital Equipment Corporation created the first digital computer in 1960, and Hewlett-Packard released the first mass-produced digital computer in 1968, the HP 9100A.

**Personal Workstation**: This is the term the WSJ author is looking for in their article. The first personal workstation, a "workstation" being a computer that can be connected to another computer (in this case, through the Ethernet technology he referenced), was created by Xerox in 1974. However, the computers used by ARPANet were technically also workstations, just not mass produced.

**Intranet** (take special note of the "a"): A connection between two or more computers within the same network. The network in your house is an "intranet".

**Internet** (take special note of the "e"): A connection between two or more networks. The wires that connect your house's network to mine are the "internet".

**ARPANet**: The first computer network (or "intranet"), created by the Department of Defense, which was fully implemented in 1969. I've never heard it associated with nuclear strikes or anything of the sort. It was created merely to replace slow and overused satellite communication between government agencies. When originally created, it did not use TCP/IP, it used NCP.

**DNS:** DNS stands for "Domain Name System". It's interesting that, for an article claiming Ethernet was more defining to the internet than TCP/IP, the article makes no mention of DNS, the third essential component to the modern internet. Though you type in "[google.com](http://google.com/)" to get to Google, Google's website actually lives at an Internet Protocol (IP) address of [173.194.34.165](tel:173.194.34.165) (at the time of this writing). This IP address is similar to a human street address. People cannot be expected to remember an IP addresses for their favorite websites, so DNS was invented to resolve a host name ([google.com](http://google.com/)) to an IP address. This is similar to me saying "Ben and Jerry's on Navy Pier" instead of "Ben & Jerry's - NAVY PIER, 700 East Grand Ave., Chicago, IL 60611-3436".

**RFC:** RFC stands for "Request for Comment". The article does not mention these, but they are crucial to understand when things were adopted. They're sort of like the Congressional bills of the technology world. RFC documents are official definitions of technological protocols or interfaces. When something is adopted as a standard, a RFC fully defining it is written, and, if other people want to interface with it, they use that "law" to know how things work. The very first RFC, RFC 1, was called "Host Software" and dictated the infrastructure of ARPANet. RFC 791 was for TCP/IP in 1981. RFC 894 was for Ethernet in 1984. RFC 1035 was for DNS in 1987. These dates do not necessarily correspond to when the interfaces were created, but they do indicate when the interfaces were standardized and/or adopted.

**World Wide Web:** The World Wide Web was formally introduced in 1989. The World Wide Web is, in very loose terms, the combination of HTTP, HTML, and database communication that transfers web content by a standardized means to a web browser.

# Difference Between Intranet and Internet

So, what is the difference between the an "intranet" and the "internet". First of all, the foundational structures of the "internet" are identical to the "intranet" (that being TCP/IP referenced in the article). Once there was the possibility for the intranet, the possibility for the internet also existed, but it was not realized until a bit later, which is why Xerox is trying to claim credit for that. It's a chicken-or-the-egg argument. Naturally, each company (and the Pentagon) claim different loose definitions of all these terms so that they can claim credit for actually inventing the end result. The fact is, none and all of them invented it ... which coincides with Obama's remarks pretty well, if you ask me.

# TCP/IP and Ethernet

First of all, it's sad that the article references Vinton Cerf but makes no mention of Bob Kahn. They collaborated together to define TCP/IP, but Kahn rarely gets the credit he deserves. Kahn was actually the one with the idea of TCP/IP, and Cerf was in charge of the implementation and later the RFC definition.

Secondly, it should be highly suspect that much of the WSJ author's claims come from a book written about Xerox. More significantly, after the WSJ article was published, the author of the cited book released a statement refuting the article and saying the article misrepresented the content of his book.

Naturally, Xerox will claim "full credit" for a discovery, as many other companies have done as well, but given they utilized standards that had already been put in place by others before them (namely TCP/IP), this is disingenuous at best. However, their contribution to the internet's development was equally strong. Ethernet was merely a communication standard that allowed passing data (at very high speeds) between two computers using TCP/IP. Neither technology would ever have been adopted by the private sector (and ultimately the world) without something like ...

# DNS

The Domain Name System was invented in 1983, and the internet would not exist without it, just like TCP/IP and Ethernet. It was created when issues were seen in how hosts were resolved with ARPANet. It was obvious that as ARPANet got larger, the way hosts were resolved (me asking, "Hey, what's Mom and Dad's address?) would become weaker and weaker (and certainly slower and slower). So they decentralized their host resolution to several Domain Name Systems rather than a centralized location at the Pentagon. This was essentially the birth of the privatized internet as we know it, but that is not to discredit its foundations.

# So Did Xerox Invent the Internet or Not?

Short answer? No. Xerox has never been one of the discussion points in the "who invented the internet" within knowledgeable circles.

Long answer? It's a bit arrogant for Xerox (or any one company or government organization) to accept or take full or even majority credit for the invention of the modern day internet. It was a combined effort of multiple unrelated parties, companies, and government entities. People usually credit the Department of Defense with the creation of the internet because, well, they created the first internet. And without the funding and research for TCP/IP, the advancement toward what we have today would have been much slower. Additionally, though Xerox coupled TCP/IP with their own technology to make Ethernet, they did not use Ethernet on the internet. They used it on their own intranet, or internal network, because at the time only government organizations had access to the internet. More importantly, TCP/IP and other internet protocols could exist outside of an internal network, which is where Ethernet is used. Ethernet is used to join computers to an intranet, not to join networks to the intranet. Xerox's contribution certainly increased the speed and reliability of internal network communication, but that is an indirect contribution to the internet. It is not an essential part of the components that makeup the internet.

# What About the Privatization of the Internet?

The reason the internet became privatized had little to do with little government/big government politics, as the WSJ implies, and everything to do with decentralization. The fundamental structure and combination of TCP/IP and network-to-network communications led to DNS, and once DNS was introduced it became obvious that the internet was going to become a worldwide tool that could not be contained or centralized by any one government or entity. However, the U.S. government did still control all the DNS servers, and government organizations were the only ones with access to the internet.

Though Xerox enabled reliable intranet communications with Ethernet (which, by the way, was given back to the government for their use primarily), ARPANet expanded to become the internet, and DNS offered the potential to use the service around the globe, it was not commercialized. It was not until 1992 when Congress passed a bill (spearheaded by Al Gore, which is usually why people misquote him to make the joke in which he claims to invent the internet) that allowed commercial access to the internet. This began the privatization of the internet, but the government still controlled all DNS servers.

For six more years the internet was essentially still controlled by the U.S. government, but commercial entities were allowed to use it. In 1998 (not sure what event the article is referring to when it says 1995), the Clinton administration issued a mandate to form a non-profit organization called the International Corporation of Assigned Names and Numbers (ICANN). The U.S. government gave control of all DNS servers, maintenance, and documentation of internet infrastructure to ICANN. And you thought Google owned the internet. At that point, the internet became officially and completely privatized.

# Doesn't Britain Claim They Invented the Internet?

Actually, no. If you watched the Olympics 2012 Opening Ceremonies, Tim Berners-Lee was paraded through the stadium and loudly proclaimed as the "inventor of the World Wide Web". And there's the distinction. London never claimed he invented the "internet". There is a difference. The "internet" and the "World Wide Web" are two distinct things, though they obviously operate together and are essentially synonymous to the average internet user today.

In 1989, Tim Berners-Lee had an idea for a database of hypertext links. Berners-Lee implemented what he called the World Wide Web with the collaborative help of Robert Cailliau. It didn't take long for the two of them to realize the potential the World Wide Web could offer to the internet, so in late 1990 Berners-Lee developed the protocol necessary to transmit World Wide Web data across the internet: HyperText Transfer Protocol (HTTP) and HyperText Markup Language (HTML). Along with this, he developed the first web browser, which he called simply the WorldWideWeb. Joining HTTP, HTML, and a browser with the internet gave Berners-Lee the ability to pass much more valuable data from point to point, displaying that data in a specifically intended way to the end-user.

In regards to the WSJ article, it's also possible that the author of the WSJ was confusing the term "internet" with "World Wide Web". By 1994, better graphical browsers had been created, and the World Wide Web standard had pretty well been adopted, but primarily only by universities and research labs. In late 1994, Berners-Lee founded the World Wide Web Consortium (W3C), which maintains many of the standards for the World Wide Web still today. After W3C was founded, and in early 1995, the potential the World Wide Web coupled with the internet had to offer the commercial world became apparent, and the internet really started taking off.

## Conclusion

Even still, the Department of Defense, Vinton Cerf, and Bob Kahn do deserve full credit for the creation of the first intranet/network and the initial ideas for networking protocols. The natural successor to that was Ethernet, DNS, and ultimately a privatized and distributed internet as we know it today.

Here's a more simple example to help with the comparison. Assume for a moment that, prior to Henry Ford, nobody had ever done anything with a vehicle that moved (without assistance from an outside force) from point A to point B. Ford created the Quadricycle as his first vehicle. He then adapted that into the Model T. Is the Model T any more or less of a vehicle? It has more of the parts that we're used to today, and it was certainly much more luxurious. But to say then that, because the Model T is more like what we have today, the Quadricycle was _not_ a vehicle is silly. The Quadricycle was still a vehicle that moved you from point A to point B. The Model T was the natural successor to that, and cars have progressively become more and more advanced (with newly invented technology added to them) as society has advanced.

In the same way, ARPANet moved network information from point A to point B. The internet was the natural successor to an intranet, but the same ideas and fundamental technology were used for it, so it is safe to say that the government formed what has become the internet. Which, I believe, was President Obama's point. No argument here that the internet boomed came in 1998 when it was fully privatized, but the internet also would not have been established in the first place without government research and funding.
