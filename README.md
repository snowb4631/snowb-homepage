# home.stock-snow.com — 주식회사 스노우볼 홈페이지

> 먼저 한 걸음, 끝은 창대하리.

빌드 없는 정적 HTML 1페이지 회사 홈페이지. 참고: [100m1s-homepage](https://github.com/nicehugepark/100m1s-homepage)

## 구조

```
.
├── index.html            # 메인 (Hero 캐러셀 / About / Products / Contact)
├── privacy.html          # 개인정보처리방침
├── terms.html            # 이용약관
├── site.css              # 공통 스타일 (라이트/다크 토큰)
├── menu.js               # 모바일 메뉴 + 카드 부유 모션
├── carousel.js           # Hero 캐러셀 (원형 순환 · 5초 자동 넘김 · 드래그 · 키보드)
├── assets/               # hero-800/1400.jpg (키 비주얼), hero-*.svg (캐러셀 슬라이드 5종), logo-96.png (헤더 로고)
├── favicon.png · apple-touch-icon.png   # 'Snowball co.,ltd' 눈덩이 크롭 (헤더 로고와 동일)
├── og-image.jpg          # 링크 공유 미리보기 (1200×630, 키 비주얼 크롭)
├── CNAME                 # home.stock-snow.com
├── robots.txt · sitemap.xml · .nojekyll
├── scripts/preview.sh    # 로컬 미리보기 (local / github 두 형태)
├── scripts/gen-hero-slides.py  # 캐러셀 SVG 슬라이드 생성기 (표준 라이브러리만)
├── SETUP.md              # 배포 + DNS 가이드
└── WORKLOG.md            # 작업내역서
```

모든 내부 링크는 **상대 경로**라서 루트(`/`)와 하위 경로(`/snowb-homepage/`) 어디에 올려도 동작합니다.

## 로컬 미리보기

```bash
scripts/preview.sh          # 두 형태 동시 실행
scripts/preview.sh local    # http://localhost:8000/               — 커스텀 도메인 형태
scripts/preview.sh github   # http://localhost:8001/snowb-homepage/ — github.io 기본 주소 형태
```

## Hero 캐러셀

메인 이미지는 6장 캐러셀입니다: 키 비주얼 → 대시보드 → 데이터 탐색 → 차트 분석 → 퀀트 → SnowNote.

- 슬라이드 SVG 수정: `scripts/gen-hero-slides.py` 를 고친 뒤 `python3 scripts/gen-hero-slides.py` (시드 고정 — 결과가 매번 같음)
- 슬라이드 추가: 생성기에 함수 추가 → `index.html` 에 `.hero-slide` + 점(`role="tab"`) 추가, `aria-label="n / 전체"` 갱신
- 이미지 속 수치는 **예시** — 캐러셀 아래 안내 문구(`.hero-note`)를 지우지 말 것 (유사투자자문업 광고 규제)
- `site.css`·`*.js` 를 고치면 HTML 의 `?v=` 값을 올릴 것 (GitHub Pages 10분 캐시, [SETUP.md](./SETUP.md) 참고)

## 배포

GitHub Pages — `main` 브랜치 루트를 그대로 배포 (빌드·워크플로 불필요). 자세한 절차는 [SETUP.md](./SETUP.md).

- Production: https://home.stock-snow.com
- 기본 주소: https://snowb4631.github.io/snowb-homepage/ (커스텀 도메인 연결 후 자동 리다이렉트)

© 2025 snowball Co., Ltd.
