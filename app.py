from flask import Flask,redirect,Response
from flask_cors import cross_origin
import requests
app = Flask(__name__)

cache={}
imgs={}

def Repo(path):
    r=requests.get("https://"+f"api.github.com/repos/i75ppa9/epio/contents/1/{path}".replace("//","/"))
    return r.json()
def File(path):
    r=requests.get("https://"+f"raw.githubusercontent.com/i75ppa9/epio/master/1/{path}".replace("//","/"))
    return r.text
@app.route('/')
@app.route('/<string:jiname>/')
@app.route('/<string:jiname>/<string:albumName>')
@app.route('/<string:jiname>/<string:albumName>/<int:picNumber>')
def view(jiname=None,albumName=None,picNumber=None):
    if(not jiname):
        if('' not in cache):
            j=Repo("")
            files=[]
            for file in j:
                files.append(file["name"])
            cache[""]=files
        files=cache[""]
        return "<br>".join([f'<a href="/{name}">{name}</a>' for name in files])
    elif(not albumName):
        if(jiname not in cache):
            j=Repo(jiname)
            albums=[]
            for album in j:
                albums.append(album["name"][:-4])
            cache[jiname]=albums
        albums=cache[jiname]
        return "<br>".join([f'<a href="/{jiname}/{name}">{name}</a>' for name in albums])
    elif(not picNumber):
        if(albumName not in imgs):
            pics=File(f'{jiname}/{albumName}.txt').split('\n')
            imgs[albumName]=pics
        pics=imgs[albumName]
        return "<br>".join([f'<img src="/{jiname}/{albumName}/{i+1}" style="width:100%;height:auto">' for i in range(len(pics))])
    else:
        if(albumName not in imgs):
            pics=File(f'{jiname}/{albumName}.txt').split('\n')
            imgs[albumName]=pics
        pics=imgs[albumName]
        url=pics[picNumber-1]
        r=requests.get(url,stream=True)
        return Response(r.iter_content(chunk_size=1024*10),
                        content_type=r.headers['Content-Type'])
if __name__ == '__main__':
   app.run(debug=True)
