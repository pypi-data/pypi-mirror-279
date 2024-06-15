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

class InstanceProxy():
    def __init__(self, args: InstanceArgs, client):
        self.args = args
        self.client = client
  
    async def add_target(self, args: TargetArgs):
        target = TargetProxy(self, args, self.client)
        await target.save(TargetStatusEnum.Online)
        return target

    async def save(self, status: InstanceStatusEnum):
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
            name='dummy',
            # hash=generate_hash()
        )
        if instance.id not in self.client.instances or self.client.instances[instance.id].hash != instance.hash:
            await self.client.set_data(instance, 'Instance')

        if machine.id not in self.client.machines or self.client.machines[machine.id].hash != machine.hash:
            await self.client.set_data(machine, 'Machine')
      
    async def set_status(self, status: InstanceStatusEnum):
        await self.save(status)

    def id(self) -> str:
        return f"{self.args.service_id}:{self.args.machine_id}"