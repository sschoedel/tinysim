import numpy as np

class DefaultController():
    def __init__(self, nq, nv, nu):
        self.nq = nq
        self.nv = nv
        self.nu = nu
        
    def get_joint_control_inputs(self):
        return np.zeros(self.nu)
    