# Import the necessary libraries
import rclpy # Python library for ROS 2
from rclpy.node import Node # Handles the creation of nodes
from sensor_msgs.msg import Image, CompressedImage # Image is the message type
from cv_bridge import CvBridge # Package to convert between ROS and OpenCV Images
import cv2 # OpenCV library

# Use these imports for Deep learning part
import roboflow
import base64, requests

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
      #Image, 
      CompressedImage,
      #'video_frames', 
      #'right/image_rect', # Thi works 
      'color/image/compressed',
      self.listener_callback, 
      10)
    self.subscription # prevent unused variable warning
      
    # Used to convert between ROS and OpenCV images
    self.br = CvBridge()

  # Instantiate Roboflow object with your API key
    rf = roboflow.Roboflow(api_key='wptrChO5R7M43Ga9QRi9')

      # List all projects for your workspace
    workspace = rf.workspace()

      # Load a certain project, workspace url is optional
    project = rf.workspace("wageningen-university").project("post_trunk_15-11")

      # List all versions of a specific project
    project.versions()

      # Retrieve the model of a specific project
    self.model = project.version("1").model


  def listener_callback(self, data):
    """
    Callback function.
    """
    # Display the message on the console
    self.get_logger().info('Receiving video frame')
 
    # Convert ROS Image message to OpenCV image
    #current_frame = self.br.imgmsg_to_cv2(data)
    current_frame = self.br.compressed_imgmsg_to_cv2(data)
  


    # Resize the frame, might give better results/faster?
    dim = (round(current_frame.shape[1] * 0.5), round(current_frame.shape[0] * 0.5) )
    current_frame_resize = cv2.resize(current_frame, dim, interpolation= cv2.INTER_AREA)


    # Not very nice - Save image first, then use for dl_model
    cv2.imwrite('images/img.jpg', current_frame)
    self.dl_model('images/img.jpg')
    # Encode image to base64 string
    #_, buffer = cv2.imencode('.jpg', current_frame_resize)
    #img = base64.b64encode(buffer)   #  this we should be able to use in the DL model
    
    # Display image
    #cv2.imshow("camera", current_frame)
    # Display DL image 

    # Use this for saving one random image 
    #cv2.imwrite("image.jpg", current_frame)S
    
    cv2.waitKey(1)

  def dl_model(self, img):
     
      # predict on a local image
      prediction = self.model.predict(img, confidence=25)
      #prediction = model.predict("image.jpg")

      # Predict on a hosted image
      #prediction = model.predict("YOUR_IMAGE.jpg", hosted=True)

      # Plot the prediction
      prediction.plot()

      # Convert predictions to JSON
      #prediction.json()

      # Save the prediction as an image
      #prediction.save(output_path='predictions.jpg')
  
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