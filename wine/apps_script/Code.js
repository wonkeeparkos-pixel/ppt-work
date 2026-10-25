/**
 * 와인 엑셀 자동 갱신 (Claude 전용 통로)
 *
 * Claude가 와인/_Claude_자동갱신 폴더에 올린 *.patch.json 을 1분마다 확인해서
 * 와인_가치평가_음용관리.xlsm 안의 XML을 고친 뒤, 같은 파일(같은 ID·링크)에 덮어씁니다.
 *  - 고치기 전 파일은 와인/_이전버전 에 복사해 둡니다.
 *  - 패치를 만든 뒤 엑셀이 바뀌었으면(md5 불일치) 아무것도 고치지 않습니다.
 *  - 고친 결과가 패치에 적힌 해시와 하나라도 다르면 아무것도 고치지 않습니다.
 *  - 아래 WINE_FILE_ID 파일 하나만 고칩니다.
 * 결과는 _Claude_자동갱신/처리완료 에 <이름>.result.json 으로 남습니다.
 *
 * 처음 한 번: 위쪽 함수 목록에서 setup 을 고르고 [실행] → 권한 허용.
 * 그만 쓰려면: uninstall 실행.
 */

// 공개 저장소라 실제 드라이브 ID는 넣지 않는다. 설치할 때 아래 네 값을 바꿔 넣는다.
const WINE_FILE_ID = '<와인 엑셀 파일 ID>';                // 와인/와인_가치평가_음용관리.xlsm
const BACKUP_FOLDER_ID = '<_이전버전 폴더 ID>';            // 와인/_이전버전
const INBOX_FOLDER_ID = '<_Claude_자동갱신 폴더 ID>';      // 와인/_Claude_자동갱신
const DONE_FOLDER_ID = '<처리완료 폴더 ID>';               // 와인/_Claude_자동갱신/처리완료
const XLSM_MIME = 'application/vnd.ms-excel.sheet.macroenabled.12';
const PATCH_FORMAT = 'xlsm-xml-patch-v1';

function setup() {
  DriveApp.getFileById(WINE_FILE_ID).getName();
  [BACKUP_FOLDER_ID, INBOX_FOLDER_ID, DONE_FOLDER_ID].forEach(id => DriveApp.getFolderById(id).getName());
  const wine = driveMeta_();
  ScriptApp.getProjectTriggers().forEach(t => ScriptApp.deleteTrigger(t));
  ScriptApp.newTrigger('processInbox').timeBased().everyMinutes(1).create();
  writeResult_('setup', {ok: true, at: new Date().toISOString(), wine: wine});
  processInbox();
}

function uninstall() {
  ScriptApp.getProjectTriggers().forEach(t => ScriptApp.deleteTrigger(t));
}

function processInbox() {
  const lock = LockService.getScriptLock();
  if (!lock.tryLock(1000)) return;
  try {
    const patches = [];
    const files = DriveApp.getFolderById(INBOX_FOLDER_ID).getFiles();
    while (files.hasNext()) {
      const f = files.next();
      if (/\.patch\.json$/.test(f.getName())) patches.push(f);
    }
    patches.sort((a, b) => (a.getName() < b.getName() ? -1 : 1));
    patches.forEach(f => {
      const name = f.getName().replace(/\.patch\.json$/, '');
      let result;
      try {
        result = applyPatchFile_(f, name);
      } catch (e) {
        result = {ok: false, error: String((e && e.stack) || e)};
      }
      result.patch = f.getName();
      result.finishedAt = new Date().toISOString();
      writeResult_(name, result);
      f.moveTo(DriveApp.getFolderById(DONE_FOLDER_ID));
    });
  } finally {
    lock.releaseLock();
  }
}

