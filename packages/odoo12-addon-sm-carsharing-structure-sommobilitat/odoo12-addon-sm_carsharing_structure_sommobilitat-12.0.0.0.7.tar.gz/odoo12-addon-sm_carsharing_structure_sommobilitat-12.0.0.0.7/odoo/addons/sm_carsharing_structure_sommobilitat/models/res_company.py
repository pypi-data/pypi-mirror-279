# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.tools.translate import _


class sm_company(models.Model):
    _inherit = 'res.company'

    sm_carsharing_structure_sommobilitat_analitic_group = fields.Many2one(
        'account.analytic.group',
        string=_("Fleet Analitic Account Main Group")
    )
    sm_carsharing_structure_sommobilitat_analitic_parent = fields.Many2one(
        'account.analytic.account',
        string=_("Fleet Analitic Account Main Parent")
    )
