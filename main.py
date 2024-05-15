import re
import os

# 파일 경로들을 읽어오는 함수
def read_file_list(file_list_path):
	if not os.path.exists(file_list_path):
		print(f'{file_list_path} 파일이 존재하지 않아. 파일을 생성할게.')
		with open(file_list_path, 'w') as file:
			pass
		print(f'{file_list_path} 파일이 생성됐어. 파일 경로를 추가해줘.')
		return []

	try:
		with open(file_list_path, 'r') as file:
			file_paths = [line.strip() for line in file]
		if not file_paths:
			print(f'{file_list_path} 파일이 비어 있어. 파일 경로를 추가해줘.')
		return file_paths
	except FileNotFoundError:
		print(f'{file_list_path} 파일이 존재하지 않아.')
		return []

def find_old_ip_in_file(file_path):
	# 파일 읽기
	with open(file_path, 'r') as file:
			content = file.read()
	
	# IP 주소 찾기 (IPv4 주소 패턴 사용)
	ip_pattern = re.compile(r'(\d{1,3}\.){3}\d{1,3}')
	match = ip_pattern.search(content)
	
	if match:
			return match.group()
	else:
			raise ValueError(f'파일 {file_path}에서 유효한 IP 주소를 찾을 수 없어.')

def is_valid_ip(ip):
	# IP 주소 유효성 검사 (IPv4 형식)
	ip_pattern = re.compile(r'^(\d{1,3}\.){3}\d{1,3}$')
	return ip_pattern.match(ip) is not None

def update_ip_in_file(file_path, old_ip, new_ip):
	# 파일 읽기
	with open(file_path, 'r') as file:
			content = file.read()
	
	# IP 주소 대체
	new_content = re.sub(re.escape(old_ip), new_ip, content)

	# 파일 쓰기
	with open(file_path, 'w') as file:
			file.write(new_content)

file_paths = read_file_list("file_list")

if not file_paths:
	exit()

# 사용자로부터 새로운 IP 입력 받기
while True:
	new_ip = input('새로운 IP 주소를 입력해봐: ')
	if is_valid_ip(new_ip):
			break
	else:
			print('이상한 IP 주소야. 다시 입력해봐.')

# 각 파일에서 예전 IP 주소 찾기
try:
	for file_path in file_paths:
		full_path = os.path.expanduser(file_path)
		old_ip = find_old_ip_in_file(full_path)
		update_ip_in_file(full_path, old_ip, new_ip)
		print(f'{file_path} 파일의 IP 주소를 {old_ip}에서 {new_ip}로 변경했어.')

except ValueError as e:
	print(e)
