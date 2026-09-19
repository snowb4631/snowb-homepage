# 배포 + DNS 설정 가이드

목표: `https://home.stock-snow.com` 에 이 저장소(`snowb4631/snowb-homepage`)를 GitHub Pages 로 배포.

## GitHub Actions 워크플로가 필요한가?

**필요 없습니다.** 빌드 과정이 없는 정적 HTML이라 Pages 의 "Deploy from a branch" 방식으로 `main` 에 push 하는 즉시 배포됩니다.
(Pages 가 내부적으로 `pages-build-deployment` 액션을 자동 실행하므로 Actions 탭에 실행 기록은 보입니다.)
워크플로는 나중에 링크 검사·HTML 검증 같은 사전 점검을 넣고 싶을 때 추가하면 됩니다.

---

## 0단계: push 권한 (1회)

이 PC의 `~/.ssh/config` 에 `github.com-snowb4631` 별칭이 있고, 원격은 이미 이 별칭을 씁니다.

```
origin → git@github.com-snowb4631:snowb4631/snowb-homepage.git
```

1. **snowb4631** 계정으로 GitHub 로그인 → Settings → SSH and GPG keys
2. **New SSH key** → `~/.ssh/id_ed25519_snowb4631.pub` 내용 붙여넣기
3. **New GPG key** → `gpg --armor --export BCD6191E17FC4E74` 결과 붙여넣기 (커밋 Verified 표시용)
4. 확인: `ssh -T git@github.com-snowb4631` → `Hi snowb4631!`

## 1단계: push

```bash
git push -u origin main
```

## 2단계: Pages 켜기 (1회)

1. 저장소 → Settings → **Pages**
2. Source: **Deploy from a branch** · Branch: **main** / **(root)** → Save
3. 1~2분 뒤 `https://snowb4631.github.io/snowb-homepage/` 에서 확인 ← **GitHub 배포 테스트**
4. Custom domain 칸에 `home.stock-snow.com` 이 자동으로 채워짐 (CNAME 파일)

## 3단계: DNS (1회)

`stock-snow.com` 을 관리하는 DNS(가비아 / Route 53 등)에 레코드 1개 추가:

| 타입 | 이름 | 값 |
|---|---|---|
| CNAME | `home` | `snowb4631.github.io` |

- 루트 도메인이 아니므로 A 레코드는 필요 없습니다.
- 기존 `trakit.stock-snow.com` 레코드는 건드리지 않습니다.
- 확인: `dig +short home.stock-snow.com` → `snowb4631.github.io.` 와 GitHub IP 가 나오면 성공

## 4단계: HTTPS

DNS 반영 후(수 분~수 시간) Settings → Pages 에서 DNS check 가 통과하면 **Enforce HTTPS** 체크.

## 배포 테스트 체크리스트

| 단계 | 주소 | 확인 |
|---|---|---|
| 로컬 (커스텀 도메인 형태) | `scripts/preview.sh local` → http://localhost:8000/ | 레이아웃·링크 |
| 로컬 (github.io 형태) | `scripts/preview.sh github` → http://localhost:8001/snowb-homepage/ | 하위 경로에서 CSS·이미지·링크 |
| GitHub Pages | https://snowb4631.github.io/snowb-homepage/ | 실제 배포본 |
| 운영 | https://home.stock-snow.com | DNS·HTTPS |
| 링크 미리보기 | 카카오톡에 URL 전송 / [opengraph.xyz](https://www.opengraph.xyz) | og-image.png 노출 |

카카오톡은 미리보기를 캐시합니다. 이미지를 바꾼 뒤에는 [카카오 공유 디버거](https://developers.kakao.com/tool/debugger/sharing)에서 캐시를 초기화하세요.
