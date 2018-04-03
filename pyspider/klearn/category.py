#coding=utf-8
""" 
Created on Thu Mar 23 14:19:13 2017 
对切割后的图片进行分类，及0-9 
 
@author: onlyyo 
"""  
  
import sys  
sys.path.append('C:\Users\onlyyo\Desktop\pytesseract-0.1.6\src')  
sys.path.append('C:\Python27\Lib\site-packages\pytesser')  
from pytesseract import *  
import pytesseract  
from PIL import Image  
import os  
import shutil  
  
  
#ocr图像识别  
def ocr(img):  
    try:  
        img = Image.open(img)
        rs = image_to_string(img)  
    except:  
        return 'none'  
    return rs  
      
  
#使用ocr进行训练的预分类  
def category(originfile,dirs,filename):  
    print dirs
    if not os.path.exists(dirs):  
        os.makedirs(dirs)  
    shutil.copyfile(originfile,dirs+filename)  
      
      
if __name__ == '__main__':  
    dirs = u'D:/Aptana Studio 3 Workspace/pytesser_v0.0.1/test/'  
      
    # 将ocr识别的文件按照数组编号存放在相应的文件夹中  
    for fr in os.listdir(dirs):  
        f = dirs+fr  
        if f.rfind(u'.DS_Store') == -1:  
            rs = ocr(f)  
              
            if '|' not in rs and '*' not in rs :  
                if '?' not in rs and '<'not in rs and '>' not in rs:
                    category(f,u'D:/Aptana Studio 3 Workspace/pytesser_v0.0.1/category/%s/'%rs,fr)