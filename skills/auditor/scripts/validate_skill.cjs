const fs = require('fs');
const path = require('path');

const skillName = process.argv[2];

if (!skillName) {
    console.error('Usage: node validate_skill.cjs <skill_name>');
    process.exit(1);
}

const projectRoot = path.resolve(__dirname, '../../..');
const skillDir = path.join(projectRoot, 'skills', skillName);
const skillFile = path.join(skillDir, 'SKILL.md');

if (!fs.existsSync(skillDir) || !fs.existsSync(skillFile)) {
    console.error(`Error: Skill '${skillName}' or SKILL.md not found at ${skillDir}`);
    process.exit(1);
}

console.log(`Validating skill: ${skillName}...`);

const content = fs.readFileSync(skillFile, 'utf8');

if (!content.includes('name:') || !content.includes('description:')) {
    console.error('Validation failed: SKILL.md is missing required frontmatter (name, description).');
    process.exit(1);
}

console.log(`Validation passed for ${skillName}`);
process.exit(0);
