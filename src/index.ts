import 'reflect-metadata';
import { createServer } from 'http';
import { config } from '@/config/environment';
import { logger } from '@/config/logger';
import { app } from '@/app';
import { connectDatabase } from '@/config/database';
import { initializeModules } from '@/core/module-manager';

/**
 * ERP Server Entry Point
 * Odoo-Style ERP for Kids' Clothing Retail Industry
 */
class ERPServer {
  private server: any;
  private readonly port: number;

  constructor() {
    this.port = config.port || 3000;
  }

  /**
   * Initialize the ERP server
   */
  public async initialize(): Promise<void> {
    try {
      logger.info('🚀 Starting ERP Server...');

      // Connect to database
      await connectDatabase();
      logger.info('✅ Database connected successfully');

      // Initialize modules
      await initializeModules();
      logger.info('✅ Modules initialized successfully');

      // Create HTTP server
      this.server = createServer(app);

      // Start server
      this.server.listen(this.port, () => {
        logger.info(`🎉 ERP Server running on port ${this.port}`);
        logger.info(`📊 Environment: ${config.nodeEnv}`);
        logger.info(`🔧 Debug mode: ${config.debug}`);
        logger.info(`📝 Log level: ${config.logLevel}`);
      });

      // Graceful shutdown
      this.setupGracefulShutdown();

    } catch (error) {
      logger.error('❌ Failed to start ERP server:', error);
      process.exit(1);
    }
  }

  /**
   * Setup graceful shutdown handlers
   */
  private setupGracefulShutdown(): void {
    const shutdown = async (signal: string) => {
      logger.info(`🛑 Received ${signal}. Starting graceful shutdown...`);

      if (this.server) {
        this.server.close(() => {
          logger.info('✅ HTTP server closed');
          process.exit(0);
        });
      } else {
        process.exit(0);
      }
    };

    process.on('SIGTERM', () => shutdown('SIGTERM'));
    process.on('SIGINT', () => shutdown('SIGINT'));
    process.on('SIGUSR2', () => shutdown('SIGUSR2')); // For nodemon
  }
}

// Start the server
const erpServer = new ERPServer();
erpServer.initialize().catch((error) => {
  logger.error('❌ Failed to initialize ERP server:', error);
  process.exit(1);
});

export default ERPServer;