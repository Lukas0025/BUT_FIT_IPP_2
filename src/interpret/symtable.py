import errors

class frame:
    def __init__(self):
        self.table = {}
        
    ##
    # Create varaible in frame 
    # @pram name - name of varaible
    def def_var(self, name):
        if name in self.table:
            errors.semantic("{} var exist in frame".format(name))

        self.table[name] = {
            "type": None,
            "value": None
        }

    ##
    # Check if varaible is uninicialized
    # @pram name - name of varaible
    # @return bool
    def is_uninit(self, name):
        return self.table[name]['type'] == None

    ##
    # Set value by name of varaible
    # @pram name - name of varaible
    # @pram valtype - type of value
    # @pram value - value to store
    # @return None
    def set_value(self, name, valtype, value):
        if name not in self.table:
            errors.var_not_exist("{} var not exist in frame".format(name))

        self.table[name] = {
            "type": valtype,
            "value": value
        }

    ##
    # Get value of variable by name
    # @pram name - name of varaible
    # @return Str of value
    def get_value(self, name):
        if name not in self.table:
            errors.var_not_exist("{} var not exist in frame".format(name))

        if self.is_uninit(name):
            errors.missing_val_ret_stack("var {} is uninicalized".format(name))

        return self.table[name]['value']
    
    ##
    # Get data type of variable by name
    # @pram name - name of varaible
    # @return Str of type
    def get_type(self, name):
        if name not in self.table:
            errors.var_not_exist("{} var not exist in frame".format(name))

        return self.table[name]['type']

##
# Symtable class
# using frame class
class symtable:
    frames_types = ('gf', 'lf', 'tf')
    var_types    = ('int', 'float', 'bool', 'string', 'nil', 'type')

    def __init__(self):
        self.frames = [frame()]
        self.labels = {}
        
    ##
    # parse name like GF@test to array
    # @param name - name to parse
    # @return  {'type', 'name'}
    def _parse_name(self, name):
        name_split = name.split("@", 1)

        if len(name_split) < 2:
            errors.xml_struct("fail to decode name {}".format(name))

        return {'type': name_split[0].lower(), 'name': name_split[1]}

    ##
    # get frame link from str name like GF, TF, LF
    # @param name - name of frame
    # @return  frame obj link
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

    ##
    # get type of varaible name like GF@test
    # @param name -  name of varible
    # @return  str of type
    def get_type(self, name):
        parsed_name = self._parse_name(name)
        frame = self._get_frame(parsed_name['type'])

        return frame.get_type(parsed_name['name'])

    ##
    # check if varaible is unicialized
    # @param name - lame of varaible like GF@test
    # @return  bool
    def is_uninit(self, name):
        parsed_name = self._parse_name(name)
        frame = self._get_frame(parsed_name['type'])

        return frame.is_uninit(parsed_name['name'])

    ##
    # get type of expression like GF@test or string@hello
    # @param name -  expression
    # @return  str of type
    def get_type_str(self, name):
        parsed_name = self._parse_name(name)

        if parsed_name['type'] in self.var_types:
            return parsed_name['type']
        elif parsed_name['type'] in self.frames_types:
            return self.get_type(name)

    ##
    # get value of expression like GF@test or string@hello
    # @param name -  expression
    # @return  str of value
    def get_value_str(self, name):
        parsed_name = self._parse_name(name)

        if parsed_name['type'] in self.var_types:
            return parsed_name['name']
        elif parsed_name['type'] in self.frames_types:
            return self.get_value(name)

    ##
    # get value of varaible name like GF@test
    # @param name -  name of varible
    # @return  str of value
    def get_value(self, name):
        parsed_name = self._parse_name(name)
        frame = self._get_frame(parsed_name['type'])

        return frame.get_value(parsed_name['name'])

    ##
    # get value like 1 to varaible by name like GF@test
    # @param name -  name of varible
    # @param valtype -  type of value
    # @param value  -  value to set
    def set_value(self, name, valtype, val):
        parsed_name = self._parse_name(name)
        frame = self._get_frame(parsed_name['type'])

        frame.set_value(parsed_name['name'], valtype, val)

    ##
    # Create new frame and save it to self.tmpframe
    def create_frame(self):
        self.tmpframe = frame()

    ##
    # Push frame from self.tmpframe to frame stack as current LF
    def push_frame(self):
        self.frames.append(self._get_frame("tf"))
        del self.tmpframe

    ##
    # Pop frame from frame stack to self.tmpframe
    def pop_frame(self):
        if len(self.frames) < 2:
            errors.frame_not_exist("try pop not exist local frame")

        self.tmpframe = self.frames.pop()

    ##
    # Define varaible name like GF@test
    # @param name -  name of varible
    def def_var(self, name):
        parsed_name = self._parse_name(name)
        frame = self._get_frame(parsed_name['type'])
        
        frame.def_var(parsed_name['name'])

    ##
    # Define label name like test
    # @param name -  name of varible
    # @param addr -  address of label
    def def_label(self, label, addr):
        if label in self.labels:
            errors.semantic("{} label exist".format(label))

        self.labels[label] = addr

    ##
    # Get address of label by name like test
    # @param name -  name of varible
    # @return int  address of label
    def get_label(self, label):
        if label not in self.labels:
            errors.semantic("{} label not exist".format(label))

        return self.labels[label]
