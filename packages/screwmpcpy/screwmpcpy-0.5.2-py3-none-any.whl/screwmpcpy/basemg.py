"""Base motion generation module."""
from __future__ import annotations

import numpy as np
import scipy as scp
from dqrobotics import DQ

from .dqutil import dq_exp, dq_pose_error, dq_twist
from .screwmpc import BOUND, ScrewMPC


class BaseMotionGenerator(ScrewMPC):
    r"""Base Motion generator for Dual Quaternions, while considering jerk-, acceleration- and velocity constraints.

    :param n_p: Prediction horizon :math:`n_p`.
    :type n_p: int
    :param n_c: Control horizon :math:`n_c`.
    :type n_c: int
    :param q_mpc: :math:`\boldsymbol{Q}=q_{mpc}\boldsymbol{I}`.
    :type q_mpc: float
    :param r_mpc: :math:`\boldsymbol{R}=r_{mpc}\boldsymbol{I}`.
    :type r_mpc: float
    :param lu_bound_vel: lower- and upper bound for velocity.
    :type lu_bound_vel: BOUND
    :param lu_bound_acc: lower- and upper bound for accerlation.
    :type lu_bound_acc: BOUND
    :param lu_bound_jerk: lower- and upper bound for jerk.
    :type lu_bound_jerk: BOUND
    :param sclerp: ScLERP interpolation for EE pose generatation,
        must lie in :math:`\left(0, 1\right]`, defaults to 0.1.
    :raises ValueError: If sclerp :math:`\not\in\left(0, 1\right]`.
    """

    def __init__(
        self,
        n_p: int,
        n_c: int,
        q_mpc: float,
        r_mpc: float,
        lu_bound_vel: BOUND,
        lu_bound_acc: BOUND,
        lu_bound_jerk: BOUND,
        sclerp: float = 0.1,
    ) -> None:
        super().__init__(
            n_p, n_c, q_mpc, r_mpc, lu_bound_vel, lu_bound_acc, lu_bound_jerk
        )

        if not 0 < sclerp <= 1:
            msg = "Select sclerp between 0 and 1!"
            raise ValueError(msg)

        self._sclerp = sclerp

        # setup internal states, matrices and kinematics
        self._mpc_state = np.zeros((18,))
        self._u_state = np.zeros((6,))
        self._sparse_state_transition = scp.sparse.csc_matrix(self.a_matrix)
        self._sparse_ctrl = scp.sparse.csc_matrix(self.b_matrix)

    def reset(self) -> None:
        """Reset internal states and solver."""
        self._u_state = np.zeros_like(self._u_state)
        self._mpc_state = np.zeros_like(self._mpc_state)
        self._solver = None

    def step(self, current_dq: DQ, goal_dq: DQ) -> tuple[DQ, DQ]:
        """Perform one step for motion generation.

        :param current_dq: Current pose represented as Dual Quaternion.
        :type current_dq: DQ
        :param goal_dq: Goal pose represented as Dual Quaternion.
        :type goal_dq: DQ
        :return: Cartesian pose error represented and smooth trajectory.
        :rtype: tuple[DQ, DQ]
        """

        # perform optimization
        desired_twist = dq_twist(current_dq, goal_dq, self._sclerp)
        du = super().solve(desired_twist, self._u_state, self._mpc_state)[:6]

        # calculate the errors and compute commanded dq
        twist_out = DQ(self._mpc_state[-6:])
        smooth_traj = dq_exp(twist_out) * current_dq
        error = dq_pose_error(current_dq, smooth_traj)

        # update necessary states
        self._mpc_state = (
            self._sparse_state_transition @ self._mpc_state + self._sparse_ctrl @ du
        )
        self._u_state += du

        return error, smooth_traj

    @property
    def mpc_state(self) -> np.ndarray:
        r"""Read the mpc state

        :return: :math:`\boldsymbol{s}_{mpc} \in \mathbb{R}^{18}`.
        :rtype: np.ndarray
        """
        return self._mpc_state

    @property
    def u_state(self) -> np.ndarray:
        r"""Read current internal twist state

        :return: Current internal twist state :math:`\boldsymbol{u} \in \mathbb{R}^6`.
        :rtype: np.ndarray
        """
        return self._u_state
