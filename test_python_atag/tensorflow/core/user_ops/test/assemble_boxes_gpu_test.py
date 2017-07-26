import tensorflow as tf

class AssembleBoxesTest(tf.test.TestCase):
  def testAssembleBoxes(self):
    assemble_module = tf.load_op_library('./../assemble_boxes_gpu.so')
    with self.test_session():
      test = [1,1,3,3,1,15]
      test.extend([6,1])
      #test = tf.constant(test, dtype=tf.uint16)
      test = tf.cast(test, dtype=tf.int32)
      print test
      result = assemble_module.assemble_boxes_op(test)
      print(result.eval())
      #self.assertAllEqual(result.eval(), test)

if __name__ == "__main__":
  tf.test.main()
