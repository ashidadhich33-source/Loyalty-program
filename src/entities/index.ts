/**
 * Entity exports
 * Centralized export of all entities for easy importing
 */

// Base entities
export { BaseEntity } from './base.entity';

// Core entities
export { User, UserRole, UserStatus } from './user.entity';
export { Company, CompanyType, CompanyStatus } from './company.entity';
export { Group, GroupType } from './group.entity';
export { Permission, PermissionType, PermissionCategory } from './permission.entity';

// Relationship entities
export { UserGroup } from './user-group.entity';
export { UserSession, SessionStatus, SessionType } from './user-session.entity';
export { GroupPermission, PermissionType as GroupPermissionType } from './group-permission.entity';

// Entity arrays for TypeORM configuration
export const entities = [
  // Base entities
  BaseEntity,
  
  // Core entities
  User,
  Company,
  Group,
  Permission,
  
  // Relationship entities
  UserGroup,
  UserSession,
  GroupPermission,
];

// Entity metadata for TypeORM
export const entityMetadata = {
  User: {
    tableName: 'users',
    schema: 'public',
  },
  Company: {
    tableName: 'companies',
    schema: 'public',
  },
  Group: {
    tableName: 'groups',
    schema: 'public',
  },
  Permission: {
    tableName: 'permissions',
    schema: 'public',
  },
  UserGroup: {
    tableName: 'user_groups',
    schema: 'public',
  },
  UserSession: {
    tableName: 'user_sessions',
    schema: 'public',
  },
  GroupPermission: {
    tableName: 'group_permissions',
    schema: 'public',
  },
};

// Entity relationships
export const entityRelationships = {
  User: {
    company: 'ManyToOne',
    user_groups: 'OneToMany',
    sessions: 'OneToMany',
  },
  Company: {
    users: 'OneToMany',
    groups: 'OneToMany',
    permissions: 'OneToMany',
  },
  Group: {
    company: 'ManyToOne',
    parent: 'ManyToOne',
    children: 'OneToMany',
    user_groups: 'OneToMany',
    permissions: 'OneToMany',
  },
  Permission: {
    company: 'ManyToOne',
    parent: 'ManyToOne',
    children: 'OneToMany',
    group_permissions: 'OneToMany',
  },
  UserGroup: {
    user: 'ManyToOne',
    group: 'ManyToOne',
  },
  UserSession: {
    user: 'ManyToOne',
  },
  GroupPermission: {
    group: 'ManyToOne',
    permission: 'ManyToOne',
  },
};