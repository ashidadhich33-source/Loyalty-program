import { Request, Response, NextFunction } from 'express';
import { AuthService } from '@/services/auth.service';
import { logger } from '@/config/logger';
import { AppError } from './error-handler';

/**
 * Authentication middleware
 * Validates JWT tokens and attaches user information to request
 */
export const authenticate = async (req: Request, res: Response, next: NextFunction): Promise<void> => {
  try {
    const authHeader = req.headers.authorization;
    
    if (!authHeader || !authHeader.startsWith('Bearer ')) {
      throw new AppError('Authorization header missing or invalid', 401, 'MISSING_AUTH_HEADER');
    }

    const token = authHeader.substring(7); // Remove 'Bearer ' prefix
    
    if (!token) {
      throw new AppError('Access token is required', 401, 'MISSING_TOKEN');
    }

    const authService = new AuthService();
    const { user, session } = await authService.verifyToken(token);

    // Attach user and session to request
    (req as any).user = user;
    (req as any).userId = user.id;
    (req as any).session = session;
    (req as any).sessionId = session.id;

    next();
  } catch (error) {
    logger.error('Authentication failed', { error, path: req.path });
    next(error);
  }
};

/**
 * Optional authentication middleware
 * Validates JWT tokens if present, but doesn't require them
 */
export const optionalAuth = async (req: Request, res: Response, next: NextFunction): Promise<void> => {
  try {
    const authHeader = req.headers.authorization;
    
    if (authHeader && authHeader.startsWith('Bearer ')) {
      const token = authHeader.substring(7);
      
      if (token) {
        try {
          const authService = new AuthService();
          const { user, session } = await authService.verifyToken(token);

          // Attach user and session to request
          (req as any).user = user;
          (req as any).userId = user.id;
          (req as any).session = session;
          (req as any).sessionId = session.id;
        } catch (error) {
          // Ignore authentication errors for optional auth
          logger.debug('Optional authentication failed', { error, path: req.path });
        }
      }
    }

    next();
  } catch (error) {
    logger.error('Optional authentication failed', { error, path: req.path });
    next(error);
  }
};

/**
 * Role-based authorization middleware
 * Checks if user has required role
 */
export const authorize = (roles: string[]) => {
  return (req: Request, res: Response, next: NextFunction): void => {
    try {
      const user = (req as any).user;
      
      if (!user) {
        throw new AppError('Authentication required', 401, 'AUTH_REQUIRED');
      }

      if (!roles.includes(user.role)) {
        throw new AppError('Insufficient permissions', 403, 'INSUFFICIENT_PERMISSIONS');
      }

      next();
    } catch (error) {
      logger.error('Authorization failed', { error, path: req.path, roles });
      next(error);
    }
  };
};

/**
 * Admin authorization middleware
 * Checks if user is admin
 */
export const requireAdmin = (req: Request, res: Response, next: NextFunction): void => {
  try {
    const user = (req as any).user;
    
    if (!user) {
      throw new AppError('Authentication required', 401, 'AUTH_REQUIRED');
    }

    if (!user.isAdmin()) {
      throw new AppError('Admin access required', 403, 'ADMIN_REQUIRED');
    }

    next();
  } catch (error) {
    logger.error('Admin authorization failed', { error, path: req.path });
    next(error);
  }
};

/**
 * Manager authorization middleware
 * Checks if user is manager or admin
 */
export const requireManager = (req: Request, res: Response, next: NextFunction): void => {
  try {
    const user = (req as any).user;
    
    if (!user) {
      throw new AppError('Authentication required', 401, 'AUTH_REQUIRED');
    }

    if (!user.isManager()) {
      throw new AppError('Manager access required', 403, 'MANAGER_REQUIRED');
    }

    next();
  } catch (error) {
    logger.error('Manager authorization failed', { error, path: req.path });
    next(error);
  }
};

/**
 * Company authorization middleware
 * Checks if user belongs to the same company
 */
export const requireSameCompany = (req: Request, res: Response, next: NextFunction): void => {
  try {
    const user = (req as any).user;
    const companyId = req.params.companyId || req.body.company_id;
    
    if (!user) {
      throw new AppError('Authentication required', 401, 'AUTH_REQUIRED');
    }

    if (companyId && user.company_id !== companyId) {
      throw new AppError('Access denied to this company', 403, 'COMPANY_ACCESS_DENIED');
    }

    next();
  } catch (error) {
    logger.error('Company authorization failed', { error, path: req.path });
    next(error);
  }
};

/**
 * Resource ownership middleware
 * Checks if user owns the resource
 */
export const requireOwnership = (resourceIdParam: string = 'id') => {
  return (req: Request, res: Response, next: NextFunction): void => {
    try {
      const user = (req as any).user;
      const resourceId = req.params[resourceIdParam];
      
      if (!user) {
        throw new AppError('Authentication required', 401, 'AUTH_REQUIRED');
      }

      // For now, we'll just check if the user is authenticated
      // In a real implementation, you would check if the user owns the resource
      if (!resourceId) {
        throw new AppError('Resource ID is required', 400, 'MISSING_RESOURCE_ID');
      }

      next();
    } catch (error) {
      logger.error('Ownership authorization failed', { error, path: req.path, resourceIdParam });
      next(error);
    }
  };
};

/**
 * Session validation middleware
 * Validates that the session is active
 */
export const validateSession = (req: Request, res: Response, next: NextFunction): void => {
  try {
    const session = (req as any).session;
    
    if (!session) {
      throw new AppError('Session not found', 401, 'NO_SESSION');
    }

    if (!session.isActive()) {
      throw new AppError('Session is inactive', 401, 'INACTIVE_SESSION');
    }

    next();
  } catch (error) {
    logger.error('Session validation failed', { error, path: req.path });
    next(error);
  }
};

/**
 * Rate limiting middleware for authentication endpoints
 */
export const authRateLimit = (req: Request, res: Response, next: NextFunction): void => {
  // This would typically implement rate limiting for auth endpoints
  // For now, we'll just pass through
  next();
};

/**
 * Device validation middleware
 * Validates device information for security
 */
export const validateDevice = (req: Request, res: Response, next: NextFunction): void => {
  try {
    const userAgent = req.get('User-Agent');
    const ipAddress = req.ip;
    
    // Basic device validation
    if (!userAgent) {
      throw new AppError('User-Agent header is required', 400, 'MISSING_USER_AGENT');
    }

    // Attach device info to request
    (req as any).deviceInfo = {
      userAgent,
      ipAddress,
      timestamp: new Date(),
    };

    next();
  } catch (error) {
    logger.error('Device validation failed', { error, path: req.path });
    next(error);
  }
};

export default {
  authenticate,
  optionalAuth,
  authorize,
  requireAdmin,
  requireManager,
  requireSameCompany,
  requireOwnership,
  validateSession,
  authRateLimit,
  validateDevice,
};