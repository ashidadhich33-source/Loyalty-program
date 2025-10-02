import { Entity, Column, OneToMany, Index } from 'typeorm';
import { BaseEntity } from './base.entity';
import { User } from './user.entity';
import { IsEmail, IsNotEmpty, IsOptional, IsBoolean, IsEnum } from 'class-validator';

/**
 * Company type enum
 */
export enum CompanyType {
  RETAIL = 'retail',
  WHOLESALE = 'wholesale',
  MANUFACTURING = 'manufacturing',
  SERVICE = 'service',
  ECOMMERCE = 'ecommerce',
  DISTRIBUTION = 'distribution',
}

/**
 * Company status enum
 */
export enum CompanyStatus {
  ACTIVE = 'active',
  INACTIVE = 'inactive',
  PENDING = 'pending',
  SUSPENDED = 'suspended',
  TRIAL = 'trial',
}

/**
 * Company entity
 * Represents companies in the multi-tenant system
 */
@Entity('companies')
@Index(['name'], { unique: true })
@Index(['email'], { unique: true })
export class Company extends BaseEntity {
  @Column({
    type: 'varchar',
    length: 255,
    unique: true,
  })
  @IsNotEmpty()
  name: string;

  @Column({
    type: 'varchar',
    length: 100,
    nullable: true,
  })
  @IsOptional()
  legal_name: string | null;

  @Column({
    type: 'varchar',
    length: 50,
    nullable: true,
  })
  @IsOptional()
  registration_number: string | null;

  @Column({
    type: 'varchar',
    length: 20,
    nullable: true,
  })
  @IsOptional()
  gstin: string | null;

  @Column({
    type: 'varchar',
    length: 20,
    nullable: true,
  })
  @IsOptional()
  pan: string | null;

  @Column({
    type: 'varchar',
    length: 20,
    nullable: true,
  })
  @IsOptional()
  tan: string | null;

  @Column({
    type: 'varchar',
    length: 20,
    nullable: true,
  })
  @IsOptional()
  cin: string | null;

  @Column({
    type: 'varchar',
    length: 255,
    nullable: true,
  })
  @IsOptional()
  website: string | null;

  @Column({
    type: 'varchar',
    length: 255,
    nullable: true,
  })
  @IsOptional()
  email: string | null;

  @Column({
    type: 'varchar',
    length: 20,
    nullable: true,
  })
  @IsOptional()
  phone: string | null;

  @Column({
    type: 'varchar',
    length: 20,
    nullable: true,
  })
  @IsOptional()
  mobile: string | null;

  @Column({
    type: 'text',
    nullable: true,
  })
  @IsOptional()
  address: string | null;

  @Column({
    type: 'varchar',
    length: 100,
    nullable: true,
  })
  @IsOptional()
  city: string | null;

  @Column({
    type: 'varchar',
    length: 100,
    nullable: true,
  })
  @IsOptional()
  state: string | null;

  @Column({
    type: 'varchar',
    length: 20,
    nullable: true,
  })
  @IsOptional()
  postal_code: string | null;

  @Column({
    type: 'varchar',
    length: 100,
    nullable: true,
  })
  @IsOptional()
  country: string | null;

  @Column({
    type: 'enum',
    enum: CompanyType,
    default: CompanyType.RETAIL,
  })
  @IsEnum(CompanyType)
  type: CompanyType;

  @Column({
    type: 'enum',
    enum: CompanyStatus,
    default: CompanyStatus.ACTIVE,
  })
  @IsEnum(CompanyStatus)
  status: CompanyStatus;

  @Column({
    type: 'varchar',
    length: 10,
    default: 'INR',
  })
  @IsOptional()
  currency: string;

  @Column({
    type: 'varchar',
    length: 10,
    default: 'en',
  })
  @IsOptional()
  language: string;

  @Column({
    type: 'varchar',
    length: 10,
    default: 'UTC',
  })
  @IsOptional()
  timezone: string;

  @Column({
    type: 'date',
    nullable: true,
  })
  @IsOptional()
  fiscal_year_start: Date | null;

  @Column({
    type: 'date',
    nullable: true,
  })
  @IsOptional()
  fiscal_year_end: Date | null;

  @Column({
    type: 'varchar',
    length: 255,
    nullable: true,
  })
  @IsOptional()
  logo: string | null;

  @Column({
    type: 'varchar',
    length: 255,
    nullable: true,
  })
  @IsOptional()
  banner: string | null;

  @Column({
    type: 'text',
    nullable: true,
  })
  @IsOptional()
  description: string | null;

  @Column({
    type: 'jsonb',
    nullable: true,
  })
  @IsOptional()
  settings: Record<string, any> | null;

  @Column({
    type: 'jsonb',
    nullable: true,
  })
  @IsOptional()
  features: Record<string, any> | null;

  @Column({
    type: 'jsonb',
    nullable: true,
  })
  @IsOptional()
  modules: Record<string, any> | null;

  @Column({
    type: 'boolean',
    default: false,
  })
  @IsBoolean()
  gst_enabled: boolean;

  @Column({
    type: 'boolean',
    default: false,
  })
  @IsBoolean()
  pos_enabled: boolean;

  @Column({
    type: 'boolean',
    default: false,
  })
  @IsBoolean()
  ecommerce_enabled: boolean;

  @Column({
    type: 'boolean',
    default: false,
  })
  @IsBoolean()
  multi_warehouse: boolean;

  @Column({
    type: 'boolean',
    default: false,
  })
  @IsBoolean()
  multi_company: boolean;

  @Column({
    type: 'timestamp',
    nullable: true,
  })
  @IsOptional()
  trial_ends_at: Date | null;

  @Column({
    type: 'timestamp',
    nullable: true,
  })
  @IsOptional()
  subscription_ends_at: Date | null;

  // Relationships
  @OneToMany(() => User, (user) => user.company)
  users: User[];

  /**
   * Get display name
   */
  getDisplayName(): string {
    return this.legal_name || this.name;
  }

  /**
   * Check if company is active
   */
  isActive(): boolean {
    return this.status === CompanyStatus.ACTIVE && this.active && !this.isDeleted();
  }

  /**
   * Check if company is in trial
   */
  isTrial(): boolean {
    return this.status === CompanyStatus.TRIAL && this.trial_ends_at && this.trial_ends_at > new Date();
  }

  /**
   * Check if company has subscription
   */
  hasSubscription(): boolean {
    return this.subscription_ends_at && this.subscription_ends_at > new Date();
  }

  /**
   * Check if company has feature enabled
   */
  hasFeature(feature: string): boolean {
    return this.features && this.features[feature] === true;
  }

  /**
   * Check if company has module enabled
   */
  hasModule(module: string): boolean {
    return this.modules && this.modules[module] === true;
  }

  /**
   * Get company address as string
   */
  getAddressString(): string {
    const parts = [
      this.address,
      this.city,
      this.state,
      this.postal_code,
      this.country,
    ].filter(Boolean);
    return parts.join(', ');
  }

  /**
   * Get fiscal year
   */
  getFiscalYear(): { start: Date; end: Date } | null {
    if (this.fiscal_year_start && this.fiscal_year_end) {
      return {
        start: this.fiscal_year_start,
        end: this.fiscal_year_end,
      };
    }
    return null;
  }

  /**
   * Check if company is in current fiscal year
   */
  isInCurrentFiscalYear(date: Date): boolean {
    const fiscalYear = this.getFiscalYear();
    if (!fiscalYear) return true;
    return date >= fiscalYear.start && date <= fiscalYear.end;
  }
}