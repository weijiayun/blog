from __future__ import division
import cv,os

def reduce(id,imagepath,sizew,sizeh):
    iReduce = ""
    try:
        temppath = os.path.join('/home/weijiayun/PycharmProjects/blog/flaskr/', imagepath)
        dirname = os.path.dirname(imagepath)
        basename = os.path.basename(imagepath).split('.')[0]
        sufix = os.path.basename(imagepath).split('.')[1]
        path = os.path.join(dirname,basename + str(sizew) + '.' + sufix)
        print path
        if not os.path.exists(path):

            image = cv.LoadImage(temppath,1)
            m = sizew / image.width
            n = sizeh / image.height
            H = sizeh
            W = sizew
            size = (W, H)
            iReduce = cv.CreateImage(size, image.depth, image.nChannels)
            for i in range(H):
                for j in range(W):
                    x = int(i / m)
                    y = int(j / n)
                    iReduce[i, j] = image[x, y]
            if not os.path.exists(os.path.dirname(path)):
                os.mkdir(os.path.dirname(path))
            cv.SaveImage(path, iReduce)
        path = '/static/useravatar/' + str(id) + '/' + basename + str(sizew) + '.' + sufix
        return [path, iReduce]
    except:
        path = '/static/useravatar/lena.png'
        return [path,iReduce]




