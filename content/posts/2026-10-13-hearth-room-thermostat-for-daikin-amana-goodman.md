---
title: "Hearth - a room thermostat for Daikin, Amana, and Goodman"
date: 2026-10-13
slug: "hearth-room-thermostat-for-daikin-amana-goodman"
tags: 
  - "daikin"
  - "hearth"
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

That app is Hearth, and it works with Daikin, Amana, and Goodman smart thermostats. **Get started at
[meethearth.app](https://meethearth.app/)**.

## What Hearth Does Today

The first release is all about the thermostat, doing the basics that Skyport should have been doing all along.

You get presets (Home, Away, Sleep, or your own) that switch on a weekly schedule, and holds for when plans change. If
someone bumps the thermostat on the wall, you decide whether that change sticks or Hearth goes back to its plan.

Hearth also keeps a history. There are charts of temperatures, setpoints, and when the system was heating or cooling,
plus a timeline of every change and who made it, whether that was Hearth, its schedule, or someone outside the app. It
will also alert you when heating or cooling falls behind or the thermostat goes offline.

> **Note:** With Hearth Autopilot on, Hearth runs your schedule itself, so it turns off the thermostat's own schedule.
> Switch Autopilot off any time and the app just mirrors your thermostat.

## Room Sensors Are Rolling Out

Room sensors are the reason I built Hearth in the first place, and they're already running in our home. I'm rolling
them out slowly. Soon you'll be able to bring your own Ambient Weather sensors, like I do, and I'm adding SensorPush
support too.

Once a room has a sensor, Hearth adjusts the thermostat until the room you're following hits its target. You can follow
one room, the average of your rooms, or whichever room is furthest from its target, and each preset picks its own, so
Hearth can follow the bedrooms at night and the living room by day. If a sensor goes quiet, Hearth falls back to the
thermostat.

## Early Access

Hearth is invite-only while I test it with a small group of homes. If you set up now, it's free for life. Homes that
join later will pay a small yearly fee to cover running costs. On Android, early access goes through a testing group:
ask to join, and once you're approved, I'll send you the link to install.

Spread the word! Head to [meethearth.app](https://meethearth.app/) to get started, and if you have questions or
feedback, write to [contact@meethearth.app](mailto:contact@meethearth.app).
