import logging
from qiskit.transpiler.basepasses import AnalysisPass
from qiskit.circuit.controlflow import ControlFlowOp
from qiskit.circuit import QuantumCircuit

logger = logging.getLogger(__name__)

class CollectResets(AnalysisPass):
    """
    An analysis pass to discover and record reset or stabilization 
    sub-operations across both flat and dynamic nested control flow blocks.
    """
    def __init__(self):
        super().__init__()

    def run(self, dag):
        """
        Processes the top-level DAG to extract instruction signatures recursively.
        """
        collected_resets = []

        def inspect_block(block, parent_global_indices):
            # If it's a QuantumCircuit (common in Qiskit 1.x front-end blocks), iterate its data
            if isinstance(block, QuantumCircuit):
                for inst, qargs, clargs in block.data:
                    # Map the block's local qubit index to the parent's global index footprint
                    local_indices = [block.find_bit(q).index for q in qargs]
                    global_indices = [parent_global_indices[idx] for idx in local_indices]

                    if inst.name == 'reset':
                        collected_resets.append(('standard_reset', global_indices))
                    elif inst.name == 'x':
                        collected_resets.append(('dynamic_stabilizer_x', global_indices))
                    elif isinstance(inst, ControlFlowOp):
                        for sub_block in inst.blocks:
                            inspect_block(sub_block, global_indices)
            else:
                # If it's already a DAGCircuit layer
                for node in block.op_nodes():
                    local_indices = [block.find_bit(q).index for q in node.qargs]
                    global_indices = [parent_global_indices[idx] for idx in local_indices]

                    if node.op.name == 'reset':
                        collected_resets.append(('standard_reset', global_indices))
                    elif node.op.name == 'x':
                        collected_resets.append(('dynamic_stabilizer_x', global_indices))
                    elif isinstance(node.op, ControlFlowOp):
                        for sub_block in node.op.blocks:
                            inspect_block(sub_block, global_indices)

        # Start processing from the top-level main DAG
        for node in dag.op_nodes():
            # Resolve the global layout indices for the top-level node
            top_global_indices = [dag.find_bit(q).index for q in node.qargs]

            if node.op.name == 'reset':
                collected_resets.append(('standard_reset', top_global_indices))
            elif node.op.name == 'x':
                collected_resets.append(('dynamic_stabilizer_x', top_global_indices))
            elif isinstance(node.op, ControlFlowOp):
                for sub_block in node.op.blocks:
                    # Recurse down, passing the parent node's global index footprint mapping
                    inspect_block(sub_block, top_global_indices)

        # Write results to the pass manager's centralized tracking dictionary
        self.property_set['collected_resets'] = collected_resets
