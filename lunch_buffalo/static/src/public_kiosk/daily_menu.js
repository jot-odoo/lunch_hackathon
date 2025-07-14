import { Component, useState, onWillUnmount, onWillStart } from "@odoo/owl";
import { rpc } from "@web/core/network/rpc";

import MenuItem from './menu_item';

class DailyMenu extends Component {
    static template = "lunch_buffalo.DailyMenu";
    static components = { MenuItem };

    setup() {
        super.setup();
        this.state = useState({menu:[]});
        this.timeInterval = setInterval(async () => {
            Object.assign(this.state.menu, await this.getTodaysMenu());
        }, 43200000); // Update every 12 hours
        onWillUnmount(() => {
            clearInterval(this.timeInterval);
        });
        onWillStart(async () => {
            Object.assign(this.state.menu, await this.getTodaysMenu());
        });

    }

    async getTodaysMenu() {
        const res = await rpc("/lunch_buffalo/get_current_menu");
        console.log("Today's menu:", res);
        return res;
    }
}

export default DailyMenu;
