# 작업내역서

홈페이지 home.stock-snow.com 구축 기록. 나중에 점검할 때 **결정 사항 → 산출물 → 배포 → 미결 사항** 순으로 보면 됩니다.

---

## 2026-09-19 — 초기 구축 · 배포

### 1. 환경 준비

| 작업 | 결과 |
|---|---|
| GPG 서명 키 생성 | ed25519 `BCD6191E17FC4E74` (snowball &lt;snowb4631@gmail.com&gt;, 만료 2028-09-18), 폐기 인증서 `~/.gnupg/openpgp-revocs.d/` 에 보관 |
| git 저장소 초기화 | 브랜치 `main`, 저장소 한정 설정: `user.name=snowball`, `user.email=snowb4631@gmail.com`, `commit.gpgsign=true` |
| 원격 | `git@github.com-snowb4631:snowb4631/snowb-homepage.git` (SSH 별칭 — 이 PC 기본 키는 klaud81 계정이라 push 권한 없음) |
| GitHub 키 등록 | snowb4631 계정에 GPG 키(커밋 Verified) + SSH 키 `id_ed25519_snowb4631.pub`(push) 등록 완료 |
| 제외 | `.omc/`, `MATERIALS.md`(내부 자료: 법인등록번호·상세 주소 등) → `.gitignore` |

### 2. 자료 수집 · 결정 사항

| 항목 | 결정 | 근거 |
|---|---|---|
| 참고 사이트 | nicehugepark/100m1s-homepage 구조 (Hero / About / Products / Contact / 법무 2종) | 사용자 지시 |
| 회사명 | 주식회사 스노우볼 (snowball Co., Ltd.) | 사업자 정보 이미지 |
| 슬로건 | 먼저 한 걸음, 끝은 창대하리. | 사용자 |
| 브랜드 인용 | 워런 버핏 "Life is like a snowball…" — Hero 영문 부제 + About 국문 | 사용자 선택 |
| 사업 분야 | AI 기반 투자 정보 (유사투자자문업, 자본시장법 제101조) | ai-trakit 사업계획서 |
| 표현 원칙 | "투자업"·"자산운용"·"수익 보장" 등 금지, 유사투자자문업자 고지 필수 | 사업계획서 Ⅴ-1 광고 규제 |
| 제품 P001 | ai-trakit — LIVE, trakit.stock-snow.com | 사업계획서 |
| 제품 P002 | SnowNote (가칭) — AI 메모장, TODO → 카드 COMING | 대표 기획 메모 (2026-09-15) |
| SnowNote 형태 | 자체 메모 앱, UI만 디스코드 **형식** (디스코드 연동 아님) | 사용자 정정 |
| 도메인 | home.stock-snow.com | 사용자 |
| 연락 이메일 | snowb4631@gmail.com | 사용자 (contact@stock-snow.com 에서 변경) |
| 대표이사 성명 | **홈페이지·법무 문서에 노출하지 않음** | 사용자 지시 |
| 주소 노출 | "경기도 화성시" 까지만 (자택 사무실) | 기본값 |
| 로고 · 키 비주얼 | 회사 일러스트 (설인 + "Snowball co.,ltd" 눈덩이) | 사용자 제공 이미지 |
| 디자인 | 아이스 블루 톤, Pretendard, 라이트/다크 자동 | 기본값 |
| 호스팅 | GitHub Pages (branch 배포, 워크플로 불필요) | 기본값 |

### 3. 산출물

| 파일 | 내용 |
|---|---|
| `index.html` | Hero(슬로건 + 버핏 영문 + 키 비주얼) · About(버핏 국문 + 가치 3카드) · Products(ai-trakit LIVE, SnowNote COMING) · Contact · 푸터 면책 고지·사업자 정보 |
| `privacy.html` | 개인정보처리방침 — 100m1s 구조(핵심 요약·광고 파트너·광고 식별자) + 사업계획서의 회원가입·결제·보안 내용 |
| `terms.html` | 이용약관 — 100m1s 구조 + 요금·청약철회/환불(사업계획서 Ⅳ-2)·유사투자자문 면책 |
| `site.css` · `menu.js` | 공통 스타일, 모바일 메뉴, reduced-motion 대응 |
| `assets/hero-800.jpg` · `assets/hero-1400.jpg` | 키 비주얼 (원본 1402×1122 PNG 2.7MB → JPEG 240KB/620KB) |
| `assets/logo-96.png` · `favicon.png` · `apple-touch-icon.png` | 설인 얼굴 크롭 (헤더 로고·파비콘·iOS 아이콘) |
| `og-image.jpg` | 링크 공유 미리보기 1200×630 (일러스트 가로 크롭) |
| `CNAME` · `robots.txt` · `sitemap.xml` · `.nojekyll` | 배포 설정 |
| `scripts/preview.sh` | 로컬 미리보기 — `local`(루트) / `github`(하위 경로) 두 형태 |
| `README.md` · `SETUP.md` | 구조 설명, 배포·DNS 가이드 |
| Google Drive (aitrakit 폴더) | `snowball_개인정보처리방침 (홈페이지 게시본 2026-09-19)`, `snowball_이용약관 (홈페이지 게시본 2026-09-19)` — 게시본 사본 (최종본만 유지, 이전 버전 4개는 휴지통) |

