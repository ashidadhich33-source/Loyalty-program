import { chromium, FullConfig } from '@playwright/test';

/**
 * Global setup for E2E tests
 * Runs before all E2E tests to set up the test environment
 */
async function globalSetup(config: FullConfig) {
  console.log('🚀 Setting up E2E test environment...');

  // Start the application server
  const { spawn } = require('child_process');
  const server = spawn('npm', ['run', 'dev'], {
    stdio: 'pipe',
    env: { ...process.env, NODE_ENV: 'test' },
  });

  // Wait for server to be ready
  await new Promise((resolve) => {
    server.stdout.on('data', (data: Buffer) => {
      const output = data.toString();
      if (output.includes('ERP Server running')) {
        console.log('✅ Server started successfully');
        resolve(undefined);
      }
    });
  });

  // Store server process for cleanup
  (global as any).__SERVER__ = server;

  console.log('✅ E2E test environment setup complete');
}

export default globalSetup;