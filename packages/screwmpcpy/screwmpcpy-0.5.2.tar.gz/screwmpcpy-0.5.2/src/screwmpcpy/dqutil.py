"""Utility functions for basic (unit) dual quaternion usage."""
from __future__ import annotations

import numpy as np
from dqrobotics import DQ, rotation, translation, vec3, vec4, vec6, vec8
from spatialmath import (
    DualQuaternion,
    Quaternion,
    UnitQuaternion,
)


def delta_dq(start: DQ, goal: DQ) -> DQ:
    r"""Calculate the "shortest" dual quaternion transformation between two unit dual quaternions.

    :param start: Start pose encoded as unit dual quaternion.
    :type start: DQ
    :param goal: Goal pose encoded as unit dual quaternion.
    :type goal: DQ
    :return: :math:`\boldsymbol{h}^{-1}_{start} \cdot \boldsymbol{h}_{goal}`
    :rtype: DQ
    """
    delta_dq = start.inv() * goal
    if np.dot(vec4(start), vec4(goal)) < 0:
        primal = -UnitQuaternion(vec4(delta_dq))
        translation = Quaternion.Pure(vec3(delta_dq.translation()))
        dual = 0.5 * translation * primal
        delta_dq = DQ(np.concatenate([primal.vec, dual.vec]))
    return delta_dq


def dq_angle_norm(dq_in: DQ) -> DQ:
    r"""Force the DQ to have smallest possible angle as screw axis.
       Screw angle is forced between :math:`\left[-\pi, +\pi\right]`

    :param dq_in: Input dual quaternion
    :type dq_in: DQ
    :return: Minimum screw angle DQ.
    :rtype: DQ
    """
    theta_half = np.arccos(np.clip(dq_in.q[0], -1, 1))
    u_vec = vec3(dq_in.P())
    out = np.zeros((8,))

    if not np.isclose(theta_half, 0.0):
        denom = np.sin(theta_half)
        theta_eps_half = -(dq_in.q[4] / denom)
        s = u_vec / denom
        s_eps = (vec3(dq_in.D()) - theta_eps_half * np.cos(theta_half) * s) / denom

        # force smallest possible angle
        angle = 2.0 * theta_half
        angle = (angle + np.pi) % (2 * np.pi) - np.pi
        new_theta_half = 0.5 * angle
        out[0] = np.cos(new_theta_half)
        out[1:4] = np.sin(new_theta_half) * s
        out[4] = -theta_eps_half * np.sin(new_theta_half)
        out[5:] = (
            np.sin(new_theta_half) * s_eps + theta_eps_half * np.cos(new_theta_half) * s
        )
    else:
        out = vec8(dq_in)
    return DQ(out)


def dq_to_pose(unit_dq: DQ) -> tuple[np.ndarray, UnitQuaternion]:
    """Generate a classic pose from a unit dual quaternion.

    :param unit_dq: pose represented as dual quaternion.
    :type unit_dq: DQ
    :return: translation (3d vector), orientation (quaternion)
    :rtype: tuple[np.ndarray, np.ndarray]
    """
    _translation = vec3(translation(unit_dq))
    _orientation = UnitQuaternion(vec4(rotation(unit_dq)))
    return _translation, _orientation


def pose_to_dq(pose: tuple[np.ndarray, UnitQuaternion]) -> DQ:
    """Generate classic pose from unit dual quaternion.

    :param pose: Pose consisting of translation and a quaternion.
    :type pose: tuple[np.ndarray, Quaternion]
    :return: pose represented as unit dual quaternion.
    :rtype: DQ
    """
    primal = pose[1]
    dual = 0.5 * (Quaternion.Pure(pose[0]) * primal)
    return dq_angle_norm(DQ(DualQuaternion(real=primal, dual=dual).vec))


