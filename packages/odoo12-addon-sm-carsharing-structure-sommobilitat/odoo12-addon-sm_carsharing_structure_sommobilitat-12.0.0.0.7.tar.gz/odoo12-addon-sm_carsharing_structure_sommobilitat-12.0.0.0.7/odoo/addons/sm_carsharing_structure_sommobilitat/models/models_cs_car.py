# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.tools.translate import _
from odoo.exceptions import UserError
import logging

class cs_car(models.Model):
    _name = 'fleet.vehicle'
    _inherit = 'fleet.vehicle'

    def _get_default_state(self):
        """ Overriden method originally in fleet module! """
        state = self.env.ref('sm_carsharing_structure_sommobilitat.fleet_vehicle_state_active', raise_if_not_found=False)
        return state if state and state.id else False
    
    
    battery_fee = fields.Selection([
        ('rent', _("Lloguer")),
        ('bougth', _("Compra")),
        ('no-quota', _("Sense Quota"))
    ], string=_("Bateria propietat"), default="rent")
    car_type = fields.Selection([
        ('fp', _("FP")),
        ('renting', _("Renting")),
        ('cic', _("CiC")),
        ('p2p', _("P2P")),
    ], string=_("Modalitat"), default="fp")
    bougth_km = fields.Integer(string=_("Km a la compra"))
    bougth_date = fields.Date(
        string=_("Data de compra"),
        related="purchase_invoice_id.date_invoice",
    )
    r_link_update = fields.Boolean(string=_("R-Link update"))
    key_number = fields.Char(string=_("Núm clau"))
    insurance_company = fields.Char(string=_("Asseguradora"))
    insurance_age = fields.Char(string=_("Edat assegurança"))
    insurance_policy = fields.Char(string=_("Polissa assegurança"))
    insurance_expiricy = fields.Date(string=_("Venciment Assegurança"))
    insurance_extras = fields.Text(string=_("Garanties Extres"))
    battery_size = fields.Integer(string=_("Capacitat bateria"))
    next_tech_revision = fields.Date(string=_("Propera ITV"))
    next_revision = fields.Date(string=_("Propera revisió"))
    viat_applies = fields.Boolean(string=_("Aplica Via-T"))
    viat_pan = fields.Char(string=_("PAN Via-T"))
    viat_expiricy = fields.Date(string=_("Caducitat Via-T"))
    viat_onplace = fields.Boolean(string=_("Via-T col.locat?"))
    viat_eco_accepted = fields.Boolean(string=_("Eco Via-T acceptat?"))
    viat_eco_approved_date = fields.Date(string=_("Data aprovació Eco Via-T"))
    ivtm_status = fields.Selection([
        ('no', _("No")),
        ('no_apply', _("No aplica")),
        ('presented', _("Instància presentada")),
        ('yes', _("IVTM BONIFICAT"))
    ], string=_("Tramitada bonificació IVTM"), default="no")
    live_card = fields.Char(string=_("Targeta Live"))
    live_card_status = fields.Char(string=_("Estat Targeta Live"))
    live_smou = fields.Char(string=_("Live a SMOU"))
    electromaps_code = fields.Char(string=_("Codi electromaps"))
    garagekey_code = fields.Char(string=_("Mando garatge"))
    secondary_key_location = fields.Char(string=_("Ubicacio segona clau"))
    battery_rental = fields.Float(_("Quota bateria (sense IVA)"))
    contact_person_txt = fields.Char(string=_("Contacte"))
    vinyl = fields.Char(string=_("Vinil"))
    origin = fields.Char(string=_("Origen"))
    drive_docs = fields.Char(string=_("Documentació DRIVE"))
    has_gps = fields.Boolean(string=_("Has GPS?"))


    ## NEW FIELDS ##
    
    # Dades Vehicle

    sm_version = fields.Char(string=_("Versió"))
    tire_type = fields.Char(string=_("Mida rodes"))
    vehicle_license = fields.Char(string=_("Permís circulació"))
    technical_data = fields.Char(string=_("Fitxa tècnica"))
    ownership = fields.Selection(
        [
            ('owned', 'Owned'),
            ('lesed', 'Lessed'),
            ('rented', 'Rented'),
            ('customer', 'Customer')
        ],
        default="owned",
        string="Propietat",
    )
    app_service = fields.Boolean(
        string=_("App Service")
    )


    # Dades Compra

    partner_id = fields.Many2one(
        'res.partner',
        string=_("Proveïdor/Concessionàri")
    )
    purchase_invoice_id = fields.Many2one(
        'account.invoice',
        string=_("Factura")
    )
    currency_id = fields.Many2one(
        'res.currency',
        related="purchase_invoice_id.currency_id",
    )
    bought_price = fields.Monetary(
        string="Preu de compra",
        readonly=True,
        related="purchase_invoice_id.amount_total"
    )
    financing = fields.Boolean(string="Finançament")
    account_loan_id = fields.Many2one(
      'account.loan',
      string="Préstec"
    )
    financing_end_finish = fields.Date(
      string="Data Finalització finançament"
    )
    financing_contract = fields.Char(
      string="Contracte de finançament"
    )


    # Dades Venda

    date_change_name = fields.Date(
        string="Data confirmació canvi de nom"
    )
    sale_invoice_id = fields.Many2one(
        'account.invoice',
        string="Factura"
    )
    sale_date = fields.Date(
        string="Data Venda",
        related="sale_invoice_id.date_invoice",
        readonly=True,
    )
    sale_price = fields.Monetary(
        string="Preu Venda",
        related="sale_invoice_id.amount_total",
        readonly=True,
    )
    sale_partner_id = fields.Many2one(
        'res.partner',
        string="Nom comprador",
        related="sale_invoice_id.partner_id",
        readonly=True,
    )
    sale_phone = fields.Char(
        string="Telèfon",
        related="sale_partner_id.phone",
        readonly=True,
    )
    sale_mobile = fields.Char(
        string="Telèfon",
        related="sale_partner_id.mobile",
        readonly=True,
    )
    sale_email = fields.Char(
        string="Email",
        related="sale_partner_id.email",
        readonly=True,
    )


    # Altres

    barcelona_id_code = fields.Char(
        string=_("Codi identificatiu Barcelona"),
        related="live_card",
        store=True,
        readonly=False
    )


    # Modalitat Servei

    contracte_actiu = fields.Many2one(
        'contract.contract',
        string="Contracte actiu"
    )

    state_id = fields.Many2one(
        'fleet.vehicle.state',
        'State',
        default=_get_default_state,
        group_expand='_read_group_stage_ids',
        track_visibility="onchange",
        help='Current state of the vehicle',
        ondelete="set null"
    )


    @api.multi
    @api.onchange('state_id')
    def _onchange_state_id(self):
        for vehicle in self:
            if vehicle.state_id:
                if vehicle.state_id.archived and vehicle.active:
                    vehicle.active = False
                elif not vehicle.state_id.archived and not vehicle.active:
                    vehicle.active = True

    # Dades Propietari
    owner_partner_id = fields.Many2one(
        'res.partner',
        string="Propietari"
    )


    @api.multi
    @api.onchange('license_plate')
    def _onchange_license_plate(self):
        for vehicle in self:
            if vehicle.license_plate:
                vehicle.license_plate = vehicle.license_plate.replace(" ", "")
    
    # Mantenimiento

    # Revisió anual després de compra: (fecha)
    annual_revision_after_purchase_date = fields.Date(
        string="Revisió anual després de compra",
    )
    # ITV després de compra: (Fecha)
    itv_after_purchase_date = fields.Date(
        string="ITV després de compra",
    )
    # % rodes davant després de compra: (Integer)
    front_tire_percent_after_purchase = fields.Integer(
        string="% rodes davant després de compra",
    )
    # % rodes darrera després de compra: (Integer)
    rear_tire_percent_after_purchase = fields.Integer(
        string="% rodes darrera després de compra",
    )
    document_last_itv = fields.Char(
        string="Document ITV passada",
    )



    @api.model
    def create(self, vals):
        group_id        = self.env.user.company_id.sm_carsharing_structure_sommobilitat_analitic_group
        parent_account  = self.env.user.company_id.sm_carsharing_structure_sommobilitat_analitic_parent
        if not vals.get('license_plate'):
            raise UserError("You need to provide a license plate!")
        account = self.env['account.analytic.account'].create({
                'name'      : vals.get('license_plate'),
                'group_id'  : group_id.id if group_id else None,
                'parent_id' : parent_account.id if parent_account else None,
        })
        vals.update({'analytic_account_id' : account.id})
        return super(cs_car, self).create(vals)


    @api.model
    def default_get(self, fields_list):
        defaults = super().default_get(fields_list)
        defaults.update()
        return defaults

    
    # Assegurança

    ensurance_provider = fields.Many2one(
        'res.partner',
        string="Proveïdor"
    )

    ensurance_phone = fields.Char(
        string="Telèfon",
        related="ensurance_provider.phone",
        readonly=True,
    )

    ensurance_mobile = fields.Char(
        string="Telèfon",
        related="ensurance_provider.mobile",
        readonly=True,
    )

    ensurance_polissa = fields.Char(
        string="Polissa"
    )
    
    ensurance_document = fields.Char(
        string="Document"
    )

    ensurance_extras = fields.Text(
        string="Extras"
    )



