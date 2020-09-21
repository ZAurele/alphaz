from flask import request

from ..main import AlphaException

class Parameter():
    def __init__(self,
            name:str,
            default=None,
            options=None,
            cacheable:bool=True,
            required:bool=False,
            ptype:type=str
        ):

        self.name       = name
        self.default    = default
        self.cacheable  = cacheable
        self.options    = options
        self.required   = required
        self.ptype:type = ptype
        self.type       = str(ptype).replace("<class '","").replace("'>","")
        self.value      = None

    def set_value(self):
        dataPost                = request.get_json()

        self.value              = request.args.get(self.name,self.default)

        if self.value is None and dataPost is not None and self.name in dataPost:
            self.value          = dataPost[self.name]

        if self.options is not None and self.value not in self.options:
            self.value = None

        if self.required and self.value is None:
            missing = True
            raise AlphaException('api_missing_parameter',parameters={'parameter':self.name})

        if self.ptype == bool and not self.value is None:
            str_value = str(self.value).lower()
            if str_value == 'y': value = True
            elif str_value == 'true': value = True
            elif str_value == 't': value = True
            elif str_value == 'n': value = False
            elif str_value == 'false': value = False
            elif str_value == 'f': value = False
            else: 
                raise AlphaException('api_wrong_parameter_value',parameters={'parameter':self.name})
            self.value = value