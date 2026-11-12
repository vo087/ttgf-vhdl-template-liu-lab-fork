# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles, Timer, RisingEdge, FallingEdge
from cocotb.handle import HierarchyObject, LogicObject, LogicArrayObject

from typing import cast


class ProjectDUT:
    """Statically typed interface to the project HDL."""

    def __init__(self, dut: HierarchyObject) -> None:
        # 8-bit input ports
        self.ui_in: LogicArrayObject = cast(LogicArrayObject, dut.ui_in)
        self.uio_in: LogicArrayObject = cast(LogicArrayObject, dut.uio_in)

        # 8-bit output ports
        self.uo_out: LogicArrayObject = cast(LogicArrayObject, dut.uo_out)
        self.uio_out: LogicArrayObject = cast(LogicArrayObject, dut.uio_out)
        self.uio_oe: LogicArrayObject = cast(LogicArrayObject, dut.uio_oe)

        # Single-bit input ports
        self.ena: LogicObject = cast(LogicObject, dut.ena)
        self.clk: LogicObject = cast(LogicObject, dut.clk)
        self.rst_n: LogicObject = cast(LogicObject, dut.rst_n)

        # Simulator logger
        self.log = dut._log.info

@cocotb.test()
async def test_project(raw_dut : HierarchyObject) -> None:
    dut = ProjectDUT(raw_dut)
    dut.log("Start")

    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 10, unit="us")
    cocotb.start_soon(clock.start())

    # Reset
    dut.log("Reset")
    dut.ena.value = 1
    dut.ui_in.value = 1
    dut.uio_in.value = 1
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 10)
    dut.rst_n.value = 1

    dut.log("Test project behavior")

    # Set the input values you want to test
    #dut.ui_in.value = 144
    #dut.uio_in.value = 12

    for denum in range(1, 2**8):
        try:
            dut.ui_in.value = denum
            # Wait for one clock cycle to see the output values
            await ClockCycles(dut.clk, 10)

            ans = dut.uo_out.value
            if 256//denum != ans and round(256/denum) != ans :
                print("was not equal at,  ", ans, "    256//denum =", 256//denum)
        except:
            print("Could not divide with, ", denum)
            dut.ui_in.value = 1


    # The following assersion is just an example of how to check the output values.
    # Change it to match the actual expected output of your module:
    #assert dut.uo_out.value == 2
    # Keep testing the module by changing the input values, waiting for
    # one or more clock cycles, and asserting the expected output values.
