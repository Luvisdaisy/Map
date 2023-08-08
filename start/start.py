'''
Author       : Tian Haotian qi_7ran@163.com
Date         : 2023-05-04 14:31:51
LastEditors  : Tian Haotian qi_7ran@163.com
LastEditTime : 2023-05-04 15:17:20
FilePath     : \VSCodePros\Covid_19_Project\start\start.py
Description  : 
'''
import os
import webbrowser
from http.server import HTTPServer, SimpleHTTPRequestHandler

PORT = 8888
DIRECTORY = 'E:\\ProSpace\\VSCodePros\\Covid_19_Project\\html'  
HTML_FILE = 'index.html' 

os.chdir(DIRECTORY)

httpd = HTTPServer(('localhost', PORT), SimpleHTTPRequestHandler)
print(f'Serving HTTP on http://localhost:{PORT}...')

webbrowser.open(f'http://localhost:{PORT}/{HTML_FILE}')

httpd.serve_forever()
