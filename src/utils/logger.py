#!/usr/bin/env python3
# filepath: workspace/src/utils/logger.py
"""
Logger Module

This module provides a configurable logging utility for UAV applications.
It supports both console and file logging with customizable formatting and log levels.
"""

import logging
import logging.handlers
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

# Default log format
DEFAULT_LOG_FORMAT = "[{asctime}] - {levelname:<8} - {message}"

# Log levels dictionary for easy reference
LOG_LEVELS = {
    "debug": logging.DEBUG,
    "info": logging.INFO,
    "warning": logging.WARNING,
    "error": logging.ERROR,
    "critical": logging.CRITICAL
}


class Logger:
    """
    Configurable logger for UAV applications.
    
    This class provides logging functionality with support for both
    console and file output, with customizable formatting and log levels.
    """
    
    def __init__(
        self,
        name: str = "UAV-logger",
        log_dir: Optional[str] = None,
        log_file: Optional[str] = None,
        console_level: str = "info",
        file_level: str = "debug",
        log_format: str = DEFAULT_LOG_FORMAT,
        date_format: str = "%Y-%m-%d %H:%M:%S",
        backup_count: int = 5,
        max_file_size_mb: int = 10,
        enable_console: bool = True,
        enable_file: bool = True
    ) -> None:
        """
        Initialize the logger with customizable settings.
        
        Args:
            name: Logger name for identification
            log_dir: Directory to store log files (default: logs in current directory)
            log_file: Log file name (default: uav_app_YYYY-MM-DD.log)
            console_level: Minimum log level for console output
            file_level: Minimum log level for file output
            log_format: Format string for log messages
            date_format: Format string for timestamp
            backup_count: Number of backup logs to keep
            max_file_size_mb: Maximum size of log file in MB before rotation
            enable_console: Whether to enable console logging
            enable_file: Whether to enable file logging
        """
        # Set up logger instance
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)  # Capture all levels
        self.logger.propagate = False  # Don't propagate to root logger
        
        # Clear any existing handlers (in case of reinitialization)
        if self.logger.handlers:
            self.logger.handlers.clear()
        
        # Create formatter
        self.formatter = logging.Formatter(
            fmt=log_format,
            style="{",
            datefmt=date_format
        )
        
        # Set up console handler if enabled
        self.console_handler = None
        if enable_console:
            self.console_handler = logging.StreamHandler(stream=sys.stdout)
            self.console_handler.setLevel(LOG_LEVELS.get(console_level.lower(), logging.INFO))
            self.console_handler.setFormatter(self.formatter)
            self.logger.addHandler(self.console_handler)
        
        # Set up file handler if enabled
        self.file_handler = None
        if enable_file:
            # Set up log directory
            if log_dir is None:
                log_dir = os.path.join(os.getcwd(), "logs")
            
            # Create directory if it doesn't exist
            os.makedirs(log_dir, exist_ok=True)
            
            # Set default log filename if not provided
            if log_file is None:
                date_str = datetime.now().strftime("%Y-%m-%d")
                log_file = f"uav_app_{date_str}.log"
            
            # Full path to log file
            log_path = os.path.join(log_dir, log_file)
            
            # Set up rotating file handler
            self.file_handler = logging.handlers.RotatingFileHandler(
                filename=log_path,
                mode="a",  # Append mode to preserve logs across restarts
                maxBytes=max_file_size_mb * 1024 * 1024,
                backupCount=backup_count,
                encoding="utf-8"
            )
            self.file_handler.setLevel(LOG_LEVELS.get(file_level.lower(), logging.DEBUG))
            self.file_handler.setFormatter(self.formatter)
            self.logger.addHandler(self.file_handler)
    
    def log(
        self, 
        message: str, 
        level: str = "info", 
        exc_info: bool = None
    ) -> None:
        """
        Log a message with the specified level.
        
        Args:
            message: Log message content
            level: Log level (debug, info, warning, error, critical)
            exc_info: Whether to include exception info (default: True for error/critical)
        """
        level = level.lower()
        
        # Set default exc_info based on level if not explicitly provided
        if exc_info is None:
            exc_info = level in ("error", "critical")
        
        # Call appropriate logger method
        if level == "info":
            self.logger.info(message, exc_info=exc_info)
        elif level == "warning":
            self.logger.warning(message, exc_info=exc_info)
        elif level == "error":
            self.logger.error(message, exc_info=exc_info)
        elif level == "critical":
            self.logger.critical(message, exc_info=exc_info)
        else:  # Default to debug
            self.logger.debug(message, exc_info=exc_info)
    
    def debug(self, message: str, exc_info: bool = False) -> None:
        """Log a debug message."""
        self.logger.debug(message, exc_info=exc_info)
    
    def info(self, message: str, exc_info: bool = False) -> None:
        """Log an info message."""
        self.logger.info(message, exc_info=exc_info)
    
    def warning(self, message: str, exc_info: bool = False) -> None:
        """Log a warning message."""
        self.logger.warning(message, exc_info=exc_info)
    
    def error(self, message: str, exc_info: bool = True) -> None:
        """Log an error message with exception info."""
        self.logger.error(message, exc_info=exc_info)
    
    def critical(self, message: str, exc_info: bool = True) -> None:
        """Log a critical message with exception info."""
        self.logger.critical(message, exc_info=exc_info)
    
    def set_level(self, level: str, handler_type: str = "all") -> None:
        """
        Set the logging level for handlers.
        
        Args:
            level: Log level (debug, info, warning, error, critical)
            handler_type: Handler to adjust ('console', 'file', or 'all')
        """
        log_level = LOG_LEVELS.get(level.lower(), logging.INFO)
        
        if handler_type.lower() in ("all", "console") and self.console_handler:
            self.console_handler.setLevel(log_level)
            
        if handler_type.lower() in ("all", "file") and self.file_handler:
            self.file_handler.setLevel(log_level)
    
    def get_log_path(self) -> Optional[str]:
        """
        Get the path to the current log file.
        
        Returns:
            Path to the log file or None if file logging is disabled
        """
        if self.file_handler:
            return self.file_handler.baseFilename
        return None


# Singleton logger instance for global use
_logger_instance = None


def get_logger(
    name: str = "UAV-logger",
    **kwargs: Any
) -> Logger:
    """
    Get or create a singleton logger instance.
    
    This function creates a logger instance if it doesn't exist yet,
    or returns the existing instance.
    
    Args:
        name: Logger name
        **kwargs: Additional arguments to pass to Logger constructor
        
    Returns:
        Logger instance
    """
    global _logger_instance
    
    if _logger_instance is None:
        _logger_instance = Logger(name=name, **kwargs)
        
    return _logger_instance


if __name__ == "__main__":
    # Example usage
    logger = get_logger(
        log_dir="logs",
        console_level="debug"
    )
    
    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    
    try:
        # Simulate an error
        x = 1 / 0
    except Exception as e:
        logger.error(f"Error occurred: {e}")
    
    logger.critical("This is a critical message")
    
    print(f"Log file created at: {logger.get_log_path()}")