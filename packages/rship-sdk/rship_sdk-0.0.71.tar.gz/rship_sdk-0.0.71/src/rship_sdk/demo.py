from .client import RshipExecClient
from .proxies.instance import InstanceProxy, InstanceArgs
from .proxies.target import TargetProxy, TargetArgs
from .proxies.emitter import EmitterProxy, EmitterArgs

def main():
    client = RshipExecClient("10.147.20.13", 5155)
    client.connect()
    
    instance =  client.add_instance(
        InstanceArgs(
            name="Demo",
            code="python-demo",
            service_id="python-demo",
            cluster_id=None,
            machine_id="demo-machine",
            color="#FFFF00",
            message=None
        )
    )

    print("Instance created")

    target = instance.add_target(
        TargetArgs(
            name="Whisper Live",
            short_id="whisper_live",
            category="ASR",
        )
    )

    print("Target created")

    emitter = target.add_emitter(
        EmitterArgs(
            name="Transcription",
            short_id="transcription",
            schema={
                "type": "object",
                "properties": {
                    "message": {
                        "type": "string"
                    }
                }
            },
        )
    )

    print("Rship setup completed")

if __name__ == "__main__":
    main()