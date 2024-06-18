from dataclasses import dataclass
from pydantic import BaseModel, Field as dataclass_field
from sectionproperties.analysis.section import Section
from sectionproperties.pre.geometry import Polygon, Geometry
from moapy.auto_convert import auto_schema
from moapy.project.wgsd.wgsd_flow import gsdPoints

@dataclass
class MSectionProperty:
    """
    Section Property
    {
        "HEAD": ["Area", "Asy", "Asz", "Ixx", "Iyy", "Izz", "Cy", "Cz", "Syp", "Sym", "Szp", "Szm", "Ipyy", "Ipzz", "Zy", "Zz", "ry", "rz"]
        "DATA": [10.0, 20.0, 30.0, 40.0, 50.0, 60.0, 70.0, 80.0, 90.0, 100.0, 110.0, 120.0, 130.0, 140.0, 150.0, 160.0, 170.0, 180.0]
    }
    """
    HEAD: list[str]
    DATA: list[float]

class MPolygon(BaseModel):
    """
    Polygon
    """
    outerPolygon: gsdPoints = dataclass_field(default=gsdPoints(HEAD=["x", "y"],
                                                                DATA=[[0.0, 400.0, 400.0, 0.0], [0.0, 0.0, 600.0, 600.0]]), description="Outer polygon")

@auto_schema
def calc_sectprop(polygon: MPolygon) -> MSectionProperty:
    converted_coords = [[polygon.outerPolygon.DATA[0][i], polygon.outerPolygon.DATA[1][i]] for i in range(len(polygon.outerPolygon.DATA[0]))]
    converted_coords.append(converted_coords[0])
    geom = Geometry(Polygon(converted_coords))
    geom.create_mesh(mesh_sizes=100.0)

    section = Section(geom)
    section.calculate_geometric_properties()
    section.calculate_warping_properties()
    section.calculate_plastic_properties()
    return MSectionProperty(HEAD=["Area", "Asy", "Asz", "Ixx", "Iyy", "Izz", "Cy", "Cz", "Syp", "Sym", "Szp", "Szm", "Ipyy", "Ipzz", "Zy", "Zz", "ry", "rz"],
                            DATA=[section.get_area(), section.get_as()[0], section.get_as()[1], section.get_j(), section.get_ic()[0], section.get_ic()[1],
                                  section.get_c()[0], section.get_c()[1], section.get_z()[0], section.get_z()[1], section.get_z()[2], section.get_z()[3],
                                  section.get_ip()[0], section.get_ip()[1], section.get_s()[0], section.get_s()[1], section.get_rc()[0], section.get_rc()[1]])


# def mdreport(json_data):
#     dict_vertex = json.loads(json_data)
#     peri, area, centroid, Ic = calc(dict_vertex["vertices"])
#     rpt = moapy.mdreporter.ReportUtil("test.md", "section properties")
#     rpt.add_line_fvu("Perimeter", peri, moapy.mdreporter.enUnit.LENGTH)
#     rpt.add_line_fvu("Area", area, moapy.mdreporter.enUnit.AREA)
#     rpt.add_line_fvu("Cx", centroid[0], moapy.mdreporter.enUnit.LENGTH)
#     rpt.add_line_fvu("Cy", centroid[1], moapy.mdreporter.enUnit.LENGTH)
#     rpt.add_line_fvu("Ix", Ic[0], moapy.mdreporter.enUnit.INERTIA)
#     rpt.add_line_fvu("Iy", Ic[1], moapy.mdreporter.enUnit.INERTIA)
#     return rpt.get_md_text()

#json_data = '{"vertices": [[10,10], [300,10], [300,300], [10, 300]]}'
# json_data = '{"vertices": [[0.0, 0.0], [400.0, 0.0], [400.0, 600.0], [0.0, 600.0], [0.0, 0.0]]}'
# md = mdreport(json_data)
# print(md)

# inp = MPolygon()
# res = calc_sectprop(inp)
# print(res)
