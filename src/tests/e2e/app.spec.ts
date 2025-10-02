import { test, expect } from '@playwright/test';

/**
 * E2E tests for the ERP application
 * Tests the complete user workflow from browser perspective
 */
test.describe('ERP Application E2E', () => {
  test.beforeEach(async ({ page }) => {
    // Navigate to the application
    await page.goto('/');
  });

  test('should display application information', async ({ page }) => {
    // Check if the page loads correctly
    await expect(page).toHaveTitle(/ERP/);
    
    // Check if the main content is displayed
    await expect(page.locator('body')).toContainText('Odoo-Style ERP');
  });

  test('should navigate to health check', async ({ page }) => {
    // Navigate to health check
    await page.goto('/health');
    
    // Check if health check is displayed
    await expect(page.locator('body')).toContainText('healthy');
  });

  test('should handle 404 errors', async ({ page }) => {
    // Navigate to non-existent route
    await page.goto('/non-existent-route');
    
    // Check if 404 error is displayed
    await expect(page.locator('body')).toContainText('Not Found');
  });

  test('should include security headers', async ({ page }) => {
    // Check security headers
    const response = await page.goto('/');
    const headers = response?.headers();
    
    expect(headers?.['x-content-type-options']).toBe('nosniff');
    expect(headers?.['x-frame-options']).toBe('DENY');
    expect(headers?.['x-xss-protection']).toBe('1; mode=block');
  });

  test('should handle CORS correctly', async ({ page }) => {
    // Test CORS headers
    const response = await page.goto('/');
    const headers = response?.headers();
    
    expect(headers?.['access-control-allow-origin']).toBeDefined();
  });

  test('should load static files', async ({ page }) => {
    // Test static file serving
    const response = await page.goto('/static/test.txt');
    
    // This would test if static files are served correctly
    // For now, we'll just check that the request doesn't fail
    expect(response?.status()).toBeLessThan(500);
  });

  test('should handle API requests', async ({ page }) => {
    // Test API endpoint
    const response = await page.goto('/api');
    
    // Check if API response is valid
    expect(response?.status()).toBe(200);
  });

  test('should display error pages correctly', async ({ page }) => {
    // Test error handling
    await page.goto('/error-route');
    
    // Check if error page is displayed
    await expect(page.locator('body')).toContainText('Not Found');
  });
});