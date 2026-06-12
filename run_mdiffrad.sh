#!/bin/bash
# ============================================================
# run_mdiffrad.sh  --  Run mdiffrad for all 3 vmax cuts
#
# Usage:  ./run_mdiffrad.sh
#
# Produces:
#   mc_result_nocut.txt   -- no cut on vmax
#   mc_result_vmax20.txt  -- vmax = 2.0 GeV^2
#   mc_result_vmax12.txt  -- vmax = 1.2 GeV^2
# ============================================================

set -e

if [ ! -f mdiffrad.f ]; then
    echo "ERROR: mdiffrad.f not found in current directory"
    exit 1
fi

echo "Compiling mdiffrad.f ..."
gfortran -ffree-line-length-none -std=legacy -fwrapv -w -O2 mdiffrad.f -o mdiffrad.exe
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
    cp "$INPUT" inmdi.dat
    ./mdiffrad.exe > "$OUTPUT" 2>&1
    echo "  Done. Lines: $(wc -l < $OUTPUT)"
}

run_case hermes_nocut.dat  mc_result_nocut.txt
run_case hermes_vmax20.dat mc_result_vmax20.txt
run_case hermes_vmax12.dat mc_result_vmax12.txt

echo ""
echo "All runs complete."
echo "Now run:"
echo "  python plot_mdiffrad.py mc_result_nocut.txt mc_result_vmax20.txt mc_result_vmax12.txt"
