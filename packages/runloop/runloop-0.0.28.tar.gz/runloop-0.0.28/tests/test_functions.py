import json
import pickle

from pydantic import BaseModel
from pytest import raises

from runloop import Scheduler, Session, SystemCoordinator


def test_runloop_function_simple_scalars():
    from runloop import function, runloop_manifest

    @function
    def fn1(name: str, age: int) -> int:
        pass

    test_fns = [x for x in runloop_manifest.functions if x.name == "fn1"][0]
    assert len(runloop_manifest.functions) > 0
    assert test_fns.name == "fn1"
    assert test_fns.module == "tests.test_functions"
    assert len(test_fns.parameters) == 2
    assert test_fns.parameters[0].name == "name"
    assert test_fns.parameters[0].type.type_name == "string"
    assert test_fns.parameters[1].name == "age"
    assert test_fns.parameters[1].type.type_name == "int"


def test_runloop_function_simple_model():
    from runloop import function, runloop_manifest

    class Simple(BaseModel):
        height: str
        weight: int

    @function
    def fn2(name: str, m1: Simple) -> int:
        pass

    test_fns = [x for x in runloop_manifest.functions if x.name == "fn2"][0]
    assert len(runloop_manifest.functions) > 0
    assert test_fns.name == "fn2"
    assert test_fns.module == "tests.test_functions"

    assert len(test_fns.parameters) == 2
    assert test_fns.parameters[0].name == "name"
    assert test_fns.parameters[0].type.type_name == "string"
    assert test_fns.parameters[1].name == "m1"
    # Validate children
    assert len(test_fns.parameters[1].type.model.children) == 2
    assert test_fns.parameters[1].type.model.children[0].name == "height"
    assert test_fns.parameters[1].type.model.children[0].type.type_name == "string"
    assert test_fns.parameters[1].type.model.children[1].name == "weight"
    assert test_fns.parameters[1].type.model.children[1].type.type_name == "int"


def test_runloop_function_nested_model():
    from runloop import function, runloop_manifest

    class Simple(BaseModel):
        height: str
        weight: int

    class Nested(BaseModel):
        simple: Simple
        name: str

    @function
    def fn3(name: str, m1: Nested) -> int:
        pass

    test_fns = [x for x in runloop_manifest.functions if x.name == "fn3"][0]
    assert len(runloop_manifest.functions) > 0
    assert test_fns.name == "fn3"
    assert test_fns.module == "tests.test_functions"

    assert len(test_fns.parameters) == 2
    assert test_fns.parameters[0].name == "name"
    assert test_fns.parameters[0].type.type_name == "string"
    assert test_fns.parameters[1].name == "m1"
    assert test_fns.parameters[1].type.type_name == "model"
    # Validate children
    assert len(test_fns.parameters[1].type.model.children) == 2
    assert test_fns.parameters[1].type.model.children[0].name == "simple"
    assert test_fns.parameters[1].type.model.children[0].type.type_name == "model"
    assert len(test_fns.parameters[1].type.model.children[0].type.model.children) == 2
    assert test_fns.parameters[1].type.model.children[0].type.model.children[0].name == "height"
    assert test_fns.parameters[1].type.model.children[0].type.model.children[0].type.type_name == "string"
    assert test_fns.parameters[1].type.model.children[0].type.model.children[1].name == "weight"
    assert test_fns.parameters[1].type.model.children[0].type.model.children[1].type.type_name == "int"
    assert test_fns.parameters[1].type.model.children[1].name == "name"
    assert test_fns.parameters[1].type.model.children[1].type.type_name == "string"


def test_runloop_dict_str_str():
    from runloop import function, runloop_manifest

    @function
    def fn4(dict_arg: dict[str, str]) -> int:
        pass

    test_fns = [x for x in runloop_manifest.functions if x.name == "fn4"][0]
    assert len(runloop_manifest.functions) > 0
    assert test_fns.name == "fn4"
    assert test_fns.module == "tests.test_functions"

    assert len(test_fns.parameters) == 1
    assert test_fns.parameters[0].name == "dict_arg"
    assert test_fns.parameters[0].type.type_name == "dictionary"
    assert test_fns.parameters[0].type.dictionary.key_type.type_name == "string"
    assert test_fns.parameters[0].type.dictionary.value_type.type_name == "string"


