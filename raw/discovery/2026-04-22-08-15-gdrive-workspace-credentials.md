# 2026-04-22-08-15-gdrive-workspace-credentials

**Status: [closed]**

## Objective

Research and define the implementation path for Google Drive integration using Google Workspace-specific credentials, ensuring secure and automated synchronization of architecture documents.

## Findings

### 1. Local Development (ADC)
For local development, Application Default Credentials (ADC) can be used by explicitly requesting Workspace scopes during the login process.
- **Action:** Run `gcloud auth application-default login --scopes="https://www.googleapis.com/auth/drive,https://www.googleapis.com/auth/cloud-platform"`.
- **Logic:** The Google Auth library automatically picks up these credentials. No additional service account keys are required locally.

### 2. Production/Headless (Domain-Wide Delegation)
For automated or headless environments, a **Service Account** with **Domain-Wide Delegation (DwD)** is required.
- **Setup:** 
    1. Create a Service Account in GCP.
    2. Copy the Client ID.
    3. In the Workspace Admin Console (**Security > API Controls > Manage Domain Wide Delegation**), authorize the Client ID with the `https://www.googleapis.com/auth/drive` scope.
- **Impersonation:** The code MUST specify the email of the Workspace user to impersonate (the "subject").

### 3. Implementation Code (Node.js)
```javascript
const { google } = require('googleapis');
const auth = new google.auth.GoogleAuth({
  scopes: ['https://www.googleapis.com/auth/drive'],
});

// For Domain-Wide Delegation (Service Account in Prod)
// auth.subject = 'admin@yourdomain.com'; 

const drive = google.drive({ version: 'v3', auth });
```

## Architectural Recommendations

- **Hybrid Auth Strategy:** Use ADC for local developer sessions and Service Account impersonation for CI/CD or automated background tasks.
- **Scope Restriction:** Always use the narrowest possible scope (e.g., `https://www.googleapis.com/auth/drive.file` if only managing files created by the app).
- **Environment Variables:** Store the "subject" email (impersonated user) in an environment variable (`WORKSPACE_SUBJECT_EMAIL`) rather than hardcoding.

## Next Steps

- Update `publish_to_gdocs.cjs` to support optional subject impersonation via environment variables.
- Document the `gcloud` login command in `llm/install.md` for new developers.
