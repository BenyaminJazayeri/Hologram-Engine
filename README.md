# Hologram-Engine
3D Graphics Engine with Real-Life Spatial Display Using 2D Screens and Eye Tracking

## Introduction
Hologram-Engine is a software project that transforms a standard monitor and webcam into a dynamic spatial display. Conceived and developed by me between the ages of 14 and 17 (2016-2019).

I believe the journey of the idea is an interesting attempt at hammering away at sci-fi to bring it to reality and thus it's concisely documented below.

It made me learn matrice multiplication, dot products, trigonemtry, calculating point-plane interception early because they were required for writing a 3D engine from scratch.

I do not remember the versions of the dependencies except that it was in python 2; it does not follow coding best practices and versioning is done by copying a file with different names.

The project was uploaded almost exactly how it was backed up, evident by an unrealted file called "hackinsta.py" in there.

## The Journey

### Inspiration
This project was inspired by the movie Iron Man, there are several scenes where spatial displays or "Holograms" are used by the main character. But this scene where he uses it on his design table stood out.

It's showcased in the video below.

[![Video of Iron Man's holographic table](https://github.com/user-attachments/assets/3270e99a-cd14-476b-a7ef-704216e169b8)](https://youtu.be/DZaAFADoF1M)

### First Attempt
First few searches lead to this cool trick that was popular at the time. You'd take a reflective, transparent material, cut it into a pyramid shape, place it upside down on a display and the reflection would seem like a spatial picture. It's called "Pepper's Ghost" and it's how Tupac's famous hologram was created. I believe it's currently used for some effects at Disney themeparks.

The problem with this method is that it support's exactly 4 angles and the transition between viewing angles is not continuous. Other problems include glare, extra needed hardware, etc..

It's showcased in the video below.

[![Video of Hologram Pyramid](https://github.com/user-attachments/assets/e93e82f3-65e0-4179-bd35-bbb7c5b64bf6)](https://youtu.be/7YWTtCsvgvg)

### Second Attempt
About a year and a half and a lot of googling later I stumbled upon this amazing and inspiring video that uses something called an "Anamorphic Illusion". It's displaying images at shifted perspective in a way that seems extremely realistic. It's used in street paintings. The author of this video did it with printed paper.

The problem with this method although being very impressive, is that it supports exactly 1 angle.

It's showcased in the video below.

[![Video of Anamorphic Illusion](https://github.com/user-attachments/assets/430d0c94-e6c4-4e15-bf1d-061871e1fbb8)](https://youtu.be/tBNHPk-Lnkk)

### Second Attempt - Code

At first, the code tried to post-transform a rendered image using 2D transformations, replicating Photoshop templates that were available to recreate this illusion at the time.
Upon further inspection, I noticed that it's much more streamlined if you render the image in a different way, specifically, placing the camera viewport at your table in the 3D scene, instead of at the eye of the viewer and rerendering upon viewer's change of position.

### Second Attempt - With The Help of Blender

A lot of the code for this project is basic 3D engine polygon rendering, as this is something already perfected, I turned to blender 3D engine to use the code there with the added innovation of anamorphic illusions. It could be done manually but automation was unsuccessful at the time. Here are the results.

![photo_2024-07-29_16-55-00](https://github.com/user-attachments/assets/e97023bd-58d2-4287-9d2b-6084ba73709d)

![photo_2024-07-29_16-55-01](https://github.com/user-attachments/assets/770d9992-e573-48d2-b460-48f5ae06b9f6)

### running the code

The main files are "ukno - tabletop.py" and "ukno - straight.py". The first file is used when you place your screen flat on the table and the second when you place it noramlly.

### Continuation

I had to stop obsessing over the project after 4 years. But I strongly believe that with the right business viablity this could be a great product.

There are 2 main areas that the project could improve.

1-A robust rewriting of the code

2-Finding a way to support both eyes of the viewer, currently the project supports only 1 viewing angle. Ideas for this include:

  A) Displaying a different image for each eye at alternating frame rates in a way that makes it easy for the brain to combine them in the right format.
  B) Special hardware.

### Attempts by other people and demonstration

This exact idea was discovered by a company called Hololamp. They used it for entertainment at restaurants. I do not know how they continued and I'm not sure about the dates, but The idea journey documented here was uninfluenced by their respective efforts.

A video of their product is included below. It's how this code is supposed to work.

[![Watch the video](https://img.youtube.com/vi/LQY5AvRwCN8/maxresdefault.jpg)](https://youtu.be/LQY5AvRwCN8)

I remember another gentleman demonstrating it using an Xbox Kinect with the 3D model of a human face but I cannot seem to find his video. If you know this video, please email me at benyamin.jazayeri@yahoo.com so I can include it.

### Final Word

This project stands near and dear to my heart, if you are interested in discussion or continuation of this project, please contact me at benyamin.jazayeri@yahoo.com


