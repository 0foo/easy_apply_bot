from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

class FormItem:
    element=""
    text=""
    answer=""
    type=""
    options=[]
    def __init__(self, element):
        self.element = element
        self.get_text()

    def get_text(self):
        try:
            self.text=self.element.find_element(By.TAG_NAME, "label").text.split("\n")[0]
        except Exception as e:
            print(e)

        try:
            self.text=self.element.find_element(By.XPATH, "./preceding-sibling::*[contains(@class, 't-bold')][1]").text
        except Exception as e:
            print(e)
            raise Exception("Couldn't find the text for an element")
            

    def get_options(self):
        # none available
        pass
    def to_json(self):
        out = vars(self).copy()
        out.pop("element")
        return out
        

class SelectItem(FormItem):
    def __init__(self, element):
        super().__init__(element)
        self.type = "select"

    def get_options(self):
        options=self.element.find_elements(By.TAG_NAME, "option")
        option_list=[]
        for opt in options:
            option_list.append(opt.text)
        self.options=option_list

class InputItem(FormItem):
    def __init__(self, element):
        super().__init__(element)
        self.type = "input"
        pass

class FieldSetItem(FormItem):
    def __init__(self, element):
        super().__init__(element)
        self.type = "fieldset"
    def get_text(self):
        self.text = self.element.find_element(By.TAG_NAME, "fieldset").find_element(By.TAG_NAME, "legend").text.split("\n")[0]
    def get_options(self):
        options=[]
        elements=self.element.find_elements(By.TAG_NAME, "label")
        for element in elements:
            options.append(element.text)
        self.options=options



'''
Input Item
    def populate_item(self):
        self.element.find_element(By.TAG_NAME, "input").send_keys(self.answer)
Field Set Item
    def populate_item(self):
        element = self.element.find_element(By.XPATH, f"//input[@type='radio' and @value='{self.answer}']")
        self.driver.execute_script("arguments[0].click();", element)
Select Item
    def populate_item(self):
        select_element=self.element.find_element(By.TAG_NAME, "select")
        Select(select_element).select_by_visible_text(self.answer)
'''

class FormItemFactory:
    def get_type(self, form_element):
        input_types=["fieldset", "select", "input"]
        for input_type in input_types:
            try:
                form_element.find_element(By.TAG_NAME, input_type)
                return input_type
            except:
                continue

    def get_form_item(self, form_element):
        type = self.get_type(form_element)
        if type == "select":
            return SelectItem(form_element)
        if type == "input":
            return InputItem(form_element)
        if type == "fieldset":
            return FieldSetItem(form_element)



# class FormManager:
#     form_item_list = []


#     def populate_item(self, driver):
#         if self.type == "select":
            
#         if self.type == "input":
#         if self.type=="fieldset":
   

 
#     def populate_form(self):
#         for form_item in self.form_item_list:
#             form_item.populate_item()
