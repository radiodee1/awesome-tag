# Awesome Tag

This is a java application for detecting faces in pictures using convolutional neural networks. It should be noted that the app doesn't work. 

### SOURCES

The sources for the images was the NIST IJB-A dataset. The NIST pictures are part of a contest, but are free to download if you register with them. There are thousands of pictures, and several csv files with label data. In each picture faces are identified and this data can be used to train your program.

The software libraries used in the program are from a company called Skymind. They are nd4j, deeplearning4j, and Canova. I used the distributions 0.4-rc3.8 release extensively. My CNN model was ultimately constructed with 4 layers. The first layer was a convolutional layer. The second was a pooling layer. The third was a 'DenseLayer' and the last was a output or 'softmax' layer. I am not entirely sure that the DenseLayer supported the kind of learning I was looking for, so I experemented with other layer configurations. In the end the DenseLayer performed best so I kept it.

I used the linux operating system, java 8, and the IntelliJ IDE. Training for weights and biases for the neural network have to be re-learned every time the project is installed. This is because they are too big to save with the code. There are no weight and bias files online for this project.

### SETUP

You have to get a copy of the NIST IJB-A dataset. This is a 14G download. You also need to unpack the tar g-zip file, so you need something like 28G free. Then make sure InteliJ-IDE is installed. Download the 'awesome-tag' java repository from github.com and open the project using the IDE. You should launch the GUI launcher, the file called ATAGShowImage.java. You can also try launching the `launch_rc38_cpu.sh` file. You may be able to launch the file this way without the IDE.

When opening the GUI for the first time you have to set the values for the program's operation. For example, you need to tell it where to find the IJB-A images and csv files. When this is done you can select a picture to view. The picture will probably be in the csv database, and the csv database is loaded automatically when the GUI is started, so if you want to you can click the 'Add Lines' button and see the boxes that identify the faces in the picture. This is the basic information that is provided by the IJB-A dataset.

At this stage you also identify what 'split' you want to start with and what 'split' you want to end with. Because there are so many images it is sufficient to choose 'split' 1 to start and also 'split' 1 to end. Setting these initial values creates a file in the user's home folder called `.atag`. This folder holds all the info that the GUI uses in its regular operation.

The next step is to build your own csv file. This file would contain the boxes mentioned above and also empty boxes without faces in them. These empty boxes are used by the program to train the cnn. For every box with a face there is another box with no face of the same size. You create this second csv file by clicking the 'Mod And Save' button. This process can take an hour or more just for one 'split'. If you have chosen different splits for start and finish the program will try to cycle through the set you have chosen and will process all of them. There are ten splits in the IJB-A dataset, and trying to process all ten could take a long time.

After setting up your csv file you can start training. Click the 'Reset Cursor' button to make sure that your input data cursor is starting with a zero value. Bye the way, yuo can also choose to erase all weights and biases when you click the 'Reset Cursor' button. Click the 'Train CNN' button once. This will start training. Training is very time consuming, so a mechanism is provided for saving your weights and biases, so that you can stop training and restart the process where you left off. 

Loading and saving the neural network takes from five to ten minutes. When you click the 'Train CNN' button once the program will attempt to load the model. Then it will automatically start the training process. If you click the button again the neural network will stop training and will start the save process. You will see a dialog box on screen with a cycling progress bar until the save process has stopped. Again, this takes five to ten minutes. After it has stopped you can close the app or move on to testing or prediction. It takes several hours of training to get any results at all. The idea here is to let you do that training in smaller segments. You can force the program to stop during the save operation, but you are likely to corrupt your weight and bias files and thereby loose any learning that you have completed up to that point.

Clicking the 'Test CNN' button will allow you to test the accuracy of you CNN against your own csv file data. Clicking the 'Predict' button will attempt to find faces in the currently selected image. Both these operations take time. Though you may be able to train your network to the level of 75 or 80 percent, the process employed by the 'Predict' mechanism does not identify images properly. This is the reason that the project will not be developed further.

### PREDICTION

The current 'Prediction' scheme is a two stage operation. First you click the "Prediction" button and choose the "EVEN" option from the two options presented. Then you wait for the first stage, the "EVEN" stage to complete. When it's done you see the image on the screen with some superimposed boxes on it. This is stage 1. Then click the "Prediction" button again and choose the "IMPROVE" option. Again you must wait a long time. After this is done you see the final result on the screen.

The "EVEN" operation devides the picture into evenly spaced boxes and runs them through the neural network. When this is done you get separate "areas of interest". These areas of interest are the boxes you see superimposed on the screen after the first "Prediction" phase.

The "IMPROVE" operation takes the areas of interest and searches for a box size that most clearly looks like a face. It takes each area-of-interest box seperately and in that location tries out eight boxes of different sizes to see which produces the best score.
