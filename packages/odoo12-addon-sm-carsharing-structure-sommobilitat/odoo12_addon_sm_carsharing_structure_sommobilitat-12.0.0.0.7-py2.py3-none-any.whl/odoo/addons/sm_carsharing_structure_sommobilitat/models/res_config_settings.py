# -*- coding: utf-8 -*-
from odoo import fields, api, models, _
from odoo.exceptions import UserError
import logging


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'
    
    sm_carsharing_structure_sommobilitat_analitic_group = fields.Many2one(
        'account.analytic.group',
        related='company_id.sm_carsharing_structure_sommobilitat_analitic_group',
        string=_("Fleet Analitic Account Main Group"),
        readonly=False,
    )
    sm_carsharing_structure_sommobilitat_analitic_parent = fields.Many2one(
        'account.analytic.account',
        related='company_id.sm_carsharing_structure_sommobilitat_analitic_parent',
        string=_("Fleet Analitic Account Main Parent"),
        readonly=False,
    )