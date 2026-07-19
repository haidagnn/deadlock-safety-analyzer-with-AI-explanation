# -*- coding: utf-8 -*-

def explain_rule_based(trace, is_safe):
    lines = []

    if not is_safe:
        lines.append("KET LUAN: He thong dang o trang thai KHONG AN TOAN (Unsafe State).")
        lines.append(
            "Khong con tien trinh nao co Need <= Work de tiep tuc gia dinh chay -> "
            "he thong CO NGUY CO xay ra Deadlock (chua chac chan Deadlock da xay ra "
            "ngay, nhung khong con cach nao dam bao moi tien trinh deu hoan thanh)."
        )
        return "\n".join(lines)

    lines.append("KET LUAN: He thong dang o trang thai AN TOAN (Safe State).")
    lines.append("")

    for step_no, step in enumerate(trace, start=1):
        p = step["process"]
        lines.append(
            "Buoc %d: Chon tien trinh P%d, vi Need[P%d] = %s <= Work hien tai = %s "
            "(tren tung loai tai nguyen). "
            "Gia dinh P%d duoc cap du, chay xong va TRA LAI toan bo Allocation = %s "
            "cho he thong -> Work moi = %s."
            % (
                step_no, p, p, step["need"], step["work_before"],
                p, step["allocation_returned"], step["work_after"],
            )
        )

    seq_str = " -> ".join("P%d" % s["process"] for s in trace)
    lines.append("")
    lines.append("Safe Sequence tim duoc: <%s>." % seq_str)
    lines.append(
        "Luu y quan trong: mot he thong an toan co the ton tai NHIEU Safe Sequence "
        "khac nhau, tuy thu tu chon tien trinh trong so cac tien trinh dang thoa "
        "dieu kien Need <= Work o moi buoc. Chi can TIM RA duoc it nhat MOT chuoi "
        "la du de ket luan he thong an toan; khong nhat thiet phai trung 100% voi "
        "chuoi tinh tay trong tai lieu."
    )
    return "\n".join(lines)


def explain_with_llm(trace, is_safe, api_key=None, model="claude-sonnet-4-6"):
   
    if not api_key:
        return explain_rule_based(trace, is_safe)

    import json
    import urllib.request

    payload = {"is_safe": is_safe, "trace": trace}

    prompt = (
        "Ban la tro giang mon He Dieu Hanh. Duoi day la ket qua (dang JSON) "
        "cua Thuat toan Banker chay tren mot trang thai he thong cu the. Hay "
        "viet lai thanh mot doan giai thich TIENG VIET, ro rang, de hieu cho "
        "sinh vien nam nhat, khong bia them so lieu ngoai du lieu duoc cho:\n\n"
        + json.dumps(payload, ensure_ascii=False)
    )

    body = json.dumps({
        "model": model,
        "max_tokens": 600,
        "messages": [{"role": "user", "content": prompt}],
    }).encode("utf-8")

    req = urllib.request.Request(
        "https://api.anthropic.com/v1/messages",
        data=body,
        headers={
            "Content-Type": "application/json",
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
        },
    )

    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        text = "".join(block.get("text", "") for block in data.get("content", []))
        return text if text.strip() else explain_rule_based(trace, is_safe)
    except Exception as e:
        # Khong bao gio de loi mang lam sap chuong trinh chinh
        fallback = explain_rule_based(trace, is_safe)
        return fallback + "\n\n[Ghi chu: goi LLM that bai (%s), da dung ban rule-based.]" % e
