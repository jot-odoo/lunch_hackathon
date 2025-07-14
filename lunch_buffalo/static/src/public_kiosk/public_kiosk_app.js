import { patch } from "@web/core/utils/patch";

import hr_kiosk from '@hr_attendance/public_kiosk/public_kiosk_app';
import DailyMenu from "./daily_menu.js";

patch(hr_kiosk.kioskAttendanceApp, {
    components: {
        ...hr_kiosk.kioskAttendanceApp.components,
        DailyMenu,
    }
});
