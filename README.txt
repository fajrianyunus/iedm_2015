This program is made as a prototype of the concept explained in Hui-Lin Chang's "Algorithm Application for EOT and Gate Stack Control" paper submission to the IEEE International Electron Devices Meeting (IEDM) 2015.

This program basically solves 0-1 Integer Linear Programming problem. 

This program is written in Python 2.7. It relies PuLP (https://pypi.python.org/pypi/PuLP). PuLP itself is pretty much just a programming API. PuLP relies on GLPK (http://www.gnu.org/software/glpk/) to solve the 0-1 Integer Linear Programming problem.

Requirements:

1. Python 2.7
This is the version of Python which I am using. I haven't tried the code in Python 3.

2. PuLP
There are many ways to install PuLP. But the ay which I like the most is by using pip (https://pypi.python.org/pypi/pip). The instruction on how to install PuLP by using pip can be found in https://pypi.python.org/pypi/PuLP

3. GLPK
The installation procedure depends on your OS. I am using Ubuntu 13.10 x86_64, and here is my installation procedure
* Download the file
* Run "./configure"
* Run "sudo make install"



How to use:

Open main.py, there are several variables you will have to edit. The instruction on which variables are to be edited are there as well.


For any enquiry, please send an e-mail to fajrian DOT yunus AT gmail DOT com
