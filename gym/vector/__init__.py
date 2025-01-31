"""Module for vector environments."""
from __future__ import annotations

from typing import Iterable, Optional, Union

from gym.vector.async_vector_env import AsyncVectorEnv
from gym.vector.sync_vector_env import SyncVectorEnv
from gym.vector.vector_env import VectorEnv, VectorEnvWrapper

__all__ = ["AsyncVectorEnv", "SyncVectorEnv", "VectorEnv", "VectorEnvWrapper", "make"]


def make(
    id: str,
    num_envs: int = 1,
    asynchronous: bool = True,
    wrappers: Optional[Union[callable, list[callable]]] = None,
    **kwargs,
) -> VectorEnv:
    """Create a vectorized environment from multiple copies of an environment, from its id.

    Example::

        >>> import gym
        >>> env = gym.vector.make('CartPole-v1', num_envs=3)
        >>> env.reset()
        array([[-0.04456399,  0.04653909,  0.01326909, -0.02099827],
               [ 0.03073904,  0.00145001, -0.03088818, -0.03131252],
               [ 0.03468829,  0.01500225,  0.01230312,  0.01825218]],
              dtype=float32)

    Args:
        id: The environment ID. This must be a valid ID from the registry.
        num_envs: Number of copies of the environment.
        asynchronous: If `True`, wraps the environments in an :class:`AsyncVectorEnv` (which uses `multiprocessing`_ to run the environments in parallel). If ``False``, wraps the environments in a :class:`SyncVectorEnv`.
        wrappers: If not ``None``, then apply the wrappers to each internal environment during creation.
        **kwargs: Keywords arguments applied during gym.make

    Returns:
        The vectorized environment.
    """
    from gym.envs import make as make_

    def _make_env():
        env = make_(id, **kwargs)
        if wrappers is not None:
            if callable(wrappers):
                env = wrappers(env)
            elif isinstance(wrappers, Iterable) and all(
                [callable(w) for w in wrappers]
            ):
                for wrapper in wrappers:
                    env = wrapper(env)
            else:
                raise NotImplementedError
        return env

    env_fns = [_make_env for _ in range(num_envs)]
    return AsyncVectorEnv(env_fns) if asynchronous else SyncVectorEnv(env_fns)
