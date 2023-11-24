import objaverse
import random
import os
import trimesh
import yaml

DOWNLOAD_PATH = f'/root/.objaverse/hf-objaverse-v1/objs'

def get_objaverse_subset():
    with open("./fid-objaverse/objaverse_list.txt") as f:
        ids = [l.rstrip().split("_")[-1] for l in f.readlines()]

    return ids

def download_objaverse_subset():
    print(f'Running Objaverse ver {objaverse.__version__}\n')

    uids = get_objaverse_subset()
    print(f'Total {len(uids)} 3D objects\n')

    processes = 1
    print(f'{processes} processes available')

    random.seed(42)

    objects = objaverse.load_objects(
        uids=uids,
        download_processes=processes
    )

    objects = objaverse.load_objects(uids=uids)
    object_list = list(objects.values())
    num_objects = len(object_list)

    parent_path = object_list[0][:object_list[0].find('glbs')]
    parent_path_len = len(parent_path)
    objs_path = parent_path + 'objs/'

    for i, obj in enumerate(object_list):

        obj_category = obj[parent_path_len+5 : parent_path_len+12]
        obj_uid = obj[parent_path_len+13:-4]
        obj_path = objs_path + obj_category + '/'

        os.makedirs(obj_path, exist_ok=True)

        obj_path = obj_path + obj_uid + '/'

        if os.path.exists(obj_path):
            print(f'[{i}/{num_objects}] Exists. Skipping : {obj_uid}')
            continue

        print(f'[{i}/{num_objects}] Converting : {obj_uid}')

        os.makedirs(obj_path, exist_ok=False)

        glb_path = obj
        obj_path = obj_path + 'object.obj'

        scene = trimesh.load(glb_path)
        
        try:
            scene.export(obj_path)
        except:
            print(f'[Error] when converting {obj_path}')

def get_objaverse_subset():
	subset_list = dict()

	with open("./fid-objaverse/objaverse_list.txt") as f:
		for l in f.readlines():
			id = l.rstrip().split("_")[-1]
			subset_list[id] = '_'.join(l.rstrip().split("_")[:-1])
			
	return subset_list

def get_data_list(base_path, guide_file_name):
	data_list = [] # guide_path, id, name, object_path\
	guide_list = []
	
	dir_list = os.listdir(base_path)
	objaverse_subset = get_objaverse_subset()
	
	for dir in dir_list:
		id_list = os.listdir(base_path + "/" + dir)
		
		for id in id_list:
			name = objaverse_subset[id]
			guide_path = base_path + "/" + dir + "/" + id + "/" + guide_file_name
			object_path = base_path + "/" + dir + "/" + id + "/object.obj"
			data_list.append([guide_path, id, name, object_path])
			guide_list.append(guide_path)
			
	return data_list, guide_list

def generate_guide(base_path, exp_path, guide_file_name, guide_list_name, is_rand = False):
    base_path = DOWNLOAD_PATH
    list_path = './fid-objaverse/' + guide_list_name
    data_list, guide_list = get_data_list(base_path, guide_file_name)

    for data in data_list:
        guide_path = data[0]
        id = exp_path + "/" + data[1]
        name = f"{data[2].replace('_', ' ')}, {{}} view"
        object_path = data[3]
        
        if os.path.exists(guide_path):
            os.remove(guide_path)
        
        yaml_data = {'log': {'exp_name': id}, 'guide': {'text': name, 'append_direction': True, 'shape_path': object_path}, 'optim': {'seed': 3}}

        if is_rand:
            yaml_data['guide']['use_random_viewpoint'] = True

        with open(guide_path, 'x') as file:
            yaml.dump(yaml_data, file)
            
    if os.path.exists(list_path):
        os.remove(list_path)

    with open(list_path, 'x') as file:
        file.write('\n'.join(guide_list))

if __name__ == "__main__":
    download_objaverse_subset()
    generate_guide(DOWNLOAD_PATH, 'normal', 'guide.yaml', 'guide_list.txt')
    generate_guide(DOWNLOAD_PATH, 'random', 'guide_rand.yaml', 'guide_rand_list.txt', is_rand=True)
