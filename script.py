import bpy,binascii,os,subprocess

# 获取blender.exe路径
source_file_path = bpy.app.binary_path
source_dir = os.path.dirname(source_file_path)
# 处理过程中的临时文件
new_file_path = os.path.join(source_dir, "BlenderPro.exe")

# 读取16进制文件内容
with open(source_file_path, 'rb') as f:
    content = f.read()
hex_content = binascii.hexlify(content)

# 检查包含撤销次数的特征码，如果只出现一次，就替换它
if hex_content.count(b'00010000000000000001000001000000') == 1:
    hex_content = hex_content.replace(b'00010000000000000001000001000000', b'10270000000000001027000001000000')
elif hex_content.count(b'00010000000000000001000001000000') > 1:
    raise ValueError("修改失败,发现多处特征码,你的blender版本可能过新/过旧")
else:
    raise ValueError("修改失败,没有找到特征码,你的blender版本可能过新/过旧，或者已经修改过了")
new_content = binascii.unhexlify(hex_content)
print("修改成功！")
with open(new_file_path, 'wb') as f:
    f.write(new_content)

#重启blender
copy="""
import bpy,shutil,os,subprocess,time
time.sleep(0.5)
source_file_path = bpy.app.binary_path
source_dir = os.path.dirname(source_file_path)
new_file_path = os.path.join(source_dir, "blender.exe")
shutil.copy(bpy.app.binary_path, "blender.exe")
subprocess.Popen([source_file_path,"--python-expr","import bpy;bpy.context.preferences.edit.undo_steps = 1000"])
bpy.ops.wm.quit_blender()
"""
subprocess.Popen([new_file_path,"-b","--python-expr",copy])
bpy.ops.wm.quit_blender()
