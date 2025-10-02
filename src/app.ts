import express from 'express';
import cors from 'cors';
import helmet from 'helmet';
import compression from 'compression';
import morgan from 'morgan';
import { config } from '@/config/environment';
import { logger } from '@/config/logger';
import { errorHandler } from '@/middleware/error-handler';
import { requestLogger } from '@/middleware/request-logger';
import { rateLimiter } from '@/middleware/rate-limiter';
import { securityHeaders } from '@/middleware/security-headers';
import { apiRoutes } from '@/routes/api';
import { healthRoutes } from '@/routes/health';

/**
 * Express Application Configuration
 * ERP Application with Odoo-style modular architecture
 */
export const app = express();

// Trust proxy for accurate IP addresses
app.set('trust proxy', 1);

// Security middleware
app.use(helmet({
  contentSecurityPolicy: {
    directives: {
      defaultSrc: ["'self'"],
      styleSrc: ["'self'", "'unsafe-inline'"],
      scriptSrc: ["'self'"],
      imgSrc: ["'self'", "data:", "https:"],
    },
  },
  crossOriginEmbedderPolicy: false,
}));

// CORS configuration
app.use(cors({
  origin: config.corsOrigins,
  credentials: true,
  methods: ['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS'],
  allowedHeaders: ['Content-Type', 'Authorization', 'X-Requested-With'],
}));

// Compression middleware
app.use(compression());

// Request logging
app.use(morgan('combined', {
  stream: {
    write: (message: string) => logger.info(message.trim()),
  },
}));

// Custom middleware
app.use(requestLogger);
app.use(securityHeaders);
app.use(rateLimiter);

// Body parsing middleware
app.use(express.json({ limit: '10mb' }));
app.use(express.urlencoded({ extended: true, limit: '10mb' }));

// Static files
app.use('/static', express.static('public'));

// Health check routes
app.use('/health', healthRoutes);

// API routes
app.use('/api', apiRoutes);

// Root route
app.get('/', (req, res) => {
  res.json({
    message: 'Odoo-Style ERP for Kids\' Clothing Retail Industry',
    version: '1.0.0',
    status: 'running',
    timestamp: new Date().toISOString(),
    environment: config.nodeEnv,
  });
});

// 404 handler
app.use('*', (req, res) => {
  res.status(404).json({
    error: 'Not Found',
    message: `Route ${req.originalUrl} not found`,
    timestamp: new Date().toISOString(),
  });
});

// Global error handler
app.use(errorHandler);

// Export app for testing
export default app;