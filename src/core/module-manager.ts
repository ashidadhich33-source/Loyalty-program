import { logger } from '@/config/logger';

/**
 * Module information interface
 */
export interface ModuleInfo {
  name: string;
  display_name: string;
  description: string;
  version: string;
  author: string;
  website: string;
  license: string;
  category: string;
  dependencies: string[];
  auto_install: boolean;
  installable: boolean;
  application: boolean;
  summary: string;
  icon: string;
  images: string[];
  price: number;
  currency: string;
}

/**
 * Module state enum
 */
export enum ModuleState {
  UNINSTALLED = 'uninstalled',
  INSTALLED = 'installed',
  TO_UPGRADE = 'to_upgrade',
  TO_INSTALL = 'to_install',
  TO_UNINSTALL = 'to_uninstall',
  UPGRADED = 'upgraded',
}

/**
 * Module operations interface
 */
export interface ModuleOperations {
  install(moduleName: string): Promise<void>;
  uninstall(moduleName: string): Promise<void>;
  upgrade(moduleName: string): Promise<void>;
  update(moduleName: string): Promise<void>;
  checkDependencies(moduleName: string): Promise<string[]>;
  resolveConflicts(modules: string[]): Promise<any[]>;
}

/**
 * Module Manager Class
 * Manages module installation, uninstallation, and dependencies
 */
export class ModuleManager implements ModuleOperations {
  private modules: Map<string, ModuleInfo> = new Map();
  private moduleStates: Map<string, ModuleState> = new Map();

  constructor() {
    this.initializeCoreModules();
  }

  /**
   * Initialize core modules
   */
  private initializeCoreModules(): void {
    const coreModules: ModuleInfo[] = [
      {
        name: 'core_base',
        display_name: 'Core Base',
        description: 'System configuration, utilities, translations, activation toggles',
        version: '1.0.0',
        author: 'ERP Development Team',
        website: 'https://erpcompany.com',
        license: 'LGPL-3',
        category: 'Core',
        dependencies: [],
        auto_install: true,
        installable: true,
        application: false,
        summary: 'System foundation and utilities',
        icon: 'base',
        images: [],
        price: 0,
        currency: 'USD',
      },
      {
        name: 'core_web',
        display_name: 'Core Web',
        description: 'Web client, UI assets, menus, notifications',
        version: '1.0.0',
        author: 'ERP Development Team',
        website: 'https://erpcompany.com',
        license: 'LGPL-3',
        category: 'Core',
        dependencies: ['core_base'],
        auto_install: true,
        installable: true,
        application: false,
        summary: 'Web client and UI framework',
        icon: 'web',
        images: [],
        price: 0,
        currency: 'USD',
      },
      {
        name: 'users',
        display_name: 'User Management',
        description: 'User, Group, Permission matrix, access rights, onboarding wizard',
        version: '1.0.0',
        author: 'ERP Development Team',
        website: 'https://erpcompany.com',
        license: 'LGPL-3',
        category: 'Core',
        dependencies: ['core_base', 'core_web'],
        auto_install: true,
        installable: true,
        application: false,
        summary: 'User management and permissions',
        icon: 'users',
        images: [],
        price: 0,
        currency: 'USD',
      },
      {
        name: 'company',
        display_name: 'Company Management',
        description: 'Company creation, profile, multi-company support, logo, fiscal year, address, GSTIN',
        version: '1.0.0',
        author: 'ERP Development Team',
        website: 'https://erpcompany.com',
        license: 'LGPL-3',
        category: 'Core',
        dependencies: ['core_base', 'core_web', 'users'],
        auto_install: true,
        installable: true,
        application: false,
        summary: 'Company setup and multi-company support',
        icon: 'company',
        images: [],
        price: 0,
        currency: 'USD',
      },
      {
        name: 'database',
        display_name: 'Database Management',
        description: 'Multi-database, database creation and switching',
        version: '1.0.0',
        author: 'ERP Development Team',
        website: 'https://erpcompany.com',
        license: 'LGPL-3',
        category: 'Core',
        dependencies: ['core_base', 'core_web', 'users', 'company'],
        auto_install: true,
        installable: true,
        application: false,
        summary: 'Multi-database management',
        icon: 'database',
        images: [],
        price: 0,
        currency: 'USD',
      },
    ];

    // Initialize core modules
    coreModules.forEach(module => {
      this.modules.set(module.name, module);
      this.moduleStates.set(module.name, ModuleState.INSTALLED);
    });

    logger.info('Core modules initialized', {
      modules: coreModules.map(m => m.name),
    });
  }

