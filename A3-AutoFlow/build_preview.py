#!/usr/bin/env python3
"""미리보기용 전체 페이지(ISMA3SC003M13.html)와 바로 열어 볼 수 있는 index.html 을 만든다.

기존 화면(ISMA3SC003M4.do)의 머리글·바닥글을 그대로 가져와 본문만 fragment/ISMA3SC003M13_main.html 로 바꾼다.
본문을 고친 뒤 다시 실행하면 두 파일이 갱신된다.  사용: python3 build_preview.py
"""
import re
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC_URL = "https://www.a3sc.co.kr/a3sc/ISMA3SC003M4.do"
CACHE = ROOT / "reference" / "ISMA3SC003M4.html"
PAGE_ID = "ISMA3SC003M13"
PAGE = "/a3sc/ISMA3SC003M13.do"
TITLE = "A3 AutoFlow · 업무 자동화 | 에이쓰리시큐리티"
DESC = "사내에 설치한 AI가 부서별 반복 업무를 대신 처리하는 업무 자동화 플랫폼 A3 AutoFlow를 소개합니다."
ONECYCLE = "/a3sc/ISMA3SC003M5.do"  # One Cycle Dev. Framework 화면
PAGE_CSS = ['/resources/css/A3/renewal/onecycle_product.css']
# 운영 주소(제안값) → 미리보기 주소. index.html 을 만들 때만 쓴다.
ROUTES = {'/a3sc/ISMA3SC003M11.do': '../AIMES/', '/a3sc/ISMA3SC003M12.do': '../TruthLens/', '/a3sc/ISMA3SC003M13.do': '../A3-AutoFlow/', '/a3sc/ISMA3SC003M14.do': '../NexusAI/', '/a3sc/ISMA3SC003M15.do': '../Cluster-Master/', '/a3sc/ISMA3SC003M16.do': '../PokerFace-Pro/', '/a3sc/ISMA3SC003M5.do': 'https://wdlab1958.github.io/a3sc/', '/a3sc/ISMA3SC003M4.do': '../'}


def source() -> str:
    if not CACHE.exists():
        CACHE.parent.mkdir(exist_ok=True)
        req = urllib.request.Request(SRC_URL, headers={"User-Agent": "Mozilla/5.0"})
        CACHE.write_bytes(urllib.request.urlopen(req, timeout=30).read())
    return CACHE.read_text(encoding="utf-8")


def must_sub(pattern: str, repl: str, text: str, flags: int = 0) -> str:
    out, n = re.subn(pattern, lambda _m: repl, text, count=1, flags=flags)
    if n != 1:
        sys.exit(f"기존 화면 구조가 바뀌어 치환하지 못했습니다: {pattern}")
    return out


def main() -> None:
    html = source().lstrip()
    body = (ROOT / "fragment" / f"{PAGE_ID}_main.html").read_text(encoding="utf-8")

    # 본문 교체
    html = must_sub(r"<main>.*?</main>", "<main>\n" + body + "</main>", html, re.S)
    # 머리: 제목·설명·주소, 페이지 전용 스타일 추가
    html = must_sub(r"<title>.*?</title>", f"<title>{TITLE}</title>", html)
    html = re.sub(r'(<meta (?:name="description"|property="og:description") content=")[^"]*', lambda m: m.group(1) + DESC, html)
    html = must_sub(r'(?<=<meta property="og:title" content=")[^"]*', TITLE, html)
    html = html.replace("/a3sc/ISMA3SC003M4.do\">\n<meta property=\"al", PAGE + "\">\n<meta property=\"al")
    html = html.replace('rel="canonical" href="https://www.a3sc.co.kr/a3sc/ISMA3SC003M4.do"', f'rel="canonical" href="https://www.a3sc.co.kr{PAGE}"')
    html = html.replace('global_request_uri = "/a3sc/ISMA3SC003M4.do"', f'global_request_uri = "{PAGE}"')
    html = must_sub(r'<link rel="stylesheet" href="/resources/css/A3/renewal/b\.css">',
                    '<link rel="stylesheet" href="/resources/css/A3/renewal/b.css">'
                    + "".join(f'\n<link rel="stylesheet" href="{c}">' for c in PAGE_CSS), html)
    # 상단 메뉴: 「정보센터」 뒤에 One Cycle Dev. Framework 추가
    html = must_sub(r'(?<=class="">정보센터</a>)(?=</nav>)', f'<a href="{ONECYCLE}" class="">One Cycle Dev. Framework</a>', html)
    # 모바일 전체 메뉴와 바닥글의 「AI 플랫폼」 묶음: 플랫폼 6종으로 바꾸고 One Cycle 화면 추가
    item = f'<li><a href="{ONECYCLE}">One Cycle Framework</a></li>'
    html = must_sub(r'(?<=<li><a href="/a3sc/ISMA3SC003M4\.do#lineup">플랫폼 9종</a></li>)(?=<li><a href="/a3sc/ISMA3SC003M4\.do#contact">)', item, html)
    html = must_sub(r'(?<=<li><a href="/a3sc/ISMA3SC003M4\.do#lineup">플랫폼 9종</a></li>)(?=<li class="fam-off">)', item, html)
    html = html.replace("#lineup\">플랫폼 9종</a>", "#lineup\">플랫폼 6종</a>")
    # 미리보기에서는 기존 화면 전용 스크립트(게시판·세션·통계)를 뺀다
    html = re.sub(r"<!-- jquery.*?</script>\n</head>", "</head>", html, flags=re.S)

    (ROOT / f"{PAGE_ID}.html").write_text(html, encoding="utf-8")
    print(f"written: {PAGE_ID}.html", len(html), "bytes")

    # index.html: 폴더째 열어 볼 수 있게 자원은 상대 경로로,
    # AI 플랫폼 화면과 여섯 상세 화면은 서로의 폴더로, 그 밖의 링크는 실제 사이트로 보낸다. 검토용이므로 검색 노출을 막는다.
    pages = html.replace('"/resources/', '"resources/').replace("url(/resources/", "url(resources/")
    for path, live in sorted(ROUTES.items(), key=lambda kv: -len(kv[0])):
        pages = re.sub(r'href="' + re.escape(path) + r'(?=["#])', 'href="' + ("./" if path == PAGE else live), pages)
    pages = pages.replace('href="/a3sc/', 'href="https://www.a3sc.co.kr/a3sc/')
    pages = re.sub(r'<link rel="canonical"[^>]*>\n?', "", pages)
    pages = must_sub(r'(?<=<meta name="robots" content=")[^"]*', "noindex,nofollow", pages)
    (ROOT / "index.html").write_text(pages, encoding="utf-8")
    print("written: index.html", len(pages), "bytes")


if __name__ == "__main__":
    main()
