# ✨增大blender撤销上限的脚本

[**English**](./README_EN.md) | [**中文**](./README.md)

## 使用方法

1. 下载script.py，在blender的文本编辑器中打开，或者直接复制以下代码到blender的文本编辑器中：
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
subprocess.Popen([source_file_path,"--python-expr","import bpy;bpy.context.preferences.edit.undo_steps = 1000"])
bpy.ops.wm.quit_blender()
"""
subprocess.Popen([new_file_path,"-b","--python-expr",copy])
bpy.ops.wm.quit_blender()
```

2. 运行脚本，blender会重启（记得保存当前的文件！），没有报错就是修改好了，撤销次数增大到1000，上限提高到10000


## 注意事项
> 只适用于windows，mac应该没有exe文件

> 经过测试，3.3，3.6，4.0，4.1版本都能正常使用

> 如果你下载了新版本的blender(默认撤销上限256)，但是加载了旧版本用户设置（撤销次数修改至>256）,会导致撤销功能失效。需要对新版本使用此脚本或者降低撤销次数。

## 原理
在blender源代码的`rna_userdef.cc`中，找到

RNA_def_property_int_sdna(prop, nullptr, "undosteps");

RNA_def_property_range(prop, 0, 256);

把256改成更大的数就能提高撤销上限。
> 注意，undosteps的变量类型是short，不能改成超过32767的数，也不能把short改成long这类的东西，会出现内存对齐问题导致编译失败。

不过下载和编译源码是很繁琐的过程，我把新旧文件作比较，找到变动的地方，以后直接修改这一处就可以了。然后就有了这个python脚本。由于blender运行时不能修改blender.exe自身，需要复制一个缓存文件，也就是脚本中的BlenderPro.exe.
