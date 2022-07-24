# (GNU GPL) <2022> <Taiseibutsu>" Developed for Blender 3.2, Tested on 3.1
# This program is free software: you can redistribute it and/or modify it, WITHOUT ANY WARRANTY. 

bl_info = {
    "name": "KTS_keyframe_by_type_selector(TB)",
    "author": "Taiseibutsu",
    "version": (0, 0, 1),
    "blender": (2, 80, 0),
    "location": "Dopesheet, Timeline",
    "description": "Tool to select keyframes bt type",
    "warning": "",
    "wiki_url": "",
    "category": "TB",
}


import bpy, addon_utils
from bpy.types import AddonPreferences, Panel

####
class TB_KTS_Properties(bpy.types.PropertyGroup):
    keyframe_type : bpy.props.EnumProperty(
        name = "Enumerator/Dropdown",
        description = "Object that will rename",
        items= [('KEYFRAME', "Normal", "Select Normal type keyframes",'KEYTYPE_KEYFRAME_VEC',0),
                ('BREAKDOWN', "Breakdown", "Select Brackdown type keyframes",'KEYTYPE_BREAKDOWN_VEC', 1),
                ('MOVING_HOLD',"Moving hold", "Select Moving Hold type keyframes",'KEYTYPE_MOVING_HOLD_VEC', 2),
                ('EXTREME',"Extreme", "Select Extreme type keyframes",'KEYTYPE_EXTREME_VEC', 3),
                ('JITTER',"Jitter", "Select Jitter type keyframes",'KEYTYPE_JITTER_VEC', 4)
        ]
    )
    keyframe_range : bpy.props.EnumProperty(
        name = "Enumerator/Dropdown",
        description = "Object that will rename",
        items= [('SELECTION', "Selection", "Select keyframes by type from active selection",  'RESTRICT_SELECT_OFF', 0),
                ('COLLECTION',"Collection", "Select keyframes by type from active colection",  'OUTLINER_COLLECTION', 1),
                ('SCENE',"Scene", "Select keyframes by type from scene",'SCENE_DATA', 2),
                ('ALL',"All", "Select all keyframes by type",'BLENDER', 3)
        ]
    )
    keyframe_type_KEYFRAME : bpy.props.BoolProperty(default = True, description = "Select Keyframe default Type")
    keyframe_type_BREAKDOWN : bpy.props.BoolProperty(default = True, description = "Select Keyframe breakdown Type")
    keyframe_type_MOVING_HOLD : bpy.props.BoolProperty(default = True, description = "Select Keyframe moving hold Type")
    keyframe_type_EXTREME : bpy.props.BoolProperty(default = True, description = "Select Keyframe extreme Type")
    keyframe_type_JITTER : bpy.props.BoolProperty(default = True, description = "Select Keyframe jitter Type")

    keyframe_type_icon = ['KEYTYPE_KEYFRAME_VEC','KEYTYPE_BREAKDOWN_VEC','KEYTYPE_MOVING_HOLD_VEC','KEYTYPE_EXTREME_VEC','KEYTYPE_JITTER_VEC']
    keyframe_type_text = ["Normal","Breakdown","Moving_hold","Extreme","Jitter"]
    
    keyframe_context_icon = ['RESTRICT_SELECT_OFF','OUTLINER_COLLECTION','SCENE_DATA','BLENDER']
    keyframe_context_text = ["Selection","Collection","Scene","All"]
    
    keyframe_type_context : bpy.props.BoolProperty(default = True, description = "Way to handle selection")
    
    select_from_scene : bpy.props.PointerProperty(type=bpy.types.Scene)
    select_from_active_scene : bpy.props.BoolProperty(default = True, description = "Select Keyframes from Active Scene")

    select_from_collection : bpy.props.PointerProperty(type=bpy.types.Collection)
    select_from_active_collection : bpy.props.BoolProperty(default = False, description = "Select Keyframes from Active Collection")
        
    select_only_active : bpy.props.BoolProperty(default = False, description = "Select Keyframes from Active Object Only")
    select_from_dopesheet_context : bpy.props.BoolProperty(default = True, description = "Select Keyframes using context from dopesheet")

    affect_current_scene_keyframes : bpy.props.BoolProperty(default = True, description = "Select Keyframes from scene")
