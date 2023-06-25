import bpy
from os.path import dirname,abspath
from os.path import join as join_path

bl_info = {
    "name": "Xpd Blender Utils",
    "description": "Inicializa Plantillas mas usadas por mi",
    "author": "Xavier Merizalde",
    "version": (1, 0),
    "blender": (2, 78, 0),
    "location": "View3D > Add > Mesh",
    "warning": "", # used for warning icon and text in addons panel
    "doc_url": "https://xaviermerizalde.wordpess.com",
    "tracker_url": "https://xaviermerizalde.wordpess.com",
    "support": "COMMUNITY",
    "category": "Add Mesh",
}

MALE_AVATAR_PATH = join_path( dirname( abspath(__file__) ), 'modelos' ,'Male COLLADA_1.4.1.dae' )
FEMALE_AVATAR_PATH = join_path( dirname( abspath(__file__) ), 'modelos' ,'Female COLLADA_1.4.1.dae' )
MINETEST_AVATAR_PATH = join_path( dirname( abspath(__file__) ), 'modelos' ,'skinsdb_3d_armor_character_5.dae' )
ROBLOX_AVATAR_PATH = join_path( dirname( abspath(__file__) ), 'modelos' ,'roblox1.dae' )

class ImportMaleAvatarOperator(bpy.types.Operator):
    bl_idname = "xpdoperator.import_male_avatar"
    bl_label = "Avatar Masculino"

    def execute(self, context):
        resultado = bpy.ops.wm.collada_import(filepath = MALE_AVATAR_PATH, 
                                  filter_blender=False, filter_backup=False, filter_image=False, 
                                  filter_movie=False, filter_python=False, filter_font=False, 
                                  filter_sound=False, filter_text=False, filter_btx=False, filter_collada=True, 
                                  filter_alembic=False, filter_folder=True, filter_blenlib=False, filemode=8, 
                                  display_type='DEFAULT', sort_method='FILE_SORT_ALPHA', import_units=False, 
                                  fix_orientation=False, find_chains=False, auto_connect=False, min_chain_length=0
                                  )
        print("Avatar Masculino {0}".format(repr(resultado)) )
        return resultado

class ImportFemaleAvatarOperator(bpy.types.Operator):
    bl_idname = "xpdoperator.import_female_avatar"
    bl_label = "Avatar Femenino"

    def execute(self, context):
        resultado = bpy.ops.wm.collada_import(filepath = FEMALE_AVATAR_PATH, 
                                  filter_blender=False, filter_backup=False, filter_image=False, 
                                  filter_movie=False, filter_python=False, filter_font=False, 
                                  filter_sound=False, filter_text=False, filter_btx=False, filter_collada=True, 
                                  filter_alembic=False, filter_folder=True, filter_blenlib=False, filemode=8, 
                                  display_type='DEFAULT', sort_method='FILE_SORT_ALPHA', import_units=False, 
                                  fix_orientation=False, find_chains=False, auto_connect=False, min_chain_length=0
                                  )
        print("Avatar Femenino {0}".format(repr(resultado)) )
        return resultado
    
class ImportRobloxAvatarOperator(bpy.types.Operator):
    bl_idname = "xpdoperator.import_roblox_avatar"
    bl_label = "Avatar Roblox"

    def execute(self, context):
        resultado = bpy.ops.wm.collada_import(filepath = ROBLOX_AVATAR_PATH, 
                                  filter_blender=False, filter_backup=False, filter_image=False, 
                                  filter_movie=False, filter_python=False, filter_font=False, 
                                  filter_sound=False, filter_text=False, filter_btx=False, filter_collada=True, 
                                  filter_alembic=False, filter_folder=True, filter_blenlib=False, filemode=8, 
                                  display_type='DEFAULT', sort_method='FILE_SORT_ALPHA', import_units=False, 
                                  fix_orientation=False, find_chains=False, auto_connect=False, min_chain_length=0
                                  )
        print("Avatar Roblox {0}".format(repr(resultado)) )
        return resultado

class ImportMinetestAvatarOperator(bpy.types.Operator):
    bl_idname = "xpdoperator.import_minetest_avatar"
    bl_label = "Avatar MineTest"

    def execute(self, context):
        resultado = bpy.ops.wm.collada_import(filepath = MINETEST_AVATAR_PATH, 
                                  filter_blender=False, filter_backup=False, filter_image=False, 
                                  filter_movie=False, filter_python=False, filter_font=False, 
                                  filter_sound=False, filter_text=False, filter_btx=False, filter_collada=True, 
                                  filter_alembic=False, filter_folder=True, filter_blenlib=False, filemode=8, 
                                  display_type='DEFAULT', sort_method='FILE_SORT_ALPHA', import_units=False, 
                                  fix_orientation=False, find_chains=False, auto_connect=False, min_chain_length=0
                                  )
        print("Avatar Minetest {0}".format(repr(resultado)) )
        return resultado

def menu_ImportMaleAvatar(self, context):
    self.layout.operator(ImportMaleAvatarOperator.bl_idname, text=ImportMaleAvatarOperator.bl_label)

def menu_ImportFemaleAvatar(self, context):
    self.layout.operator(ImportFemaleAvatarOperator.bl_idname, text=ImportFemaleAvatarOperator.bl_label)

def menu_ImportRobloxAvatar(self, context):
    self.layout.operator(ImportRobloxAvatarOperator.bl_idname, text=ImportRobloxAvatarOperator.bl_label)

def menu_ImportMinetestAvatar(self, context):
    self.layout.operator(ImportMinetestAvatarOperator.bl_idname, text=ImportMinetestAvatarOperator.bl_label)

def menu_Separator(self, context):
    self.layout.separator('xpdoperator.separator')

OBJETOS = [
    {'clase': ImportMaleAvatarOperator, 'menu': menu_ImportMaleAvatar},
    {'clase': ImportFemaleAvatarOperator, 'menu': menu_ImportFemaleAvatar},
    {'clase': ImportRobloxAvatarOperator, 'menu': menu_ImportRobloxAvatar},
    {'clase': ImportMinetestAvatarOperator, 'menu': menu_ImportMinetestAvatar}
    ]

def register():
    bpy.types.INFO_MT_add.append( menu_Separator ) 
    for objeto in OBJETOS:
        bpy.utils.register_class( objeto['clase'] )
        bpy.types.INFO_MT_add.append( objeto['menu'] )    
    
def unregister():
    bpy.types.INFO_MT_add.remove( menu_Separator ) 
    for objeto in OBJETOS:
        bpy.utils.unregister_class( objeto['clase'] )
        bpy.types.INFO_MT_add.remove( objeto['menu'] )    


if __name__ == "__main__":
    register()