# -*- coding: utf-8 -*-
"""
Ocean ERP - Exceptions
====================

Custom exceptions for Ocean ERP system.
"""

class OceanException(Exception):
    """Base exception for Ocean ERP"""
    pass

class ValidationError(OceanException):
    """Validation error exception"""
    pass

class AccessError(OceanException):
    """Access error exception"""
    pass

class UserError(OceanException):
    """User error exception"""
    pass

class Warning(OceanException):
    """Warning exception"""
    pass

class RedirectWarning(OceanException):
    """Redirect warning exception"""
    pass

class MissingError(OceanException):
    """Missing error exception"""
    pass

class AccessDenied(OceanException):
    """Access denied exception"""
    pass

class DeferredException(OceanException):
    """Deferred exception"""
    pass