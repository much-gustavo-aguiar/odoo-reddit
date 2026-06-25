import { registry } from "@web/core/registry";
import { stepUtils } from "@web_tour/tour_utils";

registry.category("web_tour.tours").add("contacts_phone_country_flag_tour", {
    url: "/odoo",
    steps: () => [
        ...stepUtils.goToAppSteps("contacts.menu_contacts", "Open the Contacts app"),
        {
            content: "Create a new contact",
            trigger: ".o_list_button_add",
            run: "click",
        },
        {
            content: "Enter a Belgian phone number",
            trigger: ".o_field_widget[name='phone'] input",
            run: "edit +32 2 340 02 25",
        },
        {
            content: "Blur the phone field to commit the value (triggers onchange)",
            trigger: ".o_field_widget[name='phone'] input",
            run: "press Tab",
        },
        {
            content: "The Belgian flag emoji appears next to the phone number",
            trigger: ".o_field_widget[name='phone'] .o_phone_country_flag",
            run() {
                const flag = this.anchor.textContent.trim();
                if (flag !== "🇧🇪") {
                    throw new Error(`Expected 🇧🇪 next to the phone, got "${flag}"`);
                }
            },
        },
        {
            content: "Discard the unsaved contact to leave a clean state",
            trigger: ".o_form_button_cancel",
            run: "click",
        },
        {
            content: "Back on the contacts list",
            trigger: ".o_control_panel .o_list_button_add",
        },
    ],
});
