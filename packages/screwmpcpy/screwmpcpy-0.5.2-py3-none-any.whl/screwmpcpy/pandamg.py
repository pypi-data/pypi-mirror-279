"""Screw based motion generators for panda robot."""
from __future__ import annotations

import numpy as np
import qpsolvers as qp
import roboticstoolbox as rtb
import scipy as scp
from dqrobotics import C8, DQ, haminus8, vec8
from dqrobotics.robots import FrankaEmikaPandaRobot
from dqrobotics.utils.DQ_LinearAlgebra import pinv

from .basemg import BaseMotionGenerator
from .screwmpc import BOUND


class PandaScrewMotionGenerator(BaseMotionGenerator):
    r"""Motion generator for Panda robot using Dual Quaternions, while considering jerk-, acceleration- and velocity constraints.

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
        must lie in :math:`\left(0, 1\right]`, defaults to 0.1
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
            n_p, n_c, q_mpc, r_mpc, lu_bound_vel, lu_bound_acc, lu_bound_jerk, sclerp
        )

        self._kin = FrankaEmikaPandaRobot.kinematics()
        self._dqerror: DQ = None

    def step(self, q_robot: np.ndarray, goal: DQ) -> np.ndarray:
        r"""Perform one step for motion generation.

        :param q_robot: robot joint angles :math:`q \in \mathbb{R}^7`.
        :type q_robot: np.ndarray
        :param goal: Goal pose represented as Dual Quaternion.
        :type goal: DQ
        :return: commanded joint velocity :math:`\dot{\boldsymbol{q}} \in \mathbb{R}^7`.
        :rtype: np.ndarray
        """

        x_current = self._kin.fkm(q_robot)
        error, smooth_traj = super().step(x_current, goal)
        dot_x = vec8(error)
        j_pose = np.linalg.multi_dot(
            [haminus8(smooth_traj), C8(), self._kin.pose_jacobian(q_robot)]
        )
        self._dqerror = error
        return pinv(j_pose) @ dot_x

    @property
    def dqerror(self) -> DQ:
        """Get the DQ error of the last optimization step.

        :return: The dual quaternion error of the last optimization step
        :rtype: DQ
        """
        return self._dqerror


class PandaScrewMpRGMotionGenerator(PandaScrewMotionGenerator):
    r"""
    Motion generator for Panda robot using Dual Quaternions, while considering jerk-, acceleration- and velocity constraints.
    Further, the manipulability of the robot is considered. The manipulability is maximized in nullspace via a reduced gradient approach.

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
        must lie in :math:`\left(0, 1\right]`, defaults to 0.1
    :type sclerp: float, optional
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
            n_p, n_c, q_mpc, r_mpc, lu_bound_vel, lu_bound_acc, lu_bound_jerk, sclerp
        )

        self._panda_rtb = rtb.models.Panda()

    def step(self, q_robot: np.ndarray, goal: DQ) -> np.ndarray:
        r"""Perform one step for motion generation.
            The best 6 best joints for task space operations is selected via qr-decomposition
            with column pivoting. The remaining joint maximizes the manipulability of the robot.

        :param q_robot: robot joint angles :math:`q \in \mathbb{R}^7`.
        :type q_robot: np.ndarray
        :param goal: Goal pose represented as Dual Quaternion.
        :type goal: DQ
        :return: commanded joint velocity :math:`\dot{\boldsymbol{q}} \in \mathbb{R}^7`.
        :rtype: np.ndarray
        """
        q_dot = PandaScrewMotionGenerator.step(self, q_robot, goal)
        jacobian = self._panda_rtb.jacob0(q_robot)
        hessian = self._panda_rtb.hessian0(q_robot, J0=jacobian)
        mp = self._panda_rtb.manipulability(q_robot, jacobian)
        objective = self._calc_jacobm(hessian, jacobian, mp) * np.reciprocal(
            np.linalg.norm(vec8(self.dqerror))
        )

        twist = jacobian @ q_dot

        # find the pivots for task space
        pivots = scp.linalg.qr(jacobian, pivoting=True, mode="economic")[-1]

        jac_reduced_inv = np.linalg.inv(jacobian[:, pivots[:-1]])
        jac_col = jacobian[:, pivots[-1]]

        q_b_dot = objective[pivots[-1]] - np.dot(
            (jac_reduced_inv @ jac_col), objective[pivots[:-1]]
        )
        q_a_dot = jac_reduced_inv @ (twist - jac_col * q_b_dot)
        q_dot[pivots[:-1]] = q_a_dot
        q_dot[pivots[-1]] = q_b_dot

        return q_dot

    def _calc_jacobm(
        self, hessian: np.ndarray, jacobian: np.ndarray, manipulabilty: float
    ) -> np.ndarray:
        r"""Calculate the manipulabilty gradient in vectorized manner

        :param hessian: The robot hessian :math:`\boldsymbol{H} \in \mathbb{R}^{n_{dof} \times 6 \times n_{dof}}`
        :type hessian: np.ndarray
        :param jacobian: The robot jacobian :math:`\boldsymbol{J} \in \mathbb{R}^{n_{dof} \times 6}`
        :type jacobian: np.ndarray
        :param manipulabilty: The manipulability :math:`m`.
        :type manipulabilty: float
        :return: The manipulabilty gradient :math:`\boldsymbol{J}_m \in \mathbb{R}^{n_{dof}}`
        :rtype: np.ndarray
        """
        j_dot_h_t = jacobian[None] @ hessian.transpose(0, 2, 1)
        inv = np.linalg.inv(jacobian @ jacobian.T).reshape(-1)
        res = (
            j_dot_h_t.reshape((j_dot_h_t.shape[0], np.prod(j_dot_h_t.shape[1:]))) @ inv
        )
        return manipulabilty * res


