
import { Component } from "@odoo/owl";

class MenuItem extends Component {
    static template = "lunch_buffalo.MenuItem";
    static props = {
        item: { type: Object },
    };
}

export default MenuItem;
