import os

curr_dir = os.getcwd()

def list_all_symlinks(root_dir):
	dirs_or_files = os.listdir(root_dir)
	for dir_file in dirs_or_files:
		dir_file_path = os.path.join(root_dir,dir_file)
		if os.path.islink(dir_file_path):
			#print dir_file_path,"     ", os.readlink(dir_file_path)
			src_file = os.readlink(dir_file_path)
			if cmp(src_file[0], "/") == 0:
				os.unlink(dir_file_path)
				os.symlink(curr_dir + src_file, dir_file_path)
				print "now", dir_file_path, os.readlink(dir_file_path)
		else:
			if os.path.isdir(dir_file_path):
				list_all_symlinks(dir_file_path)

list_all_symlinks(".")
