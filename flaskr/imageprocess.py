
import cv,os

def reduce(id,imagepath,sizew,sizeh):
    iReduce = ""
    try:
        dirname = os.path.dirname(imagepath)
        basename = os.path.basename(imagepath).split('.')[0]
        version = os.path.basename(imagepath).split('.')[1]
        sufix = os.path.basename(imagepath).split('.')[2]
        path = os.path.join(dirname,basename +'.'+str(sizew) + '.'+version+'.' + sufix)
        if not os.path.exists(path):
            image = cv.LoadImage(imagepath,1)
            H = sizeh
            W = sizew
            size = (H, W)
            iReduce = cv.CreateImage(size, image.depth, image.nChannels)
            for i in range(H):
                x1 = int(i*image.height/sizeh)
                x2 = int((i+1)*image.height/sizeh)
                for j in range(W):
                    y1 = int(j * image.width / sizew)
                    y2 = int((j+1) * image.width / sizew)
                    sum = [0,0,0]
                    for k in range(x1,x2):
                        for l in range(y1,y2):
                            sum[0] += image[k,l][0]#pix value
                            sum[1] += image[k,l][1]#depth
                            sum[2] += image[k,l][2]#channels
                    num = (x2-x1)*(y2-y1)
                    iReduce[i,j] = (sum[0]/num,sum[1]/num,sum[2]/num)
            if not os.path.exists(os.path.dirname(path)):
                os.mkdir(os.path.dirname(path))
            cv.SaveImage(path, iReduce)
        path = '/static/useravatar/' + str(id) + '/' + basename +'.'+ str(sizew) + '.'+version+'.' + sufix
        return [path, iReduce]
    except:
        path = '/static/useravatar/lena.png'
        return [path,iReduce]




