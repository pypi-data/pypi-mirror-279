# -*- coding: utf-8 -*-
__author__ = 'Lucas Barros'
__version__ = 1.0
__maintainer__ = 'Lucas Barros'
__email__ = 'lucasbarros2000@hotmail.com'
__status__ = 'Production'


from bson import ObjectId
from pydantic import BaseModel
from pydantic import Field


class LbCounty(BaseModel):

    id: ObjectId = Field(
        description="Object id county at mongo database",
        default=None,
        alias="_id"
    )

    code: str = Field(
        description="Code county at mongo database",
        default=None
    )

    description: str = Field(
        description="Description county at mongo database",
        default=None
    )

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
