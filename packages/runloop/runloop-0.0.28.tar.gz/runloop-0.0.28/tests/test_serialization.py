import base64

import pydantic

from runloop.serialization import _concrete_to_json_compatible, value_to_json_string


def test_concrete_to_json_compatible():
    assert _concrete_to_json_compatible(1) == 1
    assert _concrete_to_json_compatible("1") == "1"
    assert _concrete_to_json_compatible(True) is True
    assert _concrete_to_json_compatible(False) is False
    assert _concrete_to_json_compatible(1.0) == 1.0
    assert _concrete_to_json_compatible(b"1") == "MQ==\n"


class Nested(pydantic.BaseModel):
    a: int
    b: str
    bs: pydantic.Base64Bytes
    list_of_bytes: list[pydantic.Base64Bytes]
    float: float


class PyModel(pydantic.BaseModel):
    a: int
    b: str
    bs: pydantic.Base64Bytes
    list_of_bytes: list[pydantic.Base64Bytes]
    float: float
    nested: Nested


def test_value_to_json_string():
    assert value_to_json_string(1) == "1"
    assert value_to_json_string("1") == '"1"'
    assert value_to_json_string(True) == "true"
    assert value_to_json_string(False) == "false"
    assert value_to_json_string(1.0) == "1.0"
    assert value_to_json_string(b"1") == '"MQ==\\n"'
    assert value_to_json_string(b"1, 2") == '"MSwgMg==\\n"'

    p_model = PyModel(
        a=1,
        b="1",
        bs=pydantic.Base64Bytes(base64.b64encode(b"1")),
        float=1.0,
        list_of_bytes=[base64.b64encode(b"1"), base64.b64encode(b"2")],
        nested=Nested(a=1, b="1", bs=base64.b64encode(b"1"), float=1.0,
                      list_of_bytes=[base64.b64encode(b"1"), base64.b64encode(b"2")])
    )

    # Validate pydantic with bytes, also containing nested model with bytes
    res = value_to_json_string(p_model)
    assert res == ('{"a":1,"b":"1","bs":"MQ==\\n","list_of_bytes":'
                   '["MQ==\\n","Mg==\\n"],"float":1.0,"nested"'
                   ':{"a":1,"b":"1","bs":"MQ==\\n","list_of_bytes":["MQ==\\n","Mg==\\n"],"float":1.0}}'
                   )
