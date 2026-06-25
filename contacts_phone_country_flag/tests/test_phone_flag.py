# Copyright much. Consulting (https://muchconsulting.com)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0).
from odoo.tests import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestPhoneCountryFlag(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.Partner = cls.env["res.partner"]
        cls.country_be = cls.env.ref("base.be")

    def _flag(self, code):
        return self.Partner._iso_code_to_flag_emoji(code)

    def test_iso_code_to_flag_emoji(self):
        self.assertEqual(self._flag("BE"), "🇧🇪")
        self.assertEqual(self._flag("be"), "🇧🇪", "lower-case codes are accepted")
        self.assertEqual(self._flag("FR"), "🇫🇷")
        self.assertEqual(self._flag(""), "")
        self.assertEqual(self._flag(False), "")
        self.assertEqual(self._flag("B"), "", "one letter is not a valid code")
        self.assertEqual(self._flag("BEL"), "", "three letters is not a valid code")
        self.assertEqual(self._flag("B1"), "", "digits are not a valid code")

    def test_flag_from_international_prefix(self):
        partner = self.Partner.create({"name": "Test BE", "phone": "+32 2 340 02 25"})
        self.assertEqual(partner.phone_country_flag, "🇧🇪")

        partner.phone = "+33 1 86 65 22 04"
        self.assertEqual(partner.phone_country_flag, "🇫🇷", "flag recomputes on change")

        partner.phone = "+31 20 808 0000"
        self.assertEqual(partner.phone_country_flag, "🇳🇱")

    def test_flag_falls_back_to_country_id(self):
        partner = self.Partner.create({
            "name": "National number",
            "phone": "02 340 02 25",  # national format, no international prefix
            "country_id": self.country_be.id,
        })
        self.assertEqual(partner.phone_country_flag, "🇧🇪")

    def test_prefix_wins_over_country_id(self):
        partner = self.Partner.create({
            "name": "French number, Belgian contact",
            "phone": "+33 1 86 65 22 04",
            "country_id": self.country_be.id,
        })
        self.assertEqual(partner.phone_country_flag, "🇫🇷")

    def test_no_flag_without_prefix_or_country(self):
        partner = self.Partner.create({"name": "National, no country", "phone": "02 340 02 25"})
        self.assertEqual(partner.phone_country_flag, "")

    def test_no_flag_when_no_phone(self):
        partner = self.Partner.create({"name": "No phone", "country_id": False})
        self.assertEqual(partner.phone_country_flag, "")

    def test_no_flag_for_unparseable_number(self):
        partner = self.Partner.create({"name": "Garbage", "phone": "not a number"})
        self.assertEqual(partner.phone_country_flag, "")
