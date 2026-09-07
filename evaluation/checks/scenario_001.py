"""Run the accepted scenario in Blender; never manufacture passing evidence.

Example from repository root:
blender --background --factory-startup --disable-autoexec --python evaluation/checks/scenario_001.py
"""

import hashlib
import json
import math
import sys
import traceback
from pathlib import Path

import bpy
from mathutils import Vector

ROOT = Path(__file__).resolve().parents[2]
INPUT = ROOT / "work/scenarios/scenario-001/start.blend"
OUTPUT = ROOT / "work/runs/task-0001/run-001"
DIAGNOSTIC = "--diagnostic-high-accuracy" in sys.argv
if DIAGNOSTIC:
    OUTPUT = OUTPUT / "diagnostic-high-accuracy"
OUTPUT.mkdir(parents=True, exist_ok=True)
sys.path.insert(0, str(ROOT / "addon"))
import ragdoll_lab
from ragdoll_lab import binding, mapping


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True).encode()).hexdigest()


def action_content(action):
    return [
        [curve.data_path, curve.array_index,
         [[list(point.co), point.interpolation, list(point.handle_left), list(point.handle_right)]
          for point in curve.keyframe_points]]
        for layer in action.layers for strip in layer.strips
        for bag in strip.channelbags for curve in bag.fcurves
    ]


def original_content(rig, mesh):
    return {
        "actions": {a.name: digest(action_content(a)) for a in bpy.data.actions},
        "mesh": digest([[list(v.co), [[g.group, g.weight] for g in v.groups]]
                        for v in mesh.data.vertices]),
        "bones": digest([[b.name, b.parent.name if b.parent else None,
                          list(b.head_local), list(b.tail_local), b.use_connect]
                         for b in rig.data.bones]),
    }


def pose_world(rig):
    evaluated = rig.evaluated_get(bpy.context.evaluated_depsgraph_get())
    return {b.name: (evaluated.matrix_world @ b.matrix).copy() for b in evaluated.pose.bones}


def transform_error(a, b):
    # q and -q describe the same rotation. Use the shortest angular distance so
    # a harmless quaternion sign change is not reported as a full revolution.
    angle = a.to_quaternion().rotation_difference(b.to_quaternion()).angle
    return ((a.translation - b.translation).length, min(angle, abs(2 * math.pi - angle)))


def world_matrix(obj):
    return obj.evaluated_get(bpy.context.evaluated_depsgraph_get()).matrix_world.copy()


def lifecycle_checks(rig, mesh):
    """Inject a late failure to exercise real cleanup, including output actions."""
    kinds = ("objects", "meshes", "armatures", "actions", "collections")
    snapshot = {kind: set(getattr(bpy.data,kind).keys()) for kind in kinds}
    original = original_content(rig,mesh)
    original_action = rig.animation_data.action
    original_bind = binding.bind
    def fail_after_binding(*args, **kwargs):
        original_bind(*args, **kwargs)
        raise RuntimeError("Injected validation failure after binding")
    binding.bind = fail_after_binding
    try:
        try:
            bpy.ops.ragdoll.generate()
        except RuntimeError:
            # Blender raises for an operator reporting ERROR, even on CANCELLED.
            pass
    finally:
        binding.bind = original_bind
    bpy.context.view_layer.update()
    return (snapshot == {kind:set(getattr(bpy.data,kind).keys()) for kind in kinds}
            and original_content(rig,mesh)==original
            and rig.animation_data.action==original_action
            and not rig.animation_data.drivers
            and binding.BLEND_PROPERTY not in rig and binding.SETUP_PROPERTY not in rig)


