#!/bin/bash
# ============================================================
# run_idiffrad.sh  --  Run idiffrad for all 3 vmax cuts
#
# Usage:  ./run_idiffrad.sh
#
# Produces:
#   result_nocut.txt   -- no cut on vmax
#   result_vmax20.txt  -- vmax = 2.0 GeV^2
#   result_vmax12.txt  -- vmax = 1.2 GeV^2
# ============================================================

set -e

if [ ! -f idiffrad.f ]; then
    echo "ERROR: idiffrad.f not found in current directory"
    exit 1
fi

echo "Compiling idiffrad.f ..."
gfortran -ffree-line-length-none -std=legacy -fwrapv -w -O2 idiffrad.f -o idiffrad.exe
echo "Compilation successful."
echo ""

run_case() {
    INPUT=$1
    OUTPUT=$2
    if [ ! -f "$INPUT" ]; then
        echo "WARNING: $INPUT not found, skipping."
        return
    fi
    echo "Running: $INPUT  -->  $OUTPUT"
    cp "$INPUT" input.dat
    ./idiffrad.exe > "$OUTPUT" 2>&1
    echo "  Done. Lines: $(wc -l < $OUTPUT)"
}

run_case input_nocut.dat  result_nocut.txt
run_case input_vmax20.dat result_vmax20.txt
run_case input_vmax12.dat result_vmax12.txt

echo ""
echo "All runs complete."
echo "Now run:"
echo "  python plot_idiffrad.py result_nocut.txt result_vmax20.txt result_vmax12.txt"
