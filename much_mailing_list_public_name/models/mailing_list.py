# Copyright much. Consulting (https://muchconsulting.com)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0).
from odoo import api, fields, models


class MailingList(models.Model):
    _inherit = 'mailing.list'

    public_name = fields.Char(
        string='Public Name',
        help="Marketing-friendly name shown to recipients on the subscription "
             "and unsubscribe pages. When empty, the internal name is shown instead.")
    public_name_display = fields.Char(
        string='Public Display Name',
        compute='_compute_public_name_display',
        help="Name effectively shown to recipients: the public name, or the "
             "internal name when no public name is set.")

    @api.depends('public_name', 'name')
    def _compute_public_name_display(self):
        for mailing_list in self:
            mailing_list.public_name_display = mailing_list.public_name or mailing_list.name
