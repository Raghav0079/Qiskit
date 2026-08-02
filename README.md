# Qiskit

A collection of notebooks exploring [Qiskit](https://www.ibm.com/quantum/qiskit) fundamentals, transpilation, custom transpiler passes, and dynamic (mid-circuit-measurement) quantum circuits — including a small custom pass-manager plugin, `dynacir`, for collecting reset operations during transpilation.

## Project Type

Quantum computing / learning-and-research notebook collection — Python, built on Qiskit + Qiskit Aer. Not a packaged library; a working sandbox of notebooks plus one small local helper package (`dynacir`) imported directly by the notebooks.

## Project Structure

```
Qiskit/
├── dynacir/                          # Local helper package: custom transpiler passes
│   ├── __init__.py
│   └── dynacir_passes.py             # CollectResets (AnalysisPass) — tracks Reset ops in the DAG
│
├── installation.ipynb                # Environment setup walkthrough
├── intro.ipynb                       # Core Qiskit concepts — building & visualizing circuits
├── primitives.ipynb                  # Sampler / Estimator primitives
├── dynamic_circuits.ipynb            # Mid-circuit measurement, if_test, classical feed-forward
├── tfim_noise_dynamic_scaling.ipynb  # Noise-aware dynamic circuit scaling on a TFIM circuit
├── contributing.ipynb                # Notes on contributing to Qiskit
│
├── .gitignore
└── README.md
```

## Contents

| Notebook | Description |
|---|---|
| `installation.ipynb` | Setting up a Qiskit environment |
| `intro.ipynb` | Introductory Qiskit concepts — building and visualizing circuits |
| `primitives.ipynb` | Working with Qiskit's `Sampler`/`Estimator` primitives |
| `dynamic_circuits.ipynb` | Building and running dynamic circuits (mid-circuit measurement, classical feed-forward with `if_test`) |
| `tfim_noise_dynamic_scaling.ipynb` | Noise-aware dynamic circuit scaling experiments on a TFIM (Transverse-Field Ising Model) circuit |
| `contributing.ipynb` | Notes / walkthrough on contributing to Qiskit |

## `dynacir/`

A small local package containing custom transpiler passes used across the notebooks:

- **`CollectResets`** — an `AnalysisPass` that scans a circuit's DAG for `Reset` operations and stores them in the pass manager's `property_set["resets"]`, useful for analyzing and optimizing dynamic circuits that rely on qubit reuse via reset.

```python
from dynacir.dynacir_passes import CollectResets
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager

pm = generate_preset_pass_manager(optimization_level=3, backend=backend)
pm.optimization.append(CollectResets())

transpiled = pm.run(qc)
```

## Getting Started

### Prerequisites

- Python 3.11+
- [Qiskit](https://pypi.org/project/qiskit/) and [`qiskit-aer`](https://pypi.org/project/qiskit-aer/)
- Jupyter (to run the `.ipynb` notebooks)

### Installation

```bash
git clone https://github.com/Raghav0079/Qiskit.git
cd Qiskit
pip install qiskit qiskit-aer matplotlib jupyter
```

### Usage

Launch Jupyter and open any notebook:

```bash
jupyter notebook
```

Start with `installation.ipynb` and `intro.ipynb`, then move on to `primitives.ipynb` and `dynamic_circuits.ipynb` for more advanced topics.

## Notes

- Circuits are transpiled locally against `GenericBackendV2` targets (with `control_flow=True` where dynamic-circuit features like `if_test` are used), so notebooks run fully offline without needing IBM Quantum hardware access.
- Sampling is done via `qiskit_aer.primitives.SamplerV2`.

## Contributing

See `contributing.ipynb` for notes on contribution workflow. Issues and pull requests are welcome.

## License

No license specified yet — consider adding one (e.g. MIT/Apache-2.0) if you intend for others to reuse this code.
