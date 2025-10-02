import { Request, Response } from 'express';
import { UserService } from '@/services/user.service';
import { logger } from '@/config/logger';
import { asyncHandler } from '@/middleware/error-handler';
import { AppError } from '@/middleware/error-handler';

/**
 * User controller
 * Handles user management HTTP requests
 */
export class UserController {
  private userService: UserService;

  constructor() {
    this.userService = new UserService();
  }

  /**
   * Get all users
   * GET /api/users
   */
  getUsers = asyncHandler(async (req: Request, res: Response) => {
    const {
      page = 1,
      limit = 10,
      search,
      role,
      status,
      company_id,
      sort_by = 'created_at',
      sort_order = 'DESC',
    } = req.query;

    const options = {
      page: parseInt(page as string),
      limit: parseInt(limit as string),
      search: search as string,
      role: role as string,
      status: status as string,
      company_id: company_id as string,
      sort_by: sort_by as string,
      sort_order: sort_order as 'ASC' | 'DESC',
    };

    const result = await this.userService.getUsers(options);

    res.json({
      success: true,
      message: 'Users retrieved successfully',
      data: {
        users: result.users.map(user => {
          const { password: _, ...userResponse } = user;
          return userResponse;
        }),
        pagination: {
          total: result.total,
          page: result.page,
          limit: result.limit,
          pages: Math.ceil(result.total / result.limit),
        },
      },
    });
  });

  /**
   * Get user by ID
   * GET /api/users/:id
   */
  getUserById = asyncHandler(async (req: Request, res: Response) => {
    const { id } = req.params;

    if (!id) {
      throw new AppError('User ID is required', 400, 'MISSING_USER_ID');
    }

    const user = await this.userService.getUserById(id);

    // Remove sensitive data
    const { password: _, ...userResponse } = user;

    res.json({
      success: true,
      message: 'User retrieved successfully',
      data: {
        user: userResponse,
      },
    });
  });

  /**
   * Create user
   * POST /api/users
   */
  createUser = asyncHandler(async (req: Request, res: Response) => {
    const {
      username,
      email,
      password,
      first_name,
      last_name,
      phone,
      mobile,
      role,
      status,
      company_id,
    } = req.body;

    // Validate required fields
    if (!username || !email || !password) {
      throw new AppError('Username, email, and password are required', 400, 'MISSING_FIELDS');
    }

    const user = await this.userService.createUser({
      username,
      email,
      password,
      first_name,
      last_name,
      phone,
      mobile,
      role,
      status,
      company_id,
      created_by: (req as any).userId,
    });

    // Remove sensitive data
    const { password: _, ...userResponse } = user;

    res.status(201).json({
      success: true,
      message: 'User created successfully',
      data: {
        user: userResponse,
      },
    });
  });

  /**
   * Update user
   * PUT /api/users/:id
   */
  updateUser = asyncHandler(async (req: Request, res: Response) => {
    const { id } = req.params;
    const updateData = req.body;

    if (!id) {
      throw new AppError('User ID is required', 400, 'MISSING_USER_ID');
    }

    const user = await this.userService.updateUser(id, {
      ...updateData,
      updated_by: (req as any).userId,
    });

    // Remove sensitive data
    const { password: _, ...userResponse } = user;

    res.json({
      success: true,
      message: 'User updated successfully',
      data: {
        user: userResponse,
      },
    });
  });

  /**
   * Delete user
   * DELETE /api/users/:id
   */
  deleteUser = asyncHandler(async (req: Request, res: Response) => {
    const { id } = req.params;

    if (!id) {
      throw new AppError('User ID is required', 400, 'MISSING_USER_ID');
    }

    await this.userService.deleteUser(id, (req as any).userId);

    res.json({
      success: true,
      message: 'User deleted successfully',
    });
  });

  /**
   * Restore user
   * POST /api/users/:id/restore
   */
  restoreUser = asyncHandler(async (req: Request, res: Response) => {
    const { id } = req.params;

    if (!id) {
      throw new AppError('User ID is required', 400, 'MISSING_USER_ID');
    }

    const user = await this.userService.restoreUser(id, (req as any).userId);

    // Remove sensitive data
    const { password: _, ...userResponse } = user;

    res.json({
      success: true,
      message: 'User restored successfully',
      data: {
        user: userResponse,
      },
    });
  });

  /**
   * Assign user to group
   * POST /api/users/:id/groups
   */
  assignUserToGroup = asyncHandler(async (req: Request, res: Response) => {
    const { id } = req.params;
    const { group_id } = req.body;

    if (!id) {
      throw new AppError('User ID is required', 400, 'MISSING_USER_ID');
    }

    if (!group_id) {
      throw new AppError('Group ID is required', 400, 'MISSING_GROUP_ID');
    }

    const userGroup = await this.userService.assignUserToGroup(
      id,
      group_id,
      (req as any).userId
    );

    res.status(201).json({
      success: true,
      message: 'User assigned to group successfully',
      data: {
        user_group: userGroup,
      },
    });
  });

  /**
   * Remove user from group
   * DELETE /api/users/:id/groups/:groupId
   */
  removeUserFromGroup = asyncHandler(async (req: Request, res: Response) => {
    const { id, groupId } = req.params;

    if (!id) {
      throw new AppError('User ID is required', 400, 'MISSING_USER_ID');
    }

    if (!groupId) {
      throw new AppError('Group ID is required', 400, 'MISSING_GROUP_ID');
    }

    await this.userService.removeUserFromGroup(id, groupId, (req as any).userId);

    res.json({
      success: true,
      message: 'User removed from group successfully',
    });
  });

  /**
   * Get user groups
   * GET /api/users/:id/groups
   */
  getUserGroups = asyncHandler(async (req: Request, res: Response) => {
    const { id } = req.params;

    if (!id) {
      throw new AppError('User ID is required', 400, 'MISSING_USER_ID');
    }

    const userGroups = await this.userService.getUserGroups(id);

    res.json({
      success: true,
      message: 'User groups retrieved successfully',
      data: {
        user_groups: userGroups,
      },
    });
  });

  /**
   * Get user permissions
   * GET /api/users/:id/permissions
   */
  getUserPermissions = asyncHandler(async (req: Request, res: Response) => {
    const { id } = req.params;

    if (!id) {
      throw new AppError('User ID is required', 400, 'MISSING_USER_ID');
    }

    const permissions = await this.userService.getUserPermissions(id);

    res.json({
      success: true,
      message: 'User permissions retrieved successfully',
      data: {
        permissions,
      },
    });
  });

  /**
   * Check user permission
   * GET /api/users/:id/permissions/:permission
   */
  checkUserPermission = asyncHandler(async (req: Request, res: Response) => {
    const { id, permission } = req.params;

    if (!id) {
      throw new AppError('User ID is required', 400, 'MISSING_USER_ID');
    }

    if (!permission) {
      throw new AppError('Permission is required', 400, 'MISSING_PERMISSION');
    }

    const hasPermission = await this.userService.userHasPermission(id, permission);

    res.json({
      success: true,
      message: 'Permission check completed',
      data: {
        has_permission: hasPermission,
      },
    });
  });

  /**
   * Get user statistics
   * GET /api/users/stats
   */
  getUserStats = asyncHandler(async (req: Request, res: Response) => {
    const { company_id } = req.query;

    const stats = await this.userService.getUserStats(company_id as string);

    res.json({
      success: true,
      message: 'User statistics retrieved successfully',
      data: {
        stats,
      },
    });
  });
}

export default UserController;