#!/bin/sh

# Example 1 - Simple online interaction
# We expect one answer set. Extract one cStateChoice, many cActionCovers!
clingo ps.lp pAs.lp project_online.lp car_ord.lp car_psi.lp 0

# Example 2 - State-action pairs covered by an abstract state-actionpair
clingo psi.lp car_psi.lp restrict.lp project_states.lp project_actions.lp 0
