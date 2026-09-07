"""Author owned Blender rigid bodies and joint constraints."""

import bpy
import bmesh
from math import radians


def own_object(obj, collection, role, bone):
    for linked in list(obj.users_collection):
        linked.objects.unlink(obj)
    collection.objects.link(obj)
    obj["ragdoll_role"] = role
    obj["ragdoll_bone"] = bone
    obj.hide_render = True
    obj.display_type = "WIRE"


def create_bodies(context, collection, regions):
    bodies = {}
    # Skin-weight regions can be nearly empty at short spine/neck bones. Using
    # their proxy volume as mass creates extreme adjacent mass ratios. These
    # explicit segment weights keep the articulated chain physically solvable.
    masses = {"Hips":8, "Spine":4, "Spine1":4, "Spine2":8, "Neck":2, "Head":4}
    for side in ("Left", "Right"):
        masses.update({side+"Shoulder":2, side+"Arm":3, side+"ForeArm":2,
                       side+"Hand":2, side+"UpLeg":5, side+"Leg":4, side+"Foot":2})
    mass_scale = 70.0 / sum(masses.values())
    for name, region in regions.items():
        if region["hull_points"]:
            mesh = bpy.data.meshes.new(f"RD_Hull_{name}")
            bm = bmesh.new()
            try:
                for point in region["hull_points"]:
                    bm.verts.new(point)
                bmesh.ops.remove_doubles(bm, verts=list(bm.verts), dist=1e-6)
                bmesh.ops.convex_hull(bm, input=list(bm.verts), use_existing_faces=False)
                bm.to_mesh(mesh)
            finally:
                bm.free()
            body = bpy.data.objects.new(f"RD_Body_{name}", mesh)
            collection.objects.link(body)
        else:
            bpy.ops.mesh.primitive_cube_add(size=1)
            body = context.object
            body.name = f"RD_Body_{name}"
            for vertex in body.data.vertices:
                for axis in range(3):
                    vertex.co[axis] *= region["dimensions"][axis]
        own_object(body, collection, "body", name)
        body.matrix_world = region["matrix"]
        bpy.ops.object.select_all(action="DESELECT")
        body.select_set(True)
        context.view_layer.objects.active = body
        bpy.ops.rigidbody.object_add()
        rb = body.rigid_body
        rb.type = "ACTIVE"
        rb.collision_shape = "CONVEX_HULL" if region["hull_points"] else "BOX"
        rb.mass = masses[name] * mass_scale
        rb.friction = 0.8
        rb.restitution = 0.0
        rb.linear_damping = 0.75
        rb.angular_damping = 0.95
        rb.use_margin = True
        rb.collision_margin = 0.001
        rb.use_deactivation = True
        rb.use_start_deactivated = False
        bodies[name] = body
    return bodies


def create_joints(context, collection, regions, bodies):
    joints = []
    for name, region in regions.items():
        parent_name = region["parent"]
        if parent_name is None:
            continue
        joint = bpy.data.objects.new(f"RD_Joint_{name}", None)
        collection.objects.link(joint)
        joint.empty_display_type = "ARROWS"
        joint.empty_display_size = 0.04
        joint.matrix_world = region["joint_matrix"]
        joint["ragdoll_role"] = "joint"
        joint["ragdoll_bone"] = name
        bpy.ops.object.select_all(action="DESELECT")
        joint.select_set(True)
        context.view_layer.objects.active = joint
        bpy.ops.rigidbody.constraint_add()
        constraint = joint.rigid_body_constraint
        constraint.type = "GENERIC"
        constraint.object1 = bodies[parent_name]
        constraint.object2 = bodies[name]
        constraint.disable_collisions = True
        constraint.use_breaking = False
        constraint.use_override_solver_iterations = False
        for axis in "xyz":
            setattr(constraint, f"use_limit_lin_{axis}", True)
            setattr(constraint, f"limit_lin_{axis}_lower", 0.0)
            setattr(constraint, f"limit_lin_{axis}_upper", 0.0)
            setattr(constraint, f"use_limit_ang_{axis}", True)
            angle = radians(12 if name.startswith("Spine") else 45)
            if name in ("Neck", "Head") or name.endswith(("Shoulder", "Foot", "Hand")):
                angle = radians(20)
            if name == "Neck" or name.endswith("Shoulder"):
                # Short connector segments move with the torso. Articulation is
                # provided by the neighboring head/upper-arm joints.
                angle = 0.0
            if name.endswith(("ForeArm", "Leg")):
                angle = radians(70 if axis == "x" else 8)
            setattr(constraint, f"limit_ang_{axis}_lower", -angle)
            setattr(constraint, f"limit_ang_{axis}_upper", angle)
        for label, body in (("a", constraint.object1), ("b", constraint.object2)):
            joint[f"anchor_{label}"] = list(body.matrix_world.inverted() @ joint.matrix_world.translation)
        joints.append(joint)
    return joints
