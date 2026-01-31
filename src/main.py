#!/usr/bin/env python3
import os
import shutil

from generate_page import generate_pages_recursively

def export_to_dst(src, dst):
    if not os.path.exists(src):
        raise FileNotFoundError(f'The source {src} does not exist')
    if not os.path.exists(dst):
        print(f'Creating {dst} as it does not exist')
        os.mkdir(dst)

    dir_contents = os.listdir(dst)
    if dir_contents:
        _delete_contents(dst, dir_contents)

    src_contents = os.listdir(src)
    for content in src_contents:
        src_path = os.path.join(src, content)
        dst_path = os.path.join(dst, content)
        if os.path.isfile(src_path):
            print(f'Copying {src_path} to {dst_path}')
            shutil.copy(src_path, dst_path)
            continue
        if os.path.isdir(src_path):
            export_to_dst(src_path, dst_path)


def _delete_contents(dst, contents):
    for content in contents:
        path = os.path.join(dst, content)
        print(f'Deleting {path}')

        if os.path.isdir(path):
            shutil.rmtree(path)
        elif os.path.isfile(path):
            os.remove(path)
        else:
            raise Exception(f'This is not a file or a directory: {path}')


def main():
    export_to_dst('./static', './public')
    generate_pages_recursively('./content', './template.html', './public')

if __name__ == '__main__':
    main()