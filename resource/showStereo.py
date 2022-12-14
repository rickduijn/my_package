# direct to ros2_ws/src/my_package/resource (the location of this file)
# python3 convert_16UC1_2.py

# use this version for the uncompressed data

# subscribes to ros image and shows in opencv format, does also work for compressed images.

  
# Import the necessary libraries
import rclpy # Python library for ROS 2
from rclpy.node import Node # Handles the creation of nodes
from sensor_msgs.msg import Image, _compressed_image, CompressedImage # Image is the message type
from cv_bridge import CvBridge # Package to convert between ROS and OpenCV Images
import cv2 # OpenCV library
 
class ImageSubscriber(Node):
  """
  Create an ImageSubscriber class, which is a subclass of the Node class.
  """
  def __init__(self):
    """
    Class constructor to set up the node
    """
    # Initiate the Node class's constructor and give it a name
    super().__init__('image_subscriber')
      
    # Create the subscriber. This subscriber will receive an Image
    # from the video_frames topic. The queue size is 10 messages.
    self.subscription = self.create_subscription(
       Image, 
      'stereo/depth',
      self.listener_callback, 
      10)
    self.subscription # prevent unused variable warning

    #create publisher of new RGB image
    self.publisher = self.create_publisher(Image,'stereo/depth/image_rect',10)
      
    # Used to convert between ROS and OpenCV images
    self.br = CvBridge()
   
  def listener_callback(self, data):
    """
    Callback function.
    """
    # Display the message on the console
    self.get_logger().info('Receiving video frame')
 
    # Convert ROS Image message to OpenCV image
    #current_frame = self.br.compressed_imgmsg_to_cv2(data)
    #current_frame = self.br.compressed_imgmsg_to_cv2(data)
    current_frame = self.br.imgmsg_to_cv2(data)

    # convert image
    img_n = cv2.normalize(src=current_frame, dst=None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)
    im_color = cv2.cvtColor(img_n, cv2.COLOR_GRAY2BGR)
    
    # Display image
    
    #cv2.imshow("camera", im_color)
    cv2.imshow("cameraGray", current_frame)

    #publish image on ROS
    pub_img = self.br.cv2_to_imgmsg(current_frame)
    self.publisher.publish(pub_img)

    cv2.waitKey(1999)
  
def main(args=None):
  
  # Initialize the rclpy library
  rclpy.init(args=args)
  
  # Create the node
  image_subscriber = ImageSubscriber()
  
  # Spin the node so the callback function is called.
  rclpy.spin(image_subscriber)
  
  # Destroy the node explicitly
  # (optional - otherwise it will be done automatically
  # when the garbage collector destroys the node object)
  image_subscriber.destroy_node()
  
  # Shutdown the ROS client library for Python
  rclpy.shutdown()
  
if __name__ == '__main__':
  main()