"""
    Will be called from "update_fmdserver_files.sh"
"""

from pathlib import Path

from bx_py_utils.path import assert_is_dir, assert_is_file

import findmydevice


BASE_PATH = Path(findmydevice.__file__).parent
assert_is_dir(BASE_PATH)

FMD_WEB_PATH = BASE_PATH / 'web'
assert_is_dir(FMD_WEB_PATH)

EXTERNAL_DIR_NAME = 'fmd_externals'
STATIC_EXTERNAL_PATH = BASE_PATH / 'static' / EXTERNAL_DIR_NAME
assert_is_dir(STATIC_EXTERNAL_PATH)

# TODO: https://gitlab.com/jedie/django-find-my-device/-/issues/7
STATIC_URL_PREFIX = f'static/{EXTERNAL_DIR_NAME}'


class FilePatcher:
    def __init__(self, file_path: Path):
        print('_' * 100)
        assert_is_file(file_path)
        self.file_path = file_path

    def __enter__(self):
        self.content = self.file_path.read_text(encoding='utf-8')
        return self

    def patch(self, old, new):
        if old not in self.content:
            print(f'Warning: {old!r} not found in "{self.file_path}" !')
        elif new not in self.content:
            self.content = self.content.replace(old, new)

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            raise
        self.file_path.write_text(self.content, encoding='utf-8')
        print(f' *** {self.file_path} patched ***')
        print('-' * 100)


def patch_html_files():
    for file_path in FMD_WEB_PATH.glob('*.html'):
        with FilePatcher(file_path=file_path) as patcher:
            # It's not the origin server ;)
            patcher.patch('<title>FMD</title>', '<title>Django Find My Device</title>')
            patcher.patch('<h2>FMD Server</h2>', '<h2>Django Find My Device</h2>')
            patcher.patch('<h2>Find My Device</h2>', '<h2>Django Find My Device</h2>')
            patcher.patch(
                'https://gitlab.com/Nulide/findmydeviceserver/', 'https://gitlab.com/jedie/django-find-my-device'
            )

            patcher.patch('"./', f'"./{STATIC_URL_PREFIX}/')
            patcher.patch('"assets/', f'"./{STATIC_URL_PREFIX}/assets/')

            patcher.patch('</head>', f'    <link rel="icon" href="./{STATIC_URL_PREFIX}/favicon.ico">\n</head>')


def patch_js_files():
    with FilePatcher(file_path=STATIC_EXTERNAL_PATH / 'node_modules/argon2-browser/lib/argon2.js') as patcher:
        patcher.patch("'node_modules/", f"'./{STATIC_URL_PREFIX}/node_modules/")


if __name__ == '__main__':
    patch_html_files()
    patch_js_files()
