from droid import Droid

class motor(Droid):
    def __init__(self, speed, camera_index=0, FPS=20, ROH=40, ROW=40, droid_status: bool=False, frame=None):
        super.__init__(self, camera_index, FPS, ROH, ROW, frame)
        self.speed = speed
        
    def move_foward(self, seconds=None): # Not implemented -> Last minute
        pass
    
    def turn_right(self, degree): # Not implemented -> Last minute
        pass
    
    def turn_left(self, degree): # Not implemented -> Last minute
        pass
    
    def reverse(self): # Not implemented -> Last minute
        pass
    
    def halt(self): # Not implemented -> Last minute
        pass
    
    def avoid_obstacle(self, droid: Droid): # Almost Done
        # get readings from ultrasonic sensor.
        # seconds is from the data of the sensor
        droid.recalibration_function()
        #only issue with this is that the centroid could be on the far siude of the other edge miscalculating the distance
        
        # IMPLEMENT BELOW
        # possibly distance between object and tape
        
        # droid.purple_centroid[0]
        degree = droid.map_boundboxdim2_framedim() 
        
        seconds = 0 # imaging getting this from the sensor thread.
        if (droid.purple_centroid[0] - droid.center_x) > 0:
            # and there is sufficient distance between the obstacle and the left tape
            # then go around the LEFT side of the object
            # degree is based off the distance
            self.halt()
            self.turn_left(degree)
            self.move_foward(seconds)
            self.turn_right(degree)
            self.move_foward(seconds)
        elif (droid.purple_centroid[0] - droid.center_x) < 0:
            # then go around the RIGHT side of the object
            self.halt()
            self.turn_right(degree)
            self.move_foward(seconds)
            self.turn_left(degree)
            self.move_foward(seconds)
    
    def directional_capabilities(self, droid: Droid, derivative: int, degree=60) -> None: # Almost Done
        """Not now, but i need to adjust the fps if the derivative is too high"""
        """This basically makes the droid go around a curvy track"""
        
        distance = droid.estimate_object_distance()
        # use this distance to fine tune the avoid_obstacle function
        avoid = True if droid.obstacle and droid.obstacle_area[0] * droid.obstacle_area[1] > droid.obstacle_area_thresh else False
        if avoid:
                self.avoid_obstacle()
        if derivative < 0:
            # we'll fine tune the degree here when we test it depending on how big the derivative is
            self.turn_right(degree)
            
        elif derivative > 0 :
            self.turn_left(degree)
        else:
            self.move_foward()
            
            
            
            
            
            