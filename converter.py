import os
import sys

def get_files():
	result = []
	for file in sys.argv[1:]:
		if not os.path.isfile(file):
			print("could not find file {}, skipping".format(file))
			continue
		result.append(file)
	return result
	
def get_changes():
	"""
	prompts the user to define the differences between source and target files
	consists of original file location (e.g. "E:\Music\Artist\Album\Song.mp3")
	and target file location (e.g. "/storage/6264-6134/Music/Artist/Album/Song.mp3")
	
	user should provide location BEFORE Artist so that it can be changed.
	assumes that files are kept in same relative location and that folder
	structure is identical
	"""	
	ORIGINAL_FILE_DEFAULT = "\\Music\\"
	ORIGINAL_INPUT_STRING = "Please provide the original file location" +\
							" (for default ({}) leave empty)".format(ORIGINAL_FILE_DEFAULT)
	TARGET_FILE_DEFAULT = "/storage/6264-6134/"
	TARGET_INPUT_STRING = "Please provide the target file location" +\
						  " (for default ({}) leave empty)".format(TARGET_FILE_DEFAULT)
	original = input(ORIGINAL_INPUT_STRING)
	if original == "":
		original = ORIGINAL_FILE_DEFAULT
	target = input(TARGET_INPUT_STRING)
	if target == "":
		target = TARGET_FILE_DEFAULT
	return [original, target]
	
def get_new_filename(old_filename):
	parts = old_filename.split(".")
	parts[0] = parts[0] + "_converted"
	return ".".join(parts)
	
def do_exchange_location(line, changes):
	global did_a_print
	location_removed = line[len(changes[0]):]
	line_cleaned = "/".join(location_removed.split("\\"))
	converted = os.path.join(changes[1], line_cleaned)
	return converted
	
	
def do_convert(files, changes):
	for file in files:
		target_lines = []
		target_lines.append("#EXT3MU\n")  # supposed to be at beginning of file
		# read file 
		with open(file, "r") as original:
			print("reading file: " + file)
			for line in original:
				# ignore comments
				if line.startswith("#"):
					continue
				# ignore invalid file links
				if not line.startswith(changes[0]):
					print("ERROR: unexpected file location: {} expected: {}".format(line, changes[0]))
					continue
				# convert location
				target_lines.append(do_exchange_location(line, changes))
		
		# write converted file
		file_name = get_new_filename(file)
		print("writing converted playlist to " + file_name)
		with open(file_name, "w") as conv_file:
			for line in target_lines:
				conv_file.write(line)
	
if __name__ == "__main__":
	files = get_files()
	changes = get_changes()
	do_convert(files, changes)
			