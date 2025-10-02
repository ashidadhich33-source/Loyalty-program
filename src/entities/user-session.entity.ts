import { Entity, Column, ManyToOne, JoinColumn, Index } from 'typeorm';
import { BaseEntity } from './base.entity';
import { User } from './user.entity';
import { IsNotEmpty, IsOptional, IsBoolean, IsEnum } from 'class-validator';

/**
 * Session status enum
 */
export enum SessionStatus {
  ACTIVE = 'active',
  EXPIRED = 'expired',
  REVOKED = 'revoked',
  SUSPENDED = 'suspended',
}

/**
 * Session type enum
 */
export enum SessionType {
  WEB = 'web',
  MOBILE = 'mobile',
  API = 'api',
  POS = 'pos',
  ADMIN = 'admin',
}

/**
 * User Session entity
 * Represents user sessions for authentication and authorization
 */
@Entity('user_sessions')
@Index(['user_id', 'token'], { unique: true })
@Index(['token'])
@Index(['expires_at'])
export class UserSession extends BaseEntity {
  @Column({
    type: 'uuid',
  })
  @IsNotEmpty()
  user_id: string;

  @Column({
    type: 'varchar',
    length: 500,
    unique: true,
  })
  @IsNotEmpty()
  token: string;

  @Column({
    type: 'varchar',
    length: 500,
    nullable: true,
  })
  @IsOptional()
  refresh_token: string | null;

  @Column({
    type: 'enum',
    enum: SessionStatus,
    default: SessionStatus.ACTIVE,
  })
  @IsEnum(SessionStatus)
  status: SessionStatus;

  @Column({
    type: 'enum',
    enum: SessionType,
    default: SessionType.WEB,
  })
  @IsEnum(SessionType)
  type: SessionType;

  @Column({
    type: 'varchar',
    length: 45,
    nullable: true,
  })
  @IsOptional()
  ip_address: string | null;

  @Column({
    type: 'varchar',
    length: 500,
    nullable: true,
  })
  @IsOptional()
  user_agent: string | null;

  @Column({
    type: 'varchar',
    length: 100,
    nullable: true,
  })
  @IsOptional()
  device_id: string | null;

  @Column({
    type: 'varchar',
    length: 100,
    nullable: true,
  })
  @IsOptional()
  device_name: string | null;

  @Column({
    type: 'varchar',
    length: 50,
    nullable: true,
  })
  @IsOptional()
  device_type: string | null;

  @Column({
    type: 'varchar',
    length: 100,
    nullable: true,
  })
  @IsOptional()
  browser: string | null;

  @Column({
    type: 'varchar',
    length: 100,
    nullable: true,
  })
  @IsOptional()
  os: string | null;

  @Column({
    type: 'varchar',
    length: 100,
    nullable: true,
  })
  @IsOptional()
  location: string | null;

  @Column({
    type: 'timestamp',
    nullable: true,
  })
  @IsOptional()
  last_activity: Date | null;

  @Column({
    type: 'timestamp',
    nullable: true,
  })
  @IsOptional()
  expires_at: Date | null;

  @Column({
    type: 'timestamp',
    nullable: true,
  })
  @IsOptional()
  revoked_at: Date | null;

  @Column({
    type: 'varchar',
    length: 255,
    nullable: true,
  })
  @IsOptional()
  revoked_reason: string | null;

  @Column({
    type: 'jsonb',
    nullable: true,
  })
  @IsOptional()
  metadata: Record<string, any> | null;

  // Relationships
  @ManyToOne(() => User, (user) => user.sessions)
  @JoinColumn({ name: 'user_id' })
  user: User;

  /**
   * Check if session is active
   */
  isActive(): boolean {
    return this.status === SessionStatus.ACTIVE && 
           this.active && 
           !this.isDeleted() &&
           (!this.expires_at || this.expires_at > new Date());
  }

  /**
   * Check if session is expired
   */
  isExpired(): boolean {
    return this.expires_at ? this.expires_at <= new Date() : false;
  }

  /**
   * Check if session is revoked
   */
  isRevoked(): boolean {
    return this.status === SessionStatus.REVOKED;
  }

  /**
   * Check if session is suspended
   */
  isSuspended(): boolean {
    return this.status === SessionStatus.SUSPENDED;
  }

  /**
   * Get session duration in minutes
   */
  getDurationMinutes(): number {
    if (!this.last_activity) return 0;
    const now = new Date();
    const diffTime = Math.abs(now.getTime() - this.last_activity.getTime());
    return Math.ceil(diffTime / (1000 * 60));
  }

  /**
   * Get time until expiration in minutes
   */
  getTimeUntilExpiration(): number | null {
    if (!this.expires_at) return null;
    const now = new Date();
    const diffTime = this.expires_at.getTime() - now.getTime();
    return Math.ceil(diffTime / (1000 * 60));
  }

  /**
   * Update last activity
   */
  updateLastActivity(): void {
    this.last_activity = new Date();
  }

  /**
   * Revoke session
   */
  revoke(reason?: string): void {
    this.status = SessionStatus.REVOKED;
    this.revoked_at = new Date();
    this.revoked_reason = reason || 'Manually revoked';
  }

  /**
   * Suspend session
   */
  suspend(): void {
    this.status = SessionStatus.SUSPENDED;
  }

  /**
   * Activate session
   */
  activate(): void {
    this.status = SessionStatus.ACTIVE;
    this.revoked_at = null;
    this.revoked_reason = null;
  }

  /**
   * Extend session
   */
  extend(expiresAt: Date): void {
    this.expires_at = expiresAt;
    this.updateLastActivity();
  }

  /**
   * Get session info
   */
  getSessionInfo(): Record<string, any> {
    return {
      id: this.id,
      type: this.type,
      status: this.status,
      device: {
        id: this.device_id,
        name: this.device_name,
        type: this.device_type,
        browser: this.browser,
        os: this.os,
      },
      location: this.location,
      ip_address: this.ip_address,
      last_activity: this.last_activity,
      expires_at: this.expires_at,
      created_at: this.created_at,
    };
  }
}