import { Entity, Column, OneToMany, ManyToOne, JoinColumn, Index } from 'typeorm';
import { BaseEntity } from './base.entity';
import { UserGroup } from './user-group.entity';
import { GroupPermission } from './group-permission.entity';
import { Company } from './company.entity';
import { IsNotEmpty, IsOptional, IsBoolean, IsEnum } from 'class-validator';

/**
 * Group type enum
 */
export enum GroupType {
  SYSTEM = 'system',
  CUSTOM = 'custom',
  ROLE = 'role',
  DEPARTMENT = 'department',
  TEAM = 'team',
}

/**
 * Group entity
 * Represents user groups for role-based access control
 */
@Entity('groups')
@Index(['name', 'company_id'], { unique: true })
export class Group extends BaseEntity {
  @Column({
    type: 'varchar',
    length: 100,
  })
  @IsNotEmpty()
  name: string;

  @Column({
    type: 'varchar',
    length: 255,
    nullable: true,
  })
  @IsOptional()
  description: string | null;

  @Column({
    type: 'enum',
    enum: GroupType,
    default: GroupType.CUSTOM,
  })
  @IsEnum(GroupType)
  type: GroupType;

  @Column({
    type: 'boolean',
    default: true,
  })
  @IsBoolean()
  is_active: boolean;

  @Column({
    type: 'boolean',
    default: false,
  })
  @IsBoolean()
  is_system: boolean;

  @Column({
    type: 'int',
    default: 0,
  })
  sort_order: number;

  @Column({
    type: 'varchar',
    length: 50,
    nullable: true,
  })
  @IsOptional()
  color: string | null;

  @Column({
    type: 'varchar',
    length: 255,
    nullable: true,
  })
  @IsOptional()
  icon: string | null;

  @Column({
    type: 'jsonb',
    nullable: true,
  })
  @IsOptional()
  settings: Record<string, any> | null;

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
  parent_id: string | null;

  // Relationships
  @ManyToOne(() => Company, (company) => company.groups)
  @JoinColumn({ name: 'company_id' })
  company: Company;

  @ManyToOne(() => Group, (group) => group.children)
  @JoinColumn({ name: 'parent_id' })
  parent: Group;

  @OneToMany(() => Group, (group) => group.parent)
  children: Group[];

  @OneToMany(() => UserGroup, (userGroup) => userGroup.group)
  user_groups: UserGroup[];

  @OneToMany(() => GroupPermission, (groupPermission) => groupPermission.group)
  permissions: GroupPermission[];

  /**
   * Get display name
   */
  getDisplayName(): string {
    return this.name;
  }

  /**
   * Check if group is active
   */
  isActive(): boolean {
    return this.is_active && this.active && !this.isDeleted();
  }

  /**
   * Check if group is system group
   */
  isSystemGroup(): boolean {
    return this.is_system || this.type === GroupType.SYSTEM;
  }

  /**
   * Check if group has parent
   */
  hasParent(): boolean {
    return this.parent_id !== null;
  }

  /**
   * Check if group has children
   */
  hasChildren(): boolean {
    return this.children && this.children.length > 0;
  }

  /**
   * Get all descendants
   */
  getAllDescendants(): Group[] {
    const descendants: Group[] = [];
    if (this.children) {
      for (const child of this.children) {
        descendants.push(child);
        descendants.push(...child.getAllDescendants());
      }
    }
    return descendants;
  }

  /**
   * Get all ancestors
   */
  getAllAncestors(): Group[] {
    const ancestors: Group[] = [];
    if (this.parent) {
      ancestors.push(this.parent);
      ancestors.push(...this.parent.getAllAncestors());
    }
    return ancestors;
  }

  /**
   * Check if group is descendant of another group
   */
  isDescendantOf(group: Group): boolean {
    return this.getAllAncestors().some(ancestor => ancestor.id === group.id);
  }

  /**
   * Check if group is ancestor of another group
   */
  isAncestorOf(group: Group): boolean {
    return group.isDescendantOf(this);
  }

  /**
   * Get user count
   */
  getUserCount(): number {
    return this.user_groups ? this.user_groups.filter(ug => ug.isAssignmentActive()).length : 0;
  }

  /**
   * Get permission count
   */
  getPermissionCount(): number {
    return this.permissions ? this.permissions.length : 0;
  }
}