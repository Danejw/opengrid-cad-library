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

def test_wall_planner_uses_supplied_dimensions():
    plan = plan_wall(20, 15, 8, 'Sample')
    assert plan['wall_inches'] == [20, 15]
    assert plan['grid_cells'] == [18, 13]
    assert plan['number_of_panels'] == 6
    assert all(part['cells_w'] <= 8 and part['cells_h'] <= 8 for part in plan['parts'])
    assert sum(p['cells_w'] * p['cells_h'] for p in plan['parts']) == 18 * 13
    assert plan['coverage_inches'][0] <= 20
    assert plan['coverage_inches'][1] <= 15

def test_mini_custom_layout():
    plan = plan_wall(20, 15, 6, 'Sample')
    assert plan['grid_cells'] == [18, 13]
    assert plan['number_of_panels'] == 9
    assert all(p['cells_w'] <= 6 and p['cells_h'] <= 6 for p in plan['parts'])


def test_model_solids_and_sizes():
    for fn in [pitch_coupon,grid_tray,vented_crate,adapter_blank]:
        model=fn().val()
        assert model.isValid(),fn.__name__
        assert model.Volume()>0,fn.__name__
        bounds=model.BoundingBox()
        assert 0<bounds.xlen<=180 and 0<bounds.ylen<=180,fn.__name__
