import { Repository } from 'typeorm';
import { getConnection } from '@/config/database';
import { User, UserRole, UserStatus } from '@/entities/user.entity';
import { Company } from '@/entities/company.entity';
import { UserGroup } from '@/entities/user-group.entity';
import { Group } from '@/entities/group.entity';
import { logger } from '@/config/logger';
import { AppError } from '@/middleware/error-handler';

/**
 * User service
 * Handles user management operations
 */
export class UserService {
  private userRepository: Repository<User>;
  private companyRepository: Repository<Company>;
  private userGroupRepository: Repository<UserGroup>;
  private groupRepository: Repository<Group>;

  constructor() {
    const connection = getConnection();
    this.userRepository = connection.getRepository(User);
    this.companyRepository = connection.getRepository(Company);
    this.userGroupRepository = connection.getRepository(UserGroup);
    this.groupRepository = connection.getRepository(Group);
  }

  /**
   * Get all users with pagination
   */
  async getUsers(options: {
    page?: number;
    limit?: number;
    search?: string;
    role?: UserRole;
    status?: UserStatus;
    company_id?: string;
    sort_by?: string;
    sort_order?: 'ASC' | 'DESC';
  } = {}): Promise<{ users: User[]; total: number; page: number; limit: number }> {
    try {
      const {
        page = 1,
        limit = 10,
        search,
        role,
        status,
        company_id,
        sort_by = 'created_at',
        sort_order = 'DESC',
      } = options;

      const queryBuilder = this.userRepository
        .createQueryBuilder('user')
        .leftJoinAndSelect('user.company', 'company')
        .leftJoinAndSelect('user.user_groups', 'user_groups')
        .leftJoinAndSelect('user_groups.group', 'group')
        .where('user.deleted_at IS NULL');

      // Apply filters
      if (search) {
        queryBuilder.andWhere(
          '(user.username ILIKE :search OR user.email ILIKE :search OR user.first_name ILIKE :search OR user.last_name ILIKE :search)',
          { search: `%${search}%` }
        );
      }

      if (role) {
        queryBuilder.andWhere('user.role = :role', { role });
      }

      if (status) {
        queryBuilder.andWhere('user.status = :status', { status });
      }

      if (company_id) {
        queryBuilder.andWhere('user.company_id = :company_id', { company_id });
      }

      // Apply sorting
      queryBuilder.orderBy(`user.${sort_by}`, sort_order);

      // Apply pagination
      const offset = (page - 1) * limit;
      queryBuilder.skip(offset).take(limit);

      const [users, total] = await queryBuilder.getManyAndCount();

      return {
        users,
        total,
        page,
        limit,
      };
    } catch (error) {
      logger.error('Get users failed', { error, options });
      throw error;
    }
  }

  /**
   * Get user by ID
   */
  async getUserById(id: string): Promise<User> {
    try {
      const user = await this.userRepository.findOne({
        where: { id },
        relations: ['company', 'user_groups', 'user_groups.group', 'sessions'],
      });

      if (!user) {
        throw new AppError('User not found', 404, 'USER_NOT_FOUND');
      }

      return user;
    } catch (error) {
      logger.error('Get user by ID failed', { error, id });
      throw error;
    }
  }

  /**
   * Get user by email
   */
  async getUserByEmail(email: string): Promise<User | null> {
    try {
      const user = await this.userRepository.findOne({
        where: { email },
        relations: ['company'],
      });

      return user;
    } catch (error) {
      logger.error('Get user by email failed', { error, email });
      throw error;
    }
  }

  /**
   * Get user by username
   */
  async getUserByUsername(username: string): Promise<User | null> {
    try {
      const user = await this.userRepository.findOne({
        where: { username },
        relations: ['company'],
      });

      return user;
    } catch (error) {
      logger.error('Get user by username failed', { error, username });
      throw error;
    }
  }

