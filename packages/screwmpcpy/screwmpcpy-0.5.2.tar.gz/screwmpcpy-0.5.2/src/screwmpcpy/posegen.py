"""Pose generator module"""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

import numpy as np
from spatialmath import SE3, UnitQuaternion

from .screwmpc import BOUND


class PoseGenerator(ABC):
    """Generate random pose for robotic endeffector"""

    @abstractmethod
    def generate(self, *args: Any, **kwargs: Any) -> tuple[np.ndarray, UnitQuaternion]:
        pass

    def __call__(self, *args: Any, **kwds: Any) -> tuple[np.ndarray, UnitQuaternion]:
        return self.generate(*args, **kwds)


class UniformPoseGenerator(PoseGenerator):
    """Uniform pose sampling

    :param translation_bound: 3d translation bounds (forming a cuboid).
    :type translation_bound: BOUND
    :param angle_bound: 3d euler angles for EE orientation.
    :type angle_bound: BOUND
    """

    def __init__(self, translation_bound: BOUND, angle_bound: BOUND) -> None:
        super().__init__()
        self._lower_t = translation_bound.lower
        self._upper_t = translation_bound.upper
        self._lower_euler = angle_bound.lower
        self._upper_euler = angle_bound.upper
        self._rng: np.random.Generator = np.random.default_rng()

    def generate(self, *args: Any, **kwds: Any) -> tuple[np.ndarray, UnitQuaternion]:  # noqa: ARG002
        """Generate a random EE pose.

        :return: Pose (translation, orientation)
        :rtype: tuple[np.ndarray, UnitQuaternion]
        """

        trans = np.array(
            [self._rng.uniform(self._lower_t[i], self._upper_t[i]) for i in range(3)]
        )
        euler = np.array(
            [
                self._rng.uniform(self._lower_euler[i], self._upper_euler[i])
                for i in range(3)
            ]
        )
        orientation = UnitQuaternion(*SE3.RPY(*euler).angvec())
        return trans, orientation