def tb_kts_get_range():
    tbtool = bpy.context.scene.tb_kts_prop
    if tbtool.keyframe_range == 'SELECTION':
        temp_keyframe_range = bpy.context.selected_objects
        return(temp_keyframe_range)
    elif tbtool.keyframe_range == 'COLLECTION':
        if tbtool.select_from_active_collection:
            if bpy.context.collection:
                if bpy.context.collection.objects:
                    temp_keyframe_range = bpy.context.collection.objects
                else:
                    temp_keyframe_range = 'NONE'
            else:
                temp_keyframe_range = 'NONE'
        else:
            temp_keyframe_range = tbtool.select_from_collection.objects
        return(temp_keyframe_range)
    elif tbtool.keyframe_range == 'SCENE':
        temp_keyframe_range = bpy.context.scene.objects
        return(temp_keyframe_range)
    elif tbtool.keyframe_range == 'ALL':                
        temp_keyframe_range = bpy.data.objects
        return(temp_keyframe_range)
    
def tb_kts_set_selection(ob):
    tbtool = bpy.context.scene.tb_kts_prop
    if ob.animation_data:
        if ob.animation_data.action:
            fcurves = ob.animation_data.action.fcurves
            select_keyframes(fcurves)


                
                
def tb_kts_select_keyframes_by_type(context):
    tbtool = bpy.context.scene.tb_kts_prop

    if context.space_data.ui_mode in ['DOPESHEET','ACTION']:
        act_keyframe_range = tb_kts_get_range()
        if act_keyframe_range != 'NONE':
            for ob in act_keyframe_range:
                if tbtool.select_from_dopesheet_context:
                    if bpy.context.space_data.dopesheet.show_only_selected == True:
                        if ob.select_get() == True:
                            if bpy.context.space_data.dopesheet.show_hidden == True:
                                if ob.hide_viewport != False:
                                    tb_kts_set_selection(ob)
                            else:
                                tb_kts_set_selection(ob)
                            
                    else:
                        tb_kts_set_selection(ob)
    if tbtool.affect_current_scene_keyframes:
        scn = bpy.context.scene
        if scn.animation_data:
            if scn.animation_data.action:
                fcurves = scn.animation_data.action.fcurves
                select_keyframes(fcurves)                 

    if context.space_data.ui_mode == 'SHAPEKEY':
        sh =  bpy.context.active_object.data.shape_keys
        if sh:
            if sh.animation_data:
                if sh.animation_data.action:
                    fcurves = sh.fcurves
                    select_keyframes(fcurves)

    if context.space_data.ui_mode == 'GPENCIL':
        for gp in bpy.data.grease_pencils:
            if gp.animation_data:
                if gp.animation_data.action:
                    fcurves = gp.animation_data.action.fcurves
                    select_keyframes(fcurves)
    #PLANED  
     #if context.space_data.ui_mode == 'MASK':        
def select_keyframes(fcurves):
    tbtool = bpy.context.scene.tb_kts_prop
    for f in fcurves:
        for k in f.keyframe_points:    
            if tbtool.keyframe_type_context:
                if tbtool.keyframe_type_KEYFRAME:
                    if k.type == 'KEYFRAME':
                        k.select_control_point = True    
                if tbtool.keyframe_type_BREAKDOWN:
                    if k.type == 'BREAKDOWN':                    
                        k.select_control_point = True        
                if tbtool.keyframe_type_MOVING_HOLD:
                    if k.type == 'MOVING_HOLD':                    
                        k.select_control_point = True        
                if tbtool.keyframe_type_EXTREME:
                    if k.type == 'EXTREME':                                        
                        k.select_control_point = True
                if tbtool.keyframe_type_JITTER:
                    if k.type == 'JITTER':                                        
                        k.select_control_point = True
            else:
                if k.type == tbtool.keyframe_type:
                    k.select_control_point = True

class TB_KTS_SELECTOR(bpy.types.Operator):
    bl_idname = "tb_ops.kts_keyframe_selector"
    bl_label = "SKeyframe by type selector"
    bl_description = "Select Keyframes by selected type"
    
    def execute(self, context):
        tb_kts_select_keyframes_by_type(context)
        return {"FINISHED"}
    
