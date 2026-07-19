# Deadlock Safety Analyzer with AI Explanation

Bài tập lớn môn OSG203 (Operating Systems) - Dai hoc FPT.
Chuong trinh doc trang thai he thong (Available / Max / Allocation), chay
Thuat toan Banker de xac dinh he thong co dang o **Safe State** hay khong,
va sinh giai thich bang ngon ngu tu nhien cho tung buoc.

## 1) Ban se co gi

1. Data Loader doc trang thai he thong tu file `.txt`.
2. Loi Thuat toan Banker: Safety Algorithm + Resource-Request Algorithm.
3. Module sinh giai thich (AI Explanation) - mac dinh rule-based, co san
   khung mo rong goi API LLM neu muon.
4. Bo unit test doi chieu voi kich ban ground-truth trong Chuong 1.

## 2) Ly thuyet toi thieu can nho truoc khi doc code

- **Deadlock**: cac tien trinh cho nhau vinh vien, khong tien trinh nao
  chay tiep duoc. Xay ra khi hoi du **4 dieu kien Coffman**: Mutual
  Exclusion, Hold and Wait, No Preemption, Circular Wait.
- **Available[j]**: so luong tai nguyen loai Rj dang ranh.
- **Max[i][j]**: so luong toi da tai nguyen Rj ma Pi se can trong ca vong doi.
- **Allocation[i][j]**: so luong tai nguyen Rj Pi dang giu.
- **Need[i][j] = Max[i][j] - Allocation[i][j]**: phan con thieu de Pi hoan tat.
- **Safety Algorithm**: gia dinh lan luot cho tung tien trinh "muon truoc,
  tra sau" - neu tim duoc mot thu tu de TAT CA deu chay xong thi he thong
  **an toan** (Safe State); neu bi ket giua chung thi **khong an toan**
  (Unsafe State - co nguy co Deadlock).

Chi tiet day du va bang vi du xem trong tai lieu Chuong 1 nhom da co.

## 3) Cau truc du an

```text
deadlock_safety_analyzer/
  data/
    sample_state.txt       <- kich ban mau (ground-truth Chuong 1)
  outputs/                 <- bao cao JSON sinh ra sau khi chay
  src/
    data_loader.py         <- doc file .txt -> Available/Max/Allocation/Need
    banker_algorithm.py    <- Safety Algorithm + Resource-Request Algorithm
    ai_explainer.py        <- sinh giai thich ngon ngu tu nhien
    main.py                <- entry point, ghep cac module lai
  tests/
    test_banker.py         <- unit test doi chieu ground-truth
  README.md
  install.sh
  requirements.txt
```

## 4) Cai dat

Khong bat buoc thu vien ngoai cho phan loi (chi dung Python 3 chuan). Neu
muon lam them bieu do:

```bash
bash install.sh
```

## 5) Cach chay

### Buoc 1: Phan tich trang thai hien tai (Safety Algorithm)

```bash
python3 src/main.py --input data/sample_state.txt --output outputs/report.json
```

### Buoc 2 (tuy chon): Mo phong tien trinh xin cap them tai nguyen

```bash
python3 src/main.py --input data/sample_state.txt --request "1,1,0,0"
```

(nghia la P1 xin them 1 don vi tai nguyen A, 0 don vi B, 0 don vi C)

### Buoc 3: Chay unit test

```bash
python3 -m unittest tests/test_banker.py -v
```

Ket qua mong doi: he thong o trang thai **AN TOAN**, tim duoc mot Safe
Sequence hop le (co the khac thu tu tinh tay `<P1->P3->P4->P0->P2>` trong
tai lieu, vi mot he thong an toan co the co nhieu chuoi an toan khac nhau -
chuong trinh se in ro ly do trong phan giai thich).

## 6) Dinh dang file dau vao

```text
n m
Available (m so)
n dong Max (moi dong m so)
n dong Allocation (moi dong m so)
```

Xem `data/sample_state.txt` lam vi du mau.

## 7) Bao cao dau ra

`outputs/report.json` gom: `is_safe`, `safe_sequence`, `trace` (nhat ky
tung buoc) va `explanation` (giai thich tieng Viet).

## 8) Phan cong goi y cho nhom 3 nguoi

| Thanh vien | Phu trach | File chinh |
|---|---|---|
| **A - Data & Test** | Thiet ke dinh dang file dau vao, viet/hoan thien `data_loader.py`, chuan bi them 2-3 kich ban test (1 safe, 1 unsafe, 1 bien) trong `data/`, viet them test case vao `tests/test_banker.py` | `src/data_loader.py`, `tests/test_banker.py` |
| **B - Thuat toan loi** | Hieu va trinh bay lai duoc tung dong `banker_algorithm.py` (Safety Algorithm + Resource-Request Algorithm), chay tay doi chieu voi vi du Chuong 1 de bao ve truoc lop | `src/banker_algorithm.py` |
| **C - AI Explanation & Bao cao** | Hoan thien `ai_explainer.py`, quyet dinh co tich hop LLM that hay giu rule-based, viet Chuong 2/3 cua bao cao (mo ta module, ket qua chay, huong phat trien), chuan bi slide dua tren `outputs/report.json` | `src/ai_explainer.py`, bao cao/slide |

Ca 3 nguoi nen cung doc qua `banker_algorithm.py` truoc khi bao ve, vi day
la phan giang vien hoi sau nhat.

## 9) Huong mo rong (neu con thoi gian / muon diem cong)

1. Ve bieu do Available/Need theo tung tien trinh bang matplotlib.
2. Lam giao dien dong lenh (CLI) nhap tay trang thai thay vi doc file.
3. Bat `ai_explainer.explain_with_llm()` de giai thich muot hon (can API key).
4. Them thuat toan Deadlock Detection (khac Avoidance) de so sanh 2 chien luoc.

## 10) Kich ban thuyet trinh / demo

- Chay `main.py` voi kich ban mau -> chi ra he thong an toan, doc to
  Safe Sequence va giai thich tung buoc.
- Chay them `--request` voi mot yeu cau se bi TU CHOI (vi du P0 xin vuot
  Need) de minh hoa truong hop Unsafe bi chan lai.
- Mo `outputs/report.json` de chi giang vien cau truc du lieu dau ra.
