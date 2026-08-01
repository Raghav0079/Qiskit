from qiskit.transpiler.basepasses import AnalysisPass
from qiskit.circuit import Reset


class CollectResets(AnalysisPass):
    """Custom analysis pass to track reset operations for dynamic circuits."""

    def __init__(self):
        super().__init__()

    def run(self, dag):
        # Scan DAG operation nodes for hardware resets using Qiskit 1.x syntax
        resets = [node for node in dag.op_nodes() if isinstance(node.op, Reset)]
        self.property_set["resets"] = resets
        return dag
