# -*- coding: utf-8 -*-
"""
main.py
--------
Entry point cua toan bo chuong trinh:

    doc file txt (data_loader)
        -> chay Banker's Algorithm (banker_algorithm)
        -> sinh giai thich (ai_explainer)
        -> in ra man hinh + luu bao cao JSON

Cach chay (dung tu thu muc goc cua du an):

    python3 src/main.py --input data/sample_state.txt --output outputs/report.json

Neu muon thu them ca kich ban "xin cap phat them tai nguyen" (Chuong 2):

    python3 src/main.py --input data/sample_state.txt --request "1,0,2,0"

  (nghia la: tien trinh P1 xin them 2 don vi tai nguyen B -> xem ket qua)
"""
import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from data_loader import load_state
from banker_algorithm import safety_algorithm, request_algorithm
from ai_explainer import explain_rule_based


def parse_request_arg(raw):
    """
    Doc chuoi dang "pid,r1,r2,...,rm" tu tham so --request thanh
    (pid:int, request:list[int]).
    """
    parts = [x.strip() for x in raw.split(",")]
    pid = int(parts[0])
    request = list(map(int, parts[1:]))
    return pid, request


def main():
    parser = argparse.ArgumentParser(description="Deadlock Safety Analyzer (Banker's Algorithm)")
    parser.add_argument("--input", default="data/sample_state.txt", help="File trang thai dau vao (.txt)")
    parser.add_argument("--output", default="outputs/report.json", help="File bao cao dau ra (.json)")
    parser.add_argument("--request", default=None, help='Tuy chon: "pid,r1,r2,...,rm" de mo phong xin cap them tai nguyen')
    args = parser.parse_args()

    data = load_state(args.input)

    is_safe, sequence, trace = safety_algorithm(data["available"], data["allocation"], data["need"])
    explanation = explain_rule_based(trace, is_safe)

    print("=" * 64)
    print(" PHAN TICH TRANG THAI HIEN TAI (Safety Algorithm)")
    print("=" * 64)
    print(explanation)

    report = {
        "input_file": args.input,
        "is_safe": is_safe,
        "safe_sequence": ["P%d" % p for p in sequence],
        "trace": trace,
        "explanation": explanation,
    }

    if args.request:
        pid, request = parse_request_arg(args.request)
        granted, new_state, reason = request_algorithm(
            pid, request, data["available"], data["allocation"], data["need"]
        )
        print("\n" + "=" * 64)
        print(" MO PHONG YEU CAU CAP THEM TAI NGUYEN: P%d xin %s" % (pid, request))
        print("=" * 64)
        print(("CHAP NHAN" if granted else "TU CHOI") + " - " + reason)
        if granted:
            print("Safe Sequence sau khi cap:", " -> ".join("P%d" % p for p in new_state["safe_sequence"]))

        report["request_simulation"] = {
            "process": "P%d" % pid,
            "request": request,
            "granted": granted,
            "reason": reason,
            "new_state": new_state,
        }

    out_dir = os.path.dirname(args.output)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    print("\nDa luu bao cao chi tiet tai:", args.output)


if __name__ == "__main__":
    main()
