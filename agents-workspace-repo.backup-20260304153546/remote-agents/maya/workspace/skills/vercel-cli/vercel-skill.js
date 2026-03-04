#!/usr/bin/env node
/**
 * Vercel CLI Skill for OpenClaw
 * Wraps vercel CLI commands for easy deployment
 */

const { execSync } = require('child_process');
const path = require('path');

// Parse command
const args = process.argv.slice(2);
const command = args[0];
const projectPath = args[1] || process.cwd();

function runVercel(args) {
  try {
    const result = execSync(`vercel ${args}`, {
      cwd: projectPath,
      encoding: 'utf-8',
      stdio: 'pipe'
    });
    return { success: true, output: result };
  } catch (error) {
    return { success: false, error: error.stderr || error.message };
  }
}

function checkVercelInstalled() {
  try {
    execSync('which vercel', { stdio: 'pipe' });
    return true;
  } catch {
    return false;
  }
}

async function main() {
  // Check if vercel is installed
  if (!checkVercelInstalled()) {
    console.log('❌ Vercel CLI not found');
    console.log('Installing...');
    try {
      execSync('npm install -g vercel', { stdio: 'inherit' });
      console.log('✅ Vercel CLI installed');
    } catch (error) {
      console.log('❌ Failed to install Vercel CLI');
      console.log('Please run: npm install -g vercel');
      process.exit(1);
    }
  }

  switch (command) {
    case 'login':
      console.log('🔐 Opening Vercel login...');
      try {
        execSync('vercel login', { stdio: 'inherit' });
        console.log('✅ Logged in successfully');
      } catch (error) {
        console.log('❌ Login failed or cancelled');
      }
      break;

    case 'deploy':
      console.log(`🚀 Deploying ${projectPath}...`);
      const deployResult = runVercel('');
      if (deployResult.success) {
        console.log('✅ Deployed successfully');
        console.log(deployResult.output);
      } else {
        console.log('❌ Deployment failed');
        console.log(deployResult.error);
      }
      break;

    case 'deploy-prod':
      console.log(`🚀 Deploying to production...`);
      const prodResult = runVercel('--prod');
      if (prodResult.success) {
        console.log('✅ Production deployment successful');
        console.log(prodResult.output);
      } else {
        console.log('❌ Production deployment failed');
        console.log(prodResult.error);
      }
      break;

    case 'logs':
      console.log('📋 Opening logs...');
      try {
        execSync('vercel logs', { stdio: 'inherit', cwd: projectPath });
      } catch (error) {
        console.log('❌ Could not fetch logs');
      }
      break;

    case 'list':
      console.log('📋 Listing deployments...');
      const listResult = runVercel('list');
      if (listResult.success) {
        console.log(listResult.output);
      } else {
        console.log('❌ Could not list deployments');
        console.log(listResult.error);
      }
      break;

    default:
      console.log('Vercel CLI Skill');
      console.log('');
      console.log('Commands:');
      console.log('  login         - Login to Vercel');
      console.log('  deploy        - Deploy project');
      console.log('  deploy-prod   - Deploy to production');
      console.log('  logs          - View deployment logs');
      console.log('  list          - List deployments');
      console.log('');
      console.log('Usage: node vercel-skill.js <command> [path]');
  }
}

main();
