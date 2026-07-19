# -*- coding: utf-8 -*-
def safety_algorithm(available, allocation, need):
   
    n = len(allocation)
    m = len(available)

    work = list(available)      # Buoc 1
    finish = [False] * n
    sequence = []
    trace = []

    while len(sequence) < n:
        found = False
        for i in range(n):
            if finish[i]:
                continue
            if all(need[i][j] <= work[j] for j in range(m)):
                # Buoc 3
                work_before = list(work)
                work = [work[j] + allocation[i][j] for j in range(m)]
                finish[i] = True
                sequence.append(i)
                trace.append({
                    "process": i,
                    "need": list(need[i]),
                    "work_before": work_before,
                    "allocation_returned": list(allocation[i]),
                    "work_after": list(work),
                })
                found = True
                break

        if not found:
            return False, [], trace

    return True, sequence, trace


def request_algorithm(pid, request, available, allocation, need):
    m = len(available)

    # Dieu kien (1)
    if any(request[j] > need[pid][j] for j in range(m)):
        return False, None, (
            "P%d xin vuot qua Need da khai bao -> loi cua tien trinh, tu choi ngay." % pid
        )

    # Dieu kien (2)
    if any(request[j] > available[j] for j in range(m)):
        return False, None, (
            "He thong chua du tai nguyen ranh de dap ung -> P%d phai cho." % pid
        )

    # Dieu kien (3): gia dinh cap phat tren BAN SAO, khong dung du lieu goc
    new_available = [available[j] - request[j] for j in range(m)]
    new_allocation = [list(row) for row in allocation]
    new_need = [list(row) for row in need]

    new_allocation[pid] = [new_allocation[pid][j] + request[j] for j in range(m)]
    new_need[pid] = [new_need[pid][j] - request[j] for j in range(m)]

    is_safe, sequence, _ = safety_algorithm(new_available, new_allocation, new_need)

    if is_safe:
        return True, {
            "available": new_available,
            "allocation": new_allocation,
            "need": new_need,
            "safe_sequence": sequence,
        }, "Cap phat duoc CHAP NHAN - he thong sau khi cap van o Safe State."

    return False, None, (
        "Cap phat se dua he thong ve Unsafe State -> TU CHOI, P%d phai cho." % pid
    )
