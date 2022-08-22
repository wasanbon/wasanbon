import os
import sys
import traceback

# from . import node
from wasanbon.core.plugins.admin.idl_plugin.idl_parser import node

sep = '::'

primitive = [
    'boolean',
    'char', 'byte', 'octet',
    'short', 'wchar',
    'long',
    'float',
    'double',
    'string',
    'wstring']


def is_primitive(name):
    for n in name.split(' '):
        if n in primitive:
            return True
    return False


def IDLType(name, parent):
    if name == 'void':
        return IDLVoid(name, parent)

    elif name.find('sequence') >= 0:
        return IDLSequence(name, parent)
    elif name.find('[') >= 0:
        return IDLArray(name, parent)

    if is_primitive(name):
        return IDLPrimitive(name, parent)

    return IDLBasicType(name, parent)


class IDLTypeBase(node.IDLNode):
    def __init__(self, classname, name, parent):
        super(IDLTypeBase, self).__init__(classname, name, parent.root_node)
        self._is_sequence = False
        self._is_primitive = False

    def __str__(self):
        return self.name

    @property
    def is_sequence(self):
        return self._is_sequence

    @property
    def is_primitive(self):
        return self._is_primitive


class IDLVoid(IDLTypeBase):
    def __init__(self, name, parent):
        super(IDLVoid, self).__init__('IDLVoid', name, parent.root_node)
        self._verbose = True


class IDLSequence(IDLTypeBase):
    def __init__(self, name, parent):
        super(IDLSequence, self).__init__('IDLSequence', name, parent.root_node)
        self._verbose = True
        if name.find('sequence') < 0:
            raise SyntaxError()
        typ_ = name[name.find('<') + 1: name.find('>')]
        self._type = IDLType(typ_, parent)
        self._is_primitive = False  # self.inner_type.is_primitive
        self._is_sequence = True

    @property
    def inner_type(self):
        return self._type

    def __str__(self):
        return 'sequence<%s>' % str(self.inner_type)

    @property
    def obj(self):
        return self

    @property
    def type(self):
        return self._type

    @property
    def full_path(self):
        return self.parent.full_path + sep + self.name

    def to_simple_dic(self, quiet=False, full_path=False, recursive=False, member_only=False):
        name = self.full_path if full_path else self.name
        if quiet:
            return 'sequence<%s>' % str(self.inner_type)

        if recursive:
            if self.type.is_primitive:
                return {'sequence<%s>' % str(self.type): str(self.type)}
            else:
                return {'sequence<%s>' % str(self.type): self.type.obj.to_simple_dic(recursive=recursive, member_only=True)}
        """
            n = 'typedef ' + str(self.type) +' ' + name
            if not self.type.is_primitive:
                dic = { n : (self.type.obj.to_simple_dic(recursive=recursive, member_only=True))}
            else:
                dic = { n : str(self.type) }
            if member_only:
                return dic
            return {name : dic}

        dic = 'typedef %s %s' % (self.type, name)
        return dic
        """

    def to_dic(self):
        dic = {'name': self.name,
               'classname': self.classname,
               'type': str(self.type)}
        return dic


class IDLArray(IDLTypeBase):
    def __init__(self, name, parent):
        super(IDLArray, self).__init__('IDLArray', name, parent.root_node)

        self._verbose = True
        if name.find('[') < 0:
            raise SyntaxError()
        primitive_type_name = name[:name.find('[')]
        size = name[name.find('[') + 1: name.find(']')]
        inner_type_name = primitive_type_name + name[name.find(']') + 1:]
        self._size = int(size)
        self._type = IDLType(inner_type_name, parent)
        self._is_primitive = False  # self.inner_type.is_primitive
        self._is_sequence = False
        self._is_array = True

    @property
    def inner_type(self):
        return self._type

    @property
    def primitive_type(self):
        if self.inner_type.is_array:
            return self.inner_type.primitive_type
        else:
            return self.inner_type

    def __str__(self):
        n = ['%s' % self.primitive_type.name]

        def _apply_size(typ):
            n[0] = n[0] + '[%s]' % typ.size
            if typ.inner_type.is_array:
                _apply_size(typ.inner_type)

        _apply_size(self)
        return n[0]

    @property
    def obj(self):
        return self

    @property
    def size(self):
        return self._size

    @property
    def type(self):
        return self._type

    @property
    def full_path(self):
        return self.parent.full_path + sep + self.name

    def to_simple_dic(self, quiet=False, full_path=False, recursive=False, member_only=False):
        return str(self)

    def to_dic(self):
        dic = {'name': self.name,
               'classname': self.classname,
               'type': str(self.type)}
        return dic


class IDLPrimitive(IDLTypeBase):
    def __init__(self, name, parent):
        super(IDLPrimitive, self).__init__('IDLPrimitive', name, parent.root_node)
        self._verbose = True
        self._is_primitive = True


class IDLBasicType(IDLTypeBase):
    def __init__(self, name, parent):
        super(IDLBasicType, self).__init__('IDLBasicType', name, parent.root_node)
        self._verbose = True
        # if self.name.find('['):
        #    self._name = self.name[self.name.find('[')+1:]
        self._name = self.refine_typename(self.name)

    @property
    def obj(self):
        global_module = self.root_node
        typs = global_module.find_types(self.name)
        if len(typs) == 0:
            return None
        else:
            return typs[0]