def dq_pow(dq_in: DQ, alpha: float) -> DQ:
    r"""Calculate pow for unit dual quaternions representing poses in cartesian space.

    :param dq_in: Input unit dual quaternion :math:`\boldsymbol{h}`.
    :type dq_in: DQ
    :param alpha: Power raising the dual quaternion :math:`\boldsymbol{h}^\alpha`.
    :type alpha: float
    :return: :math:`\boldsymbol{h}^\alpha`.
    :rtype: DQ
    """
    theta_half = np.arccos(np.clip(dq_in.q[0], -1, 1))
    out = np.zeros((8,))
    v_vec = vec3(dq_in)
    dual = vec3(dq_in.D())

    if not np.isclose(theta_half, 0.0):
        denom = np.sin(theta_half)
        theta_eps_half = -(dq_in.q[4] / denom)

        s = v_vec / denom
        s_eps = (dual - (theta_eps_half * np.cos(theta_half) * s)) / denom

        out[0] = np.cos(alpha * theta_half)
        out[1:4] = s * np.sin(alpha * theta_half)
        out[4] = -theta_eps_half * alpha * np.sin(alpha * theta_half)
        out[5:] = s_eps * np.sin(
            alpha * theta_half
        ) + theta_eps_half * alpha * s * np.cos(alpha * theta_half)
    else:
        out[0] = 1.0
        out[5:] = alpha * dual

    return DQ(out)


def dq_log(dq_in: DQ) -> DQ:
    """Perform the dual quaternion logarithm representing poses in Cartesian space.

    :param dq_in: Input unit dual quaternion.
    :type dq_in: DQ
    :return: The dual quaternion logartihm log(dq_in).
    :rtype: DQ
    """
    out = np.zeros((8,))
    theta_half = np.arccos(np.clip(dq_in.q[0], -1, 1))
    v_hat = dq_in.q[5:]
    if not np.isclose(theta_half, 0.0):
        sin_theta_half = np.sin(theta_half)
        theta_eps_half = -dq_in.q[4] / sin_theta_half
        v_vec = vec3(dq_in.P()) / sin_theta_half  # dq_in.q[1:4] / sin_theta_half
        v_eps = (
            v_hat - theta_eps_half * np.cos(theta_eps_half) * v_vec
        ) / sin_theta_half
        out[1:4] = theta_half * v_vec
        out[5:] = theta_eps_half * v_vec + theta_half * v_eps
    else:
        out[5:] = v_hat

    return DQ(out)


def dq_exp(dq_in: DQ) -> DQ:
    """Perform dual quaternion exponentiation for poses in Cartesian space.

    :param dq_in: Input unit dual quaternion.
    :type dq_in: DQ
    :return: The dual quaternion exponentiation exp(dq_in).
    :rtype: DQ
    """
    pure_primal = vec3(dq_in)
    pure_dual = vec3(dq_in.D())
    theta_half = np.linalg.norm(pure_primal)

    out = np.zeros((8,))

    if not np.isclose(theta_half, 0.0):
        s = pure_primal / theta_half
        theta_eps_half = np.dot(s, pure_dual)
        sin_theta_half = np.sin(theta_half)
        cos_theta_half = np.cos(theta_half)
        s_eps = (pure_dual - theta_eps_half * s) / theta_half
        out[0] = cos_theta_half
        out[1:4] = sin_theta_half * s
        out[4] = -theta_eps_half * sin_theta_half
        out[5:] = theta_eps_half * cos_theta_half * s + sin_theta_half * s_eps
    else:
        out[0] = 1.0
        out[5:] = pure_dual

    return DQ(out)


def dq_sclerp(current_pose: DQ, goal_pose: DQ, alpha: float) -> DQ:
    r"""Perform scLERP (dual quaternion interpolation from one pose to another).

    :param current_pose: Current pose.
    :type current_pose: DQ
    :param goal_pose: Goal pose.
    :type goal_pose: DQ
    :param alpha: Interpolation parameter where :math:`\alpha \in \left[0, 1\right]`.
    :type alpha: float
    :raises ValueError: If :math:`\alpha \not\in \left[0, 1\right]`.
    :return: Unit dual quaternion which represents the pose.
    :rtype: DQ
    """
    if not (0 <= alpha <= 1):
        msg = "alpha must lie between 0 and 1."
        raise ValueError(msg)
    # dot = np.dot(vec4(current_pose), vec4(goal_pose))
    delta = delta_dq(current_pose, goal_pose)

    # pow_delta = dq_pow(dq_angle_norm(delta_dq), alpha)
    pow_delta = dq_pow(delta, alpha)
    return current_pose * pow_delta


