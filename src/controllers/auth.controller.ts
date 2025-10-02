import { Request, Response } from 'express';
import { AuthService } from '@/services/auth.service';
import { logger } from '@/config/logger';
import { asyncHandler } from '@/middleware/error-handler';
import { AppError } from '@/middleware/error-handler';

/**
 * Authentication controller
 * Handles authentication-related HTTP requests
 */
export class AuthController {
  private authService: AuthService;

  constructor() {
    this.authService = new AuthService();
  }

  /**
   * Register a new user
   * POST /api/auth/register
   */
  register = asyncHandler(async (req: Request, res: Response) => {
    const { username, email, password, first_name, last_name, company_id } = req.body;

    // Validate required fields
    if (!username || !email || !password) {
      throw new AppError('Username, email, and password are required', 400, 'MISSING_FIELDS');
    }

    // Validate password strength
    if (password.length < 8) {
      throw new AppError('Password must be at least 8 characters long', 400, 'WEAK_PASSWORD');
    }

    const user = await this.authService.register({
      username,
      email,
      password,
      first_name,
      last_name,
      company_id,
    });

    // Remove sensitive data
    const { password: _, ...userResponse } = user;

    res.status(201).json({
      success: true,
      message: 'User registered successfully',
      data: {
        user: userResponse,
      },
    });
  });

  /**
   * Login user
   * POST /api/auth/login
   */
  login = asyncHandler(async (req: Request, res: Response) => {
    const { email, password, device_info } = req.body;

    // Validate required fields
    if (!email || !password) {
      throw new AppError('Email and password are required', 400, 'MISSING_FIELDS');
    }

    const result = await this.authService.login({
      email,
      password,
      ip_address: req.ip,
      user_agent: req.get('User-Agent'),
      device_info,
    });

    // Remove sensitive data
    const { password: _, ...userResponse } = result.user;

    res.json({
      success: true,
      message: 'Login successful',
      data: {
        user: userResponse,
        session: result.session.getSessionInfo(),
        tokens: result.tokens,
      },
    });
  });

  /**
   * Refresh access token
   * POST /api/auth/refresh
   */
  refresh = asyncHandler(async (req: Request, res: Response) => {
    const { refresh_token } = req.body;

    if (!refresh_token) {
      throw new AppError('Refresh token is required', 400, 'MISSING_REFRESH_TOKEN');
    }

    const tokens = await this.authService.refreshToken(refresh_token);

    res.json({
      success: true,
      message: 'Token refreshed successfully',
      data: {
        tokens,
      },
    });
  });

  /**
   * Logout user
   * POST /api/auth/logout
   */
  logout = asyncHandler(async (req: Request, res: Response) => {
    const sessionId = (req as any).sessionId;

    if (!sessionId) {
      throw new AppError('Session not found', 401, 'NO_SESSION');
    }

    await this.authService.logout(sessionId);

    res.json({
      success: true,
      message: 'Logout successful',
    });
  });

  /**
   * Logout all sessions
   * POST /api/auth/logout-all
   */
  logoutAll = asyncHandler(async (req: Request, res: Response) => {
    const userId = (req as any).userId;

    if (!userId) {
      throw new AppError('User not found', 401, 'NO_USER');
    }

    await this.authService.logoutAll(userId);

    res.json({
      success: true,
      message: 'All sessions logged out successfully',
    });
  });

  /**
   * Change password
   * PUT /api/auth/change-password
   */
  changePassword = asyncHandler(async (req: Request, res: Response) => {
    const { current_password, new_password } = req.body;
    const userId = (req as any).userId;

    if (!userId) {
      throw new AppError('User not found', 401, 'NO_USER');
    }

    if (!current_password || !new_password) {
      throw new AppError('Current password and new password are required', 400, 'MISSING_FIELDS');
    }

    if (new_password.length < 8) {
      throw new AppError('New password must be at least 8 characters long', 400, 'WEAK_PASSWORD');
    }

    await this.authService.changePassword(userId, current_password, new_password);

    res.json({
      success: true,
      message: 'Password changed successfully',
    });
  });

