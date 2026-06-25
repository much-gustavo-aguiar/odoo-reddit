# Copyright much. Consulting (https://muchconsulting.com)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0).
from odoo.tests import HttpCase, tagged


@tagged("post_install", "-at_install")
class TestPhoneCountryFlagTour(HttpCase):
    def test_phone_country_flag_tour(self):
        self.start_tour(
            "/odoo",
            "contacts_phone_country_flag_tour",
            login="admin",
        )
