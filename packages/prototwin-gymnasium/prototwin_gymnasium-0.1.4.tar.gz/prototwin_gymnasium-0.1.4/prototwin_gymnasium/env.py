import gymnasium
import prototwin
import asyncio
import nest_asyncio

from typing import Any

class Env(gymnasium.Env):
    def __init__(self, client: prototwin.Client) -> None:
        """
        Base Gymnasium environment for ProtoTwin Connect

        Args:
            client (prototwin.Client): The ProtoTwin Connect client.
        """
        self.client = client
        nest_asyncio.apply()
    
    def reset(self, *, seed: int|None = None, options: dict[str, Any]|None = None) -> tuple[Any, dict[str, Any]]:
        """
        Resets the environment to an initial internal state.

        Args:
            seed (int | None, optional): The random seed. Defaults to None.
            options (dict[str, Any] | None, optional): Additional information to specify how the environment is reset. Defaults to None.

        Returns:
            tuple[Any, dict[str, Any]]:  Observation of the initial state and a dictionary containing auxiliary information.
        """
        result = super().reset(seed=seed, options=options)
        asyncio.run(self.client.reset())
        return result
    
    def get(self, address: int) -> bool|int|float:
        """
        Reads the value of a signal at the specified address.

        Args:
            address (int): The signal address.

        Returns:
            bool|int|float: The signal value.
        """
        return self.client.get(address)
    
    def set(self, address: int, value: bool|int|float) -> None:
        """
        Writes a value to a signal at the specified address.  

        Args:
            address (int): The signal address.
            value (bool | int | float): The value to write.
        """
        self.client.set(address, value)
    
    def step(self) -> None:
        """
        Steps the simulation forward in time by one time-step.
        """
        asyncio.run(self.client.step())