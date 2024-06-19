"""Test integrated joint angles for screw based motion generators."""
from __future__ import annotations

import dqrobotics
import numpy as np
import spatialmath
from dqrobotics.robots import FrankaEmikaPandaRobot

from screwmpcpy import dqutil
from screwmpcpy.dqutil import dq_pose_error
from screwmpcpy.pandamg import (
    PandaScrewMotionGenerator,
)
from screwmpcpy.screwintegrator import simulate_joint_waypoints
from screwmpcpy.screwmpc import BOUND

franka_kin = FrankaEmikaPandaRobot.kinematics()


def displacement(
    pose: dqrobotics.DQ, linear: np.ndarray, angular: spatialmath.SE3
) -> dqrobotics.DQ:
    x, q = dqutil.dq_to_pose(pose)
    dq = spatialmath.UnitDualQuaternion(
        spatialmath.SE3(*x) * spatialmath.SE3(*linear) * q.SE3() * angular
    )
    return dqrobotics.DQ(dq.vec)


def assert_case(
    q_initial: np.ndarray,
    goal: dqrobotics.DQ,
    waypoints: list[np.ndarray],
    ok: bool,
    max_steps: int,
    eps: float,
) -> None:
    assert ok
    assert len(waypoints) > 0
    assert len(waypoints) <= max_steps
    np.testing.assert_array_equal(q_initial, waypoints[0])
    _goal = franka_kin.fkm(waypoints[-1])
    error = dq_pose_error(_goal, goal)
    assert np.linalg.norm(error.vec8()) < eps


Np = 50  # prediction horizon, can be tuned;
Nc = 10  # control horizon, can be tuned
R = 10e-3  # weight matirix
Q = 10e9  # weight matrix

ub_jerk = np.array([8500.0, 8500.0, 8500.0, 4500.0, 4500.0, 4500.0])
lb_jerk = -ub_jerk.copy()

ub_acc = np.array([17.0, 17.0, 17.0, 9.0, 9.0, 9.0])
lb_acc = -ub_acc.copy()

ub_v = np.array([2.5, 2.5, 2.5, 3.0, 3.0, 3.0])
lb_v = -ub_v.copy()

jerk_bound = BOUND(lb_jerk, ub_jerk)
acc_bound = BOUND(lb_acc, ub_acc)
vel_bound = BOUND(lb_v, ub_v)

mg = PandaScrewMotionGenerator(
    Np, Nc, Q, R, vel_bound, acc_bound, jerk_bound, sclerp=0.5
)

dt = 1e-3
max_steps = 10000
eps = 5e-3

# use the robot ready position
q_initial = np.array([0, -0.78539816, 0, -2.35619449, 0, 1.57079633, 0.78539816])


def test_simulate_joint_waypoints_linear() -> None:
    # goal is slight displacement from ready position
    # move by 0.05m along x
    goal = displacement(franka_kin.fkm(q_initial), [0.05, 0, 0], spatialmath.SE3())
    waypoints, ok = simulate_joint_waypoints(
        mg, q_initial, goal, eps=eps, dt=dt, max_steps=max_steps
    )
    assert_case(q_initial, goal, waypoints, ok, max_steps, eps)


def test_simulate_joint_waypoints_angular() -> None:
    # goal is slight displacement from ready position
    # tilt by -2 degree around x
    goal = displacement(
        franka_kin.fkm(q_initial), [0, 0, 0], spatialmath.SE3.Rx(-2, "deg")
    )
    waypoints, ok = simulate_joint_waypoints(
        mg, q_initial, goal, eps=eps, dt=dt, max_steps=max_steps
    )
    assert_case(q_initial, goal, waypoints, ok, max_steps, eps)


def test_simulate_joint_waypoints() -> None:
    # goal is slight displacement from ready position
    # move by 0.05m along x
    # tilt by -2 degree around x
    goal = displacement(
        franka_kin.fkm(q_initial), [0.05, 0, 0], spatialmath.SE3.Rx(-2, "deg")
    )
    waypoints, ok = simulate_joint_waypoints(
        mg, q_initial, goal, eps=eps, dt=dt, max_steps=max_steps
    )
    assert_case(q_initial, goal, waypoints, ok, max_steps, eps)
