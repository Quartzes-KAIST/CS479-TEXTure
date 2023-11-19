import objaverse
import random
import os
import trimesh

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

if __name__ == "__main__":
    download_objaverse_subset()