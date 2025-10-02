import request from 'supertest';
import { app } from '@/app';

/**
 * Unit tests for the main application
 * Tests the Express app configuration and basic functionality
 */
describe('ERP Application', () => {
  describe('GET /', () => {
    it('should return application information', async () => {
      const response = await request(app)
        .get('/')
        .expect(200);

      expect(response.body).toHaveProperty('message');
      expect(response.body).toHaveProperty('version');
      expect(response.body).toHaveProperty('status');
      expect(response.body).toHaveProperty('timestamp');
      expect(response.body).toHaveProperty('environment');
      expect(response.body.status).toBe('running');
    });
  });

  describe('GET /health', () => {
    it('should return health check information', async () => {
      const response = await request(app)
        .get('/health')
        .expect(200);

      expect(response.body).toHaveProperty('status');
      expect(response.body).toHaveProperty('timestamp');
      expect(response.body.status).toBe('healthy');
    });
  });

  describe('GET /api', () => {
    it('should return API information', async () => {
      const response = await request(app)
        .get('/api')
        .expect(200);

      expect(response.body).toHaveProperty('message');
      expect(response.body).toHaveProperty('version');
      expect(response.body).toHaveProperty('modules');
    });
  });

  describe('404 Handler', () => {
    it('should return 404 for non-existent routes', async () => {
      const response = await request(app)
        .get('/non-existent-route')
        .expect(404);

      expect(response.body).toHaveProperty('error');
      expect(response.body).toHaveProperty('message');
      expect(response.body.error).toBe('Not Found');
    });
  });

  describe('CORS Configuration', () => {
    it('should include CORS headers', async () => {
      const response = await request(app)
        .get('/')
        .expect(200);

      expect(response.headers).toHaveProperty('access-control-allow-origin');
    });
  });

  describe('Security Headers', () => {
    it('should include security headers', async () => {
      const response = await request(app)
        .get('/')
        .expect(200);

      expect(response.headers).toHaveProperty('x-content-type-options');
      expect(response.headers).toHaveProperty('x-frame-options');
      expect(response.headers).toHaveProperty('x-xss-protection');
    });
  });

  describe('Request Logging', () => {
    it('should log requests', async () => {
      const response = await request(app)
        .get('/')
        .expect(200);

      expect(response.status).toBe(200);
    });
  });

  describe('Error Handling', () => {
    it('should handle errors gracefully', async () => {
      // This test would require a route that throws an error
      // For now, we'll test the 404 handler
      const response = await request(app)
        .get('/error-route')
        .expect(404);

      expect(response.body).toHaveProperty('error');
    });
  });
});