import glob
import os

svgs = glob.glob("*.pdf.svg")
obrazcy = {"ma-pe": "Ma et al. (reanalyzed), K562, capture", "ma-wgs": "Ma et al. (reanalyzed), K562, WGS", "s30": "Protocol Ramani et al., biotin-fillin", "ramani-brain": "Ramani et al. (reanalyzed), M. musculus", "s5": "Protocol: Ma et al., K562"}
svgs = [{"Name": item, "Data": [(i if i not in obrazcy.keys() else obrazcy[i]) for i in item[:-8].split('_')]} for item in svgs]
new = open("zaplatka.txt", 'rb').readlines()

for svg in svgs:
	with open(svg["Name"], 'rt') as filehandle: data = filehandle.readlines()
	data[-1] = data[-1][:-6]
	new = [f'''
	<path style="opacity:1;vector-effect:none;fill:#ffffff;fill-opacity:1;fill-rule:evenodd;stroke:none;stroke-width:3.02362204;stroke-linecap:butt;stroke-linejoin:miter;stroke-miterlimit:4;stroke-dasharray:3.02362204, 3.02362204;stroke-dashoffset:0;stroke-opacity:1;paint-order:fill markers stroke" d="M 3304.6816,-9.8645673e-5 V 3304.6815 H 0 v 187.6016 H 5816.6934 V -9.8645673e-5 Z" id="rect1066" inkscape:connector-curvature="0" /><flowRoot transform="matrix(8.7121005,0,0,8.7121005,5819.4694,2264.0657)" xml:space="preserve" id="flowRoot4829-6-1-8" style="font-style:normal;font-weight:normal;font-size:40px;line-height:0;font-family:sans-serif;text-align:start;letter-spacing:0px;word-spacing:0px;text-anchor:start;fill:#000000;fill-opacity:1;stroke:none;stroke-width:0.11478288;stroke-linecap:butt;stroke-linejoin:round"><flowRegion style="line-height:0;text-align:start;text-anchor:start;fill:#000000;stroke-width:0.11478288;stroke-linecap:butt;stroke-linejoin:round" id="flowRegion4831-0-1-4"><rect style="line-height:0;text-align:start;text-anchor:start;fill:#000000;stroke-width:0.11478288;stroke-linecap:butt;stroke-linejoin:round" id="rect4833-4-0-3" width="401.90277" height="95.004715" x="-630" y="135.37683" /></flowRegion><flowPara id="flowPara4835-8-8-7" style="font-style:normal;font-variant:normal;font-weight:normal;font-stretch:normal;font-size:9.79480553px;line-height:1;font-family:'Liberation Mono';-inkscape-font-specification:'Liberation Mono';text-align:start;text-anchor:start;fill:#000000;stroke-width:0.11478288;stroke-linecap:butt;stroke-linejoin:round"><flowSpan style="font-style:normal;font-variant:normal;font-weight:bold;font-stretch:normal;font-family:'Liberation Mono';-inkscape-font-specification:'Liberation Mono Bold'" id="flowSpan1151">''' + 
	(f'''Above diagonal:</flowSpan> {svg["Data"][1]}</flowPara><flowPara style="font-style:normal;font-variant:normal;font-weight:normal;font-stretch:normal;font-size:9.79480553px;line-height:1;font-family:'Liberation Mono';-inkscape-font-specification:'Liberation Mono';text-align:start;text-anchor:start;fill:#000000;stroke-width:0.11478288;stroke-linecap:butt;stroke-linejoin:round" id="flowPara1099"><flowSpan style="font-style:normal;font-variant:normal;font-weight:bold;font-stretch:normal;font-family:'Liberation Mono';-inkscape-font-specification:'Liberation Mono Bold'" id="flowSpan1153">Below diagonal:</flowSpan> {svg["Data"][0]}</flowPara>''' if (svg["Data"][0] != "Ramani et al. (reanalyzed), M. musculus") else f'''Sample:</flowSpan> {svg["Data"][0]}</flowPara>''') +
	
	f'''<flowPara style="font-style:normal;font-variant:normal;font-weight:normal;font-stretch:normal;font-size:9.79480553px;line-height:1;font-family:'Liberation Mono';-inkscape-font-specification:'Liberation Mono';text-align:start;text-anchor:start;fill:#000000;stroke-width:0.11478288;stroke-linecap:butt;stroke-linejoin:round" id="flowPara1103">'''+
	
	(f'''<flowSpan style="font-style:normal;font-variant:normal;font-weight:bold;font-stretch:normal;font-family:'Liberation Mono';-inkscape-font-specification:'Liberation Mono Bold'" id="flowSpan1155">Resolution:</flowSpan> {svg["Data"][-2]}</flowPara><flowPara style="font-style:normal;font-variant:normal;font-weight:bold;font-stretch:normal;font-size:9.79480553px;line-height:0;font-family:sans-serif;-inkscape-font-specification:'sans-serif Bold';text-align:start;text-anchor:start;fill:#000000;stroke-width:0.11478288;stroke-linecap:butt;stroke-linejoin:round" id="flowPara1167"><flowSpan style="font-style:normal;font-variant:normal;font-weight:normal;font-stretch:normal;line-height:1;font-family:'Liberation Mono';-inkscape-font-specification:'Liberation Mono'" id="flowSpan1131"><flowSpan style="font-style:normal;font-variant:normal;font-weight:bold;font-stretch:normal;font-family:'Liberation Mono';-inkscape-font-specification:'Liberation Mono Bold'" id="flowSpan1157">Chromosome:</flowSpan> {svg["Data"][-3]}</flowSpan></flowPara>''' if ('ALL' not in svg["Data"]) else 
  
  f'''<flowSpan style="font-style:normal;font-variant:normal;font-weight:bold;font-stretch:normal;font-family:'Liberation Mono';-inkscape-font-specification:'Liberation Mono Bold'" id="flowSpan1155">Full-genome view</flowSpan></flowPara>''') + 
	f'''<flowPara style="font-style:normal;font-variant:normal;font-weight:bold;font-stretch:normal;font-size:9.79480553px;line-height:0;font-family:sans-serif;-inkscape-font-specification:'sans-serif Bold';text-align:start;text-anchor:start;fill:#000000;stroke-width:0.11478288;stroke-linecap:butt;stroke-linejoin:round" id="flowPara1175"><flowSpan style="font-style:normal;font-variant:normal;font-weight:normal;font-stretch:normal;line-height:1;font-family:'Liberation Mono';-inkscape-font-specification:'Liberation Mono'" id="flowSpan1177"><flowSpan style="font-style:normal;font-variant:normal;font-weight:bold;font-stretch:normal;font-family:'Liberation Mono';-inkscape-font-specification:'Liberation Mono Bold'" id="flowSpan1179">Color scale:</flowSpan> {svg["Data"][-1]}</flowSpan> </flowPara></flowRoot><flowRoot transform="matrix(8.7121005,0,0,8.7121005,5479.0945,-1784.648)" xml:space="preserve" id="flowRoot4829-6-1-8-0" style="font-style:normal;font-weight:normal;font-size:40px;line-height:1.25;font-family:sans-serif;text-align:center;letter-spacing:0px;word-spacing:0px;text-anchor:middle;fill:#000000;fill-opacity:1;stroke:none;stroke-width:0.11478288;stroke-linecap:butt;stroke-linejoin:round"><flowRegion style="text-align:center;text-anchor:middle;fill:#000000;stroke-width:0.11478288;stroke-linecap:butt;stroke-linejoin:round" id="flowRegion4831-0-1-4-2"><rect style="text-align:center;text-anchor:middle;fill:#000000;stroke-width:0.11478288;stroke-linecap:butt;stroke-linejoin:round" id="rect4833-4-0-3-7" width="404.21158" height="47.298599" x="-630" y="135.37683" /></flowRegion><flowPara style="font-style:normal;font-variant:normal;font-weight:bold;font-stretch:normal;font-size:13.33333397px;font-family:sans-serif;-inkscape-font-specification:'sans-serif Bold';text-align:center;text-anchor:middle;fill:#000000;stroke-width:0.11478288;stroke-linecap:butt;stroke-linejoin:round" id="flowPara5258"> </flowPara></flowRoot></svg>
	''']
	data += new
	with open(svg["Name"] + "pfff.svg", 'wt') as h: h.writelines(data)
#print(svgs)