from __future__ import annotations

import logging
from typing import Any

import numpy as np
import panda_py
import roboticstoolbox as rtb
import swift
from panda_py.motion import JointTrajectory
from spatialmath import SE3, UnitQuaternion

from screwmpcpy.dqutil import interpolate_waypoints
from screwmpcpy.posegen import PoseGenerator, UniformPoseGenerator
from screwmpcpy.screwmpc import BOUND

# Flange to EE transform taken form
# https://github.com/JeanElsner/screwmpc-experiments/blob/main/src/screwmpc_experiments/experiments/screwmpc.py
T_F_EE: SE3 = SE3(0, 0, 0.1034) * SE3.Rz(-45, unit="deg")


def generate_random_poses(
    generator: PoseGenerator,
    n_poses: int,
    q_init: np.ndarray,
    *genargs: Any,
    **genkwds: Any,
) -> list[tuple[np.ndarray, UnitQuaternion]]:
    """Generate random pose, adapted from
    https://github.com/JeanElsner/screwmpc-experiments/blob/main/src/screwmpc_experiments/experiments/screwmpc.py

    :param generator: Pose generator
    :type generator: PoseGenerator
    :param n_poses: Number of poses to generate.
    :type n_poses: int
    :param q_init: Initial robot configuration in joint angle representation.
    :type q_init: np.ndarray
    :return: Random generated poses.
    :rtype: list[tuple[np.ndarray, UnitQuaternion]]
    """
    poses: list[tuple[np.ndarray, UnitQuaternion]] = []
    _q_init = q_init.copy()

    while len(poses) < n_poses:
        pose = generator(*genargs, **genkwds)
        se3 = SE3(pose[0]) * UnitQuaternion(pose[1]).SE3() * T_F_EE
        q_ik = panda_py.ik(se3, _q_init)

        if not np.any(np.isnan(q_ik)):
            poses.append(pose)
            _q_init = q_ik

    return poses


def ik_feasible_path(
    q_init: np.ndarray,
    poses: list[tuple[np.ndarray, UnitQuaternion]],
) -> tuple[np.ndarray, np.ndarray]:
    """Check the path with ik solver

    :param q_init: Initial joint configuration.
    :type q_init: np.ndarray
    :param poses: List of poses.
    :type poses: list[tuple[np.ndarray, UnitQuaternion]]
    :return: Valid joint configurations and valid indices of original poses.
    :rtype: tuple[np.ndarray, np.ndarray]
    """
    joint_config: list[np.ndarray] = []
    indices: list[int] = []
    _q_init = q_init.copy()

    for i, pose in enumerate(poses):
        se3 = SE3(pose[0]) * pose[1].SE3() * T_F_EE
        q_ik = panda_py.ik(se3, _q_init)

        # pose feasible
        if not np.any(np.isnan(q_ik)):
            _q_init = q_ik
            joint_config.append(_q_init)
            indices.append(i)

    return joint_config, np.array(indices)


def main() -> None:
    logging.basicConfig(level=logging.INFO)
    n_waypoints: int = 8
    n_poses: int = 5

    # initial joint angles taken from
    # https://github.com/JeanElsner/dm_robotics_panda/blob/main/src/dm_robotics/panda/parameters.py
    q_init: np.ndarray = np.array([0, -0.785, 0, -2.356, 0, 1.571, 0.785])

    dp = [0.1, 0.3, 0.3]
    dr = [45, 45, 45]

    min_pos_bound = np.array([0.307 - dp[0], 0 - dp[1], 0.487 + 0.1034 - dp[2]])
    max_pos_bound = np.array([0.307 + dp[0], 0 + dp[1], 0.487 + 0.1034 + dp[2]])
    min_euler_bound = np.array([np.pi - dr[0], 0 - dr[1], 0.25 * np.pi - dr[2]])
    max_euler_bound = np.array([np.pi + dr[0], 0 + dr[1], 0.25 * np.pi + dr[2]])

    euler_bound = BOUND(min_euler_bound, max_euler_bound)
    trans_bound = BOUND(min_pos_bound, max_pos_bound)

    generator = UniformPoseGenerator(trans_bound, euler_bound)
    poses = generate_random_poses(generator, n_poses, q_init.copy())
    msg = f"Generated: {len(poses)} poses."
    logging.info(msg)
    new_poses = interpolate_waypoints(poses, n_waypoints, adaptive=True)

    msg = f"Number of poses after interpolation: {len(new_poses)}"
    logging.info(msg)
    joint_configs, _ = ik_feasible_path(q_init.copy(), new_poses)
    msg = f"Initial motion plan feasible: {len(joint_configs) == len(new_poses)}"
    logging.info(msg)

    msg = f"Number of poses after pruning: {len(joint_configs)}"
    logging.info(msg)

    panda = rtb.models.Panda()
    panda.q = q_init

    dt = 0.05
    joint_traj = JointTrajectory(joint_configs)
    exec_time = joint_traj.get_duration()

    env = swift.Swift()
    env.launch(realtime=True)
    env.add(panda)
    t = 0.0

    while t < exec_time:
        # panda.q = joint_traj.get_joint_positions(t, panda.q)
        panda.qd = joint_traj.get_joint_velocities(t, panda.q)
        panda.qdd = joint_traj.get_joint_accelerations(t, panda.q)
        env.step(dt)
        t += dt


if __name__ == "__main__":
    main()
