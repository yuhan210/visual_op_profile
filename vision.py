import os
import cv2
import time
import numpy as np



def getSobel(img, k_size = 3):

    ddepth = cv2.CV_16S
    scale = 1
    delta = 0

    cv2.GaussianBlur(img, (3,3), 0)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    #Gradient-x
    grad_x = cv2.Sobel(gray, ddepth, 1, 0, ksize = k_size, scale = scale, delta = delta, borderType = cv2.BORDER_DEFAULT)

   
    #Gradient-y
    grad_y = cv2.Sobel(gray, ddepth, 0, 1, ksize = k_size, scale = scale, delta = delta, borderType = cv2.BORDER_DEFAULT)

    # converting back to uint8
    abs_grad_x = cv2.convertScaleAbs(grad_x)
    abs_grad_y = cv2.convertScaleAbs(grad_y)
   
    dst = cv2.addWeighted(abs_grad_x,0.5,abs_grad_y,0.5,0)
    #dst = cv2.add(abs_grad_x,abs_grad_y)

    return dst.mean()

def getIlluminance(img):

    img_out = cv2.cvtColor(img, cv2.COLOR_BGR2YUV)
    y,u,v = cv2.split(img_out) 
    ave_lum = np.mean(y)
    
    return ave_lum

def getFrameDiff(prev_frame, cur_frame):

    prev_frame = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
    cur_frame = cv2.cvtColor(cur_frame, cv2.COLOR_BGR2GRAY)
    
    frameDelta = cv2.absdiff(prev_frame, cur_frame)
    thresh = cv2.threshold(frameDelta, 35, 255, cv2.THRESH_BINARY)[1]

    thresh = cv2.dilate(thresh, None, iterations=2)
    movement = cv2.countNonZero(thresh)


    return movement

if __name__ == "__main__":

    video_path = '/home/ubuntu/ffmpeg/doc/examples/14_year_old_girl_playing_guitar_cover_van_halen__eruption_solo_hd_best_quality_fDTm1IzQf-U.mp4'
    cap = cv2.VideoCapture(video_path)

    counter = 0
    sobel_time = []
    illu_time = []
    framediff_time = []
    resize_time = []
    while(cap.isOpened()):
        ret, frame = cap.read()
        if frame == None or frame.size == 0:
            break
        #print frame.shape
        tic = time.time()
        frame = cv2.resize(frame, (160, 120)) 
        toc = time.time()
        resize_time += [(toc - tic) * 1000]
        tic = time.time()
        getSobel(frame)
        toc = time.time()
        sobel_time += [(toc - tic) * 1000]
        tic = time.time()
        getIlluminance(frame)
        toc = time.time()
        illu_time += [(toc - tic) * 1000]
        tic = time.time()
        getFrameDiff(frame, frame)
        toc = time.time()
        framediff_time += [(toc - tic) * 1000]
    cap.release()
    print np.mean(resize_time), np.std(resize_time)
    print np.mean(sobel_time), np.std(sobel_time)
    print np.mean(illu_time), np.std(illu_time)
    print np.mean(framediff_time), np.std(framediff_time)

