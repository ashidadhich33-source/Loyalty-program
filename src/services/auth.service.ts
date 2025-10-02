import bcrypt from 'bcryptjs';
import jwt from 'jsonwebtoken';
import { Repository } from 'typeorm';
import { getConnection } from '@/config/database';
import { User, UserStatus } from '@/entities/user.entity';
import { UserSession, SessionStatus, SessionType } from '@/entities/user-session.entity';
import { config } from '@/config/environment';
import { logger } from '@/config/logger';
import { AppError } from '@/middleware/error-handler';

/**
 * Authentication service
 * Handles user authentication, authorization, and session management
 */
export class AuthService {
  private userRepository: Repository<User>;
  private sessionRepository: Repository<UserSession>;

  constructor() {
    const connection = getConnection();
    this.userRepository = connection.getRepository(User);
    this.sessionRepository = connection.getRepository(UserSession);
  }

  /**
   * Register a new user
   */
  async register(userData: {
    username: string;
    email: string;
    password: string;
    first_name?: string;
    last_name?: string;
    company_id?: string;
  }): Promise<User> {
    try {
      // Check if user already exists
      const existingUser = await this.userRepository.findOne({
        where: [
          { email: userData.email },
          { username: userData.username },
        ],
      });

      if (existingUser) {
        throw new AppError('User already exists', 409, 'USER_EXISTS');
      }

      // Hash password
      const hashedPassword = await bcrypt.hash(userData.password, 12);

      // Create user
      const user = this.userRepository.create({
        ...userData,
        password: hashedPassword,
        status: UserStatus.ACTIVE,
        email_verified: false,
        phone_verified: false,
      });

      const savedUser = await this.userRepository.save(user);

      logger.info('User registered successfully', {
        userId: savedUser.id,
        username: savedUser.username,
        email: savedUser.email,
      });

      return savedUser;
    } catch (error) {
      logger.error('User registration failed', { error, userData });
      throw error;
    }
  }

  /**
   * Authenticate user with email/username and password
   */
  async login(credentials: {
    email: string;
    password: string;
    ip_address?: string;
    user_agent?: string;
    device_info?: {
      device_id?: string;
      device_name?: string;
      device_type?: string;
      browser?: string;
      os?: string;
      location?: string;
    };
  }): Promise<{ user: User; session: UserSession; tokens: { access_token: string; refresh_token: string } }> {
    try {
      // Find user by email or username
      const user = await this.userRepository.findOne({
        where: [
          { email: credentials.email },
          { username: credentials.email },
        ],
        relations: ['company'],
      });

      if (!user) {
        throw new AppError('Invalid credentials', 401, 'INVALID_CREDENTIALS');
      }

      // Check if user can login
      if (!user.canLogin()) {
        throw new AppError('Account is locked or inactive', 401, 'ACCOUNT_LOCKED');
      }

      // Verify password
      const isPasswordValid = await bcrypt.compare(credentials.password, user.password);
      if (!isPasswordValid) {
        user.incrementLoginAttempts();
        await this.userRepository.save(user);
        throw new AppError('Invalid credentials', 401, 'INVALID_CREDENTIALS');
      }

      // Reset login attempts
      user.resetLoginAttempts();
      user.updateLastLogin(credentials.ip_address || '');
      await this.userRepository.save(user);

      // Create session
      const session = await this.createSession(user, {
        ip_address: credentials.ip_address,
        user_agent: credentials.user_agent,
        device_info: credentials.device_info,
      });

      // Generate tokens
      const tokens = await this.generateTokens(user, session);

      logger.info('User logged in successfully', {
        userId: user.id,
        username: user.username,
        sessionId: session.id,
      });

      return { user, session, tokens };
    } catch (error) {
      logger.error('User login failed', { error, email: credentials.email });
      throw error;
    }
  }

  /**
   * Create user session
   */
  async createSession(user: User, sessionData: {
    ip_address?: string;
    user_agent?: string;
    device_info?: {
      device_id?: string;
      device_name?: string;
      device_type?: string;
      browser?: string;
      os?: string;
      location?: string;
    };
  }): Promise<UserSession> {
    try {
      const session = this.sessionRepository.create({
        user_id: user.id,
        token: this.generateSessionToken(),
        refresh_token: this.generateSessionToken(),
        status: SessionStatus.ACTIVE,
        type: SessionType.WEB,
        ip_address: sessionData.ip_address,
        user_agent: sessionData.user_agent,
        device_id: sessionData.device_info?.device_id,
        device_name: sessionData.device_info?.device_name,
        device_type: sessionData.device_info?.device_type,
        browser: sessionData.device_info?.browser,
        os: sessionData.device_info?.os,
        location: sessionData.device_info?.location,
        last_activity: new Date(),
        expires_at: new Date(Date.now() + 24 * 60 * 60 * 1000), // 24 hours
      });

      const savedSession = await this.sessionRepository.save(session);

      logger.info('User session created', {
        userId: user.id,
        sessionId: savedSession.id,
        deviceType: savedSession.device_type,
      });

      return savedSession;
    } catch (error) {
      logger.error('Session creation failed', { error, userId: user.id });
      throw error;
    }
  }

