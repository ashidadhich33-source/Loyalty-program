import { Request, Response, NextFunction } from 'express';
import rateLimit from 'express-rate-limit';
import { logger } from '@/config/logger';

/**
 * Rate limiting configuration
 * Prevents abuse by limiting requests per IP address
 */
export const rateLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // Limit each IP to 100 requests per windowMs
  message: {
    error: 'Too many requests',
    message: 'Too many requests from this IP, please try again later',
    retryAfter: '15 minutes',
  },
  standardHeaders: true, // Return rate limit info in the `RateLimit-*` headers
  legacyHeaders: false, // Disable the `X-RateLimit-*` headers
  handler: (req: Request, res: Response) => {
    logger.warn('Rate limit exceeded', {
      ip: req.ip,
      method: req.method,
      url: req.url,
      userAgent: req.get('User-Agent'),
      timestamp: new Date().toISOString(),
    });

    res.status(429).json({
      error: 'Too many requests',
      message: 'Too many requests from this IP, please try again later',
      retryAfter: '15 minutes',
    });
  },
  skip: (req: Request) => {
    // Skip rate limiting for health checks
    return req.url === '/health';
  },
});

/**
 * Strict rate limiter for authentication endpoints
 */
export const authRateLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 5, // Limit each IP to 5 login attempts per windowMs
  message: {
    error: 'Too many authentication attempts',
    message: 'Too many login attempts, please try again later',
    retryAfter: '15 minutes',
  },
  standardHeaders: true,
  legacyHeaders: false,
  handler: (req: Request, res: Response) => {
    logger.warn('Authentication rate limit exceeded', {
      ip: req.ip,
      method: req.method,
      url: req.url,
      userAgent: req.get('User-Agent'),
      timestamp: new Date().toISOString(),
    });

    res.status(429).json({
      error: 'Too many authentication attempts',
      message: 'Too many login attempts, please try again later',
      retryAfter: '15 minutes',
    });
  },
});

/**
 * API rate limiter for API endpoints
 */
export const apiRateLimiter = rateLimit({
  windowMs: 1 * 60 * 1000, // 1 minute
  max: 60, // Limit each IP to 60 requests per minute
  message: {
    error: 'API rate limit exceeded',
    message: 'Too many API requests, please try again later',
    retryAfter: '1 minute',
  },
  standardHeaders: true,
  legacyHeaders: false,
  handler: (req: Request, res: Response) => {
    logger.warn('API rate limit exceeded', {
      ip: req.ip,
      method: req.method,
      url: req.url,
      userAgent: req.get('User-Agent'),
      timestamp: new Date().toISOString(),
    });

    res.status(429).json({
      error: 'API rate limit exceeded',
      message: 'Too many API requests, please try again later',
      retryAfter: '1 minute',
    });
  },
});

export default rateLimiter;