# TODO: Restore typed_dicts
# def test_typed_dict():
#     from typing import TypedDict
#
#     from runloop import function, runloop_manifest
#
#     class TypedDictInput(TypedDict):
#         name: str
#         age: int
#
#     @function
#     def typed_dict1(dict_arg: TypedDictInput) -> int:
#         pass
#
#     test_fns = [x for x in runloop_manifest.functions if x.name == "typed_dict1"][0]
#     assert len(runloop_manifest.functions) > 0
#     assert test_fns.name == "typed_dict1"
#     assert test_fns.module == "tests.test_functions"
#
#     assert len(test_fns.parameters) == 1
#     assert test_fns.parameters[0].name == "dict_arg"
#     assert test_fns.parameters[0].type.type_name == "typed_dictionary"
#     assert test_fns.parameters[0].type.typed_dictionary.children[0].name == "name"
#     assert test_fns.parameters[0].type.typed_dictionary.children[0].type.type_name == "string"
#     assert test_fns.parameters[0].type.typed_dictionary.children[1].name == "age"
#     assert test_fns.parameters[0].type.typed_dictionary.children[1].type.type_name == "int"
#
#     class TypedDictNested(TypedDict):
#         a1: list[TypedDictInput]
#
#     @function
#     def typed_dict2(d2: TypedDictNested) -> int:
#         pass
#
#     test_fns = [x for x in runloop_manifest.functions if x.name == "typed_dict2"][0]
#     assert len(runloop_manifest.functions) > 0
#     assert test_fns.name == "typed_dict2"
#     assert test_fns.module == "tests.test_functions"
#
#     assert len(test_fns.parameters) == 1
#     assert test_fns.parameters[0].name == "d2"
#     assert test_fns.parameters[0].type.type_name == "typed_dictionary"
#     assert test_fns.parameters[0].type.typed_dictionary.children[0].name == "a1"
#     assert test_fns.parameters[0].type.typed_dictionary.children[0].type.type_name == "array"
#     a1 = test_fns.parameters[0].type.typed_dictionary.children[0]
#     assert a1.type.array.element_type.type_name == "typed_dictionary"
#     assert a1.type.array.element_type.typed_dictionary.children[0].name == "name"
#     assert a1.type.array.element_type.typed_dictionary.children[0].type.type_name == "string"
#
#     @function
#     def typed_dict3(i1: int) -> TypedDictNested:
#         pass
#
#     test_fns = [x for x in runloop_manifest.functions if x.name == "typed_dict3"][0]
#     assert len(runloop_manifest.functions) > 0
#     assert test_fns.name == "typed_dict3"
#
#     assert test_fns.return_type.type_name == "typed_dictionary"
#     assert test_fns.return_type.typed_dictionary.children[0].name == "a1"
#     assert test_fns.return_type.typed_dictionary.children[0].type.type_name == "array"
#     a1 = test_fns.return_type.typed_dictionary.children[0]
#     assert a1.type.array.element_type.type_name == "typed_dictionary"
#     assert a1.type.array.element_type.typed_dictionary.children[0].name == "name"
#     assert a1.type.array.element_type.typed_dictionary.children[0].type.type_name == "string"


def test_runloop_dict_str_simple_model():
    from runloop import function, runloop_manifest

    class Simple(BaseModel):
        height: str
        weight: int

    @function
    def fn5(dict_arg: dict[str, Simple]) -> int:
        pass

    test_fns = [x for x in runloop_manifest.functions if x.name == "fn5"][0]
    assert len(runloop_manifest.functions) > 0
    assert test_fns.name == "fn5"
    assert test_fns.module == "tests.test_functions"

    assert len(test_fns.parameters) == 1
    assert test_fns.parameters[0].name == "dict_arg"
    assert test_fns.parameters[0].type.type_name == "dictionary"
    assert test_fns.parameters[0].type.dictionary.key_type.type_name == "string"
    assert test_fns.parameters[0].type.dictionary.value_type.type_name == "model"

    # Validate children
    assert len(test_fns.parameters[0].type.dictionary.value_type.model.children) == 2
    assert test_fns.parameters[0].type.dictionary.value_type.model.children[0].name == "height"
    assert test_fns.parameters[0].type.dictionary.value_type.model.children[0].type.type_name == "string"
    assert test_fns.parameters[0].type.dictionary.value_type.model.children[1].name == "weight"
    assert test_fns.parameters[0].type.dictionary.value_type.model.children[1].type.type_name == "int"


