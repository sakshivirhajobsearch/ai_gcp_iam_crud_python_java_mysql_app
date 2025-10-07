def analyze_iam_permissions(iam_users):
    """
    AI analysis for IAM data:
    - Flags disabled users who are still active.
    - Flags users with suspicious domains.
    - Dummy check for excessive roles.
    """
    alerts = []

    suspicious_domains = ["example.com", "test.com"]

    for user in iam_users:
        email = user.get('email', '')
        name = user.get('name', '')
        disabled = user.get('disabled', False)

        if disabled:
            alerts.append(f"⚠️ Disabled user {email} is still listed in IAM.")

        if any(domain in email for domain in suspicious_domains):
            alerts.append(f"⚠️ User {email} uses a suspicious domain.")

        if len(name) > 15:  # dummy example
            alerts.append(f"⚠️ User {email} may have excessive roles.")

    if not alerts:
        alerts.append("✅ No anomalies detected.")

    return alerts
