#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - Database Manager
===================================

Database management for the standalone ERP system.
"""

import logging
import psycopg2
from psycopg2 import pool
from psycopg2.extras import RealDictCursor
from typing import Dict, List, Any, Optional
import json

class DatabaseManager:
    """Database Manager for ERP System"""
    
    def __init__(self, config):
        """Initialize database manager"""
        self.config = config
        self.connection_pool = None
        self.logger = logging.getLogger('ERP.Database')
        
    def initialize(self):
        """Initialize database connection pool"""
        try:
            # Get database configuration
            db_config = self.config.get('database')
            
            # Create connection pool
            self.connection_pool = psycopg2.pool.ThreadedConnectionPool(
                minconn=1,
                maxconn=db_config.get('pool_size', 20),
                host=db_config['host'],
                port=db_config['port'],
                user=db_config['user'],
                password=db_config['password'],
                database=db_config['name']
            )
            
            self.logger.info("Database connection pool initialized")
            
            # Test connection
            self._test_connection()
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to initialize database: {e}")
            return False
    
    def _test_connection(self):
        """Test database connection"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT 1")
            cursor.close()
            conn.close()
            self.logger.info("Database connection test successful")
        except Exception as e:
            self.logger.error(f"Database connection test failed: {e}")
            raise
    
    def get_connection(self):
        """Get database connection from pool"""
        if not self.connection_pool:
            raise Exception("Database connection pool not initialized")
        return self.connection_pool.getconn()
    
    def return_connection(self, conn):
        """Return connection to pool"""
        if self.connection_pool:
            self.connection_pool.putconn(conn)
    
    def execute_query(self, query: str, params: tuple = None) -> List[Dict]:
        """Execute SELECT query and return results"""
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute(query, params)
            results = cursor.fetchall()
            cursor.close()
            return [dict(row) for row in results]
        except Exception as e:
            self.logger.error(f"Query execution failed: {e}")
            raise
        finally:
            if conn:
                self.return_connection(conn)
    
    def execute_update(self, query: str, params: tuple = None) -> int:
        """Execute UPDATE/INSERT/DELETE query and return affected rows"""
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            affected_rows = cursor.rowcount
            cursor.close()
            return affected_rows
        except Exception as e:
            if conn:
                conn.rollback()
            self.logger.error(f"Update execution failed: {e}")
            raise
        finally:
            if conn:
                self.return_connection(conn)
    
    def create_table(self, table_name: str, columns: Dict[str, str]) -> bool:
        """Create table with specified columns"""
        try:
            column_definitions = []
            for col_name, col_type in columns.items():
                column_definitions.append(f"{col_name} {col_type}")
            
            query = f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(column_definitions)})"
            self.execute_update(query)
            self.logger.info(f"Table {table_name} created successfully")
            return True
        except Exception as e:
            self.logger.error(f"Failed to create table {table_name}: {e}")
            return False
    
    def drop_table(self, table_name: str) -> bool:
        """Drop table"""
        try:
            query = f"DROP TABLE IF EXISTS {table_name}"
            self.execute_update(query)
            self.logger.info(f"Table {table_name} dropped successfully")
            return True
        except Exception as e:
            self.logger.error(f"Failed to drop table {table_name}: {e}")
            return False
    
    def insert_record(self, table_name: str, data: Dict[str, Any]) -> int:
        """Insert record and return ID"""
        try:
            columns = list(data.keys())
            values = list(data.values())
            placeholders = ['%s'] * len(values)
            
            query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({', '.join(placeholders)}) RETURNING id"
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute(query, values)
            record_id = cursor.fetchone()[0]
            conn.commit()
            cursor.close()
            self.return_connection(conn)
            
            return record_id
        except Exception as e:
            self.logger.error(f"Failed to insert record: {e}")
            raise
    
    def update_record(self, table_name: str, record_id: int, data: Dict[str, Any]) -> bool:
        """Update record by ID"""
        try:
            set_clauses = []
            values = []
            for col, val in data.items():
                set_clauses.append(f"{col} = %s")
                values.append(val)
            
            values.append(record_id)
            query = f"UPDATE {table_name} SET {', '.join(set_clauses)} WHERE id = %s"
            affected_rows = self.execute_update(query, tuple(values))
            
            return affected_rows > 0
        except Exception as e:
            self.logger.error(f"Failed to update record: {e}")
            return False
    
    def delete_record(self, table_name: str, record_id: int) -> bool:
        """Delete record by ID"""
        try:
            query = f"DELETE FROM {table_name} WHERE id = %s"
            affected_rows = self.execute_update(query, (record_id,))
            return affected_rows > 0
        except Exception as e:
            self.logger.error(f"Failed to delete record: {e}")
            return False
    
    def get_record(self, table_name: str, record_id: int) -> Optional[Dict]:
        """Get record by ID"""
        try:
            query = f"SELECT * FROM {table_name} WHERE id = %s"
            results = self.execute_query(query, (record_id,))
            return results[0] if results else None
        except Exception as e:
            self.logger.error(f"Failed to get record: {e}")
            return None
    
    def search_records(self, table_name: str, filters: Dict[str, Any] = None, 
                      limit: int = None, offset: int = None) -> List[Dict]:
        """Search records with filters"""
        try:
            query = f"SELECT * FROM {table_name}"
            params = []
            
            if filters:
                where_clauses = []
                for col, val in filters.items():
                    where_clauses.append(f"{col} = %s")
                    params.append(val)
                query += f" WHERE {' AND '.join(where_clauses)}"
            
            if limit:
                query += f" LIMIT {limit}"
            if offset:
                query += f" OFFSET {offset}"
            
            return self.execute_query(query, tuple(params))
        except Exception as e:
            self.logger.error(f"Failed to search records: {e}")
            return []
    
    def close(self):
        """Close database connection pool"""
        if self.connection_pool:
            self.connection_pool.closeall()
            self.logger.info("Database connection pool closed")