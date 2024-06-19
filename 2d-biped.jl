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


left_shin_mesh = load("biped_model/shin.STL")
setobject!(vis[:robot][:left_shin], left_shin_mesh)

right_shin_mesh = load("biped_model/shin.STL")
setobject!(vis[:robot][:right_shin], right_shin_mesh)

left_thigh_mesh = load("biped_model/thigh.STL")
setobject!(vis[:robot][:left_thigh], left_thigh_mesh)

right_thigh_mesh = load("biped_model/thigh.STL")
setobject!(vis[:robot][:right_thigh], right_thigh_mesh)

left_hip_mesh = load("biped_model/hip.STL")
setobject!(vis[:robot][:left_hip], left_hip_mesh)

right_hip_mesh = load("biped_model/hip.STL")
setobject!(vis[:robot][:right_hip], right_hip_mesh)

left_body_mesh = load("biped_model/body.STL")
setobject!(vis[:robot][:left_body], left_body_mesh)

delete!(vis[:robot])



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