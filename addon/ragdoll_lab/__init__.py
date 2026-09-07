"""Blender authoring tools for the first supported humanoid ragdoll."""

bl_info = {
    "name": "Ragdoll Lab",
    "author": "Blender Ragdoll Lab contributors",
    "version": (0, 1, 0),
    "blender": (5, 1, 0),
    "location": "View3D > Sidebar > Ragdoll Lab",
    "description": "Generate editable whole-body physics with a keyable pose blend",
    "category": "Animation",
}

import bpy
from .generate import RAGDOLL_OT_generate
from .panel import RAGDOLL_PT_panel

CLASSES = (RAGDOLL_OT_generate, RAGDOLL_PT_panel)


def register():
    for cls in CLASSES:
        bpy.utils.register_class(cls)


def unregister():
    # Authored setups use Blender primitives and remain usable without the UI.
    for cls in reversed(CLASSES):
        bpy.utils.unregister_class(cls)
