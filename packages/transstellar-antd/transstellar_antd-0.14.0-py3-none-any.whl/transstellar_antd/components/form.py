from transstellar.framework import Element

from .checkbox import Checkbox
from .form_item import FormItem
from .input import Input
from .select import Select
from .switch import Switch
from .text_area import TextArea


class Form(Element):
    XPATH_CURRENT = "//form"
    INPUT_CLASS = Input
    TEXT_AREA_CLASS = TextArea
    SELECT_CLASS = Select
    SWITCH_CLASS = Switch
    CHECKBOX_CLASS = Checkbox

    def input(self, label: str, value: str):
        input_element: Input = self.__find_element_by_label(label, self.INPUT_CLASS)
        input_element.input(value)

    def text_area_input(self, label: str, value: str):
        text_area_element: TextArea = self.__find_element_by_label(
            label, self.TEXT_AREA_CLASS
        )
        text_area_element.input(value)

    def select(self, label: str, value: str):
        select_element: Select = self.__find_element_by_label(label, self.SELECT_CLASS)
        select_element.select(value)

    def switch(self, label: str, value: str):
        switch_element: Switch = self.__find_element_by_label(label, self.SWITCH_CLASS)
        switch_element.switch(value)

    def check(self, label: str, value: str):
        checkbox_element: Checkbox = self.__find_element_by_label(
            label, self.CHECKBOX_CLASS
        )
        checkbox_element.check(value)

    def __find_element_by_label(self, label: str, element_class):
        form_item: FormItem = self.find_element_by_label(FormItem, label)
        element: element_class = form_item.find_form_control(element_class)

        return element
