#coding=utf-8
import os  
from cross_svc import cross_validation  
from PIL import Image,ImageEnhance  
from PIL import * 
from cut import *
from feature import *

def cutPictures2(name):  
    im = Image.open(name)
    im = im.resize((220, 80), Image.NEAREST)
    pix = im.load()
    new_im = Image.new('RGB', im.size, (0,0,0))
    pix2 = new_im.load()
    for x in range(0, im.size[0]):
        for y in range(0, im.size[1]):
            r,g,b,a = pix[x,y]
            pix2[x, y] = rgba2rgb(r,g,b,a)
            
    pics = segment(new_im)  

    pics[0].save(u'D:/Aptana Studio 3 Workspace/pytesser_v0.0.1/test_picture/1.jpeg')
    pics[1].save(u'D:/Aptana Studio 3 Workspace/pytesser_v0.0.1/test_picture/2.jpeg')
    pics[2].save(u'D:/Aptana Studio 3 Workspace/pytesser_v0.0.1/test_picture/3.jpeg')
    pics[3].save(u'D:/Aptana Studio 3 Workspace/pytesser_v0.0.1/test_picture/4.jpeg')  
  
def load_Predict(name):  
#  
    cutPictures2(name)      #切割图片  
    
    dirs = u'D:/Aptana Studio 3 Workspace/pytesser_v0.0.1/test_picture/'  
    fs = os.listdir(dirs)    # 获取图片名称  
    clf = cross_validation()    
    predictValue = []  
      
    for fname in fs:  
        fn = dirs + fname  
        binpix = getBinaryPix(fn)         
        predictValue.append(clf.predict(binpix))  
          
    predictValue = [str(int(i)) for i in predictValue]  
    print "the picture number is :" ,"".join(predictValue)  


import urllib2
name ='verifyCode111.png' 
r = urllib2.Request('http://lljiuzhu.mca.gov.cn:8090/insiis6/verifyCode')
res = urllib2.urlopen(r)
content = res.read()
f = open(name, 'wb')
f.write(content)
f.close()

load_Predict(name)