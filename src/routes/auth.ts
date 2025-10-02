import { Router } from 'express';
import { AuthController } from '@/controllers/auth.controller';
import { authenticate, validateSession, authRateLimit } from '@/middleware/auth.middleware';
import { rateLimiter, authRateLimiter } from '@/middleware/rate-limiter';

/**
 * Authentication routes
 * Handles all authentication-related endpoints
 */
const router = Router();
const authController = new AuthController();

// Apply rate limiting to all auth routes
router.use(authRateLimiter);

/**
 * Public routes (no authentication required)
 */
router.post('/register', authController.register);
router.post('/login', authController.login);
router.post('/refresh', authController.refresh);
router.post('/verify-email', authController.verifyEmail);
router.post('/resend-verification', authController.resendVerification);
router.post('/forgot-password', authController.forgotPassword);
router.post('/reset-password', authController.resetPassword);

/**
 * Protected routes (authentication required)
 */
router.use(authenticate);
router.use(validateSession);

// Session management
router.post('/logout', authController.logout);
router.post('/logout-all', authController.logoutAll);
router.get('/sessions', authController.getSessions);
router.delete('/sessions/:sessionId', authController.revokeSession);

// Profile management
router.get('/profile', authController.getProfile);
router.put('/profile', authController.updateProfile);
router.put('/change-password', authController.changePassword);

export { router as authRoutes };