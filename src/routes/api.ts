import { Router } from 'express';
import { logger } from '@/config/logger';
import { authRoutes } from './auth';
import { userRoutes } from './users';
import { companyRoutes } from './companies';

/**
 * API routes
 * Main API router for the ERP application
 */
const router = Router();

/**
 * API information endpoint
 * GET /api
 */
router.get('/', (req, res) => {
  res.json({
    message: 'ERP API',
    version: '1.0.0',
    status: 'running',
    timestamp: new Date().toISOString(),
    modules: [
      'core_base',
      'core_web',
      'users',
      'company',
      'database',
      'contacts',
      'products',
      'sales',
      'crm',
      'pos',
      'inventory',
      'purchase',
      'accounting',
      'l10n_in',
      'hr',
      'reports',
    ],
    endpoints: {
      health: '/health',
      modules: '/api/modules',
      users: '/api/users',
      companies: '/api/companies',
      contacts: '/api/contacts',
      products: '/api/products',
      sales: '/api/sales',
      crm: '/api/crm',
      pos: '/api/pos',
      inventory: '/api/inventory',
      purchase: '/api/purchase',
      accounting: '/api/accounting',
      hr: '/api/hr',
      reports: '/api/reports',
    },
  });
});

/**
 * Modules endpoint
 * GET /api/modules
 */
router.get('/modules', (req, res) => {
  res.json({
    message: 'Available modules',
    modules: [
      {
        name: 'core_base',
        display_name: 'Core Base',
        description: 'System configuration and utilities',
        version: '1.0.0',
        status: 'installed',
        dependencies: [],
      },
      {
        name: 'core_web',
        display_name: 'Core Web',
        description: 'Web client and UI assets',
        version: '1.0.0',
        status: 'installed',
        dependencies: ['core_base'],
      },
      {
        name: 'users',
        display_name: 'User Management',
        description: 'User management and permissions',
        version: '1.0.0',
        status: 'installed',
        dependencies: ['core_base', 'core_web'],
      },
      {
        name: 'company',
        display_name: 'Company Management',
        description: 'Company setup and multi-company support',
        version: '1.0.0',
        status: 'installed',
        dependencies: ['core_base', 'core_web', 'users'],
      },
      {
        name: 'database',
        display_name: 'Database Management',
        description: 'Multi-database management',
        version: '1.0.0',
        status: 'installed',
        dependencies: ['core_base', 'core_web', 'users', 'company'],
      },
      {
        name: 'contacts',
        display_name: 'Contacts',
        description: 'Customer and supplier management',
        version: '1.0.0',
        status: 'available',
        dependencies: ['core_base', 'core_web', 'users', 'company'],
      },
      {
        name: 'products',
        display_name: 'Products',
        description: 'Product catalog with variants',
        version: '1.0.0',
        status: 'available',
        dependencies: ['core_base', 'core_web', 'users', 'company'],
      },
      {
        name: 'sales',
        display_name: 'Sales',
        description: 'Sales orders and quotations',
        version: '1.0.0',
        status: 'available',
        dependencies: ['contacts', 'products'],
      },
      {
        name: 'crm',
        display_name: 'CRM',
        description: 'Lead management and opportunities',
        version: '1.0.0',
        status: 'available',
        dependencies: ['contacts', 'sales'],
      },
      {
        name: 'pos',
        display_name: 'Point of Sale',
        description: 'Point of sale system',
        version: '1.0.0',
        status: 'available',
        dependencies: ['contacts', 'products', 'sales', 'inventory'],
      },
      {
        name: 'inventory',
        display_name: 'Inventory',
        description: 'Stock management and transfers',
        version: '1.0.0',
        status: 'available',
        dependencies: ['products', 'contacts'],
      },
      {
        name: 'purchase',
        display_name: 'Purchase',
        description: 'Procurement and vendor management',
        version: '1.0.0',
        status: 'available',
        dependencies: ['contacts', 'products', 'inventory'],
      },
      {
        name: 'accounting',
        display_name: 'Accounting',
        description: 'Financial management and invoicing',
        version: '1.0.0',
        status: 'available',
        dependencies: ['sales', 'purchase', 'contacts'],
      },
      {
        name: 'l10n_in',
        display_name: 'Indian Localization',
        description: 'Indian localization and compliance',
        version: '1.0.0',
        status: 'available',
        dependencies: ['accounting'],
      },
      {
        name: 'hr',
        display_name: 'Human Resources',
        description: 'Human resources and payroll',
        version: '1.0.0',
        status: 'available',
        dependencies: ['users', 'company'],
      },
      {
        name: 'reports',
        display_name: 'Reports',
        description: 'Custom reporting system',
        version: '1.0.0',
        status: 'available',
        dependencies: ['sales', 'inventory', 'purchase', 'accounting'],
      },
    ],
  });
});

/**
 * Module installation endpoint
 * POST /api/modules/install
 */
router.post('/modules/install', (req, res) => {
  const { moduleName } = req.body;
  
  if (!moduleName) {
    return res.status(400).json({
      error: 'Module name is required',
      message: 'Please provide a module name to install',
    });
  }

  logger.info('Module installation requested', {
    moduleName,
    timestamp: new Date().toISOString(),
  });

  // TODO: Implement actual module installation
  res.json({
    message: 'Module installation initiated',
    moduleName,
    status: 'pending',
    timestamp: new Date().toISOString(),
  });
});

/**
 * Module uninstallation endpoint
 * DELETE /api/modules/:moduleName
 */
router.delete('/modules/:moduleName', (req, res) => {
  const { moduleName } = req.params;
  
  logger.info('Module uninstallation requested', {
    moduleName,
    timestamp: new Date().toISOString(),
  });

  // TODO: Implement actual module uninstallation
  res.json({
    message: 'Module uninstallation initiated',
    moduleName,
    status: 'pending',
    timestamp: new Date().toISOString(),
  });
});

// Authentication routes
router.use('/auth', authRoutes);

// User management routes
router.use('/users', userRoutes);

// Company management routes
router.use('/companies', companyRoutes);

export { router as apiRoutes };