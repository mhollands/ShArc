# ShArc

I recreated the work from [this paper!](https://dl.acm.org/doi/10.1145/3313831.3376269)

I use an AD7446 to sense mutual capacitance between TX and RX electrodes of 4 pixels on a pair of flexes. This capacitance varies approximately linearly with the curvature of the two flexes. An STM32 microcontroller bridges the gap between the host computer and AD7446 via USB. The design has four parts:

- Sense board which holds the electronics and connects to the host computer via USB
- RX Flex which has 4 receive electrodes
- TX Flex which has 4 transmit electrodes
- Separator which is a dumb piece of polymide material to fit between the RX and TX flexes

Schematics and gerbers can be found for each part and the design was build using OSHPark standard PCBs and Flexes.

[![Watch the video](https://img.youtube.com/vi/9scRBK16ceY/maxresdefault.jpg)](https://youtu.be/9scRBK16ceY)
