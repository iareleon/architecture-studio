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

function auditStructure() {
    const projectRoot = path.resolve(__dirname, '../../..');
    const templatePath = path.join(projectRoot, 'skills/auditor/assets/templates/folder-structure.template.md');
    const planPath = path.join(projectRoot, '_os/audit-fix-plan.md');
    const timestamp = getSASTTimestamp();
    const reportPath = path.join(projectRoot, 'raw/reports', `${timestamp}-structural-audit.md`);
    
    console.log('Auditing project structure against folder-structure.template.md...');

    if (!fs.existsSync(templatePath)) {
        console.error('Error: folder-structure.template.md not found.');
        process.exit(1);
    }

    const templateContent = fs.readFileSync(templatePath, 'utf8');
    const requiredPaths = [];
    
    const lines = templateContent.split('\n');
    let inTree = false;
    lines.forEach(line => {
        if (line.trim() === '```text') {
            inTree = true;
            return;
        }
        if (line.trim() === '```') {
            inTree = false;
            return;
        }
        if (inTree) {
            // Match paths in the tree (e.g., ├── llm/)
            const match = line.match(/[├└]──\s(.*?)(?:\/|\s|$)/);
            if (match && match[1]) {
                requiredPaths.push(match[1]);
            }
        }
    });

    const missingPaths = [];
    requiredPaths.forEach(reqPath => {
        const fullPath = path.join(projectRoot, reqPath);
        if (!fs.existsSync(fullPath)) {
            missingPaths.push(reqPath);
        }
    });

    if (!fs.existsSync(path.join(projectRoot, 'raw/reports'))) {
        fs.mkdirSync(path.join(projectRoot, 'raw/reports'), { recursive: true });
    }

    if (missingPaths.length === 0) {
        console.log('Audit complete: Workspace structure is healthy. Generating report...');
        let reportContent = `# Structural Audit Report\n\n**Timestamp:** ${timestamp}\n**Status:** Pass\n\nNo missing required paths found. Workspace structure is healthy.\n`;
        fs.writeFileSync(reportPath, reportContent);
        console.log(`Audit report written to: ${reportPath}`);
        return;
    }

    console.log(`Found ${missingPaths.length} missing required paths. Generating fix plan and report...`);
    
    if (!fs.existsSync(path.join(projectRoot, '_os'))) {
        fs.mkdirSync(path.join(projectRoot, '_os'), { recursive: true });
    }

    let planContent = '# Audit Fix Plan\n\n## Missing Directories/Files\n\n';
    let reportContent = `# Structural Audit Report\n\n**Timestamp:** ${timestamp}\n**Status:** Fail\n\n## Missing Required Paths\n\n`;

    missingPaths.forEach(p => {
        planContent += `- [ ] Create \`${p}\`\n`;
        reportContent += `- \`${p}\`\n`;
    });
    
    planContent += '\nTo execute this plan, prompt the LLM to "Execute the fixes outlined in _os/audit-fix-plan.md"';

    fs.writeFileSync(planPath, planContent);
    fs.writeFileSync(reportPath, reportContent);
    console.log(`Fix plan written to: ${planPath}`);
    console.log(`Audit report written to: ${reportPath}`);
}

auditStructure();
