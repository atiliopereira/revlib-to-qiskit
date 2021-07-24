# revlib-to-qiskit
Convert a circuit in RevLib format to a Qiskit circuit object.

This program is intended to be used for benchmarks and test algorithms in IBM QX architecture Quantum computers. 

It is based in RevLib Version 2.0.1 – May 23, 2011.

You can find a list of RevLib resources here: http://www.revlib.org


## Requirements

- Python 3.6+
- Qiskit 0.26.2
- Matplotlib 3.4.1
- Pillow 8.2.0 
- Jupyter 1.0.0

## Install
```
git clone https://github.com/atiliopereira/revlib-to-qiskit
cd revlib-to-qiskit
python3 -m venv env
source env/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```
## Use
- Copy a RevLib file (.real) in the resources folder
- Open the test.ipynb file, it is a Jupyter notebook to test the program
- Change the name of the file, for the one you want to test
- Running the steps, it will plot the circuit created


Feel free to add or modify anything sending a pull request.
