# Pipeline Failure Notifications Setup

This guide explains how to configure failure notifications for your CI/CD pipeline.

## Overview

The pipeline includes automatic failure notifications that trigger when:
- ✅ Build or test steps fail
- ✅ Staging deployment fails
- ✅ Production deployment fails (critical alert)

**Current Status:** Logging to pipeline console (enabled by default)

## Notification Channels

### 1. Slack Integration (Recommended)

**Setup:**

1. **Create Slack Webhook:**
   - Go to https://api.slack.com/apps
   - Create new app → From scratch
   - Add "Incoming Webhooks" feature
   - Activate and create webhook for your channel
   - Copy the webhook URL

2. **Add Secret to CloudBees Unify:**
   - Navigate to Settings → Secrets
   - Add secret: `SLACK_WEBHOOK_URL`
   - Value: Your webhook URL

3. **Enable in Pipeline:**
   - Edit `.cloudbees/workflows/ci-cd-pipeline.yaml`
   - Uncomment the Slack notification code (line ~137)
   - Push changes

**Example Notification:**
```json
{
  "text": "🚨 Pipeline Failed",
  "blocks": [
    {
      "type": "section",
      "text": {
        "type": "mrkdwn",
        "text": "*Pipeline Failure Alert*\n❌ Repository: UNIFY-PYTHON-SAMPLE-APP\n🌿 Branch: main\n📝 Commit: a1b2c3d4"
      }
    }
  ]
}
```

### 2. Email Notifications

**Setup:**

1. **Configure SMTP Settings:**
   Add these secrets to CloudBees Unify:
   - `SMTP_HOST` - Your SMTP server (e.g., smtp.gmail.com)
   - `SMTP_PORT` - Port (usually 587)
   - `SMTP_USERNAME` - Your email
   - `SMTP_PASSWORD` - App password or SMTP password
   - `NOTIFY_EMAIL` - Recipient email address

2. **Add Email Step to Pipeline:**

```yaml
- name: Send email notification
  if: failure()
  uses: docker://alpine:latest
  shell: sh
  env:
    SMTP_HOST: ${{ secrets.SMTP_HOST }}
    SMTP_USERNAME: ${{ secrets.SMTP_USERNAME }}
    SMTP_PASSWORD: ${{ secrets.SMTP_PASSWORD }}
    NOTIFY_EMAIL: ${{ secrets.NOTIFY_EMAIL }}
  run: |
    apk add --no-cache mailx
    echo "Pipeline failed for ${CLOUDBEES_SCM_BRANCH}" | \
      mailx -s "Pipeline Failure Alert" \
      -S smtp=$SMTP_HOST:587 \
      -S smtp-use-starttls \
      -S smtp-auth=login \
      -S smtp-auth-user=$SMTP_USERNAME \
      -S smtp-auth-password=$SMTP_PASSWORD \
      $NOTIFY_EMAIL
```

### 3. Microsoft Teams

**Setup:**

1. **Create Teams Webhook:**
   - Open Teams channel
   - Click "..." → Connectors → Incoming Webhook
   - Configure and copy webhook URL

2. **Add Secret:**
   - `TEAMS_WEBHOOK_URL` in CloudBees Unify

3. **Add to Pipeline:**

```yaml
- name: Send Teams notification
  if: failure()
  uses: docker://curlimages/curl:latest
  shell: sh
  env:
    TEAMS_WEBHOOK_URL: ${{ secrets.TEAMS_WEBHOOK_URL }}
  run: |
    curl -H "Content-Type: application/json" -d '{
      "@type": "MessageCard",
      "themeColor": "FF0000",
      "title": "Pipeline Failure",
      "text": "Build failed for '"${CLOUDBEES_SCM_BRANCH}"'"
    }' $TEAMS_WEBHOOK_URL
```

### 4. PagerDuty (For Critical Alerts)

**Setup:**

1. **Get PagerDuty Integration Key:**
   - Service → Integrations → Add Integration
   - Choose "Events API v2"
   - Copy the Integration Key

2. **Add Secret:**
   - `PAGERDUTY_INTEGRATION_KEY` in CloudBees Unify

3. **Add to Pipeline:**

```yaml
- name: Send PagerDuty alert
  if: failure()
  uses: docker://curlimages/curl:latest
  shell: sh
  env:
    PAGERDUTY_KEY: ${{ secrets.PAGERDUTY_INTEGRATION_KEY }}
  run: |
    curl -X POST https://events.pagerduty.com/v2/enqueue \
      -H "Content-Type: application/json" \
      -d '{
        "routing_key": "'"$PAGERDUTY_KEY"'",
        "event_action": "trigger",
        "payload": {
          "summary": "Pipeline Failure: '"${CLOUDBEES_SCM_BRANCH}"'",
          "severity": "critical",
          "source": "CloudBees Unify"
        }
      }'
```

