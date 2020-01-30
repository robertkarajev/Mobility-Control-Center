import cv2
import numpy as np 

def canny(image):
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    blur = cv2.GaussianBlur(gray,(5,5),0)
    canny = cv2.Canny(blur,50,150)
    return canny

def makeCor(image,lineparameter):
    slope, intercept = lineparameter
    y1 = image.shape[0]
    y2= int(y1*(3/5))
    x1 = int((y1-intercept)/slope)
    x2 = int((y2-intercept)/slope)
    return np.array([x1,y1,x2,y2])

def average_slope_intercept(image,lines):
    left_fit=[]
    right_fit=[]
    
    for line in lines:
        x1,y1,x2,y2 =line.reshape(4)
        parameters = np.polyfit((x1,x2),(y1,y2),1)
        slope= parameters[0]
        intercept= parameters[1]
        if slope < 0 :
            left_fit.append((slope,intercept))
        else:
            right_fit.append((slope,intercept))

    left_fit_average = np.average(left_fit,0)
    right_fit_average = np.average(right_fit,0)
    left_line=makeCor(image,left_fit_average)
    right_line =makeCor(image,right_fit_average)
    return np.array([left_line,right_line])

def region_of_interest(image):
    height = image.shape[0]
    polygons = np.array([[(250,height),(1100,height),(550,250)]])
    mask =  np.zeros_like(image)
    cv2.fillPoly(mask,polygons,255)
    masked_image = cv2.bitwise_and(image,mask)
    return masked_image

def display_lines(image,lines):
    line_image=np.zeros_like(image)
    if lines is not None:
        for line in lines:
            x1,y1,x2,y2 = line.reshape(4)
            cv2.line(line_image,(x1,y1),(x2,y2),(255,50,120),10) # pink is life
    return line_image


cap = cv2.VideoCapture("test2.mp4")
while (cap.isOpened()):
    try:
        frame_read_correct,frame=cap.read()

        if frame_read_correct:
            canny_image = canny(frame)
            cropped_image=region_of_interest(canny_image)
            lines = cv2.HoughLinesP(cropped_image,2,np.pi/180,100,np.array([]),minLineLength=50,maxLineGap=80)
            averaged_lines = average_slope_intercept(frame,lines)
            line_image = display_lines(frame,averaged_lines)
            combo = cv2.addWeighted(frame,0.8,line_image,1,1)
            cv2.imshow("result",combo)
        if cv2.waitKey(1) == ord('q'):
            break
        if frame_read_correct is False:
            print("Frame wordt niet correct gelezen")
    except Exception as e:
        print(e)

cap.release()
cv2.destroyAllWindows()







