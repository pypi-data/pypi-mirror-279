# -*- coding: utf-8 -*-
from odoo import models, fields, api


class cs_state(models.Model):
    _name = 'fleet.vehicle.state'
    _inherit = 'fleet.vehicle.state'
    
    archived = fields.Boolean(string='Arxivat')
