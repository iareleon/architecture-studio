const fs = require('fs');
const path = require('path');

const CATEGORIES = ['new skill', 'new core instruction', 'new local instruction'];

function logImprovement(category, description) {
    if (!CATEGORIES.includes(category)) {
        console.error(`Error: Invalid category. Must be one of: ${CATEGORIES.join(', ')}`);
        process.exit(1);
    }

    const improvementsPath = path.join(process.env.USERPROFILE, 'Development', 'architecture-studio', 'improvements.md');
    const timestamp = new Date().toISOString();
    const entry = `- [ ] [${category.toUpperCase()}] (${timestamp}): ${description}\n`;

    try {
        fs.appendFileSync(improvementsPath, entry, 'utf8');
        console.log(`Successfully logged improvement to ${improvementsPath}`);
    } catch (err) {
        console.error(`Error writing to improvements file: ${err.message}`);
        process.exit(1);
    }
}

const [,, category, ...descriptionParts] = process.argv;
const description = descriptionParts.join(' ');

if (!category || !description) {
    console.log('Usage: node log_improvement.cjs <category> <description>');
    process.exit(1);
}

logImprovement(category, description);
