# -*- coding: utf-8 -*-
r"""
FBT 카페 매주 자동 수집 (윈도우 작업 스케줄러 등록/해제)
  - 매주자동수집_켜기.bat : 매주 일요일 오전 10시에 수집기가 저절로 돌게 등록
  - 매주자동수집_끄기.bat : 등록 해제
일요일에 컴퓨터가 꺼져 있었으면 다음에 켤 때 실행됩니다.
Enter를 누를 필요 없이 끝까지 돌고, 끝나면 창도 저절로 닫힙니다.
"""
import os
import sys
import json
import time
import shutil
import socket
import ntpath
import datetime
import subprocess
from xml.sax.saxutils import escape

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

TASK_NAME = "FBT_weekly_collect"
WEEKDAY = 6                    # 0=월요일 ... 6=일요일
AT_HOUR, AT_MINUTE = 10, 0     # 오전 10시
DAY_NAMES = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
DAY_KO = ["월", "화", "수", "목", "금", "토", "일"]

LOCAL_DIR  = r"C:\FBT"
LOCAL_COPY = os.path.join(LOCAL_DIR, "fbt_weekly.py")    # 스케줄러는 이 사본을 실행 (G: 준비 전에도 뜨도록)
CONFIG     = os.path.join(LOCAL_DIR, "fbt_weekly.json")
LOCK       = os.path.join(LOCAL_DIR, "fbt_weekly.lock")
LOG        = os.path.join(LOCAL_DIR, "logs", "주간자동수집.txt")
DEFAULT_COLLECTOR = r"G:\내 드라이브\claude\FBT\수집기\fbt_collector.py"

WAIT_DRIVE_MIN = 20            # 구글 드라이브(G:)가 뜰 때까지 기다리는 최대 시간(분)
WAIT_NET_MIN   = 10            # 인터넷이 될 때까지 기다리는 최대 시간(분)
POLL_SEC       = 15