def test_runloop_dict_no_types_throws():
    from runloop import function

    with raises(TypeError):

        @function
        def fn6(_: dict) -> int:
            pass


def test_runloop_array_str():
    from runloop import function, runloop_manifest

    @function
    def fn7(array_arg: list[str]) -> int:
        pass

    test_fns = [x for x in runloop_manifest.functions if x.name == "fn7"][0]
    assert test_fns.name == "fn7"
    assert test_fns.module == "tests.test_functions"

    assert len(test_fns.parameters) == 1
    assert test_fns.parameters[0].name == "array_arg"
    assert test_fns.parameters[0].type.type_name == "array"
    assert test_fns.parameters[0].type.array.element_type.type_name == "string"


def test_runloop_array_nested_model():
    from runloop import function, runloop_manifest

    class Simple(BaseModel):
        height: str
        weight: int

    @function
    def fn8(array_arg: list[Simple]) -> int:
        pass

    test_fns = [x for x in runloop_manifest.functions if x.name == "fn8"][0]
    assert test_fns.name == "fn8"
    assert test_fns.module == "tests.test_functions"

    assert len(test_fns.parameters) == 1
    assert test_fns.parameters[0].name == "array_arg"
    assert test_fns.parameters[0].type.type_name == "array"
    assert test_fns.parameters[0].type.array.element_type.type_name == "model"

    assert len(test_fns.parameters[0].type.array.element_type.model.children) == 2
    assert test_fns.parameters[0].type.array.element_type.model.children[0].name == "height"
    assert test_fns.parameters[0].type.array.element_type.model.children[0].type.type_name == "string"
    assert test_fns.parameters[0].type.array.element_type.model.children[1].name == "weight"
    assert test_fns.parameters[0].type.array.element_type.model.children[1].type.type_name == "int"


def test_runloop_list_no_types_throws():
    from runloop import function

    with raises(TypeError):

        @function
        def fn9(_: list) -> int:
            pass


def test_runloop_return_type_simple():
    from runloop import function, runloop_manifest

    @function
    def fn10(arg1: int) -> int:
        pass

    test_fns = [x for x in runloop_manifest.functions if x.name == "fn10"][0]
    assert test_fns.name == "fn10"
    assert test_fns.return_type.type_name == "int"

    @function
    def fn11(arg1: int) -> bool:
        pass

    test_fns = [x for x in runloop_manifest.functions if x.name == "fn11"][0]
    assert test_fns.name == "fn11"
    assert test_fns.return_type.type_name == "boolean"

    @function
    def fn12(arg1: int) -> str:
        pass

    test_fns = [x for x in runloop_manifest.functions if x.name == "fn12"][0]
    assert test_fns.name == "fn12"
    assert test_fns.return_type.type_name == "string"


def test_runloop_return_type_complex():
    from runloop import function, runloop_manifest

    @function
    def fn_cplx_1(arg1: int) -> list[str]:
        pass

    test_fns = [x for x in runloop_manifest.functions if x.name == "fn_cplx_1"][0]
    assert test_fns.name == "fn_cplx_1"
    assert test_fns.return_type.type_name == "array"
    assert test_fns.return_type.array.element_type.type_name == "string"

    class Simple(BaseModel):
        height: str
        weight: int

    @function
    def fn_cplx_2(arg1: int) -> Simple:
        pass

    test_fns = [x for x in runloop_manifest.functions if x.name == "fn_cplx_2"][0]
    assert test_fns.name == "fn_cplx_2"
    assert test_fns.return_type.type_name == "model"
    assert len(test_fns.return_type.model.children) == 2
    assert test_fns.return_type.model.children[0].name == "height"
    assert test_fns.return_type.model.children[0].type.type_name == "string"
    assert test_fns.return_type.model.children[1].name == "weight"
    assert test_fns.return_type.model.children[1].type.type_name == "int"


