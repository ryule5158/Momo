"""Convert the approved SVG's cubic paths to exact Illustrator path points."""
from pathlib import Path
from xml.etree import ElementTree as ET
import json
import re

ROOT=Path(__file__).resolve().parents[1]
result=[]
for element in ET.parse(ROOT/'current/svg/MOMO_FLOW_CAT_MARK.svg').getroot():
    if element.tag.rsplit('}',1)[-1] != 'path': continue
    tokens=re.findall(r'[MC]|[-+]?(?:\d*\.\d+|\d+)',element.get('d'))
    subpaths=[]
    pos=0
    while pos<len(tokens):
        cmd=tokens[pos];pos+=1
        if cmd=='M':
            anchor=list(map(float,tokens[pos:pos+2]));pos+=2
            subpaths.append([{'a':anchor,'l':anchor[:],'r':anchor[:]}])
        elif cmd=='C':
            numbers=list(map(float,tokens[pos:pos+6]));pos+=6
            subpaths[-1][-1]['r']=numbers[:2]
            subpaths[-1].append({'a':numbers[4:6],'l':numbers[2:4],'r':numbers[4:6]})
        else: raise ValueError(cmd)
    result.append({'name':element.get('id'),'stroke':element.get('stroke'),'width':float(element.get('stroke-width')),'subpaths':subpaths})
assert len(result)==7 and sum(len(p['subpaths']) for p in result)==8
(ROOT/'verification/REQ156_LOGO_PATH_DATA.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
code='''var data=DATA;
var d=app.activeDocument;
if(d.name!=='MOMO_R166_REQ146_PANEL.ai')throw Error('Wrong target document');
for(var n=0;n<d.groupItems.length;n++)if(d.groupItems[n].name==='req156-flow-cat-mark')throw Error('Approved logo already exists');
var layer=d.layers.add();layer.name='MOMO_MODULE_LOGO_FLOW_VECTOR';
var g=layer.groupItems.add();g.name='req156-flow-cat-mark';
var ab=d.artboards[0].artboardRect;var pt=72/25.4;
function xy(p){return [ab[0]+(53.3+p[0])*pt,ab[1]-(1.8+p[1])*pt];}
for(var i=0;i<data.length;i++){
 var s=data[i],container=g;
 if(s.subpaths.length>1){container=g.compoundPathItems.add();container.name=s.name;}
 for(var j=0;j<s.subpaths.length;j++){
  var p=container.pathItems.add();p.name=s.subpaths.length>1?s.name+'-'+j:s.name;
  p.filled=false;p.stroked=true;p.closed=false;p.strokeWidth=s.width*pt;
  var c=new RGBColor();c.red=parseInt(s.stroke.substr(1,2),16);c.green=parseInt(s.stroke.substr(3,2),16);c.blue=parseInt(s.stroke.substr(5,2),16);p.strokeColor=c;
  p.strokeCap=StrokeCap.ROUNDENDCAP;p.strokeJoin=StrokeJoin.ROUNDENDJOIN;
  for(var k=0;k<s.subpaths[j].length;k++){var v=s.subpaths[j][k];var q=p.pathPoints.add();q.anchor=xy(v.a);q.leftDirection=xy(v.l);q.rightDirection=xy(v.r);q.pointType=PointType.CORNER;}
 }
}
return {status:'NEW_LOGO_ADDED_OLD_RETAINED',name:g.name,bounds:g.geometricBounds,paths:d.pathItems.length,groups:d.groupItems.length};
'''.replace('DATA',json.dumps(result,separators=(',',':')))
(ROOT/'tools/add_momo_logo_native_ai.jsx').write_text(code,encoding='utf-8')
print('PASS 7 SVG paths -> 8 native subpaths; exact Bezier controls retained')
