from __future__ import annotations

import numpy as np
from dqrobotics import DQ, robots

from . import dqutil
from .pandamg import PandaScrewMotionGenerator


def simulate_joint_waypoints(
    mg: PandaScrewMotionGenerator,
    q_init: np.ndarray,
    ee_goal_pose: DQ,
    eps: float = 0.005,
    dt: float = 0.001,
    max_steps: int = 1000,
) -> tuple[list[np.ndarray], bool]:
    r"""Simulate screwmpc controller given initial condition and a goal pose.

    :param mg: Motion generator.
    :type mg: PandaScrewMotionGenerator
    :param q_init: Initial joint configuration :math:`\boldsymbol{q}_0`.
    :type q_init: np.ndarray
    :param ee_goal_pose: End-effector goal pose.
    :type ee_goal_pose: DQ
    :param eps: Error threshold :math:`\epsilon`, defaults to 0.005.
    :type eps: float, optional
    :param dt: Integration stepsize :math:`\delta t`, defaults to 0.001 [s].
    :type dt: float, optional
    :param max_steps: Maximum number of simulation steps, defaults to 1000.
    :type max_steps: int, optional
    :return: The integrated joint configurations, the state of the simulation.
    :rtype: tuple[list[np.ndarray], bool]
    """
    error: float = float("inf")
    q_robot: np.ndarray = q_init.copy()
    joint_angles: list[np.ndarray] = [q_init]
    step: int = 0
    done: bool = False
    kin = robots.FrankaEmikaPandaRobot.kinematics()
    while not done:
        dq = mg.step(q_robot, ee_goal_pose)
        q_robot += dq * dt
        joint_angles.append(q_robot.copy())
        error = np.linalg.norm(
            dqutil.dq_pose_error(kin.fkm(q_robot), ee_goal_pose).vec8()
        )
        done = error < eps or step >= max_steps
        step += 1

    return joint_angles, error < eps
