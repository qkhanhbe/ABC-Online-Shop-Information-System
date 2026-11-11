"""Product details in the class models (lecturer's remark: no single product table for every product kind).

CL01  analysis: Category.detailKind, ProductDetail {abstract} with four kinds, Product 1 - 1 ProductDetail
DCL03 design:   the same hierarchy with Python types and the operations of model/product.py
PKG01 layers:   the five classes in model.product
"""
from vp import call, colour

KINDS = {
    "FootwearDetail": [("sizes", "String"), ("upperMaterial", "String"), ("sole", "String"), ("purpose", "String")],
    "ApparelDetail": [("sizes", "String"), ("material", "String"), ("fit", "String")],
    "BagDetail": [("capacityL", "float"), ("material", "String"), ("laptopSleeve", "boolean")],
    "WatchDetail": [("movement", "String"), ("strap", "String"), ("waterResistanceM", "int"), ("batteryDays", "int")],
}
DESIGN = {
    "FootwearDetail": [("sizes", "str"), ("upper_material", "str"), ("sole", "str"), ("purpose", "str")],
    "ApparelDetail": [("sizes", "str"), ("material", "str"), ("fit", "str")],
    "BagDetail": [("capacity_l", "float"), ("material", "str"), ("laptop_sleeve", "bool")],
    "WatchDetail": [("movement", "str"), ("strap", "str"), ("water_resistance_m", "int"), ("battery_days", "int")],
}


def analysis():
    d, mp = "CL01 Analysis Class Diagram", "Analysis Model"
    call("addAttribute", className="Category", attributeName="detailKind", attributeType="String",
         visibility="private", diagramName=d)
    call("addClass", diagramName=d, className="ProductDetail", isAbstract=True, modelPackage=mp)
    for cls, attrs in KINDS.items():
        call("addClass", diagramName=d, className=cls, modelPackage=mp)
        for n, t in attrs:
            call("addAttribute", quiet=True, className=cls, attributeName=n, attributeType=t, visibility="private", diagramName=d)
        call("addGeneralization", diagramName=d, fromClass=cls, toClass="ProductDetail")
    call("addComposition", diagramName=d, fromClass="Product", toClass="ProductDetail", fromMultiplicity="1", toMultiplicity="1")
    call("setAssociationProperties", diagramName=d, fromClass="Product", toClass="ProductDetail", name="described by")
    colour(d, ["ProductDetail"] + list(KINDS))


def design():
    d = "DCL03 Design Classes - Catalogue and Inventory"
    call("addAttribute", className="Category", attributeName="detail_kind", attributeType="str",
         visibility="public", diagramName=d)
    call("addClass", diagramName=d, className="ProductDetail", isAbstract=True, modelPackage="product")
    call("addAttribute", className="ProductDetail", attributeName="product_id", attributeType="str",
         visibility="public", diagramName=d)
    call("addOperation", className="ProductDetail", operationName="spec_rows", returnType="list", params="",
         visibility="public", diagramName=d)
    call("addOperation", className="ProductDetail", operationName="search_terms", returnType="str", params="",
         visibility="public", diagramName=d)
    for cls, attrs in DESIGN.items():
        call("addClass", diagramName=d, className=cls, modelPackage="product")
        for n, t in attrs:
            call("addAttribute", quiet=True, className=cls, attributeName=n, attributeType=t, visibility="public", diagramName=d)
        call("addGeneralization", diagramName=d, fromClass=cls, toClass="ProductDetail")
    call("addComposition", diagramName=d, fromClass="Product", toClass="ProductDetail", fromMultiplicity="1", toMultiplicity="0..1")
    call("setAssociationProperties", diagramName=d, fromClass="Product", toClass="ProductDetail", name="detail",
         toRole="detail", fromRole="-", fromNavigable="unspecified", toNavigable="true")
    colour(d, ["ProductDetail"] + list(DESIGN))


def packages():
    d = "PKG01 Layers, Packages and Classes"
    for cls in ["ProductDetail"] + list(DESIGN):
        call("addClassInPackage", diagramName=d, packageName="product", className=cls)


if __name__ == "__main__":
    analysis()
    design()
    packages()
