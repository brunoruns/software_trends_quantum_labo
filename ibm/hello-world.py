from qiskit_ibm_runtime import QiskitRuntimeService
# als je de code op een echte quantum wilt runnen, heb je wel account voor nodig en code vergt nog wat aanpassing

options = {
	'backend_name': 'ibmq_qasm_simulator'
}

runtime_inputs = {
	# Number of iterations to run.
	# Each iteration generates and runs
	# a random circuit.
	# 'iterations': 1 # integer
}

service = QiskitRuntimeService(
	channel='ibm_quantum'
)

job = service.run(
	program_id='hello-world',
	options=options,
	inputs=runtime_inputs,
	instance='ibm-q/open/main'
)

# Job id
print(job.job_id)
# See job status
print(job.status())

# Get results
result = job.result()