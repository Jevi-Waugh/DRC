
# from arrowcnn import ArrowCnn
import cv2 as cv
import numpy as np
import typing
import time

class Droid():
    def __init__(self, camera_index=1, FPS=20, ROH=40, ROW=40, droid_status:bool = False, frame=None):
        self.FPS = FPS  # Frames per second
        self.frame = frame
        # low FPS for straight line and a higher one for curvy lines and corners
        self.camera = cv.VideoCapture(camera_index)
        self.droid_status = droid_status
        self.obstacle:bool = False
        self.deviation = 0
        self.center_x, self.center_y = 0, 0
        self.cannyt1, self.cannyt2 = 50, 150
        self.purple_centroid: tuple[int, int] = None # this is actually the center point of the obstacle.[bounding box though]
        
        self.REAL_OBSTACLE_HEIGHT = ROH
        self.REAL_OBSTACLE_WIDTH = ROW
        self.focal_length = 700 # double check this
        # adjust thresh by 50% or howvever long the droid is for it to have enough space to curve around safely
        self.obstacle_area_thresh = (ROH * ROW)*0.5 
        self.obstacle_area: tuple[int, int] = 0,0 #just in case i need dimensions

        self.blue_lower, self.blue_upper = None, None
        self.yellow_lower, self.yellow_upper = None, None
        self.purple_lower, self.purple_upper = None, None
        self.green_lower, self.green_upper = None, None
        self.red_lower, self.red_upper = None, None
        
        self.PURPLE_MASK, self.GREEN_MASK, self.RED_MASK = None, None, None
        self.green_line: list[int, int] = [0,0] #start and end positions
        self.green_contours = None
        # self.line : list = ArrowCnn.detect_trail()
    def __repr__(self) -> str:
        return f"Droid(droid_status={self.droid_status}, Centroid(cX={self.center_x}, cY={self.center_y}), Focal Length={self.focal_length}"
    
    def __str__(self) -> str:
        return f"Not important atm"
        
    def arrow_detection(self):  # Not implemented -> Urgent
        """detect arrow -> either use contour detection or harris corner detection and get 7 corners"""
        
        # get frame and send to pytorch
        
        # get current image/ from pytorch model
        # evaliuate whethere it's right or a left turn
        
        # determine a threshold to determine which arrow image is good to start counting distance
        # for e.g we don't want to count just lines
        
        def turn_degree(self):  # Not implemented -> Urgent
            """Find the degree of turning"""
            pass
    
    def recalibration_function(self, yellow: bool, blue: bool):  # Not implemented -> Urgent
        """the strict identification and perception of both Blue and Yellow tape"""
        """Assume only one tape was detected"""
        """need a strong value for colour detection this time"""
        pass

    def perspective_transformation(self): # Not implemented -> Urgent
        """This should map the original coordinates to new ones so that it mimics human perception for better input of data"""
        pass
    
    def map_boundboxdim2_framedim(self) -> float: # Not implemented -> Urgent
        """This function maps the boundign box of the object to the frame
        and returns the distance between a line and the object"""
        # update new value for purple centroid
        pass
    
    def detect_red_droid(self, mask):
        # if mask matches red contour:
            # if obstacle:
                # MAYBE SEND AN ARGUMENT TO DC OR AO TO SAY THAT THERE IS A DROID OR SOMETHING
                
        #       then calculate distance:
        #           and adjust distance
        pass
    
    # ^^^^^^^
    # |||||||
    
    def distance_to_turn(self, frame_width, cX, arrow=None) -> int:
        """This function calculates the difference between the track and the center of the camera.
        Thus returns the difference for how much distance there is to turn for the steering function"""
        # perhaps get value from recalibration function that may invoke another function providing
        # the estimated distance its meant to have away from the line.
        frame_center = frame_width // 2
        print(f"frame center={frame_center}, cX={cX}")
        return frame_center - cX if cX!= None else frame_center
        
    def test_obstacle_detection(self, i, text, image): #Testing function
        """This function is only created to test the obstacle detection algorithm not to be deployed"""
        print("[Iteration] {i}".format(text))
        cv.imshow("Approximated Contour", image)
        cv.waitKey(0)
    
    def estimate_object_distance(self) -> int: # Done
        """A mathematical expression to determine how far is the object in the front -> distance of obstacle"""
        return int((self.REAL_OBSTACLE_HEIGHT * self.focal_length) / self.obstacle_area[1])
    
    def rbg_2_hsv(self) -> np.ndarray: #Improved function defined below
        
        # [125, 50, 50]) is what i should get for the purple lower one
        # These are RGB Colours from RapidTables
        # Formatting
        blue_lower_rbg =np.array([21,40,50], dtype=np.uint8)
        blue_upper_rbg = np.array([170,0,255], dtype=np.uint8)
        
        green_lower_rbg =np.array([89,255, 255], dtype=np.uint8)
        green_upper_rbg = np.array([0,255, 0], dtype=np.uint8)
        
        yellow_lower_rbg = np.array([100, 87, 61], dtype=np.uint8)
        yellow_upper_rbg = np.array([255, 255, 0], dtype=np.uint8)
        
        purple_lower_rbg = np.array([230,230,250], dtype=np.uint8)
        
        red_lower_rbg = np.array([[[255, 0, 0]]], dtype=np.uint8)
        red_upper_rbg = np.array([[[255, 51, 51]]], dtype=np.uint8)
        
        # converting it to an image with the channels
        blue_lower_rgb_img = np.array([[blue_lower_rbg]], dtype=np.uint8)
        blue_upper_rgb_img = np.array([[blue_upper_rbg]], dtype=np.uint8)
        
        yellow_lower_rgb_img = np.array([[yellow_lower_rbg]], dtype=np.uint8)
        yellow_upper_rgb_img = np.array([[yellow_upper_rbg]], dtype=np.uint8)
        
        purple_lower_rgb_img = np.array([[purple_lower_rbg]], dtype=np.uint8)
        
        green_lower_rgb_img = np.array([[green_lower_rbg]], dtype=np.uint8)
        green_upper_rgb_img = np.array([[green_upper_rbg]], dtype=np.uint8)
        
        
        # converting to hsv and extracting the single pixel
        self.blue_lower = cv.cvtColor(blue_lower_rgb_img, cv.COLOR_RGB2HSV)[0][0]
        self.blue_upper = cv.cvtColor(blue_upper_rgb_img, cv.COLOR_RGB2HSV)[0][0]
        
        self.yellow_lower = cv.cvtColor(yellow_lower_rgb_img, cv.COLOR_RGB2HSV)[0][0]
        self.yellow_upper = cv.cvtColor(yellow_upper_rgb_img, cv.COLOR_RGB2HSV)[0][0]
        
        self.purple_upper = cv.cvtColor(blue_upper_rgb_img, cv.COLOR_RGB2HSV)[0][0]
        self.purple_lower = cv.cvtColor(purple_lower_rgb_img, cv.COLOR_RGB2HSV)[0][0]
        # experimenting adjustment for the range of yellow
        # self.yellow_lower = np.array([light_yellow_hsv_img[0] - 10, 100, 100])
        # self.yellow_upper = np.array([light_yellow_hsv_img[0] + 10, 255, 255])
        
        self.green_upper = cv.cvtColor(green_upper_rgb_img, cv.COLOR_RGB2HSV)[0][0]
        self.green_lower = cv.cvtColor(green_lower_rgb_img, cv.COLOR_RGB2HSV)[0][0]
        
        self.red_lower= cv.cvtColor(red_upper_rbg, cv.COLOR_RGB2HSV)[0][0]
        self.red_upper = cv.cvtColor(red_lower_rbg, cv.COLOR_RGB2HSV)[0][0]
       
    def rgb_2_hsv_improved(self, r, g, b) -> None: #DONE
        rbg = np.uint8([[[r,g,b]]])
        hsv = cv.cvtColor(rbg, cv.COLOR_RGB2HSV)[0][0]
        return tuple(int(cl) for cl in hsv)
    
    def deploy_rgb_2_hsv(self) -> None: # Fine-Tuning needed
    # Work on yellow tape and test purple obstacle and green lines
        self.red_lower = self.rgb_2_hsv_improved(255,0,0)
        self.red_upper = self.rgb_2_hsv_improved(255,51,51)
        
        self.blue_lower = self.rgb_2_hsv_improved(21,40,50)
        self.blue_upper = self.rgb_2_hsv_improved(170,0,255)
        
        self.yellow_lower = self.rgb_2_hsv_improved(100, 87, 61)
        self.yellow_upper = self.rgb_2_hsv_improved(255, 255, 0)
        
        self.green_lower = self.rgb_2_hsv_improved(35,100,100)
        self.green_upper = self.rgb_2_hsv_improved(85,255,255)
        
        self.purple_lower = self.rgb_2_hsv_improved(230,230,250)
        self.purple_upper = self.rgb_2_hsv_improved(170,0,255)
        
    def open_camera(self) -> bool:
        # Create a VideoCapture object to capture frames from the webcam
        if not self.camera.isOpened():
            print("uanble to open camera")
            return False 
    
    def close_camera(self) -> None:
        # Release the video capture object and close all windows
        self.camera.release()
        cv.destroyAllWindows()
    
    def colour_detection(self, frame) -> list: 
        """This function blurs each frame to reduce noise and also converts it to HSV to create masks"""
        # Included Purple masks
        # convert t`1`o Hue/Sat/Val
        blurred_frame = cv.GaussianBlur(frame, (5, 5), 0)
        hsv = cv.cvtColor(blurred_frame, cv.COLOR_BGR2HSV)
        # Create masks for blue and yellow
        # identify the colours in the image and isolate
        BLUE_MASK = cv.inRange(hsv, self.blue_lower, self.blue_upper)
        YELLOW_MASK = cv.inRange(hsv, self.yellow_lower, self.yellow_upper)
        self.PURPLE_MASK = cv.inRange(hsv, self.purple_lower, self.purple_upper)
        self.GREEN_MASK = cv.inRange(hsv, self.green_lower, self.green_upper)
        self.RED_MASK = cv.inRange(hsv, self.red_lower, self.red_upper)
        
        # Combine masks to see the track
        # Combining Blue and Yellow first for boundaries/track
        COMBINED_MASKS = cv.bitwise_or(BLUE_MASK, YELLOW_MASK)
        # Adding Purple for object detection
        COMBINED_MASKS = cv.bitwise_or(COMBINED_MASKS, self.PURPLE_MASK)
        # Adding Green for start and end line
        COMBINED_MASKS = cv.bitwise_or(COMBINED_MASKS, self.GREEN_MASK)
        # Adding Red to detect other Droids
        COMBINED_MASKS = cv.bitwise_or(COMBINED_MASKS, self.RED_MASK)
        
        return [COMBINED_MASKS, BLUE_MASK, YELLOW_MASK]

    def canny_edge(self, mask):
        """Detects edges"""
        return cv.Canny(mask, threshold1=self.cannyt1, threshold2=self.cannyt2)
        
    def find_contours(self,mask):
        # mask can be edge as well
        # cv2.RETR_EXTERNAL will focus on the outer shape of the track
        # for Contour Approximation Method
        # maybe use simple for now to save memory, but later on prototyping
        # we might need to approximate for more boundary points 
        # although a little computationally expensive for the raspberry pi
        """make sure that the versions of opencv does not mess with the returned tuple for contours. check again"""
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
        red_edges = self.canny_edge(self.RED_MASK)
        green_edges = self.canny_edge(self.GREEN_MASK)
        
        # Get Contours
        blue_contours = self.find_contours(blue_edges)
        yellow_contours = self.find_contours(yellow_edges)
        red_contours = self.find_contours(red_edges)
        self.green_contours = self.find_contours(green_edges)
    
        # Calculate the center of the track and return a tuple of (x,y)
        return self.calculate_center_line(blue_contours, yellow_contours)

    def calculate_wac(self, centers : list[tuple, tuple, tuple, tuple], weights : list) -> tuple[int, int]:
        # calculate weighted average center
        if centers and weights:
            sum_weighted_x = sum(l[0]* w for l, w in zip(centers, weights))
            sum_weighted_y = sum(l[1]* w for l, w in zip(centers, weights))
            avg_x = sum_weighted_x//sum(weights)
            avg_y = sum_weighted_y//sum(weights)
            return (avg_x, avg_y)
        return None, None
    
    def detect_track(self) -> tuple[int, int]:
        while True: 
            self.open_camera()
            ret, self.frame = self.camera.read()
            frame = self.frame
            if not ret:
                print("CAN'T EXTRACT FRAME! CRITICAL ISSUE!!")
                break
            
            combined, blue, yellow = self.colour_detection(frame)
            
            height, width, _ = frame.shape
            third_frame = (height//2) + (height//4)
            
            FUTURE_ROI1 = frame[:height//4,:]
            FUTURE_ROI = frame[height//4:height//2,:]
            NEXT_ROI = frame[height//2:third_frame,:]
            CURRENT_ROI = frame[third_frame:,:]
            ROI = [CURRENT_ROI, NEXT_ROI, FUTURE_ROI, FUTURE_ROI1]
            
            centers: list[tuple[int, int]] = [] # A list of centers for trial and optimization
            weights = [4,3,2,1]
            # find what reverse does
            # Get the centers of centroids
            # centers = [self.centroids_center(i) for i in ROI]
            for i in range(len(ROI)):
                center_x, center_y = self.centroids_center(ROI[i])
                if center_x != None and center_y != None:
                    centers.append((center_x, center_y))
            # print(centers)
            self.center_x, self.center_y = self.calculate_wac(centers, weights[:len(centers)])
            
            if self.center_x is not None and self.center_y is not None:
                for i in range(len(centers)):
                    cv.circle(CURRENT_ROI, centers[i], 5, (255, 0, 0), -1)
                cv.circle(CURRENT_ROI, (self.center_x, self.center_y), 5, (255, 0, 0), -1)
            # print((self.frame.shape[1]), self.center_x)
            # for debugging, if there is no tape for testing just have a dummy value for cx
            # print(self.frame.shape[0])
            # deviation = self.distance_to_turn(self.frame.shape[1], cx=self.center_x)

            cv.imshow('1. FUTURE_ROI1', FUTURE_ROI1)
            cv.imshow('2. FUTURE_ROI', FUTURE_ROI)
            cv.imshow('3. NEXT_ROI', NEXT_ROI)
            cv.imshow('4. CURRENT_ROI', CURRENT_ROI)
            cv.imshow("combined", combined)
            # print(self.purple_lower, self.purple_upper)
            # Check for the 'q' key press to exit the loop
            if cv.waitKey(1000 // self.FPS) == ord('q'):  # Adjust delay based on desired FPS
                break 
            
            return self.center_x, self.center_y
    
    def detect_green_line(self) -> bool:
        pass