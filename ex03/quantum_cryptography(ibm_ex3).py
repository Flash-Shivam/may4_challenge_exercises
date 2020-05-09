%matplotlib inline

# Importing standard Qiskit libraries
import random
from qiskit import execute, Aer, IBMQ, QuantumCircuit
from qiskit.tools.jupyter import *
from qiskit.visualization import *
from may4_challenge.ex3 import alice_prepare_qubit, check_bits, check_key, check_decrypted, show_message
from may4_challenge.ex1 import return_state, vec_in_braket, statevec
# Configuring account
provider = IBMQ.load_account()
backend = provider.get_backend('ibmq_qasm_simulator')  # with this simulator it wouldn't work \

# Initial setup
random.seed(84) # do not change this seed, otherwise you will get a different key

# This is your 'random' bit string that determines your bases
numqubits = 100
bob_bases = str('{0:0100b}'.format(random.getrandbits(numqubits)))
encode = []
def bb84():
    print('Bob\'s bases:', bob_bases)

    # Now Alice will send her bits one by one...
    all_qubit_circuits = []
    for qubit_index in range(numqubits):

        # This is Alice creating the qubit
        thisqubit_circuit = alice_prepare_qubit(qubit_index)

        # This is Bob finishing the protocol below
        bob_measure_qubit(bob_bases, qubit_index, thisqubit_circuit)

        # We collect all these circuits and put them in an array
        all_qubit_circuits.append(thisqubit_circuit)

    # Now execute all the circuits for each qubit
    results = execute(all_qubit_circuits, backend=backend, shots=1).result()

    # And combine the results
    bits = ''
    for qubit_index in range(numqubits):
        bits += [measurement for measurement in results.get_counts(qubit_index)][0]

    return bits

# Here is your task
def bob_measure_qubit(bob_bases, qubit_index, qubit_circuit):
    #
    x = bob_bases[qubit_index]
    qc1 = QuantumCircuit(1)
    qc1.h(0)
    state1 = statevec(qc1)
    qc2 = QuantumCircuit(1)
    qc2.x(0)
    qc2.h(0)
    state2 = statevec(qc2)
    qc3 = QuantumCircuit(1)
    state3 = statevec(qc3)
    qc4 = QuantumCircuit(1)
    qc4.x(0)
    state4 = statevec(qc4)
    state5 = statevec(qubit_circuit)
    var = -1
    if state5 == state4:
        var = 4
    elif state5 == state3:
        var = 3
    elif state5 == state2:
        var = 2
    elif state5 == state1:
        var = 1
    #qubit_circuit.measure(0,0)
    encode.append(var)
    #print(var, x, qubit_index)
    if var == 1 and x == '1':
        qubit_circuit.h(0)
    elif var == 2 and x == '1':
        qubit_circuit.h(0)

    qubit_circuit.measure(0,0)

    #print(qubit_circuit)
    #for i in range(0,len(qubit_circuitit)):

    #
    # insert your code here to measure Alice's bits
    #
    #
    ...

bits = bb84()
print('Bob\'s bits: ', bits)
print(encode)
check_bits(bits)

'''
Bob's bases: 1100111010011111111111110100000111010100100010011001001110100001010010111011010001011001111111011111
Bob's bits:  1000001000011100001110100010000111100101000011100101000100000111000010001100010111000001001001000001
[2, 3, 3, 3, 3, 3, 4, 3, 3, 3, 3, 2, 4, 4, 3, 1, 1, 1, 2, 2, 2, 1, 4, 3, 1, 1, 4, 2, 2, 3, 3, 2, 4, 2, 4, 3, 3, 2, 1, 2, 1, 1, 3, 1, 4, 4, 1, 1, 3, 1, 1, 2, 2, 1, 1, 4, 3, 3, 1, 2, 3, 4, 4, 4, 3, 1, 2, 3, 4, 3, 3, 3, 2, 4, 3, 1, 1, 4, 3, 4, 1, 2, 1, 3, 3, 1, 1, 2, 3, 1, 4, 3, 1, 4, 3, 3, 3, 1, 1, 4]
So far, so good 🎉! You got the right bits!
'''

alice_bases = '10000000000100011111110011011001010001111101001101111110001100000110000010011000111'\
              '00111010010000110' # Alice's bases bits
