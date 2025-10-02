import { Router } from 'express';
import { UserController } from '@/controllers/user.controller';
import { authenticate, validateSession, authorize, requireAdmin } from '@/middleware/auth.middleware';

/**
 * User routes
 * Handles all user management endpoints
 */
const router = Router();
const userController = new UserController();

// Apply authentication to all user routes
router.use(authenticate);
router.use(validateSession);

/**
 * User statistics (admin only)
 * GET /api/users/stats
 */
router.get('/stats', requireAdmin, userController.getUserStats);

/**
 * User CRUD operations
 */
router.get('/', authorize(['admin', 'manager']), userController.getUsers);
router.get('/:id', userController.getUserById);
router.post('/', authorize(['admin']), userController.createUser);
router.put('/:id', userController.updateUser);
router.delete('/:id', authorize(['admin']), userController.deleteUser);
router.post('/:id/restore', authorize(['admin']), userController.restoreUser);

/**
 * User group management
 */
router.get('/:id/groups', userController.getUserGroups);
router.post('/:id/groups', authorize(['admin', 'manager']), userController.assignUserToGroup);
router.delete('/:id/groups/:groupId', authorize(['admin', 'manager']), userController.removeUserFromGroup);

/**
 * User permissions
 */
router.get('/:id/permissions', userController.getUserPermissions);
router.get('/:id/permissions/:permission', userController.checkUserPermission);

export { router as userRoutes };