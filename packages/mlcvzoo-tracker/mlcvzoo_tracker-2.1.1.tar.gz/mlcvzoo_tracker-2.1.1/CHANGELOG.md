# MLCVZoo mlcvzoo_tracker module Versions:

2.1.1 (2024-06-18):
------------------
Adapt python package management:
- Replace poetry by uv as dependency resolver and installer
- Replace poetry by the python native build package for building the python package

2.1.0 (2024-02-16)
------------------
Add consecutive check for Tracks in the INITIAL state:
- Tracks only become ACTIVE when they have gotten the configured number
  of sensor updates in consecutive frames
- Add configuration parameter 'min_consecutive_detections_active'

2.0.1 (2024-02-07):
------------------
Updated links in pyproject.toml

2.0.0 (2024-01-23)
------------------
Ensure valid boxes:
- Add width and height as kalman filter states to have correctly shaped bounding boxes
- Check whether a box is outside of the image borders, if so it is no longer valid
- Usability:
  - Since the HungarianImageTracker is designed to track objects of a specific class-identifier,
    the multiple configuration entries of the TrackingToolTrackerConfigObjectSpeed are confusing. Therefore,
    now there is only one configuration entry instead of a list
  - Rename:
    - TrackingToolTrackerConfigObjectSpeed.x => TrackingToolTrackerConfigObjectSpeed.v
    - TrackingToolTrackerConfigObjectSpeed.b => TrackingToolTrackerConfigObjectSpeed.s_0
- Change timestamp of tracks from datetime.now() to datetime.utcnow()
- Correct re-detection radius

1.0.0 (2023-10-16)
------------------
Refactor handling of ImageTracks:
- Rely on a "current_track_event" rather than managing a complete dictionary of the whole track sequence
- However, provide the possibility to manage such a dictionary if needed
- Apply runtime performance optimizations where possible

0.1.1 (2023-05-25)
------------------
Relicense to OLFL-1.3 which succeeds the previous license

0.1.0 (2023-03-15)
------------------
- initial release of the package
