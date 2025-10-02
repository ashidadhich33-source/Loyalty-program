import { Router } from 'express';
import { checkDatabaseHealth } from '@/config/database';
import { logger } from '@/config/logger';

/**
 * Health check routes
 * Provides health status for the application and its dependencies
 */
const router = Router();

/**
 * Basic health check
 * GET /health
 */
router.get('/', async (req, res) => {
  try {
    const timestamp = new Date().toISOString();
    
    // Check database health
    const dbHealthy = await checkDatabaseHealth();
    
    const health = {
      status: 'healthy',
      timestamp,
      uptime: process.uptime(),
      memory: process.memoryUsage(),
      version: process.version,
      environment: process.env.NODE_ENV,
      services: {
        database: dbHealthy ? 'healthy' : 'unhealthy',
      },
    };

    if (!dbHealthy) {
      health.status = 'degraded';
    }

    res.status(200).json(health);
  } catch (error) {
    logger.error('Health check failed:', error);
    
    res.status(503).json({
      status: 'unhealthy',
      timestamp: new Date().toISOString(),
      error: 'Health check failed',
    });
  }
});

/**
 * Detailed health check
 * GET /health/detailed
 */
router.get('/detailed', async (req, res) => {
  try {
    const timestamp = new Date().toISOString();
    
    // Check database health
    const dbHealthy = await checkDatabaseHealth();
    
    const health = {
      status: 'healthy',
      timestamp,
      uptime: process.uptime(),
      memory: process.memoryUsage(),
      cpu: process.cpuUsage(),
      version: process.version,
      environment: process.env.NODE_ENV,
      services: {
        database: {
          status: dbHealthy ? 'healthy' : 'unhealthy',
          connection: dbHealthy ? 'connected' : 'disconnected',
        },
      },
      system: {
        platform: process.platform,
        arch: process.arch,
        pid: process.pid,
        title: process.title,
      },
    };

    if (!dbHealthy) {
      health.status = 'degraded';
    }

    res.status(200).json(health);
  } catch (error) {
    logger.error('Detailed health check failed:', error);
    
    res.status(503).json({
      status: 'unhealthy',
      timestamp: new Date().toISOString(),
      error: 'Detailed health check failed',
    });
  }
});

/**
 * Readiness check
 * GET /health/ready
 */
router.get('/ready', async (req, res) => {
  try {
    const dbHealthy = await checkDatabaseHealth();
    
    if (dbHealthy) {
      res.status(200).json({
        status: 'ready',
        timestamp: new Date().toISOString(),
      });
    } else {
      res.status(503).json({
        status: 'not ready',
        timestamp: new Date().toISOString(),
        reason: 'Database not available',
      });
    }
  } catch (error) {
    logger.error('Readiness check failed:', error);
    
    res.status(503).json({
      status: 'not ready',
      timestamp: new Date().toISOString(),
      error: 'Readiness check failed',
    });
  }
});

/**
 * Liveness check
 * GET /health/live
 */
router.get('/live', (req, res) => {
  res.status(200).json({
    status: 'alive',
    timestamp: new Date().toISOString(),
    uptime: process.uptime(),
  });
});

export { router as healthRoutes };