import asyncio
import json
import websocket
from typing import Any, Callable, Dict
from myko import MEvent, MEventType, MCommand, WSMEvent, WSMCommand

from .models import Target, Action, Emitter, Pulse, Instance, Machine, Alert, InstanceStatusEnum, TargetStatus, TargetStatusEnum, AlertEntityType, AlertLevel
from .utils import generate_hash, get_current_timestamp, make_instance_id

from .proxies.instance import InstanceProxy, InstanceArgs

from threading import Thread

class RshipExecClient:
    def __init__(self, rship_host: str, rship_port: int, on_exec_connected: Callable = None):
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

        self.instance_proxies: Dict[str, InstanceProxy] = {}
        self.on_exec_connected = on_exec_connected

    ##############################
    # Websockets
    ##############################

    def on_open(self, ws):
        print("Connected to Rship server successfully.")
        self.is_connected = True

    def on_message(self, ws, message):
        print(f"Received message: {message}")
        self.handle_message(message)

    def on_close(self, ws, status):
        print("Connection to Rship server closed.")
        self.is_connected = False

    def connect(self):
        uri = f"ws://{self.rship_host}:{self.rship_port}/myko"
        print(f"Attempting to connect to {uri}")
        try:
            self.websocket = websocket.WebSocketApp(
                url=uri, 
                on_message=lambda ws, message: self.on_message(ws, message), 
                on_open=lambda ws: self.on_open(ws),
                on_close=lambda ws, close_status_code: self.on_close(ws, close_status_code),
                on_error=lambda ws, error: print(f"Error: {error}")
            )

            self.ws_thread = Thread(target=self.websocket.run_forever)
            self.ws_thread.setDaemon(True)
            self.ws_thread.start()

        except Exception as e:
            print(f"Failed to connect: {e}")

    def disconnect(self):
        if self.websocket:
            self.websocket.close()
            self.websocket = None
            self.ws_thread = None
            print("Disconnected from Rship server")
            self.is_connected = False

    def send_event(self, event: MEvent):
        try: 
            self.websocket.send(json.dumps(WSMEvent(event).__dict__))
        except TypeError:
            print("Failed to send event: TypeError")

    def send_command(self, command: MCommand):
        try:
            self.websocket.send(json.dumps(WSMCommand(command).__dict__))
        except ConnectionError:
            print("Failed to send command: ConnectionError")

    def handle_message(self, message: str):
        data = json.loads(message)
        if data["event"] == "ws:m:command":
            command_data = data["data"]
            command_id = command_data["commandId"]
            if command_id == "client:setId":
                self.client_id = command_data["command"]["clientId"]
                print(f"Received client ID: {self.client_id}")
                if self.on_exec_connected:
                    self.on_exec_connected()
                for instance_proxy in self.instance_proxies.values():
                    instance_proxy.save(InstanceStatusEnum.Available)
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

    def set_data(self, item: Any, item_type: str):
        event = MEvent(item=item, item_type=item_type, change_type=MEventType.SET,
                       created_at=get_current_timestamp(), tx=generate_hash())
        self.send_event(event)


    def delete_data(self, item: Any):
        event = MEvent(item=item, item_type=type(item).__name__, change_type=MEventType.DEL,
                       created_at=get_current_timestamp(), tx=generate_hash())
        self.send_event(event)


    def add_instance(self, args: InstanceArgs):

        instance_proxy = InstanceProxy(args=args, 
                                       client=self)

        instance_proxy.save(InstanceStatusEnum.Available)
        self.instance_proxies[instance_proxy.id()] = instance_proxy   
        return instance_proxy


    def pulse_emitter(self, service_short_id: str, target_short_id: str, emitter_short_id: str, data: Any):
        full_emitter_id = f"{service_short_id}:{target_short_id}:{emitter_short_id}"
        pulse = Pulse(name="", emitter_id=full_emitter_id, data=data)
        self.set_data(pulse, 'Pulse')



client = RshipExecClient(rship_host="10.147.20.13", rship_port=5155)