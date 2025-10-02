import { Entity, Column, ManyToOne, JoinColumn, Index } from 'typeorm';
import { BaseEntity } from './base.entity';
import { User } from './user.entity';
import { Group } from './group.entity';
import { IsNotEmpty, IsOptional, IsBoolean } from 'class-validator';

/**
 * User Group entity
 * Represents the many-to-many relationship between users and groups
 */
@Entity('user_groups')
@Index(['user_id', 'group_id'], { unique: true })
export class UserGroup extends BaseEntity {
  @Column({
    type: 'uuid',
  })
  @IsNotEmpty()
  user_id: string;

  @Column({
    type: 'uuid',
  })
  @IsNotEmpty()
  group_id: string;

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
  assigned_at: Date | null;

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
  assigned_by: string | null;

  // Relationships
  @ManyToOne(() => User, (user) => user.user_groups)
  @JoinColumn({ name: 'user_id' })
  user: User;

  @ManyToOne(() => Group, (group) => group.user_groups)
  @JoinColumn({ name: 'group_id' })
  group: Group;

  /**
   * Check if assignment is active
   */
  isAssignmentActive(): boolean {
    if (!this.is_active) return false;
    if (this.expires_at && this.expires_at < new Date()) return false;
    return true;
  }

  /**
   * Check if assignment is expired
   */
  isExpired(): boolean {
    return this.expires_at ? this.expires_at < new Date() : false;
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
}