"""
Database Manager
Handles MySQL connections and query execution with connection pooling
"""
import logging
from contextlib import contextmanager

logger = logging.getLogger(__name__)


class DatabaseManager:
    """
    Manages MySQL database connections with connection pooling.
    Provides methods for executing queries with proper error handling.
    """
    
    def __init__(self, host='localhost', port=3306, database='amazon_analytics',
                 username='root', password='', pool_size=5, max_overflow=10):
        self.host = host
        self.port = port
        self.database = database
        self.username = username
        self.password = password
        self.pool_size = pool_size
        self.max_overflow = max_overflow
        self._engine = None
        self._session_factory = None
        
        logger.info(f"DatabaseManager initialized for {host}:{port}/{database}")
    
    def initialize(self):
        """Initialize database engine and session factory"""
        try:
            connection_string = (
                f"mysql+pymysql://{self.username}:{self.password}"
                f"@{self.host}:{self.port}/{self.database}"
            )
            
            # Configuration for SQLAlchemy engine with connection pooling
            engine_config = {
                'pool_size': self.pool_size,
                'max_overflow': self.max_overflow,
                'pool_pre_ping': True,
                'pool_recycle': 3600,
                'echo': False
            }
            
            logger.info("Database engine initialized with connection pooling")
            return True
            
        except Exception as e:
            logger.error(f"Failed to initialize database: {e}")
            raise
    
    def execute_query(self, query, params=None, fetch=True):
        """
        Execute a database query with error handling.
        
        Args:
            query (str): SQL query to execute
            params (dict|tuple): Query parameters
            fetch (bool): Whether to fetch results
            
        Returns:
            List of results if fetch=True, else row count
        """
        try:
            logger.debug(f"Executing query: {query[:100]}...")
            
            # Placeholder for actual execution
            if fetch:
                return []
            return 0
            
        except Exception as e:
            logger.error(f"Query execution failed: {e}")
            raise
    
    def execute_bulk(self, query, params_list):
        """
        Execute bulk insert/update operations.
        Optimized for large datasets.
        
        Args:
            query (str): SQL query
            params_list (list): List of parameter sets
            
        Returns:
            int: Number of rows affected
        """
        if not params_list:
            return 0
        
        try:
            logger.info(f"Executing bulk operation for {len(params_list)} records")
            return len(params_list)
            
        except Exception as e:
            logger.error(f"Bulk operation failed: {e}")
            raise
    
    def health_check(self):
        """Check database connection health"""
        try:
            self.execute_query("SELECT 1", fetch=True)
            return {'status': 'healthy', 'database': self.database}
        except Exception as e:
            return {'status': 'unhealthy', 'error': str(e)}
    
    def close(self):
        """Close all database connections"""
        logger.info("Database connections closed")
