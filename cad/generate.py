"""Generate editable STEP and printable STL examples using CadQuery."""
import argparse
from pathlib import Path
from library import BUILDERS,export_model

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--part', choices=['all',*BUILDERS],default='all')
    ap.add_argument('--out',default=str(Path(__file__).resolve().parents[1]/'output'))
    args=ap.parse_args()
    parts=BUILDERS if args.part=='all' else {args.part:BUILDERS[args.part]}
    for name,fn in parts.items():
        obj=fn()
        export_model(obj,Path(args.out)/name)
        bounds=obj.val().BoundingBox()
        print(f'{name}: {bounds.xlen/25.4:.2f} x {bounds.ylen/25.4:.2f} x {bounds.zlen/25.4:.2f} inches => STEP + STL')

if __name__=='__main__': main()
