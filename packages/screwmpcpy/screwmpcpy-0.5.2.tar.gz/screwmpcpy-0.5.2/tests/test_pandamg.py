"""Test the motion generator for panda robot."""
from __future__ import annotations

import numpy as np
import pytest
from dqrobotics import vec8
from dqrobotics.robots import FrankaEmikaPandaRobot
from roboticstoolbox.models import Panda

from screwmpcpy.pandamg import PandaScrewMotionGenerator, PandaScrewMpMotionGenerator
from screwmpcpy.screwmpc import BOUND


def test_panda_base_mg():
    """Test base panda motion generator."""
    Np = 50  # prediction horizon, can be tuned;
    Nc = 10  # control horizon, can be tuned
    R = 10e-3  # weight matirix
    Q = 10e9  # weight matrix

    JOINT_STATE = np.array(
        [
            0.000165068,
            -0.785579,
            0.000134417,
            -2.35485,
            0.00100466,
            1.57225,
            0.785951,
            -6.904296578564673e-18,
            7.806316005606509e-17,
            -3.694169137454414e-17,
            1.075687377186247e-16,
            -2.603546867034339e-17,
            -2.953811484569149e-17,
            -5.316185667767154e-17,
        ]
    )

    ub_jerk = np.array([8500.0, 8500.0, 8500.0, 4500.0, 4500.0, 4500.0])
    lb_jerk = -ub_jerk.copy()

    ub_acc = np.array([17.0, 17.0, 17.0, 9.0, 9.0, 9.0])
    lb_acc = -ub_acc.copy()

    ub_v = np.array([2.5, 2.5, 2.5, 3.0, 3.0, 3.0])
    lb_v = -ub_v.copy()

    jerk_bound = BOUND(lb_jerk, ub_jerk)
    acc_bound = BOUND(lb_acc, ub_acc)
    vel_bound = BOUND(lb_v, ub_v)

    franka_kin = FrankaEmikaPandaRobot.kinematics()
    goal = franka_kin.fkm(
        [0.173898, 0.667434, 0.782032, -1.86421, 1.44847, 1.57491, 0.889156]
    )

    mg = PandaScrewMotionGenerator(Np, Nc, Q, R, vel_bound, acc_bound, jerk_bound)
    dq = mg.step(JOINT_STATE[: JOINT_STATE.shape[0] // 2], goal)

    np.testing.assert_almost_equal(dq, JOINT_STATE[JOINT_STATE.shape[0] // 2 :])
    mg.reset()
    assert mg._solver is None

    # assert that reset enforces all zeros
    assert not np.any(mg._mpc_state)
    assert not np.any(mg._u_state)
    assert not np.any(mg.mpc_state)
    assert not np.any(mg.u_state)

    error_msg = "Select sclerp between 0 and 1!"
    with pytest.raises(ValueError, match=error_msg):
        PandaScrewMotionGenerator(Np, Nc, Q, R, vel_bound, acc_bound, jerk_bound, -1)


def test_panda_manipulability_mg():
    """Test panda manipulability motion generator."""
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

    # np.testing.assert_almost_equal(dq, JOINT_STATE[JOINT_STATE.shape[0] // 2 :])

    error_msg = "Select sclerp between 0 and 1!"
    with pytest.raises(ValueError, match=error_msg):
        PandaScrewMpMotionGenerator(Np, Nc, Q, R, vel_bound, acc_bound, jerk_bound, -1)

    error_msg = "rho_i must be greater than rho_s!"
    with pytest.raises(ValueError, match=error_msg):
        PandaScrewMpMotionGenerator(
            Np, Nc, Q, R, vel_bound, acc_bound, jerk_bound, rho_i=0.1, rho_s=0.9
        )


def test_panda_mg_util():
    """Test the utility functions on correctness!"""

    Np = 50  # prediction horizon, can be tuned;
    Nc = 10  # control horizon, can be tuned
    R = 10e-3  # weight matirix
    Q = 10e9  # weight matrix
    JOINT_STATE = np.array(
        [0.173898, 0.667434, 0.782032, -1.86421, 1.44847, 1.57491, 0.889156]
    )

    ub_jerk = np.array([8500.0, 8500.0, 8500.0, 4500.0, 4500.0, 4500.0])
    lb_jerk = -ub_jerk.copy()

    ub_acc = np.array([17.0, 17.0, 17.0, 9.0, 9.0, 9.0])
    lb_acc = -ub_acc.copy()

    ub_v = np.array([2.5, 2.5, 2.5, 3.0, 3.0, 3.0])
    lb_v = -ub_v.copy()

    jerk_bound = BOUND(lb_jerk, ub_jerk)
    acc_bound = BOUND(lb_acc, ub_acc)
    vel_bound = BOUND(lb_v, ub_v)
    mg = PandaScrewMpMotionGenerator(Np, Nc, Q, R, vel_bound, acc_bound, jerk_bound)
    model = Panda()

    upper = model.qdlim[:7]
    lower = -upper.copy()

    dist_low = JOINT_STATE - lower
    dist_up = upper - JOINT_STATE
    dist_low = np.abs(np.mod((dist_low + np.pi), 2 * np.pi) - np.pi)
    dist_up = np.abs(np.mod((dist_up + np.pi), 2 * np.pi) - np.pi)
    dist = np.where(dist_low < dist_up, dist_low, dist_up)
    idx = np.where(dist < mg._rho_i)[0]

    b_ineq = np.zeros_like(dist)
    b_ineq[idx] = mg._damping_gain * (dist[idx] - mg._rho_s) / (mg._rho_i - mg._rho_s)
    _b_ineq, _idx = mg._get_b_ineq(JOINT_STATE)

    _a_ineq = mg._get_a_ineq(7, mg._m_lower.shape[0], _idx)
    a_ineq = np.zeros((7, 13))
    a_ineq[idx, idx] = 1

    franka_kin = FrankaEmikaPandaRobot.kinematics()
    goal = franka_kin.fkm(JOINT_STATE)

    # seed motion generator for further calculations
    mg.step(
        JOINT_STATE,
        goal,
    )

    _c_vec = mg._get_c_vec(np.squeeze(model.jacobm(JOINT_STATE)))
    c_vec = np.zeros((13,))
    c_vec[:7] = -np.squeeze(model.jacobm(JOINT_STATE))

    q_mat = np.eye(13)
    _indices = np.arange(7)
    q_mat[_indices, _indices] = mg._gain
    _indices = np.arange(7, 13)
    error = np.linalg.norm(vec8(mg._dqerror))
    q_mat[_indices, _indices] = np.reciprocal(error)
    _q_mat = mg._get_q(7, mg._gain, np.reciprocal(error))
    jacobian = model.jacob0(JOINT_STATE)

    hessian = model.hessian0(JOINT_STATE, J0=jacobian)
    manipulability = model.manipulability(JOINT_STATE, J=jacobian)
    _j_m = mg._calc_jacobm(hessian, jacobian, manipulability)

    j_m = np.squeeze(model.jacobm(JOINT_STATE, jacobian))

    assert np.linalg.norm(j_m - _j_m) < 1e-12

    np.testing.assert_equal(a_ineq, _a_ineq)
    np.testing.assert_equal(_b_ineq, b_ineq)
    np.testing.assert_equal(_idx, idx)
    np.testing.assert_equal(_c_vec, c_vec)
    np.testing.assert_equal(_q_mat, q_mat)
