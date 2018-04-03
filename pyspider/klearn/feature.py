#coding=utf-8
""" 
Created on Thu Mar 23 15:46:59 2017 
 
@author: onlyyo 
批量将切割后并且已经分好类的图像，得到的图片进行二值化处理，变成像素值，然后保存在TXT文件下 
"""  
from PIL import Image  
import numpy as np  
import os  
  
# 特征提取，获取图像二值化数学值  
def getBinaryPix(im):  
    im = Image.open(im)  
    im = im.convert('L')
    img = np.array(im)  
    rows = img.shape[0]
    cols = img.shape[1] 
    for i in range(rows):  
        for j in range(cols):  
            if (img[i,j]<= 128):                  
                img[i,j] = 0
            else:  
                img[i,j] = 1  
      
    binpix = np.ravel(img)  
    return binpix  
      
  
  
def getfiles(dirs):  
    fs = []  
    for fr in os.listdir(dirs):  
        f = dirs + fr  
        if f.rfind(u'.DS_Store') == -1:  
            fs.append(f)  
    return fs  
      
      
def writeFile(content):  
    with open(u'D:/Aptana Studio 3 Workspace/pytesser_v0.0.1/traindata/train_data.txt','a+') as f:  
        f.write(content)  
        f.write('\n')  
        f.close()  
          
  
if __name__ == '__main__':  
    dirs = u'D:/Aptana Studio 3 Workspace/pytesser_v0.0.1/category/%s/'  
      
    for i in range(10):  
        print i
        for f in getfiles(dirs %(i)):  
            pixs = getBinaryPix(f).tolist()  
            pixs.append(i)  
            pixs =  [str(i) for i in pixs]  
            content = ','.join(pixs)  
            writeFile(content) 