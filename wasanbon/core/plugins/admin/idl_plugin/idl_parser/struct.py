import os
import sys
import traceback

# from . import node
# from . import type as idl_type
from wasanbon.core.plugins.admin.idl_plugin.idl_parser import node
from wasanbon.core.plugins.admin.idl_plugin.idl_parser import type as idl_type


class IDLValue(node.IDLNode):
    def __init__(self, parent):
        super(IDLValue, self).__init__('IDLValue', '', parent)
        self._verbose = True
        self._type = None
        self.sep = '::'

    @property
    def full_path(self):
        return self.parent.full_path + self.sep + self.name

    def parse_blocks(self, blocks, filepath=None):
        self._filepath = filepath
        name, typ = self._name_and_type(blocks)
        if typ.find('[') >= 0:
            # print self.name, ':',typ
            pass
        if name.find('[') > 0:
            name_ = name[:name.find('[')]
            # print typ
            typ = typ.strip() + ' ' + name[name.find('['):]
            name = name_
        self._name = name
        self._type = idl_type.IDLType(typ, self)

    def to_simple_dic(self, recursive=False, member_only=False):
        if recursive:
            if self.type.is_primitive:
                return str(self.type) + ' ' + self.name
            elif self.type.obj.is_enum:
                return str('enum') + ' ' + self.name
            dic = {str(self.type) + ' ' + self.name:
                   self.type.obj.to_simple_dic(recursive=recursive, member_only=True)}
            return dic
        dic = {self.name: str(self.type)}
        return dic

    def to_dic(self):
        dic = {'name': self.name,
               'filepath': self.filepath,
               'classname': self.classname,
               'type': str(self.type)}
        return dic

    @property
    def type(self):
        return self._type

    def post_process(self):
        #self._type = self.refine_typename(self.type)
        pass


class IDLStruct(node.IDLNode):

    def __init__(self, name, parent):
        super(IDLStruct, self).__init__('IDLStruct', name.strip(), parent)
        self._verbose = True
        self._members = []
        self.sep = '::'

    @property
    def full_path(self):
        return (self.parent.full_path + self.sep + self.name).strip()

    def to_simple_dic(self, quiet=False, full_path=False, recursive=False, member_only=False):
        name = self.full_path if full_path else self.name
        if quiet:
            return 'struct %s' % name

        dic = {'struct %s' % name: [v.to_simple_dic(recursive=recursive) for v in self.members]}

        if member_only:
            return list(dic.values())[0]
        return dic

    def to_dic(self):
        dic = {'name': self.name,
               'classname': self.classname,
               'members': [v.to_dic() for v in self.members]}
        return dic

    def parse_tokens(self, token_buf, filepath=None):
        self._filepath = filepath
        kakko = token_buf.pop()
        if not kakko == '{':
            if self._verbose:
                sys.stdout.write('# Error. No kakko "{".\n')
            raise SyntaxError()

        block_tokens = []
        while True:

            token = token_buf.pop()
            if token == None:
                if self._verbose:
                    sys.stdout.write('# Error. No kokka "}".\n')
                raise SyntaxError()

            elif token == '}':
                token = token_buf.pop()
                if not token == ';':
                    if self._verbose:
                        sys.stdout.write('# Error. No semi-colon after "}".\n')
                    raise SyntaxError()
                break

            if token == ';':
                self._parse_block(block_tokens)
                block_tokens = []
                continue
            block_tokens.append(token)

        self._post_process()

    def _parse_block(self, blocks):
        v = IDLValue(self)
        v.parse_blocks(blocks, self.filepath)
        self._members.append(v)

    def _post_process(self):
        self.forEachMember(lambda m: m.post_process())

    @property
    def members(self):
        return self._members

    def forEachMember(self, func):
        for m in self._members:
            func(m)
