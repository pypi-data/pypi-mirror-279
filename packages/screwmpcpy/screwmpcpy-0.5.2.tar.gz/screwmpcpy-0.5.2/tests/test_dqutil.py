""" Test Dual UnitQuaternion related utility functions. """
from __future__ import annotations

import numpy as np
from dqrobotics import DQ, vec8
from spatialmath import UnitQuaternion

from screwmpcpy.dqutil import (
    dq_angle_norm,
    dq_exp,
    dq_log,
    dq_pose_error,
    dq_pow,
    dq_sclerp,
    dq_to_pose,
    generate_intermediate_waypoints,
    interpolate_waypoints,
    pose_to_dq,
)


def test_pow() -> None:
    """Test pow for unit dual quaternions, which represent a screw motion."""

    pose = np.zeros((8,))
    pose[0] = 1.0
    pose[5:] = np.array([0.0, 0.0, -1.0])
    pose = DQ(pose)

    new_pose = dq_pow(pose, 0.5)
    np.testing.assert_array_equal(new_pose.D().vec3(), np.array([0.0, 0.0, -0.5]))


def test_exp_log() -> None:
    """Test exp and log unit dual quaternions."""
    pose = (
        np.array([0, 0, -1]),
        UnitQuaternion(-np.pi / 4, np.array([0, 1, 0])),
    )
    pose = pose_to_dq(pose)
    assert dq_exp(dq_log(pose)) == pose


def test_dq_angle_norm() -> None:
    """Test angle normalization of DQ stuff"""

    test_dq = DQ(np.zeros((8,)))
    assert test_dq == dq_angle_norm(test_dq)


def test_dq_sclerp() -> None:
    """Test scLERP for unit dual quaternions"""

    initial_pose = (
        np.array([0, 1, 0]),
        UnitQuaternion(np.pi, np.array([1, 0, 0])),
    )
    goal_pose = (
        np.array([0, 0, -1]),
        UnitQuaternion(-np.pi / 4, np.array([0, 1, 0])),
    )
    initial_pose, goal_pose = pose_to_dq(initial_pose), pose_to_dq(goal_pose)
    inter_pose = dq_sclerp(initial_pose, goal_pose, 0)
    assert inter_pose == initial_pose
    inter_pose = dq_sclerp(initial_pose, goal_pose, 1)
    assert inter_pose == goal_pose


def test_generate_waypoints() -> None:
    """Test the generated waypoints."""

    initial_pose = (
        np.array([0, 1, 0]),
        UnitQuaternion(np.pi, np.array([1, 0, 0])),
    )
    goal_pose = (
        np.array([0, 0, -1]),
        UnitQuaternion(-np.pi / 4, np.array([0, 1, 0])),
    )
    initial_pose, goal_pose = pose_to_dq(initial_pose), pose_to_dq(goal_pose)
    waypoints = generate_intermediate_waypoints(initial_pose, goal_pose, 10)

    assert len(waypoints) == 10

    steps = np.linspace(0, 1, len(waypoints))

    for step, waypoint in zip(steps, waypoints):
        inter_pose = dq_sclerp(initial_pose, goal_pose, step)
        assert inter_pose == waypoint


def test_dq_to_pose() -> None:
    """Test retrieved poses"""

    pose = (np.array([0, 1, 0]), UnitQuaternion(np.pi, np.array([1, 0, 0])))
    _pose = dq_to_pose(pose_to_dq(pose))
    np.testing.assert_array_almost_equal(pose[1].vec, _pose[1], decimal=12)
    np.testing.assert_array_almost_equal(pose[0], _pose[0], decimal=12)


def test_dq_pose_error() -> None:
    """Test retrieved pose error"""
    pose = (np.array([0, 1, 0]), UnitQuaternion(np.pi, np.array([1, 0, 0])))
    pose = pose_to_dq(pose)
    error = np.linalg.norm(dq_pose_error(pose, pose).vec8())
    assert error < 1e-15


def test_waypoints() -> None:
    """Test the generated intermediate way points."""

    initial_pose = (
        np.array([0, 1, 0]),
        UnitQuaternion(np.pi / 2, np.array([1, 0, 0])),
    )
    goal_pose = (
        np.array([0, 0, -1]),
        UnitQuaternion(-np.pi / 4, np.array([0, 1, 0])),
    )
    waypoints = interpolate_waypoints([initial_pose, goal_pose], 8)
    assert len(waypoints) == 10

    np.testing.assert_array_almost_equal(initial_pose[0], waypoints[0][0], decimal=12)
    np.testing.assert_array_almost_equal(
        initial_pose[1].vec, waypoints[0][1].vec, decimal=12
    )
    np.testing.assert_array_almost_equal(goal_pose[0], waypoints[-1][0], decimal=12)
    np.testing.assert_array_almost_equal(
        goal_pose[1].vec, waypoints[-1][1].vec, decimal=12
    )

    error = np.linalg.norm(
        vec8(dq_pose_error(pose_to_dq(initial_pose), pose_to_dq(goal_pose)))
    )
    expected_len = int((8 + 2) * np.clip(error, 0, 1))
    waypoints = interpolate_waypoints([initial_pose, goal_pose], 8, adaptive=True)
    assert len(waypoints) == expected_len
