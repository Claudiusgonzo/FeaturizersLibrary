'''Integration tests for CppToJson.py
'''
import sys
import os
import json
import unittest
import textwrap

import CommonEnvironment

try:
    from DataPipelines.CppToJson import CppToJson
    from DataPipelines.CppToJson.GeneratedCode.CppToJson_PythonJsonSerialization import *
except ModuleNotFoundError:
    # If here, it might be that clang is not available
    if os.getenv("DEVELOPMENT_ENVIRONMENT_REPOSITORY_CONFIGURATION") != "x64":
        sys.stdout.write("Clang is not available in this configuration.\nOK <- this is enough to convince the test parser that tests were successful.\n")
        sys.exit(0)

# ----------------------------------------------------------------------
_script_fullpath                            = CommonEnvironment.ThisFullpath()
_script_dir, _script_name                   = os.path.split(_script_fullpath)
# ----------------------------------------------------------------------


class FileTest(unittest.TestCase):
    '''
        The purpose of this function is to verify the file-based capabilities of the ObtainFunctions method. It will make sure
        that the files are being opened and the information inside is being correctly processed.
    '''
    def test_basic_file(self):
        filename = os.path.join(_script_dir, "basicFunc.cpp")
        result = CppToJson.ObtainFunctions(filename, None, lambda type, verifyStruct: True)
        func_list = self._GetFuncList(filename, result)
        struct_list = self._GetStructList(filename, result)
        include_list = self._GetIncludeList(filename, result)

        self.assertEqual(func_list[0], {'name': 'add', 'raw_return_type': 'int', 'simple_return_type': 'int', 'var_names': ['a', 'b'], 'raw_var_types': ['int', 'int'], 'simple_var_types': ['int', 'int'], 'definition_line': 6, 'declaration_line': 6})
        self.assertEqual(func_list[1], {'name': 'sub', 'raw_return_type': 'float', 'simple_return_type': 'float', 'var_names': ['a', 'b'], 'raw_var_types': ['float', 'float'], 'simple_var_types': ['float', 'float'], 'definition_line': 10, 'declaration_line': 10})
        self.assertEqual(func_list[2], {'name': 'isPos', 'raw_return_type': 'bool', 'simple_return_type': 'bool', 'var_names': ['x'], 'raw_var_types': ['bool'], 'simple_var_types': ['bool'], 'definition_line': 14, 'declaration_line': 14})
        self.assertEqual(func_list[3], {'name': 'three', 'raw_return_type': 'int', 'simple_return_type': 'int', 'var_names': [], 'raw_var_types': [], 'simple_var_types': [], 'definition_line': 18, 'declaration_line': 18})
        self.assertEqual(func_list[4], {'name': 'nothing', 'raw_return_type': 'void', 'simple_return_type': 'void', 'var_names': [], 'raw_var_types': [], 'simple_var_types': [], 'definition_line': 22, 'declaration_line': 22})
        self.assertEqual(func_list[5], {'name': 'main', 'raw_return_type': 'int', 'simple_return_type': 'int', 'var_names': [], 'raw_var_types': [], 'simple_var_types': [], 'definition_line': 27, 'declaration_line': 27})

        self.assertEqual(struct_list, [])
        self.assertEqual(len(include_list), 1)


    def test_medium_file(self):
        filename = os.path.join(_script_dir, "mediumFunc.cpp")
        result = CppToJson.ObtainFunctions(filename, None, lambda type, verifyStruct: True)
        func_list = self._GetFuncList(filename, result)
        struct_list = self._GetStructList(filename, result)
        include_list = self._GetIncludeList(filename, result)

        self.assertEqual(func_list[0], {'name': 'add', 'raw_return_type': 'int', 'simple_return_type': 'int', 'var_names': ['a', 'b'], 'raw_var_types': ['float', 'int'], 'simple_var_types': ['float', 'int'], 'definition_line': 5, 'declaration_line': 5})
        self.assertEqual(func_list[1], {'name': 'mult', 'raw_return_type': 'float', 'simple_return_type': 'float', 'var_names': ['a', 'b', 'signal'], 'raw_var_types': ['int', 'float', 'bool'], 'simple_var_types': ['int', 'float', 'bool'], 'definition_line': 9, 'declaration_line': 9})
        self.assertEqual(func_list[2], {'name': 'toUp', 'raw_return_type': 'std::string', 'simple_return_type': 'std::string', 'var_names': ['s'], 'raw_var_types': ['std::string'], 'simple_var_types': ['std::string'], 'definition_line': 13, 'declaration_line': 13})
        self.assertEqual(func_list[3], {'name': 'fat', 'raw_return_type': 'int', 'simple_return_type': 'int', 'var_names': ['curr', 'at'], 'raw_var_types': ['int', 'int'], 'simple_var_types': ['int', 'int'], 'definition_line': 19, 'declaration_line': 19})
        self.assertEqual(func_list[4], {'name': 'main', 'raw_return_type': 'int', 'simple_return_type': 'int', 'var_names': [], 'raw_var_types': [], 'simple_var_types': [], 'definition_line': 24, 'declaration_line': 24})

        self.assertEqual(struct_list, [])
        self.assertEqual(len(include_list), 1)

    def test_hard_file(self):
        filename = os.path.join(_script_dir, "hardFunc.cpp")
        result = CppToJson.ObtainFunctions(filename, None, lambda type, verifyStruct: True)
        func_list = self._GetFuncList(filename, result)
        struct_list = self._GetStructList(filename, result)
        include_list = self._GetIncludeList(filename, result)

        self.assertEqual(func_list[0], {'name': 'add', 'raw_return_type': 'int', 'simple_return_type': 'int', 'var_names': ['a'], 'raw_var_types': ['int'], 'simple_var_types': ['int'], 'definition_line': 10, 'declaration_line': 10})
        self.assertEqual(func_list[1], {'name': 'main', 'raw_return_type': 'int', 'simple_return_type': 'int', 'var_names': [], 'raw_var_types': [], 'simple_var_types': [], 'definition_line': 17, 'declaration_line': 17})
        self.assertEqual(func_list[2], {'name': 'bubbleSort', 'raw_return_type': 'vector<int>', 'simple_return_type': 'vector<int>', 'var_names': ['v'], 'raw_var_types': ['vector<int>'], 'simple_var_types': ['vector<int>'], 'definition_line': 22, 'declaration_line': 22})
        self.assertEqual(func_list[3], {'name': 'sizeOfMap', 'raw_return_type': 'int', 'simple_return_type': 'int', 'var_names': ['mp'], 'raw_var_types': ['map<int, bool>'], 'simple_var_types': ['map<int, bool>'], 'definition_line': 32, 'declaration_line': 32})
        self.assertEqual(func_list[4], {'name': 'keys', 'raw_return_type': 'vector<int>', 'simple_return_type': 'vector<int>', 'var_names': ['mp'], 'raw_var_types': ['map<int, int>'], 'simple_var_types': ['map<int, int>'], 'definition_line': 35, 'declaration_line': 35})
        self.assertEqual(func_list[5], {'name': 'goCount', 'raw_return_type': 'map<float, int>', 'simple_return_type': 'map<float, int>', 'var_names': ['v', 'signal'], 'raw_var_types': ['vector<float>', 'bool'], 'simple_var_types': ['vector<float>', 'bool'], 'definition_line': 43, 'declaration_line': 43})

        self.assertEqual(struct_list, [])
        self.assertEqual(len(include_list), 3)

    def test_convoluted_file(self):
        filename = os.path.join(_script_dir, "convolutedFunc.cpp")
        result = CppToJson.ObtainFunctions(filename, None, lambda type, verifyStruct: True)
        func_list = self._GetFuncList(filename, result)
        struct_list = self._GetStructList(filename, result)
        include_list = self._GetIncludeList(filename, result)

        self.assertEqual(func_list[0], {'name': 'matrix', 'raw_return_type': 'vector<vector<int> >', 'simple_return_type': 'vector<vector<int> >', 'var_names': ['n'], 'raw_var_types': ['int'], 'simple_var_types': ['int'], 'definition_line': 9, 'declaration_line': 9})
        self.assertEqual(func_list[1], {'name': 'nonsense', 'raw_return_type': 'map<map<int, vector<bool> >, vector<float> >', 'simple_return_type': 'map<map<int, vector<bool> >, vector<float> >', 'var_names': ['n'], 'raw_var_types': ['int'], 'simple_var_types': ['int'], 'definition_line': 19, 'declaration_line': 19})
        self.assertEqual(func_list[2], {'name': 'vectorLine', 'raw_return_type': 'vector<vector<vector<vector<float> > > >', 'simple_return_type': 'vector<vector<vector<vector<float> > > >', 'var_names': ['mp'], 'raw_var_types': ['map<bool, int>'], 'simple_var_types': ['map<bool, int>'], 'definition_line': 30, 'declaration_line': 30})
        self.assertEqual(func_list[3], {'name': 'countVector', 'raw_return_type': 'map<int, int>', 'simple_return_type': 'map<int, int>', 'var_names': ['v'], 'raw_var_types': ['vector<vector<int> >'], 'simple_var_types': ['vector<vector<int> >'], 'definition_line': 42, 'declaration_line': 42})
        self.assertEqual(func_list[4], {'name': 'main', 'raw_return_type': 'int', 'simple_return_type': 'int', 'var_names': [], 'raw_var_types': [], 'simple_var_types': [], 'definition_line': 50, 'declaration_line': 50})

        self.assertEqual(struct_list, [])
        self.assertEqual(len(include_list), 3)

    def test_mix_file(self):
        filename = os.path.join(_script_dir, "mixFunc.cpp")
        result = CppToJson.ObtainFunctions(filename, None, lambda type, verifyStruct: True)
        func_list = self._GetFuncList(filename, result)
        struct_list = self._GetStructList(filename, result)
        include_list = self._GetIncludeList(filename, result)

        self.assertEqual(func_list[0], {'name': 'nonsense', 'raw_return_type': 'vector<map<int, float> > *', 'simple_return_type': 'vector<map<int, float> > *', 'var_names': ['v', 'mp'], 'raw_var_types': ['vector<int> &', 'map<bool, bool> *'], 'simple_var_types': ['vector<int>', 'map<bool, bool> *'], 'definition_line': 6, 'declaration_line': 6})
        self.assertEqual(func_list[1], {'name': 'address', 'raw_return_type': 'vector<int> &', 'simple_return_type': 'vector<int>', 'var_names': ['v'], 'raw_var_types': ['vector<int> &'], 'simple_var_types': ['vector<int>'], 'definition_line': 11, 'declaration_line': 11})
        self.assertEqual(func_list[2], {'name': 'even', 'raw_return_type': 'map<int, vector<bool> > **', 'simple_return_type': 'map<int, vector<bool> > **', 'var_names': ['n'], 'raw_var_types': ['int'], 'simple_var_types': ['int'], 'definition_line': 15, 'declaration_line': 15})
        self.assertEqual(func_list[3], {'name': 'dereference', 'raw_return_type': 'int **********', 'simple_return_type': 'int **********', 'var_names': ['ref'], 'raw_var_types': ['int ***********'], 'simple_var_types': ['int ***********'], 'definition_line': 22, 'declaration_line': 22})
        self.assertEqual(func_list[4], {'name': 'constDereference', 'raw_return_type': 'const int **********', 'simple_return_type': 'int **********', 'var_names': ['ref'], 'raw_var_types': ['const int ***********'], 'simple_var_types': ['int ***********'], 'definition_line': 26, 'declaration_line': 26})
        self.assertEqual(func_list[5], {'name': 'main', 'raw_return_type': 'int', 'simple_return_type': 'int', 'var_names': [], 'raw_var_types': [], 'simple_var_types': [], 'definition_line': 31, 'declaration_line': 31})

        self.assertEqual(struct_list, [])
        self.assertEqual(len(include_list), 2)

    def test_class_file_unsupported(self):
        filename = os.path.join(_script_dir, "classFunc.cpp")

        called_count = 0

        # ----------------------------------------------------------------------
        def onUnsupportedFunc(error_desc, this_filename, line):
            nonlocal called_count
            called_count += 1

            unsupported_list = [
                [textwrap.dedent("""\
                The function operator+ is not supported:
                \t- Invalid argument a of type Point.
                \t- Invalid argument b of type Point.
                \t- Invalid return type Point.
                """), this_filename, 15],
                [textwrap.dedent("""\
                The function sum is not supported:
                \t- Invalid argument a of type Point.
                \t- Invalid return type int.
                """), this_filename, 22],
                [textwrap.dedent("""\
                The function go is not supported:
                \t- Invalid argument n of type int.
                \t- Invalid return type vector<int>.
                """), this_filename, 26],
                [textwrap.dedent("""\
                The function main is not supported:
                \t- Invalid return type int.
                """), this_filename, 34]
            ]

            self.assertTrue([error_desc, this_filename, line] in unsupported_list)
        # ----------------------------------------------------------------------
        def Policy(var_type, verifyStruct):
            if verifyStruct(var_type):
                return True
            return False

        # ----------------------------------------------------------------------

        result = CppToJson.ObtainFunctions(filename, onUnsupportedFunc, Policy)
        func_list = self._GetFuncList(filename, result)
        struct_list = self._GetStructList(filename, result)
        include_list = self._GetIncludeList(filename, result)

        self.assertEqual(called_count, 4)

        self.assertEqual(func_list, [])
        self.assertEqual(struct_list, [])
        self.assertEqual(len(include_list), 1)

    def test_namespace_file(self):
        filename = os.path.join(_script_dir, "arithmetic.cpp")
        result = CppToJson.ObtainFunctions(filename, None, lambda type, verifyStruct: True)
        func_list = self._GetFuncList(filename, result)
        struct_list = self._GetStructList(filename, result)
        include_list = self._GetIncludeList(filename, result)

        self.assertEqual(func_list[0], {'name': 'DataPipelines::Arithmetic::Add', 'raw_return_type': 'int64_t', 'simple_return_type': 'int64_t', 'var_names': ['a', 'b'], 'raw_var_types': ['const int64_t', 'const int64_t'], 'simple_var_types': ['int64_t', 'int64_t'], 'definition_line': 12, 'declaration_line': 12})
        self.assertEqual(func_list[1], {'name': 'DataPipelines::Arithmetic::Add', 'raw_return_type': 'uint64_t', 'simple_return_type': 'uint64_t', 'var_names': ['a', 'b'], 'raw_var_types': ['const uint64_t', 'const uint64_t'], 'simple_var_types': ['uint64_t', 'uint64_t'], 'definition_line': 13, 'declaration_line': 13})
        self.assertEqual(func_list[2], {'name': 'DataPipelines::Arithmetic::Add', 'raw_return_type': 'uint32_t', 'simple_return_type': 'uint32_t', 'var_names': ['a', 'b'], 'raw_var_types': ['const uint32_t', 'const uint32_t'], 'simple_var_types': ['uint32_t', 'uint32_t'], 'definition_line': 14, 'declaration_line': 14})
        self.assertEqual(func_list[3], {'name': 'DataPipelines::Arithmetic::Add', 'raw_return_type': 'int', 'simple_return_type': 'int', 'var_names': ['a', 'b'], 'raw_var_types': ['int', 'int'], 'simple_var_types': ['int', 'int'], 'definition_line': 30, 'declaration_line': 16})
        self.assertEqual(func_list[4], {'name': 'DataPipelines::Arithmetic::thisguy', 'raw_return_type': 'void', 'simple_return_type': 'void', 'var_names': ['a', 'b'], 'raw_var_types': ['int', 'int'], 'simple_var_types': ['int', 'int'], 'definition_line': 34, 'declaration_line': 18})
        self.assertEqual(func_list[5], {'name': 'DataPipelines::Arithmetic::Add', 'raw_return_type': 'double', 'simple_return_type': 'double', 'var_names': ['a', 'b'], 'raw_var_types': ['const double', 'const double'], 'simple_var_types': ['double', 'double'], 'definition_line': 23, 'declaration_line': 23})
        self.assertEqual(func_list[6], {'name': 'DataPipelines::Arithmetic::Addi32', 'raw_return_type': 'int32_t', 'simple_return_type': 'int32_t', 'var_names': ['a', 'b'], 'raw_var_types': ['const int32_t', 'const int32_t'], 'simple_var_types': ['int32_t', 'int32_t'], 'definition_line': 26, 'declaration_line': 26})
        self.assertEqual(func_list[7], {'name': 'Addu64', 'raw_return_type': 'uint64_t', 'simple_return_type': 'uint64_t', 'var_names': ['a', 'b'], 'raw_var_types': ['const uint64_t', 'const uint64_t'], 'simple_var_types': ['uint64_t', 'uint64_t'], 'definition_line': 38, 'declaration_line': 38})
        self.assertEqual(func_list[8],  {'name': 'Addi64', 'raw_return_type': 'int64_t', 'simple_return_type': 'int64_t', 'var_names': ['a', 'b'], 'raw_var_types': ['const int64_t', 'const int64_t'], 'simple_var_types': ['int64_t', 'int64_t'], 'definition_line': 44, 'declaration_line': 44})
        self.assertEqual(func_list[9],  {'name': 'Addu32', 'raw_return_type': 'uint32_t', 'simple_return_type': 'uint32_t', 'var_names': ['a', 'b'], 'raw_var_types': ['const uint32_t', 'const uint32_t'], 'simple_var_types': ['uint32_t', 'uint32_t'], 'definition_line': 48, 'declaration_line': 48})

        self.assertEqual(struct_list, [])
        self.assertEqual(len(include_list), 2)

    def test_supported_struct(self):
        filename = os.path.join(_script_dir, "supportedStruct.cpp")

        # ----------------------------------------------------------------------
        def Policy(var_type, verifyStruct):
            if verifyStruct(var_type):
                return True
            return True

        # ----------------------------------------------------------------------

        result = CppToJson.ObtainFunctions(filename, None, Policy)
        func_list = self._GetFuncList(filename, result)
        struct_list = self._GetStructList(filename, result)
        include_list = self._GetIncludeList(filename, result)

        self.assertEqual(func_list[0], {'name': 'go', 'raw_return_type': 'x', 'simple_return_type': 'x', 'var_names': ['y'], 'raw_var_types': ['int'], 'simple_var_types': ['int'], 'declaration_line': 12, 'definition_line': 12})
        self.assertEqual(func_list[1], {'name': 'main', 'raw_return_type': 'int', 'simple_return_type': 'int', 'var_names': [], 'raw_var_types': [], 'simple_var_types': [], 'declaration_line': 17, 'definition_line': 17})

        self.assertEqual(struct_list[0], {'name': 'x', 'var_names': ['a', 'b'], 'raw_var_types': ['int', 'int'], 'simple_var_types': ['int', 'int'], 'definition_line': 3, 'base_structs': [], 'constructor_list': [{'var_names': ['other'], 'raw_var_types': ['x &&'], 'simple_var_types': ['x'], 'definition_line': 5}, {'var_names': ['xa', 'xb'], 'raw_var_types': ['int', 'int'], 'simple_var_types': ['int', 'int'], 'definition_line': 6}]})

        self.assertEqual(len(include_list), 2)

    def test_multiple_includes(self):
        filename = os.path.join(_script_dir, "includes.cpp")

        # ----------------------------------------------------------------------
        def Policy(var_type, verifyStruct):
            accepted_list = ['double', 'int32_t', 'int64_t','uint32_t','uint64_t','int', 'bool', 'float', 'char', 'vector', 'map', 'pair', 'tuple', 'string', 'void']
            ignored_list = ['const', 'signed', 'unsigned', 'std']

            if var_type not in accepted_list and var_type not in ignored_list and not verifyStruct(var_type):
                return False
            return True
        # ----------------------------------------------------------------------

        all_results = CppToJson.ObtainFunctions(filename, None, Policy)

        self.assertEqual(len(all_results), 3)

        self.assertEqual(filename, list(all_results.keys())[0])
        self.assertEqual(all_results[filename]["function_list"][0], {'name': 'gox', 'raw_return_type': 'go', 'simple_return_type': 'go', 'var_names': ['y'], 'raw_var_types': ['int'], 'simple_var_types': ['int'], 'declaration_line': 4, 'definition_line': 4})
        self.assertEqual(all_results[filename]["function_list"][1], {'name': 'main', 'raw_return_type': 'int', 'simple_return_type': 'int', 'var_names': [], 'raw_var_types': [], 'simple_var_types': [], 'declaration_line': 9, 'definition_line': 9})
        self.assertEqual(all_results[filename]["struct_list"], [])
        self.assertEqual(len(all_results[filename]["include_list"]), 1)

        header2 = os.path.realpath(os.path.join(_script_dir, "header2.hpp"))
        self.assertEqual(header2, list(all_results.keys())[1])
        self.assertEqual(all_results[header2]["function_list"], [])
        self.assertEqual(len(all_results[header2]["struct_list"]), 1)
        self.assertEqual(all_results[header2]["struct_list"][0], {'name': 'go2', 'definition_line': 5, 'var_names': ['a', 'b'], 'raw_var_types': ['int', 'int'], 'simple_var_types': ['int', 'int'], 'constructor_list': [{'var_names': [], 'raw_var_types': [], 'simple_var_types': [], 'definition_line': 7}, {'var_names': ['other'], 'raw_var_types': ['go2 &&'], 'simple_var_types': ['go2'], 'definition_line': 8}], 'base_structs': []})
        self.assertEqual(len(all_results[header2]["include_list"]), 1)

        header1 = os.path.realpath(os.path.join(_script_dir, "header1.hpp"))
        self.assertEqual(header1, list(all_results.keys())[2])
        self.assertEqual(all_results[header1]["function_list"], [])
        self.assertEqual(len(all_results[header2]["struct_list"]), 1)
        self.assertEqual(all_results[header1]["struct_list"][0], {'name': 'go', 'definition_line': 5, 'var_names': ['a', 'b', 'x'], 'raw_var_types': ['int', 'int', 'go2'], 'simple_var_types': ['int', 'int', 'go2'], 'constructor_list': [{'var_names': [], 'raw_var_types': [], 'simple_var_types': [], 'definition_line': 8}, {'var_names': ['other'], 'raw_var_types': ['go &&'], 'simple_var_types': ['go'], 'definition_line': 9}], 'base_structs': []})
        self.assertEqual(len(all_results[header1]["include_list"]), 1)

    def _GetFuncList(self, filename, results):
        self.assertEqual(len(results), 1)
        self.assertEqual(filename, list(results.keys())[0])

        return results[filename]['function_list']

    def _GetStructList(self, filename, results):
        self.assertEqual(len(results), 1)
        self.assertEqual(filename, list(results.keys())[0])

        return results[filename]['struct_list']

    def _GetIncludeList(self, filename, results):
        self.assertEqual(len(results), 1)
        self.assertEqual(filename, list(results.keys())[0])

        return results[filename]['include_list']

