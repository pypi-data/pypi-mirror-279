import asyncio
import json
import websockets
from typing import Any, Callable, Dict
from myko import MEvent, MEventType, MCommand, WSMEvent, WSMCommand

from .models import Target, Action, Emitter, Pulse, Instance, Machine, Alert, InstanceStatusEnum, TargetStatus, TargetStatusEnum, AlertEntityType, AlertLevel
from .utils import generate_hash, get_current_timestamp, make_instance_id

from .proxies.instance import InstanceProxy, InstanceArgs

class RshipExecClient:
    def __init__(self, rship_host: str, rship_port: int):
        self.rship_host = rship_host
        self.rship_port = rship_port
        self.is_connected = False
        self.client_id = None
        self.websocket = None
        self.targets: Dict[str, Target] = {}
        self.target_statuses: Dict[str, TargetStatus] = {}
        self.actions: Dict[str, Action] = {}
        self.emitters: Dict[str, Emitter] = {}
        self.instances: Dict[str, Instance] = {}
        self.machines: Dict[str, Machine] = {}
        self.alerts: Dict[str, Alert] = {}
        self.handlers: Dict[str, Callable[[Action, Any], None]] = {}

    ##############################
    # Websockets
    ##############################

    async def connect(self):
        uri = f"ws://{self.rship_host}:{self.rship_port}/myko"
        print(f"Attempting to connect to {uri}")
        try:
            self.websocket = await websockets.connect(uri)
            print("Connected to Rship server successfully.")
            self.is_connected = True
        except Exception as e:
            print(f"Failed to connect: {e}")

    async def disconnect(self):
        if self.websocket:
            await self.websocket.close()
            self.websocket = None
            print("Disconnected from Rship server")
            self.is_connected = False

    async def send_event(self, event: MEvent):
        try: 
            await self.websocket.send(json.dumps(WSMEvent(event).__dict__))
        except TypeError:
            print("Failed to send event: TypeError")

    async def send_command(self, command: MCommand):
        try:
            await self.websocket.send(json.dumps(WSMCommand(command).__dict__))
        except ConnectionError:
            print("Failed to send command: ConnectionError")

    async def receive_messages(self):
        while self.websocket:
            try:
                message = await self.websocket.recv()
                await self.handle_message(message)
            except websockets.ConnectionClosed:
                await self.disconnect()

    async def handle_message(self, message: str):
        data = json.loads(message)
        if data["event"] == "ws:m:command":
            command_data = data["data"]
            command_id = command_data["commandId"]
            if command_id == "client:setId":
                self.client_id = command_data["command"]["clientId"]
                print(f"Received client ID: {self.client_id}")
            elif command_id == "target:action:exec":
                action_id = command_data["command"]["action"]["id"]
                if action_id in self.actions:
                    action = self.actions[action_id]
                    handler = self.handlers.get(action_id)
                    if handler:
                        handler(action, command_data["command"]["data"])

    ##############################
    # Models
    ##############################

    async def set_data(self, item: Any, item_type: str):
        event = MEvent(item=item, item_type=item_type, change_type=MEventType.SET,
                       created_at=get_current_timestamp(), tx=generate_hash())
        await self.send_event(event)


    async def delete_data(self, item: Any):
        event = MEvent(item=item, item_type=type(item).__name__, change_type=MEventType.DEL,
                       created_at=get_current_timestamp(), tx=generate_hash())
        await self.send_event(event)


    async def add_instance(self, args: InstanceArgs):
        instance_proxy = InstanceProxy(args=args, 
                                       client=self)
        await instance_proxy.save(InstanceStatusEnum.Available)
        return instance_proxy


    async def pulse_emitter(self, service_short_id: str, target_short_id: str, emitter_short_id: str, data: Any):
        full_emitter_id = f"{service_short_id}:{target_short_id}:{emitter_short_id}"
        pulse = Pulse(name="", emitter_id=full_emitter_id, data=data)
        await self.set_data(pulse, 'Pulse')
