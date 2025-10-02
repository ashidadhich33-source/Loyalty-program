import {
  PrimaryGeneratedColumn,
  CreateDateColumn,
  UpdateDateColumn,
  DeleteDateColumn,
  VersionColumn,
  Column,
  BeforeInsert,
  BeforeUpdate,
} from 'typeorm';
import { Exclude } from 'class-transformer';

/**
 * Base entity class
 * Provides common fields and functionality for all entities
 */
export abstract class BaseEntity {
  @PrimaryGeneratedColumn('uuid')
  id: string;

  @CreateDateColumn({
    type: 'timestamp',
    default: () => 'CURRENT_TIMESTAMP(6)',
  })
  created_at: Date;

  @UpdateDateColumn({
    type: 'timestamp',
    default: () => 'CURRENT_TIMESTAMP(6)',
    onUpdate: 'CURRENT_TIMESTAMP(6)',
  })
  updated_at: Date;

  @DeleteDateColumn({
    type: 'timestamp',
    nullable: true,
  })
  @Exclude()
  deleted_at: Date | null;

  @VersionColumn()
  version: number;

  @Column({
    type: 'boolean',
    default: true,
  })
  active: boolean;

  @Column({
    type: 'text',
    nullable: true,
  })
  notes: string | null;

  @Column({
    type: 'jsonb',
    nullable: true,
  })
  metadata: Record<string, any> | null;

  /**
   * Lifecycle hooks
   */
  @BeforeInsert()
  beforeInsert(): void {
    this.created_at = new Date();
    this.updated_at = new Date();
  }

  @BeforeUpdate()
  beforeUpdate(): void {
    this.updated_at = new Date();
  }

  /**
   * Soft delete
   */
  softDelete(): void {
    this.deleted_at = new Date();
    this.active = false;
  }

  /**
   * Restore from soft delete
   */
  restore(): void {
    this.deleted_at = null;
    this.active = true;
  }

  /**
   * Check if entity is deleted
   */
  isDeleted(): boolean {
    return this.deleted_at !== null;
  }

  /**
   * Get entity age in days
   */
  getAgeInDays(): number {
    const now = new Date();
    const diffTime = Math.abs(now.getTime() - this.created_at.getTime());
    return Math.ceil(diffTime / (1000 * 60 * 60 * 24));
  }
}