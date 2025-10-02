import { Router } from 'express';
import { CompanyController } from '@/controllers/company.controller';
import { authenticate, validateSession, authorize, requireAdmin } from '@/middleware/auth.middleware';

/**
 * Company routes
 * Handles all company management endpoints
 */
const router = Router();
const companyController = new CompanyController();

// Apply authentication to all company routes
router.use(authenticate);
router.use(validateSession);

/**
 * Company statistics (admin only)
 * GET /api/companies/stats
 */
router.get('/stats', requireAdmin, companyController.getCompanyStats);

/**
 * Company CRUD operations
 */
router.get('/', authorize(['admin', 'manager']), companyController.getCompanies);
router.get('/:id', companyController.getCompanyById);
router.post('/', authorize(['admin']), companyController.createCompany);
router.put('/:id', companyController.updateCompany);
router.delete('/:id', authorize(['admin']), companyController.deleteCompany);
router.post('/:id/restore', authorize(['admin']), companyController.restoreCompany);

/**
 * Company user management
 */
router.get('/:id/users', companyController.getCompanyUsers);
router.post('/:id/users', authorize(['admin', 'manager']), companyController.addUserToCompany);
router.delete('/:id/users/:userId', authorize(['admin', 'manager']), companyController.removeUserFromCompany);

/**
 * Company features and modules
 */
router.get('/:id/features/:feature', companyController.checkCompanyFeature);
router.get('/:id/modules/:module', companyController.checkCompanyModule);
router.post('/:id/features/:feature/enable', authorize(['admin']), companyController.enableCompanyFeature);
router.post('/:id/features/:feature/disable', authorize(['admin']), companyController.disableCompanyFeature);

export { router as companyRoutes };