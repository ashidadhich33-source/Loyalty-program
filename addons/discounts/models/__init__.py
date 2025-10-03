#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - Discounts Models
====================================

Discount program models for kids clothing retail.
"""

from .discount_program import DiscountProgram, DiscountProgramProduct, DiscountProgramCategory
from .discount_rule import DiscountRule, DiscountRuleProduct, DiscountRuleCategory
from .discount_coupon import DiscountCouponTemplate, DiscountCoupon, DiscountCouponUsage
from .discount_approval import DiscountApprovalWorkflow, DiscountApprovalStep, DiscountApprovalApprover, DiscountApprovalRequest
from .discount_campaign import DiscountCampaign, DiscountCampaignProduct, DiscountCampaignCategory, DiscountCampaignRule
from .discount_analytics import DiscountAnalytics, DiscountCustomerAnalytics