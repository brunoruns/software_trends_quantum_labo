import qiskit
from qiskit import ClassicalRegister, QuantumRegister, QuantumCircuit, transpile
from qiskit_aer import Aer
from configparser import RawConfigParser

type = 'real' # keuze om uit te voeren op een 'echte' quantum computer of een simulator
type = 'sim'

def run(program, type, shots = 1024):
  if type == 'real':
    if not run.isInit:
        # Setup the API key for the real quantum computer.
        parser = RawConfigParser()
        parser.read('config.ini')
        IBMQ.enable_account(parser.get('IBM', 'key'))
        run.isInit = True

    # Set backend server
    backend = qiskit.providers.ibmq.least_busy(qiskit.IBMQ.backends(simulator=False))

    # Uitvoeren op een quantum computer
    print("Running on", backend.name())
    job = qiskit.execute(program, backend)
    return job.result().get_counts()
  else:
    # Uitvoeren op een simulator
    print("Running on the simulator.")
    simulator = Aer.get_backend('qasm_simulator')
    transpiled_program = transpile(program, simulator)
    job = simulator.run(transpiled_program, shots=shots)
    return job.result().get_counts()

run.isInit = False

#
# Voorbeeld 1: Meet 2 qubits in hun initiele state, alles zeros.
#

# Setup qubits.
qr = QuantumRegister(2)
cr = ClassicalRegister(2)
program = QuantumCircuit(qr, cr);

# Meting (meten is een niet triviale actie !)
program.measure(qr, cr);

# Uitvoeren programma.
print(run(program, type))

#
# Voorbeeld 2: Creëer een Bell state (|00> + |11>), (|00> - |11>), (|01> + |10>), (|01> - |10>), dit zijn states met perfecte entanglement: 
# Entangle 2 qubits, met de eerste in superpositie (50% kans 0 , 50% kans 1) en meet het resultaat, dit zou 50% 00 en 50% 11 moeten zijn.
#

# Setup qubits.
qr = QuantumRegister(2)
cr = ClassicalRegister(2)
program = QuantumCircuit(qr, cr);

# Eerste qubit in superpositie brengen.
program.h(qr[0]) # Gebruik de Hadamard Gate

# Entangle de qubits met een  controlled NOT operator. Als de eerste qubit 1 is, wordt de tweede qubit geïnverteerd. 
# Afhankelijk van de intiele qubit states, geeft dit de 4 Bell States (|00> + |11>), (|00> - |11>), (|01> + |10>), (|01> - |10>).
program.cx(qr[0], qr[1])


# Meting: evenveel 00 en 11.
program.measure(qr, cr);

# Uitvoeren programma.
print(run(program, type))

#
# Voorbeeld 3: Superdense coding: stuur two classical bits van informatie  (01) terwijl we maar 1 qubit manipuleren: 

# Dit gaat door een Bell state ongedaan te maken: Entangle 2 qubits, met de eerste in superpositie, 
# Maak dan de stappen achteruit ongedaan.
# De eerste qubit is van Alice, de zender.
# De tweede qubit is van Bob, de ontvanger.
# Alice past haar qubit qr[0] aan om uiteindelijk 01 aan te geven aan Bob.
# Bob zal de qubit van Alice 'reverse' entangelen en uit superpositie halen en de resultaten meten, 
# en Bob zal dan  01 krijgen uit de qubits (zijn qubit zal in 1 wijzigen).

# Setup qubits.
qr = QuantumRegister(2)
cr = ClassicalRegister(2)
program = QuantumCircuit(qr, cr);

# Zender: Eerste qubit in superpositie brengen.
program.h(qr[0]) # Gebruik de Hadamard Gate

# Zender: Entangle de qubits met een  controlled NOT operator. Als de eerste qubit 1 is, wordt de tweede qubit geïnverteerd. 
program.cx(qr[0], qr[1])

# Verzender: Inverteer de eerste qubit om deze  van 0 naar 1 te zetten (remember, we willen 01 voorstellen met slechts manipulatie van de eertse qubit q[0]).
# 00  I  - identiteit, niets doen
# 01  Z  - program.z(qr[0])
# 10  X  - program.x(qr[0])
# 11  XZ - program.x(qr[0]) program.z(qr[0])
#program.x(qr[0])
program.x(qr[0]) #X is the invert operator, oftewel the not gate

# Ontvanger: Herhaal de controlled NOT operator, om de entanglement ongedaan te maken.
program.cx(qr[0], qr[1])

# Ontvanger: Herhaal de Hadamard, om de superposition state ongedaan te maken.
program.h(qr[0])

# Ontvanger: meet de waarde van de qubits, nu kunnen we de originele waardes terugkrijgen.
program.measure(qr, cr);

# Execute the program.
print(run(program, type))