#!/usr/bin/env python3
"""폴더 안 파일들의 중복을 검사하고 하나의 ZIP으로 묶는 도구.

검사 단계
 1. SHA-256 해시로 내용이 완전히 같은 파일을 찾는다 (파일명이 달라도 잡힘).
 2. .xls/.xlsx 표 파일은 첫 행을 머리글로 보고, 지정한 열(기본: 첫 열 '순번')을 뺀
    나머지 열 값으로 행 집합을 만들어 파일끼리 겹치는 행이 있는지 대조한다.
 3. 결과를 '중복검사_결과.txt'로 적고, 중복 파일(같은 해시 그룹의 2번째 이후)을 뺀
    나머지를 폴더 구조 그대로 ZIP에 담는다.

사용법
    python scripts/dedup_zip_tool.py <원본폴더> <출력.zip> [--keep-dups] [--seq-col 0]

    --keep-dups   해시가 같은 파일도 빼지 않고 전부 담는다(보고서만 작성).
    --seq-col N   표 대조에서 제외할 열 번호(0부터). 없으면 -1.

필요 패키지: xlrd (xls), openpyxl (xlsx). 없으면 표 대조는 건너뛴다.
"""
import argparse, collections, datetime, hashlib, itertools, os, sys, warnings, zipfile

warnings.filterwarnings("ignore")


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def _cell(v):
    if isinstance(v, float) and v.is_integer():
        return str(int(v))
    return "" if v is None else str(v).strip()


def table_rows(path):
    """표 파일의 (머리글 제외) 행 목록을 문자열 리스트로 돌려준다. 못 읽으면 None."""
    try:
        if path.lower().endswith(".xls"):
            import xlrd
            sh = xlrd.open_workbook(path).sheet_by_index(0)
            rows = [[_cell(sh.cell_value(r, c)) for c in range(sh.ncols)] for r in range(1, sh.nrows)]
        else:
            import openpyxl
            wb = openpyxl.load_workbook(path, read_only=True, data_only=True, keep_links=False)
            it = wb.worksheets[0].iter_rows(values_only=True)
            next(it, None)
            rows = [[_cell(v) for v in row] for row in it]
    except Exception as e:  # noqa: BLE001
        print(f"  (표 읽기 실패: {os.path.basename(path)}: {e})", file=sys.stderr)
        return None
    return [r for r in rows if any(r)]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src")
    ap.add_argument("out")
    ap.add_argument("--keep-dups", action="store_true")
    ap.add_argument("--seq-col", type=int, default=0)
    a = ap.parse_args()

    files = []
    for root, _, names in os.walk(a.src):
        for n in sorted(names):
            files.append(os.path.join(root, n))
    files.sort()
    rel = {f: os.path.relpath(f, a.src) for f in files}

    # 1) 해시 중복
    groups = collections.defaultdict(list)
    for f in files:
        groups[sha256(f)].append(f)
    dup_groups = [g for g in groups.values() if len(g) > 1]
    drop = set()
    if not a.keep_dups:
        for g in dup_groups:
            drop.update(g[1:])

    # 2) 표 행 대조
    tables = {}
    for f in files:
        if f.lower().endswith((".xls", ".xlsx")):
            rows = table_rows(f)
            if rows is not None:
                key = (lambda r: tuple(r[:a.seq_col] + r[a.seq_col + 1:])) if a.seq_col >= 0 else tuple
                tables[f] = set(key(r) for r in rows)
    overlaps = []
    for x, y in itertools.combinations(tables, 2):
        inter = len(tables[x] & tables[y])
        if inter:
            overlaps.append((rel[x], len(tables[x]), rel[y], len(tables[y]), inter))

    # 3) 보고서 + ZIP
    lines = [f"중복 검사 결과  ({datetime.datetime.now():%Y-%m-%d %H:%M})", f"원본 폴더: {a.src}", ""]
    lines.append(f"파일 {len(files)}개 검사, 내용이 완전히 같은 파일 그룹 {len(dup_groups)}개")
    for g in dup_groups:
        lines.append("  - " + " == ".join(rel[f] for f in g) + ("" if a.keep_dups else "   → 첫 파일만 수록"))
    lines.append("")
    lines.append(f"표 파일 {len(tables)}개 행 대조, 겹치는 행이 있는 파일 쌍 {len(overlaps)}개")
    for x, nx, y, ny, inter in overlaps:
        lines.append(f"  - {x} ({nx}행) ∩ {y} ({ny}행) = {inter}행")
    lines.append("")
    lines.append("수록 파일")
    for f in files:
        if f not in drop:
            lines.append(f"  {rel[f]}  ({os.path.getsize(f):,} bytes)")
    report = "\r\n".join(lines) + "\r\n"
    print(report)

    top = os.path.basename(os.path.normpath(a.src))
    with zipfile.ZipFile(a.out, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr(f"{top}/중복검사_결과.txt", report.encode("utf-8-sig"))
        for f in files:
            if f not in drop:
                zf.write(f, f"{top}/{rel[f]}")
    print(f"ZIP 작성: {a.out} ({os.path.getsize(a.out):,} bytes, 제외 {len(drop)}개)")


if __name__ == "__main__":
    main()
