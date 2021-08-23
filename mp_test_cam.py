# import the necessary packages
from __future__ import print_function
# from imutils.video import WebcamVideoStream
# from imutils.video import FPS
import argparse
# # import imutils
# import cv2 as cv2
import time
from datetime import datetime
# import warnings
import csv
import os
import PySpin
# import llpyspin
from llpyspin import primary
from llpyspin import secondary
import sys
# from daq import DaqController
from keylogger import Keylogger 



if __name__ == '__main__':
    fps = 60
    width = 720
    height = 480

    # numCams = 1
    # fileNames = ['Cam_1.avi', 'Cam_2.avi', 'Cam_3.avi', 'Cam_4.avi']

    # construct the argument parse and parse the arguments
    # ap = argparse.ArgumentParser()
    # ap.add_argument("-f", "--fps", type=int, default=fps,
    # 	help="Targeted fps")
    # ap.add_argument("-w", "--width", type=int, default=width,
    # 	help="Width of video")
    # ap.add_argument("-h", "--height", type=int, default=height,
    # 	help="Height of video")
    # ap.add_argument("-n", "--num-cams", type=int, default=numCams,
    # 	help="# of Cameras used")
    # ap.add_argument("-d", "--display", type=int, default=1,
    # 	help="Whether or not frames should be displayed")
    # args = vars(ap.parse_args())

    folder = 'data/%s'%datetime.now().strftime("%Y-%m-%d")
    # if not os.path.exists(folder):
    #     os.makedirs(folder)
    # created a *threaded* video stream, allow the camera sensor to warmup,
    # and start the FPS counter
    date = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    frames = {}
    out = {}
    log = []
    
    # font                   = cv2.FONT_HERSHEY_SIMPLEX
    topLeftCornerOfText = (5,30)
    fontScale              = 1
    fontColor              = (255,255,255)
    lineType               = 2
    
    first_start = True
    recording = False
    next_file = True
    run_nr = 1

    print("[INFO] initiating webcams (this may take a minute)...")
    system = PySpin.System.GetInstance()
    # Get current library version
    version = system.GetLibraryVersion()
    print('Library version: %d.%d.%d.%d' % (version.major, version.minor, version.type, version.build))
    # Retrieve list of cameras from the system
    cam_list = system.GetCameras()
    sn_list = {}
    num_cameras = cam_list.GetSize()
    print('Number of cameras detected: %d' % num_cameras)

    if num_cameras == 0:

        # Clear camera list before releasing system
        cam_list.Clear()

        # Release system instance
        system.ReleaseInstance()

        print('Not enough cameras!')
        input('Done! Press Enter to exit...')
        sys.exit(1)

    print('[INFO] Registering cameras...')
    for i, cam in enumerate(cam_list):
        nodemap_tldevice = cam.GetTLDeviceNodeMap()
        node_device_serial_number = PySpin.CStringPtr(nodemap_tldevice.GetNode("DeviceSerialNumber"))

        if PySpin.IsAvailable(node_device_serial_number) and PySpin.IsReadable(node_device_serial_number):
            sn_list[i] = node_device_serial_number.GetValue()
        else:
            print('[WARNING] Could not retrieve serial number of camera %d!' % i)
            input('Exiting due to error! Press Enter to exit...')
            sys.exit(1)


    # cv2.namedWindow("Camera feed")
    # print("[INFO] initiating DAQ and Keylogger...")
    
    # daq = DaqController(channels=[0,1], folder=folder,sample_rate=1000)
    
    print('[INFO] Initiating primary camera')
    cam_prime = primary.PrimaryCamera(str(sn_list[0]))
    cam_prime.framerate = fps   
    cam_prime.prime(f'data/test_cam1_{date}.mp4')

    print('[INFO] Initiating secondary cameras (if any)')
    sec_cams = {}
    for ind, sn in list(sn_list.items())[1:]:
        filename = f'data/test_cam{ind}_{sn}_{date}.mp4' # suffixed with .mp4
        sec_cams[ind] = secondary.SecondaryCamera(str(sn))
        sec_cams[ind].prime(filename,cam_prime.framerate)


    
    print("[INFO] initiating Keylogger...")
    kl = Keylogger().start()
    timestamps_sec = {}
    while True:
        if first_start and kl.recording:
            print('[INFO] Start recording')
            recording = kl.recording
            first_start = False
            cam_prime.trigger()
        elif not first_start and not kl.recording and next_file:
            print('[INFO] Stop recording')
            recording = kl.recording
            run_nr = kl.run
            print(run_nr)
            next_file = False
            timestamps_prime = cam_prime.stop()
            for ind, cam in sec_cams.items():
                timestamps_sec[sn_list[ind]] = cam.stop()
            break
        else:
            recording = kl.recording


    data = {}
    data[sn_list[0]] = timestamps_prime
    for ind, sn in list(sn_list.items())[1:]:
        data[sn] = timestamps_sec[sn]

    # with open('%s/%s_log.csv' % (folder,date), 'w') as csvfile:
    #     writer = csv.DictWriter(csvfile, fieldnames=sn_list)
    #     writer.writeheader()
    #     writer.writerows(data)

    







    # fpsObj = FPS().start()
    # loop over some frames...this time using the threaded stream
    # print("[INFO] sampling THREADED frames from webcam...")
    # frameCallStart = time.time_ns()
    # try:
    #     while True:
    #     	# grab the frame from the threaded video stream and resize it
    #     	# to have a maximum width of 400 pixels
    #         if first_start and kl.recording:
    #             recording = kl.recording
    #             # print('First start!!! starting DAQ')
    #             daq.start()
    #             first_start = False
    #         elif not first_start and not kl.recording and next_file:
    #             recording = kl.recording
    #             run_nr = kl.run
    #             print(run_nr)
    #             # release write stream
    #             for i in range(numCams):
    #                 out[i].release()
    #                 time.sleep(0.2)
    #                 out[i] = cv2.VideoWriter("%s/%s_run%i_%s"%(folder,date,run_nr,fileNames[i]),cv2.VideoWriter_fourcc('M','J','P','G'), fps, (width,height))
    #             # print('stopping DAQ')
    #             daq.stop()
    #             next_file = False
    #         elif not first_start and not recording and not next_file and kl.recording:
    #             recording = kl.recording
    #             # print('starting DAQ')
    #             daq.start(date=date)
    #             next_file = True
    #         # else:
    #         #     recording = kl.recording
    #         timestamps = {}
    #         for i in range(numCams):
    #             frames[i] = cams[i].read()
    #             frames[i] = cv2.resize(frames[i], (width, height))
    #             if recording:
    #                 out[i].write(frames[i])
    #                 timestamps[fileNames[i]] = time.time_ns()
                
                    
    #         # check to see if the frame should be displayed to our screen
    #         if args["display"] > 0:
    #             pos = kl.pos%numCams
    #             img2show = frames[pos]
    #             cv2.putText(img2show,fileNames[pos], 
    #                 topLeftCornerOfText, 
    #                 font, 
    #                 fontScale,
    #                 fontColor,
    #                 lineType)
    #             cv2.imshow("Camera feed", img2show)
    #         if recording:
    #             log.append(timestamps)
    #         key = cv2.waitKey(1)
    #         if key == 27: break
    #     	# update the FPS counter
    #         # frameCallStop = time.time_ns()
    #         # stime = 1/fps - (frameCallStop-frameCallStart)/10**9
    #         # print((time.time_ns()-frameCallStart)*1000)
    #         if 1/fps > (time.time_ns()-frameCallStart)/10**9:
    #             while 1/fps > (time.time_ns()-frameCallStart)/10**9:
    #                 pass
    #                 # stime = 1/fps - (time.time_ns()-frameCallStart)/10**9
    #             # print((time.time_ns()-frameCallStart)/10**6)
    #         else:
    #             print("Program can't keep up!! Call duration {:.4f} > {:.4f}".format((time.time_ns()-frameCallStart)/10**6,1000/fps))
    #         fpsObj.update()
    #         frameCallStart = time.time_ns()
    #         # print("-----------")
    # except Exception as e:
    #     print('\n', e)
    # finally:
    #     # stop the timer and display FPS information
    #     fpsObj.stop()
    #     print("[INFO] elasped time: {:.2f}".format(fpsObj.elapsed()))
    #     print("[INFO] approx. FPS: {:.2f}".format(fpsObj.fps()))
    #     # do a bit of cleanup
    #     cv2.destroyAllWindows()
    
    #     # stop cams and release write stream
    #     for i in range(numCams):
    #         cams[i].stop()
    #         out[i].release()
            
    #     # stop daq and write to mat file
    #     daq.release()
    #     # save log to csv file
    #     with open('%s/%s_log.csv' % (folder,date), 'w') as csvfile:
    #         writer = csv.DictWriter(csvfile, fieldnames=fileNames)
    #         writer.writeheader()
    #         writer.writerows(log)