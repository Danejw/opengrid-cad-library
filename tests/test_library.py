import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'cad'))
from library import GRID_IN,grid_span,centered_grid_locations,mounting_pattern,test_pitch_coupon as pitch_coupon,grid_tray,vented_crate,adapter_blank
from wall_planner import plan_wall,segments

def test_basic_dimensions():
    assert abs(GRID_IN-28/25.4)<1e-10
    assert grid_span(3)==84
    assert centered_grid_locations(2)==[-14,14]
    assert len(mounting_pattern(4,3))==12

def test_wall_plans():
    a,b=plan_wall(64,64,8),plan_wall(54,60,8)
    assert a['grid_cells']==[58,58]
    assert a['number_of_panels']==64
    assert b['grid_cells']==[48,54]
    assert b['number_of_panels']==42
    assert a['coverage_inches'][0]<=64
    assert b['coverage_inches'][1]<=60
    assert all(part['cells_w']<=8 and part['cells_h']<=8 for p in [a,b] for part in p['parts'])
    assert sum(part['cells_w']*part['cells_h'] for part in a['parts'])==58*58
    assert sum(part['cells_w']*part['cells_h'] for part in b['parts'])==48*54

def test_mini():
    a,b=plan_wall(64,64,6),plan_wall(54,60,6)
    assert a['number_of_panels']==100
    assert b['number_of_panels']==72

def test_model_solids_and_sizes():
    for fn in [pitch_coupon,grid_tray,vented_crate,adapter_blank]:
        model=fn().val()
        assert model.isValid(),fn.__name__
        assert model.Volume()>0,fn.__name__
        bounds=model.BoundingBox()
        assert 0<bounds.xlen<=180 and 0<bounds.ylen<=180,fn.__name__
