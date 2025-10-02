import { Entity, Column, OneToMany, ManyToOne, JoinColumn, Index } from 'typeorm';
import { BaseEntity } from './base.entity';
import { GroupPermission } from './group-permission.entity';
import { Company } from './company.entity';
import { IsNotEmpty, IsOptional, IsBoolean, IsEnum } from 'class-validator';

/**
 * Permission type enum
 */
export enum PermissionType {
  READ = 'read',
  WRITE = 'write',
  DELETE = 'delete',
  EXECUTE = 'execute',
  ADMIN = 'admin',
  CUSTOM = 'custom',
}

/**
 * Permission category enum
 */
export enum PermissionCategory {
  SYSTEM = 'system',
  USER = 'user',
  COMPANY = 'company',
  CONTACT = 'contact',
  PRODUCT = 'product',
  SALES = 'sales',
  CRM = 'crm',
  POS = 'pos',
  INVENTORY = 'inventory',
  PURCHASE = 'purchase',
  ACCOUNTING = 'accounting',
  HR = 'hr',
  REPORT = 'report',
  SETTINGS = 'settings',
}

/**
 * Permission entity
 * Represents system permissions for role-based access control
 */
@Entity('permissions')
@Index(['name', 'company_id'], { unique: true })
@Index(['category'])
export class Permission extends BaseEntity {
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
    type: 'varchar',
    length: 100,
  })
  @IsNotEmpty()
  resource: string;

  @Column({
    type: 'enum',
    enum: PermissionType,
    default: PermissionType.READ,
  })
  @IsEnum(PermissionType)
  type: PermissionType;

  @Column({
    type: 'enum',
    enum: PermissionCategory,
    default: PermissionCategory.SYSTEM,
  })
  @IsEnum(PermissionCategory)
  category: PermissionCategory;

  @Column({
    type: 'varchar',
    length: 100,
    nullable: true,
  })
  @IsOptional()
  action: string | null;

  @Column({
    type: 'varchar',
    length: 255,
    nullable: true,
  })
  @IsOptional()
  module: string | null;

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
  conditions: Record<string, any> | null;

  @Column({
    type: 'jsonb',
    nullable: true,
  })
  @IsOptional()
  metadata: Record<string, any> | null;

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
  @ManyToOne(() => Company, (company) => company.permissions)
  @JoinColumn({ name: 'company_id' })
  company: Company;

  @ManyToOne(() => Permission, (permission) => permission.children)
  @JoinColumn({ name: 'parent_id' })
  parent: Permission;

  @OneToMany(() => Permission, (permission) => permission.parent)
  children: Permission[];

  @OneToMany(() => GroupPermission, (groupPermission) => groupPermission.permission)
  group_permissions: GroupPermission[];

  /**
   * Get display name
   */
  getDisplayName(): string {
    return this.name;
  }

  /**
   * Get full permission name
   */
  getFullName(): string {
    const parts = [this.resource];
    if (this.action) parts.push(this.action);
    if (this.type !== PermissionType.READ) parts.push(this.type);
    return parts.join('.');
  }

  /**
   * Check if permission is active
   */
  isActive(): boolean {
    return this.is_active && this.active && !this.isDeleted();
  }

  /**
   * Check if permission is system permission
   */
  isSystemPermission(): boolean {
    return this.is_system || this.category === PermissionCategory.SYSTEM;
  }

  /**
   * Check if permission has parent
   */
  hasParent(): boolean {
    return this.parent_id !== null;
  }

  /**
   * Check if permission has children
   */
  hasChildren(): boolean {
    return this.children && this.children.length > 0;
  }

  /**
   * Get all descendants
   */
  getAllDescendants(): Permission[] {
    const descendants: Permission[] = [];
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
  getAllAncestors(): Permission[] {
    const ancestors: Permission[] = [];
    if (this.parent) {
      ancestors.push(this.parent);
      ancestors.push(...this.parent.getAllAncestors());
    }
    return ancestors;
  }

  /**
   * Check if permission is descendant of another permission
   */
  isDescendantOf(permission: Permission): boolean {
    return this.getAllAncestors().some(ancestor => ancestor.id === permission.id);
  }

  /**
   * Check if permission is ancestor of another permission
   */
  isAncestorOf(permission: Permission): boolean {
    return permission.isDescendantOf(this);
  }

  /**
   * Check if permission matches resource and action
   */
  matches(resource: string, action?: string): boolean {
    if (this.resource !== resource) return false;
    if (action && this.action && this.action !== action) return false;
    return true;
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

  /**
   * Get permission level
   */
  getLevel(): number {
    let level = 0;
    let current = this.parent;
    while (current) {
      level++;
      current = current.parent;
    }
    return level;
  }

  /**
   * Get permission path
   */
  getPath(): string {
    const path = [this.name];
    let current = this.parent;
    while (current) {
      path.unshift(current.name);
      current = current.parent;
    }
    return path.join(' > ');
  }
}