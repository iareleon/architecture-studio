const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

/**
 * Gets the current timestamp in SAST (GMT+2) formatted as YYYY-MM-DD-HH24-MM.
 */
function getSASTTimestamp() {
    const now = new Date();
    // SAST is GMT+2. Offset in minutes.
    const SAST_OFFSET = 120;
    const utc = now.getTime() + (now.getTimezoneOffset() * 60000);
    const sastDate = new Date(utc + (3600000 * 2));

    const yyyy = sastDate.getFullYear();
    const mm = String(sastDate.getMonth() + 1).padStart(2, '0');
    const dd = String(sastDate.getDate()).padStart(2, '0');
    const hh = String(sastDate.getHours()).padStart(2, '0');
    const min = String(sastDate.getMinutes()).padStart(2, '0');

    return `${yyyy}-${mm}-${dd}-${hh}-${min}`;
}

function prepareCommit() {
    const projectRoot = path.resolve(__dirname, '../../..');
    const timestamp = getSASTTimestamp();
    const slug = 'staged-changes-summary';
    const changeFileName = `${timestamp}-${slug}.md`;
    const changeFilePath = path.join(projectRoot, 'raw/changes', changeFileName);
    const changeLogPath = path.join(projectRoot, 'raw/change-log.md');

    console.log('Gathering Git diff for commit summary...');

    let diff;
    try {
        // Check staged changes first
        diff = execSync('git diff --staged', { encoding: 'utf8' }).trim();
        if (!diff) {
            // If no staged changes, check all changes
            diff = execSync('git diff HEAD', { encoding: 'utf8' }).trim();
        }
    } catch (err) {
        console.error('Error running git diff:', err.message);
        process.exit(1);
    }

    if (!diff) {
        console.log('No changes detected. Nothing to summarize.');
        return;
    }

    const changeContent = `# ${timestamp}-${slug}

**Status: [todo]**

## Summary

- [ ] AI: Generate summary from the diff below.

## Justification

User triggered commit summary preparation from terminal.

## Impact

- **Systems:** Git
- **Documents:** Multiple (see diff)

## Technical Context (Diff)

\`\`\`diff
${diff}
\`\`\`
`;

    try {
        fs.writeFileSync(changeFilePath, changeContent);
        console.log(`Change scaffolded: ${changeFilePath}`);

        const logEntry = `
**Staged Changes Summary**
	- **Date-Time :** ${timestamp}
	- **Phase Impacted :** Development
	- **Status :** [todo]
	- **Question :** Generate a commit message summary for the current changes.
	- **Reference:** [[raw/changes/${changeFileName}]]
`;
        fs.appendFileSync(changeLogPath, logEntry);
        console.log('Added [todo] entry to raw/change-log.md');

        console.log('\nSUCCESS: Commit context prepared.');
        console.log(`Prompt Gemini: "Process the pending commit in raw/changes/${changeFileName}"`);
    } catch (err) {
        console.error('Error writing files:', err.message);
        process.exit(1);
    }
}

prepareCommit();
