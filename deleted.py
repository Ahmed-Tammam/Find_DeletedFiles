import argparse
import os
import shutil
from winreg import *


def sid_to_user(sid):
    try:
        key = OpenKey(HKEY_LOCAL_MACHINE,
                      "SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\ProfileList" + '\\' + sid)
        (value, type) = QueryValueEx(key, "ProfileImagePath")
        user = value.split('\\')
        return user
    except:
        return sid


def find_recycled_bin():
    recycled_bin_dirs = ['C:\\Recycler\\', 'C:\\Recycled\\', 'C:\\$Recycle.Bin\\']
    for recycled_bin_dir in recycled_bin_dirs:
        if os.path.isdir(recycled_bin_dir):
            return recycled_bin_dir
    return None


def dump_recycled_files(recycled_bin_dir, dump_dir, recursive=False, filter_type=None, filter_size=None, restore=False, log_file=None):
    if not os.path.exists(dump_dir):
        os.makedirs(dump_dir)
    sid_dirs = os.listdir(recycled_bin_dir)
    for sid_dir in sid_dirs:
        files = os.listdir(os.path.join(recycled_bin_dir, sid_dir))
        user = sid_to_user(sid_dir)
        print(f'\n[*] Dumping files for User: {user}')
        for file in files:
            recycled_file_path = os.path.join(recycled_bin_dir, sid_dir, file)
            if recursive and os.path.isdir(recycled_file_path):
                dump_recycled_files(recycled_file_path, dump_dir, recursive, filter_type, filter_size, restore, log_file)
            elif filter_type and not file.endswith(filter_type):
                continue
            elif filter_size and os.path.getsize(recycled_file_path) < filter_size:
                continue
            else:
                if restore:
                    shutil.move(recycled_file_path, os.path.join(user[0], 'Desktop', file))
                    print(f'[*] Restored file: {recycled_file_path}')
                else:
                    dumped_file_path = os.path.join(dump_dir, file)
                    shutil.move(recycled_file_path, dumped_file_path)
                    print(f'[*] Dumped file: {dumped_file_path}')
                    if log_file:
                        with open(log_file, 'a') as f:
                            f.write(dumped_file_path + '\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Dump files from the Windows Recycle Bin.')
    parser.add_argument('--dump-dir', '-d', type=str, default='E:\\DumpedFiles\\',
                        help='Directory to dump recovered files to.')
    parser.add_argument('--recursive', '-r', action='store_true',
                        help='Recursively dump files from subdirectories of the Recycle Bin.')
    parser.add_argument('--filter-type', '-t', type=str, default=None,
                        help='Only dump files with the specified extension (e.g. ".txt").')
    parser.add_argument('--filter-size', '-s', type=int, default=None,
                        help='Only dump files larger than the specified size (in bytes).')
    parser.add_argument('--restore', '-R', action='store_true',
                        help='Restore files to their original location instead of dumping them.')
    parser.add_argument('--log-file', '-l', type=str, default=None,
                        help='Log dumped file paths to the specified file.')
    args = parser.parse_args()

    recycled_bin_dir = find_recycled_bin()
    if not recycled_bin_dir:
        print('Recycle Bin not found on this system.')
    else:
        dump_recycled_files(recycled_bin_dir, args.dump_dir, args.recursive, args.filter_type, args.filter_size, args.restore, args.log_file)
