# awesome-tag
Facial detection and tagging experiments -- this project was not working for several months. Presently, though, it does a better job of detection than it did. It does not, however, do that detection any faster than before. It presently takes several minutes for each image.

The method used for detection can be described as follows. All the code is written in python. First a program devides the image into small boxes, 7 pixels to a side. Then a simple two layer neural network is used to determine which of these boxes are areas of the image where a face might be. This layer basically detects skin tones. Then an aggregating program is used to draw together squares that are immediately adjacent. Then a more sophisticated convolutional neural network is used to determine which of these resulting boxes is actually a face.

Tensorflow is used to implement the neural networks on the author's computer using the gpu on that computer. Because Tensorflow is used there was a conflict in importing in python the TF library and the Gtk library at the same time. To get around this a separate program was created for the TF functions that is called by the gui using the 'subprocess' functionality.

When the experment was tried for the first time Java was used. This worked poorly and good results were never fully realized. The java code is included in the github repository for completeness. Also included in the repository is some python code that uses tensorflow to work on the MNIST dataset, just as is suggested by the Tensorflow 'getting started' page.

The training data that I use came from www.nist.gov . They have a dataset of labled facial images for a facial recognition challenge (note, this is for facial recognition, not really detection). The dataset is called the 'IJB-A' dataset. The download is large and you must apply for permission to access the download page. I beleive most students of computer science would be approved, if you are clear that you are interested in research.

You are required to add the following text to any publication: This product contains or makes use of the following data made available by the Intelligence Advanced Research Projects Activity (IARPA): IARPA Janus Benchmark A (IJB-A) data detailed at http://www.nist.gov/itl/iad/ig/facechallenges.cfm .

The first step to using this project is downloading the dataset. Then the working environment must be set up. The project uses, among other things, a dot-folder in your home directory called '.atag' for storing the location of the IJB-A database as well as the location of several of its own files. Then you must train the two databases on the images in the dataset folders. Then you can go ahead and test the facial detector on the images in the database or any image of your own.

-----

Programming was done in python on a Ubuntu 16.10 linux computer, using the nvidia card, and a sophisticated programming IDE (PyCharm Community Edition). Some of the python libraries used in this project are: python2.7, python-numpy, python-pil, Tensorflow, python-easygui, python-opengl. The link to the Tensorflow website is: https://www.tensorflow.org/ . Instructions on installing Tensorflow can be found there. The link to the PyCharm website is: https://www.jetbrains.com/pycharm/ . At the time of this writing I am using Tensorflow 0.11.0. 
