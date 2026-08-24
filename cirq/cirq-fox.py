import cirq

print("Cirq version:", cirq.__version__)

try:
    print(cirq.google.FoxtailV2)
except Exception as e:
    print(f"Error: {e}")