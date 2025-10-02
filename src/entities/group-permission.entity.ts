import { Entity, Column, ManyToOne, JoinColumn, Index } from 'typeorm';
import { BaseEntity } from './base.entity';
import { Group } from './group.entity';
import { Permission } from './permission.entity';
import { IsNotEmpty, IsOptional, IsBoolean } from 'class-validator';

/**
 * Permission type enum
 */
export enum PermissionType {
  ALLOW = 'allow',
  DENY = 'deny',
  INHERIT = 'inherit',
}

/**
 * Group Permission entity
 * Represents the many-to-many relationship between groups and permissions
 */
@Entity('group_permissions')
@Index(['group_id', 'permission_id'], { unique: true })
export class GroupPermission extends BaseEntity {
  @Column({
    type: 'uuid',
  })
  @IsNotEmpty()
  group_id: string;

  @Column({
    type: 'uuid',
  })
  @IsNotEmpty()
  permission_id: string;

  @Column({
    type: 'enum',
    enum: PermissionType,
    default: PermissionType.ALLOW,
  })
  type: PermissionType;

  @Column({
    type: 'boolean',
    default: true,
  })
  @IsBoolean()
  is_active: boolean;

  @Column({
    type: 'timestamp',
    nullable: true,
  })
  @IsOptional()
  granted_at: Date | null;

  @Column({
    type: 'timestamp',
    nullable: true,
  })
  @IsOptional()
  expires_at: Date | null;

  @Column({
    type: 'uuid',
    nullable: true,
  })
  @IsOptional()
  granted_by: string | null;

  @Column({
    type: 'varchar',
    length: 255,
    nullable: true,
  })
  @IsOptional()
  reason: string | null;

  @Column({
    type: 'jsonb',
    nullable: true,
  })
  @IsOptional()
  conditions: Record<string, any> | null;

  // Relationships
  @ManyToOne(() => Group, (group) => group.permissions)
  @JoinColumn({ name: 'group_id' })
  group: Group;

  @ManyToOne(() => Permission, (permission) => permission.group_permissions)
  @JoinColumn({ name: 'permission_id' })
  permission: Permission;

  /**
   * Check if permission is active
   */
  isPermissionActive(): boolean {
    if (!this.is_active) return false;
    if (this.expires_at && this.expires_at < new Date()) return false;
    return true;
  }

  /**
   * Check if permission is expired
   */
  isExpired(): boolean {
    return this.expires_at ? this.expires_at < new Date() : false;
  }

  /**
   * Check if permission is allowed
   */
  isAllowed(): boolean {
    return this.type === PermissionType.ALLOW && this.isPermissionActive();
  }

  /**
   * Check if permission is denied
   */
  isDenied(): boolean {
    return this.type === PermissionType.DENY && this.isPermissionActive();
  }

  /**
   * Check if permission is inherited
   */
  isInherited(): boolean {
    return this.type === PermissionType.INHERIT;
  }

  /**
   * Get days until expiration
   */
  getDaysUntilExpiration(): number | null {
    if (!this.expires_at) return null;
    const now = new Date();
    const diffTime = this.expires_at.getTime() - now.getTime();
    return Math.ceil(diffTime / (1000 * 60 * 60 * 24));
  }

  /**
   * Grant permission
   */
  grant(grantedBy: string, reason?: string, expiresAt?: Date): void {
    this.type = PermissionType.ALLOW;
    this.is_active = true;
    this.granted_at = new Date();
    this.granted_by = grantedBy;
    this.reason = reason;
    this.expires_at = expiresAt;
  }

  /**
   * Deny permission
   */
  deny(grantedBy: string, reason?: string): void {
    this.type = PermissionType.DENY;
    this.is_active = true;
    this.granted_at = new Date();
    this.granted_by = grantedBy;
    this.reason = reason;
    this.expires_at = null;
  }

  /**
   * Revoke permission
   */
  revoke(): void {
    this.is_active = false;
    this.expires_at = new Date();
  }

  /**
   * Check if permission meets conditions
   */
  meetsConditions(context: Record<string, any>): boolean {
    if (!this.conditions) return true;
    
    for (const [key, value] of Object.entries(this.conditions)) {
      if (context[key] !== value) return false;
    }
    
    return true;
  }
}