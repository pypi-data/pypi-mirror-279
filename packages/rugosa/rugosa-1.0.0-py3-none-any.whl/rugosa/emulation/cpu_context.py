"""
Interface for handling the context of emulation: registers, memory, variables, actions, etc.
"""
from __future__ import annotations

import warnings
from copy import deepcopy
import collections
import logging
from typing import List, Tuple, Optional, TYPE_CHECKING, Any

import dragodis
from dragodis import NotExistError

from . import utils
from .instruction import Instruction
from .memory import Memory
from .registers import RegisterMap
from .variables import VariableMap
from .operands import Operand, OperandLite
from .functions import FunctionSignature, FunctionArgument
from .objects import File, RegKey, Service, ObjectMap
from .actions import ActionList

if TYPE_CHECKING:
    from .emulator import Emulator

logger = logging.getLogger(__name__)


class JccContext:
    """
    Stores information pertaining to a Jcc instruction encountered when tracing.

    When a Jcc instruction is encountered, several pieces of information inherently need to be tracked since
    we are blindly taking every branch to ensure we get all possible data at any given address.  It turns out
    we need to know the target of the Jcc instruction for the condition as emulated
    (condition_target_ea).  We also need to know the value of the branch we would NOT have taken (at least as
    best of a guess as we can make in some cases) and where that value would have been set.  In order to
    calculate the value, we need to know what kind of test instruction was used, so that mnem is tracked as well.When
    we trace our condition_target_ea branch, we need not modify the context.  Whenever we trace the alternative branch,
    we'll need to modify the context as specified.
    """

    def __init__(self):
        self.condition_target_ea = None  # The branch actually taken
        self.alt_branch_data_dst = None  # The location which was tested (typically opnd 0 of the condition test)
        self.alt_branch_data = None  # The data stored in _alt_branc_data_dst
        self.flag_opnds = {}  # Dictionary containing the operands at a particular instruction which set
        # specific flags.  Dictionary is keyed on flag registery names.

    def __deepcopy__(self, memo):
        copy = JccContext()
        copy.condition_target_ea = self.condition_target_ea
        copy.alt_branch_data_dst = self.alt_branch_data_dst
        copy.alt_branch_data = self.alt_branch_data
        copy.flag_opnds = {flag: list(operands) for flag, operands in list(self.flag_opnds.items())}
        return copy

    def update_flag_opnds(self, flags, opnds):
        """
        Set the operands which last changed the specified flags.

        :param flags: list of flags which were modified utilizing the supplied opnds
        :param opnds: list of operands (instance of Operand) at the instruction which modified the flags
        """
        for flag in flags:
            # Converting Operand classes to OperandLite classes to help speed up deepcopies.
            self.flag_opnds[flag] = [OperandLite(opnd.ip, opnd.idx, opnd.text, opnd.value) for opnd in opnds]

    def get_flag_opnds(self, flags):
        """
        Extracts all the operands of for the list of flags and reduces the set.  However, since the operands
        need to remain in order, we can't use set operations.  In all actuality, assuming our code is correct and
        the compiler isn't doing something funky, any more than 1 flag should really just be a duplicate list.

        :param flags: list of flags for which to extract operands
        :return: list of operands which were utilized in the instruction that modified the requested flags
        """
        # TODO: Is there a better way to do this?
        operands = []
        for flag in flags:
            for operand in self.flag_opnds.get(flag, []):
                if operand not in operands:
                    operands.append(operand)

        return operands

    def is_alt_branch(self, ip) -> bool:
        """
        Test our IP against the branch information to determine if we are in the branch that would have been
        emulated or in the alternate branch.
        """
        return bool(self.condition_target_ea and self.condition_target_ea != ip)


