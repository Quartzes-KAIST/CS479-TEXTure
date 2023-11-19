import yaml
import os

def get_objaverse_subset():
	subset_list = dict()

	with open("./fid-objaverse/objaverse_list.txt") as f:
		for l in f.readlines():
			id = l.rstrip().split("_")[-1]
			subset_list[id] = '_'.join(l.rstrip().split("_")[:-1])
			
	return subset_list

def get_data_list(base_path):
	data_list = [] # guide_path, id, name, object_path\
	guide_list = []
	
	dir_list = os.listdir(base_path)
	objaverse_subset = get_objaverse_subset()
	
	for dir in dir_list:
		id_list = os.listdir(base_path + "/" + dir)
		
		for id in id_list:
			name = objaverse_subset[id]
			guide_path = base_path + "/" + dir + "/" + id + "/guide.yaml"
			object_path = base_path + "/" + dir + "/" + id + "/object.obj"
			data_list.append([guide_path, id, name, object_path])
			guide_list.append(guide_path)
			
	return data_list, guide_list

base_path = f'/root/.objaverse/hf-objaverse-v1/objs'
data_list, guide_list = get_data_list(base_path)

for data in data_list:
	guide_path = data[0]
	id = data[1]
	name = f"{data[2]}, {{}} view"
	object_path = data[3]
	
	if os.path.exists(guide_path):
		print(f'{guide_path} Exists. Skipping')
		continue
	
	yaml_data = {'log': {'exp_name': id}, 'guide': {'text': name, 'append_direction': True, 'shape_path': object_path}, 'optim': {'seed': 3}}

	with open(guide_path, 'x') as file:
		yaml.dump(yaml_data, file)
		
if os.path.exists('./fid-objaverse/guide_list.txt'):
    print(f'{guide_path} Exists. Skipping')

with open('./fid-objaverse/guide_list.txt', 'x') as file:
	file.write('\n'.join(guide_list))