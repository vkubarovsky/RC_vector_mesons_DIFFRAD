#!/bin/bash

# ==============================

# Usage:

# ./run_fortran.sh program_name input_file

# Example:

# ./run_fortran.sh mdiffrad inmdi.dat

# ==============================

set -e

# -------- Arguments --------

PROG="$1"
INPUT_FILE="$2"

if [ -z "$PROG" ] || [ -z "$INPUT_FILE" ]; then
echo "Usage: ./run_fortran.sh program_name input_file"
exit 1
fi

SRC="${PROG}.f"
EXE="${PROG}.exe"

# -------- Check files --------

if [ ! -f "$SRC" ]; then
echo "Error: source file $SRC not found"
exit 1
fi

if [ ! -f "$INPUT_FILE" ]; then
echo "Error: input file $INPUT_FILE not found"
exit 1
fi

# -------- Decide input name --------

LOWER=$(echo "$PROG" | tr '[:upper:]' '[:lower:]')

if [[ "$LOWER" == *"mdi"* ]]; then
TARGET_INPUT="inmdi.dat"
else
TARGET_INPUT="input.dat"
fi

echo "Using input file: $TARGET_INPUT"

# -------- Copy input --------

cp "$INPUT_FILE" "$TARGET_INPUT"

# -------- Compile --------

echo "Compiling $SRC ..."
echo "PROG = [$PROG]"
echo "SRC  = [$SRC]"
echo "EXE  = [$EXE]"

#gfortran -ffree-line-length-none -std=legacy -w -O2 "$SRC" -o "$EXE"
gfortran -ffree-line-length-none -std=legacy -w -O2 -fwrapv "$SRC" -o "$EXE"
# -------- Check compilation --------

if [ ! -f "$EXE" ]; then
echo "Compilation failed: executable not created"
exit 1
fi

echo "Compilation successful: $EXE"

# -------- Run --------

echo "Running $EXE ..."
echo "--------------------------------"

./"$EXE"

STATUS=$?

echo "--------------------------------"

if [ $STATUS -ne 0 ]; then
echo "Program exited with error code $STATUS"
exit 1
fi

echo "Run completed successfully"
