#!/usr/bin/env python3
"""와인_가치평가_음용관리.xlsm 을 XML 패치로 고치는 도구.

드라이브 커넥터로는 큰 xlsm을 덮어쓸 수 없어서, 바뀐 부분만 담은 패치(JSON)를
와인/_Claude_자동갱신 폴더에 올리고, 사용자 계정의 Apps Script(apps_script/Code.js)가
같은 작업을 다시 적용해 원본 파일(같은 ID)에 덮어쓴다.

작업 종류 (Code.js 의 applyOps_ 와 똑같이 동작해야 한다)
  replace     part 안에서 find 가 정확히 한 곳이어야 하고, 그곳을 replace 로 바꾼다
  replaceAll  part 안의 find 를 모두 바꾼다. count 가 있으면 개수가 같아야 한다
  put         part 를 text(UTF-8)로 새로 쓰거나 덮어쓴다
  putBase64   part 를 바이너리로 새로 쓰거나 덮어쓴다
  delete      part 를 지운다

사용
  p = Patch(open('base.xlsm', 'rb').read())
  p.replace('xl/worksheets/sheet2.xml', '<dimension ref="A1:Z361"/>', '<dimension ref="A1:Z362"/>')
  p.write('out.patch.json', label='W209추가')   # expectSha256·baseMd5 포함
  open('new.xlsm', 'wb').write(p.build())       # 로컬 확인용

  python3 xlsm_patch.py verify base.xlsm out.patch.json     # JSON만으로 다시 적용해 해시 확인
  python3 xlsm_patch.py apply  base.xlsm out.patch.json new.xlsm
  python3 xlsm_patch.py compare result.xlsm base.xlsm out.patch.json  # 적용된 드라이브 파일 확인
"""
import base64
import datetime
import hashlib
import io
import json
import sys
import zipfile

FORMAT = 'xlsm-xml-patch-v1'


def read_zip(data):
    zf = zipfile.ZipFile(io.BytesIO(data))
    order = [i.filename for i in zf.infolist() if not i.is_dir()]
    return order, {n: zf.read(n) for n in order}


def sha256(b):
    return hashlib.sha256(b).hexdigest()


def apply_ops(order, parts, ops):
    """Code.js applyOps_ 와 같은 규칙. order·parts 를 고쳐서 바뀐 파트 이름 목록을 돌려준다."""
    texts, changed = {}, []

    def text(n):
        if n not in texts:
            if n not in parts:
                raise ValueError('파트 없음: ' + n)
            texts[n] = parts[n].decode('utf-8')
        return texts[n]

    for i, op in enumerate(ops):
        kind, n = op['op'], op['part']
        where = f'작업 {i} ({kind} {n})'
        if kind == 'replace':
            f, s = op['find'], text(n)
            if not f:
                raise ValueError(where + ': find 비어 있음')
            at = s.find(f)
            if at < 0:
                raise ValueError(where + ': 찾을 문자열 없음')
            if s.find(f, at + 1) >= 0:
                raise ValueError(where + ': 찾을 문자열이 여러 곳')
            texts[n] = s[:at] + op['replace'] + s[at + len(f):]
        elif kind == 'replaceAll':
            f, s = op['find'], text(n)
            if not f:
                raise ValueError(where + ': find 비어 있음')
            if op.get('count') is not None and s.count(f) != op['count']:
                raise ValueError(f"{where}: 개수 {s.count(f)} != {op['count']}")
            texts[n] = s.replace(f, op['replace'])
        elif kind == 'put':
            if n not in parts:
                order.append(n)
                parts[n] = None
            texts[n] = op['text']
        elif kind == 'putBase64':
            if n not in parts:
                order.append(n)
            parts[n] = base64.b64decode(op['base64'])
            texts.pop(n, None)
        elif kind == 'delete':
            if n not in parts:
                raise ValueError(where + ': 파트 없음')
            del parts[n]
            texts.pop(n, None)
            order.remove(n)
        else:
            raise ValueError(where + ': 모르는 작업')
        if n not in changed:
            changed.append(n)
    for n, s in texts.items():
        parts[n] = s.encode('utf-8')
    return changed


