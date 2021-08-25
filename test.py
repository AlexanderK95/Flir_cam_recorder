from llpyspin import primary
from llpyspin import secondary
import time


if __name__ == '__main__':
    fps = 15

    device1 = str(21190983)
    device2 = str(21187340)
    # device = str(21187340)
    cam0 = primary.PrimaryCamera(device1)    
    cam0.framerate = fps
    cam1 = secondary.SecondaryCamera(device2)  

    filename = 'test_cam0.mp4' # suffixed with .mp4
    cam0.prime(filename)
    filename2 = 'test_cam1.mp4' # suffixed with .mp4
    cam1.prime(filename2, cam0.framerate)

    cam0.trigger()
    time.sleep(5)

    cam0.stop()
    cam1.stop()
