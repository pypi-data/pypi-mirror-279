from transstellar.framework import Element


class Switch(Element):
    XPATH_CURRENT = '//button[contains(@class, "ant-switch")]'

    def switch(self, on: bool):
        self.logger.info(f"switch on: {on}")

        ant_switch = self.get_current_dom_element()
        current_checked = ant_switch.get_attribute("aria-checked")

        should_click = (current_checked == "true" and not on) or (
            current_checked == "false" and on
        )

        if should_click:
            ant_switch.click()

        updated_ant_switch = self.refresh()
        current_checked = updated_ant_switch.get_attribute("aria-checked")

        if on:
            assert current_checked == "true"
        else:
            assert current_checked == "false"
