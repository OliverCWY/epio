import base64
import urllib.request as request
from flask import Flask,Response
import lzma,json,string
from pypinyin import lazy_pinyin
from flask_cors import CORS
loading_img="data:image/gif;base64,"+base64.b64encode(request.urlopen("https://www.coursehero.com/assets/img/books/loading.gif").read()).decode()
js="""
    new Vue({
      el: '#app',
      vuetify: new Vuetify(),
      data:()=>data
    })
"""
css="""
.v-card{
  max-width:600px;
  width:100%;
}
.v-list-item a{
  text-decoration:none;
  overflow:hidden;text-overflow:ellipsis;white-space:nowrap;
  width:100%
}
.container .v-img{
  width:100%;
  height:auto;
}
"""
html='''
    <v-app><v-card class="mx-auto" elevation="10">
      <v-breadcrumbs :items="path" large></v-breadcrumbs>
      <v-row no-gutters v-if="kind=='list'">
        <v-col disabled cols=1 v-if="index!=null"><v-list dense>
          <v-list-item v-for="item in index">
            {{item}}
          </v-list-item>
        </v-list></v-col>
        <v-col :cols="index!=null?11:12"><v-list dense>
          <v-list-item v-for="item in data_main" ripple>
            <a style="color:black" :href="item">{{item}}</a>
          </v-list-item>
        </v-list></v-col>
      </v-row>
      <v-container v-if="kind=='images'">
        <v-lazy v-for="item in data_main" style="min-height:360px">
          <v-img :lazy-src="loading_img" :src="item">
        </v-lazy>
      </v-container>
    </v-card></v-app>
'''
def renderHTML(data):
  title=data["path"][-1] if len(data["path"])>0 else "首页"
  path=[dict(text="首页",href="/",disabled=False)]
  if data["kind"]=="images":data["loading_img"]=loading_img
  p="/"
  for item in data["path"]:
    p+=item
    path.append(dict(text=item,href=p,disabled=False))
  path[-1]["disabled"]=True
  data["path"]=path
  return '''
<html>
<head>
  <title>{4}</title>
  <link href="https://fonts.googleapis.com/css?family=Roboto:100,300,400,500,700,900" rel="stylesheet">
  <link href="https://cdn.jsdelivr.net/npm/@mdi/font@5.x/css/materialdesignicons.min.css" rel="stylesheet">
  <link href="https://cdn.jsdelivr.net/npm/vuetify@2.x/dist/vuetify.min.css" rel="stylesheet">
  <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no, minimal-ui">
  <style>{3}</style>
</head>
<body><br>
  <div id="app" style="display:none">
    {0}
  </div><br>
  <script src="https://cdn.jsdelivr.net/npm/vue@2.x/dist/vue.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/vuetify@2.x/dist/vuetify.js"></script>
  <script>
    data={1};
    if(data.index==undefined)data.index=null;
    {2}
    document.getElementById("app").style="";
  </script>
</body>
</html>
'''.format(html,json.dumps(data,ensure_ascii=False),js,css,title)
app = Flask(__name__)
images=json.loads(lzma.decompress(request.urlopen("https://github.com/i75ppa9/epio/raw/master/data.jsx").read()))["images"]
jis=list(images.keys())
def key(word):
  py=[[string.upper() for string in item] for item in lazy_pinyin(word)]
  for i in range(len(py)):
    if py[i][0][0] not in string.digits+string.ascii_uppercase:py[i][0]="#"+py[i][0]
  return py
jis.sort(key=key)
index=[]
_tmp=set()
for ji in jis:
  start=lazy_pinyin(ji)[0][0].upper()
  if start not in string.digits+string.ascii_uppercase:start="#"
  if start in _tmp:index.append("")
  else:
    _tmp.add(start)
    index.append(start)
