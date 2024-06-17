# upic
# TagDetector Class Documentation

## Overview
The `TagDetector` class is designed for real-time detection of AprilTags using a camera feed. It leverages OpenCV and the AprilTag library to identify and track specific tags within the camera's field of view. This class encapsulates functionalities such as camera initialization, AprilTag detection setup, resolution adjustment, and control over the detection process, including start, stop, pause, and resume operations.

## Key Features
- **AprilTag Detection**: Utilizes the `Detector` from the AprilTag library with customizable settings for tag family, processing threads, decimation, edge refinement, and debug mode.
- **Configuration Flexibility**: Offers a nested `Config` class to centralize and manage default configurations like operation mode (single tag vs. multiple), resolution scaling, tag ordering strategy, interval for halting checks, and default/error tag IDs.
- **Camera Management**: Provides methods to open, release, and adjust the camera resolution dynamically, ensuring efficient resource handling and适应性to different hardware capabilities and requirements.
- **Detection Loop**: Implements a threaded detection loop that can be controlled externally to start, halt, and resume tag detection without interrupting the main application flow. This design enables non-blocking operation and responsiveness in applications where real-time feedback is crucial.
- **Tag Ordering Strategies**: Supports two ordering methods for handling multiple detections: "nearest" (prioritizes the closest tag to the frame center) and "single" (uses the first detected tag), enhancing flexibility based on application needs.
- **Error Handling**: Includes exception handling within the detection loop to gracefully manage camera failures or unexpected errors during tag processing.
- **Property Access**: Exposes properties for querying the current detected tag ID and accessing the underlying camera device instance.

## Usage Example

### Initialization
```python
from upic import TagDetector  # Assuming TagDetector is defined in 'your_module'

# Initialize with optional camera ID and custom resolution multiplier
detector = TagDetector(cam_id=0, resolution_multiplier=0.75)
```

### Camera Operations
```python
# Open camera and start detection
detector.open_camera().apriltag_detect_start()

# At any point, you can halt detection without releasing the camera
detector.halt_detection()

# To resume detection after halting
detector.resume_detection()

# When done, release camera resources
detector.release_camera()
```

### Retrieving Detected Tag ID
```python
current_tag_id = detector.tag_id
print(f"Current Tag ID: {current_tag_id}")
```

### Complete code
```python
from upic import TagDetector  # Assuming TagDetector is defined in 'your_module'

# Initialize with optional camera ID and custom resolution multiplier
detector = TagDetector(cam_id=0, resolution_multiplier=0.75)
# Open camera and start detection
detector.open_camera().apriltag_detect_start()

# At any point, you can halt detection without releasing the camera
detector.halt_detection()

# To resume detection after halting
detector.resume_detection()

# When done, release camera resources
detector.release_camera()

current_tag_id = detector.tag_id
print(f"Current Tag ID: {current_tag_id}")
```