### 5. Discord

**Setup:**

1. **Create Discord Webhook:**
   - Server Settings → Integrations → Webhooks
   - Create webhook and copy URL

2. **Add Secret:**
   - `DISCORD_WEBHOOK_URL` in CloudBees Unify

3. **Add to Pipeline:**

```yaml
- name: Send Discord notification
  if: failure()
  uses: docker://curlimages/curl:latest
  shell: sh
  env:
    DISCORD_WEBHOOK_URL: ${{ secrets.DISCORD_WEBHOOK_URL }}
  run: |
    curl -H "Content-Type: application/json" -d '{
      "content": "🚨 **Pipeline Failed**",
      "embeds": [{
        "title": "Build Failure",
        "description": "Branch: '"${CLOUDBEES_SCM_BRANCH}"'\nCommit: '"${CLOUDBEES_SCM_COMMIT:0:8}"'",
        "color": 15158332
      }]
    }' $DISCORD_WEBHOOK_URL
```

## Notification Best Practices

### ✅ Do:
- Use different channels for different severity levels
- Include relevant context (branch, commit, logs link)
- Set up notifications early in development
- Test notifications regularly
- Use threading/replies to reduce noise

### ❌ Don't:
- Send notifications for every minor failure
- Expose sensitive data in notifications
- Use personal accounts for automated notifications
- Forget to test the notification flow
- Spam channels with duplicate messages

## Troubleshooting

### Issue: Notifications not sending

**Solution:**
1. Check secrets are correctly configured
2. Verify webhook URLs are valid
3. Check CloudBees logs for error messages
4. Test webhook manually with curl

### Issue: Rate limiting errors

**Solution:**
- Slack: Implement backoff strategy
- Email: Use batch notifications
- Consider notification aggregation

### Issue: Notifications missing context

**Solution:**
Add more CloudBees variables:
- `${CLOUDBEES_SCM_AUTHOR}` - Who triggered the build
- `${CLOUDBEES_RUN_URL}` - Link to build logs
- `${CLOUDBEES_RUN_ID}` - Unique build ID

## Testing Notifications

To test your notification setup:

1. **Create a test branch:**
   ```bash
   git checkout -b test-notifications
   ```

2. **Break a test intentionally:**
   ```python
   # In test_app.py
   def test_intentional_failure():
       assert False, "Testing notification system"
   ```

3. **Push and watch:**
   ```bash
   git add test_app.py
   git commit -m "Test: trigger notification"
   git push origin test-notifications
   ```

4. **Verify notification received**

5. **Clean up:**
   ```bash
   git checkout main
   git branch -D test-notifications
   git push origin --delete test-notifications
   ```

## Advanced Configuration

### Conditional Notifications

Send notifications only for specific branches:

```yaml
- name: Send critical production alert
  if: failure() && cloudbees.scm.branch == 'main'
  run: |
    # Send to PagerDuty for production failures only
```

### Rich Notifications

Include more context:

```yaml
run: |
  FAILED_STEP=$(echo "$CLOUDBEES_STEP_NAME" | grep -o "failed")
  curl -X POST $SLACK_WEBHOOK_URL -d '{
    "text": "Pipeline Failed",
    "attachments": [{
      "color": "danger",
      "fields": [
        {"title": "Repository", "value": "UNIFY-PYTHON-SAMPLE-APP"},
        {"title": "Branch", "value": "'"$CLOUDBEES_SCM_BRANCH"'"},
        {"title": "Commit", "value": "'"$CLOUDBEES_SCM_COMMIT"'"},
        {"title": "Author", "value": "'"$CLOUDBEES_SCM_AUTHOR"'"},
        {"title": "Failed Step", "value": "'"$FAILED_STEP"'"}
      ],
      "actions": [{
        "type": "button",
        "text": "View Logs",
        "url": "'"$CLOUDBEES_RUN_URL"'"
      }]
    }]
  }'
```

## Support

- **CloudBees Unify:** Contact your administrator
- **Slack API:** https://api.slack.com/docs
- **Email Issues:** Check SMTP settings
- **PagerDuty:** https://support.pagerduty.com

---

**Last Updated:** 2026-03-17
**Maintained by:** TEJAS DESAI (tdesai@cloudbees.com)
