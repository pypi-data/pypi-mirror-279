# -*- coding: utf-8 -*-
__author__ = 'Lucas Barros'
__version__ = 1.0
__maintainer__ = 'Lucas Barros'
__email__ = 'lucasbarros2000@hotmail.com'
__status__ = 'Production'


from bson import ObjectId
from pydantic import BaseModel
from pydantic import Field


class LbMenu(BaseModel):

    id: ObjectId = Field(
        description="Object id menu at mongo database",
        default=None,
        alias="_id"
    )

    name: str = Field(
        description="Name menu at mongo database",
        default=None
    )

    path: str = Field(
        description="Path menu at mongo database",
        default=None
    )

    label: str = Field(
        description="Label menu at mongo database",
        default=None
    )

    icon: str = Field(
        description="Icon menu at mongo database",
        default=None
    )

    data_cy: str = Field(
        description="Data CY menu at mongo database",
        default=None
    )

    order: int = Field(
        description="Order menu at mongo database",
        default=None
    )

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
