import 'reflect-metadata';
import { config } from '@/config/environment';

/**
 * Test setup configuration
 * Runs before all tests to configure the test environment
 */

// Set test environment
process.env.NODE_ENV = 'test';

// Mock external dependencies
jest.mock('@/config/logger', () => ({
  logger: {
    info: jest.fn(),
    error: jest.fn(),
    warn: jest.fn(),
    debug: jest.fn(),
  },
}));

// Mock database connection
jest.mock('@/config/database', () => ({
  dataSource: {
    isInitialized: true,
    initialize: jest.fn().mockResolvedValue(undefined),
    destroy: jest.fn().mockResolvedValue(undefined),
    query: jest.fn().mockResolvedValue([]),
    getRepository: jest.fn(),
    createQueryBuilder: jest.fn(),
  },
  connectDatabase: jest.fn().mockResolvedValue(undefined),
  disconnectDatabase: jest.fn().mockResolvedValue(undefined),
  getConnection: jest.fn(),
  checkDatabaseHealth: jest.fn().mockResolvedValue(true),
}));

// Mock Redis connection
jest.mock('redis', () => ({
  createClient: jest.fn().mockReturnValue({
    connect: jest.fn().mockResolvedValue(undefined),
    disconnect: jest.fn().mockResolvedValue(undefined),
    get: jest.fn().mockResolvedValue(null),
    set: jest.fn().mockResolvedValue('OK'),
    del: jest.fn().mockResolvedValue(1),
    exists: jest.fn().mockResolvedValue(0),
    expire: jest.fn().mockResolvedValue(1),
  }),
}));

// Mock file system operations
jest.mock('fs', () => ({
  ...jest.requireActual('fs'),
  mkdirSync: jest.fn(),
  writeFileSync: jest.fn(),
  readFileSync: jest.fn(),
  existsSync: jest.fn().mockReturnValue(true),
}));

// Mock path operations
jest.mock('path', () => ({
  ...jest.requireActual('path'),
  join: jest.fn((...args) => args.join('/')),
  resolve: jest.fn((...args) => args.join('/')),
}));

// Global test timeout
jest.setTimeout(10000);

// Global test setup
beforeAll(async () => {
  // Setup test database
  // await setupTestDatabase();
});

// Global test teardown
afterAll(async () => {
  // Cleanup test database
  // await cleanupTestDatabase();
});

// Setup for each test
beforeEach(() => {
  // Clear all mocks
  jest.clearAllMocks();
});

// Teardown for each test
afterEach(() => {
  // Cleanup after each test
});

// Global error handler for tests
process.on('unhandledRejection', (reason, promise) => {
  console.error('Unhandled Rejection at:', promise, 'reason:', reason);
});

// Global exception handler for tests
process.on('uncaughtException', (error) => {
  console.error('Uncaught Exception:', error);
  process.exit(1);
});