from .target import TargetProxy, TargetArgs
from ..models import TargetStatusEnum, Instance, InstanceStatusEnum, Machine

class InstanceArgs():
    def __init__(self, name: str, code: str, service_id: str, cluster_id: str, 
                 color: str, machine_id: str, message: str):
        self.name = name
        self.code = code
        self.service_id = service_id
        self.cluster_id = cluster_id
        self.machine_id = machine_id
        self.color = color
        self.message = message


        self.target_proxies = {}

class InstanceProxy():
    def __init__(self, args: InstanceArgs, client):
        self.args = args
        self.client = client
  
    def add_target(self, args: TargetArgs):
        target = TargetProxy(self, args, self.client)
        target.save(TargetStatusEnum.Online)
        self.target_proxies[target.id()] = target
        return target

    def save(self, status: InstanceStatusEnum):
        instance = Instance(
            id=self.id(),
            name=self.args.name,
            service_id=self.args.service_id,
            service_type_code=self.args.code,
            client_id=self.client.client_id, # get client id at all costs
            cluster_id=self.args.cluster_id,
            machine_id=self.args.machine_id,
            color=self.args.color,
            # hash=generate_hash()

            message=self.args.message,
            status=status,
        )

        machine = Machine(
            name=self.args.machine_id,
        )

        self.client.set_data(instance, 'Instance')
        self.client.set_data(machine, 'Machine')

      
    def set_status(self, status: InstanceStatusEnum):
        self.save(status)

    def id(self) -> str:
        return f"{self.args.service_id}:{self.args.machine_id}"