class PandaScrewMpMotionGenerator(PandaScrewMpRGMotionGenerator):
    r"""
    Motion generator for Panda robot using Dual Quaternions, while considering jerk-, acceleration- and velocity constraints.
    Further, the manipulability of the robot is considered. The manipulability is maximized via an additional quadratic program.

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
        must lie in :math:`\left(0, 1\right]`, defaults to 0.1
    :type sclerp: float, optional
    :param slack: slack variable for manipulability maximization, defaults to 10.0
    :type slack: float, optional.
    :param gain: gain for manipulabiliy quadratic program, defaults to 0.01.
    :type gain: float, optional.
    :param rho_i: Influence distance :math:`rho_i`, defaults to 0.87 rad.
    :type rho_i: float, optional.
    :param rho_s: Stopping distance :math:`rho_s`, defaults to 0.03 rad.
    :type rho_s: float, optional.
    :param damping_gain: The joint velocity damping gain used for inequality constraints. If negative or zero,
        the inequality constraints and thus the joint velocities and therefore the joint limits are
        ignored in the quadratic program. Defaults to 0.0.
    :type damping_gain: float, optional.
    :raises ValueError: If :math:`\rho_i \leq \rho_s`.
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
        slack: float = 10.0,
        gain: float = 0.01,
        rho_i: float = 0.87,
        rho_s: float = 0.03,
        damping_gain: float = 0.0,
    ) -> None:
        super().__init__(
            n_p, n_c, q_mpc, r_mpc, lu_bound_vel, lu_bound_acc, lu_bound_jerk, sclerp
        )

        rho_i = abs(rho_i)
        rho_s = abs(rho_s)
        gain = abs(gain)

        if rho_i <= rho_s:
            msg = "rho_i must be greater than rho_s!"
            raise ValueError(msg)

        self._gain = gain
        self._rho_i = rho_i
        self._rho_s = rho_s
        self._m_upper = np.zeros((13,))
        self._m_upper[:7] = self._panda_rtb.qdlim[:7]
        self._m_upper[7:] = abs(slack)
        self._m_lower = -self._m_upper.copy()
        self._damping_gain = damping_gain

    def step(self, q_robot: np.ndarray, goal: DQ) -> np.ndarray:
        r"""Perform one step for motion generation.

        :param q_robot: robot joint angles :math:`q \in \mathbb{R}^7`.
        :type q_robot: np.ndarray
        :param goal: Goal pose represented as Dual Quaternion.
        :type goal: DQ
        :raises ValueError: If the the number of arguments mismatch.
        :return: commanded joint velocity :math:`\dot{\boldsymbol{q}} \in \mathbb{R}^7`.
        :rtype: np.ndarray
        """

        dq_desired = PandaScrewMotionGenerator.step(self, q_robot, goal)
        return self._get_dq(dq_desired, q_robot)

    def _get_b_ineq(self, q_robot: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        """Get the inequality constraints.

        :param q_robot: Current robot configuration (joint angles).
        :type q_robot: np.ndarray
        :return: The inequality constraints and the indices where the constraints are active.
        :rtype: Tuple[np.ndarray, np.ndarray]
        """
        upper = self._panda_rtb.qdlim[:7]
        lower = -upper.copy()
        distu = upper - q_robot
        distl = q_robot - lower
        distu = np.abs(np.mod((distu + np.pi), 2 * np.pi) - np.pi)
        distl = np.abs(np.mod((distl + np.pi), 2 * np.pi) - np.pi)

        dist = np.where(distl < distu, distl, distu)
        idx = np.where(dist < self._rho_i)[0]
        out = np.zeros_like(dist)
        out[idx] = self._damping_gain * (
            (dist[idx] - self._rho_s) / (self._rho_i - self._rho_s)
        )
        return out, idx

    def _get_a_ineq(
        self, n_dof: int, n_const: int, active_idx: np.ndarray
    ) -> np.ndarray:
        r"""Get the in equality matrix.

        :param n_dof: DoF of robot arm.
        :type n_dof: int
        :param n_const: Number of constraints :math:`n_{const}`.
        :type n_const: int
        :param active_idx: The indices where the constraints are active.
        :type active_idx: np.ndarray
        :return: the inequality matrix :math:`\boldsymbol{A} \in \mathbb{R}^{n_{dof} \times n_{const}}`
        :rtype: np.ndarray
        """
        out = np.zeros((n_dof, n_const))
        out[active_idx, active_idx] = 1.0
        return out

    def _get_q(self, n_dof: int, joint_gain: float, slack_gain: float) -> np.ndarray:
        r"""Get symmetric cost matrix :math:`\boldsymbol{Q}` for quadratic program.

        :param n_dof: DoF of robot arm.
        :type n_dof: int
        :param joint_gain: joint velocity gain.
        :type joint_gain: float
        :param slack_gain: slack gain.
        :type slack_gain: float
        :return: _description_
        :rtype: np.ndarray
        """
        q_mat = np.eye(n_dof + 6)
        idx = np.arange(n_dof)
        q_mat[idx, idx] = joint_gain
        idx = np.arange(n_dof, q_mat.shape[-1])
        q_mat[idx, idx] = slack_gain
        return q_mat

    def _get_c_vec(self, jac_m: np.ndarray) -> np.ndarray:
        r"""Get cost vector :math:`\boldsymbol{c} \in \mathbb{R}^{n_{dof} + 6}`,
            where :math:`n_{dof}` denotes the DoF of the robot arm.

        :param jac_m: Manipulability jacobian gradient :math:`\boldsymbol{J}_m \in mathbb{R}^{n_{dof}}`.
        :type jac_m: np.ndarray
        :return: Cost vector :math:`\boldsymbol{c} \in \mathbb{R}^{n_{dof} + 6}`.
        :rtype: np.ndarray
        """
        out = np.zeros((jac_m.shape[0] + 6,))
        out[: jac_m.shape[0]] = -jac_m
        return out

    def _get_j_eq(self, j_robot: np.ndarray) -> np.ndarray:
        r"""Get the equality matrix :math:`\mathcal{J} \in \mathbb{R}^{6 \times \left(n_{dof} + 6\right)}`.

        :param j_robot: Robot jacobian :math:`\boldsymbol{J} \in \mathbb{R}^{n_{dof} \times 6}}`
        :type j_robot: np.ndarray
        :return: Equality matrix :math:`\mathcal{J} \in \mathbb{R}^{6 \times \left(n_{dof} + 6\right)}`.
        :rtype: np.ndarray
        """
        _identity = np.eye(6)
        return np.concatenate([j_robot, _identity], axis=-1)

    def _get_dq(self, dq_desired: np.ndarray, q_robot: np.ndarray) -> np.ndarray:
        r"""Include the manipulability- and velocity constraints for desired joint velocities.

        :param dq_desired: The desired joint velocities.
        :type dq_desired: np.ndarray
        :param q_robot: Current robot configuration :math:`\boldsymbol{q} \in \mathbb{R}^{n_{dof}}`.
        :type q_robot: np.ndarray
        :return: Corrected joint velocities.
        :rtype: np.ndarray
        """
        jacobian = self._panda_rtb.jacob0(q_robot)
        hessian = self._panda_rtb.hessian0(q_robot, J0=jacobian)
        mp = self._panda_rtb.manipulability(q_robot, jacobian)
        twist = jacobian @ dq_desired
        error_norm = np.linalg.norm(vec8(self.dqerror))
        a_eq = self._get_j_eq(jacobian)
        q_mat = self._get_q(q_robot.shape[0], self._gain, np.reciprocal(error_norm))
        c_vec = self._get_c_vec(self._calc_jacobm(hessian, jacobian, mp))

        if self._damping_gain > 0:
            b_ineq, idx = self._get_b_ineq(q_robot)
            a_ineq = self._get_a_ineq(q_robot.shape[0], self._m_upper.shape[0], idx)
        else:
            b_ineq = None
            a_ineq = None

        return qp.solve_qp(
            q_mat,
            c_vec,
            a_ineq,
            b_ineq,
            a_eq,
            twist,
            lb=self._m_lower,
            ub=self._m_upper,
            solver="daqp",
        )[: q_robot.shape[0]]
