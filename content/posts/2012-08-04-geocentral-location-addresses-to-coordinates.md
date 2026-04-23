---
title: "Geocentral Location; Addresses to Coordinates"
date: 2012-08-04
tags: 
  - "google"
  - "internet"
  - "programming"
---

Recently, I needed to plot numerous addresses on a map and, ultimately, find the geocentral location of all addresses. The geocentral location is the weighted center of all the addresses, which can be useful in helping determine numerous things, including the average distance between all addresses and some other location.

The geocentral location is attained through relatively simple vector math. Let's say, for instance, you have a set of points on a graph. Adding each point together would give you the weighted center of all the points, which can help you determine quite a bit about how that population of points interacts with you or each other.

I've put together a simple script below that interacts with Google Maps to do just that. Input a list of addresses in the text box below, attain the coordinates for each address, and plot each address, and the address' geocentral location, on the map below.

 

**A few things to keep in mind:**

- One address per line
- Addresses must be properly formatted
- Ensure no address lines are blank
- The geocentral location is marked with a blue flag
- In order to keep strain on my server low, the tool below only allows 150 or less addresses to be processed. The source is available [on GitHub here](https://github.com/alexdlaird/geocentral-location), so you're welcome to modify the tool for use on your own server.