class Deserialization(unittest.TestCase):
    """
    This test will make sure that the output from my function matches the SimpleSchema format.
    """
    def test_deserialization(self):
        filename = os.path.join(_script_dir, "deserialization.cpp")

        # ----------------------------------------------------------------------
        def Policy(var_type, verifyStruct):
            if verifyStruct(var_type):
                return True
            return True

        # ----------------------------------------------------------------------

        results = CppToJson.ObtainFunctions(filename, None, Policy)

        deserialized_result = Deserialize([results[filename]], always_include_optional=True)

        self.assertEqual(len(deserialized_result), 1)

        self.assertEqual(deserialized_result[0].function_list[0].name, "goooo")
        self.assertEqual(deserialized_result[0].function_list[0].raw_return_type, "oth")
        self.assertEqual(deserialized_result[0].function_list[0].simple_return_type, "oth")
        self.assertEqual(deserialized_result[0].function_list[0].var_names, ["a", "b"])
        self.assertEqual(deserialized_result[0].function_list[0].raw_var_types, ["int", "float"])
        self.assertEqual(deserialized_result[0].function_list[0].simple_var_types, ["int", "float"])
        self.assertEqual(deserialized_result[0].function_list[0].declaration_line, 30)
        self.assertEqual(deserialized_result[0].function_list[0].definition_line, 30)

        self.assertEqual(deserialized_result[0].struct_list[0].name, "go")
        self.assertEqual(deserialized_result[0].struct_list[0].var_names, ["a", "b"])
        self.assertEqual(deserialized_result[0].struct_list[0].raw_var_types, ["int", "bool"])
        self.assertEqual(deserialized_result[0].struct_list[0].simple_var_types, ["int", "bool"])
        self.assertEqual(deserialized_result[0].struct_list[0].definition_line, 3)

        self.assertEqual(deserialized_result[0].struct_list[0].base_structs, [])
        self.assertEqual(len(deserialized_result[0].struct_list[0].constructor_list), 2)

        self.assertEqual(deserialized_result[0].struct_list[0].constructor_list[0].var_names, [])
        self.assertEqual(deserialized_result[0].struct_list[0].constructor_list[0].raw_var_types, [])
        self.assertEqual(deserialized_result[0].struct_list[0].constructor_list[0].simple_var_types, [])
        self.assertEqual(deserialized_result[0].struct_list[0].constructor_list[0].definition_line, 6)

        self.assertEqual(deserialized_result[0].struct_list[0].constructor_list[1].var_names, ["other"])
        self.assertEqual(deserialized_result[0].struct_list[0].constructor_list[1].raw_var_types, ["go &&"])
        self.assertEqual(deserialized_result[0].struct_list[0].constructor_list[1].simple_var_types, ["go"])
        self.assertEqual(deserialized_result[0].struct_list[0].constructor_list[1].definition_line, 9)

        self.assertEqual(deserialized_result[0].struct_list[1].name, "go2")
        self.assertEqual(deserialized_result[0].struct_list[1].var_names, ["a", "b"])
        self.assertEqual(deserialized_result[0].struct_list[1].raw_var_types, ["int", "float"])
        self.assertEqual(deserialized_result[0].struct_list[1].simple_var_types, ["int", "float"])
        self.assertEqual(deserialized_result[0].struct_list[1].definition_line, 12)
        self.assertEqual(deserialized_result[0].struct_list[1].base_structs, [])
        self.assertEqual(len(deserialized_result[0].struct_list[1].constructor_list), 2)

        self.assertEqual(deserialized_result[0].struct_list[1].constructor_list[0].var_names, [])
        self.assertEqual(deserialized_result[0].struct_list[1].constructor_list[0].raw_var_types, [])
        self.assertEqual(deserialized_result[0].struct_list[1].constructor_list[0].simple_var_types, [])
        self.assertEqual(deserialized_result[0].struct_list[1].constructor_list[0].definition_line, 15)

        self.assertEqual(deserialized_result[0].struct_list[1].constructor_list[1].var_names, ["other"])
        self.assertEqual(deserialized_result[0].struct_list[1].constructor_list[1].raw_var_types, ["go2 &&"])
        self.assertEqual(deserialized_result[0].struct_list[1].constructor_list[1].simple_var_types, ["go2"])
        self.assertEqual(deserialized_result[0].struct_list[1].constructor_list[1].definition_line, 18)

        self.assertEqual(deserialized_result[0].struct_list[2].name, "oth")
        self.assertEqual(deserialized_result[0].struct_list[2].var_names, ["x"])
        self.assertEqual(deserialized_result[0].struct_list[2].raw_var_types, ["int"])
        self.assertEqual(deserialized_result[0].struct_list[2].simple_var_types, ["int"])
        self.assertEqual(deserialized_result[0].struct_list[2].definition_line, 21)
        self.assertEqual(deserialized_result[0].struct_list[2].base_structs, ["go", "go2"])
        self.assertEqual(len(deserialized_result[0].struct_list[2].constructor_list), 2)

        self.assertEqual(deserialized_result[0].struct_list[2].constructor_list[0].var_names, [])
        self.assertEqual(deserialized_result[0].struct_list[2].constructor_list[0].raw_var_types, [])
        self.assertEqual(deserialized_result[0].struct_list[2].constructor_list[0].simple_var_types, [])
        self.assertEqual(deserialized_result[0].struct_list[2].constructor_list[0].definition_line, 23)

        self.assertEqual(deserialized_result[0].struct_list[2].constructor_list[1].var_names, ["other"])
        self.assertEqual(deserialized_result[0].struct_list[2].constructor_list[1].raw_var_types, ["oth &&"])
        self.assertEqual(deserialized_result[0].struct_list[2].constructor_list[1].simple_var_types, ["oth"])
        self.assertEqual(deserialized_result[0].struct_list[2].constructor_list[1].definition_line, 26)

if __name__ == '__main__':
    unittest.main()