def tb_kts_panel(self, context):
        tbtool = bpy.context.scene.tb_kts_prop
        layout = self.layout
        box = layout.box()
        row = box.row(align=True)
        tb_kts_context_index = 0
        if tbtool.keyframe_range == 'SELECTION':
            tb_kts_context_index = 0
        elif tbtool.keyframe_range == 'COLLECTION':
            tb_kts_context_index = 1
        elif tbtool.keyframe_range == 'SCENE':
            tb_kts_context_index = 2
        elif tbtool.keyframe_range == 'ALL':
            tb_kts_context_index = 3      
        tb_kts_type_index = 0
        if tbtool.keyframe_type == 'KEYFRAME':
            tb_kts_type_index = 0
        elif tbtool.keyframe_type == 'BREAKDOWN':
            tb_kts_type_index = 1
        elif tbtool.keyframe_type == 'MOVING_HOLD':
            tb_kts_type_index = 2
        elif tbtool.keyframe_type == 'EXTREME':
            tb_kts_type_index = 3       
        elif tbtool.keyframe_type == 'JITTER':
            tb_kts_type_index = 4                           
        if tbtool.keyframe_type_context:
            row.prop(tbtool, "keyframe_type_KEYFRAME",text="",icon=tbtool.keyframe_type_icon[0])
            row.prop(tbtool, "keyframe_type_BREAKDOWN",text="",icon=tbtool.keyframe_type_icon[1])
            row.prop(tbtool, "keyframe_type_MOVING_HOLD",text="",icon=tbtool.keyframe_type_icon[2])
            row.prop(tbtool, "keyframe_type_EXTREME",text="",icon=tbtool.keyframe_type_icon[3])
            row.prop(tbtool, "keyframe_type_JITTER",text="",icon=tbtool.keyframe_type_icon[4])  
        else:
            row.prop(tbtool, "keyframe_type",text="",icon=tbtool.keyframe_type_icon[tb_kts_type_index])      
        row.separator()         
        if context.space_data.ui_mode in ['DOPESHEET','ACTION']:
            if tbtool.keyframe_range == 'COLLECTION':
                if tbtool.select_from_active_collection:
                    row.prop(tbtool,"select_from_active_collection",text="Active Collection",icon='PIVOT_ACTIVE')
                else:
                    row.prop(tbtool,"select_from_active_collection",text="",icon='PIVOT_ACTIVE')                    
                    row.prop(tbtool,"select_from_collection",text="")
                row.prop(tbtool, "keyframe_range",text="",icon=tbtool.keyframe_context_icon[tb_kts_context_index])
            else:
                row.prop(tbtool, "keyframe_range",text="",icon=tbtool.keyframe_context_icon[tb_kts_context_index])
            row.prop(tbtool,"affect_current_scene_keyframes",text="",icon='SCENE_DATA')
        row = box.row(align=True)
        row.operator("tb_ops.kts_keyframe_selector",text="Select Keyframes")

class TB_PT_KBS(bpy.types.Panel):
    bl_space_type = 'DOPESHEET_EDITOR'
    bl_region_type = 'UI'
    bl_category = "TB"
    bl_label = ""
    bl_idname = "TB_KTS_panel"
    @classmethod
    def poll(cls, context):
        return context.space_data.ui_mode in ['DOPESHEET','ACTION']
    def draw_header(self,context):
        tbtool = context.scene.tb_kts_prop
        layout = self.layout
        layout.label(icon='KEYFRAME_HLT')

        layout.label(text="KTS Keyframe by type selector")
        layout.prop(tbtool,"keyframe_type_context",text="",icon='ARROW_LEFTRIGHT')
    def draw (self,context):
        tb_kts_panel(self, context)

classes = (TB_KTS_Properties,
    TB_KTS_SELECTOR,
    TB_PT_KBS,
    )

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
        bpy.types.Scene.tb_kts_prop = bpy.props.PointerProperty(type= TB_KTS_Properties)   

def unregister():
 #CLASSES
    for cls in classes:
        bpy.utils.unregister_class(cls)
        bpy.types.Scene.tb_kts_prop
     
if __name__ == "__main__":
    register()