#
#
# insert your code here to extract the key
print(encode)
key = ""
for i in range(0,len(alice_bases)):
    if (encode[i] == 1 and alice_bases[i] == '1') or (encode[i] == 3 and alice_bases[i] == '0'):
        bit1 = '0'
    else:
        bit1 = '1'

    if bit1 == bits[i] and bob_bases[i] == alice_bases[i]:
        key += bit1

print(key)
#
#
check_key(key)

'''
[2, 3, 3, 3, 3, 3, 4, 3, 3, 3, 3, 2, 4, 4, 3, 1, 1, 1, 2, 2, 2, 1, 4, 3, 1, 1, 4, 2, 2, 3, 3, 2, 4, 2, 4, 3, 3, 2, 1, 2, 1, 1, 3, 1, 4, 4, 1, 1, 3, 1, 1, 2, 2, 1, 1, 4, 3, 3, 1, 2, 3, 4, 4, 4, 3, 1, 2, 3, 4, 3, 3, 3, 2, 4, 3, 1, 1, 4, 3, 4, 1, 2, 1, 3, 3, 1, 1, 2, 3, 1, 4, 3, 1, 4, 3, 3, 3, 1, 1, 4]
10000010001110010011101001010000110000110011100000
So far, so good 🎉! You got the right key!
'''

m = '0011011010100011101000001100010000001000011000101110110111100111111110001111100011100101011010111010111010001'\
    '1101010010111111100101000011010011011011011101111010111000101111111001010101001100101111011' # encrypted message
#
decrypted = ""
p = len(key)
for i in range(0,len(m)):
    #p = int(i%m)
    message_bit = int(key[i%p])^int(m[i])
    decrypted += str(message_bit)
    #print(message_bit)

print(decrypted)
#
# insert your code here to decrypt the message
#
#
check_decrypted(decrypted)

'''
10110100100110101001101010010100110010110101101011001101011010011011011001101100110101011010010110100110101011010011011001011001101011011001010101011001101101011001010110010110011010011001010110011011
So far, so good 🎉! You decrypted the message!
'''

MORSE_CODE_DICT = { 'a':'.-', 'b':'-...',
                    'c':'-.-.', 'd':'-..', 'e':'.',
                    'f':'..-.', 'g':'--.', 'h':'....',
                    'i':'..', 'j':'.---', 'k':'-.-',
                    'l':'.-..', 'm':'--', 'n':'-.',
                    'o':'---', 'p':'.--.', 'q':'--.-',
                    'r':'.-.', 's':'...', 't':'-',
                    'u':'..-', 'v':'...-', 'w':'.--',
                    'x':'-..-', 'y':'-.--', 'z':'--..',
                    '1':'.----', '2':'..---', '3':'...--',
                    '4':'....-', '5':'.....', '6':'-....',
                    '7':'--...', '8':'---..', '9':'----.',
                    '0':'-----', ', ':'--..--', '.':'.-.-.-',
                    '?':'..--..', '/':'-..-.', '-':'-....-',
                    '(':'-.--.', ')':'-.--.-'}
#
#
# insert your code here to decode Alice's Morse code
inv_map = {v: k for k, v in MORSE_CODE_DICT.items()}
prev = ""
morse_coded_message = ""
for i in range(0,len(decrypted)):
    curr = decrypted[i]
    if prev == "1" and curr == "1":
        morse_coded_message += '-'
        prev = ""
    elif prev == "1" and curr == "0":
        morse_coded_message += '.'
        prev = "0"
    elif prev == "":
        prev = curr
    elif prev == "0" and curr == "1":
        morse_coded_message += ""
        prev = "1"
    elif prev == "0" and curr == "0":
        prev = "00"
    elif prev == "00" and curr == "0":
        morse_coded_message += "  "
        prev = ""
    elif prev == "00" and curr == "1":
        morse_coded_message += " "
        prev = "1"

#print(morse_coded_message)
solution = ""
res = ""
for i in range(0,len(morse_coded_message)):
    curr = morse_coded_message[i]
    if curr != " ":
        res += curr
    elif res != "" and curr == " ":
        solution += inv_map[res] + curr
        res = ""
    elif res == "" and curr == " ":
        solution += curr

if res != "":
        solution += inv_map[res]

print(solution)
#
#
show_message(solution)


'''
r e d d i t . c o m / r / m a y 4 q u a n t u m
Congratulations 🎉! Submit the following text r e d d i t . c o m / r / m a y 4 q u a n t u m on the IBM Quantum Challenge page to see if you are correct.
'''
