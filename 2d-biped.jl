using Pkg; Pkg.activate(@__DIR__)

using MeshCat

vis = Visualizer()
render(vis)

##

# Figure out dynamics (probably with Lagrangian dynamics?)
# Maybe try figuring it out with Newtonian dynamics also

# Simulate the dynamics with contact (might require solving
# an optimization problem to ensure that the feet don't go
# through the ground)

# Write stabilizing controller (start with LQR) to balance
# maybe start with feet fixed to ground with baumgarte 
# stabilization for this

# Write stabilizing controller that can handle constraints
# friction cone constraints, joint limits, torque limits, etc.

# Write controller that can track a walking trajectory
# might require hybrid dynamics?