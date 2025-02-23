import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator  # Corrected import
from qiskit.visualization import plot_histogram

# Streamlit App Title
st.title("🔗 Blockchain Optimization using Quantum Algorithms")

# Sidebar: Number of Validators
num_validators = st.sidebar.slider("Number of Validators:", min_value=2, max_value=6, value=3)

# Define Stake Distribution (Randomized)
np.random.seed(42)
stakes = np.random.randint(1, 100, num_validators)  # Random stake values
normalized_stakes = stakes / np.sum(stakes)  # Normalize stakes to probabilities

# Display Stake Distribution
st.subheader("Validator Stakes (Higher Stake = Higher Selection Probability)")
for i, stake in enumerate(stakes):
    st.write(f"Validator {i+1}: {stake} tokens ({normalized_stakes[i]:.2%} probability)")

# Create Quantum Circuit for Weighted Selection
qc = QuantumCircuit(num_validators, num_validators)

# Apply Hadamard Gates to create equal superposition
qc.h(range(num_validators))

# Apply Amplitude Encoding for Stake Weighting
for i in range(num_validators):
    qc.p(2 * np.pi * normalized_stakes[i], i)  # Phase encoding stake influence

# Measure all qubits
qc.measure(range(num_validators), range(num_validators))

# Simulate Circuit Execution
try:
    backend = AerSimulator()  # Corrected backend initialization
    transpiled_circuit = transpile(qc, backend)
    result = backend.run(transpiled_circuit, shots=1024).result()
    counts = result.get_counts()
except Exception as e:
    st.error(f"Quantum Simulation Error: {e}")
    counts = {}

# Display Quantum Circuit
st.subheader("Quantum Circuit Representation")
fig = plt.figure()
qc.draw(output="mpl", filename="qc.png")  # Save as an image
img = plt.imread("qc.png")  # Read the image
st.image(img, caption="Quantum Circuit")

# Show Simulation Results
st.subheader("Validator Selection Probability (Quantum PoS)")
if counts:
    fig, ax = plt.subplots()
    plot_histogram(counts, ax=ax)
    st.pyplot(fig)
else:
    st.warning("No valid quantum results were generated.")

st.success("Quantum PoS Simulation Complete ✅")
