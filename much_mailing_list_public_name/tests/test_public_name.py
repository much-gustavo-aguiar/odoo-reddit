# Copyright much. Consulting (https://muchconsulting.com)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0).
from odoo.tests import HttpCase, tagged


@tagged('post_install', '-at_install')
class TestMailingListPublicName(HttpCase):

    INTERNAL_NAME = 'Premium plan buyers in the DACH region'
    PUBLIC_NAME = 'Our Monthly Newsletter'

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.mailing_list = cls.env['mailing.list'].create({
            'name': cls.INTERNAL_NAME,
            'public_name': cls.PUBLIC_NAME,
            'is_public': True,
        })
        cls.contact = cls.env['mailing.contact'].create({
            'name': 'Test Recipient',
            'email': 'recipient@test.example.com',
            'list_ids': [(4, cls.mailing_list.id)],
        })
        cls.mailing = cls.env['mailing.mailing'].create({
            'subject': 'Test Mailing',
            'body_arch': '<p>Hello</p>',
            'body_html': '<p>Hello</p>',
            'mailing_model_id': cls.env['ir.model']._get_id('mailing.list'),
            'contact_list_ids': [(4, cls.mailing_list.id)],
        })

    def test_public_name_display_uses_public_name(self):
        self.assertEqual(self.mailing_list.public_name_display, self.PUBLIC_NAME)

    def test_public_name_display_falls_back_to_internal_name(self):
        self.mailing_list.public_name = False
        self.assertEqual(self.mailing_list.public_name_display, self.INTERNAL_NAME)

    def test_unsubscribe_page_shows_public_name_only(self):
        """ The portal unsubscribe page must show the public name and never the
        internal mailing-list name (both in the rendered list and the
        controller-built confirmation sentence). """
        hash_token = self.mailing._generate_mailing_recipient_token(
            self.contact.id, self.contact.email_normalized)
        url = (
            f"/mailing/{self.mailing.id}/unsubscribe"
            f"?email={self.contact.email_normalized}"
            f"&document_id={self.contact.id}"
            f"&hash_token={hash_token}"
        )
        response = self.url_open(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.PUBLIC_NAME, response.text)
        self.assertNotIn(self.INTERNAL_NAME, response.text)

    def test_unsubscribe_page_falls_back_when_no_public_name(self):
        """ With no public name set, the internal name is shown (documented
        fallback) so existing lists keep working. """
        self.mailing_list.public_name = False
        hash_token = self.mailing._generate_mailing_recipient_token(
            self.contact.id, self.contact.email_normalized)
        url = (
            f"/mailing/{self.mailing.id}/unsubscribe"
            f"?email={self.contact.email_normalized}"
            f"&document_id={self.contact.id}"
            f"&hash_token={hash_token}"
        )
        response = self.url_open(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.INTERNAL_NAME, response.text)
