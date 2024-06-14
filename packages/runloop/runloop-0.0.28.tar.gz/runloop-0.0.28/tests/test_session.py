from typing import TypeVar

from pydantic import BaseModel

from runloop import Session

# TODO: Make "TestSession" first class

T = TypeVar("T")


class TestSession(Session[T]):
    def __init__(self, id: str, kv: T):
        super().__init__(id, kv)

    def commit_session(self) -> None:
        pass


def test_runloop_return_type_simple():
    class Thread(BaseModel):
        name: str
        message_count: int

    session = TestSession(id="whatisthis", kv=Thread(name="test", message_count=234))
    assert session.kv.name == "test"
    assert session.kv.message_count == 234


def test_runloop_return_type_dict():
    session = TestSession(id="thisId", kv={"name": "test", "message_count": 234})
    assert session.kv["name"] == "test"
    assert session.kv["message_count"] == 234
