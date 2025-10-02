import { DataSource } from 'typeorm';
import { config } from './environment';
import { logger } from './logger';

/**
 * Database configuration and connection
 * Uses TypeORM for database operations with PostgreSQL
 */
export const dataSource = new DataSource({
  type: 'postgres',
  host: config.database.host,
  port: config.database.port,
  username: config.database.user,
  password: config.database.password,
  database: config.database.name,
  ssl: config.database.ssl ? { rejectUnauthorized: false } : false,
  synchronize: config.database.synchronize,
  logging: config.database.logging,
  entities: [
    'src/entities/**/*.ts',
    'src/modules/**/entities/*.ts',
  ],
  migrations: [
    'src/migrations/**/*.ts',
  ],
  subscribers: [
    'src/subscribers/**/*.ts',
  ],
  cache: {
    type: 'redis',
    options: {
      host: config.redis.host,
      port: config.redis.port,
      password: config.redis.password,
    },
  },
  extra: {
    max: 20, // Maximum number of connections
    min: 5,  // Minimum number of connections
    acquire: 30000, // Maximum time to acquire connection
    idle: 10000,    // Maximum idle time
  },
});

/**
 * Connect to database
 */
export const connectDatabase = async (): Promise<void> => {
  try {
    if (!dataSource.isInitialized) {
      await dataSource.initialize();
      logger.info('✅ Database connected successfully');
      
      // Run migrations in production
      if (config.isProduction) {
        await dataSource.runMigrations();
        logger.info('✅ Database migrations completed');
      }
    }
  } catch (error) {
    logger.error('❌ Database connection failed:', error);
    throw error;
  }
};

/**
 * Disconnect from database
 */
export const disconnectDatabase = async (): Promise<void> => {
  try {
    if (dataSource.isInitialized) {
      await dataSource.destroy();
      logger.info('✅ Database disconnected successfully');
    }
  } catch (error) {
    logger.error('❌ Database disconnection failed:', error);
    throw error;
  }
};

/**
 * Get database connection
 */
export const getConnection = () => {
  if (!dataSource.isInitialized) {
    throw new Error('Database not initialized');
  }
  return dataSource;
};

/**
 * Health check for database
 */
export const checkDatabaseHealth = async (): Promise<boolean> => {
  try {
    if (!dataSource.isInitialized) {
      return false;
    }
    
    await dataSource.query('SELECT 1');
    return true;
  } catch (error) {
    logger.error('Database health check failed:', error);
    return false;
  }
};

export default dataSource;