---
title: "Hearth - a room thermostat for Daikin & Home Assistant"
date: 2026-10-13
slug: "hearth-room-thermostat-for-daikin-home-assistant"
aliases:
  - /2026/10/hearth-room-thermostat-for-daikin-amana-goodman/
tags: 
  - "daikin"
  - "hearth"
  - "home-assistant"
  - "mobile-app"
  - "programming"
  - "smart-home"
  - "thermostat"
---

<p align="center"><img alt="Hearth - Room thermostat for Daikin, Amana, and Goodman" src="https://www.meethearth.app/icon-512.png" width="200" /></p>

For years, we had a Nest and loved it. Then we put in a new HVAC system from Amana. And, the system itself ... it's
amazing and we love _it_ too ... the catch is, the system vendor locks you into using their own app for the thermostat.
The Skyport app. And, well, put bluntly ... it sucks. Not just as a thermostat app, but it lacks the ability to add
additional sensors and set up room following, among many other things.

That frustrated me for a long time. Then Daikin bought Amana, and at some point in that transition, their proprietary
thermostat on the wall finally started exposing its API. And that's all I needed! So, eager to ditch their thermostat
app, I wrote my own! I hooked it up to the Ambient Weather sensors I already had around the house, taught it to follow
the rooms we actually live in, and decided it was worth releasing for everyone else stuck in the same spot.

That app is Hearth, and it works with Daikin, Amana, and Goodman smart thermostats ... and just about any other
thermostat you've got in Home Assistant, too. And you can check it out at **[meethearth.app](https://meethearth.app/)**!

## The Rooms You Actually Live In

Here's what bugged me most. A thermostat on the wall only knows how warm it is right where it's mounted, and that's
rarely where any of us actually are. What I wanted was simple: cool bedrooms at night, a comfy living room
during the day, and a cozy basement at night when we're watching a movie, with nobody needing to get up to mess with
the thermostat or app at any point.

That's what Hearth does for us now. It watches the rooms that matter at the moment and nudges the thermostat until
they're right. Honestly, it's the part I'd have the hardest time giving up.

## Bring Your Own Sensors

I started with the Ambient Weather sensors I already had, but I didn't want Hearth to only work for folks who happen to
own the same gear I do. So it also works with Govee's Wi-Fi thermometers, which are cheap and easy if you're starting
from scratch. And if you're the tinkering type and already run Home Assistant, Hearth has an integration for it,
so pretty much any temperature sensor Home Assistant can see (Zigbee, Z-Wave, Bluetooth, your ESPHome boards) can be
a room in Hearth. Your own scripts can send their readings in, too. The
[sensor guides](https://www.meethearth.app/support#sensors) on the Hearth site have all the details.

## Home Assistant FTW

That integration doesn't stop at sensors. If your thermostat is one Hearth can't talk to directly, but Home Assistant
can, Hearth can run it through Home Assistant, room following and all. It's the same app on your phone either way;
Home Assistant just does the talking to the thermostat. If that sounds like your setup, the
[Home Assistant guide](https://www.meethearth.app/sensors/home-assistant) walks through it, and the integration itself
is open source as [ha-hearth](https://github.com/alexdlaird/ha-hearth).

## Around the Campfire

A bit of a confession. The name, and the whole look of the app, is an homage to one of my favorite video games of
all time. If you've played it, you'll probably catch it right away: a small forest planet at night, pine green
throughout, campfire orange for heating, geyser blue for cooling, and a tiny planet and its moon orbiting while things
load.

Switch to dark mode and there's a quiet night sky behind every page. Keep an eye on it long enough ... say, twenty or so
minutes ... and you just might see something. If it rings a bell, welcome home, fellow Hearthian. And if it doesn't,
no matter, none of the easter eggs in the app are otherwise intrusive, so it still adds to a generally warm and fresh
look-and-feel for the app.

## Early Access

Hearth is out now on the [App Store](https://apps.apple.com/app/id6816728401) and
[Google Play](https://play.google.com/store/apps/details?id=com.alexdlaird.hearth). If you set up now, it's free for
life. Homes that join later will pay a small yearly fee to cover running costs.

Spread the word! Head to [meethearth.app](https://meethearth.app/) to get started, and if you have questions or
feedback, let me know at [contact@meethearth.app](mailto:contact@meethearth.app).
