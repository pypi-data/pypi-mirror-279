from transstellar.framework import Element


class Checkbox(Element):
    XPATH_CURRENT = '//span[contains(@class, "ant-checkbox")]'

    def get_checkbox_xpath(self, label):
        if label:
            return f'//div[label/text()="{label}"]/following-sibling::div{self.XPATH_CURRENT}'
        else:
            return self.XPATH_CURRENT

    def check(self, on: bool):
        self.logger.info(f"check on: {on}")

        ant_checkbox = self.get_current_dom_element()
        class_names = ant_checkbox.get_attribute("class")
        current_checked = "ant-checkbox-checked" in class_names.split()

        should_click = (not current_checked and on) or (current_checked and not on)
        self.logger.debug(
            f"current_checked: {current_checked}, should_click: {should_click}, on: {on}"
        )

        if should_click:
            ant_checkbox.click()

        updated_ant_checkbox = self.refresh()
        current_checked = updated_ant_checkbox.get_attribute("aria-checked")

        updated_class_names = updated_ant_checkbox.get_attribute("class")
        current_checked = "ant-checkbox-checked" in updated_class_names.split()

        assert current_checked == on
