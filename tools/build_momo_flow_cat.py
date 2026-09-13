"""REQ156: layered flowing strokes matched to the live Volatile emblem."""
from pathlib import Path
from xml.etree import ElementTree as ET
import hashlib
import json
import re
import copy

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'verification/req156_flow_cat'
OUT.mkdir(parents=True,exist_ok=True)
PANEL=ROOT/'current/svg/MOMO_R166_REQ146_PANEL.svg'
AI=ROOT/'illustrator/MOMO_R166_REQ146_PANEL.ai'
VOL=Path('C:/Users/LENOVO/Desktop/Volatile/current/svg/VOLATILE_PANEL_MONO.svg')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
ai_before,vol_before=sha(AI),sha(VOL)
vroot=ET.parse(VOL).getroot()
vg=next(e for e in vroot.iter() if e.get('id')=='volatile-module-logo')
palette=[(e.get('stroke'),float(e.get('stroke-width'))) for e in vg]

# All geometry is curved, including the low rounded ear tips. Main and echoed
# back/haunch arcs follow the actual family mark's hierarchy and exact palette.
spec=[
('silhouette', 'M.92 3.17 C1.00 2.74 1.14 2.45 1.43 2.23 C1.50 2.05 1.37 1.68 1.49 1.59 C1.63 1.51 1.91 1.84 2.07 2.03 C2.31 1.98 2.55 2.02 2.75 2.10 C2.90 1.80 3.12 1.54 3.25 1.61 C3.39 1.70 3.24 2.09 3.28 2.25 C3.97 1.30 4.85 .97 5.82 1.09 C7.26 1.23 8.47 2.03 8.64 3.07 C8.83 4.22 7.45 4.47 6.19 4.30',0),
('back-echo', 'M3.68 2.30 C4.23 1.69 4.99 1.43 5.83 1.54 C7.05 1.69 8.04 2.36 8.15 3.12',1),
('back-inner', 'M4.24 2.34 C4.69 1.97 5.27 1.85 5.86 1.97 C6.88 2.17 7.38 2.67 7.48 3.10',2),
('face-paws', 'M.92 3.17 C.92 3.36 .73 3.45 .78 3.61 C.86 3.90 1.47 4.08 2.06 3.93 C2.50 3.83 2.78 3.59 2.91 3.25 M1.03 4.13 C1.81 4.48 3.12 4.15 3.75 3.74',3),
('haunch-tail', 'M6.88 2.78 C6.35 2.62 5.86 2.91 5.97 3.33 C6.13 4.01 7.48 4.35 8.11 3.87 C8.39 3.63 8.28 3.31 8.10 3.16',4),
('lower-return', 'M7.25 4.39 C6.06 4.47 5.33 3.82 4.30 4.02 C3.38 4.23 2.55 4.58 1.71 4.48',5),
('closed-eye', 'M1.40 3.18 C1.53 3.22 1.69 3.17 1.79 3.08',0),
]
art='\n'.join(f'<path id="flow-cat-{name}" d="{d}" fill="none" stroke="{palette[i][0]}" stroke-width="{palette[i][1]}" stroke-linecap="round" stroke-linejoin="round"/>' for name,d,i in spec)
logo=ROOT/'current/svg/MOMO_FLOW_CAT_MARK.svg'
svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="9.4mm" height="4.5mm" viewBox=".2 .5 9.4 4.5"><title>MOMO flowing cat mark - user approved 2026-09-12</title>{art}</svg>\n'
logo.write_text(svg,encoding='utf-8')
(OUT/logo.name).write_text(svg,encoding='utf-8')

# Same visible physical line widths as Volatile: factor ten converts mm to
# MOMO's panel drawing units, without rescaling stroke weights independently.
group=f'<g id="req156-flow-cat-mark" data-status="USER APPROVED 2026-09-12" data-style-reference="volatile-module-logo; exact stroke palette" transform="matrix(10 0 0 10 533 18)">\n{art}\n</g>'
pattern=re.compile(r'<g id="(?:req155-family-cat-mark|req156-flow-cat-mark)".*?</g>',re.S)
before=PANEL.read_text(encoding='utf-8')
assert len(pattern.findall(before))==1
if 'req155-family-cat-mark' in before:
    (OUT/'REJECTED_REQ155_PANEL.svg').write_text(before,encoding='utf-8')
after=pattern.sub(lambda _:group,before,count=1)
assert pattern.sub('CAT',before)==pattern.sub('CAT',after)
ET.fromstring(after)
ET.fromstring(svg)
PANEL.write_text(after,encoding='utf-8',newline='')
assert ai_before==sha(AI) and vol_before==sha(VOL)

# Actual unmodified Volatile glyph and new cat, shown at identical scale.
vparts=[]
for e in vg:
    v=copy.deepcopy(e)
    v.tag=v.tag.rsplit('}',1)[-1]
    vparts.append(ET.tostring(v,encoding='unicode'))
compare=f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="510" viewBox="0 0 24 10.2">
<rect width="24" height="10.2" fill="#f2f0e9"/>
<g font-family="Arial,sans-serif" font-size=".36" letter-spacing=".08" fill="#555"><text x="2" y="1.4">VOLATILE / CURRENT</text><text x="13" y="1.4">MOMO / APPROVED</text></g>
<g transform="translate(1.5 2.5)">{''.join(vparts)}</g>
<g transform="translate(13 2.5)">{art}</g>
</svg>'''
(OUT/'FAMILY_LOGO_COMPARISON.svg').write_text(compare,encoding='utf-8')
result={'status':'SVG_USER_APPROVED_2026-09-12','path_count':len(spec),'family_reference':'Volatile current original emblem','exact_family_strokes':palette,'outside_cat_unchanged':True,'ai_sha256_at_svg_generation':ai_before,'volatile_unchanged_sha256':vol_before,'panel_sha256':sha(PANEL),'boundary':'Visual approval granted by user. Physical manufacturing validation remains pending; AI readback is audited separately.'}
(OUT/'AUDIT.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result,ensure_ascii=False,indent=2))
