import cv2
import numpy as np

# Edge detection


def canny(image):
    """
    Converteert frame/afbeelding naar zwart wit kleuren ruimte
    voert  Gaussion blur uit om de scherpe randen weg te vagen
    converteert de frame/afbeelding uit eindelijk naar canny vorm (rand herkenning)
    :param image: een afbeelding/frame in de vorm van een numpy array 
    """
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    canny = cv2.Canny(blur, 50, 150)
    return canny


def makeCor(image, lineparameter):
    """
    berekent de coordinaten van de lijnen die getekend gaan worden
    :param image: een afbeelding/frame in de vorm van een numpy array 
    :param lineparameter: een tuple die de parameters helling en variabel hebben
    """
    slope, intercept = lineparameter
    y1 = image.shape[0]
    y2 = int(y1*(3/5))
    x1 = int((y1-intercept)/slope)
    x2 = int((y2-intercept)/slope)
    return np.array([x1, y1, x2, y2])


def average_slope_intercept(image, lines):
    """berekent de helling van de lijnen die getekend gaan worden
        :param image: een afbeelding/frame in de vorm van een numpy array 
        :param lines: resultaat van cv2.houghLinesP
"""
    left_fit = []
    right_fit = []

    for line in lines:
        x1, y1, x2, y2 = line.reshape(4)
        parameters = np.polyfit((x1, x2), (y1, y2), 1)
        slope = parameters[0]
        intercept = parameters[1]
        if slope < 0:
            left_fit.append((slope, intercept))
        else:
            right_fit.append((slope, intercept))

    left_fit_average = np.average(left_fit, 0)
    right_fit_average = np.average(right_fit, 0)
    left_line = makeCor(image, left_fit_average)
    right_line = makeCor(image, right_fit_average)
    return np.array([left_line, right_line])


def region_of_interest(image):
    """
    maakt masker voor gegeven afbeelding/frame zodat de rest van de afbeelding/frame later genegeerd kan worden.
    :param image: een afbeelding/frame in de vorm van een numpy array 

    """
    height = image.shape[0]
    polygons = np.array([[(200, height), (1100, height), (550, 250)]])
    mask = np.zeros_like(image)
    cv2.fillPoly(mask, polygons, 255)
    masked_image = cv2.bitwise_and(image, mask)
    return masked_image


def display_lines(image, lines):
    """tekent lijnen op gegeven frame/afbeelding
    :param image: een afbeelding/frame in de vorm van een numpy array
            :param lines: resultaat van cv2.houghLinesP

"""
    line_image = np.zeros_like(image)
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line.reshape(4)
            cv2.line(line_image, (x1, y1), (x2, y2), (255, 0, 0), 10)
    return line_image

#open video
cap = cv2.VideoCapture("test2.mp4")
while (cap.isOpened()): 
    try:
        #lees video
        succes, frame = cap.read()
        #edgedectection
        canny_image = canny(frame)
        #masked image
        cropped_image = region_of_interest(canny_image)
        #bereken lines
        lines = cv2.HoughLinesP(cropped_image, 2, np.pi/180,
                                100, np.array([]), minLineLength=40, maxLineGap=100)
        #bereken helling
        averaged_lines = average_slope_intercept(frame, lines)
        line_image = display_lines(frame, averaged_lines)
        # plak alles aanelkaar
        combo = cv2.addWeighted(frame, 0.8, line_image, 1, 1)
        cv2.imshow("result", combo)
        if cv2.waitKey(1) == ord('q'):
            break
    except Exception as e:
        print(e)

cap.release()
cv2.destroyAllWindows()
