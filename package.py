#coding=utf-8

from distutils.core import setup  
import py2exe 
import glob

dll_excludes = [ "api-ms-win-core-string-l1-1-0",         
"api-ms-win-core-libraryloader-l1-2-1.dll",            
"api-ms-win-core-profile-l1-1-0.dll",            
"api-ms-win-core-processthreads-l1-1-2.dll",             
"api-ms-win-core-handle-l1-1-0.dll",
"api-ms-win-core-registry-l1-1-0.dll",
"api-ms-win-core-file-l1-2-1.dll",
"api-ms-win-core-heap-l1-2-0.dll",
"api-ms-win-core-version-l1-1-1.dll",
"api-ms-win-core-heap-l2-1-0.dll",
"api-ms-win-core-io-l1-1-1.dll",          
 "api-ms-win-core-localization-l1-3-1.dll",
 "api-ms-win-core-localization-obsolete-l1-3-0.dll",
 "api-ms-win-core-libraryloader-l1-2-0.dll",
 "api-ms-win-core-delayload-l1-1-1.dll",
"api-ms-win-core-sysinfo-l1-2-1.dll",
"api-ms-win-core-synch-l1-2-0.dll",
"api-ms-win-core-errorhandling-l1-1-1.dll",
"api-ms-win-core-version-l1-1-0.dll",
"api-ms-win-core-string-l2-1-0.dll",         
"api-ms-win-core-string-obsolete-l1-1-0.dll",
"api-ms-win-security-activedirectoryclient-l1-1-0.dll",
"api-ms-win-security-base-l1-2-0.dll",
"api-ms-win-eventing-provider-l1-1-0.dll",
"api-ms-win-core-com-l1-1-1.dll",
"api-ms-win-core-memory-l1-1-2.dll",
"api-ms-win-crt-string-l1-1-0.dll",
"api-ms-win-crt-runtime-l1-1-0.dll",
"api-ms-win-crt-stdio-l1-1-0.dll",
"MSVCR80.dll",
"mswsock.dll",
"powrprof.dll",
"libifcoremd.dll",
"libiomp5md.dll",
"libmmd.dll",
"pywintypes27.dll"]

#以下依赖包是egg格式 需要解压后才能打包
#如果是要将需要导入的包全部目录都打包则用packages
#如果是类似import导入依赖模块则用includes，不一定是包里面全部的文件
packages = ['chardet', 'robotparser', 'sqlalchemy', 'cssselect', 'singledispatch', 'backports_abc', 'mysql', 'pyspider.pytesser.pytesser']
includes = ['six.*', 'jinja2.*', 'flask.*', 'flask_login.*', 'SimpleXMLRPCServer']

options = {
    'py2exe':
        {
            'compressed': 1,   
            'optimize': 2,                        #压缩优化项
            "packages":packages,
            'includes':includes,
            'dll_excludes': dll_excludes,   # 排除w9xpopen这个win9x才需要的dll文件
            'bundle_files':3                     # 将生成的调用文件打包进exe文件
        }
}

data_files = [("Microsoft.VC90.CRT", glob.glob(r'D:\MyProject\PyInstaller-2.1\VC90\*.*')),
              ("data", [])]

'''
("", ['C:\Python27\Lib\site-packages\\numpy\core\libifcoremd.dll', 
                    'C:\Python27\Lib\site-packages\\numpy\core\libiomp5md.dll',
                    'C:\Python27\Lib\site-packages\\numpy\core\libmmd.dll'])
'''

setup(
      options=options,
      data_files = data_files,
      zipfile='Python27.zip',           # 将生成的library.zip打包进exe文件
      console=['run.py']
)
