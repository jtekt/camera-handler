# Camera handler

A microservice to serve frames and streams from an USB camera over HTTP.

## API 
|Route|Method|Description|
|-|-|-|
|/|GET|Description of API|
|/frame|GET|Capture a frame using camera|
|/stream|GET|Stream a series of frames using camera|
|/settings|GET|Get the camera settings|
|/settings|PATCH|Update some of the camera settings|

## Environment variables
|Variable|Description|
|-|-|
| FPS | Stream framereate |
| INITIAL_SETTINGS | Camera intiial settings in Stringified JSON format. Example: INITIAL_SETTINGS={ "exposure_auto" : 0 } |