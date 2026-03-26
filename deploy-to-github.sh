#!/bin/bash

# Natural Language Execution Brain - GitHub Deployment Script
# This script deploys the skill to GitHub

set -e

echo "=========================================="
echo "Natural Language Execution Brain"
echo "GitHub Deployment Script"
echo "=========================================="
echo ""

# Check if USERNAME is provided
if [ -z "$1" ]; then
    echo "❌ Error: GitHub username required"
    echo ""
    echo "Usage: ./deploy-to-github.sh YOUR_GITHUB_USERNAME"
    echo ""
    echo "Example: ./deploy-to-github.sh monsterlee"
    exit 1
fi

USERNAME="$1"
REPO_NAME="natural-language-execution-brain"
REPO_URL="https://github.com/${USERNAME}/${REPO_NAME}.git"

echo "📍 Preparing to deploy..."
echo "   Username: $USERNAME"
echo "   Repository: $REPO_NAME"
echo "   URL: $REPO_URL"
echo ""

# Verify we're in the right directory
if [ ! -f "README.md" ] || [ ! -f "SKILL.md" ]; then
    echo "❌ Error: Not in the skill directory"
    echo "   Please run this script from ~/skills/natural-language-execution-brain-1.0.0"
    exit 1
fi

echo "✅ Directory verified"
echo ""

# Add remote and push
echo "🔧 Configuring Git remote..."
git remote add origin "$REPO_URL" 2>/dev/null || {
    echo "⚠️  Remote already exists, updating..."
    git remote set-url origin "$REPO_URL"
}

echo "✅ Remote configured"
echo ""

echo "📤 Pushing to GitHub..."
git branch -M main 2>/dev/null || true
git push -u origin main

echo ""
echo "=========================================="
echo "✅ Deployment Complete!"
echo "=========================================="
echo ""
echo "🎉 Your skill is now available at:"
echo "   https://github.com/${USERNAME}/${REPO_NAME}"
echo ""
echo "📋 Next steps:"
echo "   1. Visit the repository link above"
echo "   2. Share the link with your team"
echo "   3. Use as a Git submodule or clone directly"
echo ""
echo "📚 Documentation:"
echo "   - SKILL.md: Full specification and doctrine"
echo "   - README.md: Quick start guide"
echo "   - examples/: Usage examples"
echo ""

