import { Request, Response, NextFunction } from 'express';
import { logger } from '@/config/logger';
import { config } from '@/config/environment';

/**
 * Error interface for custom errors
 */
export interface AppError extends Error {
  statusCode?: number;
  isOperational?: boolean;
  code?: string;
  keyValue?: Record<string, unknown>;
  errors?: Record<string, unknown>;
}

/**
 * Global error handler middleware
 * Handles all errors in the application with proper logging and response
 */
export const errorHandler = (
  error: AppError,
  req: Request,
  res: Response,
  next: NextFunction
): void => {
  let statusCode = error.statusCode || 500;
  let message = error.message || 'Internal Server Error';
  let code = error.code || 'INTERNAL_ERROR';

  // Log error details
  logger.error('Error occurred:', {
    error: {
      message: error.message,
      stack: error.stack,
      statusCode: error.statusCode,
      code: error.code,
    },
    request: {
      method: req.method,
      url: req.url,
      headers: req.headers,
      body: req.body,
      params: req.params,
      query: req.query,
    },
    timestamp: new Date().toISOString(),
  });

  // Handle specific error types
  if (error.name === 'ValidationError') {
    statusCode = 400;
    message = 'Validation Error';
    code = 'VALIDATION_ERROR';
  } else if (error.name === 'CastError') {
    statusCode = 400;
    message = 'Invalid ID format';
    code = 'INVALID_ID';
  } else if (error.name === 'MongoError' && error.code === 11000) {
    statusCode = 409;
    message = 'Duplicate field value';
    code = 'DUPLICATE_ERROR';
  } else if (error.name === 'JsonWebTokenError') {
    statusCode = 401;
    message = 'Invalid token';
    code = 'INVALID_TOKEN';
  } else if (error.name === 'TokenExpiredError') {
    statusCode = 401;
    message = 'Token expired';
    code = 'TOKEN_EXPIRED';
  } else if (error.name === 'MulterError') {
    statusCode = 400;
    message = 'File upload error';
    code = 'FILE_UPLOAD_ERROR';
  }

  // Don't leak error details in production
  if (config.isProduction && statusCode === 500) {
    message = 'Internal Server Error';
  }

  // Send error response
  res.status(statusCode).json({
    success: false,
    error: {
      message,
      code,
      statusCode,
      timestamp: new Date().toISOString(),
      path: req.url,
      method: req.method,
      ...(config.isDevelopment && { stack: error.stack }),
    },
  });
};

/**
 * Async error handler wrapper
 * Catches async errors and passes them to the error handler
 */
export const asyncHandler = (fn: Function) => {
  return (req: Request, res: Response, next: NextFunction) => {
    Promise.resolve(fn(req, res, next)).catch(next);
  };
};

/**
 * 404 handler for undefined routes
 */
export const notFoundHandler = (req: Request, res: Response, next: NextFunction) => {
  const error: AppError = new Error(`Route ${req.originalUrl} not found`);
  error.statusCode = 404;
  error.code = 'ROUTE_NOT_FOUND';
  next(error);
};

/**
 * Validation error handler
 */
export const validationErrorHandler = (error: any) => {
  const errors = Object.values(error.errors).map((err: any) => ({
    field: err.path,
    message: err.message,
    value: err.value,
  }));

  const appError: AppError = new Error('Validation failed');
  appError.statusCode = 400;
  appError.code = 'VALIDATION_ERROR';
  appError.errors = errors;

  return appError;
};

/**
 * Database error handler
 */
export const databaseErrorHandler = (error: any) => {
  let statusCode = 500;
  let message = 'Database error';
  let code = 'DATABASE_ERROR';

  if (error.code === '23505') {
    statusCode = 409;
    message = 'Duplicate entry';
    code = 'DUPLICATE_ERROR';
  } else if (error.code === '23503') {
    statusCode = 400;
    message = 'Foreign key constraint violation';
    code = 'FOREIGN_KEY_ERROR';
  } else if (error.code === '23502') {
    statusCode = 400;
    message = 'Required field missing';
    code = 'REQUIRED_FIELD_ERROR';
  }

  const appError: AppError = new Error(message);
  appError.statusCode = statusCode;
  appError.code = code;
  appError.originalError = error;

  return appError;
};

export default errorHandler;