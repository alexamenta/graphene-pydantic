import typing as T

import pytest
from pydantic import BaseModel

from graphene_pydantic.interfacetype import PydanticInterfaceType
from graphene_pydantic.objecttype import PydanticObjectType

def test_interface_type():
    class Foo(BaseModel):
        name: str
        size: int

    class HasNameSize(PydanticInterfaceType):
        class Meta:
            model = Foo

    class Foo1(Foo):
        bar: list[int]

    class Foo2(Foo):
        baz: float

    class Foo1Obj(PydanticObjectType):
        class Meta:
            model = Foo1
            interfaces = (HasNameSize,)

    class Foo2Obj(PydanticObjectType):
        class Meta:
            model = Foo2
            interfaces = (HasNameSize,)

    assert list(Foo1Obj._meta.fields.keys()) == ["name", "size", "bar"]
    assert list(Foo2Obj._meta.fields.keys()) == ["name", "size", "baz"]

def test_interface_type_check_subclass():
    class InterfaceModel(BaseModel):
        name: str
        size: int

    class InterfaceObj(PydanticInterfaceType):
        class Meta:
            model = InterfaceModel

    class Foo(BaseModel):
        # satisfies the InterfaceModel interface but is not a subclass
        name: str
        size: int
        bar: list[int]

    with pytest.raises(AssertionError) as excinfo:
        class FooObj(PydanticObjectType):
            class Meta:
                model = Foo
                interfaces = (InterfaceObj,)

    assert "Foo" in str(excinfo)
    assert "must be a subclass" in str(excinfo)
    assert "InterfaceModel" in str(excinfo)


    # should have an error



# def test_object_type_excludefields():
#     class Foo(BaseModel):
#         name: str
#         size: int
#         color: T.Tuple[int, int, int, int]

#     class GraphFoo(PydanticObjectType):
#         class Meta:
#             model = Foo
#             exclude_fields = ("size",)

#     assert list(GraphFoo._meta.fields.keys()) == ["name", "color"]


# def test_object_type_onlyandexclude():
#     class Foo(BaseModel):
#         name: str
#         size: int
#         color: T.Tuple[int, int, int, int]

#     with pytest.raises(ValueError):

#         class GraphFoo(PydanticObjectType):
#             class Meta:
#                 model = Foo
#                 only_fields = ("name",)
#                 exclude_fields = ("size",)