def log(msg):
    line = f"{datetime.datetime.now():%Y-%m-%d %H:%M} | {msg}"
    print(line, flush=True)
    try:
        os.makedirs(os.path.dirname(LOG), exist_ok=True)
        with open(LOG, "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except Exception:
        pass


def next_run(now):
    """다음 실행 시각 (오늘이 그 요일이고 아직 시간 전이면 오늘)."""
    target = now.replace(hour=AT_HOUR, minute=AT_MINUTE, second=0, microsecond=0)
    days = (WEEKDAY - now.weekday()) % 7
    target += datetime.timedelta(days=days)
    if target <= now:
        target += datetime.timedelta(days=7)
    return target


def task_xml(python, script, start, user=""):
    principal = f"      <UserId>{escape(user)}</UserId>\n" if user else ""
    return f"""<?xml version="1.0" encoding="UTF-16"?>
<Task version="1.2" xmlns="http://schemas.microsoft.com/windows/2004/02/mit/task">
  <RegistrationInfo>
    <Description>FBT 카페 매주 자동 수집 (fbt_collector.py --auto)</Description>
  </RegistrationInfo>
  <Triggers>
    <CalendarTrigger>
      <StartBoundary>{start:%Y-%m-%dT%H:%M:%S}</StartBoundary>
      <Enabled>true</Enabled>
      <ScheduleByWeek>
        <DaysOfWeek>
          <{DAY_NAMES[WEEKDAY]} />
        </DaysOfWeek>
        <WeeksInterval>1</WeeksInterval>
      </ScheduleByWeek>
    </CalendarTrigger>
  </Triggers>
  <Principals>
    <Principal id="Author">
{principal}      <LogonType>InteractiveToken</LogonType>
      <RunLevel>LeastPrivilege</RunLevel>
    </Principal>
  </Principals>
  <Settings>
    <MultipleInstancesPolicy>IgnoreNew</MultipleInstancesPolicy>
    <DisallowStartIfOnBatteries>false</DisallowStartIfOnBatteries>
    <StopIfGoingOnBatteries>false</StopIfGoingOnBatteries>
    <AllowHardTerminate>true</AllowHardTerminate>
    <StartWhenAvailable>true</StartWhenAvailable>
    <RunOnlyIfNetworkAvailable>false</RunOnlyIfNetworkAvailable>
    <IdleSettings>
      <StopOnIdleEnd>false</StopOnIdleEnd>
      <RestartOnIdle>false</RestartOnIdle>
    </IdleSettings>
    <AllowStartOnDemand>true</AllowStartOnDemand>
    <Enabled>true</Enabled>
    <Hidden>false</Hidden>
    <RunOnlyIfIdle>false</RunOnlyIfIdle>
    <WakeToRun>true</WakeToRun>
    <ExecutionTimeLimit>PT8H</ExecutionTimeLimit>
    <Priority>7</Priority>
  </Settings>
  <Actions Context="Author">
    <Exec>
      <Command>{escape(python)}</Command>
      <Arguments>{escape(f'"{script}" --run')}</Arguments>
      <WorkingDirectory>{escape(ntpath.dirname(script))}</WorkingDirectory>
    </Exec>
  </Actions>
</Task>
"""


def schtasks(*args):
    try:
        r = subprocess.run(["schtasks", *args], capture_output=True)
    except FileNotFoundError:
        return False, "작업 스케줄러(schtasks)를 찾을 수 없어요. 윈도우에서 실행해주세요."
    enc = "mbcs" if os.name == "nt" else "utf-8"
    out = (r.stdout + r.stderr).decode(enc, errors="replace").strip()
    return r.returncode == 0, out


def install():
    here = os.path.dirname(os.path.abspath(__file__))
    collector = os.path.join(here, "fbt_collector.py")
    if not os.path.isfile(collector):
        print(f"!! 같은 폴더에 fbt_collector.py 가 없어요: {here}")
        return 1
    os.makedirs(LOCAL_DIR, exist_ok=True)
    if os.path.abspath(__file__).lower() != os.path.abspath(LOCAL_COPY).lower():
        shutil.copy2(os.path.abspath(__file__), LOCAL_COPY)
    with open(CONFIG, "w", encoding="utf-8") as f:
        json.dump({"collector": collector}, f, ensure_ascii=False)

    start = next_run(datetime.datetime.now())
    user = "\\".join(p for p in (os.environ.get("USERDOMAIN"), os.environ.get("USERNAME")) if p)
    xml_path = os.path.join(LOCAL_DIR, "fbt_weekly_task.xml")
    with open(xml_path, "w", encoding="utf-16") as f:
        f.write(task_xml(sys.executable, LOCAL_COPY, start, user))

    ok, out = schtasks("/Create", "/TN", TASK_NAME, "/XML", xml_path, "/F")
    simple = False
    if not ok:      # 예비: 기본 옵션만으로라도 등록
        tr = f'"{sys.executable}" "{LOCAL_COPY}" --run'
        ok, out2 = schtasks("/Create", "/TN", TASK_NAME, "/SC", "WEEKLY",
                            "/D", DAY_NAMES[WEEKDAY][:3].upper(),
                            "/ST", f"{AT_HOUR:02d}:{AT_MINUTE:02d}", "/TR", tr, "/F")
        out, simple = out + "\n" + out2, True

    print("")
    if ok:
        print("=" * 52)
        print(f"  매주 자동 수집을 켰어요: 매주 {DAY_KO[WEEKDAY]}요일 {AT_HOUR}시 {AT_MINUTE:02d}분")
        print(f"  첫 실행: {start:%Y-%m-%d} ({DAY_KO[start.weekday()]}) {start:%H:%M}")
        if simple:
            print("  (그 시각에 컴퓨터가 켜져 있을 때만 돌아요)")
        else:
            print("  그 시각에 컴퓨터가 꺼져 있었으면 다음에 켤 때 돌아요.")
        print("  Enter 누를 필요 없고, 끝나면 창이 저절로 닫혀요.")
        print("  결과는 드라이브 FBT\\수집기\\수집기록.txt 에 남아요.")
        print("=" * 52)
        log(f"자동 수집 등록 (첫 실행 {start:%Y-%m-%d %H:%M})")
        return 0
    print("!! 등록하지 못했어요. 아래 내용을 캡처해서 알려주세요.")
    print(out)
    return 1


def uninstall():
    ok, out = schtasks("/Delete", "/TN", TASK_NAME, "/F")
    print("")
    if ok:
        print("매주 자동 수집을 껐어요. 다시 켜려면 매주자동수집_켜기.bat 을 실행하세요.")
        log("자동 수집 해제")
        return 0
    print("!! 끄지 못했어요 (이미 꺼져 있을 수도 있어요):")
    print(out)
    return 1


def collector_path():
    try:
        with open(CONFIG, encoding="utf-8") as f:
            return json.load(f).get("collector") or DEFAULT_COLLECTOR
    except Exception:
        return DEFAULT_COLLECTOR


def internet_ok():
    try:
        socket.create_connection(("cafe.naver.com", 443), timeout=5).close()
        return True
    except OSError:
        return False


def wait_for(check, minutes):
    deadline = time.time() + minutes * 60
    while True:
        if check():
            return True
        if time.time() >= deadline:
            return False
        time.sleep(POLL_SEC)


def windows_tweaks():
    """창 제목 표시 + 기다리는 동안 절전 방지"""
    if os.name != "nt":
        return
    try:
        import ctypes
        ctypes.windll.kernel32.SetConsoleTitleW("FBT 카페 주간 자동 수집 - 끝나면 저절로 닫혀요")
        ctypes.windll.kernel32.SetThreadExecutionState(0x80000000 | 0x00000001)
    except Exception:
        pass


def run():
    windows_tweaks()
    log("주간 자동 수집 시작")
    if os.path.exists(LOCK) and time.time() - os.path.getmtime(LOCK) < 10 * 3600:
        log("다른 수집이 진행 중이라 이번에는 건너뜀")
        return 0
    os.makedirs(LOCAL_DIR, exist_ok=True)
    with open(LOCK, "w") as f:
        f.write(str(os.getpid()))
    try:
        collector = collector_path()
        if not wait_for(lambda: os.path.isfile(collector), WAIT_DRIVE_MIN):
            log(f"구글 드라이브가 준비되지 않아 이번 주는 건너뜀 ({collector})")
            return 1
        if not wait_for(internet_ok, WAIT_NET_MIN):
            log("인터넷 연결이 없어 이번 주는 건너뜀")
            return 1
        rc = subprocess.call([sys.executable, collector, "--auto"])
        log(f"수집 끝 (종료 코드 {rc})")
        return rc
    finally:
        try:
            os.remove(LOCK)
        except OSError:
            pass


if __name__ == "__main__":
    if "--install" in sys.argv:
        sys.exit(install())
    if "--uninstall" in sys.argv:
        sys.exit(uninstall())
    if "--run" in sys.argv:
        sys.exit(run())
    print(__doc__)
