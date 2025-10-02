import { Request, Response, NextFunction } from 'express';
import { logger } from '@/config/logger';

/**
 * Request logging middleware
 * Logs all incoming requests with detailed information
 */
export const requestLogger = (req: Request, res: Response, next: NextFunction): void => {
  const startTime = Date.now();
  const requestId = Math.random().toString(36).substring(7);

  // Add request ID to request object
  (req as any).requestId = requestId;

  // Log request details
  logger.info('Incoming request', {
    requestId,
    method: req.method,
    url: req.url,
    headers: {
      'user-agent': req.get('User-Agent'),
      'content-type': req.get('Content-Type'),
      'authorization': req.get('Authorization') ? 'Bearer ***' : undefined,
    },
    body: req.method !== 'GET' ? req.body : undefined,
    query: req.query,
    params: req.params,
    ip: req.ip,
    timestamp: new Date().toISOString(),
  });

  // Override res.end to log response
  const originalEnd = res.end;
  res.end = function (chunk?: any, encoding?: any) {
    const duration = Date.now() - startTime;
    const responseSize = res.get('Content-Length') || 0;

    // Log response details
    logger.info('Response sent', {
      requestId,
      method: req.method,
      url: req.url,
      statusCode: res.statusCode,
      duration: `${duration}ms`,
      responseSize: `${responseSize} bytes`,
      timestamp: new Date().toISOString(),
    });

    // Call original end method
    originalEnd.call(this, chunk, encoding);
  };

  next();
};

export default requestLogger;