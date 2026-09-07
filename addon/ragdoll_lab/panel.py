"""The user-facing generation and blend controls."""

import bpy
from .binding import BLEND_PROPERTY, SETUP_PROPERTY


class RAGDOLL_PT_panel(bpy.types.Panel):
    bl_label = "Ragdoll Lab"
    bl_idname = "RAGDOLL_PT_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Ragdoll Lab"

    def draw(self, context):
        layout = self.layout
        rig = context.active_object
        layout.operator("ragdoll.generate", text="Generate Ragdoll", icon="PHYSICS")
        if rig and rig.type == "ARMATURE" and SETUP_PROPERTY in rig:
            layout.prop(rig, f'["{BLEND_PROPERTY}"]', text="Ragdoll Blend", slider=True)
            layout.label(text="0: Animation   1: Physics")
        else:
            layout.label(text="Select the supported character rig.")
        row = layout.row()
        row.enabled = False
        row.label(text="Bake simulation", icon="ACTION")
        layout.label(text="Baking is not implemented yet.", icon="INFO")
