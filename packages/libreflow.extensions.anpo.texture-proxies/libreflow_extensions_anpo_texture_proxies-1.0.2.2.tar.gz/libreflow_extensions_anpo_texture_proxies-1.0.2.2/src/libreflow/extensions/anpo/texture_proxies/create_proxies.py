import os
import sys
import bpy
import traceback

bpy.context.scene.render.image_settings.exr_codec = 'DWAA'
bpy.context.scene.render.image_settings.file_format = 'OPEN_EXR'
bpy.context.scene.render.image_settings.color_mode = 'RGB'
bpy.context.scene.render.image_settings.color_depth = '16'

def create_proxies(tex_dir, proxy_dir, proxy_width):
    res = int(proxy_width)
    for tex in sorted(os.listdir(tex_dir)):
        img = bpy.data.images.load(os.path.join(tex_dir, tex))
        dst_path = os.path.join(proxy_dir, tex)
        # Skip existing
        if os.path.isfile(dst_path):
            continue

        proxy_img = img.copy()
        try:
            proxy_img.scale(res, res)
            proxy_img.save_render(filepath=dst_path)
        except RuntimeError:
            print(f"Image corrupted: {dst_path}")
        bpy.data.images.remove(proxy_img)
        bpy.data.images.remove(img)


if __name__ == "__main__":
    try:
        create_proxies(sys.argv[5], sys.argv[6], sys.argv[7])
    except:
        print(traceback.format_exc(), file=sys.stderr)
        sys.exit(255)
