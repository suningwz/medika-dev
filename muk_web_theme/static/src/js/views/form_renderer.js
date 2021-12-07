odoo.define('muk_web_theme.FormRenderer', function (require) {
"use strict";

const core = require('web.core');
const config = require("web.config");

const FormRenderer = require('web.FormRenderer');

FormRenderer.include({
    _renderHeaderButtons() {
        const $buttons = this._super(...arguments);
        if (
            !config.device.isMobile ||
            !$buttons.is(":has(>:not(.o_invisible_modifier))")
        ) {
            return $buttons;
        }

        $buttons.addClass("dropdown-menu");
        const $dropdown = $(
            core.qweb.render("muk_web_theme.MenuStatusbarButtons")
        );
        $buttons.addClass("dropdown-menu").appendTo($dropdown);
        return $dropdown;
    },
});

});