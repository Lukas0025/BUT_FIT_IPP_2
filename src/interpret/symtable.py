import errors

class frame:
    def __init__(self):
        self.table = {}

    def def_var(self, name):
        if name in self.table:
            errors.semantic("{} var exist in frame".format(name))

        self.table[name] = {
            "type": None,
            "value": None
        }

    def is_uninit(self, name):
        return self.table[name]['type'] == None

    def set_value(self, name, valtype, value):
        if name not in self.table:
            errors.var_not_exist("{} var not exist in frame".format(name))

        self.table[name] = {
            "type": valtype,
            "value": value
        }

    def get_value(self, name):
        if name not in self.table:
            errors.var_not_exist("{} var not exist in frame".format(name))

        if self.is_uninit(name):
            errors.missing_val_ret_stack("var {} is uninicalized".format(name))

        return self.table[name]['value']

    def get_type(self, name):
        if name not in self.table:
            errors.var_not_exist("{} var not exist in frame".format(name))

        return self.table[name]['type']

class symtable:
    frames_types = ('gf', 'lf', 'tf')
    var_types    = ('int', 'float', 'bool', 'string', 'nil', 'type')

    def __init__(self):
        self.frames = [frame()]
        self.labels = {}

    def _parse_name(self, name):
        name_split = name.split("@", 1)

        return {'type': name_split[0].lower(), 'name': name_split[1]}

    def _get_frame(self, name):
        
        if name == 'gf':
            return self.frames[0]
        elif name == 'lf':
            if len(self.frames) < 2:
                errors.frame_not_exist("try access to not exist local frame")

            return self.frames[-1]
        elif name == 'tf':
            if not hasattr(self, 'tmpframe'):
                errors.frame_not_exist("try access not exist tmp frame")

            return self.tmpframe
        
        errors.frame_not_exist("try read from unexisted frame {}".format(name))

    def get_type(self, name):
        parsed_name = self._parse_name(name)
        frame = self._get_frame(parsed_name['type'])

        return frame.get_type(parsed_name['name'])

    def is_uninit(self, name):
        parsed_name = self._parse_name(name)
        frame = self._get_frame(parsed_name['type'])

        return frame.is_uninit(parsed_name['name'])

    def get_type_str(self, name):
        parsed_name = self._parse_name(name)

        if parsed_name['type'] in self.var_types:
            return parsed_name['type']
        elif parsed_name['type'] in self.frames_types:
            return self.get_type(name)

    def get_value_str(self, name):
        parsed_name = self._parse_name(name)

        if parsed_name['type'] in self.var_types:
            return parsed_name['name']
        elif parsed_name['type'] in self.frames_types:
            return self.get_value(name)

    def get_value(self, name):
        parsed_name = self._parse_name(name)
        frame = self._get_frame(parsed_name['type'])

        return frame.get_value(parsed_name['name'])

    def set_value(self, name, valtype, val):
        parsed_name = self._parse_name(name)
        frame = self._get_frame(parsed_name['type'])

        frame.set_value(parsed_name['name'], valtype, val)

    def create_frame(self):
        self.tmpframe = frame()

    def push_frame(self):
        self.frames.append(self._get_frame("tf"))
        del self.tmpframe

    def pop_frame(self):
        if len(self.frames) < 2:
            errors.frame_not_exist("try pop not exist local frame")

        self.tmpframe = self.frames.pop()

    def def_var(self, name):
        parsed_name = self._parse_name(name)
        frame = self._get_frame(parsed_name['type'])
        
        frame.def_var(parsed_name['name'])

    def def_label(self, label, addr):
        if label in self.labels:
            errors.semantic("{} label exist".format(label))

        self.labels[label] = addr

    def get_label(self, label):
        if label not in self.labels:
            errors.semantic("{} label not exist".format(label))

        return self.labels[label]