# -*- coding: utf-8 -*-
"""

"""

import xml.etree.ElementTree as et
from copy import deepcopy
from typing import Union

import rwmap._util as utility
import rwmap._frame as frame
from rwmap._case._object import TObject
from rwmap._frame._element_ori import ElementOri
from rwmap._frame._element_property import ElementProperties

class ObjectGroup(ElementOri):
    def __init__(self, properties:ElementProperties, object_list:list[TObject])->None:
        super().__init__(properties)
        self._object_list = deepcopy(object_list)

    def __iter__(self):
        return self._object_list

    @classmethod
    def init_etElement(cls, root:et.Element)->None:
        properties = ElementProperties.init_etElement(root)
        object_list = [TObject.init_etElement(tobject) for tobject in root if tobject.tag == "object"]
        return cls(properties, object_list)
    
    @classmethod
    def init_ObjectGroup(cls, name:str)->None:
        properties = ElementProperties("objectgroup", {"name": "Triggers"})
        return cls(properties, [])
    
    def id(self)->int:
        return int(self._properties.returnDefaultProperty("id"))
    
    def changeid(self, id:int)->None:
        self._properties.assignDefaultProperty("id", id)
    
    def output_str(self, objectnum:int = -1)->str:
        str_ans = ""
        str_ans = str_ans + self._properties.output_str() + "\n"
        str_ans = str_ans + "".join([self._object_list[i].output_str() + "\n" for i in range(0, min(len(self._object_list), objectnum))]) + "\n"
        str_ans = utility.indentstr_Tab(str_ans)
        return str_ans
    
    def name(self)->str:
        return self._properties.returnDefaultProperty("name")

    def __repr__(self)->str:
        return self.output_str()

    def output_etElement(self)->et.Element:
        root = et.Element("objectgroup")
        root = self._properties.output_etElement(root)
        for tobject in self._object_list:
            tobject_element = et.Element("object")
            tobject_element = tobject.output_etElement(tobject_element)
            root.append(tobject_element)
        return root
    
    def addObject_type(self, tobject:TObject):
        self._object_list.append(tobject)

    def addObject_dict(self, default_properties:dict[str, str] = {}, optional_properties:dict[str, Union[str, dict[str, str]]] = {}, other_properties:list[et.Element] = [])->None:
        self._object_list.append(TObject("object", default_properties, optional_properties, other_properties))

    def deleteObject(self, tobject:TObject):
        self._object_list.remove(tobject)

    def index_object_s(self, tobject:TObject)->int:
        self._object_list.index(tobject)
