const fs = require('fs');
const path = require('path');
const { google } = require('googleapis');
const { marked } = require('marked');

/**
 * Publishes a local Markdown file to Google Docs.
 * Uses Drive API with media upload for full content sync (conversion from HTML).
 */
async function publishToGDocs(filePath) {
    if (!filePath) {
        console.error('Error: No file path provided.');
        console.log('Usage: node scripts/publish_to_gdocs.cjs <file_path>');
        process.exit(1);
    }

    const projectRoot = path.resolve(__dirname, '../../..');
    const absolutePath = path.resolve(filePath);
    const relativePath = path.relative(projectRoot, absolutePath);

    if (!fs.existsSync(absolutePath)) {
        console.error(`Error: File not found: ${absolutePath}`);
        process.exit(1);
    }

    console.log(`\n--- GDocs Sync Started ---`);
    console.log(`File: ${relativePath}`);

    // 1. Process Content (Mermaid placeholders)
    let mdContent = fs.readFileSync(absolutePath, 'utf8');
    const mermaidRegex = /```mermaid[\s\S]*?```/g;
    const placeholder = '\n\n[Diagram Placeholder - Insert from external source]\n\n';
    mdContent = mdContent.replace(mermaidRegex, placeholder);

    // 2. Convert to HTML
    const htmlContent = `<html><body>${marked.parse(mdContent)}</body></html>`;

    // 3. Authenticate with ADC
    let auth;
    try {
        auth = new google.auth.GoogleAuth({
            scopes: ['https://www.googleapis.com/auth/drive.file']
        });
        const authClient = await auth.getClient();
        google.options({ auth: authClient });
    } catch (err) {
        console.error('Authentication Error: Ensure ADC is configured (gcloud auth application-default login).');
        console.error(err.message);
        process.exit(1);
    }

    const drive = google.drive('v3');
    const syncMapPath = path.join(__dirname, '../assets/sync-map.json');
    let syncMap = {};
    
    if (fs.existsSync(syncMapPath)) {
        syncMap = JSON.parse(fs.readFileSync(syncMapPath, 'utf8'));
    }

    const existingDocId = syncMap[relativePath];

    try {
        if (existingDocId) {
            console.log(`Existing mapping found: ${existingDocId}`);
            console.log('Updating document content...');

            await drive.files.update({
                fileId: existingDocId,
                media: {
                    mimeType: 'text/html',
                    body: htmlContent
                }
            });
            
            console.log(`SUCCESS: Document updated.`);
        } else {
            console.log('No existing mapping found. Creating new document...');

            const res = await drive.files.create({
                requestBody: {
                    name: path.basename(filePath, '.md'),
                    mimeType: 'application/vnd.google-apps.document'
                },
                media: {
                    mimeType: 'text/html',
                    body: htmlContent
                }
            });

            const newDocId = res.data.id;
            syncMap[relativePath] = newDocId;
            fs.writeFileSync(syncMapPath, JSON.stringify(syncMap, null, 2));
            
            console.log(`SUCCESS: Created new document with ID: ${newDocId}`);
            console.log(`Sync mapping saved to: ${path.relative(projectRoot, syncMapPath)}`);
        }

        console.log(`\nView document: https://docs.google.com/document/d/${syncMap[relativePath]}/edit`);
    } catch (err) {
        console.error('API Error: Failed to sync with Google Drive.');
        console.error(err.message);
        process.exit(1);
    }
}

// Start processing
const args = process.argv.slice(2);
publishToGDocs(args[0]).catch(err => {
    console.error('Fatal Error:');
    console.error(err);
    process.exit(1);
});