### 4. 배포

| 단계 | 결과 |
|---|---|
| push | `main` — 커밋 서명 GitHub **Verified** |
| Pages | Deploy from a branch · `main` / `(root)` · 빌드 `built` |
| DNS | Cloudflare (`stock-snow.com` NS: athena/tosana.ns.cloudflare.com) — `CNAME home → snowb4631.github.io`, **DNS only (회색 구름)** |
| HTTPS | 인증서 발급 (CN=home.stock-snow.com, 만료 2026-12-18, 자동 갱신) · **Enforce HTTPS 켜짐** (http → https 301) |
| 참고 | Pages 설정에서 Custom domain 을 지웠다 다시 넣을 때마다 GitHub 이 `Create/Delete CNAME` 커밋을 자동 생성 — 원격에 6개 쌓였고 로컬에 fast-forward 반영 |
| 참고 | 레코드 추가 직후 "InvalidDNSError / Enforce HTTPS unavailable" 표시는 일시적 — 인증서 발급 후 새로고침으로 해소 |

### 5. 검증

| 항목 | 결과 |
|---|---|
| 로컬 `local` 형태 (localhost:8000) — 전 리소스 200 | ✅ |
| 로컬 `github` 형태 (localhost:8001/snowb-homepage/) — 전 리소스 200 | ✅ |
| 데스크톱 1280px 렌더 (다크) · 키 비주얼 표시 | ✅ |
| 모바일 390px 렌더 — 가로 넘침 없음, 햄버거 메뉴, 800w 이미지 | ✅ |
| 대표이사 성명 노출 0건 (html) | ✅ |
| https://home.stock-snow.com — 200, 페이지 제목 정상 | ✅ |
| http → https 리다이렉트 | ✅ |

---

## 2026-09-19 — Hero 캐러셀 · 아이콘 통일

### 1. 결정 사항

| 항목 | 결정 | 근거 |
|---|---|---|
| 메인 이미지 | 키 비주얼 1장 → 같은 시리즈 6장 캐러셀 (키 비주얼 · 대시보드 · 데이터 탐색 · 차트 분석 · 퀀트 · SnowNote) | 사용자 요청 |
| 시리즈 표현 | 설산 배경 · 아이스 블루 · "Snowball co.,ltd" 눈덩이 모티프 + 제품 UI 카드 (SVG, 생성 스크립트) | 원본이 일러스트라 래스터 신규 생성 불가 → 벡터 목업 |
| 상승/하락 색 | 상승 빨강 · 하락 파랑 | 국내 관례 |
| SnowNote 이미지 | 디스코드 **형식** 레이아웃 (주제 레일 · 채널 목록 · 기록 흐름 · 마크다운 입력 · AI 메모리 내보내기/가져오기) | 대표 기획 메모 |
| 예시 수치 고지 | 캐러셀 아래 "예시이며 실제 서비스 성과가 아닙니다 · 과거 성과가 미래 수익을 보장하지 않습니다" | 유사투자자문업 광고 규제 (사용자 승인) |
| 넘김 방식 | 원형 큐 (양 끝 복제 슬라이드) — 마지막→첫 장, 첫 장→마지막 장 | 사용자 요청 |
| 자동 넘김 | 5초, hover·포커스·화면 밖·탭 숨김 시 일시정지, ⏸/▶ 버튼, reduced-motion 시 꺼짐 | 사용자 요청 + WCAG 2.2.2 |
| 입력 | 터치 스와이프 · 트랙패드 · 마우스 드래그 · ‹ › 버튼 · 점 · 키보드 ←/→ | 사용자 요청 ("오른쪽 스크롤") |
| 파비콘 · 헤더 로고 | 설인 얼굴 → "Snowball co.,ltd" 눈덩이 크롭으로 통일 | 사용자 요청 |
| 저작권 연도 | © 2026 → © 2025 (설립연도) | 사용자 (기존 미커밋 변경) |

### 2. 산출물

