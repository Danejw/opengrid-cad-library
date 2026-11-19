"""Reproducible wall layouts in inches. Layout panels aligned to 28mm grid."""
from pathlib import Path
import argparse,csv,json,math
from library import GRID_IN, GRID_MM


def segments(total_cells:int,max_cells:int):
    count,rem=divmod(total_cells,max_cells)
    return [max_cells]*count+([rem] if rem else [])


def plan_wall(width_in:float,height_in:float,max_cells:int=8,name='Wall'):
    cols=int(math.floor((width_in+1e-9)/GRID_IN))
    rows=int(math.floor((height_in+1e-9)/GRID_IN))
    if cols<1 or rows<1:raise ValueError('Wall too small')
    cs,rs=segments(cols,max_cells),segments(rows,max_cells)
    parts=[]; y=0; i=0
    for r in rs:
        x=0
        for c in cs:
            i+=1
            parts.append(dict(id=f'{name.replace(" ","_")}_{i:03}',cells_w=c,cells_h=r,
                  width_in=round(c*GRID_IN,3),height_in=round(r*GRID_IN,3),
                  x_in=round(x*GRID_IN,3), y_in=round(y*GRID_IN,3)))
            x+=c
        y+=r
    return dict(name=name,wall_inches=[width_in,height_in],grid_cells=[cols,rows],
       coverage_inches=[round(cols*GRID_IN,3),round(rows*GRID_IN,3)],
       unused_inches=[round(width_in-cols*GRID_IN,3),round(height_in-rows*GRID_IN,3)],
       max_tile_cells=max_cells,number_of_panels=len(parts),parts=parts)


def save_svg(plan,path):
    w,h=plan['wall_inches']; scale=8.5
    W,H=int(w*scale),int(h*scale)
    lines=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">',
    '<rect width="100%" height="100%" fill="#ededed"/>']
    for p in plan['parts']:
        x=p['x_in']*scale;y=p['y_in']*scale;
        pw=p['width_in']*scale;ph=p['height_in']*scale
        lines.append(f'<rect x="{x:.2f}" y="{y:.2f}" width="{pw:.2f}" height="{ph:.2f}" fill="#e5e9ea" stroke="#3c5155" stroke-width="1.1"/>')
        # Draw real 28 mm cell pitch to show grid continuity.
        for a in range(p['cells_w']):
            for b in range(p['cells_h']):
                xx=x+(a+.5)*GRID_IN*scale; yy=y+(b+.5)*GRID_IN*scale
                r=GRID_IN*scale*.36
                lines.append(f'<rect x="{xx-r:.2f}" y="{yy-r:.2f}" width="{2*r:.2f}" height="{2*r:.2f}" rx="1.0" fill="none" stroke="#869b9c" stroke-width=".48"/>')
        lines.append(f'<text x="{x+pw/2:.2f}" y="{y+ph/2+2:.2f}" fill="#19383c" font-family="sans-serif" font-size="{8 if min(pw,ph)>35 else 5}" text-anchor="middle">{p["cells_w"]}×{p["cells_h"]}</text>')
    lines.append('</svg>')
    Path(path).write_text('\n'.join(lines))


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--printer',choices=['a1','a1-mini'],default='a1')
    p.add_argument('--out',default=str(Path(__file__).resolve().parents[1]/'output'))
    a=p.parse_args(); out=Path(a.out); out.mkdir(parents=True,exist_ok=True)
    max_cells=8 if a.printer=='a1' else 6
    plans=[plan_wall(64,64,max_cells,'Wall A'),plan_wall(54,60,max_cells,'Wall B')]
    for plan in plans:
        stem=plan['name'].replace(' ','_')+'_'+a.printer
        (out/(stem+'.json')).write_text(json.dumps(plan,indent=2))
        save_svg(plan,out/(stem+'.svg'))
        with (out/(stem+'.csv')).open('w',newline='') as f:
            wr=csv.DictWriter(f,fieldnames=list(plan['parts'][0]));wr.writeheader();wr.writerows(plan['parts'])
        print(f"{plan['name']}: {plan['number_of_panels']} tiles, {plan['coverage_inches']} inches coverage, unfilled border {plan['unused_inches']} inches")

if __name__=='__main__':main()
