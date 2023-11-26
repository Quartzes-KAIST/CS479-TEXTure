import os

BASE_PATH = f'/root/CS479-TEXTure/experiments/normal'

def get_file_list(base_path):
	file_list = []
	
	dir_list = os.listdir(base_path)
	
	for dir in dir_list:
		file_list.append(base_path + "/" + dir + "/log.txt")
			
	return file_list

def find_execution_time():
	file_list = get_file_list(BASE_PATH)
	
	execution_time_list = []
	average_iteration_time_list = []
	
	for obj_path in file_list:
		with open(obj_path, 'r') as f:
			for line in f:
				if 'Execution time: ' in line:
					execution_time_list.append(float(line.split('Execution time: ')[-1].rstrip()))
				if 'Average iteration time: ' in line:
					average_iteration_time_list.append(float(line.split('Average iteration time: ')[-1].rstrip()))
					
	print(f'Average Execution Time: {sum(execution_time_list)/len(execution_time_list)}')
	print(f'Average Iteration Execution Time: {sum(average_iteration_time_list)/len(average_iteration_time_list)}')

if __name__ == "__main__":
	find_execution_time()