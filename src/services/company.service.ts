import { Repository } from 'typeorm';
import { getConnection } from '@/config/database';
import { Company, CompanyType, CompanyStatus } from '@/entities/company.entity';
import { User } from '@/entities/user.entity';
import { logger } from '@/config/logger';
import { AppError } from '@/middleware/error-handler';

/**
 * Company service
 * Handles company management operations
 */
export class CompanyService {
  private companyRepository: Repository<Company>;
  private userRepository: Repository<User>;

  constructor() {
    const connection = getConnection();
    this.companyRepository = connection.getRepository(Company);
    this.userRepository = connection.getRepository(User);
  }

  /**
   * Get all companies with pagination
   */
  async getCompanies(options: {
    page?: number;
    limit?: number;
    search?: string;
    type?: CompanyType;
    status?: CompanyStatus;
    sort_by?: string;
    sort_order?: 'ASC' | 'DESC';
  } = {}): Promise<{ companies: Company[]; total: number; page: number; limit: number }> {
    try {
      const {
        page = 1,
        limit = 10,
        search,
        type,
        status,
        sort_by = 'created_at',
        sort_order = 'DESC',
      } = options;

      const queryBuilder = this.companyRepository
        .createQueryBuilder('company')
        .leftJoinAndSelect('company.users', 'users')
        .where('company.deleted_at IS NULL');

      // Apply filters
      if (search) {
        queryBuilder.andWhere(
          '(company.name ILIKE :search OR company.legal_name ILIKE :search OR company.email ILIKE :search)',
          { search: `%${search}%` }
        );
      }

      if (type) {
        queryBuilder.andWhere('company.type = :type', { type });
      }

      if (status) {
        queryBuilder.andWhere('company.status = :status', { status });
      }

      // Apply sorting
      queryBuilder.orderBy(`company.${sort_by}`, sort_order);

      // Apply pagination
      const offset = (page - 1) * limit;
      queryBuilder.skip(offset).take(limit);

      const [companies, total] = await queryBuilder.getManyAndCount();

      return {
        companies,
        total,
        page,
        limit,
      };
    } catch (error) {
      logger.error('Get companies failed', { error, options });
      throw error;
    }
  }

  /**
   * Get company by ID
   */
  async getCompanyById(id: string): Promise<Company> {
    try {
      const company = await this.companyRepository.findOne({
        where: { id },
        relations: ['users'],
      });

      if (!company) {
        throw new AppError('Company not found', 404, 'COMPANY_NOT_FOUND');
      }

      return company;
    } catch (error) {
      logger.error('Get company by ID failed', { error, id });
      throw error;
    }
  }

  /**
   * Get company by name
   */
  async getCompanyByName(name: string): Promise<Company | null> {
    try {
      const company = await this.companyRepository.findOne({
        where: { name },
      });

      return company;
    } catch (error) {
      logger.error('Get company by name failed', { error, name });
      throw error;
    }
  }

  /**
   * Create company
   */
  async createCompany(companyData: {
    name: string;
    legal_name?: string;
    registration_number?: string;
    gstin?: string;
    pan?: string;
    tan?: string;
    cin?: string;
    website?: string;
    email?: string;
    phone?: string;
    mobile?: string;
    address?: string;
    city?: string;
    state?: string;
    postal_code?: string;
    country?: string;
    type?: CompanyType;
    status?: CompanyStatus;
    currency?: string;
    language?: string;
    timezone?: string;
    fiscal_year_start?: Date;
    fiscal_year_end?: Date;
    description?: string;
    settings?: Record<string, any>;
    features?: Record<string, any>;
    modules?: Record<string, any>;
    gst_enabled?: boolean;
    pos_enabled?: boolean;
    ecommerce_enabled?: boolean;
    multi_warehouse?: boolean;
    multi_company?: boolean;
    created_by?: string;
  }): Promise<Company> {
    try {
      // Check if company already exists
      const existingCompany = await this.companyRepository.findOne({
        where: { name: companyData.name },
      });

      if (existingCompany) {
        throw new AppError('Company already exists', 409, 'COMPANY_EXISTS');
      }

      // Create company
      const company = this.companyRepository.create({
        ...companyData,
        type: companyData.type || CompanyType.RETAIL,
        status: companyData.status || CompanyStatus.ACTIVE,
        currency: companyData.currency || 'INR',
        language: companyData.language || 'en',
        timezone: companyData.timezone || 'UTC',
        gst_enabled: companyData.gst_enabled || false,
        pos_enabled: companyData.pos_enabled || false,
        ecommerce_enabled: companyData.ecommerce_enabled || false,
        multi_warehouse: companyData.multi_warehouse || false,
        multi_company: companyData.multi_company || false,
      });

      const savedCompany = await this.companyRepository.save(company);

      logger.info('Company created successfully', {
        companyId: savedCompany.id,
        name: savedCompany.name,
        createdBy: companyData.created_by,
      });

      return savedCompany;
    } catch (error) {
      logger.error('Create company failed', { error, companyData });
      throw error;
    }
  }