def test_runloop_return_type_none():
    from runloop import function, runloop_manifest

    @function
    def fn_empty_1(arg1: int) -> None:
        pass

    test_fns = [x for x in runloop_manifest.functions if x.name == "fn_empty_1"][0]
    assert test_fns.name == "fn_empty_1"
    assert test_fns.return_type.type_name == "null"

    @function
    def fn_empty_2(arg1: int):
        pass

    test_fns = [x for x in runloop_manifest.functions if x.name == "fn_empty_2"][0]
    assert test_fns.name == "fn_empty_2"
    assert test_fns.return_type.type_name == "null"


def test_runloop_session_parameter():
    from runloop import Session, function, runloop_manifest

    class Thread(BaseModel):
        name: str
        message_count: int

    @function
    def fn_return_session_1(session1: Session[Thread]) -> int:
        pass

    test_fns = [x for x in runloop_manifest.functions if x.name == "fn_return_session_1"][0]
    assert test_fns.name == "fn_return_session_1"
    assert test_fns.parameters[0].name == "session1"
    assert test_fns.parameters[0].type.type_name == "session"
    assert test_fns.parameters[0].type.session.kv_type.type_name == "model"
    assert test_fns.parameters[0].type.session.kv_type.model.children[0].name == "name"
    assert test_fns.parameters[0].type.session.kv_type.model.children[0].type.type_name == "string"
    assert test_fns.parameters[0].type.session.kv_type.model.children[1].name == "message_count"
    assert test_fns.parameters[0].type.session.kv_type.model.children[1].type.type_name == "int"


def test_runloop_async_function():
    from runloop import function, runloop_manifest

    @function
    def fn_async_empty(arg1: int) -> None:
        pass

    test_fns = [x for x in runloop_manifest.functions if x.name == "fn_async_empty"][0]
    assert test_fns.name == "fn_async_empty"
    assert test_fns.return_type.type_name == "null"

    @function
    def fn_async_non_empty(echo: str) -> str:
        return echo

    test_fns = [x for x in runloop_manifest.functions if x.name == "fn_async_non_empty"][0]
    assert test_fns.name == "fn_async_non_empty"
    assert test_fns.return_type.type_name == "string"


def test_runloop_function_invocation_scalars():
    from runloop import function

    @function
    def fn_invocation_1(i1: int, i2: int) -> int:
        return i1 + i2

    # Call function with *args
    invocation = fn_invocation_1(1, 2)
    assert invocation.invoke() == 3
    assert json.loads(invocation.parameters()) == {
        "i1": 1,
        "i2": 2,
    }

    # Call function with **kwargs
    invocation2 = fn_invocation_1(i1=3, i2=4)
    assert invocation2.invoke() == 7
    assert json.loads(invocation2.parameters()) == {
        "i1": 3,
        "i2": 4,
    }

    # Call function with mixed
    invocation3 = fn_invocation_1(5, i2=6)
    assert invocation3.invoke() == 11
    assert json.loads(invocation3.parameters()) == {
        "i1": 5,
        "i2": 6,
    }

    @function
    def async_invocation_1(i1: int, i2: int) -> int:
        return i1 + i2

    # Call function with *args
    async1 = async_invocation_1(12, 1)
    assert async1.invoke() == 13
    assert json.loads(async1.parameters()) == {
        "i1": 12,
        "i2": 1,
    }

    # Call function with *args
    async2 = async_invocation_1(i1=13, i2=2)
    assert async2.invoke() == 15
    assert json.loads(async2.parameters()) == {
        "i1": 13,
        "i2": 2,
    }

    # Call function with mixed
    invocation3 = async_invocation_1(5, i2=7)
    assert invocation3.invoke() == 12
    assert json.loads(invocation3.parameters()) == {
        "i1": 5,
        "i2": 7,
    }


def test_runloop_function_invocation_models():
    from runloop import function

    class Simple(BaseModel):
        height: str
        weight: int

    @function
    def fn_models_1(i1: Simple) -> int:
        return i1.weight

    # Call function with *args
    invocation = fn_models_1(Simple(height="tall", weight=200))
    assert invocation.invoke() == 200

    # Call function with **kwargs
    invocation2 = fn_models_1(i1=Simple(height="short", weight=100))
    assert invocation2.invoke() == 100

    @function
    def fn_models_2(i1: int) -> Simple:
        return Simple(height="tall", weight=i1)

    # Call function with *args
    invocation3 = fn_models_2(200)
    assert invocation3.invoke() == Simple(height="tall", weight=200)

    # Call function with **kwargs
    invocation4 = fn_models_2(i1=100)
    assert invocation4.invoke() == Simple(height="tall", weight=100)
    assert invocation4.session_id is None


