import re
import os

# 변경할 파일 경로들
batch_file_path = '~/join.bat'
ssh_config_path = '~/.ssh/config'

# 파일 경로에서 ~를 절대 경로로 변경
batch_file_path = os.path.expanduser(batch_file_path)
ssh_config_path = os.path.expanduser(ssh_config_path)

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

def update_ip_in_file(file_path, old_ip, new_ip):
	# 파일 읽기
	with open(file_path, 'r') as file:
		content = file.read()
	
	# IP 주소 대체
	new_content = re.sub(re.escape(old_ip), new_ip, content)

	# 파일 쓰기
	with open(file_path, 'w') as file:
		file.write(new_content)

# 사용자로부터 새로운 IP 입력 받기
new_ip = input('새로운 IP 주소를 입력하세요: ')

# 각 파일에서 예전 IP 주소 찾기
try:
	old_ip_batch = find_old_ip_in_file(batch_file_path)
	old_ip_ssh = find_old_ip_in_file(ssh_config_path)

	# 파일 업데이트
	update_ip_in_file(batch_file_path, old_ip_batch, new_ip)
	update_ip_in_file(ssh_config_path, old_ip_ssh, new_ip)

	print(f'IP 주소를 {old_ip_batch}에서 {new_ip}로 변경했어.')

except ValueError as e:
	print(e)