def zip_parts(order, parts, base_infos=None):
    out = io.BytesIO()
    with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED) as zf:
        for n in order:
            info = zipfile.ZipInfo(n, base_infos[n].date_time if base_infos and n in base_infos else (1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            zf.writestr(info, parts[n])
    return out.getvalue()


class Patch:
    """작업을 기록하면서 바로 적용한다. text() 로 현재 내용을 읽어 다음 작업을 만든다."""

    def __init__(self, base_bytes):
        self.base_bytes = base_bytes
        self.base_md5 = hashlib.md5(base_bytes).hexdigest()
        self.order, self.parts = read_zip(base_bytes)
        self.ops = []

    def _do(self, op):
        apply_ops(self.order, self.parts, [op])
        self.ops.append(op)

    def text(self, part):
        return self.parts[part].decode('utf-8')

    def replace(self, part, find, repl):
        self._do({'op': 'replace', 'part': part, 'find': find, 'replace': repl})

    def replace_all(self, part, find, repl, count=None):
        n = self.text(part).count(find)
        if count is not None and n != count:
            raise ValueError(f'{part}: {find!r} 개수 {n} != {count}')
        self._do({'op': 'replaceAll', 'part': part, 'find': find, 'replace': repl, 'count': n})

    def put(self, part, text):
        self._do({'op': 'put', 'part': part, 'text': text})

    def put_bytes(self, part, data):
        self._do({'op': 'putBase64', 'part': part, 'base64': base64.b64encode(data).decode()})

    def delete(self, part):
        self._do({'op': 'delete', 'part': part})

    def changed(self):
        names = []
        for op in self.ops:
            if op['part'] not in names:
                names.append(op['part'])
        return names

    def to_dict(self, label, dry_run=False, backup_name=None):
        return {
            'format': FORMAT,
            'label': label,
            'createdAt': datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds'),
            'baseMd5': self.base_md5,
            'dryRun': dry_run,
            'backupName': backup_name,
            'ops': self.ops,
            'expectSha256': {n: sha256(self.parts[n]) for n in self.changed() if n in self.parts},
            'expectPartCount': len(self.order),
        }

    def write(self, path, label, dry_run=False, backup_name=None):
        d = self.to_dict(label, dry_run, backup_name)
        text = json.dumps(d, ensure_ascii=False, separators=(',', ':'))
        check_patch(self.base_bytes, json.loads(text))
        with open(path, 'w', encoding='utf-8') as f:
            f.write(text)
        return d

    def build(self):
        base_infos = {i.filename: i for i in zipfile.ZipFile(io.BytesIO(self.base_bytes)).infolist()}
        return zip_parts(self.order, self.parts, base_infos)


def check_patch(base_bytes, patch):
    """JSON 패치만으로 다시 적용해 expectSha256 와 파트 수를 확인한다."""
    if patch.get('format') != FORMAT:
        raise ValueError('형식이 다름: %r' % patch.get('format'))
    if hashlib.md5(base_bytes).hexdigest() != patch['baseMd5']:
        raise ValueError('기준 파일 md5 가 패치와 다름')
    order, parts = read_zip(base_bytes)
    apply_ops(order, parts, patch['ops'])
    for n, h in patch['expectSha256'].items():
        if sha256(parts[n]) != h:
            raise ValueError('해시 불일치: ' + n)
    if patch.get('expectPartCount') not in (None, len(order)):
        raise ValueError('파트 수 불일치')
    return order, parts


def compare(result_bytes, base_bytes, patch):
    """드라이브에 적용된 결과 파일이 기대한 파트와 바이트 단위로 같은지 확인한다."""
    order, parts = check_patch(base_bytes, patch)
    r_order, r_parts = read_zip(result_bytes)
    problems = [n for n in order if r_parts.get(n) != parts[n]]
    problems += ['(남는 파트) ' + n for n in r_order if n not in parts]
    return problems


def main(argv):
    cmd = argv[1] if len(argv) > 1 else ''
    if cmd == 'verify' and len(argv) == 4:
        base = open(argv[2], 'rb').read()
        patch = json.load(open(argv[3], encoding='utf-8'))
        order, _ = check_patch(base, patch)
        print(f"OK  작업 {len(patch['ops'])}개, 바뀐 파트 {len(patch['expectSha256'])}개, 전체 {len(order)}개")
    elif cmd == 'apply' and len(argv) == 5:
        base = open(argv[2], 'rb').read()
        order, parts = check_patch(base, json.load(open(argv[3], encoding='utf-8')))
        base_infos = {i.filename: i for i in zipfile.ZipFile(io.BytesIO(base)).infolist()}
        open(argv[4], 'wb').write(zip_parts(order, parts, base_infos))
        print('OK ->', argv[4])
    elif cmd == 'compare' and len(argv) == 5:
        problems = compare(open(argv[2], 'rb').read(), open(argv[3], 'rb').read(),
                           json.load(open(argv[4], encoding='utf-8')))
        print('OK  모든 파트 일치' if not problems else '다른 파트: ' + ', '.join(problems))
        return 1 if problems else 0
    else:
        print(__doc__)
        return 2
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
