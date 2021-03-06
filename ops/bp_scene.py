import bpy
from bpy.types import Header, Menu, Operator, UIList, PropertyGroup
from bpy.props import (StringProperty,
                       BoolProperty,
                       IntProperty,
                       FloatProperty,
                       FloatVectorProperty,
                       BoolVectorProperty,
                       PointerProperty,
                       EnumProperty,
                       CollectionProperty)
import os


class BPSCENE_OT_delete_scene(Operator):
    bl_idname = "bp_scene.delete_scene"
    bl_label = "Delete Scene"
    bl_description = "This will delete the scene"
    bl_options = {'UNDO'}
    
    scene_name: StringProperty(name="Scene Name")
    
    @classmethod
    def poll(cls, context):
        if len(bpy.data.scenes) > 1:
            return True
        else:
            return False

    def execute(self, context):
        if self.scene_name in bpy.data.scenes:
            scene = bpy.data.scenes[self.scene_name]
            bpy.data.scenes.remove(scene,do_unlink=True)
        return {'FINISHED'}

    def invoke(self,context,event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=400)

    def draw(self, context):
        layout = self.layout
        layout.label("Are you sure you want to delete the scene?")  
        layout.label("Scene Name: " + self.scene_name)  

class BPSCENE_OT_add_audio(Operator):
    bl_idname = "bp_scene.add_audio"
    bl_label = "Add Audio"
    bl_description = "This will add an audio file to the scene"
    bl_options = {'UNDO'}

    filepath: bpy.props.StringProperty(subtype="FILE_PATH")

    def invoke(self, context, event):
        wm = context.window_manager
        wm.fileselect_add(self)
        return {'RUNNING_MODAL'}

    def execute(self, context):
        file_path, file_name = os.path.split(self.filepath)
        filename , ext = os.path.splitext(file_name)
        context.scene.sequence_editor.sequences.new_sound(filename,self.filepath,1,1)
        return {'FINISHED'}

classes = (
    BPSCENE_OT_delete_scene,
    BPSCENE_OT_add_audio,
)

register, unregister = bpy.utils.register_classes_factory(classes)

if __name__ == "__main__":
    register()        