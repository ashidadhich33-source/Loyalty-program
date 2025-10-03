# -*- coding: utf-8 -*-

from core_framework.testing import TestCase


class TestLoyaltyProgram(TestCase):
    
    def setUp(self):
        super(TestLoyaltyProgram, self).setUp()
        self.loyalty_program = self.env['loyalty.program']
        self.loyalty_points = self.env['loyalty.points']
        self.loyalty_reward = self.env['loyalty.reward']
        self.loyalty_voucher = self.env['loyalty.voucher']
        self.loyalty_offer = self.env['loyalty.offer']
        self.loyalty_tier = self.env['loyalty.tier']
    
    def test_create_loyalty_program(self):
        """Test creating a loyalty program"""
        program = self.loyalty_program.create({
            'name': 'Test Loyalty Program',
            'code': 'TEST_LOYALTY',
            'description': 'Test loyalty program',
            'is_active': True,
            'start_date': '2024-01-01',
            'points_per_currency': 1.0,
            'currency_id': self.env.ref('base.USD').id,
            'min_points_redemption': 100,
            'max_points_redemption': 10000,
            'points_expiry_days': 365,
            'expiry_notification_days': 30,
            'tier_based': True,
            'age_group_focus': 'all',
            'gender_focus': 'all',
            'seasonal_focus': 'all',
            'birthday_offers': True,
            'referral_program': True,
            'referral_points': 100,
        })
        
        self.assertEqual(program.name, 'Test Loyalty Program')
        self.assertEqual(program.code, 'TEST_LOYALTY')
        self.assertEqual(program.description, 'Test loyalty program')
        self.assertTrue(program.is_active)
        self.assertEqual(program.start_date, '2024-01-01')
        self.assertEqual(program.points_per_currency, 1.0)
        self.assertEqual(program.min_points_redemption, 100)
        self.assertEqual(program.max_points_redemption, 10000)
        self.assertEqual(program.points_expiry_days, 365)
        self.assertEqual(program.expiry_notification_days, 30)
        self.assertTrue(program.tier_based)
        self.assertEqual(program.age_group_focus, 'all')
        self.assertEqual(program.gender_focus, 'all')
        self.assertEqual(program.seasonal_focus, 'all')
        self.assertTrue(program.birthday_offers)
        self.assertTrue(program.referral_program)
        self.assertEqual(program.referral_points, 100)
    
    def test_create_loyalty_points(self):
        """Test creating loyalty points"""
        partner = self.env['res.partner'].create({
            'name': 'Test Customer',
            'email': 'test@example.com',
        })
        
        program = self.loyalty_program.create({
            'name': 'Test Program',
            'code': 'TEST',
            'start_date': '2024-01-01',
            'currency_id': self.env.ref('base.USD').id,
        })
        
        points = self.loyalty_points.create({
            'name': 'PTS-001',
            'partner_id': partner.id,
            'program_id': program.id,
            'points': 100,
            'points_type': 'earned',
            'transaction_type': 'purchase',
        })
        
        self.assertEqual(points.name, 'PTS-001')
        self.assertEqual(points.partner_id, partner)
        self.assertEqual(points.program_id, program)
        self.assertEqual(points.points, 100)
        self.assertEqual(points.points_type, 'earned')
        self.assertEqual(points.transaction_type, 'purchase')
    
    def test_create_loyalty_reward(self):
        """Test creating loyalty reward"""
        reward = self.loyalty_reward.create({
            'name': 'Test Reward',
            'description': 'Test reward description',
            'is_active': True,
            'points_required': 100,
            'reward_type': 'discount',
            'discount_type': 'percentage',
            'discount_value': 10.0,
            'total_quantity': 100,
            'age_group': 'all',
            'gender': 'all',
            'season': 'all',
            'is_birthday_reward': False,
            'is_referral_reward': False,
            'is_tier_exclusive': False,
        })
        
        self.assertEqual(reward.name, 'Test Reward')
        self.assertEqual(reward.description, 'Test reward description')
        self.assertTrue(reward.is_active)
        self.assertEqual(reward.points_required, 100)
        self.assertEqual(reward.reward_type, 'discount')
        self.assertEqual(reward.discount_type, 'percentage')
        self.assertEqual(reward.discount_value, 10.0)
        self.assertEqual(reward.total_quantity, 100)
        self.assertEqual(reward.age_group, 'all')
        self.assertEqual(reward.gender, 'all')
        self.assertEqual(reward.season, 'all')
        self.assertFalse(reward.is_birthday_reward)
        self.assertFalse(reward.is_referral_reward)
        self.assertFalse(reward.is_tier_exclusive)
    
    def test_create_loyalty_voucher(self):
        """Test creating loyalty voucher"""
        template = self.env['loyalty.voucher.template'].create({
            'name': 'Test Template',
            'code': 'TEST_TEMPLATE',
            'voucher_type': 'discount',
            'discount_type': 'percentage',
            'discount_value': 10.0,
            'validity_days': 30,
        })
        
        voucher = self.loyalty_voucher.create({
            'name': 'VOUCHER001',
            'template_id': template.id,
            'voucher_type': 'discount',
            'discount_type': 'percentage',
            'discount_value': 10.0,
            'validity_days': 30,
            'expiry_date': '2024-02-15',
            'usage_limit': 1,
            'usage_limit_per_customer': 1,
            'state': 'draft',
        })
        
        self.assertEqual(voucher.name, 'VOUCHER001')
        self.assertEqual(voucher.template_id, template)
        self.assertEqual(voucher.voucher_type, 'discount')
        self.assertEqual(voucher.discount_type, 'percentage')
        self.assertEqual(voucher.discount_value, 10.0)
        self.assertEqual(voucher.validity_days, 30)
        self.assertEqual(voucher.expiry_date, '2024-02-15')
        self.assertEqual(voucher.usage_limit, 1)
        self.assertEqual(voucher.usage_limit_per_customer, 1)
        self.assertEqual(voucher.state, 'draft')
    
    def test_create_loyalty_offer(self):
        """Test creating loyalty offer"""
        offer = self.loyalty_offer.create({
            'name': 'Test Offer',
            'description': 'Test offer description',
            'is_active': True,
            'offer_type': 'promotional',
            'start_date': '2024-01-01',
            'end_date': '2024-01-31',
            'is_permanent': False,
            'offer_value': 15.0,
            'min_purchase_amount': 50.0,
            'max_offer_amount': 100.0,
            'points_multiplier': 1.5,
            'bonus_points': 50,
            'points_required': 0,
            'customer_segment': 'all',
            'age_group': 'all',
            'gender': 'all',
            'season': 'all',
            'child_age_min': 0,
            'child_age_max': 216,
            'usage_limit': 0,
            'usage_limit_per_customer': 2,
            'is_automatic': True,
            'is_notification_sent': False,
        })
        
        self.assertEqual(offer.name, 'Test Offer')
        self.assertEqual(offer.description, 'Test offer description')
        self.assertTrue(offer.is_active)
        self.assertEqual(offer.offer_type, 'promotional')
        self.assertEqual(offer.start_date, '2024-01-01')
        self.assertEqual(offer.end_date, '2024-01-31')
        self.assertFalse(offer.is_permanent)
        self.assertEqual(offer.offer_value, 15.0)
        self.assertEqual(offer.min_purchase_amount, 50.0)
        self.assertEqual(offer.max_offer_amount, 100.0)
        self.assertEqual(offer.points_multiplier, 1.5)
        self.assertEqual(offer.bonus_points, 50)
        self.assertEqual(offer.points_required, 0)
        self.assertEqual(offer.customer_segment, 'all')
        self.assertEqual(offer.age_group, 'all')
        self.assertEqual(offer.gender, 'all')
        self.assertEqual(offer.season, 'all')
        self.assertEqual(offer.child_age_min, 0)
        self.assertEqual(offer.child_age_max, 216)
        self.assertEqual(offer.usage_limit, 0)
        self.assertEqual(offer.usage_limit_per_customer, 2)
        self.assertTrue(offer.is_automatic)
        self.assertFalse(offer.is_notification_sent)
    
    def test_create_loyalty_tier(self):
        """Test creating loyalty tier"""
        program = self.loyalty_program.create({
            'name': 'Test Program',
            'code': 'TEST',
            'start_date': '2024-01-01',
            'currency_id': self.env.ref('base.USD').id,
        })
        
        tier = self.loyalty_tier.create({
            'name': 'Test Tier',
            'code': 'TEST_TIER',
            'program_id': program.id,
            'sequence': 10,
            'is_active': True,
            'min_points': 0,
            'max_points': 999,
            'min_purchases': 0,
            'min_purchase_amount': 0.0,
            'min_purchase_frequency': 0,
            'points_multiplier': 1.0,
            'discount_percentage': 0.0,
            'free_shipping': False,
            'priority_support': False,
            'exclusive_access': False,
            'birthday_bonus_points': 0,
            'referral_bonus_points': 0,
            'seasonal_bonus_points': 0,
            'milestone_bonus_points': 0,
            'age_group_benefits': 'all',
            'gender_benefits': 'all',
            'seasonal_benefits': 'all',
        })
        
        self.assertEqual(tier.name, 'Test Tier')
        self.assertEqual(tier.code, 'TEST_TIER')
        self.assertEqual(tier.program_id, program)
        self.assertEqual(tier.sequence, 10)
        self.assertTrue(tier.is_active)
        self.assertEqual(tier.min_points, 0)
        self.assertEqual(tier.max_points, 999)
        self.assertEqual(tier.min_purchases, 0)
        self.assertEqual(tier.min_purchase_amount, 0.0)
        self.assertEqual(tier.min_purchase_frequency, 0)
        self.assertEqual(tier.points_multiplier, 1.0)
        self.assertEqual(tier.discount_percentage, 0.0)
        self.assertFalse(tier.free_shipping)
        self.assertFalse(tier.priority_support)
        self.assertFalse(tier.exclusive_access)
        self.assertEqual(tier.birthday_bonus_points, 0)
        self.assertEqual(tier.referral_bonus_points, 0)
        self.assertEqual(tier.seasonal_bonus_points, 0)
        self.assertEqual(tier.milestone_bonus_points, 0)
        self.assertEqual(tier.age_group_benefits, 'all')
        self.assertEqual(tier.gender_benefits, 'all')
        self.assertEqual(tier.seasonal_benefits, 'all')