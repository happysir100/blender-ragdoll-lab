"""Explicit first-rig support, region assignment, and collider fitting."""

import math
from mathutils import Vector

BODY_BONES = (
    "Hips", "Spine", "Spine1", "Spine2", "Neck", "Head",
    "LeftShoulder", "LeftArm", "LeftForeArm", "LeftHand",
    "RightShoulder", "RightArm", "RightForeArm", "RightHand",
    "LeftUpLeg", "LeftLeg", "LeftFoot",
    "RightUpLeg", "RightLeg", "RightFoot",
)


def validate(rig, context):
    if not rig or rig.type != "ARMATURE" or context.mode != "OBJECT":
        raise ValueError("Select the supported armature in Object Mode.")
    if rig.library or rig.data.library:
        raise ValueError("The armature must be local and editable.")
    missing = set(BODY_BONES) - set(rig.data.bones.keys())
    if missing:
        raise ValueError("Unsupported rig: missing " + ", ".join(sorted(missing)))
    if any(b.constraints for b in rig.pose.bones):
        raise ValueError("This version supports a rig without existing bone constraints.")
    scale = rig.matrix_world.to_scale()
    if min(scale) <= 0 or max(scale) - min(scale) > 1e-5:
        raise ValueError("The rig must have positive, uniform world scale.")
    meshes = [o for o in context.scene.objects if o.type == "MESH"
              and any(m.type == "ARMATURE" and m.object == rig for m in o.modifiers)]
    if len(meshes) != 1:
        raise ValueError("This version requires one mesh deformed by the selected rig.")
    if not rig.animation_data or not rig.animation_data.action:
        raise ValueError("Assign an animation action before generating this first-rig setup.")
    return meshes[0]


def owner_for(bone):
    while bone and bone.name not in BODY_BONES:
        bone = bone.parent
    if bone is None:
        raise ValueError("Every bone must descend from a supported physical segment.")
    return bone.name


def build_mapping(rig):
    return {bone.name: owner_for(bone) for bone in rig.data.bones}


def fit_regions(rig, mesh, depsgraph):
    """Fit oriented boxes to dominant skin-weight regions in evaluated world space."""
    mapping = build_mapping(rig)
    evaluated_rig = rig.evaluated_get(depsgraph)
    evaluated_mesh = mesh.evaluated_get(depsgraph)
    if len(evaluated_mesh.data.vertices) != len(mesh.data.vertices):
        raise ValueError("Topology-changing mesh modifiers are not supported yet.")
    matrices = {name: (evaluated_rig.matrix_world @ evaluated_rig.pose.bones[name].matrix)
                for name in BODY_BONES}
    # Strip inherited object scale from body transforms; mesh dimensions are world units.
    frames = {name: matrix.to_quaternion().to_matrix().to_4x4()
              for name, matrix in matrices.items()}
    for name, frame in frames.items():
        frame.translation = matrices[name].translation
    regions = {name: [] for name in BODY_BONES}
    for vertex in mesh.data.vertices:
        weights = {}
        for group in vertex.groups:
            bone_name = mesh.vertex_groups[group.group].name
            if bone_name in mapping:
                owner = mapping[bone_name]
                weights[owner] = weights.get(owner, 0.0) + group.weight
        if not weights:
            continue
        owner = max(weights, key=weights.get)
        position = evaluated_mesh.matrix_world @ evaluated_mesh.data.vertices[vertex.index].co
        regions[owner].append(frames[owner].inverted() @ position)
    result = {}
    height = max((evaluated_mesh.matrix_world @ v.co).z for v in evaluated_mesh.data.vertices)
    height -= min((evaluated_mesh.matrix_world @ v.co).z for v in evaluated_mesh.data.vertices)
    if not math.isfinite(height) or height <= 0:
        raise ValueError("The mesh must have finite, nonzero dimensions.")
    for name in BODY_BONES:
        points = regions[name]
        if len(points) < 4:
            bone = evaluated_rig.pose.bones[name]
            end = frames[name].inverted() @ (evaluated_rig.matrix_world @ bone.tail)
            half_width = height * 0.018
            points = [Vector((x, y, z)) for x in (-half_width, half_width)
                      for y in (0, max(end.y, height * 0.025))
                      for z in (-half_width, half_width)]
        low = Vector([min(p[i] for p in points) for i in range(3)])
        high = Vector([max(p[i] for p in points) for i in range(3)])
        center = (low + high) * 0.5
        dimensions = Vector([max((high[i] - low[i]) * 0.85, height * 0.015)
                             for i in range(3)])
        transform = frames[name].copy()
        transform.translation = frames[name] @ center
        parent = rig.data.bones[name].parent
        result[name] = {
            "matrix": transform,
            "dimensions": dimensions,
            "parent": owner_for(parent) if parent else None,
            "joint_matrix": frames[name],
            "region_vertices": len(regions[name]),
            "hull_points": [(p - center) * 0.85 for p in points]
                if all(high[i] - low[i] >= height * 0.015 for i in range(3)) else None,
        }
    return mapping, result
