import dotenv from 'dotenv';
import { z } from 'zod';

// Load environment variables
dotenv.config();

/**
 * Environment configuration schema
 * Validates all required environment variables
 */
const envSchema = z.object({
  // Server configuration
  NODE_ENV: z.enum(['development', 'production', 'test']).default('development'),
  PORT: z.string().transform(Number).default('3000'),
  HOST: z.string().default('localhost'),
  
  // Database configuration
  DATABASE_URL: z.string().min(1, 'Database URL is required'),
  DATABASE_HOST: z.string().default('localhost'),
  DATABASE_PORT: z.string().transform(Number).default('5432'),
  DATABASE_NAME: z.string().min(1, 'Database name is required'),
  DATABASE_USER: z.string().min(1, 'Database user is required'),
  DATABASE_PASSWORD: z.string().min(1, 'Database password is required'),
  DATABASE_SSL: z.string().transform(val => val === 'true').default('false'),
  
  // Redis configuration
  REDIS_URL: z.string().optional(),
  REDIS_HOST: z.string().default('localhost'),
  REDIS_PORT: z.string().transform(Number).default('6379'),
  REDIS_PASSWORD: z.string().optional(),
  
  // JWT configuration
  JWT_SECRET: z.string().min(32, 'JWT secret must be at least 32 characters'),
  JWT_EXPIRES_IN: z.string().default('24h'),
  JWT_REFRESH_EXPIRES_IN: z.string().default('7d'),
  
  // CORS configuration
  CORS_ORIGINS: z.string().default('http://localhost:3000,http://localhost:3001'),
  
  // Logging configuration
  LOG_LEVEL: z.enum(['error', 'warn', 'info', 'debug']).default('info'),
  LOG_FILE: z.string().default('logs/erp.log'),
  
  // File upload configuration
  MAX_FILE_SIZE: z.string().transform(Number).default('10485760'), // 10MB
  UPLOAD_PATH: z.string().default('uploads'),
  
  // Email configuration
  SMTP_HOST: z.string().optional(),
  SMTP_PORT: z.string().transform(Number).optional(),
  SMTP_USER: z.string().optional(),
  SMTP_PASSWORD: z.string().optional(),
  SMTP_SECURE: z.string().transform(val => val === 'true').default('false'),
  
  // External services
  PAYMENT_GATEWAY_URL: z.string().optional(),
  PAYMENT_GATEWAY_KEY: z.string().optional(),
  PAYMENT_GATEWAY_SECRET: z.string().optional(),
  
  // Feature flags
  ENABLE_SWAGGER: z.string().transform(val => val === 'true').default('false'),
  ENABLE_METRICS: z.string().transform(val => val === 'true').default('false'),
  ENABLE_DEBUG: z.string().transform(val => val === 'true').default('false'),
});

/**
 * Parse and validate environment variables
 */
const parseEnv = () => {
  try {
    return envSchema.parse(process.env);
  } catch (error) {
    if (error instanceof z.ZodError) {
      const errorMessages = error.errors.map(
        err => `${err.path.join('.')}: ${err.message}`
      );
      throw new Error(`Environment validation failed:\n${errorMessages.join('\n')}`);
    }
    throw error;
  }
};

const env = parseEnv();

/**
 * Application configuration
 */
export const config = {
  // Server configuration
  nodeEnv: env.NODE_ENV,
  port: env.PORT,
  host: env.HOST,
  isDevelopment: env.NODE_ENV === 'development',
  isProduction: env.NODE_ENV === 'production',
  isTest: env.NODE_ENV === 'test',
  
  // Database configuration
  database: {
    url: env.DATABASE_URL,
    host: env.DATABASE_HOST,
    port: env.DATABASE_PORT,
    name: env.DATABASE_NAME,
    user: env.DATABASE_USER,
    password: env.DATABASE_PASSWORD,
    ssl: env.DATABASE_SSL,
    synchronize: env.NODE_ENV === 'development',
    logging: env.NODE_ENV === 'development',
  },
  
  // Redis configuration
  redis: {
    url: env.REDIS_URL,
    host: env.REDIS_HOST,
    port: env.REDIS_PORT,
    password: env.REDIS_PASSWORD,
  },
  
  // JWT configuration
  jwt: {
    secret: env.JWT_SECRET,
    expiresIn: env.JWT_EXPIRES_IN,
    refreshExpiresIn: env.JWT_REFRESH_EXPIRES_IN,
  },
  
  // CORS configuration
  corsOrigins: env.CORS_ORIGINS.split(',').map(origin => origin.trim()),
  
  // Logging configuration
  logLevel: env.LOG_LEVEL,
  logFile: env.LOG_FILE,
  
  // File upload configuration
  maxFileSize: env.MAX_FILE_SIZE,
  uploadPath: env.UPLOAD_PATH,
  
  // Email configuration
  email: {
    host: env.SMTP_HOST,
    port: env.SMTP_PORT,
    user: env.SMTP_USER,
    password: env.SMTP_PASSWORD,
    secure: env.SMTP_SECURE,
  },
  
  // External services
  paymentGateway: {
    url: env.PAYMENT_GATEWAY_URL,
    key: env.PAYMENT_GATEWAY_KEY,
    secret: env.PAYMENT_GATEWAY_SECRET,
  },
  
  // Feature flags
  features: {
    swagger: env.ENABLE_SWAGGER,
    metrics: env.ENABLE_METRICS,
    debug: env.ENABLE_DEBUG,
  },
  
  // Debug configuration
  debug: env.ENABLE_DEBUG,
} as const;

export default config;