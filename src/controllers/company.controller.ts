import { Request, Response } from 'express';
import { CompanyService } from '@/services/company.service';
import { logger } from '@/config/logger';
import { asyncHandler } from '@/middleware/error-handler';
import { AppError } from '@/middleware/error-handler';

/**
 * Company controller
 * Handles company management HTTP requests
 */
export class CompanyController {
  private companyService: CompanyService;

  constructor() {
    this.companyService = new CompanyService();
  }

  /**
   * Get all companies
   * GET /api/companies
   */
  getCompanies = asyncHandler(async (req: Request, res: Response) => {
    const {
      page = 1,
      limit = 10,
      search,
      type,
      status,
      sort_by = 'created_at',
      sort_order = 'DESC',
    } = req.query;

    const options = {
      page: parseInt(page as string),
      limit: parseInt(limit as string),
      search: search as string,
      type: type as string,
      status: status as string,
      sort_by: sort_by as string,
      sort_order: sort_order as 'ASC' | 'DESC',
    };

    const result = await this.companyService.getCompanies(options);

    res.json({
      success: true,
      message: 'Companies retrieved successfully',
      data: {
        companies: result.companies,
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
   * Get company by ID
   * GET /api/companies/:id
   */
  getCompanyById = asyncHandler(async (req: Request, res: Response) => {
    const { id } = req.params;

    if (!id) {
      throw new AppError('Company ID is required', 400, 'MISSING_COMPANY_ID');
    }

    const company = await this.companyService.getCompanyById(id);

    res.json({
      success: true,
      message: 'Company retrieved successfully',
      data: {
        company,
      },
    });
  });

  /**
   * Create company
   * POST /api/companies
   */
  createCompany = asyncHandler(async (req: Request, res: Response) => {
    const companyData = req.body;

    // Validate required fields
    if (!companyData.name) {
      throw new AppError('Company name is required', 400, 'MISSING_COMPANY_NAME');
    }

    const company = await this.companyService.createCompany({
      ...companyData,
      created_by: (req as any).userId,
    });

    res.status(201).json({
      success: true,
      message: 'Company created successfully',
      data: {
        company,
      },
    });
  });

  /**
   * Update company
   * PUT /api/companies/:id
   */
  updateCompany = asyncHandler(async (req: Request, res: Response) => {
    const { id } = req.params;
    const updateData = req.body;

    if (!id) {
      throw new AppError('Company ID is required', 400, 'MISSING_COMPANY_ID');
    }

    const company = await this.companyService.updateCompany(id, {
      ...updateData,
      updated_by: (req as any).userId,
    });

    res.json({
      success: true,
      message: 'Company updated successfully',
      data: {
        company,
      },
    });
  });

  /**
   * Delete company
   * DELETE /api/companies/:id
   */
  deleteCompany = asyncHandler(async (req: Request, res: Response) => {
    const { id } = req.params;

    if (!id) {
      throw new AppError('Company ID is required', 400, 'MISSING_COMPANY_ID');
    }

    await this.companyService.deleteCompany(id, (req as any).userId);

    res.json({
      success: true,
      message: 'Company deleted successfully',
    });
  });

  /**
   * Restore company
   * POST /api/companies/:id/restore
   */
  restoreCompany = asyncHandler(async (req: Request, res: Response) => {
    const { id } = req.params;

    if (!id) {
      throw new AppError('Company ID is required', 400, 'MISSING_COMPANY_ID');
    }

    const company = await this.companyService.restoreCompany(id, (req as any).userId);

    res.json({
      success: true,
      message: 'Company restored successfully',
      data: {
        company,
      },
    });
  });

  /**
   * Get company users
   * GET /api/companies/:id/users
   */
  getCompanyUsers = asyncHandler(async (req: Request, res: Response) => {
    const { id } = req.params;
    const {
      page = 1,
      limit = 10,
      search,
      role,
      status,
    } = req.query;

    if (!id) {
      throw new AppError('Company ID is required', 400, 'MISSING_COMPANY_ID');
    }

    const options = {
      page: parseInt(page as string),
      limit: parseInt(limit as string),
      search: search as string,
      role: role as string,
      status: status as string,
    };

    const result = await this.companyService.getCompanyUsers(id, options);

    res.json({
      success: true,
      message: 'Company users retrieved successfully',
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
   * Add user to company
   * POST /api/companies/:id/users
   */
  addUserToCompany = asyncHandler(async (req: Request, res: Response) => {
    const { id } = req.params;
    const { user_id } = req.body;

    if (!id) {
      throw new AppError('Company ID is required', 400, 'MISSING_COMPANY_ID');
    }

    if (!user_id) {
      throw new AppError('User ID is required', 400, 'MISSING_USER_ID');
    }

    await this.companyService.addUserToCompany(id, user_id, (req as any).userId);

    res.json({
      success: true,
      message: 'User added to company successfully',
    });
  });

  /**
   * Remove user from company
   * DELETE /api/companies/:id/users/:userId
   */
  removeUserFromCompany = asyncHandler(async (req: Request, res: Response) => {
    const { id, userId } = req.params;

    if (!id) {
      throw new AppError('Company ID is required', 400, 'MISSING_COMPANY_ID');
    }

    if (!userId) {
      throw new AppError('User ID is required', 400, 'MISSING_USER_ID');
    }

    await this.companyService.removeUserFromCompany(id, userId, (req as any).userId);

    res.json({
      success: true,
      message: 'User removed from company successfully',
    });
  });

  /**
   * Get company statistics
   * GET /api/companies/stats
   */
  getCompanyStats = asyncHandler(async (req: Request, res: Response) => {
    const { company_id } = req.query;

    const stats = await this.companyService.getCompanyStats(company_id as string);

    res.json({
      success: true,
      message: 'Company statistics retrieved successfully',
      data: {
        stats,
      },
    });
  });

  /**
   * Check company feature
   * GET /api/companies/:id/features/:feature
   */
  checkCompanyFeature = asyncHandler(async (req: Request, res: Response) => {
    const { id, feature } = req.params;

    if (!id) {
      throw new AppError('Company ID is required', 400, 'MISSING_COMPANY_ID');
    }

    if (!feature) {
      throw new AppError('Feature is required', 400, 'MISSING_FEATURE');
    }

    const hasFeature = await this.companyService.companyHasFeature(id, feature);

    res.json({
      success: true,
      message: 'Company feature check completed',
      data: {
        has_feature: hasFeature,
      },
    });
  });

  /**
   * Check company module
   * GET /api/companies/:id/modules/:module
   */
  checkCompanyModule = asyncHandler(async (req: Request, res: Response) => {
    const { id, module } = req.params;

    if (!id) {
      throw new AppError('Company ID is required', 400, 'MISSING_COMPANY_ID');
    }

    if (!module) {
      throw new AppError('Module is required', 400, 'MISSING_MODULE');
    }

    const hasModule = await this.companyService.companyHasModule(id, module);

    res.json({
      success: true,
      message: 'Company module check completed',
      data: {
        has_module: hasModule,
      },
    });
  });

  /**
   * Enable company feature
   * POST /api/companies/:id/features/:feature/enable
   */
  enableCompanyFeature = asyncHandler(async (req: Request, res: Response) => {
    const { id, feature } = req.params;

    if (!id) {
      throw new AppError('Company ID is required', 400, 'MISSING_COMPANY_ID');
    }

    if (!feature) {
      throw new AppError('Feature is required', 400, 'MISSING_FEATURE');
    }

    await this.companyService.enableCompanyFeature(id, feature, (req as any).userId);

    res.json({
      success: true,
      message: 'Company feature enabled successfully',
    });
  });

  /**
   * Disable company feature
   * POST /api/companies/:id/features/:feature/disable
   */
  disableCompanyFeature = asyncHandler(async (req: Request, res: Response) => {
    const { id, feature } = req.params;

    if (!id) {
      throw new AppError('Company ID is required', 400, 'MISSING_COMPANY_ID');
    }

    if (!feature) {
      throw new AppError('Feature is required', 400, 'MISSING_FEATURE');
    }

    await this.companyService.disableCompanyFeature(id, feature, (req as any).userId);

    res.json({
      success: true,
      message: 'Company feature disabled successfully',
    });
  });
}

export default CompanyController;