import { Entity, Column, OneToMany, ManyToOne, JoinColumn, Index } from 'typeorm';
import { BaseEntity } from './base.entity';
import { Company } from './company.entity';
import { UserGroup } from './user-group.entity';
import { UserSession } from './user-session.entity';
import { IsEmail, IsNotEmpty, IsOptional, IsBoolean, IsEnum } from 'class-validator';
import { Exclude } from 'class-transformer';

/**
 * User roles enum
 */
export enum UserRole {
  SUPER_ADMIN = 'super_admin',
  ADMIN = 'admin',
  MANAGER = 'manager',
  EMPLOYEE = 'employee',
  CASHIER = 'cashier',
  SALES = 'sales',
  ACCOUNTANT = 'accountant',
  HR = 'hr',
  INVENTORY = 'inventory',
  PURCHASE = 'purchase',
  CUSTOMER = 'customer',
  SUPPLIER = 'supplier',
}

/**
 * User status enum
 */
export enum UserStatus {
  ACTIVE = 'active',
  INACTIVE = 'inactive',
  PENDING = 'pending',
  SUSPENDED = 'suspended',
  LOCKED = 'locked',
}

/**
 * User entity
 * Represents system users with authentication and authorization
 */
@Entity('users')
@Index(['email', 'company_id'], { unique: true })
@Index(['username', 'company_id'], { unique: true })
export class User extends BaseEntity {
  @Column({
    type: 'varchar',
    length: 100,
    unique: true,
  })
  @IsNotEmpty()
  username: string;

  @Column({
    type: 'varchar',
    length: 255,
  })
  @IsEmail()
  email: string;

  @Column({
    type: 'varchar',
    length: 255,
  })
  @Exclude()
  password: string;

  @Column({
    type: 'varchar',
    length: 100,
    nullable: true,
  })
  @IsOptional()
  first_name: string | null;

  @Column({
    type: 'varchar',
    length: 100,
    nullable: true,
  })
  @IsOptional()
  last_name: string | null;

  @Column({
    type: 'varchar',
    length: 20,
    nullable: true,
  })
  @IsOptional()
  phone: string | null;

  @Column({
    type: 'varchar',
    length: 20,
    nullable: true,
  })
  @IsOptional()
  mobile: string | null;

  @Column({
    type: 'text',
    nullable: true,
  })
  @IsOptional()
  address: string | null;

  @Column({
    type: 'varchar',
    length: 100,
    nullable: true,
  })
  @IsOptional()
  city: string | null;

  @Column({
    type: 'varchar',
    length: 100,
    nullable: true,
  })
  @IsOptional()
  state: string | null;

  @Column({
    type: 'varchar',
    length: 20,
    nullable: true,
  })
  @IsOptional()
  postal_code: string | null;

  @Column({
    type: 'varchar',
    length: 100,
    nullable: true,
  })
  @IsOptional()
  country: string | null;

  @Column({
    type: 'enum',
    enum: UserRole,
    default: UserRole.EMPLOYEE,
  })
  @IsEnum(UserRole)
  role: UserRole;

  @Column({
    type: 'enum',
    enum: UserStatus,
    default: UserStatus.ACTIVE,
  })
  @IsEnum(UserStatus)
  status: UserStatus;

  @Column({
    type: 'boolean',
    default: false,
  })
  @IsBoolean()
  email_verified: boolean;

  @Column({
    type: 'boolean',
    default: false,
  })
  @IsBoolean()
  phone_verified: boolean;

  @Column({
    type: 'timestamp',
    nullable: true,
  })
  @IsOptional()
  last_login: Date | null;

  @Column({
    type: 'varchar',
    length: 45,
    nullable: true,
  })
  @IsOptional()
  last_login_ip: string | null;

  @Column({
    type: 'timestamp',
    nullable: true,
  })
  @IsOptional()
  password_changed_at: Date | null;

  @Column({
    type: 'int',
    default: 0,
  })
  login_attempts: number;

  @Column({
    type: 'timestamp',
    nullable: true,
  })
  @IsOptional()
  locked_until: Date | null;

  @Column({
    type: 'varchar',
    length: 255,
    nullable: true,
  })
  @IsOptional()
  avatar: string | null;

  @Column({
    type: 'varchar',
    length: 10,
    default: 'en',
  })
  @IsOptional()
  language: string;

  @Column({
    type: 'varchar',
    length: 10,
    default: 'UTC',
  })
  @IsOptional()
  timezone: string;

  @Column({
    type: 'jsonb',
    nullable: true,
  })
  @IsOptional()
  preferences: Record<string, any> | null;

  @Column({
    type: 'uuid',
    nullable: true,
  })
  @IsOptional()
  company_id: string | null;

  @Column({
    type: 'uuid',
    nullable: true,
  })
  @IsOptional()
  created_by: string | null;

  @Column({
    type: 'uuid',
    nullable: true,
  })
  @IsOptional()
  updated_by: string | null;

  // Relationships
  @ManyToOne(() => Company, (company) => company.users)
  @JoinColumn({ name: 'company_id' })
  company: Company;

  @OneToMany(() => UserGroup, (userGroup) => userGroup.user)
  user_groups: UserGroup[];

  @OneToMany(() => UserSession, (session) => session.user)
  sessions: UserSession[];

  /**
   * Get full name
   */
  getFullName(): string {
    if (this.first_name && this.last_name) {
      return `${this.first_name} ${this.last_name}`;
    }
    return this.first_name || this.last_name || this.username;
  }

  /**
   * Check if user is locked
   */
  isLocked(): boolean {
    return this.locked_until && this.locked_until > new Date();
  }

  /**
   * Check if user is active
   */
  isActive(): boolean {
    return this.status === UserStatus.ACTIVE && this.active && !this.isDeleted();
  }

  /**
   * Check if user can login
   */
  canLogin(): boolean {
    return this.isActive() && !this.isLocked();
  }

  /**
   * Increment login attempts
   */
  incrementLoginAttempts(): void {
    this.login_attempts += 1;
    if (this.login_attempts >= 5) {
      this.locked_until = new Date(Date.now() + 30 * 60 * 1000); // 30 minutes
    }
  }

  /**
   * Reset login attempts
   */
  resetLoginAttempts(): void {
    this.login_attempts = 0;
    this.locked_until = null;
  }

  /**
   * Update last login
   */
  updateLastLogin(ip: string): void {
    this.last_login = new Date();
    this.last_login_ip = ip;
    this.resetLoginAttempts();
  }

  /**
   * Check if user has role
   */
  hasRole(role: UserRole): boolean {
    return this.role === role;
  }

  /**
   * Check if user has any of the roles
   */
  hasAnyRole(roles: UserRole[]): boolean {
    return roles.includes(this.role);
  }

  /**
   * Check if user is admin
   */
  isAdmin(): boolean {
    return this.hasAnyRole([UserRole.SUPER_ADMIN, UserRole.ADMIN]);
  }

  /**
   * Check if user is manager
   */
  isManager(): boolean {
    return this.hasAnyRole([UserRole.SUPER_ADMIN, UserRole.ADMIN, UserRole.MANAGER]);
  }
}