  /**
   * Create user
   */
  async createUser(userData: {
    username: string;
    email: string;
    password: string;
    first_name?: string;
    last_name?: string;
    phone?: string;
    mobile?: string;
    role?: UserRole;
    status?: UserStatus;
    company_id?: string;
    created_by?: string;
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

      // Validate company if provided
      if (userData.company_id) {
        const company = await this.companyRepository.findOne({
          where: { id: userData.company_id },
        });

        if (!company) {
          throw new AppError('Company not found', 404, 'COMPANY_NOT_FOUND');
        }
      }

      // Create user
      const user = this.userRepository.create({
        ...userData,
        role: userData.role || UserRole.EMPLOYEE,
        status: userData.status || UserStatus.ACTIVE,
      });

      const savedUser = await this.userRepository.save(user);

      logger.info('User created successfully', {
        userId: savedUser.id,
        username: savedUser.username,
        email: savedUser.email,
        createdBy: userData.created_by,
      });

      return savedUser;
    } catch (error) {
      logger.error('Create user failed', { error, userData });
      throw error;
    }
  }

  /**
   * Update user
   */
  async updateUser(id: string, updateData: {
    username?: string;
    email?: string;
    first_name?: string;
    last_name?: string;
    phone?: string;
    mobile?: string;
    address?: string;
    city?: string;
    state?: string;
    postal_code?: string;
    country?: string;
    role?: UserRole;
    status?: UserStatus;
    company_id?: string;
    language?: string;
    timezone?: string;
    preferences?: Record<string, any>;
    updated_by?: string;
  }): Promise<User> {
    try {
      const user = await this.getUserById(id);

      // Check if username/email already exists (if being changed)
      if (updateData.username && updateData.username !== user.username) {
        const existingUser = await this.userRepository.findOne({
          where: { username: updateData.username },
        });
        if (existingUser) {
          throw new AppError('Username already exists', 409, 'USERNAME_EXISTS');
        }
      }

      if (updateData.email && updateData.email !== user.email) {
        const existingUser = await this.userRepository.findOne({
          where: { email: updateData.email },
        });
        if (existingUser) {
          throw new AppError('Email already exists', 409, 'EMAIL_EXISTS');
        }
      }

      // Validate company if being changed
      if (updateData.company_id && updateData.company_id !== user.company_id) {
        const company = await this.companyRepository.findOne({
          where: { id: updateData.company_id },
        });
        if (!company) {
          throw new AppError('Company not found', 404, 'COMPANY_NOT_FOUND');
        }
      }

      // Update user
      Object.assign(user, updateData);
      const updatedUser = await this.userRepository.save(user);

      logger.info('User updated successfully', {
        userId: updatedUser.id,
        updatedBy: updateData.updated_by,
      });

      return updatedUser;
    } catch (error) {
      logger.error('Update user failed', { error, id, updateData });
      throw error;
    }
  }

  /**
   * Delete user (soft delete)
   */
  async deleteUser(id: string, deletedBy?: string): Promise<void> {
    try {
      const user = await this.getUserById(id);

      // Check if user can be deleted
      if (user.isSystemUser()) {
        throw new AppError('System users cannot be deleted', 400, 'CANNOT_DELETE_SYSTEM_USER');
      }

      // Soft delete user
      user.softDelete();
      await this.userRepository.save(user);

      logger.info('User deleted successfully', {
        userId: id,
        deletedBy,
      });
    } catch (error) {
      logger.error('Delete user failed', { error, id });
      throw error;
    }
  }

  /**
   * Restore user
   */
  async restoreUser(id: string, restoredBy?: string): Promise<User> {
    try {
      const user = await this.userRepository.findOne({
        where: { id },
        withDeleted: true,
      });

      if (!user) {
        throw new AppError('User not found', 404, 'USER_NOT_FOUND');
      }

      if (!user.isDeleted()) {
        throw new AppError('User is not deleted', 400, 'USER_NOT_DELETED');
      }

      user.restore();
      const restoredUser = await this.userRepository.save(user);

      logger.info('User restored successfully', {
        userId: id,
        restoredBy,
      });

      return restoredUser;
    } catch (error) {
      logger.error('Restore user failed', { error, id });
      throw error;
    }
  }

