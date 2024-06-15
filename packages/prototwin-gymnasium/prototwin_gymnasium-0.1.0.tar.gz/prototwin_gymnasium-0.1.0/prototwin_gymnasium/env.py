import gymnasium
import prototwin
import asyncio

from typing import Any

class Env(gymnasium.Env):
    def __init__(self, client: prototwin.Client) -> None:
        self.client = client
    
    def reset(self, *, seed: int|None = None, options: dict[str, Any]|None = None) -> tuple[Any, dict[str, Any]]:
        result = super().reset(seed=seed, options=options)
        asyncio.run(self.client.reset())
        return result
    
    def get(self, address: int) -> bool|int|float:
        return self.client.get(address)
    
    def set(self, address: int, value: bool|int|float) -> None:
        self.client.set(address, value)
    
    def step(self) -> None:
        asyncio.run(self.client.step())