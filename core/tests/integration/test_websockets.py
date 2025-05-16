import pytest
from channels.testing import WebsocketCommunicator
from taskmanager.asgi import application

@pytest.mark.asyncio
async def test_task_websocket():
    communicator = WebsocketCommunicator(application, "/ws/tasks/1/")
    connected, _ = await communicator.connect()
    assert connected

    await communicator.send_json_to({"event": "test", "data": "hello"})
    response = await communicator.receive_json_from()
    assert response["event"] == "test"
    assert response["data"] == "hello"

    await communicator.disconnect()
