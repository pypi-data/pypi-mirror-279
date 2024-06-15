from clustaar.schemas.v1 import SEND_AI_TASK_ACTION
from clustaar.schemas.models import (
    FlowConnection,
    IsSetCondition,
    MessageGetter,
    StepTarget,
    ConnectionPredicate,
    AITaskEngine,
    AITaskBehavior,
    SendAITaskAction,
    IsNotSetCondition,
    StoryTarget,
)
import pytest


@pytest.fixture
def data():
    return {
        "type": "send_ai_task_action",
        "engine": {"name": "Rune", "opts": {}, "type": "ai_task_engine"},
        "behaviors": [
            {
                "name": "low",
                "connections": [
                    {
                        "type": "flow_connection",
                        "target": {"id": "a2" * 12, "type": "story", "name": "a story"},
                        "predicates": [
                            {
                                "type": "connection_predicate",
                                "condition": {"type": "is_not_set"},
                                "valueGetter": {"type": "message"},
                            }
                        ],
                    }
                ],
                "type": "ai_task_behavior",
            }
        ],
        "defaultTarget": None,
        "userAttributes": False,
    }


@pytest.fixture
def action():
    story_connection = FlowConnection(
        predicates=[
            ConnectionPredicate(condition=IsNotSetCondition(), value_getter=MessageGetter())
        ],
        target=StoryTarget(story_id="a2" * 12, name="a story"),
    )

    engine = AITaskEngine(name="Rune", opts={})
    behaviors = [AITaskBehavior(name="low", connections=[story_connection])]

    action = SendAITaskAction(engine=engine, behaviors=behaviors, user_attributes=False)

    return action


class TestLoad(object):
    def test_returns_an_action(self, data, mapper):
        result = mapper.load(data, SEND_AI_TASK_ACTION)
        assert isinstance(result, SendAITaskAction)
        assert len(result.behaviors) == 1

        assert isinstance(result.behaviors[0].connections[0], FlowConnection)

        target = result.behaviors[0].connections[0].target
        assert isinstance(target, StoryTarget)

        assert target.story_id == "a2" * 12
        predicate = result.behaviors[0].connections[0].predicates[0]
        assert isinstance(predicate, ConnectionPredicate)
        assert isinstance(predicate.condition, IsNotSetCondition)
        assert isinstance(predicate.value_getter, MessageGetter)


class TestValidate:
    def test_validation(self, data, action, mapper):
        result = mapper.validate(data, SEND_AI_TASK_ACTION)


class TestDump(object):
    def test_returns_a_dict(self, data, action, mapper):
        result = mapper.dump(action, SEND_AI_TASK_ACTION)
        assert result == data