def dq_twist(current_dq: DQ, goal_dq: DQ, alpha: float) -> np.ndarray:
    r"""Generate 6d twist using sclerp.

    :param current_dq: Current pose represented as unit dual quaternion.
    :type current_dq: DQ
    :param goal_dq: Goal pose represented as unit dual quaternion.
    :type goal_dq: DQ
    :param alpha: Exponential s.t. :math:`\alpha \in \left[0, 1\right].`
    :type alpha: float
    :return: 6d twist :math:`\mathcal{V} \in \mathbb{R}^6`.
    :rtype: np.ndarray
    """
    next_point = dq_sclerp(current_dq, goal_dq, alpha)
    return vec6(dq_log(next_point * current_dq.conj()))


def dq_pose_error(dq_current: DQ, dq_desired: DQ) -> DQ:
    """Comput unit dual quaternion pose error

    :param dq_current: Current pose expressed as unit dual quaternion.
    :type dq_current: DQ
    :param dq_desired: Desired pose expressed as unit dual quaternion.
    :type dq_desired: DQ
    :return: Error pose expressed as unit dual quaternion.
    :rtype: DQ
    """
    dq_identity = np.zeros((8,))
    dq_identity[0] = 1.0
    return DQ(dq_identity) - delta_dq(dq_current, dq_desired)


def generate_intermediate_waypoints(
    start_pose: DQ, goal_pose: DQ, n_points: int
) -> list[DQ]:
    """Generate intermediate waypoints using unit dual quaternions.

    :param start_pose: Start pose represented as unit dual quaternion.
    :type start_pose: DQ
    :param goal_pose: Goal pose represented as unit dual quaternion.
    :type goal_pose: DQ
    :param n_points: Number of points to generate in total (including start- and goal pose).
    :type n_points: int
    :return: Generated intermediate waypoints.
    :rtype: list[DQ]
    """
    steps = np.linspace(0, 1, n_points)[1:-1]
    return (
        [start_pose]
        + [dq_sclerp(start_pose, goal_pose, step) for step in steps]
        + [goal_pose]
    )


def interpolate_waypoints(
    waypoints: list[tuple[np.ndarray, UnitQuaternion]],
    n_points: int,
    adaptive: bool = False,
) -> list[tuple[np.ndarray, UnitQuaternion]]:
    r"""Insert n_points between intermediate waypoints.

    :param waypoints: List of poses.
    :type waypoints: list[tuple[np.ndarray, np.ndarray, float]]
    :param n_points: points to be inserted between two intermediate poses.
    :type n_points: int
    :param adaptive: Set number of waypoint depending on dual quaternion error.
        Between two points then :math:`\lfloor e \left(n_p + 2\right)\rfloor - 2` are inserted,
        where :math:`e_{clipped} \in \left[0, 1\right]` represents the clipped norm of the dual quaternion error s.t. :math:`e_{clipped} = \min\left(e, 1\right), e \ge 0`.
        Defaults to False
    :type adaptive: bool, optional
    :return: New waypoints.
    :rtype: list[tuple[np.ndarray, np.ndarray, float]]
    """
    out = []
    for i in range(len(waypoints) - 1):
        left = pose_to_dq(waypoints[i])
        right = pose_to_dq(waypoints[i + 1])
        error = np.linalg.norm(vec8(dq_pose_error(left, right))) if adaptive else 1.0
        error = np.clip(error, 0.0, 1.0)
        points2add = [
            dq_to_pose(pose)
            for pose in generate_intermediate_waypoints(
                left, right, int(float(n_points + 2) * error)
            )[:-1]
        ]
        out += points2add

    return [*out, waypoints[-1]]
