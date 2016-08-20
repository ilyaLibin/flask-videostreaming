import cv2
  
class AFourDetector:

    __init__(self, image, minListW=700, minListH=495)
        self.image = image
        self.minListW = minListW
        self.minListH = minListH

    def detect(self):
        return self.detect_list()

    def detect_list(self:
        # initialize the rectangular and square kernels to be applied to the image,
        # then initialize the list of license plate regions
        rectKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (13, 9))
        squareKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        regions = []
