import numpy as np
from scipy.spatial.transform import Rotation
from git.femlab1.src.path import Path
class Polygon:
    def __init__(self,origin,order,direction: str,sidelength) -> None:
        if direction not in ["Left","Right","left","right","l","r"]: 
            raise ValueError("direction has to be left or right")
        self.origin = np.reshape(origin,(2,1))
        self.order = order
        self.direction = direction
        self.sidelength = sidelength

    @property
    def corner_angle(self):
        return 360/self.order
    @property
    def corners(self):
        side = np.reshape(np.array((self.sidelength,0)),(2,1))
        corners = [self.origin,]
        for i in range(self.order):
            beta = i*self.corner_angle%360
            total_angle = ((beta) + (self.corner_angle))
            total_angle = np.deg2rad(total_angle)
            rot = np.array(((np.cos(total_angle),-np.sin(total_angle)),(np.sin(total_angle),np.cos(total_angle)))).reshape((2,2))
            new_corner = rot@side + corners[i]
            corners.append(new_corner)
        return np.concatenate(corners,1)    
if __name__ == "__main__":
    hexagon = Polygon(origin=(0, 0), order=100, direction="left", sidelength=1)

    path = Path(hexagon.corners[0,:],hexagon.corners[1,:],1)
    path.plot()
