from compas.datastructures import Mesh
from compas.geometry import Box
from compas.geometry import Cone
from compas.geometry import Cylinder
from compas.geometry import Sphere
from ifcopenshell.api import run

from .brep import brep_to_ifc_advanced_brep
from .mesh import mesh_to_IfcPolygonalFaceSet
from .mesh import mesh_to_IfcShellBasedSurfaceModel
from .shapes import box_to_IfcBlock
from .shapes import cone_to_IfcRightCircularCone
from .shapes import cylinder_to_IfcRightCircularCylinder
from .shapes import sphere_to_IfcSphere


def write_body_representation(file, body, ifc_entity, context):
    try:
        from compas_occ.brep import OCCBrep
    except ImportError:
        OCCBrep = None

    def _body_to_shape(body):
        if isinstance(body, Box):
            shape = box_to_IfcBlock(file, body)
        elif isinstance(body, Sphere):
            shape = sphere_to_IfcSphere(file, body)
        elif isinstance(body, Cone):
            shape = cone_to_IfcRightCircularCone(file, body)
        elif isinstance(body, Cylinder):
            shape = cylinder_to_IfcRightCircularCylinder(file, body)
        elif isinstance(body, Mesh):
            if file.schema == "IFC4" or file.schema == "IFC4x3":
                shape = mesh_to_IfcPolygonalFaceSet(file, body)
            else:
                shape = mesh_to_IfcShellBasedSurfaceModel(file, body)
        elif OCCBrep and isinstance(body, OCCBrep):
            shape = brep_to_ifc_advanced_brep(file, body)
        else:
            raise Exception("Unsupported body type.")
        return shape

    if isinstance(body, list):
        shape = []
        for b in body:
            s = _body_to_shape(b)
            if not isinstance(s, list):
                shape.append(s)
            else:
                shape.extend(s)
    else:
        shape = _body_to_shape(body)
        if not isinstance(shape, list):
            shape = [shape]

    RepresentationType = "SolidModel"

    if shape and shape[0].is_a("IfcShellBasedSurfaceModel"):
        RepresentationType = "SurfaceModel"

    representation = file.create_entity(
        "IfcShapeRepresentation",
        ContextOfItems=context,
        RepresentationIdentifier="Body",
        RepresentationType=RepresentationType,
        Items=shape,
    )

    run("geometry.assign_representation", file, product=ifc_entity, representation=representation)

    return representation
