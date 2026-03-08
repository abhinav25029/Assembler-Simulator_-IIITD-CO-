RISC-V Assembler & Simulator (RV32I)

Overview

This project implements a custom Assembler and Simulator for a subset of the RV32I (RISC-V 32-bit integer) instruction set.
The goal of the project is to demonstrate the complete workflow of converting RISC-V assembly instructions into binary machine code and then executing those instructions using a simulator.

The assembler reads an assembly program, validates the syntax, handles labels and immediates, and produces 32-bit binary instructions.
The simulator then reads these binary instructions and simulates their execution by updating registers, program counter (PC), and memory.

Components

SimpleAssembler

 =>Converts RISC-V assembly instructions into 32-bit binary machine code.

 =>Handles instruction parsing, label resolution, and error detection.

AutomatedTesting

 =>Contains test cases and scripts used to verify correctness of the assembler and simulator implementations.


Features

Converts assembly instructions into 32-bit binary encoding
Handles labels and PC-relative addressing
Detects syntax errors and invalid instructions
Simulates execution with register and memory updates


Group Members
Lakshay Kathuria 2025290
Dhruv Kaushik	2025184
Abhinav Saini	2025029
Dhruv Chauhan	2025183
