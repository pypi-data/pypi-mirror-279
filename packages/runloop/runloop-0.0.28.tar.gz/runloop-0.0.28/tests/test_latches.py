
from pydantic import BaseModel


def test_runloop_latches_added_to_manifest():
    from runloop import latch, runloop_manifest

    @latch
    class MyExampleLatchType(BaseModel):
        human_name: str
        human_id: int

    latches = [x for x in runloop_manifest.external_latch_types if x.name == "MyExampleLatchType"]
    assert len(runloop_manifest.external_latch_types) == 1
    my_latch = latches[0]
    assert len(my_latch.type.model.children) == 2
    assert [child.name for child in my_latch.type.model.children] == ["human_name", "human_id"]
