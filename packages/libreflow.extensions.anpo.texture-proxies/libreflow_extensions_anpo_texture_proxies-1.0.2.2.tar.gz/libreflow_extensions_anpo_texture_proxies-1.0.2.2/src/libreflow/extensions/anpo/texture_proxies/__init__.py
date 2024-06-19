import os
import re
import subprocess
from kabaret import flow
from kabaret.flow.object import _Manager
from libreflow.baseflow.site import WorkingSite
from libreflow.baseflow.asset import AssetType, AssetFamily
from libreflow.baseflow.file import TrackedFolder
from libreflow.utils.flow.values import MultiOSParam
from libreflow.utils.os import remove_folder_content

from . import _version
__version__ = _version.get_versions()['version']

# def get_img_width(img_path):
#     '''Return the width of the provided image.'''
#     output = subprocess.check_output(
#         ["identify", "-format", "%[w]", img_path])
#     return int(output.decode())

def get_img_max_width(blender_path, tex_dir):
    '''Return the highest width found among images in the given folder.'''
    script_path = os.path.join(os.path.dirname(__file__), 'get_max_width.py')
    try:
        result = subprocess.run([
            blender_path, '-b',
            '--python', script_path, '--', tex_dir],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        print(f"[TEXTURE PROXIES] Error while checking texture sizes:")
        print(e.stderr)
        return -1

    m = re.search(r'TEXTURE_MAX_WIDTH_FOUND=(\d+)', result.stdout.decode())
    if result.returncode > 0 or m is None:
        print(f"[TEXTURE PROXIES] Error while checking texture sizes:")
        print(result.stderr.decode())
        return -1

    return int(m.group(1))

def create_proxies(blender_path, src_path, new_width, dst_path):
    script_path = os.path.join(os.path.dirname(__file__), 'create_proxies.py')
    try:
        result = subprocess.run([
            blender_path, '-b',
            '--python', script_path, '--',
            src_path, dst_path, str(new_width)],
            stdout=open(os.devnull, 'wb'), stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        print(f"[TEXTURE PROXIES] Error while creating proxies:")
        print(e.stderr)
        return False

    if result.returncode > 0:
        print(f"[TEXTURE PROXIES] Error while creating proxies:")
        print(result.stderr.decode())
        return False

    return True

class RevisionNameChoiceValue(flow.values.SessionValue):
    DEFAULT_EDITOR = 'choice'
    STRICT_CHOICES = False
    _folder = flow.Parent(2)

    def __init__(self, parent, name):
        super(RevisionNameChoiceValue, self).__init__(parent, name)
        self._revision_names = None

    def choices(self):
        if self._revision_names is None:
            self._revision_names = self._folder.get_revision_names(
                sync_status='Available', published_only=True)
        
        return self._revision_names

    def reset(self):
        self._revision_names = None
        names = self.choices()
        if names:
            self.set(names[-1])

class CreateTextureProxies(flow.Action):
    _MANAGER_TYPE = _Manager
    overwrite = flow.SessionParam(False).ui(editor='bool', \
        tooltip="Use this option to overwrite existing proxies.")

    def needs_dialog(self):
        return True

    def get_buttons(self):
        return ['Create proxies', 'Cancel']

    def get_texture_folders(self):
        raise NotImplementedError()

    def get_proxies_path(self, asset_name, task, suffix, revision_name, overwrite):
        folder_name = f"textures_{suffix}"
        path_format = None
        if not task.files.has_mapped_name(folder_name):
            task_mng = self.root().project().get_task_manager()
            if task_mng.has_default_task(task.name()):
                default_task = task_mng.default_tasks[task.name()]
                if default_task.files.has_mapped_name(folder_name):
                    print(f"[TEXTURE PROXIES] {asset_name} - Create {folder_name} from preset")
                    path_format = default_task.files[folder_name].path_format.get()

            tex_folder = task.files.add_folder(folder_name, \
                tracked=True, default_path_format=path_format)
            tex_folder.file_type.set('Works')
        else:
            tex_folder = task.files[folder_name]

        rev = tex_folder.get_revision(revision_name)
        if rev is None:
            print(f"[TEXTURE PROXIES] {asset_name} - {folder_name}: add new revision {revision_name}")
            rev = tex_folder.add_revision(revision_name)
        tex_path = rev.get_path()
        if not os.path.isdir(tex_path):
            os.makedirs(tex_path, exist_ok=True)
        elif overwrite:
            print(f"[TEXTURE PROXIES] {asset_name} - {folder_name}({revision_name}): clear folder")
            remove_folder_content(tex_path)
        return tex_path

    def get_blender_path(self):
        # Check environment
        path = os.environ.get('BLENDER_EXEC_PATH')
        if path is not None:
            return path

        # Check site runner executables
        site_env = self.root().project().get_current_site().site_environment
        if not site_env.has_mapped_name('BLENDER_EXEC_PATH'):
            return None

        value = site_env['BLENDER_EXEC_PATH'].value
        value.touch()
        return value.get()

    def run(self, button):
        if button == 'Cancel':
            return

        blender_path = self.get_blender_path()
        if blender_path is None or not os.path.isfile(blender_path):
            msg = ('<h3 style="font-weight: 400"><div style="color: red">Error: </div>'
                  f'Blender executable not set. Please define it in the site settings.</h3>')
            self.message.set(msg)
            return self.get_result(close=False)

        self.message.set("")
        overwrite = self.overwrite.get()
        for asset_name, task, tex_folder, revision_name in self.get_texture_folders():
            rev = tex_folder.get_revision(revision_name)
            if rev is None:
                continue

            rev_path = rev.get_path()
            print(f"[TEXTURE PROXIES] {asset_name} - checking texture sizes...")
            max_width = get_img_max_width(blender_path, rev_path)
            if max_width < 0:
                continue

            print(f"[TEXTURE PROXIES] {asset_name} - found max size -> {max_width}")

            for suffix, res in (
                ("1k", 1024),
                ("2k", 2048)):
                if max_width <= res:
                    print(f"[TEXTURE PROXIES] {asset_name} - skip textures_{suffix}")
                    continue

                proxy_dir = self.get_proxies_path(asset_name, task, suffix, rev.name(), overwrite)
                print(f"[TEXTURE PROXIES] {asset_name} - textures_{suffix}({rev.name()}): resizing...")
                created = create_proxies(blender_path, \
                    rev_path, res, proxy_dir)
                if created:
                    print(f"[TEXTURE PROXIES] {asset_name} - textures_{suffix}({rev.name()}): proxies created -> {proxy_dir}")

class CreateFolderTextureProxies(CreateTextureProxies):
    revision = flow.SessionParam(value_type=RevisionNameChoiceValue)
    overwrite = flow.SessionParam(False).ui(editor='bool', \
        tooltip="Use this option to overwrite existing proxies.")
    _folder = flow.Parent()
    _task = flow.Parent(3)
    _asset = flow.Parent(5)

    def needs_dialog(self):
        self.revision.reset()
        return True

    def allow_context(self, context):
        return not self._folder.is_empty()

    def get_texture_folders(self):
        return [(self._asset.name(), self._task, self._folder, self.revision.get())]

class BatchCreateTextureProxies(CreateTextureProxies):

    def get_texture_oid_filter(self):
        raise NotImplementedError()

    def get_texture_folders(self):
        project_files = self.root().project().get_entity_manager().get_file_collection()
        c = project_files.get_entity_store().get_collection(
            project_files.collection_name())
        cursor = c.find({'name': {'$regex': self.get_texture_oid_filter() }})

        def get_folder_data(doc):
            m = re.match(rf'^(?P<task_oid>{self.root().project().oid()}/asset_types/[^/]+/asset_families/[^/]+/assets/(?P<asset_name>[^/]+)/tasks/shading)', doc['name'])
            return (m.group('asset_name'),                   # asset name
                self.root().get_object(m.group('task_oid')), # task
                self.root().get_object(doc['name']),         # folder
                doc['last_revision_oid'].rsplit('/', 1)[1])  # revision name
        data = [get_folder_data(d) \
            for d in cursor]
        return data

class CreateAssetTypeTextureProxies(BatchCreateTextureProxies):
    _asset_type = flow.Parent()

    def get_texture_oid_filter(self):
        return (f"^{self._asset_type.oid()}/"
                f"asset_families/({'|'.join(self._asset_type.asset_families.mapped_names())})/"
                 "assets/[^/]+/"
                 "tasks/shading/files/textures$")

class CreateAssetFamilyTextureProxies(BatchCreateTextureProxies):
    _asset_family = flow.Parent()

    def get_texture_oid_filter(self):
        return (f"^{self._asset_family.oid()}/"
                f"assets/({'|'.join(self._asset_family.assets.mapped_names())})/"
                 "tasks/shading/files/textures$")


def create_proxies_action(parent):
    if isinstance(parent, TrackedFolder) and parent.name() == 'textures':
        r = flow.Child(CreateFolderTextureProxies)
        r.name = 'create_proxies'
        r.index = None
        return r

    if isinstance(parent, AssetFamily):
        r = flow.Child(CreateAssetFamilyTextureProxies)
        r.name = 'create_proxies'
        r.index = None
        return r

    if isinstance(parent, AssetType):
        r = flow.Child(CreateAssetTypeTextureProxies)
        r.name = 'create_proxies'
        r.index = None
        return r

def install_extensions(session):
    return {
        "texture_proxies": [
            create_proxies_action,
        ]
    }