  /**
   * Update company
   */
  async updateCompany(id: string, updateData: {
    name?: string;
    legal_name?: string;
    registration_number?: string;
    gstin?: string;
    pan?: string;
    tan?: string;
    cin?: string;
    website?: string;
    email?: string;
    phone?: string;
    mobile?: string;
    address?: string;
    city?: string;
    state?: string;
    postal_code?: string;
    country?: string;
    type?: CompanyType;
    status?: CompanyStatus;
    currency?: string;
    language?: string;
    timezone?: string;
    fiscal_year_start?: Date;
    fiscal_year_end?: Date;
    description?: string;
    settings?: Record<string, any>;
    features?: Record<string, any>;
    modules?: Record<string, any>;
    gst_enabled?: boolean;
    pos_enabled?: boolean;
    ecommerce_enabled?: boolean;
    multi_warehouse?: boolean;
    multi_company?: boolean;
    updated_by?: string;
  }): Promise<Company> {
    try {
      const company = await this.getCompanyById(id);

      // Check if name already exists (if being changed)
      if (updateData.name && updateData.name !== company.name) {
        const existingCompany = await this.companyRepository.findOne({
          where: { name: updateData.name },
        });
        if (existingCompany) {
          throw new AppError('Company name already exists', 409, 'COMPANY_NAME_EXISTS');
        }
      }

      // Update company
      Object.assign(company, updateData);
      const updatedCompany = await this.companyRepository.save(company);

      logger.info('Company updated successfully', {
        companyId: updatedCompany.id,
        updatedBy: updateData.updated_by,
      });

      return updatedCompany;
    } catch (error) {
      logger.error('Update company failed', { error, id, updateData });
      throw error;
    }
  }

  /**
   * Delete company (soft delete)
   */
  async deleteCompany(id: string, deletedBy?: string): Promise<void> {
    try {
      const company = await this.getCompanyById(id);

      // Check if company has users
      const userCount = await this.userRepository.count({
        where: { company_id: id },
      });

      if (userCount > 0) {
        throw new AppError('Cannot delete company with users', 400, 'COMPANY_HAS_USERS');
      }

      // Soft delete company
      company.softDelete();
      await this.companyRepository.save(company);

      logger.info('Company deleted successfully', {
        companyId: id,
        deletedBy,
      });
    } catch (error) {
      logger.error('Delete company failed', { error, id });
      throw error;
    }
  }

  /**
   * Restore company
   */
  async restoreCompany(id: string, restoredBy?: string): Promise<Company> {
    try {
      const company = await this.companyRepository.findOne({
        where: { id },
        withDeleted: true,
      });

      if (!company) {
        throw new AppError('Company not found', 404, 'COMPANY_NOT_FOUND');
      }

      if (!company.isDeleted()) {
        throw new AppError('Company is not deleted', 400, 'COMPANY_NOT_DELETED');
      }

      company.restore();
      const restoredCompany = await this.companyRepository.save(company);

      logger.info('Company restored successfully', {
        companyId: id,
        restoredBy,
      });

      return restoredCompany;
    } catch (error) {
      logger.error('Restore company failed', { error, id });
      throw error;
    }
  }

  /**
   * Get company users
   */
  async getCompanyUsers(companyId: string, options: {
    page?: number;
    limit?: number;
    search?: string;
    role?: string;
    status?: string;
  } = {}): Promise<{ users: User[]; total: number; page: number; limit: number }> {
    try {
      const {
        page = 1,
        limit = 10,
        search,
        role,
        status,
      } = options;

      const queryBuilder = this.userRepository
        .createQueryBuilder('user')
        .where('user.company_id = :companyId', { companyId })
        .andWhere('user.deleted_at IS NULL');

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
      logger.error('Get company users failed', { error, companyId, options });
      throw error;
    }
  }

