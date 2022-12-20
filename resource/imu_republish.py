# ROS programm to subsribe to /imu and republish adjusted data to /imu_rect
# Imu message types on https://www.programcreek.com/python/example/99836/sensor_msgs.msg.Imu
  
# Import the necessary libraries
import rclpy # Python library for ROS 2
from rclpy.node import Node # Handles the creation of nodes
from sensor_msgs.msg import  Imu # Image is the message type


 
class ImuSubscriber(Node):
  """
  Create an ImageSubscriber class, which is a subclass of the Node class.
  """
  def __init__(self):
    """
    Class constructor to set up the node
    """
    # Initiate the Node class's constructor and give it a name
    super().__init__('imu_subscriber')
    super().__init__('imu_publisher')
      
    # Create the subscriber. This subscriber will receive an Image
    # from the video_frames topic. The queue size is 10 messages.
    self.subscription = self.create_subscription(
      #Image, 
      Imu,
      #'video_frames', 
      #'right/image_rect', # Thi works 
      'imu',
      self.listener_callback, 
      10)
    self.subscription # prevent unused variable warning

    self.publisher = self.create_publisher(
        Imu,
        'imu_rect',
        10
    )

   
  def listener_callback(self, data):
    """
    Callback function.
    """
    # Display the message on the console
    self.get_logger().info('Receiving imu frame')
    
    # new imu data
    new_lin_z = data.linear_acceleration.x
    new_lin_x = data.linear_acceleration.z

    data.linear_acceleration.x , data.linear_acceleration.z = new_lin_x, new_lin_z * -1
    #data.linear_acceleration.x , data.linear_acceleration.y, data.linear_acceleration.z = 10.0 ,0.0, 0.0
    
    # TODO: see use of this next step
    #data.orientation.x = 0.5
    #data.orientation.y = 0.0
    #data.orientation.z = 0.5
    #data.orientation.w = 0.2
    #data.angular_velocity.x = 0.0
    #data.angular_velocity.y = 0.0
    #data.angular_velocity.z = 0.0
    #pub imu_rect 
    self.publisher.publish(data)


 

  
def main(args=None):
  
  # Initialize the rclpy library
  rclpy.init(args=args)
  
  # Create the node
  imu_subscriber = ImuSubscriber()
  
  # Spin the node so the callback function is called.
  rclpy.spin(imu_subscriber)
  
  # Destroy the node explicitly
  # (optional - otherwise it will be done automatically
  # when the garbage collector destroys the node object)
  imu_subscriber.destroy_node()
  
  # Shutdown the ROS client library for Python
  rclpy.shutdown()
  
if __name__ == '__main__':
  main()