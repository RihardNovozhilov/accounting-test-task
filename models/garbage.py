from calendar import monthrange

from odoo import fields, models, api
from datetime import datetime


class Garbage(models.Model):
    _name = 'garbage'
    _description = 'Collected Garbage'

    date = fields.Datetime(string='Date', required=True, default=fields.Datetime.now,
                           help="Date when garbage is collected.")

    type = fields.Selection([
        ('glass', 'Glass'),
        ('paper', 'Paper'),
        ('plastic', 'Plastic'),
    ], string='Type of Garbage', help="""Select Type of Garbage""")

    weight = fields.Float(string='Weight', digits='Garbage', required=True)
    volume = fields.Float(string='Volume', digits='Garbage', required=True)
    density = fields.Float(string="Density", compute='_compute_density', digits='Garbage')

    total_weight = fields.Float(string="Current month total Weight", compute='_compute_totals', digits='Garbage')
    total_volume = fields.Float(string="Current month total Volume", compute='_compute_totals', digits='Garbage')

    volunteer_id = fields.Many2one('volunteers', 'Related Volunteer', readonly=False, required=False)

    def _compute_density(self):
        for g in self:
            try:
                g.density = g.weight / g.volume
            except ZeroDivisionError:
                g.density = 0

    @api.depends('weight', 'volume', 'type')
    def _compute_totals(self):
        if not self.type:
            self.total_weight = 0
            self.total_volume = 0
            return
        current = datetime.now()
        fd = current.replace(day=1)
        endmonth = monthrange(current.year, current.month)
        ld = datetime(current.year, current.month, endmonth[1])

        self.total_weight = sum(self.search([('date', '>=', fd),
                                             ('date', '<=', ld),
                                             ('type', '=', self.type)]).mapped('weight'))

        self.total_volume = sum(self.search([('date', '>=', fd),
                                             ('date', '<=', ld),
                                             ('type', '=', self.type)]).mapped('volume'))