  /**
   * Add user to company
   */
  async addUserToCompany(companyId: string, userId: string, addedBy?: string): Promise<void> {
    try {
      // Check if company exists
      const company = await this.getCompanyById(companyId);

      // Check if user exists
      const user = await this.userRepository.findOne({
        where: { id: userId },
      });

      if (!user) {
        throw new AppError('User not found', 404, 'USER_NOT_FOUND');
      }

      // Update user's company
      user.company_id = companyId;
      await this.userRepository.save(user);

      logger.info('User added to company successfully', {
        companyId,
        userId,
        addedBy,
      });
    } catch (error) {
      logger.error('Add user to company failed', { error, companyId, userId });
      throw error;
    }
  }

  /**
   * Remove user from company
   */
  async removeUserFromCompany(companyId: string, userId: string, removedBy?: string): Promise<void> {
    try {
      // Check if user exists and belongs to company
      const user = await this.userRepository.findOne({
        where: { id: userId, company_id: companyId },
      });

      if (!user) {
        throw new AppError('User not found in company', 404, 'USER_NOT_IN_COMPANY');
      }

      // Remove user from company
      user.company_id = null;
      await this.userRepository.save(user);

      logger.info('User removed from company successfully', {
        companyId,
        userId,
        removedBy,
      });
    } catch (error) {
      logger.error('Remove user from company failed', { error, companyId, userId });
      throw error;
    }
  }

  /**
   * Get company statistics
   */
  async getCompanyStats(companyId?: string): Promise<{
    total: number;
    active: number;
    inactive: number;
    byType: Record<string, number>;
    byStatus: Record<string, number>;
    userCount: number;
  }> {
    try {
      const queryBuilder = this.companyRepository
        .createQueryBuilder('company')
        .where('company.deleted_at IS NULL');

      if (companyId) {
        queryBuilder.andWhere('company.id = :companyId', { companyId });
      }

      const companies = await queryBuilder.getMany();

      const stats = {
        total: companies.length,
        active: companies.filter(c => c.isActive()).length,
        inactive: companies.filter(c => !c.isActive()).length,
        byType: {} as Record<string, number>,
        byStatus: {} as Record<string, number>,
        userCount: 0,
      };

      // Count by type and status
      companies.forEach(company => {
        stats.byType[company.type] = (stats.byType[company.type] || 0) + 1;
        stats.byStatus[company.status] = (stats.byStatus[company.status] || 0) + 1;
      });

      // Get user count
      if (companyId) {
        stats.userCount = await this.userRepository.count({
          where: { company_id: companyId },
        });
      } else {
        stats.userCount = await this.userRepository.count();
      }

      return stats;
    } catch (error) {
      logger.error('Get company stats failed', { error, companyId });
      throw error;
    }
  }

  /**
   * Check if company has feature enabled
   */
  async companyHasFeature(companyId: string, feature: string): Promise<boolean> {
    try {
      const company = await this.getCompanyById(companyId);
      return company.hasFeature(feature);
    } catch (error) {
      logger.error('Check company feature failed', { error, companyId, feature });
      throw error;
    }
  }

  /**
   * Check if company has module enabled
   */
  async companyHasModule(companyId: string, module: string): Promise<boolean> {
    try {
      const company = await this.getCompanyById(companyId);
      return company.hasModule(module);
    } catch (error) {
      logger.error('Check company module failed', { error, companyId, module });
      throw error;
    }
  }

  /**
   * Enable company feature
   */
  async enableCompanyFeature(companyId: string, feature: string, enabledBy?: string): Promise<void> {
    try {
      const company = await this.getCompanyById(companyId);
      
      if (!company.features) {
        company.features = {};
      }
      
      company.features[feature] = true;
      await this.companyRepository.save(company);

      logger.info('Company feature enabled', {
        companyId,
        feature,
        enabledBy,
      });
    } catch (error) {
      logger.error('Enable company feature failed', { error, companyId, feature });
      throw error;
    }
  }

  /**
   * Disable company feature
   */
  async disableCompanyFeature(companyId: string, feature: string, disabledBy?: string): Promise<void> {
    try {
      const company = await this.getCompanyById(companyId);
      
      if (!company.features) {
        company.features = {};
      }
      
      company.features[feature] = false;
      await this.companyRepository.save(company);

      logger.info('Company feature disabled', {
        companyId,
        feature,
        disabledBy,
      });
    } catch (error) {
      logger.error('Disable company feature failed', { error, companyId, feature });
      throw error;
    }
  }
}

export default CompanyService;