from copy import deepcopy
from typing import Dict
from collections import defaultdict


class IntCode:
    def __init__(self, addresses: Dict):
        self.addr = defaultdict(lambda: 0)
        self.addr.update(addresses)

        self.program = deepcopy(self.addr)
        self.ops = {1: 3, 2: 3, 99: 0, 3: 1, 4: 1, 5: 2, 6: 2, 7: 3, 8: 3, 9: 1} # opcode -> n_params
        self.outs = []
        self.inputs = []
        self.is_halted = False
        self.pointer = 0
        self.rel_base = 0
        self.count = 0

    def get_op_mode_params(self, i):
        val = self.addr[i]
        op = val % 100
        assert op in self.ops, f"Wrong opcode: {op}"
        n_params = self.ops[op]

        modes = [int(x) for x in list(reversed(str(val)[:-2]))[:n_params]]
        while len(modes) < n_params:
            modes.append(0)

        params = [self.addr[x] for x in range(i + 1, i + 1 + n_params)]
        return op, modes, params

    def get_param_mode_val(self, mode, val):
        if mode == 0:
            return self.addr[val]
        elif mode == 1:
            return val
        elif mode == 2:
            return self.addr[val + self.rel_base]

    def run(self):
        while True:
            jump = None
            op, modes, params = self.get_op_mode_params(self.pointer)
            updated_params = [self.get_param_mode_val(mode, param) for mode, param in zip(modes, params)]

            if op == 1:
                target_addr = params[-1] if modes[-1] == 0 else params[-1] + self.rel_base

                assert modes[-1] in {0, 2}
                self.addr[target_addr] = updated_params[0] + updated_params[1]
            elif op == 2:
                assert modes[-1] in {0, 2}
                target_addr = params[-1] if modes[-1] == 0 else params[-1] + self.rel_base

                assert modes[-1] in {0, 2}
                self.addr[target_addr] = updated_params[0] * updated_params[1]
            elif op == 3:
                assert modes[-1] in {0, 2}
                if not self.inputs:
                    return
                else:
                    target_addr = params[-1] if modes[-1] == 0 else params[-1] + self.rel_base
                    self.addr[target_addr] = self.inputs.pop(0)
            elif op == 4:
                self.outs.append(updated_params[-1])
            elif op == 5:
                if updated_params[0] != 0:
                    jump = updated_params[-1]
            elif op == 6:
                if updated_params[0] == 0:
                    jump = updated_params[-1]
            elif op == 7:
                assert modes[-1] in {0, 2}
                target_addr = params[-1] if modes[-1] == 0 else params[-1] + self.rel_base
                if updated_params[0] < updated_params[1]:
                    self.addr[target_addr] = 1
                else:
                    self.addr[target_addr] = 0
            elif op == 8:
                assert modes[-1] in {0, 2}
                target_addr = params[-1] if modes[-1] == 0 else params[-1] + self.rel_base
                if updated_params[0] == updated_params[1]:
                    self.addr[target_addr] = 1
                else:
                    self.addr[target_addr] = 0
            elif op == 9:
                self.rel_base += updated_params[-1]
            elif op == 99:
                self.is_halted = True
                return
            else:
                raise Exception("Wrong Operation Code")

            if jump is not None:
                self.pointer = jump
            else:
                self.pointer += len(params) + 1

    def add_input(self, inp):
        if inp:
            try:
                _ = iter(inp)
                self.inputs.append([val for val in inp if val is not None])
            except TypeError as err:
                self.inputs.append(inp)

