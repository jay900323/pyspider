#coding=utf-8
from PIL import Image,ImageEnhance  
from PIL import *  
import time  
import  os

# 图片切割  
def segment(im):  
    im_new = []  
    im1 = im.crop((10, 0, 65, 80))  
    im_new.append(im1)  
    im2 = im.crop((55, 0, 110, 80))  
    im_new.append(im2)  
    im3 = im.crop((98, 0, 153, 80))
    im_new.append(im3)  
    im4 = im.crop((142, 0, 197, 80))  
    im_new.append(im4)      
    return im_new  
  
def remove_single_point(im):
    height = im.size[1]
    width = im.size[0]
    pix = im.load()
    for y in xrange(0, height):
        for x in xrange(0, width):
            if y > 0 and  y < height - 1 and x > 0 and x < width - 1:
                r1 = im.getpixel((x, y-1))
                r2 = im.getpixel((x, y+1))
                r3 = im.getpixel((x, y))
                r4 = im.getpixel((x-1, y))
                r5 = im.getpixel((x+1, y+1))
                if r1 > 0 and r2 > 0 and r3 == 0 and r4 > 0 and r5 > 0:
                    pix[x, y] = 255
    return im

table = []    
threshold = 130 
table = []    
for i in range(256):    
    if i < threshold:    
        table.append(0)    
    else:    
        table.append(255)
        
# 图片预处理，二值化，图片增强  
def imgTransfer(f_name):  
    '''
    im = Image.open(f_name)  
    im = im.filter(ImageFilter.MedianFilter())  
    #enhancer = ImageEnhance.Contrast(im)  
    #im = enhancer.enhancer(1)  
    im = im.convert('L')  
    '''
    im = Image.open(f_name)
    im = im.convert('L')
    im = im.point(table, '1')
    pix = im.load()
    for x in xrange(0, im.size[0]):
        for y in range(0,5):
            pix[x, y] = 0xffffff
        for y in range(17, im.size[1]):
            pix[x,y] = 0xffffff
    im = remove_single_point(im)
    
    return im  
  
def rgba2rgb(r, g, b, a):
    #白色背景色
    BGcolur = 255
    R = BGcolur *(1-a/255 ) + r*a
    G = BGcolur *(1-a/255 ) + g*a
    B = BGcolur *(1-a/255 ) + b*a
    return (R, G, B)

def cutPictures(img):  
    #im = imgTransfer(img)
    im = Image.open(img)
    im = im.resize((220, 80), Image.NEAREST)
    pix = im.load()
    new_im = Image.new('RGB', im.size, (0,0,0))
    pix2 = new_im.load()
    for x in range(0, im.size[0]):
        for y in range(0, im.size[1]):
            r,g,b,a = pix[x,y]
            pix2[x, y] = rgba2rgb(r,g,b,a)
            
    pics = segment(new_im)  
    for pic in pics:  
        print int(time.time()*1000000)
        time.sleep(0.001)
        pic.save(u'D:\\Aptana Studio 3 Workspace\\pytesser_v0.0.1\\test\\%s.jpeg'%(int(time.time()*1000000)))

#读取文件夹下的所有图片
def getAllImages(folder):  
    imageList = os.listdir(folder)  
    imageList = [os.path.abspath(item) for item in imageList if os.path.isfile(os.path.join(folder, item))]  
    return imageList  

if __name__ == '__main__':
    files_name =  getAllImages(u'D:\\Aptana Studio 3 Workspace\\pytesser_v0.0.1\\klearn\\image\\')  
      
    for i in files_name:  
        files =  i.replace('\\','/')  
        s = files.split('/')  
        name = ''  
        for j in s[:-1]:  
            name = name + j + '/'  
        name = name + 'image/' + s[-1]           
            
        cutPictures(name)
        