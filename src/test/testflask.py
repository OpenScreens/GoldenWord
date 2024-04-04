import json
import subprocess
import sys

# pingpong = subprocess.Popen(
# 	[sys.executable, "/mnt/c/Users/gaspa/Desktop/BackFront/src/biz/ping-pong-http.py"]
# )

process = subprocess.Popen(
	[sys.executable, "/mnt/c/Users/gaspa/Desktop/BackFront/src/test/chattest.py"],
	stdout=subprocess.PIPE,
	stderr=subprocess.PIPE,
	text=True
)
process.wait()
stdout, stderr = process.communicate()

if process.returncode == 0:
	print("stdout:", stdout)
	last_line = stdout.strip().split('\n')[-1]
	last_line_json = json.loads(last_line.replace("'", '"'))
	test_values = last_line_json.values()

	if all(value == "pass" for value in test_values):
		print("All tests passed")
		#pingpong.terminate()
		exit(0)
	else:
		print("Not all tests passed")
		#pingpong.terminate()
		exit(1)
else:
	print("Error:", stderr)
	exit(1)
