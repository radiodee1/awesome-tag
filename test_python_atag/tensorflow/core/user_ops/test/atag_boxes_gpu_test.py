#!/usr/bin/python

import tensorflow as tf

class AssembleBoxesTest(tf.test.TestCase):
  def testAssembleBoxes(self):
    assemble_module = tf.load_op_library('./../assemble_boxes_gpu.so')
    with self.test_session():
      with tf.device("/gpu:0"):
      
          test = [1,1,3,3,1,15]
          test.extend([4,1,3,3,2,15])
          test.extend([7,1,3,3,3,15])
          test.extend([1,4,3,3,4,15])
          test.extend([4,4,3,3,5,15])
          test.extend([7,4,3,3,6,15])
          test.extend([1,7,3,3,7,15])
          test.extend([4,7,3,3,8,15])
          test.extend([7,7,3,3,9,15])
          test.extend([6,9])
          test = tf.constant(test, dtype=tf.uint16)
          #test = tf.cast(test, dtype=tf.int32)
      print test
      result = assemble_module.assemble_boxes_op(test)
      r = result.eval()
      for i in range(9):
          print(r[ i * 6: i * 6 + 6])
          
      #print(r)
      #self.assertAllEqual(result.eval(), test)

if __name__ == "__main__":
  tf.test.main()
