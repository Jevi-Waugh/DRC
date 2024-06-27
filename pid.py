class PIDController:
    def __init__(self, kp, ki, kd):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.previous_error = 0
        self.integral = 0

    def compute(self, error):
        # Proportional term
        proportional = self.kp * error
        
        # Integral term
        self.integral += error
        integral = self.ki * self.integral
        
        # Derivative term
        derivative = self.kd * (error - self.previous_error)
        self.previous_error = error
        
        # Compute the output
        output = proportional + integral + derivative
        return output