class ProcessorContext:
    """
    Stores the context of the processor during execution.

    :param emulator: Instance of Emulator to use during emulation.
    :param registers: Instance of an initialized RegisterMap object used to store register values
        for the given architecture.
    :param instruction_pointer: Name of the register used to point to the current instruction
        being currently executed or to-be executed.
    :param stack_pointer: Name of the register used to hold the stack pointer.
    :param return_register: Name of the register used to return results from a function.
    """

    # Must be set by inherited classes.
    OPCODES = {}  # Map of opcode mnemonics to functions that emulate them.

    # Class used to generate instructions.
    _instruction_class = Instruction

    # Cache for keeping track of instructions and their operand indexes.
    _operand_indices = {}

    def __init__(
            self,
            emulator: Emulator,
            registers: RegisterMap,
            instruction_pointer: str,
            stack_pointer: str,
            return_register: str
    ):
        self.emulator = emulator
        self.registers = registers
        self.jcccontext = JccContext()
        self.memory = Memory(self)
        self.branch_history: list[tuple[int, bool]] = []  # Keeps track of branches and whether they are forced.
        self.call_history: list[tuple[int, str, tuple[str, Any]]] = []  # Keeps track of function calls.
        self.executed_instructions: list[int] = []  # Keeps track of the instructions that have been executed.
        # TODO: Should memory_copies be stored in Memory object?
        self.memory_copies = collections.defaultdict(list)  # Keeps track of memory moves.
        self.bitness = emulator.disassembler.bit_size
        self.byteness = self.bitness // 8
        self.byteorder = "big" if emulator.disassembler.is_big_endian else "little"
        self.variables = VariableMap(self)
        self.objects = ObjectMap(self)
        self.actions = ActionList()
        self.stdout = ""  # stores contents of stdout.

        # Function start address of a function we are currently hooking.
        self.hooking_call = None
        self._call_depth = 0

        self._sp = stack_pointer
        self._ip = instruction_pointer
        self._ret = return_register
        self._sp_start = self.sp

    def __deepcopy__(self, memo):
        """Implementing our own deepcopy to improve speed."""
        # Create class, but avoid calling __init__()
        # so we don't trigger the unnecessary initialization of Memory and JccContext
        klass = self.__class__
        copy = klass.__new__(klass)
        memo[id(self)] = copy

        copy.emulator = self.emulator  # This is a reference, don't create a new instance.
        copy.hooking_call = self.hooking_call
        copy.registers = deepcopy(self.registers, memo)
        copy.jcccontext = deepcopy(self.jcccontext, memo)
        copy.memory = deepcopy(self.memory, memo)
        copy.variables = deepcopy(self.variables, memo)
        copy.objects = deepcopy(self.objects, memo)
        copy.actions = deepcopy(self.actions, memo)
        copy.branch_history = list(self.branch_history)
        copy.call_history = list(self.call_history)
        copy.executed_instructions = list(self.executed_instructions)
        copy.memory_copies = self.memory_copies.copy()
        copy.stdout = self.stdout
        copy.bitness = self.bitness
        copy.byteness = self.byteness
        copy.byteorder = self.byteorder
        copy._call_depth = self._call_depth
        copy._sp = self._sp
        copy._ip = self._ip
        copy._ret = self._ret
        copy._sp_start = self._sp_start

        return copy

    def copy(self):
        return deepcopy(self)

    @property
    def ip(self) -> int:
        """Alias for retrieving instruction pointer."""
        return self.registers[self._ip]

    @ip.setter
    def ip(self, value):
        """Alias for setting instruction pointer."""
        self.registers[self._ip] = value

    @property
    def sp(self) -> int:
        """Alias for retrieving stack pointer."""
        return self.registers[self._sp]

    @sp.setter
    def sp(self, value):
        """Alias for setting stack pointer."""
        self.registers[self._sp] = value

    @property
    def sp_diff(self) -> int:
        """
        The difference between the current stack pointer and the
        stack pointer at the beginning of the function.

        This helps with debugging since this number should match the number
        shown in the IDA disassembly.
        """
        return self._sp_start - self.sp

    # TODO: A subroutine in ARM can technically pass in larger values, in which
    #   case the value spans multiple registers r0-r3
    @property
    def ret(self) -> int:
        """Alias for retrieving the return value."""
        return self.registers[self._ret]

    @ret.setter
    def ret(self, value):
        """Alias for setting return value."""
        logger.debug("Setting 0x%X into %s", value, self._ret)
        self.registers[self._ret] = value

    @property
    def prev_instruction(self):
        """That last instruction that was executed or None if no instructions have been executed."""
        if self.executed_instructions:
            return self.executed_instructions[-1]
        else:
            return None

    @property
    def forced_path(self) -> bool:
        """Whether the context path has a forced branch."""
        return any(forced for _, forced in self.branch_history)

    def execute(self, start=None, end=None, call_depth: int = 0, max_instructions: int = None) -> bool:
        """
        "Execute" the instruction at IP and store results in the context.
        The instruction pointer register will be set to the value supplied in .ip so that
        it is correct.

        :param start: instruction address to start execution (defaults to currently set ip)
        :param end: instruction to stop execution (not including)
            (defaults to only run start)
            Can also be an instruction mnemonic.
            Can also be a callable function which takes a context and instruction object.
        :param call_depth: Number of function calls we are allowed to emulate into.
            When we hit our limit (depth is 0), emulation will no longer jump into function calls.
            (Defaults to not emulating into any function calls.)
            NOTE: This does not affect call hooks.
        :param max_instructions: Maximum number of instructions to execute before
            raising an RuntimeError.
            Uses max_instructions set by emulator constructor if not provided.

        :returns: True if the given endpoint was hit.
        :raises RuntimeError: If maximum number of instructions get hit.
        """
        if max_instructions is None:
            max_instructions = self.emulator.max_instructions

        if not start:
            start = self.ip

        # Set instruction pointer to where we are currently executing.
        self.ip = start

        # Set current call depth.
        if call_depth < 0:
            raise ValueError(f"call_depth must be a positive number.")
        self._call_depth = call_depth

        # If end is provided, recursively run execute() until ip is end.
        if end is not None:
            if isinstance(end, str):
                if end == "ret":
                    end = lambda _, insn: insn.is_terminal
                else:
                    opcode = end
                    end = lambda _, insn: insn.mnem == opcode
            if isinstance(end, int):
                end_address = end
                end = lambda ctx, _: ctx.ip == end_address
            if not callable(end):
                raise ValueError(f"end must be an integer or callable function, got {type(end)}")
            count = max_instructions
            instruction = self.instruction
            while not end(self, instruction):
                if instruction.is_terminal:
                    return False  # TODO: Should we be executing the terminal instruction?
                instruction.execute()
                count -= 1
                if not count:
                    raise RuntimeError('Hit maximum number of instructions.')
                instruction = self.instruction
            return True
        else:
            self.instruction.execute()
            return True

    def _execute_call(self, func_address: int, func_name: str = None, call_address: int = None):
        """
        Executes the call to the given function.
        If a call hook has been provided, the hook will get run. Otherwise, instructions in the function
        will get emulated if set call_depth allows.

        :param func_address: Address of function to call.
        :param func_name: Name of the function (only required for name based call hook lookups)
        :param call_address: Address of call instruction (if available)
        """
        # Tell context that we are currently emulating a function hook.
        # This information is import for things like pulling out function arguments out correctly.
        self.hooking_call = func_address

        try:
            if not func_name:
                try:
                    func_name = self.emulator.disassembler.get_function_signature(func_address).name
                except NotExistError:
                    pass

            # See if we have a hook registered for this function.
            call_hook = self.emulator.get_call_hook(func_address)
            if not call_hook and func_name:
                call_hook = self.emulator.get_call_hook(func_name)
                if not call_hook:
                    # Try one more time with a sanitized name.
                    func_name = utils.sanitize_func_name(func_name)
                    call_hook = self.emulator.get_call_hook(func_name)

            num_args = None
            if call_hook and func_name and hasattr(call_hook, "num_args"):
                num_args = call_hook.num_args(func_name)

            # Report on function call and their arguments.
            arg_objs = self.get_function_args(func_address, num_args)
            self.call_history.append((call_address, func_name, [(arg.name, arg.value) for arg in arg_objs]))
            arg_values = [arg_obj.value for arg_obj in arg_objs]

            # Execute call hook if provided.
            if call_hook:
                try:
                    logger.debug(
                        "Emulating %s(%s)",
                        func_name,
                        ", ".join(f"{arg_obj.name}={hex(arg_obj.value)}" for arg_obj in arg_objs)
                    )
                    logger.debug("Running hook: %r", call_hook)
                    ret = call_hook(self, func_name, arg_values)
                    if ret is True:
                        ret = 1
                    elif ret is False:
                        ret = 0
                    # Set return value to rax
                    if ret is not None:
                        if not isinstance(ret, int):
                            raise TypeError(f"Invalid return type. Expected 'int' but got '{type(ret)}'")
                        self.ret = ret
                except RuntimeError:
                    raise  # Allow RuntimeError exceptions to be thrown.
                except Exception as e:
                    logger.debug("Failed to emulate builtin function: %s() with error: %s", func_name, e)

            # Otherwise, emulate the function instructions if set call_depth allows.
            elif self._call_depth:
                try:
                    func = self.emulator.disassembler.get_function(func_address)
                except NotExistError as e:
                    logger.warning("Failed to execute call at 0x%X : %s", func_address, e)
                    return
                call_depth = self._call_depth
                sp_start = self._sp_start
                try:
                    self.execute(start=func.start, end=func.end, call_depth=call_depth - 1)
                finally:
                    # Reset after we leave call.
                    self._call_depth = call_depth
                    self._sp_start = sp_start

        finally:
            self.hooking_call = None

    @property
    def func_calls(self) -> dict:
        warnings.warn(f".func_calls is deprecated. Please use .call_history instead.", DeprecationWarning)
        # Original .func_calls overwrote calls at the same instruction. So pulling the last one to replicate this logic.
        return {
            address: (func_name, [value for name, value in args])
            for address, func_name, args in self.call_history
        }

    def get_call_history(self, func_name_or_ea) -> List[Tuple[int, List]]:
        """
        Returns the call history for a specific function name.

        :returns: List of tuples containing: (ea of call, list of function arguments)
        """
        if isinstance(func_name_or_ea, str):
            func_name = func_name_or_ea
        else:
            ea = func_name_or_ea
            func_name = self.emulator.disassembler.get_function_signature(ea).name
        return [
            (address, [value for name, value in args])
            for address, _func_name, args in self.call_history
            if _func_name == func_name
        ]

    def prep_for_branch(self, bb_start_ea):
        """
        Modify this current context in preparation for a specific path.
        """
        forced = self.jcccontext.is_alt_branch(bb_start_ea)
        self.branch_history.append((bb_start_ea, forced))

        # Modify operands to make forced branch more valid.
        if forced:
            logger.debug("Modifying context for branch at 0x%08X", bb_start_ea)
            # Set the destination operand relative to the current context
            # to a valid value that makes this branch true.
            dst_opnd = self.jcccontext.alt_branch_data_dst
            dst_opnd = self.get_operands(ip=dst_opnd.ip)[dst_opnd.idx]
            dst_opnd.value = self.jcccontext.alt_branch_data

        self.jcccontext = JccContext()

    def get_instruction(self, ip=None) -> Instruction:
        """
        Gets the Instruction object for the current instruction pointed by the instruction pointer.

        :param ip: location of instruction pointer to pull Instruction from (default to current ip in context)
        :return: Instruction object
        """
        if ip is None:
            ip = self.ip
        return self._instruction_class(self, ip)

    @property
    def instruction(self) -> Instruction:
        return self.get_instruction()

    def get_operands(self, ip=None) -> List[Operand]:
        """
        Gets the Operand objects of all operands in the current instruction and returns them in a list.

        :param int ip: location of instruction pointer to pull operands from (defaults to current rip in context)

        :return: list of Operand objects
        """
        return self.get_instruction(ip=ip).operands

    @property
    def operands(self) -> List[Operand]:
        return self.get_operands()

    def get_pointer_history(self, ea):
        """
        Retrieves the history of a specific pointer.
        :param ea: Pointer to start with.
        :return: list of tuples containing (address of the memory copy, source pointer)
            - sorted by earliest to latest incarnation of the pointer. (not including itself)
        """
        history = []
        for ip, copies in sorted(list(self.memory_copies.items()), reverse=True):
            for src, dst, size in sorted(copies, reverse=True):
                if dst == ea:
                    history.append((ip, src))
                    ea = src
        history.reverse()
        return history

    def get_original_location(self, addr):
        """
        Retrieves the original location for a given address by looking through it's pointer history.

        :param addr: address of interest

        :return: a tuple containing:
            - instruction pointer where the original location was first copied
                or None if given address is already loaded or the original location could not be found.
            - either a loaded address, a tuple containing (frame_id, stack_offset) for a stack variable,
                or None if the original location could not be found.
        """
        # TODO: Consider refactoring.

        # Pull either the first seen loaded address or last seen stack variable.
        try:
            line = self.emulator.disassembler.get_line(addr)
            if not line.is_loaded:
                return None, addr
        except dragodis.NotExistError:
            return None, addr

        ip = None

        var = self.variables.get(addr, None)
        for ip, ea in reversed(self.get_pointer_history(addr)):
            try:
                line = self.emulator.disassembler.get_line(ea)
                if line.is_loaded:
                    return ip, ea
            except dragodis.NotExistError:
                pass
            var = self.variables.get(ea, var)

        if var and var.is_stack:
            # TODO: frame_id is an IDA specific thing. We are going to need to refactor this.
            #   - Perhaps have a "Variable" or "Data" object in dragodis?
            return ip, (var.frame_id, var.stack_offset)
        else:
            return ip, None

    def get_function_signature(
            self, func_ea: int = None, num_args: int = None, default_data_type: str = None
    ) -> Optional[FunctionSignature]:
        """
        Returns the function signature of the given func_ea with argument values pulled
        from this context.

        :param int func_ea: address of the function to pull signature from.
            The first operand is used if not provided. (helpful for a "call" instruction)
        :param int num_args: Force a specific number of arguments in the signature.
            If not provided, number of arguments is determined by the disassembler.
            Extra arguments not defined by the disassembler are assumed to be the default_data_type.
            Avoid using num_args and adjust the returned FunctionSignature manually
            if more customization is needed.

            WARNING: Setting the number of arguments will permanently change the
            signature on the backend disassembler.
        :param str default_data_type: The default data type to use when forcing extra arguments.
            (Defaults to "dword" for 32-bit or "qword" for 64-bit)

        :return: FunctionSignature object or None if not applicable

        :raises NotExistError: If a function signature could not be created from given ea.
        :raises ValueError: If num_args is negative
        """
        # If func_ea is not given, assume we are using the first operand from a call instruction.
        if not func_ea:
            if not self.operands:
                return None
            operand = self.operands[0]
            # function pointer can be a memory reference or immediate.
            func_ea = operand.addr or operand.value

        disassembler = self.emulator.disassembler
        signature = disassembler.get_function_signature(func_ea)
        signature = FunctionSignature(self, func_ea, signature)

        if num_args is not None:
            if num_args < 0:
                raise ValueError("num_args is negative")

            arguments = signature.arguments
            if len(arguments) > num_args:
                for _ in range(len(arguments) - num_args):
                    signature.remove_argument(-1)

            elif len(arguments) < num_args:
                if not default_data_type:
                    default_data_type = "qword" if self.bitness == 64 else "dword"
                for _ in range(num_args - len(arguments)):
                    signature.add_argument(default_data_type)

        return signature

    def get_function_args(
            self, func_ea: int = None, num_args: int = None, default_data_type: str = None
    ) -> List[FunctionArgument]:
        """
        Returns the FunctionArg objects for this context based on the
        given function.

        >>> cpu_context = ProcessorContext()
        >>> args = cpu_context.get_function_args(0x180011772)

        :param int func_ea: Ea of the function to pull a signature from.
        :param int num_args: Force a specific number of arguments.
            If not provided, number of arguments is determined by the disassembler.
            Extra arguments not defined by the disassembler are assumed to be 'int' type.
            Use get_function_signature() and adjust the FunctionSignature manually
            if more customization is needed.
            (NOTE: The function signature will be forced on failure if this is set.)
        :param str default_data_type: The default data type to use when forcing extra arguments.
            (Defaults to "dword" for 32-bit or "qword" for 64-bit)

        :returns: list of FunctionArg objects
        """
        func_sig = self.get_function_signature(func_ea, num_args=num_args, default_data_type=default_data_type)
        if not func_sig:
            return []

        return func_sig.arguments

    def get_function_arg_values(
            self, func_ea: int = None, num_args: int = None, default_data_type: str = None
    ) -> List[int]:
        """
        Returns the FunctionArg values for this context based on the given function.
        """
        return [arg.value for arg in self.get_function_args(func_ea=func_ea, num_args=num_args, default_data_type=default_data_type)]

    @property
    def function_args(self) -> List[FunctionArgument]:
        """
        The function arguments currently set based on the function in the first operand of the current instruction.
        """
        return self.get_function_args()

    @property
    def function_arg_values(self) -> List[int]:
        """
        The function argument values currently set based on the function in the first operand of the current instruction.
        """
        return self.get_function_arg_values()

    @property
    def passed_in_args(self) -> List[FunctionArgument]:
        """
        The function arguments for the current function.
        """
        func = self.emulator.disassembler.get_function(self.ip)
        return self.get_function_args(func.start)

    @property
    def files(self) -> List[File]:
        """
        All File objects in the current context.
        """
        return list(self.objects.query(File))

    @property
    def reg_keys(self) -> List[RegKey]:
        """
        The opened registry keys for this context.
        """
        return list(self.objects.query(RegKey))

    @property
    def services(self) -> List[Service]:
        """
        The created services for this context.
        """
        return list(self.objects.query(Service))
