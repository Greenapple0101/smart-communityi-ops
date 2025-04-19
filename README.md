# Smart Community Ops - AWS 운영 자동화 포트폴리오

> 실무 배포 가능한 AWS 기반 운영 자동화 시스템

---

## 🚀 프로젝트 개요

- **프로젝트 이름**: Smart Community Ops
- **목표**: AWS CDK를 사용하여 서버리스 자동화 인프라를 배포하고, 매일 EC2/RDS 스냅샷을 생성·정리한 뒤 결과를 Slack으로 실시간 알림
- **주요 기술 스택**:
  - AWS CDK (Python)
  - AWS Lambda
  - Amazon EventBridge (스케줄러)
  - Amazon SNS (선택적 알림)
  - Slack Webhook
  - boto3, urllib3

---

## 📂 프로젝트 구조

```
smart-community-ops/
├── infra/                         # CDK 인프라 코드
│   ├── app.py                     # CDK 진입점
│   ├── cdk.json                   # CDK 설정
│   ├── ops_stack.py               # 스택 정의
│   └── requirements.txt           # Python 라이브러리 목록
├── lambdas/                       # Lambda 함수 코드
│   ├── backup_snapshots.py        # EC2/RDS 스냅샷 생성 및 삭제
│   └── notify.py                  # Slack/Webhook 알림 전송
├── .github/                       # GitHub Actions 워크플로우
│   └── deploy_infra.yml           # CDK 자동 배포 설정
├── README.md                      # 프로젝트 설명 (이 파일)
└── .gitignore                     # Git 무시 파일 설정
```

---

## 🔧 주요 기능

1. **EC2/RDS 스냅샷 자동 생성**: 매일 UTC 02:00에 모든 EC2 볼륨과 RDS 인스턴스의 스냅샷 생성
2. **오래된 스냅샷 자동 삭제**: 설정된 보존 기간(기본 30일) 이후 스냅샷 자동 삭제
3. **Slack 알림**: 백업 생성/삭제 결과를 Slack Webhook으로 전송하여 실시간 모니터링
4. **CDK 기반 인프라 코드**: GitHub Actions와 연계, 코드 변경 시 자동 배포 가능

---

## ⚙️ 배포 및 실행 가이드

### 1. 사전 준비
- AWS 계정 및 IAM 사용자 (Programmatic Access 권한)
- AWS CLI 설정(`aws configure`)
- Node.js, npm 설치 (CDK CLI)
- Python 3.9 이상 설치

### 2. CDK CLI 설치
```bash
npm install -g aws-cdk
cdk --version
```

### 3. 가상환경 생성 및 라이브러리 설치
```bash
cd infra
python -m venv .venv
# PowerShell:
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
& ./.venv/Scripts/Activate.ps1
# 또는 CMD:
# .venv\Scripts\activate.bat

pip install --upgrade pip
pip install -r requirements.txt aws-cdk-lib constructs boto3 urllib3
```

### 4. CDK 부트스트랩 (최초 1회)
```bash
cdk bootstrap aws://<AWS_ACCOUNT_ID>/ap-northeast-2 \
  --app ".\.venv\Scripts\python.exe app.py"
```

### 5. 스택 배포
```bash
cdk synth  --app ".\.venv\Scripts\python.exe app.py"
cdk deploy --app ".\.venv\Scripts\python.exe app.py"
```

### 6. Lambda 테스트
1. AWS Console → Lambda → `SmartCommunityOpsStack-BackupFn...` → [테스트] 실행
2. AWS Console → Lambda → `SmartCommunityOpsStack-NotifyFn...` → 이벤트 JSON 입력 후 [테스트]
3. Slack 채널에서 알림 확인

---

## 📖 코드 설명

### `backup_snapshots.py`
- `create_ec2_snapshots()`: 모든 EC2 인스턴스의 EBS 볼륨 스냅샷 생성
- `create_rds_snapshots()`: 모든 RDS 인스턴스의 DB 스냅샷 생성
- `delete_old_*_snapshots()`: 30일 이상 스냅샷 자동 삭제

### `notify.py`
- Slack Webhook 또는 SNS Topic으로 실행 결과 전송
- 알림 메시지에 생성/삭제 개수 및 실행 일시 포함

### `ops_stack.py`
- SNS Topic 및 Lambda 함수 정의
- EventBridge 스케줄링 (매일 UTC 02:00)
- Lambda 권한(EC2, RDS, SNS 퍼블리시) 배정

---

## 🎯 학습 포인트
- **Infrastructure as Code**: AWS CDK로 인프라 정의 및 배포 자동화
- **Serverless 운영 자동화**: Lambda + EventBridge로 주기 작업 구성
- **실시간 알림**: Slack Webhook과 통합하여 DevOps 모니터링 구축
- **Cost Optimization**: 스냅샷 보존 주기 자동화로 스토리지 비용 절감

---

## 👷‍♂️ CI/CD (옵션)
- `.github/workflows/deploy_infra.yml`을 통해 main 브랜치 푸시 시 인프라 자동 배포

---

## 📝 LICENSE
MIT License

