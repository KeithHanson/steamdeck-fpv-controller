# Steamdeck FPV Controller

This is an open source and open hardware project that allows you to control a remote drone and receive FPV video from cheap, simple components. 

## Current Status

Brand New - I have prototype code running on an MCU and a Steamdeck. No radio comms yet, no video yet. Video TX and RX Parts are shipping.

## Updates

June 1st 2024: You are reading the first commit for this repository. Parts are shipping, and prototype code on the steamdeck has been written.

## Goals

Primarily, we want to transmit joystick signals to a remote receiver/drone/robot from a steamdeck.

Secondarily, we want to receive a video feed from the remote drone.

A stretch goal of mine will be able to provide an entire kit for purchase, ready for wiring and assembly.

## Basic Criteria

1. 3D Printed Frame - I have a printer, and love the idea of an arm being replaced in a couple hours.
1. Off the shelf components - I will break this. A lot. I want cheap/fast ways to repair (Amazon parts, DIY). 
1. As much as possible, tap into already provided hardware/software - IE: esp-fc, ESCs, MMUs, etc. 
1. Provide everything in a portable, simple to understand way (pygame, micropython) - *ideally* we don't need devmode or having to unlock the drive.

## Research

### Overview

The steamdeck is a computer. It runs Arch, a flavor of linux that I daily drive. 

From basic tests, one can setup a pyenv, install pygame, and run pygame all without needing devmode or write access to the drive. 

With some code, this gives us access to the joystick and buttons. 

To provide the steamdeck the capability to radio transmit those joystick and button signals over long distance, we will use LoRa, which can transmit up to nearly 1KM.  

To control a LoRa module, we'll talk to a microcontroller (ESP32) that powers the LoRa transmitter via serial over usb (/dev/ttyUSB0). 

The basic control will look something like:

pygame (steamdeck controls) <-> USB Serial <-> ESP32 <-> LoRa <-> Radio Signals <-> ESP32 <-> Flight Controller <-> ESC <-> Drone Motors
pygame (steamdeck video) <-> OTG 5.8GHz Webcam Stream via USB <-> 5.8GHz VTX <-> Drone Camera

### Video

Inspired by this comment: https://www.reddit.com/r/Steam/comments/omf8xf/comment/l3ffasi/

I've never done any drone stuff, so this was what sparked my interest. These things are cheap, $30-40 receivers. 

The VTX is also cheap, and depending on your desired camera quality, the camera is cheap. 

All in, I am spending (with Amazon premiums applied - you can of course get this cheaper elsewhere) about $80 to begin testing video transmission to the Steamdeck from a remote drone camera.

### Joysticks

The steamdeck has a LOT of capability for all kinds of customized ways to handle input.

It feels like it could be the perfect companion to amateur drone flying.

Right now, I am using the default controller detected by pygame, but further experimentation should help us figure out how to tap into the Steamdeck's configurations.

### Joystick Signal Transceiver

ChatGPT and I had a long talk around which was the best module to use. https://chatgpt.com/share/0b7a110e-f3e7-45c4-b29e-e4f8c12da1b3

In there, I proposed the worst case scenario I could think of - very noisy, downtown environment with lots of objects in the way of transmissions.

Ultimately, I settled on settings that were corroborated via other commenters on Reddit, and also noticed there were commercial products using the settings provided.

Roughly, we will use LoRa via the FSK mode, with a Spread Factor of 7 and as high a bandwidth and power as our chip will allow. 

The chip I ended up settling on was the SX1262. These are widely available, well supported, and plenty of devkits for it. 

More importantly, it is well supported in micropython and achieves all of the characteristics we need (sub 50ms latency from control to drone).

#### Transmission

One SX1262 will be responsible for transmitting to the drone. 

I'll do this via a fairly dumb "pass through" program running on the ESP32 that listens for serial input and pushes it over Lora.

#### Receiver

The other SX1262 will be on the drone, and needs to be able to talk to the FC. 

Further research is needed on exactly how to make that happen :) 

## Current BOM

I'll be trying to use an ESP32 for the FC for initial experiments (so you won't see it in this list).

See: https://github.com/rtlopez/esp-fc

I'm adding my Amazon list for convenience for now. Once I've tested enough I'll solidify everything into the repo here.

I have never hooked up any commission anything, so I don't think that is present here, but if it is, it is unintended:

https://www.amazon.com/hz/wishlist/ls/B53DGAOXK9V6

For now, I am prototyping with a Heltec V3 LoRa board since it is so simple to interface with and test basic TX/RX.

## Flashing

TBD (micropython)

## Wiring

TBD

## Assembly

TBD, see:
https://makerworld.com/en/models/236234#profileId-269467

## Configuration

TBD (Betaflight)

## End to End Testing

TBD

## First Flight

TBD

## Customizations

TBD
