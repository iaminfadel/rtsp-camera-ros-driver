#!/usr/bin/env python3

import rospy
import cv2
import yaml
import numpy as np
from sensor_msgs.msg import Image, CameraInfo
from cv_bridge import CvBridge

class RtspCameraDriver:
    def __init__(self):
        # Initialize ROS node
        rospy.init_node('rtsp_camera_driver', anonymous=True)
        
        # Get parameters from ROS parameter server
        self.rtsp_url = rospy.get_param('~rtsp_url', 'rtsp://username:password@camera_ip:554/stream')
        self.frame_id = rospy.get_param('~frame_id', 'camera_optical_frame')
        self.calibration_file = rospy.get_param('~calibration_file', 'calibration.yml')
        self.publish_rate = rospy.get_param('~publish_rate', 30)
        
        # Initialize CV Bridge
        self.bridge = CvBridge()
        
        # Initialize publishers
        self.image_pub = rospy.Publisher('~image_raw', Image, queue_size=10)
        self.camera_info_pub = rospy.Publisher('~camera_info', CameraInfo, queue_size=10)
        
        # Load camera calibration
        self.camera_info = self.load_camera_calibration()
        
        # Initialize video capture
        self.cap = None
        self.connect_to_camera()

    def load_camera_calibration(self):
        try:
            with open(self.calibration_file, 'r') as f:
                calib_data = yaml.safe_load(f)
            
            camera_info_msg = CameraInfo()
            camera_info_msg.header.frame_id = self.frame_id
            camera_info_msg.height = calib_data['image_height']
            camera_info_msg.width = calib_data['image_width']
            camera_info_msg.distortion_model = calib_data['distortion_model']
            
            # Convert calibration data to the correct format
            camera_info_msg.D = calib_data['distortion_coefficients']['data']
            
            # Convert camera matrix (K), rectification matrix (R), and projection matrix (P)
            K = calib_data['camera_matrix']['data']
            camera_info_msg.K = K if len(K) == 9 else [0.0] * 9
            
            R = calib_data['rectification_matrix']['data']
            camera_info_msg.R = R if len(R) == 9 else [1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0]
            
            P = calib_data['projection_matrix']['data']
            camera_info_msg.P = P if len(P) == 12 else [0.0] * 12
            
            rospy.loginfo("Camera calibration loaded successfully")
            return camera_info_msg
            
        except Exception as e:
            rospy.logerr(f"Failed to load camera calibration: {str(e)}")
            return self.create_default_camera_info()

    def create_default_camera_info(self):
        """Create a default camera info message if calibration file cannot be loaded"""
        camera_info_msg = CameraInfo()
        camera_info_msg.header.frame_id = self.frame_id
        camera_info_msg.height = 1080  # Default height
        camera_info_msg.width = 1920   # Default width
        camera_info_msg.distortion_model = 'plumb_bob'
        camera_info_msg.D = [0.0] * 5
        camera_info_msg.K = [1000.0, 0.0, 960.0, 0.0, 1000.0, 540.0, 0.0, 0.0, 1.0]
        camera_info_msg.R = [1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0]
        camera_info_msg.P = [1000.0, 0.0, 960.0, 0.0, 0.0, 1000.0, 540.0, 0.0, 0.0, 0.0, 1.0, 0.0]
        return camera_info_msg

    def connect_to_camera(self):
        try:
            self.cap = cv2.VideoCapture(self.rtsp_url)
            if not self.cap.isOpened():
                raise Exception("Failed to open RTSP stream")
            rospy.loginfo("Successfully connected to camera")
        except Exception as e:
            rospy.logerr(f"Error connecting to camera: {str(e)}")
            self.cap = None

    def run(self):
        rate = rospy.Rate(self.publish_rate)
        
        while not rospy.is_shutdown():
            if self.cap is None or not self.cap.isOpened():
                rospy.logwarn("Attempting to reconnect to camera...")
                self.connect_to_camera()
                rate.sleep()
                continue
                
            try:
                ret, frame = self.cap.read()
                if not ret:
                    rospy.logwarn("Failed to grab frame, attempting to reconnect...")
                    self.connect_to_camera()
                    rate.sleep()
                    continue
                
                # Convert frame to ROS Image message
                current_time = rospy.Time.now()
                image_msg = self.bridge.cv2_to_imgmsg(frame, "bgr8")
                image_msg.header.stamp = current_time
                image_msg.header.frame_id = self.frame_id
                
                # Update camera info timestamp
                if self.camera_info is not None:
                    self.camera_info.header.stamp = current_time
                    
                # Publish messages
                self.image_pub.publish(image_msg)
                if self.camera_info is not None:
                    self.camera_info_pub.publish(self.camera_info)
                
            except Exception as e:
                rospy.logerr(f"Error processing frame: {str(e)}")
                
            rate.sleep()

    def __del__(self):
        if self.cap is not None and self.cap.isOpened():
            self.cap.release()

if __name__ == '__main__':
    try:
        camera_driver = RtspCameraDriver()
        camera_driver.run()
    except rospy.ROSInterruptException:
        pass