@app.route("/")
def main():return renderHTML(data=dict(path=[],kind="list",data_main=[name for name in jis],index=index))
@app.route("/favicon.ico")
def icon():return Response(b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x01\x90\x00\x00\x01\x90\x08\x03\x00\x00\x00\xb7a\xc6\xfe\x00\x00\x02.PLTELiqA\xb8\x83A\xb8\x83<zr?\x9e|A\xb8\x83A\xb8\x83A\xb8\x83<zrA\xb8\x83<zrA\xb8\x83A\xb8\x83A\xb8\x83<zrA\xb8\x83<zrA\xb8\x83A\xb8\x83;yqA\xb8\x83A\xb8\x83<yqA\xb8\x83A\xb8\x83<xqA\xb8\x83<yqA\xb8\x83<xpA\xb8\x83<xpA\xb8\x83<wpA\xb8\x83A\xb8\x83<wpA\xb8\x83A\xb8\x83A\xb8\x83<vpA\xb8\x83A\xb8\x83<vpA\xb8\x83A\xb8\x83;upA\xb8\x83A\xb8\x83<toA\xb8\x83A\xb8\x83<toA\xb8\x83<toA\xb8\x83A\xb8\x83<soA\xb8\x83A\xb8\x83;rnA\xb8\x83A\xb8\x83;qnA\xb8\x83;qoA\xb8\x83A\xb8\x83A\xb8\x83;qnA\xb8\x83A\xb8\x83A\xb8\x83;omA\xb8\x83A\xb8\x83:omA\xb8\x83;nmA\xb8\x83A\xb8\x83;mmA\xb8\x83A\xb8\x83:llA\xb8\x83A\xb8\x83:klA\xb8\x83:klA\xb8\x83A\xb8\x83:jlA\xb8\x83:ikA\xb8\x83A\xb8\x83:hjA\xb8\x83A\xb8\x83:fjA\xb8\x83A\xb8\x839diA\xb8\x839ciA\xb8\x83A\xb8\x839ahA\xb8\x83A\xb8\x839`gA\xb8\x838^gA\xb8\x83A\xb8\x838\\fA\xb8\x83A\xb8\x838ZeA\xb8\x837XdA\xb8\x837WdA\xb8\x83A\xb8\x837TcA\xb8\x836Rb6PaA\xb8\x835M`5I^5J^5K^5L_5M`6O`6Qa6Sb7Uc7Xd8[e8^g9`g9ah9di:fj:gj:hj:kl;mm;nm;pn<so;vp;xp<zr<|r=~s<\x81s=\x83t=\x86u=\x89v>\x8bw>\x8cw>\x8fx>\x91y>\x94z?\x97z?\x99{>\x9b{?\x9e|?\xa0}?\xa3}@\xa6~A\xa8~@\xaa\x7fA\xac\x7fA\xae\x80A\xaf\x80B\xb1\x80A\xb3\x81A\xb6\x82B\xb7\x82A\xb8\x83\xfb\x98vh\x00\x00\x00\x84tRNS\x00\x01\x02\x02\x03\x04\x07\x08\x08\x0b\r\x0e\x10\x12\x12\x15\x16\x17\x1a\x1a\x1e!"%(*+,/13478:>?@DEFHKMPSVWZ]^bbfgimopuwx||\x80\x81\x83\x84\x87\x89\x8a\x8f\x92\x93\x96\x99\x9b\x9d\x9f\xa1\xa5\xa6\xa8\xac\xae\xb0\xb4\xb5\xb7\xb9\xba\xbb\xbc\xbf\xc0\xc2\xc7\xc7\xcc\xcf\xd0\xd3\xd6\xd6\xda\xdc\xde\xe2\xe2\xe4\xe6\xe7\xea\xea\xed\xef\xef\xf2\xf3\xf4\xf6\xf6\xf7\xf8\xfa\xfb\xfb\xfc\xfd\xfd\xfe\xfe\xcb\xe7&\'\x00\x00\nxIDATx\xda\xec\xc1\x81\x00\x00\x00\x00\xc3\xa0\xfbS\x1fd\xd5\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xc8:5\xf7\xa0^k\xba\x05Q\xb8\xb6m\xdb\xb6m\xdb\xb6m[3v\xce\xb6m{^\xddi\xbb\x93\xa5\x91\xf4\xf7\xbf\xb71\x9e\xaau\xce*4HZ/\x95\x99^i\x06)\xfc\xee\xa8uj}\xd1Q\xaf\xd3\x0crXe\xe6\xb0A\xd2^;\xeabki\x96\xb3n\x18e\x8a\xca\xc8\x14\xa3\xdcp\xd6,I\xf5\x0e9\xeaC\x96A\xce\xd6T\x99\xa8y\xd6 Y\x1f\x1cu\xa8\x9e$\x8dt\xd6\x03\xa3\xacP\x99Xa\x94\xfb\xce\x1a\xa9\x9fT\xd9\xea\xa8oy\x06\xb9\xd4F\xe2\xb5\xb9d\x90\xbco\x8e\xdaZE?\xeb\xe1\xac\xe7F\xd9!\xf1v\x18\xe5\xb9\xb3z\xe8WK\x9d\xf5?\xa3\x0c\x16n\xb0Q\x8a\x9d\xb5T\xbfiv\xdaQo\xd3\rr\xac\x92`\x95\x8e\x19$\xfd\xad\xa3N7\xd3\xef\xa6:\xeb\x96Qf\x0b6\xdb(\xb7\x9c5U\x7f\xa8\xb5\xdfQ\x9fs\x0cr\xbe\x91P\x8d\xce\x1b$\xfb\xb3\xa3\xf6\xd7\xd2\x9f\x0cr\xd6#\xa3l\x10j\x83Q\x1e9k\x90\xfe\xac\xe2FG}\xcb7HFg\x81:g\x18$\xff\x9b\xa36V\xd4_tt\xd6K\xa3\xec\x13h\x9fQ^:\xab\xa3\xfef\xbe\xb3\xae\x1ae\xb40\xa3\x8dr\xd5Y\xf3\xf5w\r\x8f;\xea}\xa6ANU\x17\xa4\xfa)\x83d\xbew\xd4\xf1\x86\xfa\x87\xb1\xce\xbak\x94\xc5\x82,6\xca]g\x8d\xd5?U\xdb\xe9\xa8\xaf\xb9\x06\xc9j*D\xd3,\x83\xe4~q\xd4\xcej\xfa\x17}\x9c\xf5\xd4(\xdb\x84\xd8f\x94\xa7\xce\xea\xa3\x7f\xb5\xc6YE\x06I\xeb+@\xdf4\x83\x149k\x8d\xfe]\xebs\x8ez\x13V\xcd\r\xb6\xdb\x9ek\xad\x12\xcc\x8c~\xcd\x8db\xb7\x9d\xa9\x92\xd4\x81k\xeeG\xae\xe6\xd6U\x8a\xear\xdd\xf6#\xdcm\xeb\xa8D\xc3\x83\xad\xb9\xab\x95\xa2\xd5Fy\xe0\xac\xe1*Y\xb857\xb3\x9dR\xd2.3\xd4n\xbb\xa5\x8aJ\xd1-\xd8\x9a\xbb[)\xd9\x1dl\xb7\xed\xaaR-q\xd6e\xa3\x0cU\n\x86\x1a\xe5\xb2\xb3\x96\xa8tM\xe0\x9a\xfb.\xc3 \'\xaa(iUN\x18$\xe3\x1d\xdcm\x9b(\x86\xc9\xce\xbam\x94\xb9J\xda\\\xa3\xdcv\xd6d\xc5Rk/\\s\xb3\rr\xa1\x91\x92\xd4\xe8B\xa8\xddvo\r\xc540:57\xfa\xddv\xa0b\xab\xb0\xdeQ\xdf\x0b\x0c\x92\xde]I\xe9\x9en\x90\x82\xef\x8eZ_Aqh\xef\xacWF9\xa0\xa4\x1c0\xca+g\xb5W\\\xe69\xeb\x9aQ\xc6)\t\xe3\x8cr\xcdY\xf3\x14\x9f\x86G\x03\x18(\x005\x97\xee\xb6Yp\xb7=\xdaPq\x1a\xe3\xac{|\xcd\xfd/\xba\xed=g\x8dQ\xbc\xaa\x86[s[(A-\xb8n\xfb\x15\xee\xb6U\x15\xb7\xde\xcez\xc6\xd7\xdc\xe8w\xdb\xdeJ\xc0*g\x15\xf35\xb7\xbc\xbbm\xb1\xb3V*\x11-\xc3\xad\xb9\x95\x94\x80J\\\xb7}\x03w\xdb\x96J\xc8tg\xdd4\xca\x0c%`\x86Qn:k\xba\x12S\xe7\xa0\xa3>e\x1b\xe4|]\xc5\xad.7>\xf8\xe4\xa8\x83u\x94\xa0a\xc1\xd6\xdc\xb5\x8a\xdb\xda`\xbb\xed0%\xaa\xca\x96`\x07\n\x1d\x14\xa7\x0e\xc1\x8e\x0f\xb6TV\xc2\xba8\xebE\xf9\xd7\xdc\xddFy\xe1\xac.J\xc2"g]1\xca\x08\xc5e\x84Q\xae8k\x91\x92\xd1\xe4d\xb4kn\xb8\xdd\xf6d\x13%e\x92\xb3\xee\x18e\x81\xe2\xb0 \xd8n;Q\xc9\xa9\xb1\xc7Q_r\xb0\x9a\xdbT15\xc5\xbam\xce\x17G\xed\xa9\xa1$\xf5w\xd6c\xa3lVL\x9b\x8d\xf2\xd8Y\xfd\x95\xb8\xe0kn/\xc5\xd0+\xe4n\x9b\xb4\xb6\xc1\xde\xcd\x1d(\xb7n\x9b\x06w\xdb\x8bm\x95\x829\xce\xban\x94\t*\xd5\x04\xa3\\w\xd6\x1c\xa5\xa2\xc1\x91h\xde\xcd\x85{\x1aw\xa4\x81R2\xcaY\xf7\x8d\xb2L\xa5X\x16l\xb7\x1d\xa5\xd4T\xdd\x0e\xd7\xdc<\x83d\xb5R\x89Ze\x19$\x0f\xee\xb6\xdb\xab*E=\x83\xad\xb9;\xca\xe34\xee\x99\xb3z*e\xcb\x83\xad\xb9\x03T\x82\x01\xc1v\xdb\xe5J]\xf33Q\xbb\x9b\x0b\xf74\xeeLs\x01\xa6\x05{77#j\xddv\x9a\x08\xb5\xf7\x07[s\xeb\xeb_\xd4\x0f\xb6\xdb\xee\xaf%\xc4\x10g=,\xdb\x81\xc2\x06\xa3<t\xd6\x101*n\x8a\xd2\xdd\\\xb8\xa7q\x9b*\n\xd2)Jws\xbb\x83=\x8d\xeb$\xcc\xc2`\xef\xe6FD\xa7\xdb.\x14\xa7\xf1q\xba\xe6\xd2\x03\x05~|@w\xdb\xe3\x8d\x05\x1a\x1f~\xcd\xa5\xbb\xed\x1dg\x8d\x17\xa9\xda.G}\x81\xef\xe6\xc2?\x8d\xdbUM\xa8~\xcez\xc2\xd7\\\xb6\xdb>qV?\xb1~`\xef\x0e0\x02\x81\x02(\x8a\x1a\x00\xb3\xee\xc1\x10\x02!\x92 \x10\x04\xd1\xee\xda\xc4\xc3\xf9\xdd\x7f\xb7\xf1x\xe7\x0f\x8e\x87\xf9\xd8\xd78\x1e\x0f\xf3\xb1\xafm<\x1e\xe6c_\xdb|<\xcc\xc7\xbe\xa6\xf9x\x98\x8f}m\xf3\xf10\x1f\xfb\x9a\xe6\xe3a>\xf6\xb5\xcc\xc7\xc3|\xeck\x99\x8f\x87\xf9\xd8\xd74\x1f\x0f;\x03\xfbZ7\xc7\xc3vk\xae\x8f}M\xf3\xf10\x1f\xfb\x9a\xe6\xe3a>\xf6\xb5\xcd\xc7\xc3|\xeck\x9b\x8f\x87\xf9\xd8\xd74\x1f\x0f\xf3\xb1\xafm>\x1e\xe6c_\xd3|<\xcc\xc7\xbe\xb6\xf9x\x98\x8f}M\xf3\xf10\x1f\xfb\xda\xe6\xe3a>\xf6\xb5\xcd\xc7\xc3|\xeck\x9a\x8f\x87\xf9\xd8\xd76\x1f\x0f\xf3\xb1\xaf\xc0\x9a\xdb\xdam}<\xcc\xc7\xbe\xf6\xf9x\x98\x8f}\xed\xf3\xf10\x1f\xfb\x9a\xe5\xe3a>\xf65\xc8\xc7\xc3X\xeck\xbf\xdb\x1e\x8c\x87\xf9\xd8\xd7>\xfan\xce?\x8d\xdb\xe6\xe3a>\xf6\xb5\xcd\xc7\xc3|\xeck\x9a\x8f\x87\xf9\xd8\xd76\x1f\x0f\xf3\xb1\xafi>\x1e\xe6c_\xdb|<\xcc\xc7\xbe\xa6\xf9x\x98\x8f}m\xf3\xf10\x1f\xfb\xda\xe6\xe3a>\xf65\xca\xc7\xc3|\xeck\x90\x8f\x87\xf9\xd8\xd7 \x1f\x0f\xf3\xb1\xafA>\x1e\x06c_@\x00\x1e\xe6`_@\x00\x1e\x06a_@\x00\x1e\xe6`_@\x00\x1e\x06a_@\x00\x1e\x86c_w\xcd\r\xec\xb6\x12\x1e\x06c_@\x00\x1e\xe6`_@\x00\x1e\x06a_@\x00\x1e\xe6`_@\x00\x1e\x06a_@\x00\x1e\xe6`_@\x00\x1e\xe6`_@\x00\x1e\x06a_@\x00\x1e\xe6`_@\x00\x1e\x06a_@\x00\x1e\xe6`_@\x00\x1e\x06a_@\x00\x1e\xe6`_@\x00\x1e\xe6`_@\x00\x1e\x06a_@\x00\x1e\xe6`_@\x00\x1e\x06a_@\x00\x1e\xa6c_\x83|<l\xd0\xe37\x8e}\x85\xf0\xb03\xb0\xaf\x12\x1ev\x02\xf6\x95\xc2\xc3N\xc1\xbe|<l\xd6\x1b\x85}\xdd\xbb9\xff4\xae\x85\x87\xf9\xd8W\x0b\x0f\xf3\xb1\xaf\x18\x1e\xe6c_-<\xcc\xc7\xbebx\x98\x8f}\xb5\xf00\x1f\xfb\x8a\xe1a>\xf6\xd5\xc2\xc3|\xec\xab\x85\x87\xf9\xd8W\x0c\x0f\xf3\xb1\xaf\x16\x1e\xe6c_1<\xec\xe1\xcb\xc7\xbeRx\x98\x8f}\xb5\xf00\x1f\xfbj\xe1a>\xf6\x15\xc3\xc3|\xec\xab\x85\x87\xf9\xd8W\x00\x0fC\xb0\xaf\xbb\xe6\xde\xdd\xd6\xc7\xc3|\xec\xab\x85\x87\xf9\xd8W\x0b\x0f\xf3\xb1\xaf\x18\x1e\xe6c_-<\xcc\xc7\xbe\x02x\x98\x8b}\xdd\xbb9\xff4.\x86\x87\xf9\xd8W\x0b\x0f\xf3\xb1\xaf\x16\x1e\xf6\xff\xd3\xc7\xbeRx\x98\x8f}\xb5\xf00\x1f\xfb\xfa=x\xd8{\x0e\xfb\xf2\xf1\xb0\x18\xf6\xe5\xe3a5\xec\xcb\xc7\xc3b\xd8\x97\x8f\x87\xd5\xb0/\x1f\x0f\x8ba_>\x1eV\xc3\xbe|<\xac\x86}\xf9xX\x0c\xfb\xf2\xf1\xb0\xf3\xb1\xaf\x08\x1e\xf6\xe2c_\x01<,\x80}\xf9x\x98\x86}\xdd5\xf7\xee\xb6>\x1e\xf6\xef\xc3\xc7\xbeRx\x98\x8f}e\xf0\xb0\x00\xf6\xe5\xe3a\xaf5\xec\xcb\xc7\xc3j\xd8\x97\x8f\x87\xd5\xb0/\x1f\x0f\x8ba_>\x1e\xd6\xc2\xbe|<\xec\xd9\xc6\xbe\xfc\xfe\xee\xf1\xb0\x18\xf6\xe5\xe3a1\xec\xcb\xc7\xc3b\xd8\x97\x8f\x87\x1d\x88}\x05\xf0\xb0\'\x1f\xfbJ\xe1a>\xf6\x15\xc3\xc3|\xec\xab\x85\x87\xf9\xd8W\x0c\x0f\xc3\xb1/\xbf5\x1e\xe6c_1<\xcc\xc7\xbejx\x98\x8f}\xc5\xf00\x1f\xfb*\xe1a\x18\xf6u\xef\xe6\xeei\x9c\x88\x87\xf9\xd8W\r\x0f\xf3\xb1\xaf\x18\x1e\xe6c_\r<\x0c\xc3\xbe\xee\x9a{w[\x17\x0f\xf3\xb1\xaf\x18\x1e\xe6c_5<\xcc\xc7\xbeJx\x98\x8f}\x05\xf0\xb0\x9f\xf6\xee\xe9J\x12\x00\x00\xa2\xe8*\x8f\xb5m\x8dm\x9bqvv\x93D\xe3}\xdc\x97F\x9dS\x17\xf6\xd5\xc2\xc3`_1<\x0c\xf6\xd5\xc2\xc3`_-<\x0c\xf6\x15\xc3\xc3`_-<\x0c\xf6\x15\xc3\xc3`_Q<\x0c\xf6\x95^s\xed\xb6C\xe8\xd5`\x08\xc5\xb0/xX\x0b\xfb\x82\x87\xc5\xb0/xX\x0b\xfb\x82\x87\xc5\xb0/xX\x00\xfbr7\xe74\xae\x82\x87\xc1\xbeZx\x18\xec+\x86\x87\xc1\xbeZx\x18\xec+\x89\x87\xf5\xb1/x\x18\xeck\xd8]\x0c\x86P\x00\xfb\x82\x87\xc1\xbe\x02x\x18\xec\xab\x86\x87\xf5\xb1/x\x18\xeck\xd8=\x1a\x02\x1e\x16\xc0\xbe\xe0a\xb0\xaf\x06\x1e\xd6\xc7\xbe\xe0a\xb0\xafa\xb70\x18B\x01\xec\x0b\x1e\x16\xc0\xbe\xe0a\xb0\xaf\xc0\x9ak\xb7m\xe0a\xb0\xaf\x16\x1e\x06\xfb\x8a\xe1a\xb0\xaf\x16\x1e\x06\xfb\x8a\xe1a\xb0\xaf\x16\x1e\x06\xfbj\xe1a\xb0\xaf\x18\x1e\x06\xfb\xaa\xe1a\xb0\xaf\xc0\xdd\x9c\xd3\xb8*\x1e\x06\xfb\x8a\xe1a\xb0\xaf\x16\x1e\x06\xfbj\xe1a\xb0\xaf\x1e\x1e\xd6\xc7\xbe\xe0a}\xec\x0b\x1e\xd6\xc7\xbe\xe0a\xb0\xafaw\x0b\xfb\xaa\xe1a-\xecK\x9b\xb0\xaf0\x1e\x16\xc0\xbe\xf4\xaf\x86}\xb9\x9bk\x9d\xc6\xe9m\x0c\xfb\xd2\t\xec\xab\x86\x87\xb5\xb0/\xad\xd4\xb0/knk\xb7\xd5w\xd8W\r\x0fka_z\x16\xc3\xbe\xb4W\xc3\xbe\xe0a-\xecK35\xec\x0b\x1e\xd6\xc2\xbe\xf41\x86}\xe9\xba\x86}\xc1\xc3Z\xd8\x976j\xd8\x17<\xac\x85}\xe9O\x18\xfb\xb2\xe6\xdam\x03\xbd\x8aa_:\xaea_\xf0\xb0\x16\xf6\xa5\xa5\x1a\xf6\x05\x0fka_\xfa\x16\xc6\xbe\xdc\xcd9\x8d\x0b\xf4\x04\xf6\x15k\x17\xf6\x15\xc6\xc3`_\x81\xa6a_a<\x0c\xf6\x15\xe8\x03\xec+\xd6\x05\xec+\x8c\x87\xc1\xbe\x02\xad\xc1\xbe\xc2x\x18\xec+\xd0o\xd8W\x18\x0f\x83}\x05z\t\xfb\x8au\x08\xfb\n\xe3a\xb0\xaf@\x0b\xb0\xaf0\x1e\x06\xfb\n\xf4\x05\xf6\xd5_s\xed\xb6\x19<\x0c\xf6\x15h\x1b\xf6\x15\xc6\xc3`_\x81\xfe\xc3\xbe\xc2x\x18\xec+\xd0;\xd8W\xac3\xd8W\x17\x0f\x83}\x15Z\x85}U\xef\xe6\x9c\xc65\xfa\xd9\xc4\xbe\xe0a\xb0\xafJ\xcfa_\xb1\x0ez\xd8\x17<\x0c\xf6Uj\xae\x86}\xc1\xc3`_\xad>\xc3\xbe$I\x92$I\x92$I\x92$I\x92$I\x92$\r\xb3;\x9c(\x0b\x93\xa0\xbf\x83\x89\x00\x00\x00\x00IEND\xaeB`\x82')
@app.route("/<jiname>/")
def ji(jiname):return renderHTML(data=dict(path=[jiname],kind="list",data_main=[name for name in images[jiname].keys()]))
@app.route("/<jiname>/<albumname>/")
def album(jiname,albumname):return renderHTML(data=dict(path=[jiname,albumname],kind="images",data_main=[f"{i}.jpg" for i in range(len(images[jiname][albumname]))]))
@app.route("/<jiname>/<albumname>/<filename>")
def file(jiname,albumname,filename):
  _img=images[jiname][albumname][int(filename[:-4])]
  if type(_img)==str:
    _img=request.urlopen(_img).read()
    images[jiname][albumname][int(filename[:-4])]=_img
  return Response(_img)
CORS(app,resorces={r'/*': {"origins": '*'}})
app.run()