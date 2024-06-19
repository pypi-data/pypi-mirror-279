import os
import bpy
import sys
import traceback


def get_max_width(tex_dir):
    max_width = -1
    for tex in os.listdir(tex_dir):
        print(tex)
        tex_path = os.path.join(tex_dir, tex)
        # Skip folders
        if not os.path.isfile(tex_path):
            continue

        img = bpy.data.images.load(tex_path)
        max_width = max(max_width, img.size[0])
        print(tex_path, img.size[0])
        bpy.data.images.remove(img)
    return max_width


if __name__ == "__main__":
    try:
        width = get_max_width(sys.argv[5])
    except:
        print(traceback.format_exc(), file=sys.stderr)
        sys.exit(255)
    else:
        if width <= 0:
            print(f"No valid texture found in {sys.argv[5]}", file=sys.stderr)
            sys.exit(255)

        print(f"TEXTURE_MAX_WIDTH_FOUND={width}")