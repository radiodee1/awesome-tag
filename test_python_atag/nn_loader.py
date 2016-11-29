import numpy as np

class Load(object):
    def __init__(self, atag):
        self.csv_filename = ""
        self.mnist_train = {}
        self.mnist_test = {}

    def get_mnist_dat(self):
        train = [0] * 784
        test = [0] * 784
        labels = [0] * 10

        test = [test]
        #np.reshape(test, (-1,784))
        labels = [labels]
        #np.reshape(labels, (-1, 10))

        self.mnist_train = Map({'images':train, 'labels': train})
        self.mnist_test = Map({'images':test, 'labels': labels})
        #self.mnist_test = test
        print self.mnist_test
        return self.mnist_train, self.mnist_test

class Map(dict):

    def __init__(self, *args, **kwargs):
        super(Map, self).__init__(*args, **kwargs)
        for arg in args:
            if isinstance(arg, dict):
                for k, v in arg.iteritems():
                    self[k] = v

        if kwargs:
            for k, v in kwargs.iteritems():
                self[k] = v

    def __getattr__(self, attr):
        return self.get(attr)

    def __setattr__(self, key, value):
        self.__setitem__(key, value)

    def __setitem__(self, key, value):
        super(Map, self).__setitem__(key, value)
        self.__dict__.update({key: value})

    def __delattr__(self, item):
        self.__delitem__(item)

    def __delitem__(self, key):
        super(Map, self).__delitem__(key)
        del self.__dict__[key]