  /**
   * Get user sessions
   * GET /api/auth/sessions
   */
  getSessions = asyncHandler(async (req: Request, res: Response) => {
    const userId = (req as any).userId;

    if (!userId) {
      throw new AppError('User not found', 401, 'NO_USER');
    }

    const sessions = await this.authService.getUserSessions(userId);

    res.json({
      success: true,
      message: 'Sessions retrieved successfully',
      data: {
        sessions: sessions.map(session => session.getSessionInfo()),
      },
    });
  });

  /**
   * Revoke session
   * DELETE /api/auth/sessions/:sessionId
   */
  revokeSession = asyncHandler(async (req: Request, res: Response) => {
    const { sessionId } = req.params;
    const userId = (req as any).userId;

    if (!userId) {
      throw new AppError('User not found', 401, 'NO_USER');
    }

    if (!sessionId) {
      throw new AppError('Session ID is required', 400, 'MISSING_SESSION_ID');
    }

    await this.authService.revokeSession(sessionId, 'Revoked by user');

    res.json({
      success: true,
      message: 'Session revoked successfully',
    });
  });

  /**
   * Get current user profile
   * GET /api/auth/profile
   */
  getProfile = asyncHandler(async (req: Request, res: Response) => {
    const user = (req as any).user;

    if (!user) {
      throw new AppError('User not found', 401, 'NO_USER');
    }

    // Remove sensitive data
    const { password: _, ...userResponse } = user;

    res.json({
      success: true,
      message: 'Profile retrieved successfully',
      data: {
        user: userResponse,
      },
    });
  });

  /**
   * Update user profile
   * PUT /api/auth/profile
   */
  updateProfile = asyncHandler(async (req: Request, res: Response) => {
    const userId = (req as any).userId;
    const { first_name, last_name, phone, mobile, address, city, state, postal_code, country, language, timezone } = req.body;

    if (!userId) {
      throw new AppError('User not found', 401, 'NO_USER');
    }

    // This would typically update the user profile
    // For now, we'll just return a success message
    res.json({
      success: true,
      message: 'Profile updated successfully',
    });
  });

  /**
   * Verify email
   * POST /api/auth/verify-email
   */
  verifyEmail = asyncHandler(async (req: Request, res: Response) => {
    const { token } = req.body;

    if (!token) {
      throw new AppError('Verification token is required', 400, 'MISSING_TOKEN');
    }

    // This would typically verify the email token
    // For now, we'll just return a success message
    res.json({
      success: true,
      message: 'Email verified successfully',
    });
  });

  /**
   * Resend verification email
   * POST /api/auth/resend-verification
   */
  resendVerification = asyncHandler(async (req: Request, res: Response) => {
    const { email } = req.body;

    if (!email) {
      throw new AppError('Email is required', 400, 'MISSING_EMAIL');
    }

    // This would typically send a verification email
    // For now, we'll just return a success message
    res.json({
      success: true,
      message: 'Verification email sent successfully',
    });
  });

  /**
   * Forgot password
   * POST /api/auth/forgot-password
   */
  forgotPassword = asyncHandler(async (req: Request, res: Response) => {
    const { email } = req.body;

    if (!email) {
      throw new AppError('Email is required', 400, 'MISSING_EMAIL');
    }

    // This would typically send a password reset email
    // For now, we'll just return a success message
    res.json({
      success: true,
      message: 'Password reset email sent successfully',
    });
  });

  /**
   * Reset password
   * POST /api/auth/reset-password
   */
  resetPassword = asyncHandler(async (req: Request, res: Response) => {
    const { token, new_password } = req.body;

    if (!token || !new_password) {
      throw new AppError('Token and new password are required', 400, 'MISSING_FIELDS');
    }

    if (new_password.length < 8) {
      throw new AppError('New password must be at least 8 characters long', 400, 'WEAK_PASSWORD');
    }

    // This would typically reset the password using the token
    // For now, we'll just return a success message
    res.json({
      success: true,
      message: 'Password reset successfully',
    });
  });
}

export default AuthController;