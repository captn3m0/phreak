PHreak
======
PHreak is a simple linux app that sits in your system tray and shows you current top stories from Product Hunt.

![Screenshot](http://i.imgur.com/33AGurt.png)

PHreak was made for the Product Hunt Hackathon and uses the official Product Hunt API.

###Requirements:

- appindicator (install `python-appindicator`)
- pip
- python 2.7

###Installation

PHreak is installed as a simple Python package:

    (sudo) pip install phreak

Then, you invoke it via the `phreak` command.

###Disclaimer

PHreak was made for a hackathon. As such, there are no promises that it will work on your system. It was tested on the following setups:

1. Ubuntu 14.04 + Cinnamon
2. Debian wheezy (7.6) + KDE (with `python-appindicator` installed)
3. Ubuntu 14.04 + Unity

Your mileage may vary.