| 파일 | 내용 |
|---|---|
| `assets/hero-{dashboard,search,chart,quant,snownote}.svg` | 캐러셀 슬라이드 1400×1120 (각 21–28KB) |
| `scripts/gen-hero-slides.py` | 슬라이드 생성기 — 표준 라이브러리만, 시드 고정 |
| `carousel.js` | 캐러셀 동작 (원형 큐 · 자동 넘김 · 드래그 · 키보드 · 점 동기화) |
| `index.html` · `site.css` | `.hero-visual` → 캐러셀 마크업·스타일, 안내 문구 `.hero-note` |
| `favicon.png`(48) · `apple-touch-icon.png`(180) · `assets/logo-96.png` | 키 비주얼 1400px 의 눈덩이 영역(460×460) 크롭 |
| `SETUP.md` | CSS·JS 캐시 버전(`?v=`) 운영 규칙 추가 |

### 3. 배포 · 검증

| 커밋 | 내용 |
|---|---|
| `15c0f48` | 저작권 연도 2025 |
| `052dfa5` | 캐러셀 + 슬라이드 5종 |
| `d9bb5e8` | 자동 넘김 · 원형 순환 · 드래그 · 예시 안내 문구 |
| `b5555de` | CSS·JS 캐시 무효화 `?v=20260919b` |
| `4b75abc` | 파비콘·헤더 로고 통일 (`?v=2`) |

| 항목 | 결과 |
|---|---|
| 실도메인 — 슬라이드 SVG 5종 200 `image/svg+xml`, 이미지 8장(복제 포함) 로드 | ✅ |
| 실도메인 — 첫 장 ‹ → 마지막 장, 마지막 장 › → 첫 장, 점 이동, 드래그 좌/우, 5초 자동 넘김 | ✅ |
| 모바일 390px — 가로 넘침 없음, 버튼 숨김(스와이프) | ✅ |
| 실도메인 아이콘 3종 — 로컬 파일과 해시 일치, 헤더 로고 표시 | ✅ |
| 부드러운 스크롤 애니메이션 육안 확인 | ⚠ 테스트 탭이 백그라운드라 미확인 (로직은 즉시 스크롤로 검증) |
| 문제 → 해결 | 첫 배포 직후 실도메인에서 캐러셀 무반응 — Pages `max-age=600` 로 새 HTML + 옛 `carousel.js`/`site.css` 가 섞여 로드됨 → 버전 쿼리로 해결 |

---

## 미결 사항 (점검 시 확인)

- [x] push 권한 — snowb4631 계정 SSH·GPG 키 등록 (2026-09-19)
- [x] DNS `home` CNAME + HTTPS 강제 (2026-09-19)
- [x] 로고: 회사 일러스트로 교체 (2026-09-19)
- [ ] **ai-trakit 소개 문구 확인**: 사업계획서는 "KOSPI·미국 ETF 리밸런싱 시그널, Pro 월 9,900원"이지만, 현재 trakit.stock-snow.com 화면은 "TQQQ Value Rebalancing Dashboard"(로그인·후원·AdSense). 홈페이지 카드 문구를 실제 서비스에 맞출지 결정 필요
- [ ] **ai-trakit 자체 개인정보처리방침**: 로그인 기능이 있으므로 trakit 사이트에도 방침 링크 필요 (현재 `/privacy` 경로 없음) → https://home.stock-snow.com/privacy.html 링크 연결 권장
- [ ] **개인정보 보호책임자**: 성명 비노출로 "대표이사"만 표기 — 법령상 성명 또는 담당 부서·연락처 기재가 필요하므로 부서명(예: 개인정보보호 담당) 표기 검토
- [ ] 통신판매업 신고번호 · 유사투자자문업 신고번호 → 푸터·약관에 추가
- [ ] 결제대행사(PG) · 본인인증기관 업체명 → 개인정보처리방침 4.2
- [ ] 단순 로고 마크(작은 크기용 벡터) 필요 여부 — 헤더·파비콘을 눈덩이 크롭으로 바꿨지만 48px 이하에서는 "co.,ltd" 가 읽히지 않음
- [ ] 캐러셀 이미지 속 예시 수치 — 실제 공개 성과가 생기면 교체 검토 (그 전까지 `.hero-note` 유지)
- [ ] og-image.jpg 는 아직 기존 키 비주얼 크롭 — 캐러셀·아이콘과 맞출지 결정
- [ ] 캐러셀 부드러운 스크롤 실기기(데스크톱·iOS·Android) 육안 확인
- [ ] SnowNote 제품명 확정 / 출시 시기
- [ ] 카카오톡 링크 미리보기(og-image.jpg) 실기기 확인
- [ ] 법무 문서 전문가 검토 (현재 초안 고지 포함)
