# 작업내역서

홈페이지 home.stock-snow.com 구축 기록. 나중에 점검할 때 **결정 사항 → 산출물 → 미결 사항** 순으로 보면 됩니다.

---

## 2026-09-19 — 초기 구축

### 1. 환경 준비

| 작업 | 결과 |
|---|---|
| GPG 서명 키 생성 | ed25519 `BCD6191E17FC4E74` (snowball &lt;snowb4631@gmail.com&gt;, 만료 2028-09-18), 폐기 인증서 `~/.gnupg/openpgp-revocs.d/` 에 보관 |
| git 저장소 초기화 | 브랜치 `main`, 저장소 한정 설정: `user.name=snowball`, `user.email=snowb4631@gmail.com`, `commit.gpgsign=true` |
| 원격 | `git@github.com-snowb4631:snowb4631/snowb-homepage.git` (SSH 별칭 — 기본 키는 klaud81 계정이라 push 권한 없음) |
| 제외 | `.omc/`, `MATERIALS.md`(내부 자료) → `.gitignore` |

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
| 디자인 | 아이스 블루 톤, Pretendard, 라이트/다크 자동, 눈덩이 임시 로고 | 기본값 |
| 호스팅 | GitHub Pages (branch 배포, 워크플로 불필요) | 기본값 |

### 3. 산출물

| 파일 | 내용 |
|---|---|
| `index.html` | Hero(슬로건 + 버핏 영문) · About(버핏 국문 + 가치 3카드) · Products(ai-trakit LIVE, SnowNote COMING) · Contact · 푸터 면책 고지·사업자 정보 |
| `privacy.html` | 개인정보처리방침 — 100m1s 구조(핵심 요약·광고 파트너·광고 식별자) + 사업계획서의 회원가입·결제·보안 내용 |
| `terms.html` | 이용약관 — 100m1s 구조 + 요금·청약철회/환불(사업계획서 Ⅳ-2)·유사투자자문 면책 |
| `site.css` · `menu.js` | 공통 스타일, 모바일 메뉴, reduced-motion 대응 |
| `logo.svg` · `favicon.svg` · `apple-touch-icon.png` · `og-image.*` | 임시 브랜드 이미지 |
| `CNAME` · `robots.txt` · `sitemap.xml` · `.nojekyll` | 배포 설정 |
| `scripts/preview.sh` | 로컬 미리보기 — `local`(루트) / `github`(하위 경로) 두 형태 |
| `README.md` · `SETUP.md` | 구조 설명, 배포·DNS 가이드 |
| Google Drive (aitrakit 폴더) | `snowball_개인정보처리방침 (홈페이지 게시본 2026-09-19)`, `snowball_이용약관 (홈페이지 게시본 2026-09-19)` — 게시본 사본 |

### 4. 검증

| 항목 | 결과 |
|---|---|
| 로컬 `local` 형태 (localhost:8000) — 전 리소스 200 | ✅ |
| 로컬 `github` 형태 (localhost:8001/snowb-homepage/) — 전 리소스 200 | ✅ |
| 데스크톱 1280px 렌더 (다크) | ✅ |
| 모바일 390px 렌더 — 가로 넘침 없음, 햄버거 메뉴 표시 | ✅ |
| 대표이사 성명 노출 0건 (html) | ✅ |
| GitHub Pages 실배포 | ⏳ push 권한 대기 |

---

## 미결 사항 (점검 시 확인)

- [ ] **push 권한**: snowb4631 계정에 SSH 키(`id_ed25519_snowb4631.pub`)와 GPG 키 등록 → SETUP.md 0단계
- [ ] **ai-trakit 소개 문구 확인**: 사업계획서는 "KOSPI·미국 ETF 리밸런싱 시그널, Pro 월 9,900원"이지만, 현재 trakit.stock-snow.com 화면은 "TQQQ Value Rebalancing Dashboard"(로그인·후원·AdSense). 홈페이지 카드 문구를 실제 서비스에 맞출지 결정 필요
- [ ] **ai-trakit 자체 개인정보처리방침**: 로그인 기능이 있으므로 trakit 사이트에도 방침 링크 필요 (현재 `/privacy` 경로 없음) → 홈페이지 privacy.html 링크 연결 권장
- [ ] **개인정보 보호책임자**: 성명 비노출로 "대표이사"만 표기 — 법령상 성명 또는 담당 부서·연락처 기재가 필요하므로 부서명(예: 개인정보보호 담당) 표기 검토
- [ ] 통신판매업 신고번호 · 유사투자자문업 신고번호 → 푸터·약관에 추가
- [ ] 결제대행사(PG) · 본인인증기관 업체명 → 개인정보처리방침 4.2
- [x] 로고: 회사 일러스트(설인 + "Snowball co.,ltd" 눈덩이)로 교체 — Hero 키 비주얼, 헤더·파비콘은 설인 얼굴 크롭, OG는 가로 크롭 (2026-09-19)
- [ ] 단순 로고 마크(작은 크기용 벡터) 필요 여부 — 현재 36px 헤더·파비콘은 일러스트 크롭이라 작은 크기에서 디테일이 뭉개질 수 있음
- [ ] SnowNote 제품명 확정 / 출시 시기
- [ ] DNS: `home` CNAME → `snowb4631.github.io`, HTTPS 강제
- [ ] 법무 문서 전문가 검토 (현재 초안 고지 포함)
