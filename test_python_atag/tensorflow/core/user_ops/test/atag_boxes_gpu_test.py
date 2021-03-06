#!/usr/bin/python

import tensorflow as tf
import atag_csv_draw_mod as draw

class AssembleBoxesTest(object):
  def __init__(self):

    self.d = draw.Read()
    self.d.process_read_file_predict_list()
    self.r = []

  def do_test(self):
    test = []
    test = self.d.gpu_test
    assemble_module = tf.load_op_library('./../assemble_boxes_gpu.so')
    with tf.Session():
      with tf.device("/gpu:0"):
          if len(test) == 0:
              test = [1,1,3,3,1,15]
              test.extend([4,1,3,3,2,15])
              test.extend([7,1,3,3,3,15])
              test.extend([1,4,3,3,4,15])
              test.extend([4,4,3,3,5,15])
              test.extend([7,4,3,3,6,15])
              test.extend([1,7,3,3,7,15])
              test.extend([4,7,3,3,8,15])
              test.extend([7,7,3,3,9,15])
              test.extend([6,9, 16])
          test = tf.constant(test, dtype=tf.uint16)
          #test = tf.cast(test, dtype=tf.int32)
      print test
      #result = assemble_module.assemble_boxes_op(test)
      result = assemble_module.assemble_boxes_cpu(test)
      self.r = result.eval()
      s = []
      for i in range(len(self.r) // 6):
          print(self.r[ i * 6: i * 6 + 6])
          g = self.r[i * 6 + 4]
          if not g in s:
              s.append(g)
      print "simple list:" , s

  def do_show(self):
      self.d.process_show_gpu_output(self.r)
      pass

if __name__ == "__main__":
    a = AssembleBoxesTest()
    a.do_test()
    a.do_show()
