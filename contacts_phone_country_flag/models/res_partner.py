# Copyright much. Consulting (https://muchconsulting.com)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0).
from odoo import api, fields, models
from odoo.addons.phone_validation.tools.phone_validation import (
    phone_get_region_data_for_number,
)

# Offset between an ASCII uppercase letter and its Unicode regional indicator
# symbol; concatenating the two indicators of an ISO code yields a flag emoji.
_REGIONAL_INDICATOR_OFFSET = ord("\U0001F1E6") - ord("A")


class ResPartner(models.Model):
    _inherit = "res.partner"

    phone_country_flag = fields.Char(
        string="Phone Country Flag",
        compute="_compute_phone_country_flag",
        help="Flag emoji of the phone number's country, detected from its "
        "international prefix and falling back to the contact's country.",
    )

    @api.depends("phone", "country_id")
    def _compute_phone_country_flag(self):
        for partner in self:
            partner.phone_country_flag = partner._phone_country_flag_emoji()

    def _phone_country_flag_emoji(self):
        """Return the flag emoji for this contact's phone number."""
        self.ensure_one()
        code = ""
        if self.phone:
            code = phone_get_region_data_for_number(self.phone).get("code") or ""
        if not code and self.country_id:
            code = self.country_id.code or ""
        return self._iso_code_to_flag_emoji(code)

    @staticmethod
    def _iso_code_to_flag_emoji(code):
        """Convert an ISO 3166-1 alpha-2 code (e.g. ``BE``) into its flag emoji."""
        if not code or len(code) != 2 or not code.isalpha():
            return ""
        return "".join(
            chr(ord(char) + _REGIONAL_INDICATOR_OFFSET) for char in code.upper()
        )
