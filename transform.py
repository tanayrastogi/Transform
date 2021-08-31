import numpy as np 
import cv2 

class PerspectiveTransform:
    def __init__(self, polygon):
        """
        INPUT
            polygon(list):     The list of coordinate tuple. 
                                    The tuple has to have coordinates in order,
                                        *TopLeft, *TopRight, *BottomRight, *BottomLeft
        """
        # Generate Perpective Matrix
        self.__perspectiveMatrix(polygon)
        self.__check(polygon)

    @classmethod
    def __perspectiveMatrix(cls, polygon):
        """
        Function to generate the perpective transformation matrix.
        """
        # Original frame
        polygon = np.array(polygon, dtype="float32")
        (tl, tr, br, bl) = polygon
    
        # Width for the new frame
        widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
        widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
        maxWidth = max(int(widthA), int(widthB))
        # Height for the new frame
        heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
        heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
        maxHeight = max(int(heightA), int(heightB))
    
        # The destination frame
        dst = np.array([
            [0, 0],
            [maxWidth, 0],
            [maxWidth, maxHeight],
            [0, maxHeight]], dtype = "float32")
        
        # compute the perspective transform matrix and then apply it
        cls.perpectiveMatrix = cv2.getPerspectiveTransform(polygon, dst)
        cls.transformed_width  = maxWidth
        cls.transformed_height = maxHeight
    
    @classmethod
    def transform(cls, point):
        """
        Function to transform a point to the Polygon perspective

        INPUT
            point:  Point to be transformed in (X,Y)
        
        RETURN
            Return the point that is transformed to given polygon perspective.
        """
        pt = np.dot(cls.perpectiveMatrix, np.append(np.array(point), 1))
        return np.array((pt/pt[-1])[:2], dtype="int")

    
    @classmethod
    def __check(cls, polygon):
        (tl, tr, br, bl) = polygon
        if (cls.transform(tl) == np.array([0, 0])).all():
            pass
        else:
            print("Polygon: ", polygon)
            print("Transformed: ", [cls.transform(tl), cls.transform(tr), cls.transform(br), cls.transform(bl)])
            raise ValueError("Issue with Initializing polygon")

        if (cls.transform(br) == np.array([cls.transformed_width - 1,
                                      cls.transformed_height - 1])).all():
            pass
        else:
            print("Polygon: ", polygon)
            print("Transformed: ", [cls.transform(tl), cls.transform(tr), cls.transform(br), cls.transform(bl)])
            raise ValueError("Issue with Initializing polygon")


if __name__ == "__main__":
    # Dimensions of polygon to transform
    polygon = [(910, 558), (1073, 558), (1396, 1078), (511, 1078)]

    # Object
    pT = PerspectiveTransform(polygon)

    # Points to transform from one coordinate to destination coordinates
    print(pT.transform([910, 558]))
    