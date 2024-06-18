from datetime import datetime

from ..models import Target, TargetStatus, TargetStatusEnum
from .emitter import EmitterArgs, EmitterProxy

class TargetArgs():
    def __init__(self, name: str, short_id: str, category: str):
        self.name = name
        self.short_id = short_id
        self.category = category

class TargetProxy():
    def __init__(self, instance, args: TargetArgs, client):
        self.instance = instance
        self.args = args
        self.client = client

    async def add_emitter(self, args: EmitterArgs):
        emitter_proxy = EmitterProxy(self, args, self.client)
        await emitter_proxy.save()
        return emitter_proxy

    # async def add_action(self, args: EmitterArgs):
    #    return

    async def save(self, status: TargetStatusEnum):
        target = Target(
          id=self.id(),
          name=self.args.name,
          category=self.args.category,
          bg_color=self.instance.args.color,
          fg_color=self.instance.args.color,
          parent_targets=[],
          sub_targets=[],
          service_id=self.instance.args.service_id,
          last_updated=datetime.now().isoformat(),
          root_level=True,
          # hash=generate_hash(),
        )

        status = TargetStatus(
            id=self.id(),
            name=self.args.name,
            target_id=self.id(),
            status=status,
            last_updated=datetime.now().isoformat(),
            instance_id=self.instance.id(),
            # hash=generate_hash()
        )

        if target.id not in self.client.targets or self.client.targets[target.id].hash != target.hash:
            await self.client.set_data(target, 'Target')

        if status.id not in self.client.target_statuses or self.client.target_statuses[status.id].hash != status.hash:
            await self.client.set_data(status, 'TargetStatus')

    def id(self) -> str:
        return f"{self.instance.args.service_id}:{self.args.short_id}"
    
    async def set_status(self, status: TargetStatusEnum):
        await self.save(status)