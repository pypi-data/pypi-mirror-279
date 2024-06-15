"""Defines the MDP class."""

from typing import Dict, Tuple

import symengine.lib.symengine_wrapper as core
from xaddpy.xadd.xadd import VAR_TYPE

from pyRDDLGym_symbolic.core.model import RDDLModelXADD
from pyRDDLGym_symbolic.mdp import Action, CAction, BActions


class MDP:
    """Defines the MDP class.
    
    Args:
        model: The RDDL model compiled in XADD.
        is_linear: Whether the MDP is linear or not.
        discount: The discount factor.
        concurrency: The number of concurrent boolean actions.
    """
    def __init__(
            self,
            model: RDDLModelXADD,
            is_linear: bool = False,
            discount: float = 1.0,
            concurrency: int = 1,
    ):
        self.model = model
        self.context = model.context
        self.is_linear = is_linear
        self.discount = discount
        self.cpfs = {}
        self.max_allowed_actions = concurrency
        self._prime_subs = self.get_prime_subs()

        self.cont_ns_vars = set()
        self.bool_ns_vars = set()
        self.cont_i_vars = set()
        self.bool_i_vars = set()
        self.bool_s_vars = set()
        self.bool_a_vars = set()
        self.cont_s_vars = set()
        self.cont_a_vars = set()

        self.actions: Dict[str, Action] = {}
        self.bool_actions: Dict[str, BActions] = {}
        self.cont_actions: Dict[str, CAction] = {}
        self.a_var_to_action: Dict[VAR_TYPE, Action] = {}
        self.action_to_a_var: Dict[Action, VAR_TYPE] = {}

        # Bounds
        self.cont_state_bounds: Dict[core.Symbol, Tuple[float, float]] = {}
        self.cont_action_bounds: Dict[core.Symbol, Tuple[float, float]] = {}

        # Cache
        self.cont_regr_cache: Dict[Tuple[str, int, int], int] = {}

    def get_prime_subs(self) -> Dict[VAR_TYPE, VAR_TYPE]:
        """Returns the substitution dictionary for the primed variables."""
        m = self.model
        s_to_ns = m.next_state
        prime_subs = {}
        for s, ns in s_to_ns.items():
            s_var = m.ns[s]
            ns_var, var_node_id = m.add_sym_var(ns, m.variable_ranges[ns])
            prime_subs[s_var] = ns_var
        return prime_subs

    def update_state_var_sets(self):
        m = self.model
        for v, vtype in m.variable_ranges.items():
            if v in m.non_fluents:
                continue
            v_, v_node_id = m.add_sym_var(v, vtype)
            if v in m.state_fluents:
                if vtype == 'bool':
                    self.bool_s_vars.add(v_)
                else:
                    self.cont_s_vars.add(v_)

    def update_i_and_ns_var_sets(self):
        m = self.model
        for v, vtype in m.variable_ranges.items():
            if v in m.non_fluents:
                continue
            v_, v_node_id = m.add_sym_var(v, vtype)
            if v in m.next_state.values():
                if vtype == 'bool':
                    self.bool_ns_vars.add(v_)
                else:
                    self.cont_ns_vars.add(v_)
            elif v in m.interm_fluents:
                if vtype == 'bool':
                    self.bool_i_vars.add(v_)
                else:
                    self.cont_i_vars.add(v_)

    def add_action(self, action: Action):
        """Adds an action to the MDP."""
        self.actions[action.name] = action
        if isinstance(action, BActions):
            self.bool_a_vars.update(set(action.symbol))
            self.bool_actions[action.name] = action
        elif isinstance(action, CAction):
            self.cont_a_vars.add(action.symbol)
            self.cont_actions[action.name] = action
        else:
            raise ValueError(f'{action} is not a valid action type.')

    def update(self, is_vi: bool) -> None:
        """Goes through all CPFs and actions and updates them."""
        dual_cpfs_bool = {}
        action_subst_dict = {a: False for a in self.bool_a_vars}
        for v_name, cpf in self.model.cpfs.items():
            # Handle Boolean next state and interm variables.
            s_v_name = self.model._var_name_to_sym_var_name[v_name]
            v = self.context._str_var_to_var[s_v_name]
            if v.is_Boolean and (
                (v_name in self.model.next_state.values() or v_name in self.model.interm_fluents)
            ):
                cpf_ = dual_cpfs_bool.get(v_name)
                if cpf_ is None:
                    var_id, _ = self.context.get_dec_expr_index(v, create=False)
                    high = cpf
                    low = self.context.apply(self.context.ONE, high, op='subtract')
                    cpf_ = self.context.get_inode_canon(var_id, low, high)
                    dual_cpfs_bool[v_name] = cpf_
                cpf = cpf_

            # Update CPFs and reward.
            self.cpfs[v] = cpf
            for a_name, act in self.actions.items():
                cpf_ = cpf
                # Boolean actions can be restricted for VI.
                if is_vi and isinstance(act, BActions):
                    cpf_ = act.restrict(cpf_, action_subst_dict)
                    reward = act.restrict(self.reward, action_subst_dict)
                else:
                    reward = self.reward
                act.add_cpf(v, cpf_)
                act.reward = reward

    @property
    def prime_subs(self):
        return self._prime_subs

    @property
    def reward(self) -> int:
        return self.model.reward

    @prime_subs.setter
    def prime_subs(self, prime_subs: Dict[VAR_TYPE, VAR_TYPE]):
        self._prime_subs = prime_subs

    def get_bounds(self, a: core.Symbol) -> Tuple[float, float]:
        return self.cont_action_bounds[a]

    def standardize(self, dd: int) -> int:
        """Standardizes the given XADD node."""
        dd = self.context.make_canonical(dd)
        if self.is_linear:
            dd = self.context.reduce_lp(dd)
        return dd
