/**
 * Global teardown for E2E tests
 * Runs after all E2E tests to clean up the test environment
 */
async function globalTeardown() {
  console.log('🧹 Cleaning up E2E test environment...');

  // Kill the server process
  const server = (global as any).__SERVER__;
  if (server) {
    server.kill();
    console.log('✅ Server stopped');
  }

  console.log('✅ E2E test environment cleanup complete');
}

export default globalTeardown;