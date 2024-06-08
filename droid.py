
# from arrowcnn import ArrowCnn
import cv2 as cv
import numpy as np
import typing


class Droid():
    def __init__(self, camera_index):
        self.camera = cv.VideoCapture(camera_index)
        self.droid_status = True
        # self.line : list = ArrowCnn.detect_trail()
        self.FPS = 50  # Frames per second
        # I reckon have a low FPS for straight line and a higher one for curvy lines and corners
        self.blue_lower = None
        self.blue_upper = None
        self.yellow_lower = None
        self.yellow_upper = None
        # Not sure yet.
        self.center_x = 0
        self.center_y = 0
        distance_thresh = 0
    
        # test these thresholds on frames with masks on.
        
    def arrow_detection(self):
        """detect arrow"""
        # get frame and send to pytorch
        
        # get current image/ from pytorch model
        # evaliuate whethere it's right or a left turn
        
        # determine a threshold to determine which arrow image is good to start counting distance
        # for e.g we don't want to count just lines
        pass
    
    def turn_degree(self):
        """Find the degree of turning"""
        pass
    
    def obstacle_diversion(self) -> int:
        # get distance from c code
        # purple
        pass
    
    def sliding_window(self):
        pass
    
    def avoid_obstacles(self) -> None:
        # Wait to see for the ultrasonic sensor
        pass
    
    def rbg_bgr_2_hsv(self) -> np.ndarray:
        # These are RGB Colours from RapidTables
        # "Light_purple" : np.uint8([[[230,230,250]]]),
        
        blue_lower_rbg =np.array([21,40,50], dtype=np.uint8)
        blue_upper_rbg = np.array([170,0,255], dtype=np.uint8)
        
        # converting it to an image with the channels
        blue_lower_rgb_img = np.array([[blue_lower_rbg]], dtype=np.uint8)
        blue_upper_rgb_img = np.array([[blue_upper_rbg]], dtype=np.uint8)
        
        # converting to hsv and extracting the single pixel
        self.blue_lower = cv.cvtColor(blue_lower_rgb_img, cv.COLOR_RGB2HSV)[0][0]
        self.blue_upper = cv.cvtColor(blue_upper_rgb_img, cv.COLOR_RGB2HSV)[0][0]
        
        yellow_lower_rbg = np.array([100, 87, 61], dtype=np.uint8)
        yellow_upper_rbg = np.array([255, 255, 0], dtype=np.uint8)
        yellow_lower_rgb_img = np.array([[yellow_lower_rbg]], dtype=np.uint8)
        yellow_upper_rgb_img = np.array([[yellow_upper_rbg]], dtype=np.uint8)
        yellow_lower_hsv = cv.cvtColor(yellow_lower_rgb_img, cv.COLOR_RGB2HSV)[0][0]
        yellow_upper_hsv = cv.cvtColor(yellow_upper_rgb_img, cv.COLOR_RGB2HSV)[0][0]
        # adjusting the range for yellow
        # self.yellow_lower = np.array([light_yellow_hsv_img[0] - 10, 100, 100])
        # self.yellow_upper = np.array([light_yellow_hsv_img[0] + 10, 255, 255])
        self.yellow_lower = yellow_lower_hsv
        self.yellow_upper = yellow_upper_hsv
        
    def steering(self, derivative: int) -> None:
        """Not now, but i need to adjust the fps if the derivative is too high"""
        """I also need to figure out speed too"""
        if derivative == 0:
            # Move forward
            pass
        else:
            if derivative < 0 :
                # steer right
                # Run c code and provide relevant parameters
                print(f"Steering right")
                pass
            if derivative > 0 :
                # steer left
                print(f"Steering left")
                pass
    
    def close(self) -> None:
        # Release the video capture object and close all windows
        self.camera.release()
        cv.destroyAllWindows()
    
    def colour_detection(self, frame) -> list:
        """This function blurs each frame to reduce noise and also converts it to HSV to create masks"""
        # convert to Hue/Sat/Val
        blurred_frame = cv.GaussianBlur(frame, (5, 5), 0)
        hsv = cv.cvtColor(blurred_frame, cv.COLOR_BGR2HSV)
        # Create masks for blue and yellow
        # identify the colours in the image and isolate
        BLUE_MASK = cv.inRange(hsv, self.blue_lower, self.blue_upper)
        YELLOW_MASK = cv.inRange(hsv, self.yellow_lower, self.yellow_upper)
        # Combine masks to see the track
        COMBINED_MASKS = cv.bitwise_or(BLUE_MASK, YELLOW_MASK)
        return [COMBINED_MASKS, BLUE_MASK, YELLOW_MASK]

    def canny_edge(self, mask):
        """Detects edges"""
        edges = cv.Canny(mask, threshold1=50, threshold2=150)
        return edges 
    
    def find_contours(self,mask):
        # mask can be edge as well
        # cv2.RETR_EXTERNAL will focus on the outer shape of the track
        # for Contour Approximation Method
        # maybe use simple for now to save memory, but later on prototyping
        # we might need to approximate for more boundary points 
        # although a little computationally expensive for the raspberry pi
        contours, _ = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        # offset irrelevant for now
        # Optional offset by which every contour point is shifted. 
        # This is useful if the contours are extracted from the image ROI and then they should be analyzed in the whole image context
        return contours

    def get_centroid(self, contour) -> tuple[int, int]:
        # moments will have area, centroid, and orientation of the pixel.
        # M will return a few moments in a dict format
        M = cv.moments(contour)
        # print(type(M["m10"]))
        # The zeroth moment, which represents the area of the contour.
        if M["m00"] != 0:
            # Typecasting is crucial as the moments are in default float.
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
        else:
            cX, cY = 0, 0
        return (cX, cY)

    def calculate_center_line(self, blue_contours, yellow_contours) -> tuple[int, int]:
        if blue_contours and yellow_contours:
            blue_c = max(blue_contours, key=cv.contourArea)
            yellow_c = max(yellow_contours, key=cv.contourArea)

            # get centroids and return these coordinates as a tuple
            blue_centroid = self.get_centroid(blue_c)
            yellow_centroid = self.get_centroid(yellow_c)

            # get middle of the line.
            center_x = (blue_centroid[0] + yellow_centroid[0]) // 2
            center_y = (blue_centroid[1] + yellow_centroid[1]) // 2

            return (center_x, center_y)
        return None, None
    
    def centroids_center(self, roi) -> tuple[int, int]:
        combined_mask, blue_mask, yellow_mask = self.colour_detection(roi)
        blue_edges = self.canny_edge(blue_mask)
        yellow_edges = self.canny_edge(yellow_mask)
        
        # Get Contours
        blue_contours = self.find_contours(blue_edges)
        yellow_contours = self.find_contours(yellow_edges)
        
        # Calculate the center of the track
        center_x, center_y = self.calculate_center_line(blue_contours, yellow_contours)
        return center_x, center_y
    
    def distance_to_turn(self, frame_width: int, cx: int, arrow=None) -> int:
        """This function calculates the difference between the track and the center of the camera."""
        """Thus returns the difference for how much distance there is to turn for the steering function"""
        # check if frame_width and center is not the same
        #  ??
        # I might have to use multithreading here unfortunately 
        # OMG mutexes and stuff
        # Only because i have to check for arrows as well.
        # but not here instead where this function is invoked
        frame_center = frame_width // 2
        derivative = frame_center - cx
        return derivative

    def calculate_wac(self, centers : list[tuple, tuple, tuple, tuple], weights : list) -> tuple[int, int]:
        # calculate weighted average center
        if centers and weights:
            sum_weighted_x = sum(l[0]* w for l, w in zip(centers, weights))
            sum_weighted_y = sum(l[1]* w for l, w in zip(centers, weights))
            avg_x = sum_weighted_x//sum(weights)
            avg_y = sum_weighted_y//sum(weights)
            return (avg_x, avg_y)
        return None, None
    
    def detect_track(self) -> None:
        # Create a VideoCapture object to capture frames from the webcam
        if not self.camera.isOpened():
            print("Cannot open camera")
            # return False

        while True:
            ret, frame = self.camera.read()
            if not ret:
                print("CAN'T EXTRACT FRAME! CRITICAL ISSUE!!")
                break
            
            # debuggiung
            self.rbg_bgr_2_hsv()
            combined, blue, yellow = self.colour_detection(frame)
            
            height, width, _ = frame.shape
            third_frame = (height//2) + (height//4)
            
            FUTURE_ROI1 = frame[:height//4,:]
            FUTURE_ROI = frame[height//4:height//2,:]
            NEXT_ROI = frame[height//2:third_frame,:]
            CURRENT_ROI = frame[third_frame:,:]
    
            
            ROI = [CURRENT_ROI, NEXT_ROI, FUTURE_ROI, FUTURE_ROI1]
            
            centers, weights = [],[4,3,2,1]
            # find what reverse does
            # Get the centers of centroids
            # centers = [self.centroids_center(i) for i in ROI]
            for i in range(len(ROI)):
                center_x, center_y = self.centroids_center(ROI[i])
                if center_x != None and center_y != None:
                    centers.append((center_x, center_y))
            # print(centers)
                # perhaps consider a dictionary
            # OMG Big bug avoided here
            self.center_x, self.center_y = self.calculate_wac(centers, weights[:len(centers)])
            
    
            if self.center_x is not None and self.center_y is not None:
                for i in range(len(centers)):
                    cv.circle(CURRENT_ROI, centers[i], 5, (255, 0, 0), -1)
                cv.circle(CURRENT_ROI, (self.center_x, self.center_y), 5, (255, 0, 0), -1)
                # deviation = self.distance_to_turn(frame.shape[1], cx=self.center_x)
                # self.steering(deviation)
                
                # ----INVOKE STEERING FUNCTION HERE-----

            cv.imshow('1. FUTURE_ROI1', FUTURE_ROI1)
            cv.imshow('2. FUTURE_ROI', FUTURE_ROI)
            cv.imshow('3. NEXT_ROI', NEXT_ROI)
            cv.imshow('4. CURRENT_ROI', CURRENT_ROI)
            
            # cv.imshow("Yellow", yellow)
            # cv.imshow("blue", blue)
            cv.imshow("combined", combined)
            # cv.imshow('5. Frame', frame)
            
    
            
            # Check for the 'q' key press to exit the loop
            if cv.waitKey(1000 // self.FPS) == ord('q'):  # Adjust delay based on desired FPS
                break 
    
