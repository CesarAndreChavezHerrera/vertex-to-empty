import bpy
import bmesh

# crea a empty
def add_empty(obj,vertex_group_name,size):
    
    # crear empty
    bpy.ops.object.mode_set(mode='OBJECT')
    
    bpy.ops.object.empty_add(type='PLAIN_AXES', align='WORLD')
  
    #configuracion del empty
    empty = bpy.context.active_object
    empty.name = vertex_group_name
    empty.empty_display_size = size

    #add constraints to the empty
    contraint = empty.constraints.new(type = "COPY_LOCATION")
    contraint.target = obj
    contraint.subtarget = vertex_group_name

    #select the main obj
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode='EDIT')
    pass

class OBJECT_OT_ADD_VERTEX_GROUP(bpy.types.Operator):
    bl_idname = "object.add_group"
    bl_label  = "Generar vertex group"
    bl_options = {"REGISTER","UNDO"}
    
    name_group  : bpy.props.StringProperty(
                    name = "name of vertex group",
                    default = "")
                    
    mirror_group: bpy.props.BoolProperty(
                    name = "Mirror Select",
                    default = True)
                    
    add_empty: bpy.props.BoolProperty(
                    name = "add empty to vertex group",
                    default = True)
    size_empty: bpy.props.FloatProperty(
                    name = "empty size",
                    default = 1)
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)
    
    
    def execute(self,context):
        
        #selecionar vertices
        
        obj = context.active_object
        
        bm = bmesh.from_edit_mesh(obj.data)
        selected_indices = [v.index for v in bm.verts if v.select]

        # if something are not select
        if not len(selected_indices) == 0:
            
            if not self.mirror_group == True:
                new_group = obj.vertex_groups.new(name =self.name_group )
                
                
                bpy.ops.object.mode_set(mode='OBJECT')
                new_group.add(selected_indices,1.0,"REPLACE")
                if add_empty:
                    add_empty(obj,new_group.name,self.size_empty)
                    pass
                else:
                    bpy.ops.object.mode_set(mode='EDIT')
                pass
            else:
                # Mirror objection
                # Left 
                new_group = obj.vertex_groups.new(name =self.name_group+".L")
                bpy.ops.object.mode_set(mode='OBJECT')
                new_group.add(selected_indices,1.0,"REPLACE")
                if add_empty:
                    add_empty(obj,new_group.name,self.size_empty)
                    pass
                else:
                    bpy.ops.object.mode_set(mode='EDIT')
                    pass
                # Rigt 
                bpy.ops.mesh.select_mirror()
                bm = bmesh.from_edit_mesh(obj.data)
                selected_indices = [v.index for v in bm.verts if v.select]
                
                new_group = obj.vertex_groups.new(name =self.name_group+".R")
                bpy.ops.object.mode_set(mode='OBJECT')
                new_group.add(selected_indices,1.0,"REPLACE")
                if add_empty:
                    add_empty(obj,new_group.name,self.size_empty)
                    pass
                else:
                    bpy.ops.object.mode_set(mode='EDIT')
                pass
                
                bpy.ops.mesh.select_all(action='DESELECT')
            pass
        else:
            self.report({"INFO"},"None vertex select")   
        
        return {"FINISHED"}
        pass
    pass

# main UI
class VIEW3D_PT_grupo_empty(bpy.types.Panel):
    bl_label = "Vertex to empty"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'        # 'UI' indica que es el N-Panel
    bl_category = "Vertex To Empty"
    
    @classmethod 
    def poll(cls, context):
        return context.mode == 'EDIT_MESH'

        
    def draw(self, context): 
        layout = self.layout
        layout.operator("object.add_group")
    pass 


classes = ( 
    VIEW3D_PT_grupo_empty,
    OBJECT_OT_ADD_VERTEX_GROUP,
    ) 

def register(): 
    for cls in classes: 
        bpy.utils.register_class(cls)
        
def unregister(): 
    for cls in reversed(classes): 
        bpy.utils.unregister_class(cls) 
        
if __name__ == "__main__": register()
