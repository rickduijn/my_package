#import roslib
#roslib.load_manifest('converter_depth_image')
import sys
import rospy
import cv2
import numpy as np
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

class image_converter:

    def __init__(self):
      self.image_pub = rospy.Publisher("image_topic_3",Image)

      self.bridge = CvBridge()
      self.image_sub = rospy.Subscriber("camera/depth/image_rect_raw",Image,self.callback)

    def callback(self,data):

      try:
        data.encoding='mono16'
        cv_image = self.bridge.imgmsg_to_cv2(data, "mono16")
      except CvBridgeError as e:
        print(e)

      img_n = cv2.normalize(src=cv_image, dst=None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)
      im_color = cv2.cvtColor(img_n, cv2.COLOR_GRAY2BGR)


      try:
        self.image_pub.publish(self.bridge.cv2_to_imgmsg(im_color, "bgr8"))
      except CvBridgeError as e:
        print(e)

def main(args):
    rospy.init_node('image_converter', anonymous=True)
    ic = image_converter()

    try:
      rospy.spin()
    except KeyboardInterrupt:
      print("Shutting down")

if __name__ == '__main__':
      main(sys.argv)