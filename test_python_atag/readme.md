# awesome-tag
Facial detection and tagging experiments -- this project was not working for several months. Presently, though, it does a better job of detection than it did. It does not, however, do that detection any faster than before. It presently takes several minutes for each image.

The method used for detection can be described as follows. All the code is written in python. First a program devides the image into small boxes, 7 pixels to a side. Then a simple two layer neural network is used to determine which of these boxes are areas of the image where a face might be. This layer basically detects skin tones. Then an aggregating program is used to draw together squares that are immediately adjacent. Then a more sophisticated convolutional neural network is used to determine which of these resulting boxes is actually a face.

Tensorflow is used to implement the neural networks on the author's computer using the gpu on that computer. Because Tensorflow is used there was a conflict in importing in python the TF library and the Gtk library at the same time. To get around this a separate program was created for the TF functions that is called by the gui using the 'subprocess' functionality.

When the experment was tried for the first time Java was used. This worked poorly and good results were never fully realized. The java code is included in the github repository for completeness. Also included in the repository is some python code that uses tensorflow to work on the MNIST dataset, just as is suggested by the Tensorflow 'getting started' page.

