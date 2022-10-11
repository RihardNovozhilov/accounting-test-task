from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError


class Volunteer(models.Model):
    _name = 'volunteers'
    _description = 'Volunteers'

    name = fields.Char(string='Name', required=True, help="Volunteer name")
    last_name = fields.Char(string='Last Name', required=True, help="Volunteer Last Name")
    year_of_birth = fields.Integer(string='Year Of Birth', help="Volunteer Year Of Birth")

    email = fields.Char(string='E-mail', help="Volunteer E-mail")
    phone = fields.Char(string='Phone', help="Volunteer Phone")

    address = fields.Char(string='Address', help="Volunteer Address")
    image = fields.Image(string='Image')
    notes = fields.Text(string='Notes')

    garbage_total_weight = fields.Float(string="Volunteer total weight", compute='_compute_totals', digits='Garbage')
    garbage_total_volume = fields.Float(string="Volunteer total volume", compute='_compute_totals', digits='Garbage')

    collected_garbage = fields.One2many('garbage', 'volunteer_id', string="Collected Garbage", readonly=True,
                                        ondelete='cascade')

    # username = fields.Char(string="Username", compute='_compute_username', store=False)
    def _compute_totals(self):
        self.garbage_total_weight = 0
        self.garbage_total_volume = 0
        for g in self.collected_garbage:
            self.garbage_total_weight += g.weight
            self.garbage_total_volume += g.volume

    @api.constrains('name')
    def check_name(self):
        for rec in self:
            if any(char.isdigit() for char in rec.name):
                raise ValidationError(_('The first name must contain alpha characters only.'))

    @api.constrains('year_of_birth')
    def check_year(self):
        for rec in self:
            if rec.year_of_birth < 0:
                raise ValidationError(_('Field: Year Of Birth\nOnly positive numbers allowed.'))

    def name_get(self):
        result = []
        for v in self:
            result.append((v.id, f'{v.name or ""} {v.last_name or ""} {v.email or ""}'))
        return result

    # @api.onchange('year_of_birth')
    # def _onchange_year(self):
    #     if self.year_of_birth < 0:
    #         raise ValidationError(_('Only positive numbers allowed.'))
