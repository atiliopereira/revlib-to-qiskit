from qiskit import QuantumCircuit, QuantumRegister
from qiskit.circuit.library.standard_gates import SwapGate
from qiskit.quantum_info import Operator


def get_registers_sequence(instruction, registers):
    """
    Read a Revlib instruction and get positions of the registers in the instruction.
    :param instruction: RevLib format instruction string
    :param registers: list of all registers of the Qiskit circuit
    :returns a list of registers positions in the circuit that involved in the instruction

    """
    result = []
    for command in instruction[1:]:
        for i, register in enumerate(registers):
            if command == register.name:
                result.append(i)
    return result



def read_circuit(file):
    """
    Read a Revlib circuit file and create a Qiskit circuit objetc
    :param file: Revlib circuit file
    :returns a Qiskit circuit object 

    """
    with open(file, mode="r") as file:

        lines = []
        begin = end = 0
        variables = ''

        for index, line in enumerate(file):
            lines.append(line.split())
            if ".numvars" in line:
                numvars = int(line.split()[1])
            if ".variables" in line:
                variables = line.split()[1:]
            if ".inputs" in line:
                inputs = line.split()[1:]
            if ".outputs" in line:
                outputs = line.split()[1:]
            if ".constants" in line:
                constants = line.split()[1:]
            if ".garbage" in line:
                garbage = line.split()[1:]
            if ".begin" in line:
                begin = index
            if ".end" in line:
                end = index

        instructions = lines[begin+1:end]
        registers = [QuantumRegister(1, variable) for variable in variables]
        circ = QuantumCircuit(*registers)

        for instruction in instructions:
            #Toffoli Gates
            if "t" in instruction[0]:
                qubits = int(instruction[0][1:])
                if qubits == 1:
                    circ.x(*get_registers_sequence(instruction, registers))
                else:
                    circ.mcx(control_qubits=get_registers_sequence(instruction, registers)[:-1],
                            target_qubit=get_registers_sequence(instruction, registers)[-1])
            #Fredkin Gates
            elif "f" in instruction[0]:
                qubits = int(instruction[0][1:])
                if qubits == 2:
                    circ.swap(*get_registers_sequence(instruction, registers))
                else:
                    num_ctrl_qubits = len(instruction[3:])
                    controlled_fredkin_gate = SwapGate().control(num_ctrl_qubits)
                    regs = [registers[n] for n in get_registers_sequence(instruction, registers)]
                    circ.append(controlled_fredkin_gate, regs)

            #Peres Gates
            elif "p" in instruction[0]:
                cont = 1
                while cont < len(instruction[1:]):
                    circ.mcx(control_qubits=get_registers_sequence(instruction, registers)[:-cont],
                            target_qubit=get_registers_sequence(instruction, registers)[-cont])
                    cont += 1

            #Controlled-V
            elif "v" == instruction[0]:
                v_gate = Operator([[complex(0.5, 0.5), complex(0.5, -0.5)], [complex(0.5, -0.5), complex(0.5, 0.5)]])
                qc = QuantumCircuit(1, name="v")
                num_ctrl_qubits = len(instruction[2:])
                qc.unitary(v_gate, 0, label='v')
                cv_gate = qc.to_gate().control(num_ctrl_qubits)
                regs = [registers[n] for n in get_registers_sequence(instruction, registers)]
                circ.append(cv_gate, regs)

            #Controlled-V+
            elif "v+" == instruction[0]:
                vdg_gate = Operator([[complex(0.5, -0.5), complex(0.5, 0.5)], [complex(0.5, 0.5), complex(0.5, -0.5)]])
                qc = QuantumCircuit(1, name="v+")
                num_ctrl_qubits = len(instruction[2:])
                qc.unitary(vdg_gate, 0, label='v+')
                cvdg_gate = qc.to_gate().control(num_ctrl_qubits)
                regs = [registers[n] for n in get_registers_sequence(instruction, registers)]
                circ.append(cvdg_gate, regs)
            else:
                print(f'Instruction {instruction} not processed')

        return circ
