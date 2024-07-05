class PIDController:
    # Proportional–integral–derivative controller
    def __init__(self, kp, ki, kd):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.previous_error = 0
        self.integral = 0

    def compute(self, error):
        # Proportional term
        proportional = self.kp * error
        
        # Integrand
        self.integral += error
        integral = self.ki * self.integral
        
        # rate of change
        derivative = self.kd * (error - self.previous_error)
        self.previous_error = error
        return proportional + integral + derivative
        
