# rtsp-camera-ros-driver

This ROS package contains a driver node that reads frames from an RTSP video stream (e.g., IP Camera) and publishes them out as [sensor_msgs/Image](http://docs.ros.org/api/sensor_msgs/html/msg/Image.html) ROS messages.
It also takes in calibration yaml file from [MRPT Calibration Tool](https://docs.mrpt.org/reference/latest/app_camera-calib.html) and publishes [sensor_msgs/CameraInfo](https://docs.ros.org/en/noetic/api/sensor_msgs/html/msg/CameraInfo.html) ROS message.

# Configuration

`rtsp_ros_driver` implements the ROS interface.
This means that the driver node can seamlessly handle camera calibration files. `rtsp_ros_driver` stores camera
calibration files in the directory `./config/calibration.yml`.


# Tutorial

You can launch the `rtsp_ros_driver` main node by running:

```
roslaunch rtsp_ros_driver rtsp_camera.launch <arguments>
```


# Launch files

## rtsp_camera.launch
Launches the main node of the package (i.e., `rtsp_driver_node`). Unlike the `rtsp_driver_node` node, this launch file allows us to specify the feed URL and other parameters about the camera separately. It also specifies the calibration file location and the published topics names.

### Subscribed topics
None.

### Published topics
Identical to the `rtsp_driver_node` node (see below).

### Arguments

#### Mandatory arguments

_rtsp\_url_
  &nbsp;&nbsp;
  (`string`)
<br/>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 
    URL of the video stream published by the RTSP camera.
    <br/>    
    

#### Optional arguments

_camera\_name_
  &nbsp;&nbsp;
  (`string`, default: _camera_)
<br/>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 
    Namespace of the camera.
    <br/>

_frame\_id_
  &nbsp;&nbsp;
  (`string`, default: _camera\_optical\_frame_)
<br/>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 
    Name of the camera reference frame.
    <br/>

_calibration\_file_
  &nbsp;&nbsp;
  (`string`, default: $(find rtsp\_ros\_driver)/config/calibration.yml)
<br/>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 
    Location of the calibration file.
    <br/>

_image\_raw\_topic_
  &nbsp;&nbsp;
  (`string`, default: _$(arg camera\_name)/image\_raw_)
<br/>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 
    Name of the output image topic.
    <br/> 

_camera\_info\_topic_
  &nbsp;&nbsp;
  (`string`, default: _$(arg camera\_name)/camera\_info_)
<br/>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 
    Name of the output camera info topic.
    <br/> 

_enable\_image\_view_
  &nbsp;&nbsp;
  (`bool`, default: _false_)
<br/>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 
    Image viewer for debugging.
    <br/>

_publish\_rate_
  &nbsp;&nbsp;
  (`int`, default: _30_)
<br/>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 
    Publishing rate in Hz.
    <br/>
    

# Nodes

## rtsp_driver_node
Main node of the package, it is responsible for reading frames from the given RTSP video stream source and publishing them out as [sensor_msgs/Image](http://docs.ros.org/api/sensor_msgs/html/msg/Image.html) ROS messages.

### Subscribed topics
None.

### Published topics

_/<camera\_name>/<image\_raw\_topic>_
  &nbsp;&nbsp;
  ([sensor_msgs/Image](http://docs.ros.org/api/sensor_msgs/html/msg/Image.html))
<br/>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 
    Raw image stream from the camera.
    <br/>
    
_/<camera\_name>/<camera\_info\_topic>_
  &nbsp;&nbsp;
  ([sensor_msgs/CameraInfo](http://docs.ros.org/api/sensor_msgs/html/msg/CameraInfo.html))
<br/>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 
    Camera metadata.
    <br/>

### Parameters

#### Mandatory parameters

~_rtsp\_url_
  &nbsp;&nbsp;
  (`string`)
<br/>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 
    RTSP URL to the camera string.
    <br/>


#### Optional parameters

_camera\_name_
  &nbsp;&nbsp;
  (`string`, default: _camera_)
<br/>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 
    Namespace of the camera.
    <br/>

_frame\_id_
  &nbsp;&nbsp;
  (`string`, default: _camera\_optical\_frame_)
<br/>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 
    Name of the camera reference frame.
    <br/>

_calibration\_file_
  &nbsp;&nbsp;
  (`string`, default: $(find rtsp\_ros\_driver)/config/calibration.yml)
<br/>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 
    Location of the calibration file.
    <br/>

_image\_raw\_topic_
  &nbsp;&nbsp;
  (`string`, default: _$(arg camera\_name)/image\_raw_)
<br/>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 
    Name of the output image topic.
    <br/> 

_camera\_info\_topic_
  &nbsp;&nbsp;
  (`string`, default: _$(arg camera\_name)/camera\_info_)
<br/>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 
    Name of the output camera info topic.
    <br/> 

_enable\_image\_view_
  &nbsp;&nbsp;
  (`bool`, default: _false_)
<br/>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 
    Image viewer for debugging.
    <br/>

_publish\_rate_
  &nbsp;&nbsp;
  (`int`, default: _30_)
<br/>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 
    Publishing rate in Hz.
    <br/>
