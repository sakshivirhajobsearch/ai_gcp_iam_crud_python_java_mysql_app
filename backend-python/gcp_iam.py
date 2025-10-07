from config import USE_DUMMY, credentials
if not USE_DUMMY:
    from googleapiclient.discovery import build

def list_iam_users(project_id=None):
    """
    Fetch IAM users from GCP if USE_DUMMY=False
    Otherwise, return dummy users for demo
    """
    if USE_DUMMY:
        # ---------- Dummy IAM users ----------
        return [
            {'name': 'Alice Admin', 'email': 'alice.admin@example.com', 'disabled': False},
            {'name': 'Bob Dev', 'email': 'bob.dev@test.com', 'disabled': False},
            {'name': 'Charlie Ops', 'email': 'charlie.ops@example.com', 'disabled': True},
            {'name': 'David QA', 'email': 'david.qa@example.com', 'disabled': False},
            {'name': 'Eve Manager', 'email': 'eve.manager@example.com', 'disabled': False},
        ]

    # ---------- Real GCP IAM fetching ----------
    if not project_id:
        raise ValueError("project_id is required for real GCP IAM fetching.")

    service = build('iam', 'v1', credentials=credentials)
    request = service.projects().serviceAccounts().list(name=f'projects/{project_id}')
    response = request.execute()

    users = []
    for account in response.get('accounts', []):
        users.append({
            'name': account['name'],
            'email': account['email'],
            'disabled': account.get('disabled', False)
        })

    return users