function applyPatchFile_(file, name) {
  const patch = JSON.parse(file.getBlob().getDataAsString('UTF-8'));
  if (patch.format !== PATCH_FORMAT) throw new Error('모르는 패치 형식: ' + patch.format);
  const before = driveMeta_();
  if (patch.ping) return {ok: true, ping: true, wine: before};
  if (before.md5Checksum !== patch.baseMd5) return {ok: false, reason: 'base_changed', wine: before};

  const wine = DriveApp.getFileById(WINE_FILE_ID);
  const order = [];
  const parts = {};
  Utilities.unzip(wine.getBlob().setContentType('application/zip')).forEach(b => {
    order.push(b.getName());
    parts[b.getName()] = b;
  });
  const changed = applyOps_(patch.ops, order, parts, {
    readText: b => b.getDataAsString('UTF-8'),
    text: (s, n) => Utilities.newBlob('', 'application/xml', n).setDataFromString(s, 'UTF-8'),
    binary: (b64, n) => Utilities.newBlob(Utilities.base64Decode(b64), 'application/octet-stream', n),
  });
  Object.keys(patch.expectSha256 || {}).forEach(n => {
    if (!parts[n]) throw new Error('검증: 파트 없음 ' + n);
    if (hex_(Utilities.computeDigest(Utilities.DigestAlgorithm.SHA_256, parts[n].getBytes())) !== patch.expectSha256[n]) {
      throw new Error('검증: 해시 불일치 ' + n);
    }
  });
  if (patch.expectPartCount && patch.expectPartCount !== order.length) {
    throw new Error('검증: 파트 수 ' + order.length + ' ≠ ' + patch.expectPartCount);
  }

  const zip = Utilities.zip(order.map(n => parts[n].setName(n)), wine.getName()).getBytes();
  if (zip.length < 100000) throw new Error('결과 파일이 너무 작음: ' + zip.length);
  const md5 = hex_(Utilities.computeDigest(Utilities.DigestAlgorithm.MD5, zip));
  if (patch.dryRun) {
    const out = DriveApp.getFolderById(DONE_FOLDER_ID).createFile(Utilities.newBlob(zip, XLSM_MIME, name + '.dryrun.xlsm'));
    return {ok: true, dryRun: true, outputId: out.getId(), size: zip.length, md5: md5, parts: order.length, changed: changed};
  }

  const backupName = patch.backupName ||
    '와인_가치평가_음용관리_' + (patch.label || name) + '전_' + Utilities.formatDate(new Date(), 'Asia/Seoul', 'yyyyMMdd_HHmm') + '.xlsm';
  const backup = wine.makeCopy(backupName, DriveApp.getFolderById(BACKUP_FOLDER_ID));
  const res = UrlFetchApp.fetch(
    'https://www.googleapis.com/upload/drive/v3/files/' + WINE_FILE_ID + '?uploadType=media&fields=md5Checksum,size,modifiedTime,version', {
      method: 'patch',
      contentType: XLSM_MIME,
      payload: zip,
      headers: {Authorization: 'Bearer ' + ScriptApp.getOAuthToken()},
      muteHttpExceptions: true,
    });
  if (res.getResponseCode() !== 200) throw new Error('덮어쓰기 실패 ' + res.getResponseCode() + ': ' + res.getContentText());
  const after = JSON.parse(res.getContentText());
  return {ok: after.md5Checksum === md5, before: before, after: after, md5: md5, size: zip.length,
    parts: order.length, changed: changed, backupId: backup.getId(), backupName: backupName};
}

/** xlsm_patch.py 의 apply_ops 와 같은 규칙. 바뀐 파트 이름 목록을 돌려준다. */
function applyOps_(ops, order, parts, io) {
  const has = (o, k) => Object.prototype.hasOwnProperty.call(o, k);
  const texts = {};
  const changed = [];
  const text = n => {
    if (!has(texts, n)) {
      if (!has(parts, n)) throw new Error('파트 없음: ' + n);
      texts[n] = io.readText(parts[n]);
    }
    return texts[n];
  };
  (ops || []).forEach((op, i) => {
    const n = op.part;
    const where = '작업 ' + i + ' (' + op.op + ' ' + n + ')';
    if (op.op === 'replace') {
      if (!op.find || typeof op.replace !== 'string') throw new Error(where + ': find/replace 잘못됨');
      const s = text(n);
      const at = s.indexOf(op.find);
      if (at < 0) throw new Error(where + ': 찾을 문자열 없음');
      if (s.indexOf(op.find, at + 1) >= 0) throw new Error(where + ': 찾을 문자열이 여러 곳');
      texts[n] = s.slice(0, at) + op.replace + s.slice(at + op.find.length);
    } else if (op.op === 'replaceAll') {
      if (!op.find || typeof op.replace !== 'string') throw new Error(where + ': find/replace 잘못됨');
      const pieces = text(n).split(op.find);
      if (op.count != null && pieces.length - 1 !== op.count) throw new Error(where + ': 개수 ' + (pieces.length - 1) + ' ≠ ' + op.count);
      texts[n] = pieces.join(op.replace);
    } else if (op.op === 'put') {
      if (typeof op.text !== 'string') throw new Error(where + ': text 없음');
      if (!has(parts, n)) {
        order.push(n);
        parts[n] = null;
      }
      texts[n] = op.text;
    } else if (op.op === 'putBase64') {
      if (!has(parts, n)) order.push(n);
      parts[n] = io.binary(op.base64, n);
      delete texts[n];
    } else if (op.op === 'delete') {
      if (!has(parts, n)) throw new Error(where + ': 파트 없음');
      delete parts[n];
      delete texts[n];
      order.splice(order.indexOf(n), 1);
    } else {
      throw new Error(where + ': 모르는 작업');
    }
    if (changed.indexOf(n) < 0) changed.push(n);
  });
  Object.keys(texts).forEach(n => {
    parts[n] = io.text(texts[n], n);
  });
  return changed;
}

function driveMeta_() {
  const res = UrlFetchApp.fetch(
    'https://www.googleapis.com/drive/v3/files/' + WINE_FILE_ID + '?fields=md5Checksum,size,modifiedTime,version', {
      headers: {Authorization: 'Bearer ' + ScriptApp.getOAuthToken()},
      muteHttpExceptions: true,
    });
  if (res.getResponseCode() !== 200) throw new Error('파일 정보 읽기 실패 ' + res.getResponseCode() + ': ' + res.getContentText());
  return JSON.parse(res.getContentText());
}

function writeResult_(name, obj) {
  DriveApp.getFolderById(DONE_FOLDER_ID).createFile(name + '.result.json', JSON.stringify(obj, null, 1), 'application/json');
}

function hex_(bytes) {
  return bytes.map(b => ('0' + (b & 0xff).toString(16)).slice(-2)).join('');
}

if (typeof module !== 'undefined') module.exports = {applyOps_, hex_};