def run():
    bpy.ops.wm.open_mainfile(filepath=str(INPUT))
    rig = bpy.data.objects["Human Armature"]
    mesh = bpy.data.objects["Human_Mesh"]
    scene = bpy.context.scene
    if DIAGNOSTIC:
        # Separate experiment only. Never report altered fixture settings as an
        # accepted-scenario pass or save over the frozen scenario input.
        scene.rigidbody_world.substeps_per_frame = 30
        scene.rigidbody_world.solver_iterations = 100
    before = original_content(rig, mesh)
    world_settings = (scene.rigidbody_world.substeps_per_frame,
                      scene.rigidbody_world.solver_iterations)
    unrelated = {o.name: digest([list(row) for row in o.matrix_world])
                 for o in scene.objects if o not in (rig, mesh)}
    baseline = {}
    for frame in range(1, 25):
        scene.frame_set(frame)
        baseline[frame] = pose_world(rig)
    scene.frame_set(1)
    ragdoll_lab.register()
    rollback_clean = lifecycle_checks(rig,mesh)
    if not rollback_clean:
        raise RuntimeError("Late-failure cleanup did not restore the source scene.")
    invalid_before = len(bpy.data.objects)
    bpy.context.view_layer.objects.active = bpy.data.objects["ScenarioFloor"]
    invalid = bpy.ops.ragdoll.generate()
    invalid_clean = invalid == {"CANCELLED"} and len(bpy.data.objects) == invalid_before
    bpy.context.view_layer.objects.active = rig
    generated = bpy.ops.ragdoll.generate()
    if generated != {"FINISHED"}:
        raise RuntimeError(f"Generator did not finish: {generated}")
    after = original_content(rig, mesh)
    generation_preserved = (before["mesh"] == after["mesh"] and before["bones"] == after["bones"]
                            and all(after["actions"].get(name) == value
                                    for name,value in before["actions"].items()))
    duplicate_before = len(bpy.data.objects)
    duplicate = bpy.ops.ragdoll.generate()
    duplicate_clean = duplicate == {"CANCELLED"} and len(bpy.data.objects) == duplicate_before
    collection = bpy.data.collections[rig[binding.SETUP_PROPERTY]]
    bodies = {o["ragdoll_bone"]: o for o in collection.objects if o.get("ragdoll_role") == "body"}
    joints = [o for o in collection.objects if o.get("ragdoll_role") == "joint"]
    targets = {o["ragdoll_bone"]: o for o in collection.objects if o.get("ragdoll_role") == "pose_target"}
    inventory = {
        "bodies": [{"bone":name, "dimensions":list(body.dimensions), "mass":body.rigid_body.mass}
                   for name, body in bodies.items()],
        "joints": [{"bone":o["ragdoll_bone"], "a":o.rigid_body_constraint.object1.name,
                    "b":o.rigid_body_constraint.object2.name} for o in joints],
        "bone_mapping": mapping.build_mapping(rig),
    }
    # The run's blend keys are user-authored test input, not generator behavior.
    # The generator supplies an editable copy; key it without touching Idle.
    for frame, value in ((1, 0.0), (24, 0.0), (48, 1.0), (240, 1.0)):
        rig[binding.BLEND_PROPERTY] = value
        rig.keyframe_insert(data_path=f'["{binding.BLEND_PROPERTY}"]', frame=frame)
    for layer in rig.animation_data.action.layers:
        for strip in layer.strips:
            for bag in strip.channelbags:
                for curve in bag.fcurves:
                    if curve.data_path == f'["{binding.BLEND_PROPERTY}"]':
                        for point in curve.keyframe_points:
                            point.interpolation = "LINEAR"
    # Adding the first control keys changes animation dependencies. Explicitly tag
    # the affected datablocks, just as the interactive animation editor does.
    rig.update_tag(refresh={"OBJECT", "TIME"})
    for body in bodies.values():
        body.update_tag(refresh={"OBJECT", "TIME"})
    bpy.context.view_layer.update()
    scene.frame_set(1)
    bpy.ops.wm.save_as_mainfile(filepath=str(OUTPUT / "generated.blend"), compress=True)
    rows = []
    previous = None
    worst = {"animation_position_m":0.0, "animation_rotation_rad":0.0,
             "physics_position_m":0.0, "physics_rotation_rad":0.0,
             "joint_separation_m":0.0, "floor_penetration_m":0.0,
             "settling_linear_m_s":0.0, "settling_angular_rad_s":0.0}
    finite = True
    for frame in range(1, 241):
        scene.frame_set(frame)
        bpy.context.view_layer.update()
        poses = pose_world(rig)
        matrices = {name:world_matrix(body) for name,body in bodies.items()}
        finite = finite and all(math.isfinite(v) for mat in matrices.values() for row in mat for v in row)
        finite = finite and all(math.isfinite(v) for mat in poses.values() for row in mat for v in row)
        linear = {}; angular = {}
        if previous:
            for name, matrix in matrices.items():
                pos, angle = transform_error(previous[name], matrix)
                linear[name] = pos * 24
                angular[name] = angle * 24
        separations = {j["ragdoll_bone"]: (world_matrix(j.rigid_body_constraint.object1) @ Vector(j["anchor_a"])
                          - world_matrix(j.rigid_body_constraint.object2) @ Vector(j["anchor_b"])).length
                         for j in joints}
        separation = max(separations.values())
        # Measure the actual convex collision mesh, not its enclosing box corners.
        penetration = max(0.0, -min((matrices[name] @ vertex.co).z
                                    for name,body in bodies.items() for vertex in body.data.vertices))
        if frame <= 24:
            for name,matrix in poses.items():
                pos, angle = transform_error(baseline[frame][name], matrix)
                worst["animation_position_m"] = max(worst["animation_position_m"],pos)
                worst["animation_rotation_rad"] = max(worst["animation_rotation_rad"],angle)
        if frame >= 48:
            for name,matrix in poses.items():
                pos, angle = transform_error(world_matrix(targets[name]), matrix)
                worst["physics_position_m"] = max(worst["physics_position_m"],pos)
                worst["physics_rotation_rad"] = max(worst["physics_rotation_rad"],angle)
        # Joint anchors are physical simulation assertions after release.
        if frame >= 25:
            worst["joint_separation_m"] = max(worst["joint_separation_m"], separation)
            worst["floor_penetration_m"] = max(worst["floor_penetration_m"],penetration)
        if frame >= 193:
            worst["settling_linear_m_s"] = max(worst["settling_linear_m_s"],max(linear.values(),default=0))
            worst["settling_angular_rad_s"] = max(worst["settling_angular_rad_s"],max(angular.values(),default=0))
        rows.append({"frame":frame,"blend":rig[binding.BLEND_PROPERTY],
                     "max_joint_separation_m":separation,"floor_penetration_m":penetration,
                     "max_linear_speed_m_s":max(linear.values(),default=0),
                     "max_angular_speed_rad_s":max(angular.values(),default=0),
                     "body_positions":{name:list(mat.translation) for name,mat in matrices.items()},
                     "joint_separations_m":separations,"linear_speeds_m_s":linear,"angular_speeds_rad_s":angular,
                     "kinematic_bodies":sum(body.rigid_body.kinematic for body in bodies.values())})
        previous = matrices
    (OUTPUT / "frames.json").write_text(json.dumps(rows,indent=2)+"\n")
    (OUTPUT / "inventory.json").write_text(json.dumps(inventory,indent=2)+"\n")
    current_actions = {a.name:digest(action_content(a)) for a in bpy.data.actions}
    preserved_original_actions = all(current_actions.get(name)==value for name,value in before["actions"].items())
    unchanged_unrelated = all(digest([list(row) for row in bpy.data.objects[name].matrix_world])==value
                              for name,value in unrelated.items())
    checks = {
        "generation": generated == {"FINISHED"},
        "late_failure_rollback": rollback_clean,
        "invalid_selection_unchanged": invalid_clean,
        "duplicate_generation_unchanged": duplicate_clean,
        "generation_preserves_source_content": generation_preserved,
        "original_actions_preserved_after_control_keys": preserved_original_actions,
        "unrelated_objects_unchanged": unchanged_unrelated,
        "world_settings_preserved": world_settings == (scene.rigidbody_world.substeps_per_frame,scene.rigidbody_world.solver_iterations),
        "coverage": len(bodies)==20 and len(joints)==19 and len(targets)==41,
        "finite": finite,
        "animation_endpoint": worst["animation_position_m"]<=0.001 and worst["animation_rotation_rad"]<=math.radians(0.1),
        "physics_endpoint": worst["physics_position_m"]<=0.001 and worst["physics_rotation_rad"]<=math.radians(0.1),
        "joint_separation": worst["joint_separation_m"]<=0.01,
        "floor_penetration": worst["floor_penetration_m"]<=0.01,
        "settling": worst["settling_linear_m_s"]<=0.05 and worst["settling_angular_rad_s"]<=0.1,
        "blend_schedule": rows[23]["blend"]==0 and abs(rows[35]["blend"]-0.5)<1e-6 and rows[47]["blend"]==1,
        "release_schedule": all(r["kinematic_bodies"]==20 for r in rows[:24]) and all(r["kinematic_bodies"]==0 for r in rows[24:]),
    }
    result = {"status":"automated_checks_passed" if all(checks.values()) else "failed",
              "checks":checks,"worst":worst,"sampled_frames":len(rows),
              "human_motion_review":"pending","continuous_transition_review":"pending",
              "blender_version":bpy.app.version_string}
    result["diagnostic_only"] = DIAGNOSTIC
    result["input_sha256"] = hashlib.sha256(INPUT.read_bytes()).hexdigest()
    result["code_sha256"] = {str(p.relative_to(ROOT)).replace("\\", "/"):hashlib.sha256(p.read_bytes()).hexdigest()
                              for p in sorted((ROOT/"addon/ragdoll_lab").glob("*.py"))}
    result["runner_sha256"] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    if DIAGNOSTIC:
        result["status"] = "diagnostic_only"
    (OUTPUT / "result.json").write_text(json.dumps(result,indent=2)+"\n")
    print("SCENARIO_RESULT="+json.dumps(result))
    if "--record" in sys.argv:
        scene.render.image_settings.media_type = "VIDEO"
        scene.render.image_settings.file_format = "FFMPEG"
        scene.render.ffmpeg.format = "MPEG4"
        scene.render.ffmpeg.codec = "H264"
        scene.render.ffmpeg.constant_rate_factor = "MEDIUM"
        scene.render.filepath = str(OUTPUT / "playback.mp4")
        scene.frame_set(1)
        bpy.ops.render.render(animation=True)
        scene.render.image_settings.media_type = "IMAGE"
        scene.render.image_settings.file_format = "PNG"
        for frame in (1,24,36,48,96,193,240):
            scene.frame_set(frame)
            scene.render.filepath = str(OUTPUT / f"frame-{frame:03d}.png")
            bpy.ops.render.render(write_still=True)
    ragdoll_lab.unregister()
    return result


if __name__ == "__main__":
    (OUTPUT / "result.json").unlink(missing_ok=True)
    try:
        result = run()
        if not DIAGNOSTIC and result["status"] != "automated_checks_passed":
            raise AssertionError("Accepted scenario failed; see result.json for individual checks.")
    except Exception:
        error = traceback.format_exc()
        if not (OUTPUT / "result.json").exists():
            (OUTPUT / "result.json").write_text(json.dumps({"status":"incomplete","error":error},indent=2)+"\n")
        print(error)
        raise
