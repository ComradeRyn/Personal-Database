import subprocess
import os
import time

# Make sure the autograder is in the same directory as a1.c
FILE_NAME = "a1" # do not include extension
TESTCASE_DIR = "./testcases"
RESULTS_DIR = "./results"

def compile_program():
	compile_result = subprocess.run(["gcc", "-fsanitize=address", FILE_NAME+".c", "-o", FILE_NAME], capture_output=True, text=True)
	if compile_result.returncode != 0:
		print("Compilation failed:", compile_result.stderr)
		return False
	return True

def run_test_set(program, test_set, output_file):
	try:
		with open(output_file, 'w') as f_out:
			process = subprocess.Popen(program, stdin=subprocess.PIPE, stdout=f_out, stderr=f_out, text=True)
			time.sleep(0.05)
			for command in test_set:
				process.stdin.write(f"{command}\n")
				process.stdin.flush()
				time.sleep(0.05)
			process.communicate()
	except Exception as e:
		print(f"An error occurred while running {program} on {output_file}: {e}", flush=True)

def compare_outputs(solution_output, submission_output):
	with open(solution_output, 'r') as f_sol, open(submission_output, 'r') as f_sub:
		solution = f_sol.read().strip()
		try:
			submission = f_sub.read().strip()
		except:
			return False
		
		if solution.strip() != submission.strip():
			return False
		
		return True

def run_test(test_number, test_input, expected_output):
	process = subprocess.Popen(["./"+FILE_NAME, *(test_input.split(' '))], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
	stdout, stderr = process.communicate()

	print(f"Test Case {test_number}: Input = {test_input}", end=" ")

	if stdout.strip() == expected_output.strip() or stderr.strip() == expected_output.strip():
		print("✓ Passed")
		return True
	else:
		print("✗ Failed")
		print(f"   Expected: {expected_output}")
		print(f"   Got: {stdout.strip() if stdout != '' else stderr.strip()}")
		return False

def main():
	if not compile_program():
		return

	for test_case in sorted(os.listdir(TESTCASE_DIR)):
		if "solution" in test_case: continue

		print(f"Testing {test_case}...", end=" ")
		test_case_path = os.path.join(TESTCASE_DIR, test_case)
		with open(test_case_path, 'r') as f:
			test_set = [line.strip() for line in f]

		submission_output = os.path.join(RESULTS_DIR, f"{test_case[:-4]}_output.txt")
		solution_output = os.path.join(TESTCASE_DIR, f"solution_{test_case}")

		run_test_set("./"+FILE_NAME, test_set, submission_output)
		if compare_outputs(solution_output, submission_output):
			print("✓ Passed")
		else:
			print("✗ Failed")

if __name__ == "__main__":
	main()
