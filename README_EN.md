# ✨Increase Blender's Undo Limit

[**English**](./README_EN.md) | [**中文**](./README.md)

## How to Use

1. Download script.py, open it in Blender's text editor, or directly copy the following code into Blender's text editor:
```
import bpy,binascii,os,subprocess
source_file_path = bpy.app.binary_path
source_dir = os.path.dirname(source_file_path)
new_file_path = os.path.join(source_dir, "BlenderPro.exe")
with open(source_file_path, 'rb') as f:
    content = f.read()
hex_content = binascii.hexlify(content)
if hex_content.count(b'00010000000000000001000001000000') == 1:
    hex_content = hex_content.replace(b'00010000000000000001000001000000', b'10270000000000001027000001000000')
elif hex_content.count(b'00010000000000000001000001000000') > 1:
    raise ValueError("修改失败,发现多处特征码,你的blender版本可能过新/过旧")
else:
    raise ValueError("修改失败,没有找到特征码,你的blender版本可能过新/过旧，或者已经修改过了")
new_content = binascii.unhexlify(hex_content)
with open(new_file_path, 'wb') as f:
    f.write(new_content)
copy="""
import bpy,shutil,os,subprocess,time
time.sleep(0.5)
source_file_path = bpy.app.binary_path
source_dir = os.path.dirname(source_file_path)
new_file_path = os.path.join(source_dir, "blender.exe")
shutil.copy(bpy.app.binary_path, "blender.exe")
subprocess.Popen([new_file_path,"--python-expr","import bpy;bpy.context.preferences.edit.undo_steps = 1000"])
bpy.ops.wm.quit_blender()
"""
subprocess.Popen([new_file_path,"-b","--python-expr",copy])
bpy.ops.wm.quit_blender()
```

2. Run the script, Blender will restart (save your current file first!). If there are no errors, it's done. The undo steps has been set to 1000, and the upper limit is increased to 10000.


## Cautions
> Only applicable to Windows, Mac should not have exe files

> Tested with blender 3.3, 3.6, 4.0, 4.1 and they all work well

> If you download a new version of Blender (default undo limit is 256), but then load the old user preferences (undo number modified to >256), it will cause the undo function to fail. You should run this script for the new version or reduce the number of undo steps.

## Behind the script
In the Blender source code `rna_userdef.cc`, find
RNA_def_property_int_sdna(prop, nullptr, "undosteps");
RNA_def_property_range(prop, 0, 256);
Changing 256 to a larger number can increase the undo limit.
> Note, the variable type of undosteps is short, so it cannot be changed to a number greater than 32767, and short cannot be changed to things like long, which will cause memory alignment problems and compilation failure.

However, downloading and compiling the source code is a tedious process. I compared the new and old files, found the changes, and later directly modify them. Eventually this Python script was created. Since blender.exe cannot be modified while Blender is running, I need to copy a cache file which is BlenderPro.exe in the script.