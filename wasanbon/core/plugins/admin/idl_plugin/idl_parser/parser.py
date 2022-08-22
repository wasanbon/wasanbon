import os
import sys

# from . import module, token_buffer
# from . import type as idl_type
from wasanbon.core.plugins.admin.idl_plugin.idl_parser import module, token_buffer
from wasanbon.core.plugins.admin.idl_plugin.idl_parser import type as idl_type


class IDLParser():

    def __init__(self, idl_dirs=[]):
        self._global_module = module.IDLModule()
        self._dirs = idl_dirs
        self._verbose = False

    @property
    def global_module(self):
        return self._global_module

    def is_primitive(self, name):
        return idl_type.is_primitive(name)

    @property
    def dirs(self):
        return self._dirs

    def parse(self, idls=[], idl_dirs=[], except_files=[]):
        """ Parse IDL files. Result of parsing can be accessed via global_module property.
        :param idls: List of IDL files. Must be fullpath.
        :param idl_dirs: List of directory which contains target IDL files. Must be fullpath.
        :param except_files: List of IDL files that should be ignored. Do not have to use fullpath.
        :returns: None
        """
        self.forEachIDL(self.parse_idl, except_files=except_files, idls=idls)

    def parse_idl(self, idl_path):
        if self._verbose:
            sys.stdout.write(' - Parsing IDL (%s)\n' % idl_path)
        f = open(idl_path, 'r')
        lines = []
        for line in f:
            lines.append(line)

        lines = self._clear_comments(lines)
        lines = self._paste_include(lines)
        lines = self._clear_ifdef(lines)

        self._token_buf = token_buffer.TokenBuffer(lines)

        self._global_module.parse_tokens(self._token_buf, filepath=idl_path)

    def forEachIDL(self, func, idl_dirs=[], except_files=[], idls=[]):
        """ Parse IDLs and apply function.
        :param func: Function. IDL file fullpath will be passed to the function.
        :param idls: List of IDL files. Must be fullpath.
        :param idl_dirs: List of directory which contains target IDL files. Must be fullpath.
        :param except_files: List of IDL files that should be ignored. Do not have to use fullpath.
        :returns: None
        """
        idl_dirs = self._dirs + idl_dirs
        self._dirs = idl_dirs
        idls_ = []
        basenames_ = []
        for idl_dir in idl_dirs:
            for f in os.listdir(idl_dir):
                if f.endswith('.idl'):
                    if not f in except_files:
                        path = os.path.join(idl_dir, f)
                        if not f in basenames_:
                            idls_.append(path)
                            basenames_.append(os.path.basename(path))

        idls_ = idls_ + idls
        for f in idls_:
            if self._verbose:
                sys.stdout.write(' - Apply function to %s\n' % f)
            func(f)

    def _find_idl(self, filename, apply_func, idl_dirs=[]):
        if self._verbose:
            sys.stdout.write(' --- Find %s\n' % filename)

        global retval
        retval = None

        def func(filepath):
            if os.path.basename(filepath) == filename:
                global retval
                retval = apply_func(filepath)

        self.forEachIDL(func, idl_dirs=idl_dirs)
        return retval

    def _paste_include(self, lines):
        output_lines = []
        for line in lines:
            output_line = ''
            if line.startswith('#include'):
                def _include_paste(filepath):
                    return filepath

                if line.find('"') >= 7:
                    filename = line[line.find('"') + 1: line.rfind('"')]
                    if self._verbose:
                        sys.stdout.write(' -- Includes %s\n' % filename)
                    p = self._find_idl(filename, _include_paste)
                    if p is None:
                        sys.stdout.write(' # IDL (%s) can not be found.\n' % filename)
                        raise FileNotFoundError
                    self.parse_idl(idl_path=p)

                    inc_lines = []
                    f = open(p, 'r')
                    for l in f:
                        inc_lines.append(l)
                    inc_lines = self._clear_comments(inc_lines)
                    inc_lines = self._paste_include(inc_lines)
                    output_lines = output_lines + inc_lines

                elif line.find('<') >= 7:
                    filename = line[line.find('<') + 1: line.rfind('>')]
                    if self._verbose:
                        sys.stdout.write(' -- Includes %s\n' % filename)
                    p = self._find_idl(filename, _include_paste)
                    if p is None:
                        sys.stdout.write(' # IDL (%s) can not be found.\n' % filename)
                        continue
                    inc_lines = []

                    self.parse_idl(idl_path=p)

                    f = open(p, 'r')
                    for l in f:
                        inc_lines.append(l)
                    inc_lines = self._clear_comments(inc_lines)
                    inc_lines = self._paste_include(inc_lines)
                    output_lines = output_lines + inc_lines

            else:
                output_line = line

            output_lines.append(output_line)

        return output_lines

    def _clear_comments(self, lines):
        output_lines = []
        in_comment = False

        for line in lines:
            line = line.strip()
            output_line = ''
            if line.find('//') >= 0:
                line = line[:line.find('//')]

            for token in line.split(' '):

                if in_comment and token.find('*/') >= 0:
                    in_comment = False
                    output_line = output_line + ' ' + token[token.find('*/') + 2:].strip()

                elif in_comment:
                    continue

                elif token.startswith('//'):
                    break  # ignore this line

                elif token.find('/*') >= 0:
                    in_comment = True
                    output_line = output_line + ' ' + token[0: token.find('/*')]
                else:
                    if token.find('{') >= 0:
                        token = token.replace('{', ' { ')
                    if token.find(';') >= 0:
                        token = token.replace(';', ' ;')
                    if token.find('(') >= 0:
                        token = token.replace('(', ' ( ')
                    token = token.replace(',', ' , ')
                    token = token.replace(')', ' ) ')
                    token = token.replace('}', ' } ')
                    output_line = output_line + ' ' + token.strip()
            if len(output_line.strip()) > 0:
                output_lines.append(output_line.strip() + '\n')

        return output_lines

    def _clear_ifdef(self, lines):
        output_lines = []
        def_tokens = []
        global offset
        offset = 0

        def _parse(flag):
            global offset
            while offset < len(lines):
                line = lines[offset]
                if line.startswith('#define'):
                    def_token = line.split(' ')[1]
                    def_tokens.append(def_token)
                    offset = offset + 1
                elif line.startswith('#ifdef'):
                    def_token = line.split(' ')[1]
                    offset = offset + 1
                    _parse(def_token in def_tokens)

                elif line.startswith('#ifndef'):
                    def_token = line.split(' ')[1]
                    offset = offset + 1
                    _parse(not def_token in def_tokens)

                elif line.startswith('#endif'):
                    offset = offset + 1
                    return

                else:
                    offset = offset + 1
                    if flag:
                        output_lines.append(line)

        _parse(True)
        return output_lines

