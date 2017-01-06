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

-----
### SOURCES

The sources for the images was the NIST IJB-A dataset. The NIST pictures are part of a contest, but are free to download if you register with them. There are thousands of pictures, and several csv files with label data. In each picture faces are identified and this data can be used to train your program.

I used the linux operating system, java 8, and the Pycharm IDE. Training for weights and biases for the neural network have to be re-learned every time the project is installed. This is because they are too big to save with the code. There are no weight and bias files online for this project.

### SETUP

You have to get a copy of the NIST IJB-A dataset. This is a 14G download. You also need to unpack the tar g-zip file, so you need something like 28G free. Then make sure InteliJ-IDE is installed. Download the 'awesome-tag' java repository from github.com and open the project using the IDE. There are actually three projects in the repository. For the purposes of this document you are interested in the `test_python_atag` directory. You should launch the GUI launcher, the file called `launch_menu.sh`. You may be able to launch the file this way without the IDE.

When opening the GUI for the first time you have to set the values for the program's operation. For example, you need to tell it where to find the IJB-A images and csv files. If you correctly identify one of the split csv directories to the program, you can press the 'Read And Write CSV' and generate the files needed for training and testing.

Setting these initial values creates a file in the user's home folder called `.atag`. This folder holds all the info that the GUI uses in its regular operation.

When this is done you can select a picture to view. The picture will probably be in the generated csv file, and the csv file is loaded automatically when the GUI is started, so if you want to you can click the 'Read CSV, Show Boxes' button (and then the 'Train' button) and see the boxes that identify the faces in the picture. This is the basic information that is provided by the IJB-A dataset plus some training info. There is a possibility that the picture you choose doesn't have data associated with it in the loaded training file. If this is the case you either have to choose a different training file (from a different split) or choose a different picture. You will notice a red box around every face and another red box floating around somewhere in the picture. For every boxed face there is one box that is supposed to be empty. 

After setting up your csv file you can start training. Click 'Train', and after that either the 'DOT' or the 'CONVOLUTION' button. This will start training. Training is very time consuming, so a mechanism is provided for saving your weights and biases, so that you can stop training and restart the process where you left off. 

Loading Tensorflow takes a number of seconds. When you click the 'DOT' or 'CONVOLUTION' button the program will attempt to load the model. Then it will automatically start the training process. It will continue for one epoch. For the 'DOT' network one epoch may take several hours. For the 'CONVOLUTION' network one epoch takes less than an hour. 

Clicking the 'More Options' button will allow you to test the accuracy of you CNN against your own csv file data. Clicking the 'Predict' button will attempt to find faces in the currently selected image. Both these operations take time. You may be able to train your 'DOT' network to the level of 69 percent, and the 'CONVOLUTION' network to the level of 83 percent. Both are required for proper operation of the program.

### PREDICTION

The current 'Prediction' scheme is a two stage operation. First you click the 'Predict' button. Then the program launches and loads the neural network models and then saves a file that contains the prediction results. Then you click the 'Read CSV, Show Boxes' button and select the 'PREDICT' option. Results from the prediction operation are superimposed on the currently loaded image.


