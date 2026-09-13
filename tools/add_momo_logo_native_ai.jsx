var data=[{"name":"flow-cat-silhouette","stroke":"#646464","width":0.14,"subpaths":[[{"a":[0.92,3.17],"l":[0.92,3.17],"r":[1.0,2.74]},{"a":[1.43,2.23],"l":[1.14,2.45],"r":[1.5,2.05]},{"a":[1.49,1.59],"l":[1.37,1.68],"r":[1.63,1.51]},{"a":[2.07,2.03],"l":[1.91,1.84],"r":[2.31,1.98]},{"a":[2.75,2.1],"l":[2.55,2.02],"r":[2.9,1.8]},{"a":[3.25,1.61],"l":[3.12,1.54],"r":[3.39,1.7]},{"a":[3.28,2.25],"l":[3.24,2.09],"r":[3.97,1.3]},{"a":[5.82,1.09],"l":[4.85,0.97],"r":[7.26,1.23]},{"a":[8.64,3.07],"l":[8.47,2.03],"r":[8.83,4.22]},{"a":[6.19,4.3],"l":[7.45,4.47],"r":[6.19,4.3]}]]},{"name":"flow-cat-back-echo","stroke":"#929292","width":0.11,"subpaths":[[{"a":[3.68,2.3],"l":[3.68,2.3],"r":[4.23,1.69]},{"a":[5.83,1.54],"l":[4.99,1.43],"r":[7.05,1.69]},{"a":[8.15,3.12],"l":[8.04,2.36],"r":[8.15,3.12]}]]},{"name":"flow-cat-back-inner","stroke":"#9B9B9B","width":0.105,"subpaths":[[{"a":[4.24,2.34],"l":[4.24,2.34],"r":[4.69,1.97]},{"a":[5.86,1.97],"l":[5.27,1.85],"r":[6.88,2.17]},{"a":[7.48,3.1],"l":[7.38,2.67],"r":[7.48,3.1]}]]},{"name":"flow-cat-face-paws","stroke":"#757575","width":0.12,"subpaths":[[{"a":[0.92,3.17],"l":[0.92,3.17],"r":[0.92,3.36]},{"a":[0.78,3.61],"l":[0.73,3.45],"r":[0.86,3.9]},{"a":[2.06,3.93],"l":[1.47,4.08],"r":[2.5,3.83]},{"a":[2.91,3.25],"l":[2.78,3.59],"r":[2.91,3.25]}],[{"a":[1.03,4.13],"l":[1.03,4.13],"r":[1.81,4.48]},{"a":[3.75,3.74],"l":[3.12,4.15],"r":[3.75,3.74]}]]},{"name":"flow-cat-haunch-tail","stroke":"#A0A0A0","width":0.105,"subpaths":[[{"a":[6.88,2.78],"l":[6.88,2.78],"r":[6.35,2.62]},{"a":[5.97,3.33],"l":[5.86,2.91],"r":[6.13,4.01]},{"a":[8.11,3.87],"l":[7.48,4.35],"r":[8.39,3.63]},{"a":[8.1,3.16],"l":[8.28,3.31],"r":[8.1,3.16]}]]},{"name":"flow-cat-lower-return","stroke":"#969696","width":0.105,"subpaths":[[{"a":[7.25,4.39],"l":[7.25,4.39],"r":[6.06,4.47]},{"a":[4.3,4.02],"l":[5.33,3.82],"r":[3.38,4.23]},{"a":[1.71,4.48],"l":[2.55,4.58],"r":[1.71,4.48]}]]},{"name":"flow-cat-closed-eye","stroke":"#646464","width":0.14,"subpaths":[[{"a":[1.4,3.18],"l":[1.4,3.18],"r":[1.53,3.22]},{"a":[1.79,3.08],"l":[1.69,3.17],"r":[1.79,3.08]}]]}];
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
