# Odoo-Style ERP System

A comprehensive ERP system designed specifically for the Kids' Clothing Retail Industry, built with modern web technologies and following Odoo's modular architecture principles.

## 🚀 Features

### Core Modules
- **Authentication & Authorization**: JWT-based auth with role-based access control
- **User Management**: Complete user lifecycle with groups and permissions
- **Company Management**: Multi-tenant architecture with company-specific settings
- **Dashboard**: Real-time analytics and business insights

### Business Modules (Planned)
- **Contacts**: Customer and supplier management
- **Products**: Product catalog with variants and categories
- **Sales**: Sales orders, quotations, and CRM
- **POS**: Point of sale system for retail operations
- **Inventory**: Stock management and warehouse operations
- **Purchase**: Procurement and supplier management
- **Accounting**: Financial management and reporting
- **HR**: Human resources and employee management
- **Reports**: Custom reporting and analytics

### Technical Features
- **Modular Architecture**: Install/uninstall modules like Odoo
- **Multi-tenancy**: Company-based data isolation
- **API-First Design**: RESTful APIs with comprehensive documentation
- **Real-time Updates**: WebSocket support for live data
- **Mobile Responsive**: Works on all devices
- **Internationalization**: Multi-language support
- **Customization**: Theme and module customization

## 🏗️ Architecture

### Backend (Node.js/TypeScript)
- **Express.js**: Web framework
- **TypeORM**: Database ORM with PostgreSQL
- **JWT**: Authentication and authorization
- **Winston**: Logging
- **Jest**: Testing framework
- **Playwright**: E2E testing

### Frontend (React/TypeScript)
- **React 18**: UI framework
- **Vite**: Build tool and dev server
- **Tailwind CSS**: Utility-first CSS framework
- **React Query**: Data fetching and caching
- **Zustand**: State management
- **React Router**: Client-side routing

## 📦 Installation

### Prerequisites
- Node.js 18+ 
- PostgreSQL 14+
- npm 8+

### Quick Start

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd odoo-style-erp
   ```

2. **Install dependencies**
   ```bash
   npm run setup
   ```

3. **Environment setup**
   ```bash
   cp .env.example .env
   # Edit .env with your database and other configurations
   ```

4. **Database setup**
   ```bash
   # Create PostgreSQL database
   createdb erp_system
   
   # Run migrations (when available)
   npm run migrate
   ```

5. **Start development servers**
   ```bash
   npm run dev
   ```

This will start:
- Backend API server on `http://localhost:3000`
- Frontend development server on `http://localhost:3001`

## 🛠️ Development

### Available Scripts

#### Full Stack
- `npm run dev` - Start both backend and frontend
- `npm run build` - Build both backend and frontend
- `npm run test` - Run all tests
- `npm run lint` - Lint all code
- `npm run format` - Format all code

#### Backend Only
- `npm run dev:backend` - Start backend server
- `npm run build:backend` - Build backend
- `npm run test:backend` - Run backend tests
- `npm run lint:backend` - Lint backend code

#### Frontend Only
- `npm run dev:frontend` - Start frontend server
- `npm run build:frontend` - Build frontend
- `npm run test:frontend` - Run frontend tests
- `npm run lint:frontend` - Lint frontend code

### Project Structure

```
├── src/                    # Backend source code
│   ├── entities/          # Database entities
│   ├── services/          # Business logic
│   ├── controllers/       # HTTP controllers
│   ├── routes/           # API routes
│   ├── middleware/       # Express middleware
│   ├── config/          # Configuration
│   └── tests/           # Backend tests
├── frontend/             # Frontend source code
│   ├── src/
│   │   ├── components/   # React components
│   │   ├── pages/        # Page components
│   │   ├── services/     # API services
│   │   ├── stores/       # State management
│   │   └── utils/        # Utility functions
│   └── public/          # Static assets
├── docs/                 # Documentation
└── scripts/             # Utility scripts
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the root directory:

```env
# Server
NODE_ENV=development
PORT=3000
DEBUG=true

# Database
DB_HOST=localhost
DB_PORT=5432
DB_NAME=erp_system
DB_USER=postgres
DB_PASSWORD=password

# JWT
JWT_SECRET=your-secret-key
JWT_EXPIRES_IN=24h
JWT_REFRESH_EXPIRES_IN=7d

# Email
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASS=your-password

# File Upload
MAX_FILE_SIZE=10485760
UPLOAD_PATH=uploads

# Logging
LOG_LEVEL=info
LOG_FILE=logs/app.log
```

## 🧪 Testing

### Backend Tests
```bash
npm run test:backend
npm run test:coverage
```

### Frontend Tests
```bash
npm run test:frontend
```

### E2E Tests
```bash
npm run test:e2e
```

## 📚 API Documentation

The API documentation is available at:
- **Development**: `http://localhost:3000/api-docs`
- **Documentation**: `src/docs/api-documentation.md`

### Key Endpoints

#### Authentication
- `POST /api/auth/login` - User login
- `POST /api/auth/register` - User registration
- `POST /api/auth/logout` - User logout
- `GET /api/auth/profile` - Get user profile

#### Users
- `GET /api/users` - List users
- `POST /api/users` - Create user
- `GET /api/users/:id` - Get user
- `PUT /api/users/:id` - Update user
- `DELETE /api/users/:id` - Delete user

#### Companies
- `GET /api/companies` - List companies
- `POST /api/companies` - Create company
- `GET /api/companies/:id` - Get company
- `PUT /api/companies/:id` - Update company
- `DELETE /api/companies/:id` - Delete company

## 🚀 Deployment

### Production Build
```bash
npm run build
```

### Docker Deployment
```bash
# Build Docker image
docker build -t erp-system .

# Run with Docker Compose
docker-compose up -d
```

### Environment Setup
1. Set `NODE_ENV=production`
2. Configure production database
3. Set up SSL certificates
4. Configure reverse proxy (nginx)
5. Set up monitoring and logging

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

### Development Guidelines
- Follow TypeScript best practices
- Write comprehensive tests
- Use conventional commits
- Follow the existing code style
- Update documentation

## 📄 License

This project is licensed under the LGPL-3.0 License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

For support and questions:
- **Documentation**: Check the `docs/` directory
- **Issues**: Create an issue on GitHub
- **Email**: support@erpcompany.com

## 🗺️ Roadmap

### Phase 1: Core System ✅
- [x] Authentication & Authorization
- [x] User Management
- [x] Company Management
- [x] Basic Dashboard

### Phase 2: Business Modules (In Progress)
- [ ] Contacts Module
- [ ] Products Module
- [ ] Sales Module
- [ ] POS Module
- [ ] Inventory Module

### Phase 3: Advanced Features
- [ ] Purchase Module
- [ ] Accounting Module
- [ ] HR Module
- [ ] Reports Module
- [ ] Mobile App

### Phase 4: Enterprise Features
- [ ] Advanced Analytics
- [ ] AI/ML Integration
- [ ] Third-party Integrations
- [ ] Advanced Customization
- [ ] Multi-currency Support

---

**Built with ❤️ for the Kids' Clothing Retail Industry**