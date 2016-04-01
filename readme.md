# Awesome Tag

This is a java application for detecting faces in pictures using convolutional neural networks. It should be noted that the app doesn't work. 

## SOURCES

The sources for the images was the NIST IJB-A dataset. The NIST pictures are part of a contest, but are free to download if you register with them. There are thousands of pictures, and several csv files with label data. In each picture faces are identified and this data can be used to train your program.

The software libraries used in the program are from a company called Skymind. They are nd4j, deeplearning4j, and Canova. I used the distributions 0.4-rc3.8 release extensively. My CNN model was ultimately constructed with 4 layers. The first layer was a convolutional layer. The second was a pooling layer. The third was a 'DenseLayer' and the last was a output or 'softmax' layer. I am not entirely sure that the DenseLayer supported the kind of learning I was looking for, so I experemented with other layer configurations. In the end the DenseLayer performed best so I kept it.


