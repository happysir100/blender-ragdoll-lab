"""Generation operator: validate, author, bind, and roll back only owned data."""

import bpy
from . import binding, mapping, physics


class RAGDOLL_OT_generate(bpy.types.Operator):
    bl_idname = "ragdoll.generate"
    bl_label = "Generate Ragdoll"
    bl_description = "Create editable full-body ragdoll physics for the supported selected rig; existing animation is preserved"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        rig = context.active_object
        try:
            if rig and (binding.SETUP_PROPERTY in rig or binding.BLEND_PROPERTY in rig):
                raise ValueError("This rig already has a ragdoll setup or blend property. Undo generation before trying again.")
            mesh = mapping.validate(rig, context)
            if context.scene.frame_current != context.scene.frame_start:
                raise ValueError("Return to the scene's first frame before generating.")
            bone_map, regions = mapping.fit_regions(rig, mesh, context.evaluated_depsgraph_get())
        except ValueError as error:
            self.report({"WARNING"}, str(error))
            return {"CANCELLED"}
        collection_names_before = set(bpy.data.collections.keys())
        collection = bpy.data.collections.new(f"Ragdoll_{rig.name}")
        context.scene.collection.children.link(collection)
        collection["ragdoll_owner"] = rig.name
        existing_world = context.scene.rigidbody_world
        original_action = rig.animation_data.action
        original_slot = rig.animation_data.action_slot
        data_before = {"meshes": set(bpy.data.meshes), "armatures": set(bpy.data.armatures), "actions": set(bpy.data.actions)}
        try:
            reference = binding.make_reference(rig, collection)
            bodies = physics.create_bodies(context, collection, regions)
            context.view_layer.update()
            physics.create_joints(context, collection, regions, bodies)
            binding.bind(context, rig, reference, collection, bone_map, regions, bodies)
        except Exception as error:
            rig.animation_data.action = original_action
            rig.animation_data.action_slot = original_slot
            for bone in rig.pose.bones:
                for constraint in list(bone.constraints):
                    if constraint.name.startswith(binding.CONSTRAINT_PREFIX):
                        # Remove the driver before the constraint to avoid invalid paths.
                        try:
                            constraint.driver_remove("influence")
                        except (TypeError, RuntimeError):
                            pass
                        bone.constraints.remove(constraint)
            for key in (binding.BLEND_PROPERTY, binding.SETUP_PROPERTY):
                if key in rig:
                    del rig[key]
            for obj in list(collection.objects):
                bpy.data.objects.remove(obj, do_unlink=True)
            bpy.data.collections.remove(collection)
            for kind, previous in data_before.items():
                data = getattr(bpy.data, kind)
                for item in set(data) - previous:
                    if item.users == 0:
                        data.remove(item)
            if existing_world is None and context.scene.rigidbody_world:
                bpy.ops.rigidbody.world_remove()
            for candidate in list(bpy.data.collections):
                if candidate.name not in collection_names_before and not candidate.objects:
                    bpy.data.collections.remove(candidate)
            self.report({"ERROR"}, f"Generation rolled back: {error}")
            return {"CANCELLED"}
        finally:
            bpy.ops.object.select_all(action="DESELECT")
            rig.select_set(True)
            context.view_layer.objects.active = rig
        self.report({"INFO"}, "Created 20 bodies and 19 joints. Key Ragdoll Blend to transition into physics.")
        return {"FINISHED"}
