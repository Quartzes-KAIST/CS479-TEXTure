import trimesh
import os
import io
import pyglet
import numpy as np
import math

from PIL import Image
from pyglet import gl

pyglet.options["headless"] = True

BASE_PATH = f'/root/CS479-TEXTure/experiments/normal'
TEST_PATH = f'/root/.objaverse/hf-objaverse-v1/texture_normal_tests/'

def get_objaverse_subset():
	subset_list = dict()

	with open("./fid-objaverse/objaverse_list.txt") as f:
		for l in f.readlines():
			id = l.rstrip().split("_")[-1]
			subset_list[id] = '_'.join(l.rstrip().split("_")[:-1])
			
	return subset_list

def get_file_list(base_path):
	file_list = []
	id_result = []
	
	dir_list = os.listdir(base_path)
	
	for dir in dir_list:
		file_list.append(base_path + "/" + dir + "/mesh/mesh.obj")
		id_result.append(dir)
			
	return file_list, id_result

def generate_gif(source_dir:str, prefix:str, postfix:str, save_dir:str):
	img_list = os.listdir(source_dir)

	prefix_len  = len(prefix)
	postfix_len = len(postfix)

	if postfix_len > 0:
		idx_list = sorted([int(i[:-4][prefix_len:-postfix_len]) for i in img_list])
	else:
		idx_list = sorted([int(i[:-4][prefix_len:]) for i in img_list])

	img_list = [f'{prefix}{idx:02}{postfix}.png' for idx in idx_list]

	img_list = [os.path.join(source_dir , x) for x in img_list]
	images = [Image.open(x) for x in img_list]
	
	im = images[0]
	im.save(os.path.join(save_dir, 'out.gif'), save_all=True, append_images=images[1:],loop=0xff, duration=500)

# render qualitative results
def render_qualitative_results():
	render_list, id_result = get_file_list(BASE_PATH)

	for obj_path in render_list:
		save_dir = '/root/.objaverse/hf-objaverse-v1/texture_renders/' + obj_path[len(BASE_PATH):-11]

		print(save_dir)

		if os.path.exists(save_dir):
			print(f'{save_dir} Exists. Skipping')
			continue

		os.makedirs(save_dir, exist_ok=True)

		scene = trimesh.load(obj_path, force='mesh')
		window_conf = gl.Config(double_buffer=True, depth_size=6)

		scene.vertices = np.dot(scene.vertices - scene.centroid, trimesh.transformations.rotation_matrix(90 * (math.pi / 180), direction=[0, 1, 0], point=[0, 0, 0])[:3, :3])
		center = scene.bounds.mean(axis=0)

		png = scene.scene().save_image(resolution=[1920, 1080], visible=True, window_conf=window_conf)

		image = Image.open(io.BytesIO(png))
		im1 = image.save(os.path.join(save_dir, 'render.png')) 

		gif_dir = os.path.join(save_dir, 'gif')

		os.makedirs(gif_dir, exist_ok=True)

		for i in range(0,18):
			scene.vertices = np.dot(scene.vertices, trimesh.transformations.rotation_matrix(10 * (math.pi / 180), direction=[0, 1, 0], point=center)[:3, :3])
			png = scene.scene().save_image(resolution=[1920, 1080], visible=True, window_conf=window_conf)

			image = Image.open(io.BytesIO(png))
			im1 = image.save(os.path.join(gif_dir, f'{i:02}.png'))

		# Generated animaged gif using results (rotating encompassing views)
		generate_gif(gif_dir, '', '', save_dir)

# render quantitative results
def render_quantitative_results():
	render_list, id_result = get_file_list(BASE_PATH)

	os.makedirs(TEST_PATH, exist_ok=True)

	for idx, obj_path in enumerate(render_list):
		print(f'[{idx + 1}/{len(render_list)}] Now rendering images for fid evaluation')
		
		scene = trimesh.load(obj_path, force='mesh')
		window_conf = gl.Config(double_buffer=True, depth_size=6)

		scene.vertices = np.dot(scene.vertices - scene.centroid, trimesh.transformations.rotation_matrix(90 * (math.pi / 180), direction=[0, 1, 0], point=[0, 0, 0])[:3, :3])
		center = scene.bounds.mean(axis=0)

		for i in range(0,18):
			scene.vertices = np.dot(scene.vertices, trimesh.transformations.rotation_matrix(10 * (math.pi / 180), direction=[0, 1, 0], point=center)[:3, :3])
			png = scene.scene().save_image(resolution=[500, 500], visible=True, window_conf=window_conf)

			image = Image.open(io.BytesIO(png))
			image.save(os.path.join(TEST_PATH, f'{id_result[idx]}_{i:02}.png'))

if __name__ == "__main__":
    # render_qualitative_results() # takes long time
	render_quantitative_results()