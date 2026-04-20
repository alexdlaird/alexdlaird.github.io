---
title: "Java: OS X Dock Icon and Name"
date: 2011-02-07
tags: 
  - "apple"
  - "instructional"
  - "programming"
---

For as long as I've been developing in Java, its lack of native support for OS X has always bothered me. This is more than likely an issue with Apple's proprietary interface rather than Java, but, for the sake of being loyal to my Master, we'll pretend the fault is on Java.

I don't want the default Java icon--I want my applications icon to appear in the dock! And why does setTitle not actually change the name of my program in the menu bar? It still remains the name of the Java package that the main () method is contained within. I don't want people to know the package layout of my software.

Of course, Apple's "solution" to this is contained within Xcode ... Just make an .app wrapper for your application! Native dock icon, native dock name. But then that's just the problem--the application now appears to be native and is no longer portable. There has to a better solution ...

Well, there isn't. There's no real _solution_ to this problem, but I can offer you a slight hack that works for the dock icon and name, at least. Unfortunately, it only works for the dock icon, and the actual application icon in Finder will still remain the Java default.

First, we'll look at the snippet of code that allows you to change the dock icon ...

```java
com.apple.eawt.Application macApp = com.apple.eawt.Application.getApplication(); macApp.setDockIconImage (new ImageIcon (getClass (). getResource ("/path/to/package/icon.png")). getImage ());
```

You'll find that there are actually quite a few cool things you can do to the dock from inside the Application class. Unfortunately, none of them are changing the dock name of your Java application. You'll also notice that, while your program now compiles and runs beautifully on OS X, it is broken everywhere else ... Apparently com.apple.eawt is a missing package on anything but OS X. What happened to portability?

Never fear. Apple has been kind enough to give us stubs that can still be called (and ignored) from platforms other than OS X. You'll need to include the stubs JAR in your project for your application to be able to compile and run on other platforms again.

[Download AppleJavaExtensions](http://developer.apple.com/library/mac/#samplecode/AppleJavaExtensions/Introduction/Intro.html "Download the AppleJavaExtensions")

Okay, so what about the OS X dock name then? Sadly, there's no good solution to that. Here's the best work-around that I've found--put your main () in a class by itself in your applications default package. I know, the default package is evil ... That's why the first and only thing you'll do is call JFrame.setVisible () from within this function.

This does mean that, as far as the menu bar is concerned, your application title cannot have any spaces. It will be the exact name of the class your main function is in, so, for instance, Get Organized shows up as GetOrganized. My GetOrganized class immediately launches MainFrame from deeper within the package system, but the average user no longer has to see the package layout.

A lousy work-around? Definitely. But it's all they're giving us. And considering Apple seems to hate Java as of late, I doubt they'll ever give us anything more.
