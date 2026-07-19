# -*- coding: utf-8 -*-
"""
banker_algorithm.py
--------------------
Cai dat 2 phan cot loi cua Thuat toan Banker (muc 1.2 tai lieu OSG203):

1. safety_algorithm()   -> ung voi phan "kiem tra Safe State" (dung cho
                            kich ban tinh - Chuong 1).
2. request_algorithm()  -> ung voi tinh huong mot tien trinh xin cap phat
                            THEM tai nguyen tai thoi diem chay (dung cho
                            phan kiem thu dong o Chuong 2).

Ca hai ham deu KHONG lam thay doi du lieu goc truyen vao (khong sua Available/
Allocation/Need cua he thong that) - chi lam viec tren ban sao, dung nguyen
tac "gia dinh roi kiem tra" giong y tuong Ngan hang trong tai lieu.
"""


def safety_algorithm(available, allocation, need):
    """
    Trien khai dung 4 buoc kinh dien cua Safety Algorithm:

      Buoc 1: Work = Available ; Finish[i] = False voi moi i
      Buoc 2: Tim i sao cho Finish[i] == False va Need[i] <= Work
              (khong tim duoc -> sang Buoc 4)
      Buoc 3: Gia dinh Pi chay xong va tra lai tai nguyen:
                  Work = Work + Allocation[i] ; Finish[i] = True
              quay lai Buoc 2
      Buoc 4: Neu Finish[i] == True voi moi i -> He thong AN TOAN

    Tham so:
        available : list[int]         - do dai m
        allocation: list[list[int]]   - ma tran n x m
        need      : list[list[int]]   - ma tran n x m

    Tra ve tuple (is_safe, sequence, trace):
        is_safe  : bool           - True neu tim duoc Safe Sequence
        sequence : list[int]      - danh sach chi so tien trinh theo dung
                                     thu tu an toan (rong neu unsafe)
        trace    : list[dict]     - "nhat ky" tung buoc, dung lam du lieu
                                     dau vao cho module ai_explainer.py
    """
    n = len(allocation)
    m = len(available)

    work = list(available)      # Buoc 1
    finish = [False] * n
    sequence = []
    trace = []

    while len(sequence) < n:
        found = False

        # Buoc 2: duyet tu chi so nho -> lon, tim tien trinh dau tien thoa dieu kien.
        # Cach lam nay tuong duong "khach hang den truoc, ngan hang xet truoc"
        # -> luon tao ra MOT Safe Sequence hop le (co the khac thu tu ghi trong
        # tai lieu, vi mot he thong an toan co the co NHIEU Safe Sequence).
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
            # Buoc 4 (truong hop xau): khong tien trinh nao con lai thoa
            # dieu kien -> KHONG the tiep tuc -> Unsafe State
            return False, [], trace

    # Buoc 4 (truong hop tot): tat ca da Finish = True
    return True, sequence, trace


def request_algorithm(pid, request, available, allocation, need):
    """
    Mo phong tinh huong tien trinh `pid` xin cap phat THEM `request`
    (list[int], cung do dai voi available). Ap dung dung 3 dieu kien
    kiem tra chuan cua Banker's Algorithm cho yeu cau tai nguyen:

        (1) Request[i] <= Need[i]       - khong xin vuot nhu cau da khai bao
        (2) Request[i] <= Available     - phai co du tai nguyen ranh
        (3) Gia dinh cap phat -> chay lai safety_algorithm() tren trang thai
            MOI -> chi CAP THAT neu he thong van o Safe State

    Tra ve tuple (granted, new_state, reason):
        granted   : bool
        new_state : dict hoac None - trang thai moi neu duoc cap
        reason    : str - loi giai thich ngan cho nguoi doc / AI explainer
    """
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
