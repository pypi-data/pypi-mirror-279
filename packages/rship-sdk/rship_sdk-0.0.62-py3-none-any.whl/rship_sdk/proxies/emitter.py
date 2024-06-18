from ..models import Emitter

class EmitterArgs():
  def __init__(self, name: str, short_id: str, schema: any):
    self.name = name
    self.short_id = short_id
    self.schema = schema

class EmitterProxy():
  def __init__(self, target_proxy, args: EmitterArgs, client):
    self.target = target_proxy
    self.args = args
    self.client = client

  async def save(self):
    emitter = Emitter(
      id=self.id(),
      name=self.args.name,
      schema=self.args.schema,
      target_id=self.target.id(),
      service_id=self.target.instance.args.service_id,
    )
    if emitter.id not in self.client.emitters or self.client.emitters[emitter.id].hash != emitter.hash:
      await self.client.set_data(emitter, 'Emitter')

  def id(self) -> str:
    return f"{self.target.instance.args.service_id}:{self.target.args.short_id}:{self.args.short_id}"
  
  async def pulse(self, data: any):
    await self.client.pulse_emitter(
      self.target.instance.args.service_id, 
      self.target.args.short_id,
      self.args.short_id,
      data,
    )