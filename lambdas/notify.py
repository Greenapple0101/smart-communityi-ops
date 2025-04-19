import json
import urllib3
import os

http = urllib3.PoolManager()

# Webhook URL (보통은 환경변수로 두지만, 지금은 직접 넣을게요!)
SLACK_WEBHOOK_URL = "https://hooks.slack.com/services/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"

def handler(event, context):
    created_ec2 = event.get("created_ec2", [])
    created_rds = event.get("created_rds", [])
    deleted_ec2 = event.get("deleted_ec2", [])
    deleted_rds = event.get("deleted_rds", [])

    msg = f"""
📦 *AWS 자동 백업 보고서*

✅ 생성된 EC2 스냅샷: `{len(created_ec2)}`
✅ 생성된 RDS 스냅샷: `{len(created_rds)}`
🧹 삭제된 EC2 스냅샷: `{len(deleted_ec2)}`
🧹 삭제된 RDS 스냅샷: `{len(deleted_rds)}`

📅 실행 일시: `{context.timestamp if hasattr(context, "timestamp") else "N/A"}`
🔁 람다 실행 완료
    """

    message = {
        "text": msg
    }

    encoded_data = json.dumps(message).encode("utf-8")
    resp = http.request(
        "POST",
        SLACK_WEBHOOK_URL,
        body=encoded_data,
        headers={"Content-Type": "application/json"}
    )

    print(f"✅ Slack 응답 코드: {resp.status}")
    return {"status": resp.status}