  /**
   * Generate JWT tokens
   */
  async generateTokens(user: User, session: UserSession): Promise<{ access_token: string; refresh_token: string }> {
    try {
      const payload = {
        userId: user.id,
        username: user.username,
        email: user.email,
        role: user.role,
        companyId: user.company_id,
        sessionId: session.id,
      };

      const access_token = jwt.sign(payload, config.jwt.secret, {
        expiresIn: config.jwt.expiresIn,
        issuer: 'erp-system',
        audience: 'erp-users',
      });

      const refresh_token = jwt.sign(
        { userId: user.id, sessionId: session.id },
        config.jwt.secret,
        {
          expiresIn: config.jwt.refreshExpiresIn,
          issuer: 'erp-system',
          audience: 'erp-users',
        }
      );

      return { access_token, refresh_token };
    } catch (error) {
      logger.error('Token generation failed', { error, userId: user.id });
      throw error;
    }
  }

  /**
   * Verify JWT token
   */
  async verifyToken(token: string): Promise<{ user: User; session: UserSession }> {
    try {
      const decoded = jwt.verify(token, config.jwt.secret) as any;

      const user = await this.userRepository.findOne({
        where: { id: decoded.userId },
        relations: ['company'],
      });

      if (!user) {
        throw new AppError('User not found', 401, 'USER_NOT_FOUND');
      }

      const session = await this.sessionRepository.findOne({
        where: { id: decoded.sessionId },
      });

      if (!session || !session.isActive()) {
        throw new AppError('Invalid session', 401, 'INVALID_SESSION');
      }

      // Update session activity
      session.updateLastActivity();
      await this.sessionRepository.save(session);

      return { user, session };
    } catch (error) {
      if (error instanceof jwt.JsonWebTokenError) {
        throw new AppError('Invalid token', 401, 'INVALID_TOKEN');
      }
      if (error instanceof jwt.TokenExpiredError) {
        throw new AppError('Token expired', 401, 'TOKEN_EXPIRED');
      }
      logger.error('Token verification failed', { error });
      throw error;
    }
  }

  /**
   * Refresh access token
   */
  async refreshToken(refreshToken: string): Promise<{ access_token: string; refresh_token: string }> {
    try {
      const decoded = jwt.verify(refreshToken, config.jwt.secret) as any;

      const session = await this.sessionRepository.findOne({
        where: { refresh_token: refreshToken },
        relations: ['user'],
      });

      if (!session || !session.isActive()) {
        throw new AppError('Invalid refresh token', 401, 'INVALID_REFRESH_TOKEN');
      }

      // Generate new tokens
      const tokens = await this.generateTokens(session.user, session);

      // Update session with new refresh token
      session.refresh_token = tokens.refresh_token;
      session.updateLastActivity();
      await this.sessionRepository.save(session);

      logger.info('Token refreshed successfully', {
        userId: session.user_id,
        sessionId: session.id,
      });

      return tokens;
    } catch (error) {
      logger.error('Token refresh failed', { error });
      throw error;
    }
  }

  /**
   * Logout user
   */
  async logout(sessionId: string): Promise<void> {
    try {
      const session = await this.sessionRepository.findOne({
        where: { id: sessionId },
      });

      if (session) {
        session.revoke('User logout');
        await this.sessionRepository.save(session);

        logger.info('User logged out successfully', {
          userId: session.user_id,
          sessionId: session.id,
        });
      }
    } catch (error) {
      logger.error('Logout failed', { error, sessionId });
      throw error;
    }
  }

  /**
   * Logout all user sessions
   */
  async logoutAll(userId: string): Promise<void> {
    try {
      await this.sessionRepository.update(
        { user_id: userId, status: SessionStatus.ACTIVE },
        { status: SessionStatus.REVOKED, revoked_at: new Date(), revoked_reason: 'Logout all sessions' }
      );

      logger.info('All user sessions logged out', { userId });
    } catch (error) {
      logger.error('Logout all sessions failed', { error, userId });
      throw error;
    }
  }

  /**
   * Change user password
   */
  async changePassword(userId: string, currentPassword: string, newPassword: string): Promise<void> {
    try {
      const user = await this.userRepository.findOne({
        where: { id: userId },
      });

      if (!user) {
        throw new AppError('User not found', 404, 'USER_NOT_FOUND');
      }

      // Verify current password
      const isCurrentPasswordValid = await bcrypt.compare(currentPassword, user.password);
      if (!isCurrentPasswordValid) {
        throw new AppError('Current password is incorrect', 400, 'INVALID_CURRENT_PASSWORD');
      }

      // Hash new password
      const hashedNewPassword = await bcrypt.hash(newPassword, 12);

      // Update password
      user.password = hashedNewPassword;
      user.password_changed_at = new Date();
      await this.userRepository.save(user);

      // Logout all sessions
      await this.logoutAll(userId);

      logger.info('Password changed successfully', { userId });
    } catch (error) {
      logger.error('Password change failed', { error, userId });
      throw error;
    }
  }

  /**
   * Generate session token
   */
  private generateSessionToken(): string {
    return Math.random().toString(36).substring(2) + Date.now().toString(36);
  }

  /**
   * Get user sessions
   */
  async getUserSessions(userId: string): Promise<UserSession[]> {
    try {
      const sessions = await this.sessionRepository.find({
        where: { user_id: userId },
        order: { created_at: 'DESC' },
      });

      return sessions;
    } catch (error) {
      logger.error('Get user sessions failed', { error, userId });
      throw error;
    }
  }

  /**
   * Revoke session
   */
  async revokeSession(sessionId: string, reason?: string): Promise<void> {
    try {
      const session = await this.sessionRepository.findOne({
        where: { id: sessionId },
      });

      if (session) {
        session.revoke(reason);
        await this.sessionRepository.save(session);

        logger.info('Session revoked', {
          sessionId,
          userId: session.user_id,
          reason,
        });
      }
    } catch (error) {
      logger.error('Session revocation failed', { error, sessionId });
      throw error;
    }
  }
}

export default AuthService;