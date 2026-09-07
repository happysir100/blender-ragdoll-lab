"""Independent source animation, physical targets, and persistent Blender drivers."""

import bpy

BLEND_PROPERTY = "ragdoll_blend"
SETUP_PROPERTY = "ragdoll_setup"
CONSTRAINT_PREFIX = "Ragdoll Lab: "


def blend_driver(owner, path, rig, expression="blend"):
    curve = owner.driver_add(path)
    driver = curve.driver
    driver.type = "SCRIPTED"
    variable = driver.variables.new()
    variable.name = "blend"
    variable.type = "SINGLE_PROP"
    variable.targets[0].id = rig
    variable.targets[0].data_path = f'["{BLEND_PROPERTY}"]'
    driver.expression = expression
    return curve


def make_reference(rig, collection):
    reference = rig.copy()
    reference.data = rig.data.copy()
    reference.name = "RD_AnimationReference"
    collection.objects.link(reference)
    reference["ragdoll_role"] = "animation_reference"
    reference.hide_render = True
    reference.hide_set(True)
    return reference


def target_at(collection, name, matrix, parent=None):
    target = bpy.data.objects.new(name, None)
    collection.objects.link(target)
    target.empty_display_size = 0.02
    target.hide_render = True
    target.parent = parent
    target.matrix_world = matrix
    return target


def bind(context, rig, reference, collection, mapping, regions, bodies):
    rig[BLEND_PROPERTY] = 0.0
    rig.id_properties_ui(BLEND_PROPERTY).update(
        min=0.0, max=1.0, soft_min=0.0, soft_max=1.0,
        description="Blend source animation (0) into full-body ragdoll physics (1). Keyframe to transition; recompute the physics cache after edits.",
    )
    # Give the output rig an editable action copy; the reference retains the
    # untouched source action. Declare an empty control channel before creating
    # dependent drivers so Blender knows that the property can be animated.
    rig.animation_data.action = rig.animation_data.action.copy()
    rig.animation_data.action.name = "RD_" + reference.animation_data.action.name
    rig.animation_data.action_slot = rig.animation_data.action.slots[0]
    action = rig.animation_data.action
    bag = action.layers[0].strips[0].channelbag(rig.animation_data.action_slot)
    bag.fcurves.new(data_path=f'["{BLEND_PROPERTY}"]')
    context.view_layer.update()
    for name, body in bodies.items():
        # Bone parenting uses bone-tail coordinates. Derive matrix_parent_inverse
        # through the evaluated parent relation to preserve the exact fitted offset.
        target = target_at(collection, f"RD_Animated_{name}", body.matrix_world)
        target.parent = reference
        target.parent_type = "BONE"
        target.parent_bone = name
        context.view_layer.update()
        target.matrix_world = regions[name]["matrix"]
        target["ragdoll_role"] = "animation_target"
        target["ragdoll_bone"] = name
        constraint = body.constraints.new("COPY_TRANSFORMS")
        constraint.name = CONSTRAINT_PREFIX + "Animated body"
        constraint.target = target
        blend_driver(body.rigid_body, "kinematic", rig, "blend <= 0.0")
    context.view_layer.update()
    evaluated = reference.evaluated_get(context.evaluated_depsgraph_get())
    for bone in rig.pose.bones:
        matrix = evaluated.matrix_world @ evaluated.pose.bones[bone.name].matrix
        body = bodies[mapping[bone.name]]
        target = target_at(collection, f"RD_Pose_{bone.name}", matrix, parent=body)
        target["ragdoll_role"] = "pose_target"
        target["ragdoll_bone"] = bone.name
        target["ragdoll_body_bone"] = mapping[bone.name]
        constraint = bone.constraints.new("COPY_TRANSFORMS")
        constraint.name = CONSTRAINT_PREFIX + "Physics pose"
        constraint.target = target
        constraint.owner_space = "WORLD"
        constraint.target_space = "WORLD"
        blend_driver(constraint, "influence", rig)
    rig[SETUP_PROPERTY] = collection.name
    rig.id_properties_ui(SETUP_PROPERTY).update(description="Collection owning this rig's generated ragdoll setup.")
