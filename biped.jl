using Pkg; Pkg.activate(@__DIR__)

using MeshCat
using MeshCatMechanisms
using RigidBodyDynamics
using FileIO, MeshIO
using GeometryBasics

vis = Visualizer()
render(vis)

##

urdfpath = joinpath(@__DIR__, "biped_model/biped.urdf");
mech = parse_urdf(urdfpath, floating=true, remove_fixed_tree_joints=true)

delete!(vis)
mvis = MechanismVisualizer(mech, URDFVisuals(urdfpath), vis)

##

function rk4(model::Nadia, x, u, h; gains=RigidBodyDynamics.default_constraint_stabilization_gains(Float64))
    k1 = dynamics(model, x, u; gains=gains)
    k2 = dynamics(model, x + h/2*k1, u; gains=gains)
    k3 = dynamics(model, x + h/2*k2, u; gains=gains)
    k4 = dynamics(model, x + h*k3, u; gains=gains)
    return x + h/6*(k1 + 2*k2 + 2*k3 + k4)
end

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