import aggdraw
import PIL

from CompleteStyleGuide import CompleteStyleGuide
from map_lib.TMap import TMap

def rRiver(csg: CompleteStyleGuide, tmap: TMap, IMG):
    draw = aggdraw.Draw(IMG)
    pen2 = aggdraw.Pen((0, 0, 0, 255), 20)

    for feature in tmap.feature_list:
        for thing in feature.render_list:
            thing.execute_render(draw, pen2)

    draw.flush()
    return IMG