  /**
   * Install a module
   */
  public async install(moduleName: string): Promise<void> {
    try {
      logger.info('Installing module', { moduleName });

      // Check if module exists
      const module = this.modules.get(moduleName);
      if (!module) {
        throw new Error(`Module ${moduleName} not found`);
      }

      // Check dependencies
      const dependencies = await this.checkDependencies(moduleName);
      for (const dep of dependencies) {
        if (this.moduleStates.get(dep) !== ModuleState.INSTALLED) {
          throw new Error(`Dependency ${dep} not installed`);
        }
      }

      // Install module
      this.moduleStates.set(moduleName, ModuleState.INSTALLED);
      
      logger.info('Module installed successfully', { moduleName });
    } catch (error) {
      logger.error('Module installation failed', { moduleName, error });
      throw error;
    }
  }

  /**
   * Uninstall a module
   */
  public async uninstall(moduleName: string): Promise<void> {
    try {
      logger.info('Uninstalling module', { moduleName });

      // Check if module is installed
      if (this.moduleStates.get(moduleName) !== ModuleState.INSTALLED) {
        throw new Error(`Module ${moduleName} not installed`);
      }

      // Check if other modules depend on this module
      const dependents = this.getDependents(moduleName);
      if (dependents.length > 0) {
        throw new Error(`Cannot uninstall ${moduleName}. Other modules depend on it: ${dependents.join(', ')}`);
      }

      // Uninstall module
      this.moduleStates.set(moduleName, ModuleState.UNINSTALLED);
      
      logger.info('Module uninstalled successfully', { moduleName });
    } catch (error) {
      logger.error('Module uninstallation failed', { moduleName, error });
      throw error;
    }
  }

  /**
   * Upgrade a module
   */
  public async upgrade(moduleName: string): Promise<void> {
    try {
      logger.info('Upgrading module', { moduleName });

      // Check if module is installed
      if (this.moduleStates.get(moduleName) !== ModuleState.INSTALLED) {
        throw new Error(`Module ${moduleName} not installed`);
      }

      // Upgrade module
      this.moduleStates.set(moduleName, ModuleState.UPGRADED);
      
      logger.info('Module upgraded successfully', { moduleName });
    } catch (error) {
      logger.error('Module upgrade failed', { moduleName, error });
      throw error;
    }
  }

  /**
   * Update a module
   */
  public async update(moduleName: string): Promise<void> {
    try {
      logger.info('Updating module', { moduleName });

      // Check if module is installed
      if (this.moduleStates.get(moduleName) !== ModuleState.INSTALLED) {
        throw new Error(`Module ${moduleName} not installed`);
      }

      // Update module
      this.moduleStates.set(moduleName, ModuleState.INSTALLED);
      
      logger.info('Module updated successfully', { moduleName });
    } catch (error) {
      logger.error('Module update failed', { moduleName, error });
      throw error;
    }
  }

  /**
   * Check module dependencies
   */
  public async checkDependencies(moduleName: string): Promise<string[]> {
    const module = this.modules.get(moduleName);
    if (!module) {
      throw new Error(`Module ${moduleName} not found`);
    }
    return module.dependencies;
  }

  /**
   * Resolve module conflicts
   */
  public async resolveConflicts(modules: string[]): Promise<any[]> {
    const conflicts: any[] = [];
    
    for (const moduleName of modules) {
      const module = this.modules.get(moduleName);
      if (!module) continue;

      // Check for dependency conflicts
      for (const dep of module.dependencies) {
        if (!this.modules.has(dep)) {
          conflicts.push({
            type: 'missing_dependency',
            module: moduleName,
            dependency: dep,
            message: `Module ${moduleName} requires ${dep} which is not available`,
          });
        }
      }
    }

    return conflicts;
  }

  /**
   * Get modules that depend on a module
   */
  private getDependents(moduleName: string): string[] {
    const dependents: string[] = [];
    
    for (const [name, module] of this.modules) {
      if (module.dependencies.includes(moduleName)) {
        dependents.push(name);
      }
    }
    
    return dependents;
  }

  /**
   * Get all modules
   */
  public getModules(): ModuleInfo[] {
    return Array.from(this.modules.values());
  }

  /**
   * Get module by name
   */
  public getModule(moduleName: string): ModuleInfo | undefined {
    return this.modules.get(moduleName);
  }

  /**
   * Get module state
   */
  public getModuleState(moduleName: string): ModuleState | undefined {
    return this.moduleStates.get(moduleName);
  }

  /**
   * Get installed modules
   */
  public getInstalledModules(): ModuleInfo[] {
    return this.getModules().filter(module => 
      this.moduleStates.get(module.name) === ModuleState.INSTALLED
    );
  }
}

/**
 * Initialize modules
 */
export const initializeModules = async (): Promise<void> => {
  try {
    const moduleManager = new ModuleManager();
    logger.info('Modules initialized successfully', {
      totalModules: moduleManager.getModules().length,
      installedModules: moduleManager.getInstalledModules().length,
    });
  } catch (error) {
    logger.error('Module initialization failed:', error);
    throw error;
  }
};

export default ModuleManager;