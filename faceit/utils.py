
import numpy as np
import math

# taken from http://www.paulvangent.com/2016/08/05/emotion-recognition-using-facial-landmarks/
def get_meanPoint(shape):
    xlist = []
    ylist = []
    for i in range(0,67): #Store X and Y coordinates in two lists
        xlist.append(float(shape.part(i).x))
        ylist.append(float(shape.part(i).y))
    xmean = np.mean(xlist) #Find both coordinates of centre of gravity
    ymean = np.mean(ylist)
    xcentral = [(x-xmean) for x in xlist] #Calculate distance centre <-> other points in both axes
    ycentral = [(y-ymean) for y in ylist]
    
    landmarks_vectorised = []
    for x, y, w, z in zip(xcentral, ycentral, xlist, ylist):
        landmarks_vectorised.append(w)
        landmarks_vectorised.append(z)
        meannp = np.asarray((ymean,xmean))
        coornp = np.asarray((z,w))
        dist = np.linalg.norm(coornp-meannp)
        landmarks_vectorised.append(dist)
        landmarks_vectorised.append((math.atan2(y, x)*360)/(2*math.pi))
    mean = (int(xmean),int(ymean))
    return (mean,landmarks_vectorised)
    


    