def test_runloop_function_invocation_session():
    """Validate calling function with session ignores session for now in invocation."""
    from runloop import function

    class SessionImpl(Session[dict[str, str]]):
        def commit_session(self) -> None:
            pass

    @function
    def fn_session_1(i1: Session[dict[str, str]], i2: int) -> int:
        return i2

    # Call function with *args
    invocation = fn_session_1(SessionImpl(id="123", kv={}), 200)
    assert invocation.invoke() == 200
    assert json.loads(invocation.parameters()) == {
        "i2": 200,
    }
    assert invocation.session_id == "123"


def test_scheduler():
    from runloop import function, runloop_manifest

    @function
    def fn_scheduler(scheduler: Scheduler) -> int:
        return 0

    test_fns = [x for x in runloop_manifest.functions if x.name == "fn_scheduler"][0]
    assert test_fns.name == "fn_scheduler"
    assert test_fns.return_type.type_name == "int"
    assert len(test_fns.parameters) == 1
    assert test_fns.parameters[0].name == "scheduler"


def test_system_coordinator():
    from runloop import function, runloop_manifest

    @function
    def fn_system_coordinator(system_coordinator: SystemCoordinator) -> int:
        return 0

    test_fns = [x for x in runloop_manifest.functions if x.name == "fn_system_coordinator"][0]
    assert test_fns.name == "fn_system_coordinator"
    assert test_fns.return_type.type_name == "int"
    assert len(test_fns.parameters) == 1
    assert test_fns.parameters[0].name == "system_coordinator"
    assert test_fns.parameters[0].type.type_name == "system_coordinator"


def test_json_schema():
    from runloop import function, runloop_manifest

    class Simple(BaseModel):
        height: str
        weight: int

    @function
    def schema_test_fn(my_param1: str, my_param2: int, scheduler: Scheduler) -> Simple:
        return Simple(height="tall", weight=200)

    test_fns = [x for x in runloop_manifest.functions if x.name == "schema_test_fn"][0]
    assert test_fns.name == "schema_test_fn"
    assert (
        test_fns.rpc_json_schema.request_json_schema
        == '{"properties": {"my_param1": {"title": "My Param1", "type": "string"}, "my_param2": {"title": "My Param2", "type": "integer"}}, "required": ["my_param1", "my_param2"], "title": "schema_test_fnRequestModel", "type": "object"}'  # noqa: E501
    )
    assert (
        test_fns.rpc_json_schema.response_json_schema
        == '{"properties": {"height": {"title": "Height", "type": "string"}, "weight": {"title": "Weight", "type": "integer"}}, "required": ["height", "weight"], "title": "Simple", "type": "object"}'  # noqa: E501
    )

    @function
    def schema_test_fn2(my_param1: Simple, my_param2: Session[Simple]) -> int:
        return 1

    test_fns = [x for x in runloop_manifest.functions if x.name == "schema_test_fn2"][0]
    assert test_fns.name == "schema_test_fn2"
    assert (
        test_fns.rpc_json_schema.request_json_schema
        == '{"$defs": {"Simple": {"properties": {"height": {"title": "Height", "type": "string"}, "weight": {"title": "Weight", "type": "integer"}}, "required": ["height", "weight"], "title": "Simple", "type": "object"}}, "properties": {"my_param1": {"$ref": "#/$defs/Simple"}}, "required": ["my_param1"], "title": "schema_test_fn2RequestModel", "type": "object"}'  # noqa: E501
    )
    assert test_fns.rpc_json_schema.response_json_schema == '{"type": "integer"}'


def _is_pickleable(obj):
    try:
        pickle.dumps(obj)
        return True
    except (pickle.PicklingError, TypeError) as e:
        print(e)
        return False


# TODO: Wrapped functions are not pickleable
# def test_function_pickleable():
#     """Validate calling function with session ignores session for now in invocation."""
#     from runloop import function
#     from tests.user.simple.simple_function import simple_echo
#
#     # assert _is_pickleable(pickle_me_scalar_1)
#     assert _is_pickleable(simple_echo.fn())
