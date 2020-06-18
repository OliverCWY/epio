from flask import Flask,Response
from flask_cors import CORS
import os
import builtins
app=Flask(__name__)
builtins.app = app
CORS(app,resorces={r'/*': {"origins": '*'}})
def apiText(lines,length=40):
    text=""
    for line in lines:
        last=length
        for arg in line:
            text+=" "*(length-last)+arg
            last=len(arg)
        text+="\n"
    return Response(text,content_type="text/plain; charset=utf-8")
@app.route('/')
def index():
    return apiText([
        ['通用接口:'],
        ["/bilibili","bilibili音频解析"],
        ['/qyk','人工智能回复（青云客接口）'],
        ['/cors','通过python下载网页内容'],
        ['/bullshit','狗屁不通'],
        ['/qr',"二维码生成"]
    ])
from plugins import *
if __name__=="__main__":
    app.run(debug=True)
