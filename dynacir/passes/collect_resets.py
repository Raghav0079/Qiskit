from qiskit.transpiler.basepasses import AnalysisPass

class CollectResets(AnalysisPass):
    """A custom analysis pass to collect and track mid-circuit reset/measurement operations."""
    def __init__(self):
        super().__init__()
        self.resets = []

    def run(self, dag):
        self.resets.clear()
        for node in dag.op_nodes():
            if node.name == 'reset' or (node.name == 'measure' and getattr(node.op, 'condition', None) is not None):
                self.resets.append(node)
        self.property_set['collected_resets'] = self.resets
        return dag