  /**
   * Assign user to group
   */
  async assignUserToGroup(userId: string, groupId: string, assignedBy?: string): Promise<UserGroup> {
    try {
      // Check if user exists
      const user = await this.getUserById(userId);

      // Check if group exists
      const group = await this.groupRepository.findOne({
        where: { id: groupId },
      });

      if (!group) {
        throw new AppError('Group not found', 404, 'GROUP_NOT_FOUND');
      }

      // Check if assignment already exists
      const existingAssignment = await this.userGroupRepository.findOne({
        where: { user_id: userId, group_id: groupId },
      });

      if (existingAssignment) {
        throw new AppError('User is already assigned to this group', 409, 'ASSIGNMENT_EXISTS');
      }

      // Create assignment
      const userGroup = this.userGroupRepository.create({
        user_id: userId,
        group_id: groupId,
        assigned_at: new Date(),
        granted_by: assignedBy,
      });

      const savedUserGroup = await this.userGroupRepository.save(userGroup);

      logger.info('User assigned to group successfully', {
        userId,
        groupId,
        assignedBy,
      });

      return savedUserGroup;
    } catch (error) {
      logger.error('Assign user to group failed', { error, userId, groupId });
      throw error;
    }
  }

  /**
   * Remove user from group
   */
  async removeUserFromGroup(userId: string, groupId: string, removedBy?: string): Promise<void> {
    try {
      const userGroup = await this.userGroupRepository.findOne({
        where: { user_id: userId, group_id: groupId },
      });

      if (!userGroup) {
        throw new AppError('User is not assigned to this group', 404, 'ASSIGNMENT_NOT_FOUND');
      }

      await this.userGroupRepository.remove(userGroup);

      logger.info('User removed from group successfully', {
        userId,
        groupId,
        removedBy,
      });
    } catch (error) {
      logger.error('Remove user from group failed', { error, userId, groupId });
      throw error;
    }
  }

  /**
   * Get user groups
   */
  async getUserGroups(userId: string): Promise<UserGroup[]> {
    try {
      const userGroups = await this.userGroupRepository.find({
        where: { user_id: userId },
        relations: ['group'],
        order: { created_at: 'DESC' },
      });

      return userGroups;
    } catch (error) {
      logger.error('Get user groups failed', { error, userId });
      throw error;
    }
  }

  /**
   * Get user permissions
   */
  async getUserPermissions(userId: string): Promise<any[]> {
    try {
      // This would typically get all permissions for a user through their groups
      // For now, we'll return an empty array
      return [];
    } catch (error) {
      logger.error('Get user permissions failed', { error, userId });
      throw error;
    }
  }

  /**
   * Check if user has permission
   */
  async userHasPermission(userId: string, permission: string): Promise<boolean> {
    try {
      // This would typically check if user has specific permission
      // For now, we'll return true for admin users
      const user = await this.getUserById(userId);
      return user.isAdmin();
    } catch (error) {
      logger.error('Check user permission failed', { error, userId, permission });
      throw error;
    }
  }

  /**
   * Get user statistics
   */
  async getUserStats(companyId?: string): Promise<{
    total: number;
    active: number;
    inactive: number;
    byRole: Record<string, number>;
    byStatus: Record<string, number>;
  }> {
    try {
      const queryBuilder = this.userRepository
        .createQueryBuilder('user')
        .where('user.deleted_at IS NULL');

      if (companyId) {
        queryBuilder.andWhere('user.company_id = :companyId', { companyId });
      }

      const users = await queryBuilder.getMany();

      const stats = {
        total: users.length,
        active: users.filter(u => u.isActive()).length,
        inactive: users.filter(u => !u.isActive()).length,
        byRole: {} as Record<string, number>,
        byStatus: {} as Record<string, number>,
      };

      // Count by role
      users.forEach(user => {
        stats.byRole[user.role] = (stats.byRole[user.role] || 0) + 1;
        stats.byStatus[user.status] = (stats.byStatus[user.status] || 0) + 1;
      });

      return stats;
    } catch (error) {
      logger.error('Get user stats failed', { error, companyId });
      throw error;
    }
  }
}

export default UserService;