# -*- coding: utf-8 -*-
"""
data_loader.py
----------------
Doc file cau hinh dang .txt va tra ve cac ma tran dau vao cho thuat toan Banker.

DINH DANG FILE DAU VAO (vi du: data/sample_state.txt)
------------------------------------------------------
    5 3                <- dong 1: n (so tien trinh)  m (so loai tai nguyen)
    3 3 2               <- dong 2: Available (m so)
    7 5 3                \
    3 2 2                 \
    9 0 2                  }  n dong tiep theo: ma tran Max (n x m)
    2 2 2                 /
    4 3 3                /
    0 1 0                \
    2 0 0                 \
    3 0 2                  }  n dong tiep theo: ma tran Allocation (n x m)
    2 1 1                 /
    0 0 2                /

Need duoc TINH TU DONG, khong doc tu file, theo dung cong thuc bat bien:
    Need[i][j] = Max[i][j] - Allocation[i][j]
(day chinh la diem "Data Loader" ma tai lieu Chuong 1 nhac toi truoc khi
sang thuat toan loi o Chuong 2)
"""


def load_state(filepath):
    """
    Doc file tai `filepath` va tra ve 1 dict gom:
        n, m, available, max, allocation, need
    """
    with open(filepath, "r") as f:
        # bo qua dong trong / dong comment (bat dau bang '#') cho de mo rong sau nay
        lines = [ln.strip() for ln in f if ln.strip() != "" and not ln.strip().startswith("#")]

    pos = 0

    # Dong 1: n m
    n, m = map(int, lines[pos].split())
    pos += 1

    # Dong 2: Available
    available = list(map(int, lines[pos].split()))
    pos += 1
    if len(available) != m:
        raise ValueError("So phan tu Available (%d) khong khop m (%d)" % (len(available), m))

    # n dong tiep theo: Max
    max_matrix = []
    for i in range(n):
        row = list(map(int, lines[pos].split()))
        if len(row) != m:
            raise ValueError("Dong Max cua P%d khong du %d cot" % (i, m))
        max_matrix.append(row)
        pos += 1

    # n dong tiep theo: Allocation
    allocation = []
    for i in range(n):
        row = list(map(int, lines[pos].split()))
        if len(row) != m:
            raise ValueError("Dong Allocation cua P%d khong du %d cot" % (i, m))
        allocation.append(row)
        pos += 1

    # Tinh Need = Max - Allocation, dong thoi kiem tra tinh hop le
    # (Allocation khong duoc vuot Max, vi khong the giu nhieu hon nhu cau da khai bao)
    need = []
    for i in range(n):
        need_row = []
        for j in range(m):
            n_ij = max_matrix[i][j] - allocation[i][j]
            if n_ij < 0:
                raise ValueError(
                    "P%d dang giu %d thuc the tai nguyen R%d, vuot qua Max da khai bao (%d)"
                    % (i, allocation[i][j], j, max_matrix[i][j])
                )
            need_row.append(n_ij)
        need.append(need_row)

    return {
        "n": n,
        "m": m,
        "available": available,
        "max": max_matrix,
        "allocation": allocation,
        "need": need,
    }


if __name__ == "__main__":
    # Chay thu truc tiep: python3 src/data_loader.py data/sample_state.txt
    import sys

    path = sys.argv[1] if len(sys.argv) > 1 else "data/sample_state.txt"
    data = load_state(path)

    print("So tien trinh n =", data["n"], " | So loai tai nguyen m =", data["m"])
    print("Available:", data["available"])
    print("\n%-4s %-12s %-12s %-12s" % ("PID", "Max", "Allocation", "Need"))
    for i in range(data["n"]):
        print("P%-3d %-12s %-12s %-12s" % (i, data["max"][i], data["allocation"][i], data["need"][i]))
