import os

curr_dir = os.getcwd()

def recover_all_symlinks(root_dir):
	dirs_or_files = os.listdir(root_dir)
	for dir_file in dirs_or_files:
		dir_file_path = os.path.join(root_dir,dir_file)
		if os.path.islink(dir_file_path):
			src_file = os.readlink(dir_file_path)
			if curr_dir in src_file:
				os.unlink(dir_file_path)
				new_src_file = src_file[len(curr_dir):]
				os.symlink(new_src_file, dir_file_path)
				print "now", dir_file_path, os.readlink(dir_file_path)
		else:
			if os.path.isdir(dir_file_path):
				recover_all_symlinks(dir_file_path)

recover_all_symlinks(".")
