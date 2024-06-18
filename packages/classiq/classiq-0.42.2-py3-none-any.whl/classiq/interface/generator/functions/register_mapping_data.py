from __future__ import annotations

import itertools
from typing import Any, Dict, Iterable, List, Tuple

import pydantic

from classiq.interface.generator.functions.register import Register, get_register_names
from classiq.interface.generator.register_role import RegisterRole as Role
from classiq.interface.helpers.custom_pydantic_types import PydanticNonEmptyString

from classiq.exceptions import ClassiqValueError

REGISTER_NOT_FOUND_ERROR = "Register name not found"


class RegisterMappingData(pydantic.BaseModel):
    input_registers: List[Register] = pydantic.Field(default_factory=list)
    output_registers: List[Register] = pydantic.Field(default_factory=list)
    zero_input_registers: List[Register] = pydantic.Field(default_factory=list)

    @pydantic.root_validator()
    def validate_mapping(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        input_registers = values.get("input_registers", list())
        output_registers = values.get("output_registers", list())
        zero_input_registers = values.get("zero_input_registers", list())

        input_qubits = cls._get_qubit_range(input_registers)
        output_qubits = cls._get_qubit_range(output_registers)
        zero_input_qubits = cls._get_qubit_range(zero_input_registers)

        all_input_qubits = sorted(input_qubits + zero_input_qubits)
        if not cls._validate_no_overlap(all_input_qubits):
            raise ClassiqValueError("overlapping input qubits are not allowed")
        if not cls._validate_no_overlap(output_qubits):
            raise ClassiqValueError("overlapping output qubits are not allowed")

        if not output_qubits == all_input_qubits:
            raise ClassiqValueError(
                "output registers should be included within the input / zero input registers"
            )

        return values

    @pydantic.validator("input_registers", "output_registers")
    def validate_input_registers_are_distinct(
        cls, field_value: List[Register]
    ) -> List[Register]:
        if len(field_value) != len({io_register.name for io_register in field_value}):
            raise ClassiqValueError(
                "The names of PortDirection registers must be distinct."
            )
        return field_value

    @staticmethod
    def _validate_no_overlap(reg_list: List[int]) -> bool:
        return len(reg_list) == len(set(reg_list))

    @staticmethod
    def _get_qubit_range(registers: Iterable[Register]) -> List[int]:
        return sorted(itertools.chain.from_iterable(reg.qubits for reg in registers))

    @property
    def input_names(self) -> Iterable[str]:
        return get_register_names(self.input_registers)

    @property
    def output_names(self) -> Iterable[str]:
        return get_register_names(self.output_registers)

    def validate_equal_mappings(self, other: RegisterMappingData) -> None:
        if any(
            [
                self.input_registers != other.input_registers,
                self.output_registers != other.output_registers,
                self.zero_input_registers != other.zero_input_registers,
            ]
        ):
            raise ClassiqValueError(
                "Interface should be identical in all implementations"
            )

    def get_input_register(self, name: PydanticNonEmptyString) -> Register:
        for reg in self.input_registers:
            if reg.name == name:
                return reg
        raise ClassiqValueError(REGISTER_NOT_FOUND_ERROR)

    def get_output_register(self, name: PydanticNonEmptyString) -> Register:
        for reg in self.output_registers:
            if reg.name == name:
                return reg
        raise ClassiqValueError(REGISTER_NOT_FOUND_ERROR)

    @staticmethod
    def from_registers_dict(
        regs_dict: Dict[Role, Tuple[Register, ...]]
    ) -> RegisterMappingData:
        return RegisterMappingData(
            input_registers=list(regs_dict[Role.INPUT]),
            output_registers=list(regs_dict[Role.OUTPUT]),
            zero_input_registers=list(regs_dict[Role.ZERO_INPUT]),
        )

    class Config:
        extra = "forbid"
