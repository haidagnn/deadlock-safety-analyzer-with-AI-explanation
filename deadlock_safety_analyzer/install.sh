#!/bin/bash
# Cai dat moi truong cho du an Deadlock Safety Analyzer with AI Explanation
set -e

echo "Kiem tra Python..."
python3 --version

echo "Cai thu vien (tuy chon - chi can neu lam bieu do truc quan hoa)..."
pip install -r requirements.txt --break-system-packages 2>/dev/null || pip install -r requirements.txt

echo "Done."
echo ""
echo "Chay phan tich tren kich ban mau (Chuong 1):"
echo "  python3 src/main.py --input data/sample_state.txt --output outputs/report.json"
echo ""
echo "Chay them mo phong xin cap tai nguyen (Chuong 2, tuy chon):"
echo "  python3 src/main.py --input data/sample_state.txt --request \"1,1,0,0\""
echo ""
echo "Chay bo unit test doi chieu ground-truth:"
echo "  python3 -m unittest tests/test_banker.py -v"
