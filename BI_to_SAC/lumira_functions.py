import xml.etree.ElementTree as ET
import pprint
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException, ElementNotInteractableException
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, InvalidArgumentException, InvalidElementStateException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
from test import *
import re
import json
import test
import streamlit as st



options = None
driver = None
wait = None

def start_sac_screen(model_name1):
    
    # Create an instance of ChromeOptions
    global options
    global driver
    global wait
    options = Options()

# Add command-line arguments
    options.add_argument("force-device-scale-factor=0.8")
    options.add_argument("high-dpi-support=0.8")
    options.add_argument("start-maximized")
    # Initialize the Chrome driver with the options
    driver = webdriver.Chrome(options=options)

    wait = WebDriverWait(driver, 10)

    # Resize the window to a specific zoom level (75%)
    driver.execute_script("document.body.style.zoom='75%'") 

    driver.get("https://maventic.jp10.hcs.cloud.sap/")
    try:
        username = driver.find_element(By.ID, "j_username")
    except (StaleElementReferenceException, TimeoutException) as e:
        username = driver.find_element(By.ID, "j_username")
    try:
        password = driver.find_element(By.ID, "j_password")
    except (StaleElementReferenceException, TimeoutException) as e:
        password = driver.find_element(By.ID, "j_password")
    
    username.send_keys("piyush.gahlot@maventic.com")
    password.send_keys("Maven2020@")

    #logOnFormSubmit
    try:
        login = driver.find_element(By.ID, "logOnFormSubmit")
        login.click()
    except (StaleElementReferenceException, TimeoutException) as e:
        login = driver.find_element(By.ID, "logOnFormSubmit")
        login.click()

    # Initialize WebDriverWait with a timeout of 30 seconds
    wait = WebDriverWait(driver, 10)
    time.sleep(10)
    # Story Button
    try:
        story = wait.until(EC.element_to_be_clickable((By.XPATH, "//li[@title='Stories']")))
        story.click()
    except (StaleElementReferenceException, TimeoutException, NoSuchElementException, ElementClickInterceptedException) as e:
        story = driver.find_element(By.XPATH, "//li[@title='Stories']")
        story.click()

    # Select Canvas
    try:
        canvas = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//div[@title='Canvas'][@role='button']"))
        )
        canvas.click()
    except (StaleElementReferenceException, TimeoutException) as e:
        canvas = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div[title='Canvas'][role='button']")))
        # Click the element
        canvas.click()

    # Select Optimized Design Experience
    # ode = wait.until(EC.element_to_be_clickable((By.ID, "__button32-label-bdi")))
    # ode.click()


    # Select Create Button
    try:
        create = wait.until(EC.element_to_be_clickable((By.XPATH, "//*/*/*/footer/div/button[1]")))
        create.click()
    except TimeoutException as e:
        create = driver.find_element(By.XPATH, "//*/*/*/footer/div/button[1]")
        create.click()
    time.sleep(10)
    try:
        outline = wait.until(EC.element_to_be_clickable((By.ID, "outline")))
        outline.click()
    except TimeoutException as e:
        outline = wait.until(EC.element_to_be_clickable((By.ID, "outline")))
        outline.click()

    # For First Time, select model

    # title="Model (Analytic)"
    # title="Model (Planning)"

    # Select Chart button +
    try:
        chart_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@title='Chart']"))) 
        chart_btn.click()
    except (StaleElementReferenceException, TimeoutException) as e:
        chart_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@title='Chart']"))) 
        chart_btn.click()

    print(model_name1)
    model_name = model_name1
    try:
        search_model = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@type='search']")))
        search_model.click()
        search_model.clear()
        search_model.send_keys(model_name + Keys.ENTER)
    except (StaleElementReferenceException, TimeoutException, ElementClickInterceptedException ) as e:
        search_input = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[type='search']")))
        search_input.click()  # Click to focus
        search_input.clear()  # Clear the input field
        search_input.send_keys(model_name + Keys.ENTER)

    wait.until(EC.element_to_be_clickable((By.XPATH, "//span[@title='Model (Analytic)' or @title='Model (Planning)']"))).click()

    # Delete Chart
    # time.sleep(3)
    try:
        more_actions = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[@aria-label='More Actions']")))
        more_actions.click()

        delete_chart = wait.until(EC.element_to_be_clickable((By.XPATH, "//li[@title='Remove']")))
        delete_chart.click()
    except (StaleElementReferenceException, TimeoutException, ElementClickInterceptedException) as e:
        chart_1 = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Chart_1')]"))) 
        chart_1.click()
        delete_chart = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@title='Delete']")))
        delete_chart.click()



    right_panel_handler('Styling')



class Lumira:
    class Component:
        def __init__(self, name, type_=None):
            self.name = name
            self.type_ = type_
            self.children = []

        def add_child(self, child):
            self.children.append(child)

        def __repr__(self, level=0):
            ret = "\t" * level + repr(self.name) + (f" (Type: {self.type_})" if self.type_ else "") + "\n"
            for child in self.children:
                ret += child.__repr__(level + 1)
            return ret
        
        def iterate(self):
            yield self
            for child in self.children:
                yield from child.iterate()

    def __init__(self, xml_file):
        self.component_tree = None
        self.component_properties = None
        self.xml_file = xml_file

    def build_component_tree(self):
        tree = ET.parse(self.xml_file)
        root = tree.getroot()
        component_hierarchy = self.build_hierarchy(root)
        self.component_tree = self.build_component_tree_from_hierarchy(component_hierarchy['ROOT'])

    def build_hierarchy(self, element):
        namespaces = {
            'bi': 'http://xml.sap.com/2011/biml/biapp',
            'jsp': 'http://java.sun.com/JSP/Page',
            'html': 'http://www.w3.org/TR/REC-html40',
            'h': 'http://www.w3.org/TR/REC-html40',
            'sdk1': 'com.sap.ip.bi'
        }
        hierarchy = {}
        for child in element:
            if 'name' in child.attrib:
                child_name = child.attrib['name']
                if not child.tag.endswith('property'):
                    child_hierarchy = self.build_hierarchy(child)
                    if child_name not in hierarchy:
                        hierarchy[child_name] = []
                    if child_hierarchy:
                        hierarchy[child_name].append(child_hierarchy)
        return hierarchy

    def build_component_tree_from_hierarchy(self, components):
        root = self.Component('ROOT')

        def add_components(parent, components):
            for key, value in components.items():
                # Determine the type for the component if available
                component_type = self.find_component_type(key)
                component = self.Component(key, component_type)
                parent.add_child(component)
                if isinstance(value, list):
                    for item in value:
                        add_components(component, item)
                elif isinstance(value, dict):
                    add_components(component, value)

        for component_dict in components:
            for key, value in component_dict.items():
                add_components(root, {key: value})

        return root

    def extract_component_properties(self):
        tree = ET.parse(self.xml_file)
        root = tree.getroot()
        component_hierarchy, component_properties = self.build_hierarchy_and_properties(root)
        self.component_properties = component_properties

    def build_hierarchy_and_properties(self, element):
        namespaces = {
            'bi': 'http://xml.sap.com/2011/biml/biapp',
            'jsp': 'http://java.sun.com/JSP/Page',
            'html': 'http://www.w3.org/TR/REC-html40',
            'h': 'http://www.w3.org/TR/REC-html40',
            'sdk1': 'com.sap.ip.bi'
        }
        hierarchy = {}
        properties_dict = {}

        for child in element:
            if 'name' in child.attrib:
                child_name = child.attrib['name']

                # Extract properties that are direct children of this component
                properties = {}
                for prop in child.findall('bi:property', namespaces):
                    prop_name = prop.attrib.get('name')
                    prop_value = prop.attrib.get('value', '')
                    if prop_name:
                        properties[prop_name] = prop_value

                # Update properties_dict for this component
                properties_dict[child_name] = properties

                # Recursively build the hierarchy and get child properties
                child_hierarchy, child_properties = self.build_hierarchy_and_properties(child)
                if child_name not in hierarchy:
                    hierarchy[child_name] = []
                if child_hierarchy:
                    hierarchy[child_name].extend(child_hierarchy.keys())

                # Merge child properties into the main properties dictionary
                properties_dict.update(child_properties)

        return hierarchy, properties_dict

    def find_component_type(self, component_name):
        namespaces = {'bi': 'http://example.com/bi'}
        with open(self.xml_file, 'r') as f:
            lines = f.readlines()

        component_name_tag = f'<bi:component name="{component_name}"'
        try:
            for line in lines:
                if component_name_tag in line:
                    component_line = line.strip()
                    component_line_with_ns = component_line.replace('<bi:', '<').replace('</bi:', '</')
                    element = ET.fromstring(component_line_with_ns + "</component>")
                    name = element.attrib.get('name')
                    type_ = element.attrib.get('type')
                    return type_
        except:
            pass 
        return None

    def print_component_tree(self):
        def print_tree(component, parent_name="ROOT", level=0):
            if component.name != "ROOT":  # Skip printing the root element itself
                print(f"${parent_name} -> {component.name} (Type: {component.type_})")
            for child in component.children:
                print_tree(child, component.name, level + 1)

        if self.component_tree:
            print_tree(self.component_tree)

    def call_sac(self):
        res_sac = []

        def iterate_with_parent_and_grandparent(component, parent_name, parent_type, grandparent_name, grandparent_type):
            yield (parent_name, parent_type, grandparent_name, grandparent_type, component)
            for child in component.children:
                yield from iterate_with_parent_and_grandparent(child, component.name, component.type_, parent_name, parent_type)

        if self.component_tree:
            for parent_name, parent_type, grandparent_name, grandparent_type, component in iterate_with_parent_and_grandparent(self.component_tree, "ROOT", None, None, None):
                type_ = self.find_component_type(component.name)
                name = component.name
                prop = self.component_properties.get(name, {})
                prop['Name'] = name
                prop['Type'] = type_
                prop['Parent_Name'] = parent_name
                prop['Parent_Type'] = parent_type
                if parent_type == 'PANEL_COMPONENT' and type_ in ['info/number']:
                    prop['Grandparent_Name'] = grandparent_name
                    prop['Grandparent_Type'] = grandparent_type
                res_sac.append(prop)
        return res_sac


def parent_selector(parent_name):
    if parent_name != 'ROOT':
        try:
            parent_selector = wait.until(EC.element_to_be_clickable((By.XPATH, f"//span[text() = '{parent_name}']"))) 
            parent_selector.click()
            parent_selector.click()
        except (ElementClickInterceptedException, TimeoutException) as e:
            parent_selector = wait.until(EC.element_to_be_clickable((By.XPATH, f"//span[text() = '{parent_name}']"))) 
            parent_selector.click()
            parent_selector.click()
    else:
        # //span[@class='subTitle' and text()='ROOT']
        try:
            parent_selector = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[@class='subTitle' and text() = 'ROOT']"))) 
            parent_selector.click()
        except (ElementClickInterceptedException, TimeoutException) as e:
            parent_selector = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[@class='subTitle' and text() = 'ROOT']"))) 
            parent_selector.click()


#styling menu navigation
# styling_btn_text = driver.find_element(By.XPATH, "//span[contains(text(), 'Styling')]")

def right_panel_handler(pane_name):

  wait = WebDriverWait(driver, 4)
  if pane_name == 'Styling':
    try:
      styling_btn_text = driver.find_element(By.XPATH, "//span[contains(text(), 'Styling')]")
      if styling_btn_text.is_displayed():
        styling_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[@title='Styling']")))
        styling_btn.click()
      else:
        try:
            styling_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[@title='Styling']")))
            styling_btn.click()
        except (ElementClickInterceptedException, TimeoutException) as e:
            styling_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[@title='Styling']")))
            styling_btn.click()
    except TimeoutException as e:
      right_panel = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@title='Right Side Panel']"))) 
      right_panel.click()
      styling_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[@title='Styling']")))
      styling_btn.click()
  else:
    try:
      styling_btn_text = driver.find_element(By.XPATH, "//span[contains(text(), 'Builder')]")
      if styling_btn_text.is_displayed():
        styling_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[@title='Builder']")))
        styling_btn.click()
        print('Hello from FPanel Builder')
      else:
        styling_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[@title='Builder']")))
        styling_btn.click()
    except TimeoutException as e:
      right_panel = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@title='Right Side Panel']"))) 
      right_panel.click()
      styling_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[@title='Builder']")))
      styling_btn.click()



# Containers Functions

def fpanel(name, css_class):
    # Select Add button +
    try:
        add_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@title='Add']"))) 
        add_btn.click()
    except (ElementClickInterceptedException, TimeoutException) as e:
        add_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@title='Add']"))) 
        add_btn.click()

    # Select Containers
    try:
        containers = wait.until(EC.element_to_be_clickable((By.XPATH, "//li[@title='Containers' and @role='menuitem']"))) 
        containers.click()
    except (ElementClickInterceptedException, TimeoutException) as e:
        containers = wait.until(EC.element_to_be_clickable((By.XPATH, "//li[@title='Containers' and @role='menuitem']"))) 
        containers.click()

    # Select Second Drop Down to select FPanel
    try:
        flow_layout_panel = wait.until(EC.element_to_be_clickable((By.XPATH, "//li[@title='Flow Layout Panel' and @role='menuitem']"))) 
        flow_layout_panel.click()
    except (ElementClickInterceptedException, TimeoutException) as e:
        flow_layout_panel = wait.until(EC.element_to_be_clickable((By.XPATH, "//li[@title='Flow Layout Panel' and @role='menuitem']"))) 
        flow_layout_panel.click()

    right_panel_handler('Styling')

    try:
        change_name = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Enter text'][1]")))
        change_name.clear()
        change_name.send_keys(name + Keys.ENTER)

    except TimeoutException as e:
        change_name = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Enter text'][1]")))
        change_name.clear()
        change_name.send_keys(name + Keys.ENTER)

    # //input[@placeholder='Enter a class name (overwrites global default class)'][1]
    try:
        css_class_name = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Enter a class name (overwrites global default class)'][1]")))
        css_class_name.clear()
        css_class_name.send_keys(css_class + Keys.ENTER)
    except TimeoutException as e:
        css_class_name = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Enter a class name (overwrites global default class)'][1]")))
        css_class_name.clear()
        css_class_name.send_keys(css_class + Keys.ENTER)


def panel(name, css_class):
    #Panel

    # Select Add button +
    try:
        add_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@title='Add' and @class='sapEpmUiButton']"))) 
        add_btn.click()

    except (ElementClickInterceptedException, TimeoutException) as e:
        add_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@title='Add' and @class='sapEpmUiButton']"))) 
        add_btn.click()

    # Select Containers
    try:
        containers = wait.until(EC.element_to_be_clickable((By.XPATH, "//li[@title='Containers' and @role='menuitem']"))) 
        containers.click()
    except (ElementClickInterceptedException, TimeoutException) as e:
        containers = wait.until(EC.element_to_be_clickable((By.XPATH, "//li[@title='Containers' and @role='menuitem']"))) 
        containers.click()

    # Select Containers
    try:
        panel = wait.until(EC.element_to_be_clickable((By.XPATH, "//li[@title='Panel' and @role='menuitem']"))) 
        panel.click()
    except (ElementClickInterceptedException, TimeoutException, StaleElementReferenceException) as e:
        panel = wait.until(EC.element_to_be_clickable((By.XPATH, "//li[@title='Panel' and @role='menuitem']"))) 
        panel.click()

    right_panel_handler('Styling')
    try:
        change_name = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Enter text'][1]")))
        change_name.clear()
    
        change_name.send_keys(name + Keys.ENTER)
    except (ElementClickInterceptedException, ElementNotInteractableException) as e:
        change_name = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "//input[@placeholder='Enter text'][1]")))
        change_name.clear()
        change_name.send_keys(name + Keys.ENTER)

    # //input[@placeholder='Enter a class name (overwrites global default class)'][1]
    try:
        css_class_name = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Enter a class name (overwrites global default class)'][1]")))
        css_class_name.clear()

        css_class_name.send_keys(css_class + Keys.ENTER)
    except ElementClickInterceptedException as e:
        css_class_name = wait.until(EC.element_to_be_clickable(By.CSS_SELECTOR, "//input[@placeholder='Enter a class name (overwrites global default class)'][1]"))
        css_class_name.clear()

        css_class_name.send_keys(css_class + Keys.ENTER)

def create_chart(vizType):
    chart_types = {
        'info/pie' : 'Pie (more)',
        'info/bar' : 'Bar/Column (comparison)',
        'info/stacked_bar' : 'Stacked Bar/Column (comparison)',
        'info/number' : 'Numeric Point (indicator)',
        'info/combinationEx' : 'Combination Column & Line (comparison)', # line and bar
        'info/column' : 'Bar/Column (comparison)', # column chart
        'info/bullet' : 'Stacked Bar/Column (comparison)',
        'info/stacked_column' : 'Stacked Bar/Column (comparison)',
        'info/treemap' : 'Tree Map (distribution)',
        'info/bubble' : 'Bubble (correlation)'
    }
    type_of_chart = chart_types[vizType]

    try:
        chart_icon = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@title='Chart']")))
        chart_icon.click()
    except TimeoutException as e:
        chart_icon = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@title='Chart']")))
        chart_icon.click()

    try:
        chart_type_dd = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@data-testid='customSelectSelectionDiv']")))
        chart_type_dd.click()
    except TimeoutException as e:
        chart_type_dd = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@data-testid='customSelectSelectionDiv']")))
        chart_type_dd.click()

    try:
        chart = wait.until(EC.element_to_be_clickable((By.XPATH, f"//span[@title='{type_of_chart}']")))
        chart.click()
    except TimeoutException as e:
        chart = wait.until(EC.element_to_be_clickable((By.XPATH, f"//span[@title='{type_of_chart}']")))
        chart.click()

    # Creating a chart automatically opens the right side pane in builder menu
    

   


xpath_size_selector = {
        'width' : "(//div[@role='combobox']//div[@role='presentation'])[1]",
        'height': "(//div[@role='combobox']//div[@role='presentation'])[2]",
        'left'  : "(//div[@role='combobox']//div[@role='presentation'])[3]",
        'right' : "(//div[@role='combobox']//div[@role='presentation'])[5]",
        'top'   : "(//div[@role='combobox']//div[@role='presentation'])[4]",
        'bottom': "(//div[@role='combobox']//div[@role='presentation'])[6]",
        'auto': "//li[@title='auto']"
        }

#   (//div[contains(@class, 'sapEpmUiDropDown')]//div[contains(@class, 'sapUiTfComboIcon')])[1]
# [1] = width 
# [2] = height 
# [3] = left 
# [4] = top 
# [5] = right 
# [6] = bottom
xpath_size_text = {
            'width' : "//label[@title='Width']/following-sibling::div//input",
            'height': "//label[@title='Height']/following-sibling::div//input",
            'left'  : "//label[@title='Left (X)']/following-sibling::div//input",
            'right' : "//label[@title='Right']/following-sibling::div//input",
            'top'   : "//label[@title='Top (Y)']/following-sibling::div//input",
            'bottom': "//label[@title='Bottom']/following-sibling::div//input"
}

def check_size(size):
    if int(size) <= 32:
        return 32
    else:
        return size


def change_size(dim, y):
    if dim in ['height', 'width']:
        y = check_size(y)
    try:
        x = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_size_text[dim])))
        x.clear()
        x.send_keys(str(y) + Keys.ENTER)
    except (StaleElementReferenceException, ElementClickInterceptedException, InvalidElementStateException) as e:
        x = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_size_text[dim])))
        x.clear()
        x.send_keys(str(y) + Keys.ENTER)


def select_auto(dim):
    try:
        wait.until(EC.element_to_be_clickable((By.XPATH, xpath_size_selector[dim]))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, xpath_size_selector['auto']))).click()
    except (TimeoutException, StaleElementReferenceException) as e:
        a = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_size_selector[dim])))
        a.click()
        b = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_size_selector['auto'])))
        b.click()
def sizing_for_elements_inside_panel(h, w, t, b, l, r):
    # Open the Right Panel
    right_panel_handler('Styling')
    if w == 'auto': #width
        select_auto('width')
        change_size('right', r)
        change_size('left', l)

    elif l == 'auto': #left
        select_auto('left')
        change_size('right', r)
        change_size('width', w)
        
    else:
        change_size('width', w)
        change_size('left', l)

    if h == 'auto': #height
        select_auto('height')
        # if b < 150:
        #     b=150
        change_size('bottom', b)
        change_size('top', t)

    elif t == 'auto': #top
        select_auto('top')
        change_size('bottom', b)
        change_size('height', h)

    else:
        change_size('height', h)
        change_size('top', t)


def sizing_for_elements_inside_fpanel(parent_name,element_name,css_class, h, w_s, w_m, w_l, w_xl):
    print("Inside FPanel", h, w_s, w_m, w_l, w_xl)
    
    right_panel_handler('Styling')
    change_name = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Enter text'][1]")))
    change_name.clear()
 
    change_name.send_keys(element_name + Keys.ENTER)
    
    # //input[@placeholder='Enter a class name (overwrites global default class)'][1]
    css_class_name = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Enter a class name (overwrites global default class)'][1]")))
    css_class_name.clear()

    css_class_name.send_keys(css_class + Keys.ENTER)

    xpath_size_selector = {
        'width' : "(//div[@role='combobox']//div[@role='presentation'])[1]",
        'height': "(//div[@role='combobox']//div[@role='presentation'])[2]"
        }
    
    xpath_size_text = {
            'width' : "//label[@title='Width']/following-sibling::div//input",
            'height': "//label[@title='Height']/following-sibling::div//input"
    }

    # Height and width will be 384 px 
    # or in other words, both will always be in px

    # ------------ as they are already in px, we don't need the below code 
    # wait.until(EC.element_to_be_clickable((By.XPATH, xpath_size_selector['height']))).click()
    # wait.until(EC.element_to_be_clickable((By.XPATH, xpath_size_selector['px']))).click()

    x = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_size_text['height'])))
    x.clear()
    x.send_keys(str(h) + Keys.ENTER)

    parent_selector = wait.until(EC.element_to_be_clickable((By.XPATH, f"//span[text() = '{parent_name}']"))) 
    parent_selector.click()
    parent_selector.click()
    
    #builder pane navigation
    right_panel_handler('Builder')

    # BREAKPOINT EDIT
    w_s = str(round((int(w_s) / 12) * 100, 2))
    w_m = str(round((int(w_m) / 12) * 100, 2))
    w_l = str(round((int(w_l) / 12) * 100, 2))
    w_xl = str(round((int(w_xl) / 12) * 100, 2))
    
    breakpoints = {
        '414' : w_s,
        '650' : w_m,
        '1200': w_l,
        '3000': w_xl
    }
    # breakpoints - given in the Lumira
        # s = 414
        # m = 640
        # l = 1024
        # xl = 1920
    # time.sleep(1)
    try:
        no_rule = driver.find_element(By.XPATH, "//label[contains(text(), 'No rule has been specified')]")
        # add a for loop to create 4 breakpoints
        time.sleep(5)
        if no_rule.is_displayed():
            temp, dd_num = 0, 1
            for key, value in breakpoints.items(): 
                print(key, value)
                temp += 1
                # (//input[@type='number'])[temp] ---- for screen width --- number is odd
                # (//input[@type='number'])[twmp] ---- for widget % ----- number is even
                try:
                    add_breakpoint = wait.until(EC.element_to_be_clickable((By.XPATH, "//bdi[contains(text(), 'Add Breakpoint')]")))
                    add_breakpoint.click()
                except TimeoutException as e:
                    add_breakpoint = wait.until(EC.element_to_be_clickable((By.XPATH, "//bdi[contains(text(), 'Add Breakpoint')]")))
                    add_breakpoint.click()

                screen_wid_text = driver.find_element(By.XPATH, f"(//input[@type='number'])[{temp}]")
                screen_wid_text.clear()
                screen_wid_text = driver.find_element(By.XPATH, f"(//input[@type='number'])[{temp}]")
                screen_wid_text.send_keys(key + Keys.ENTER)

                # (//div[@role='combobox'])[1] - Each Widget dropdown
                widget_name_dd = wait.until(EC.element_to_be_clickable((By.XPATH, f"(//div[@role='combobox'])[{dd_num}]")))
                widget_name_dd.click()

    
                wid_name_click = wait.until(EC.element_to_be_clickable((By.XPATH, f"//span[contains(text(), '{element_name}')]")))
                wid_name_click.click()
                dd_num += 1

                temp += 1
                widget_text_percent = wait.until(EC.element_to_be_clickable((By.XPATH, f"(//input[@type='number'])[{temp}]")))
                widget_text_percent.clear()
                widget_text_percent = wait.until(EC.element_to_be_clickable((By.XPATH, f"(//input[@type='number'])[{temp}]")))
                widget_text_percent.send_keys(value + Keys.ENTER)

        print('First Breakpoint Added Successfully')

        # Check the closing and opening of the right side pane once again
    except NoSuchElementException:
        time.sleep(5)
        # Counting number of text boxes that is present already in the breakpoint pane
        text_boxes = driver.find_elements(By.XPATH, '//input[@type="number"]')
        count_text_boxes = len(text_boxes)
        print('No. of text boxes in the breakpoint pane', count_text_boxes)
        dd_box = driver.find_elements(By.XPATH, "(//div[@class='sapFpaAppBuildingBreakPointEntrySetting']//div[@role='combobox'])")
        count_dd_box = len(dd_box)
        print('No. of dropdown boxes in the breakpoint pane', count_dd_box)
        print('Element Name', element_name)


        # temp = text box, dd_num = element selection dropdown, widget = add widget button
        temp, dd_num, widget = 0, 0, 1
        text_new = ((count_text_boxes - 8)//4) + 3
        widget_new = 2      # Always 2, Because add widget index is 1, 3, 5, 7 for all cases
        dd_new = round(count_dd_box/4) + 1
        for key, value in breakpoints.items():
            # We don't need to add breakpoint every time, so we are skipping it
            
            # 1, 3, 5, 7 for add_widget
            try:
                add_widget = wait.until(EC.element_to_be_clickable((By.XPATH, f"(//bdi[contains(text(), 'Add Widget')])[{widget}]")))
                add_widget.click()
            except (TimeoutException, ElementClickInterceptedException) as e:
                add_widget = wait.until(EC.element_to_be_clickable((By.XPATH, f"(//bdi[contains(text(), 'Add Widget')])[{widget}]")))
                add_widget.click()

            widget += widget_new

            dd_num += dd_new
            # (//div[@role='combobox'])[1] - Each Widget dropdown
            try:
                widget_name_dd = wait.until(EC.element_to_be_clickable((By.XPATH, f"(//div[@role='combobox'])[{dd_num}]")))
                widget_name_dd.click()
            except (TimeoutException, ElementClickInterceptedException) as e:
                widget_name_dd = wait.until(EC.element_to_be_clickable((By.XPATH, f"(//div[@role='combobox'])[{dd_num}]")))
                widget_name_dd.click()

            try:
                wid_name_click = wait.until(EC.element_to_be_clickable((By.XPATH, f"//span[text() = '{element_name}']")))
                wid_name_click.click()
            except (TimeoutException, ElementClickInterceptedException) as e:
                wid_name_click = wait.until(EC.element_to_be_clickable((By.XPATH, f"//span[text() = '{element_name}']")))
                wid_name_click.click()


            temp += text_new
            widget_text_percent = wait.until(EC.element_to_be_clickable((By.XPATH, f"(//input[@type='number'])[{temp}]")))
            widget_text_percent.clear()
            widget_text_percent = wait.until(EC.element_to_be_clickable((By.XPATH, f"(//input[@type='number'])[{temp}]")))
            widget_text_percent.send_keys(value + Keys.ENTER)


        print('Existing Breakpoint Added Successfully')
def change_name(name, css_class):

    right_panel_handler('Styling')
    try:
        change_name = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Enter text'][1]")))
        change_name.clear()

        change_name.send_keys(name + Keys.ENTER)
    except (TimeoutException, StaleElementReferenceException, ElementClickInterceptedException) as e:
        change_name = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Enter text'][1]")))
        change_name.clear()

        change_name.send_keys(name + Keys.ENTER)
    # //input[@placeholder='Enter a class name (overwrites global default class)'][1]
    try:
        css_class_name = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Enter a class name (overwrites global default class)'][1]")))
        css_class_name.clear()

        css_class_name.send_keys(css_class + Keys.ENTER)
    except TimeoutException as e:
        css_class_name = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Enter a class name (overwrites global default class)'][1]")))
        css_class_name.clear()

        css_class_name.send_keys(css_class + Keys.ENTER)


def text_component(content):
    # Select Add button +
    add_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@title='Add']"))) 
    add_btn.click()

    # Select Button Component
    text_box = wait.until(EC.element_to_be_clickable((By.XPATH, "//li[@title='Text' and @role='menuitem']"))) 
    text_box.click()

    
    div_element = wait.until(
    EC.presence_of_element_located((By.XPATH, "(//div[@contenteditable='true'])[2]"))
    )
    p_element = wait.until(
    EC.presence_of_element_located((By.TAG_NAME, 'p'))
    )
    try:
        p_element = div_element.find_element(By.XPATH, ".//p")  # Look for <p> anywhere inside

        p_element.clear()  # Clear existing text if needed
        p_element.send_keys(content)  # Set new content
    except (StaleElementReferenceException, TimeoutException, NoSuchElementException) as e:
        div_element = wait.until(
            EC.presence_of_element_located((By.XPATH, "(//div[@contenteditable='true'])[2]"))
        )

        # Use JavaScript to set the content of the <p> element
        driver.execute_script("""
            var pElement = arguments[0].querySelector('p');
            if (pElement) {
                pElement.innerHTML = arguments[1];
            }
        """, div_element, content)

def start(model_name):# Initialize Lumira instance with XML file
    lumira_instance = Lumira(f'lumira_files/content.xml')

    # Build component tree
    lumira_instance.build_component_tree()

    # Extract component properties
    lumira_instance.extract_component_properties()

    # Print component tree with parent-child relationships
    # print("Component Tree with Parent-Child Relationships:")
    # lumira_instance.print_component_tree()


    # Call SAC method
    res = lumira_instance.call_sac()
    pbar = st.progress(0, text="Converting Dashboard to SAC")

    # STARTTT
    start_sac_screen(model_name)
    key_value = {}
    per_per_ele = 100/len(res)
    per = 0
    for i in res:
        # print(i['Name'])
        per += per_per_ele
        if per < 99:
            pbar.progress(int(per), text=f"Converting {i['Name']} - {str(round(int(per), 2))}%")
        if i['Type'] == 'ABSOLUTE_LAYOUT_COMPONENT':
            page_name = i['Name']
            # Open Right Panel
            
            right_panel_handler('Styling')

            try:
                page_selector = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[@class='subTitle' and text() = 'Page_1']"))) 
                page_selector.click()
            except TimeoutException as e:
                page_selector = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[@class='subTitle' and text() = 'Page_1']"))) 
                page_selector.click()

            try:
                page_title = wait.until(EC.element_to_be_clickable((By.XPATH, "(//input[@placeholder='Enter text'])[1]"))) 
                page_title.click()
                page_title.clear()
                page_title.send_keys(page_name + Keys.ENTER)
            except TimeoutException as e:
                page_title = wait.until(EC.element_to_be_clickable((By.XPATH, "(//input[@placeholder='Enter text'])[1]"))) 
                page_title.click()
                page_title.clear()
                page_title.send_keys(page_name + Keys.ENTER)


            try:
                page_id = wait.until(EC.element_to_be_clickable((By.XPATH, "(//input[@placeholder='Enter text'])[2]"))) 
                page_id.click()
                page_id.clear()
                page_id.send_keys(page_name + Keys.ENTER)

            except TimeoutException as e:
                page_id = wait.until(EC.element_to_be_clickable((By.XPATH, "(//input[@placeholder='Enter text'])[2]"))) 
                page_id.click()
                page_id.clear()
                page_id.send_keys(page_name + Keys.ENTER)

        elif i['Type'] == 'ADAPTIVE_LAYOUT_COMPONENT':
            css_class = i.get('CSS_CLASS', '')
            parent_selector(i['Parent_Name'])
            fpanel(i['Name'], css_class)
            if i['Parent_Type'] == 'PANEL_COMPONENT' or i['Parent_Type'] == 'BLOCK_COMPONENT' or i['Parent_Type'] == None:
                h = i.get('HEIGHT', 'auto')
                w = i.get('WIDTH', 'auto')
                t = i.get('TOP_MARGIN', 'auto')
                b = i.get('BOTTOM_MARGIN', 'auto')
                l = i.get('LEFT_MARGIN', 'auto')
                r = i.get('RIGHT_MARGIN', '5')
                print((h, w, t, b, l, r))
                sizing_for_elements_inside_panel(h, w, t, b, l, r)
                
            elif i['Parent_Type'] == 'ADAPTIVE_LAYOUT_COMPONENT':
                h = i.get('HEIGHT', '150')
                w_s = i['COL_SPAN_S']
                w_m = i['COL_SPAN_M']
                w_l = i['COL_SPAN_L']
                w_xl = i['COL_SPAN_XL']
                sizing_for_elements_inside_fpanel(i['Parent_Name'], i['Name'], css_class, h, w_s, w_m, w_l, w_xl)
            
        elif i['Type'] == 'PANEL_COMPONENT' or i['Type'] == 'BLOCK_COMPONENT':
            css_class = i.get('CSS_CLASS', '')
            parent_selector(i['Parent_Name'])
            panel(i['Name'], css_class)
            # The below case does not work for parent type = None or parent = Root
            if i['Parent_Type'] == 'PANEL_COMPONENT' or i['Parent_Type'] == 'BLOCK_COMPONENT' or i['Parent_Type'] == None:
                h = i.get('HEIGHT', 'auto')
                w = i.get('WIDTH', 'auto')
                t = i.get('TOP_MARGIN', 'auto')
                b = i.get('BOTTOM_MARGIN', 'auto')
                l = i.get('LEFT_MARGIN', 'auto')
                r = i.get('RIGHT_MARGIN', 'auto')
                print((h, w, t, b, l, r))
                sizing_for_elements_inside_panel(h, w, t, b, l, r)
                
            elif i['Parent_Type'] == 'ADAPTIVE_LAYOUT_COMPONENT':
                h = i.get('HEIGHT', '150')
                w_s = i['COL_SPAN_S']
                w_m = i['COL_SPAN_M']
                w_l = i['COL_SPAN_L']
                w_xl = i['COL_SPAN_XL']
                sizing_for_elements_inside_fpanel(i['Parent_Name'], i['Name'], css_class, h, w_s, w_m, w_l, w_xl)

        elif i['Type'] == 'com_sap_ip_bi_VizFrame' and i['vizType'] == 'info/bar':
            name = i['Name']
            css_class = i.get('CSS_CLASS', '')

            feed_items = json.loads(i['feedItems'])
            filter_data = json.loads(i.get('data', '[]')) if isinstance(i.get('data', '[]'), str) else i.get('data', [])


            # feed_items[0] = dimension
            # feed_items[1] = color
            # feed_items[2] = measure
            # all the above three are in dictionary
            

            dime = []
            meas = []
            color = []
            updated_filter = {}

            # Dimension
            dim_list = feed_items[0]['values']

            for val in dim_list:
                dime.append(val['name'])
                key_value[val['id']] = val['name']

            # Measure
            meas_list = feed_items[2]['values']   
            for val in meas_list:
                meas.append(val['name'])
                key_value[val['id']] = val['name']

            # Color
            color_list = feed_items[1]['values']
            for val in color_list:
                color.append(val['name'])
                key_value[val['id']] = val['name']

            print(name, dime, meas, filter_data, [h, w, t, b, l, r])
            parent_selector(i['Parent_Name'])
            create_chart(i['vizType'])

            # data-testid="valueAxis"  ------------ Measure
            try:
                measure = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@data-testid='valueAxis']")))
                measure.click()
            except (ElementClickInterceptedException, TimeoutException) as e:
                measure = driver.find_element(By.XPATH, "//div[@data-testid='valueAxis']")
                measure.click()

            for key_figure in meas:
                try:
                    measure_value = wait.until(EC.element_to_be_clickable((By.XPATH, f"//span[text() = '{key_figure}']")))
                    measure_value.click()
                except (ElementClickInterceptedException, TimeoutException) as e:
                    measure_value = driver.find_element(By.XPATH, f"//span[text() = '{key_figure}']")
                    measure_value.click()

            # to click outside to remove the popup of dimension or measure selection
            try:
                element = driver.find_element(By.ID, 'simple-popover')
                element.click()
            except (ElementClickInterceptedException, TimeoutException) as e:
                element = driver.find_element(By.ID, 'simple-popover')
                element.click()


            # data-testid="categoryAxis" -------------- Dimension
            try:
                dimension = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Add Dimension')]")))
                dimension.click()
            except (ElementClickInterceptedException, TimeoutException) as e:
                dimension = driver.find_element(By.XPATH, "//span[contains(text(), 'Add Dimension')]")
                dimension.click()

            for dim_value in dime:
                try:
                    x = wait.until(EC.element_to_be_clickable((By.XPATH, f"//input[@type='checkbox' and @value='{dim_value}']")))
                    x.click()
                except (ElementClickInterceptedException, TimeoutException) as e:
                    x = driver.find_element(By.XPATH, f"//input[@type='checkbox' and @value='{dim_value}']")
                    x.click()

            # to click outside to remove the popup of dimension or measure selection
            try:
                element = driver.find_element(By.ID, 'simple-popover')
                element.click()
            except (ElementClickInterceptedException, TimeoutException) as e:
                element = driver.find_element(By.ID, 'simple-popover')
                element.click()

            right_panel_handler('Styling')
            change_name(name, css_class)
            
            #  # The pane will be in builder pane once we create a chart and it will automatically open in builder even if styling pane is opened
            if i['Parent_Type'] == 'PANEL_COMPONENT' or i['Parent_Type'] == 'BLOCK_COMPONENT':
                h = i.get('HEIGHT', 'auto')
                w = i.get('WIDTH', 'auto')
                t = i.get('TOP_MARGIN', 'auto')
                b = i.get('BOTTOM_MARGIN', 'auto')
                l = i.get('LEFT_MARGIN', 'auto')
                r = i.get('RIGHT_MARGIN', 'auto')
                sizing_for_elements_inside_panel(h, w, t, b, l, r)
            elif i['Parent_Type'] == 'ADAPTIVE_LAYOUT_COMPONENT':
                h = i.get('HEIGHT', '300')
                w_s = i['COL_SPAN_S']
                w_m = i['COL_SPAN_M']
                w_l = i['COL_SPAN_L']
                w_xl = i['COL_SPAN_XL']
                
                sizing_for_elements_inside_fpanel(i['Parent_Name'], i['Name'], css_class, h, w_s, w_m, w_l, w_xl)

        elif i['Type'] == 'com_sap_ip_bi_VizFrame' and i['vizType'] == 'info/column':
            name = i['Name']
            css_class = i.get('CSS_CLASS', '')
            feed_items = json.loads(i['feedItems'])
            filter_data = json.loads(i.get('data', '[]')) if isinstance(i.get('data', '[]'), str) else i.get('data', [])


            # feed_items[0] = dimension
            # feed_items[1] = color
            # feed_items[2] = measure
            # all the above three are in dictionary
            

            dime = []
            meas = []
            color = []
            updated_filter = {}

            # Dimension
            dim_list = feed_items[0]['values']

            for val in dim_list:
                dime.append(val['name'])
                key_value[val['id']] = val['name']

            # Measure
            meas_list = feed_items[2]['values']   
            for val in meas_list:
                meas.append(val['name'])
                key_value[val['id']] = val['name']

            # Color
            color_list = feed_items[1]['values']
            for val in color_list:
                color.append(val['name'])
                key_value[val['id']] = val['name']

        # print(name, dime, meas, filter_data, [h, w, t, b, l, r])
            parent_selector(i['Parent_Name'])
            create_chart(i['vizType'])

            # Changing the chart orientation to vertical for the column chart

            try:
                orientation = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@type='text' and @value='Horizontal' and @placeholder='Select an option']")))
                orientation.click()
            except (ElementClickInterceptedException, TimeoutException) as e:
                orientation = driver.find_element(By.XPATH, "//input[@type='text' and @value='Horizontal' and @placeholder='Select an option']")
                orientation.click()

            try:
                vertical = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Vertical')]")))
                vertical.click()

            except (ElementClickInterceptedException, TimeoutException) as e:
                vertical = driver.find_element(By.XPATH, "//span[contains(text(), 'Vertical')]")
                vertical.click()

            # data-testid="valueAxis"  ------------ Measure
            try:
                measure = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@data-testid='valueAxis']")))
                measure.click()

            except (ElementClickInterceptedException, TimeoutException) as e:
                measure = driver.find_element(By.XPATH, "//div[@data-testid='valueAxis']")
                measure.click()

            for key_figure in meas:
                try:
                    measure_value = wait.until(EC.element_to_be_clickable((By.XPATH, f"//span[text() = '{key_figure}' and not(parent::p)]")))
                    measure_value.click()
                except (ElementClickInterceptedException, TimeoutException) as e:
                    measure_value = driver.find_element(By.XPATH, f"//span[text() = '{key_figure}' and not(parent::p)]")
                    measure_value.click()

            # to click outside to remove the popup of dimension or measure selection
            try:
                element = driver.find_element(By.ID, 'simple-popover')
                element.click()
            except (ElementClickInterceptedException, TimeoutException) as e:
                element = driver.find_element(By.ID, 'simple-popover')
                element.click()


            # data-testid="categoryAxis" -------------- Dimension
            try:
                dimension = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Add Dimension')]")))
                dimension.click()
            except (ElementClickInterceptedException, TimeoutException) as e:
                dimension = driver.find_element(By.XPATH, "//span[contains(text(), 'Add Dimension')]")
                dimension.click()

            # for dim_value in dime:
            #     x = driver.find_element(By.XPATH, f"//input[@type='checkbox' and @value='{dim_value}']")
            #     x.click()

            for dim_value in dime:
                dim_value = dim_value.replace(' ', '_')
                try:
                    print(dim_value)
                    x = wait.until(EC.element_to_be_clickable((By.XPATH, f"//input[@type='checkbox' and @value='{dim_value}']")))
                    x.click()
                except (ElementClickInterceptedException, TimeoutException) as e:
                    print(dim_value)
                    x = driver.find_element(By.XPATH, f"//input[@type='checkbox' and @value='{dim_value}']")
                    x.click()

            # to click outside to remove the popup of dimension or measure selection
            try:
                element = driver.find_element(By.ID, 'simple-popover')
                element.click()
            except (ElementClickInterceptedException, TimeoutException) as e:
                element = driver.find_element(By.ID, 'simple-popover')
                element.click()

            right_panel_handler('Styling')

            change_name(name, css_class)
            if i['Parent_Type'] == 'PANEL_COMPONENT' or i['Parent_Type'] == 'BLOCK_COMPONENT':
                h = i.get('HEIGHT', 'auto')
                w = i.get('WIDTH', 'auto')
                t = i.get('TOP_MARGIN', 'auto')
                b = i.get('BOTTOM_MARGIN', 'auto')
                l = i.get('LEFT_MARGIN', 'auto')
                r = i.get('RIGHT_MARGIN', 'auto')
                sizing_for_elements_inside_panel(h, w, t, b, l, r)
            elif i['Parent_Type'] == 'ADAPTIVE_LAYOUT_COMPONENT':
                h = i.get('HEIGHT', '300')

                w_s = i['COL_SPAN_S']
                w_m = i['COL_SPAN_M']
                w_l = i['COL_SPAN_L']
                w_xl = i['COL_SPAN_XL']
                
                sizing_for_elements_inside_fpanel(i['Parent_Name'], i['Name'], css_class, h, w_s, w_m, w_l, w_xl)
            #  # The pane will be in builder pane once we create a chart and it will automatically open in builder even if styling pane is opened
            # if i['Parent_Type'] == 'PANEL_COMPONENT':
            #     # h = i.get('HEIGHT', 'auto')
            #     # w = i.get('WIDTH', 'auto')
            #     # t = i.get('TOP_MARGIN', 'auto')
            #     # b = i.get('BOTTOM_MARGIN', 'auto')
            #     # l = i.get('LEFT_MARGIN', 'auto')
            #     # r = i.get('RIGHT_MARGIN', 'auto')
            #     h = 'auto'
            #     w = 'auto'
            #     t = '0'
            #     b = '0'
            #     l = '0'
            #     r = '0'
            #     print((h, w, t, b, l, r))
                
            #     # Add Name and CSS Class
            #     sizing_for_elements_inside_panel(h, w, t, b, l, r)
            #     # Grandparent Selector
            #     grand_parent_name = find_grand_parent(i['Parent_Name'])
            #     grand_parent_selector = wait.until(EC.element_to_be_clickable((By.XPATH, f"//span[text() = '{grand_parent_name}']"))) 
            #     grand_parent_selector.click()
            #     grand_parent_selector.click()
            #     right_panel_handler('Styling')
            #     # parent_selector = wait.until(EC.element_to_be_clickable((By.XPATH, f"//span[text() = '{parent_name}']"))) 
            #     # parent_selector.click()
            #     # parent_selector.click()

            #     # change height to 350
            #     # try:
            #     #     wait.until(EC.element_to_be_clickable((By.XPATH, xpath_size_selector['height']))).click()
            #     #     wait.until(EC.element_to_be_clickable((By.XPATH, xpath_size_selector['px']))).click()
            #     # except TimeoutException as e:
            #     #     a = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_size_selector['height'])))
            #     #     a.click()
            #     #     b = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_size_selector['px'])))
            #     #     b.click()

            #     try:
            #         x = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_size_text['height'])))
            #         x.clear()
            #         x.send_keys(str(350) + Keys.ENTER)
            #     except (StaleElementReferenceException, ElementClickInterceptedException) as e:
            #         x = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_size_text['height'])))
            #         x.clear()
            #         x.send_keys(str(350) + Keys.ENTER)


            # elif i['Parent_Type'] == 'BLOCK_COMPONENT':
            #     h = 'auto'
            #     w = 'auto'
            #     t = '0'
            #     b = '0'
            #     l = '0'
            #     r = '0'
            #     print((h, w, t, b, l, r))
                
            #     # Add Name and CSS Class
            #     sizing_for_elements_inside_panel(h, w, t, b, l, r)

            #     parent_name = i['Parent_Name']
            #     parent_selector = wait.until(EC.element_to_be_clickable((By.XPATH, f"//span[text() = '{parent_name}']"))) 
            #     parent_selector.click()
            #     parent_selector.click()
            #     # change height to 350
            #     try:
            #         x = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_size_text['height'])))
            #         x.clear()
            #         x.send_keys(str(350) + Keys.ENTER)
            #     except (StaleElementReferenceException, ElementClickInterceptedException) as e:
            #         x = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_size_text['height'])))
            #         x.clear()
            #         x.send_keys(str(350) + Keys.ENTER)


        elif i['Type'] == 'com_sap_ip_bi_VizFrame' and i['vizType'] == 'info/pie':
            name = i['Name']
            css_class = i.get('CSS_CLASS', '')
            feed_items = json.loads(i['feedItems'])
            filter_data = json.loads(i.get('data', '[]')) if isinstance(i.get('data', '[]'), str) else i.get('data', [])

            
            # len(feedItems) = 2 -----------> 
            # [0] = Measure ----------> There will always be only one measure
            # [1] = Color (As in Dimension) can be more

            
            # Measure
            meas = feed_items[0]['values'][0]['name']
            color_dime = []
            updated_filter = {}


            # Color
            color_list = feed_items[1]['values']
            for val in color_list:
                color_dime.append(val['name'])
                key_value[val['id']] = val['name']

            # # print(name, meas, filter_data, [h, w, t, b, l, r])


            parent_selector(i['Parent_Name'])
            create_chart(i['vizType'])

            # data-testid="valueAxis"  ------------ Measure
            try:
                measure = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'At least 1 Measure required')]")))
                measure.click()
            except (ElementClickInterceptedException, TimeoutException) as e:
                measure = driver.find_element(By.XPATH, "//span[contains(text(), 'At least 1 Measure required')]")
                measure.click()

            try:
                measure_value = wait.until(EC.element_to_be_clickable((By.XPATH, f"//p[text() = '{meas}']")))
                measure_value.click()
            except (ElementClickInterceptedException, TimeoutException) as e:
                measure_value = driver.find_element(By.XPATH, f"//p[text() = '{meas}']")
                measure_value.click()


            # data-testid="categoryAxis" -------------- Dimension
            try:
                color = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'At least 1 Dimension required')]")))
                color.click()
            except (ElementClickInterceptedException, TimeoutException) as e:
                color = driver.find_element(By.XPATH, "//span[contains(text(), 'At least 1 Dimension required')]")
                color.click()

            for dim_value in color_dime:
                try:
                    x = wait.until(EC.element_to_be_clickable((By.XPATH, f"//input[@type='checkbox' and @value='{dim_value}']")))
                    x.click()
                except (ElementClickInterceptedException, TimeoutException) as e:
                    x = driver.find_element(By.XPATH, f"//input[@type='checkbox' and @value='{dim_value}']")
                    x.click()


            # to click outside to remove the popup of dimension or measure selection
            try:
                element = driver.find_element(By.ID, 'simple-popover')
                element.click()
            except (ElementClickInterceptedException, TimeoutException) as e:
                element = driver.find_element(By.ID, 'simple-popover')
                element.click()

            #  # The pane will be in builder pane once we create a chart and it will automatically open in builder even if styling pane is opened
            #styling menu navigation
            right_panel_handler('Styling')

            change_name(name, css_class)
            if i['Parent_Type'] == 'PANEL_COMPONENT' or i['Parent_Type'] == 'BLOCK_COMPONENT':
                h = i.get('HEIGHT', 'auto')
                w = i.get('WIDTH', 'auto')
                t = i.get('TOP_MARGIN', 'auto')
                b = i.get('BOTTOM_MARGIN', 'auto')
                l = i.get('LEFT_MARGIN', 'auto')
                r = i.get('RIGHT_MARGIN', 'auto')
                sizing_for_elements_inside_panel(h, w, t, b, l, r)
            elif i['Parent_Type'] == 'ADAPTIVE_LAYOUT_COMPONENT':
                h = i.get('HEIGHT', '300')
                w_s = i['COL_SPAN_S']
                w_m = i['COL_SPAN_M']
                w_l = i['COL_SPAN_L']
                w_xl = i['COL_SPAN_XL']
                
                sizing_for_elements_inside_fpanel(i['Parent_Name'], i['Name'], css_class, h, w_s, w_m, w_l, w_xl)
            # if i['Parent_Type'] == 'PANEL_COMPONENT':
            #     # h = i.get('HEIGHT', 'auto')
            #     # w = i.get('WIDTH', 'auto')
            #     # t = i.get('TOP_MARGIN', 'auto')
            #     # b = i.get('BOTTOM_MARGIN', 'auto')
            #     # l = i.get('LEFT_MARGIN', 'auto')
            #     # r = i.get('RIGHT_MARGIN', 'auto')
            #     h = 'auto'
            #     w = 'auto'
            #     t = '0'
            #     b = '0'
            #     l = '0'
            #     r = '0'
            #     print((h, w, t, b, l, r))
                
            #     # Add Name and CSS Class
            #     sizing_for_elements_inside_panel(h, w, t, b, l, r)
            #     # Grandparent Selector
            #     grand_parent_name = find_grand_parent(i['Parent_Name'])
            #     grand_parent_selector = wait.until(EC.element_to_be_clickable((By.XPATH, f"//span[text() = '{grand_parent_name}']"))) 
            #     grand_parent_selector.click()
            #     grand_parent_selector.click()
            #     right_panel_handler('Styling')
            #     # parent_selector = wait.until(EC.element_to_be_clickable((By.XPATH, f"//span[text() = '{parent_name}']"))) 
            #     # parent_selector.click()
            #     # parent_selector.click()

            #     # change height to 350
            #     # try:
            #     #     wait.until(EC.element_to_be_clickable((By.XPATH, xpath_size_selector['height']))).click()
            #     #     wait.until(EC.element_to_be_clickable((By.XPATH, xpath_size_selector['px']))).click()
            #     # except TimeoutException as e:
            #     #     a = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_size_selector['height'])))
            #     #     a.click()
            #     #     b = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_size_selector['px'])))
            #     #     b.click()

            #     try:
            #         x = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_size_text['height'])))
            #         x.clear()
            #         x.send_keys(str(350) + Keys.ENTER)
            #     except (StaleElementReferenceException, ElementClickInterceptedException) as e:
            #         x = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_size_text['height'])))
            #         x.clear()
            #         x.send_keys(str(350) + Keys.ENTER)


            # elif i['Parent_Type'] == 'BLOCK_COMPONENT':
            #     h = 'auto'
            #     w = 'auto'
            #     t = '0'
            #     b = '0'
            #     l = '0'
            #     r = '0'
            #     print((h, w, t, b, l, r))
                
            #     # Add Name and CSS Class
            #     sizing_for_elements_inside_panel(h, w, t, b, l, r)

            #     parent_name = i['Parent_Name']
            #     parent_selector = wait.until(EC.element_to_be_clickable((By.XPATH, f"//span[text() = '{parent_name}']"))) 
            #     parent_selector.click()
            #     parent_selector.click()
            #     # change height to 350
            #     try:
            #         x = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_size_text['height'])))
            #         x.clear()
            #         x.send_keys(str(350) + Keys.ENTER)
            #     except (StaleElementReferenceException, ElementClickInterceptedException) as e:
            #         x = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_size_text['height'])))
            #         x.clear()
            #         x.send_keys(str(350) + Keys.ENTER)

        elif i['Type'] == 'com_sap_ip_bi_VizFrame' and i['vizType'] == 'info/treemap':
            name = i['Name']
            css_class = i.get('CSS_CLASS', '')
            
            feed_items = json.loads(i['feedItems'])
            filter_data = json.loads(i.get('data', '[]')) if isinstance(i.get('data', '[]'), str) else i.get('data', [])


            # feed_items[0] = dimension - can be one or more
            # feed_items[1] = color - only one
            # feed_items[2] = measure (weight - size) only one
            # all the above three are in dictionary
            

            dime = []
            meas = []
            color = []
            updated_filter = {}

            # Dimension
            dim_list = feed_items[0]['values']

            for val in dim_list:
                dime.append(val['name'])
                key_value[val['id']] = val['name']

            # Measure
            meas = feed_items[2]['values'][0]['name']

            # Color
            color_list = feed_items[1]['values'][0]['name']
            

            # # print(name, dime, meas, filter_data, [h, w, t, b, l, r])
            parent_selector(i['Parent_Name'])
            create_chart(i['vizType'])

            # data-testid="valueAxis"  ------------ Measure
            try:
                measure = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'At least 1 Measure required')]")))
                measure.click()
            except (ElementClickInterceptedException, TimeoutException) as e:
                measure = driver.find_element(By.XPATH, "//span[contains(text(), 'At least 1 Measure required')]")
                measure.click()

            # Size (only one value)
            try:
                measure_value = wait.until(EC.element_to_be_clickable((By.XPATH, f"//p[contains(text(), '{meas}')]")))
                measure_value.click()
            except (ElementClickInterceptedException, TimeoutException) as e:
                measure_value = driver.find_element(By.XPATH, f"//p[contains(text(), '{meas}')]")
                measure_value.click()

            # to click outside to remove the popup of dimension or measure selection
            # this below code is not required as it automatically closes the measure selection popup
            # element = driver.find_element(By.ID, 'simple-popover')
            # element.click()


            # data-testid="categoryAxis" -------------- Dimension
            try:
                dimension = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'At least 1 Dimension required')]")))
                dimension.click()
            except (ElementClickInterceptedException, TimeoutException) as e:
                dimension = driver.find_element(By.XPATH, "//span[contains(text(), 'At least 1 Dimension required')]")
                dimension.click()

            for dim_value in dime:
                try:
                    x = wait.until(EC.element_to_be_clickable((By.XPATH, f"//input[@type='checkbox' and @value='{dim_value}']")))
                    x.click()
                except (NoSuchElementException, ElementClickInterceptedException, TimeoutException) as e:
                    x = driver.find_element(By.XPATH, f"//input[@type='checkbox' and @value='{dim_value}']")
                    x.click()

            # to click outside to remove the popup of dimension or measure selection
            try:
                element = driver.find_element(By.ID, 'simple-popover')
                element.click()
            except (ElementClickInterceptedException, TimeoutException) as e:
                element = driver.find_element(By.ID, 'simple-popover')
                element.click()

            try:
                add_measure_color = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Add Measure')]")))
                add_measure_color.click()
            except (ElementClickInterceptedException, TimeoutException) as e:
                add_measure_color = driver.find_element(By.XPATH, "//span[contains(text(), 'Add Measure')]")
                add_measure_color.click()

            try:
                color_value = wait.until(EC.element_to_be_clickable((By.XPATH, f"//p[contains(text(), '{color_list}')]")))
                color_value.click()

            except (ElementClickInterceptedException, TimeoutException) as e:
                color_value = driver.find_element(By.XPATH, f"//p[contains(text(), '{color_list}')]")
                color_value.click()
            #  # The pane will be in builder pane once we create a chart and it will automatically open in builder even if styling pane is opened

            right_panel_handler('Styling')

            change_name(name, css_class)

            if i['Parent_Type'] == 'PANEL_COMPONENT' or i['Parent_Type'] == 'BLOCK_COMPONENT':
                h = i.get('HEIGHT', 'auto')
                w = i.get('WIDTH', 'auto')
                t = i.get('TOP_MARGIN', 'auto')
                b = i.get('BOTTOM_MARGIN', 'auto')
                l = i.get('LEFT_MARGIN', 'auto')
                r = i.get('RIGHT_MARGIN', 'auto')
                sizing_for_elements_inside_panel(h, w, t, b, l, r)
            elif i['Parent_Type'] == 'ADAPTIVE_LAYOUT_COMPONENT':
                h = i.get('HEIGHT', '300')
                w_s = i['COL_SPAN_S']
                w_m = i['COL_SPAN_M']
                w_l = i['COL_SPAN_L']
                w_xl = i['COL_SPAN_XL']
                
                sizing_for_elements_inside_fpanel(i['Parent_Name'], i['Name'], css_class, h, w_s, w_m, w_l, w_xl)
            # if i['Parent_Type'] == 'PANEL_COMPONENT':
            #     # h = i.get('HEIGHT', 'auto')
            #     # w = i.get('WIDTH', 'auto')
            #     # t = i.get('TOP_MARGIN', 'auto')
            #     # b = i.get('BOTTOM_MARGIN', 'auto')
            #     # l = i.get('LEFT_MARGIN', 'auto')
            #     # r = i.get('RIGHT_MARGIN', 'auto')
            #     h = 'auto'
            #     w = 'auto'
            #     t = '0'
            #     b = '0'
            #     l = '0'
            #     r = '0'
            #     print((h, w, t, b, l, r))
                
            #     # Add Name and CSS Class
            #     sizing_for_elements_inside_panel(h, w, t, b, l, r)
            #     # Grandparent Selector
            #     grand_parent_name = find_grand_parent(i['Parent_Name'])
            #     grand_parent_selector = wait.until(EC.element_to_be_clickable((By.XPATH, f"//span[text() = '{grand_parent_name}']"))) 
            #     grand_parent_selector.click()
            #     grand_parent_selector.click()
            #     right_panel_handler('Styling')
            #     # parent_selector = wait.until(EC.element_to_be_clickable((By.XPATH, f"//span[text() = '{parent_name}']"))) 
            #     # parent_selector.click()
            #     # parent_selector.click()

            #     # change height to 350
            #     # try:
            #     #     wait.until(EC.element_to_be_clickable((By.XPATH, xpath_size_selector['height']))).click()
            #     #     wait.until(EC.element_to_be_clickable((By.XPATH, xpath_size_selector['px']))).click()
            #     # except TimeoutException as e:
            #     #     a = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_size_selector['height'])))
            #     #     a.click()
            #     #     b = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_size_selector['px'])))
            #     #     b.click()

            #     try:
            #         x = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_size_text['height'])))
            #         x.clear()
            #         x.send_keys(str(350) + Keys.ENTER)
            #     except (StaleElementReferenceException, ElementClickInterceptedException) as e:
            #         x = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_size_text['height'])))
            #         x.clear()
            #         x.send_keys(str(350) + Keys.ENTER)


            # elif i['Parent_Type'] == 'BLOCK_COMPONENT':
            #     h = 'auto'
            #     w = 'auto'
            #     t = '0'
            #     b = '0'
            #     l = '0'
            #     r = '0'
            #     print((h, w, t, b, l, r))
                
            #     # Add Name and CSS Class
            #     sizing_for_elements_inside_panel(h, w, t, b, l, r)

            #     parent_name = i['Parent_Name']
            #     parent_selector = wait.until(EC.element_to_be_clickable((By.XPATH, f"//span[text() = '{parent_name}']"))) 
            #     parent_selector.click()
            #     parent_selector.click()
            #     # change height to 350
            #     try:
            #         x = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_size_text['height'])))
            #         x.clear()
            #         x.send_keys(str(350) + Keys.ENTER)
            #     except (StaleElementReferenceException, ElementClickInterceptedException) as e:
            #         x = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_size_text['height'])))
            #         x.clear()
            #         x.send_keys(str(350) + Keys.ENTER)


        elif i['Type'] == 'com_sap_ip_bi_VizFrame' and i['vizType'] == 'info/combinationEx':
            name = i['Name']
            css_class = i.get('CSS_CLASS', '')
            
            feed_items = json.loads(i['feedItems'])
            filter_data = json.loads(i.get('data', '[]')) if isinstance(i.get('data', '[]'), str) else i.get('data', [])


            # feed_items[0] = dimension - can be one or more
            # feed_items[1] = color 
            # feed_items[2] = measure - column axis
            # feed_items[3] = measure - line axis
            # all the above four are in dictionary
            

            dime = []
            meas = []
            line = []
            color = []
            updated_filter = {}

            # Dimension
            dim_list = feed_items[0]['values']

            for val in dim_list:
                dime.append(val['name'])
                key_value[val['id']] = val['name']

            # Color
            color_list = feed_items[1]['values']
            for val in color_list:
                color.append(val['name'])
                key_value[val['id']] = val['name']

            # Measure - column axis
            meas_list = feed_items[2]['values']   
            for val in meas_list:
                meas.append(val['name'])
                key_value[val['id']] = val['name']

            # Measure - line axis
            if len(feed_items) > 3:
                meas_line_list = feed_items[3]['values']
                for val in meas_line_list:
                    line.append(val['name'])
                    key_value[val['id']] = val['name']
            else:
                line.append(meas[1])
                meas.pop()

        # # print(name, dime, meas, filter_data, [h, w, t, b, l, r])
            parent_selector(i['Parent_Name'])
            create_chart(i['vizType'])

            # data-testid="valueAxis"  ------------ Measure
            try:
                measure = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@data-testid='valueAxis']")))
                measure.click()
            except (ElementClickInterceptedException, TimeoutException) as e:
                measure = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@data-testid='valueAxis']")))
                measure.click()


            # Measure / Column Axis
            for key_figure in meas:
                try:
                    measure_value = wait.until(EC.element_to_be_clickable((By.XPATH, f"//div[@role='button']//span[text() =  '{key_figure}']")))
                    measure_value.click()
                except (ElementClickInterceptedException, TimeoutException) as e:
                    measure_value = wait.until(EC.element_to_be_clickable((By.XPATH, f"//div[@role='button']//span[text() =  '{key_figure}']")))
                    measure_value.click()

            # to click outside to remove the popup of dimension or measure selection
            try:
                element = driver.find_element(By.ID, 'simple-popover')
                element.click()
            except (ElementClickInterceptedException, TimeoutException) as e:
                element = driver.find_element(By.ID, 'simple-popover')
                element.click()


            # data-testid="categoryAxis" -------------- Dimension
            try:
                dimension = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'At least 1 Dimension required')]")))
                dimension.click()
            except (ElementClickInterceptedException, TimeoutException) as e:
                dimension = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'At least 1 Dimension required')]")))
                dimension.click()


            # for dim_value in dime:
            #     x = driver.find_element(By.XPATH, f"//input[@type='checkbox' and @value='{dim_value}']")
            #     x.click()

            for dim_value in dime:
                try:
                    x = wait.until(EC.element_to_be_clickable((By.XPATH, f"//input[@type='checkbox' and @value='{dim_value}']")))
                    x.click()
                except (ElementClickInterceptedException, TimeoutException) as e:
                    x = driver.find_element(By.XPATH, f"//input[@type='checkbox' and @value='{dim_value}']")
                    x.click()

            # to click outside to remove the popup of dimension or measure selection
            try:
                element = driver.find_element(By.ID, 'simple-popover')
                element.click()
            except (ElementClickInterceptedException, TimeoutException) as e:
                element = driver.find_element(By.ID, 'simple-popover')
                element.click()

            # Line
            try:
                measure_2 = wait.until(EC.element_to_be_clickable((By.XPATH, "(//span[contains(text(), 'Add Measure')])[2]")))
                measure_2.click()
            except (ElementClickInterceptedException, TimeoutException) as e:
                measure_2 = wait.until(EC.element_to_be_clickable((By.XPATH, "(//span[contains(text(), 'Add Measure')])[2]")))
                measure_2.click()


            for line_key_figure in line:
                try:
                    measure_value = wait.until(EC.element_to_be_clickable((By.XPATH, f"//div[@role='button']//span[contains(text(), '{line_key_figure}')]")))
                    measure_value.click()

                except (ElementClickInterceptedException, TimeoutException) as e:
                    measure_value = wait.until(EC.element_to_be_clickable((By.XPATH, f"//div[@role='button']//span[contains(text(), '{line_key_figure}')]")))
                    measure_value.click()

            # to click outside to remove the popup of dimension or measure selection
            try:
                element = driver.find_element(By.ID, 'simple-popover')
                element.click()
            except (ElementClickInterceptedException, TimeoutException) as e:
                element = driver.find_element(By.ID, 'simple-popover')
                element.click()
            
            #  # The pane will be in builder pane once we create a chart and it will automatically open in builder even if styling pane is opened


            right_panel_handler('Styling')

            change_name(name, css_class)

            # if i['Parent_Type'] == 'PANEL_COMPONENT':
            #     # h = i.get('HEIGHT', 'auto')
            #     # w = i.get('WIDTH', 'auto')
            #     # t = i.get('TOP_MARGIN', 'auto')
            #     # b = i.get('BOTTOM_MARGIN', 'auto')
            #     # l = i.get('LEFT_MARGIN', 'auto')
            #     # r = i.get('RIGHT_MARGIN', 'auto')
            #     h = 'auto'
            #     w = 'auto'
            #     t = '0'
            #     b = '0'
            #     l = '0'
            #     r = '0'
            #     print((h, w, t, b, l, r))
                
            #     # Add Name and CSS Class
            #     sizing_for_elements_inside_panel(h, w, t, b, l, r)
            #     # Grandparent Selector
            #     grand_parent_name = find_grand_parent(i['Parent_Name'])
            #     grand_parent_selector = wait.until(EC.element_to_be_clickable((By.XPATH, f"//span[text() = '{grand_parent_name}']"))) 
            #     grand_parent_selector.click()
            #     grand_parent_selector.click()
            #     right_panel_handler('Styling')
            #     # parent_selector = wait.until(EC.element_to_be_clickable((By.XPATH, f"//span[text() = '{parent_name}']"))) 
            #     # parent_selector.click()
            #     # parent_selector.click()

            #     # change height to 350
            #     # try:
            #     #     wait.until(EC.element_to_be_clickable((By.XPATH, xpath_size_selector['height']))).click()
            #     #     wait.until(EC.element_to_be_clickable((By.XPATH, xpath_size_selector['px']))).click()
            #     # except TimeoutException as e:
            #     #     a = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_size_selector['height'])))
            #     #     a.click()
            #     #     b = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_size_selector['px'])))
            #     #     b.click()

            #     try:
            #         x = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_size_text['height'])))
            #         x.clear()
            #         x.send_keys(str(350) + Keys.ENTER)
            #     except (StaleElementReferenceException, ElementClickInterceptedException) as e:
            #         x = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_size_text['height'])))
            #         x.clear()
            #         x.send_keys(str(350) + Keys.ENTER)
            if i['Parent_Type'] == 'PANEL_COMPONENT' or i['Parent_Type'] == 'BLOCK_COMPONENT':
                h = i.get('HEIGHT', 'auto')
                w = i.get('WIDTH', 'auto')
                t = i.get('TOP_MARGIN', 'auto')
                b = i.get('BOTTOM_MARGIN', 'auto')
                l = i.get('LEFT_MARGIN', 'auto')
                r = i.get('RIGHT_MARGIN', 'auto')
                sizing_for_elements_inside_panel(h, w, t, b, l, r)
            elif i['Parent_Type'] == 'ADAPTIVE_LAYOUT_COMPONENT':
                h = i.get('HEIGHT', '300')

                w_s = i['COL_SPAN_S']
                w_m = i['COL_SPAN_M']
                w_l = i['COL_SPAN_L']
                w_xl = i['COL_SPAN_XL']
                
                sizing_for_elements_inside_fpanel(i['Parent_Name'], i['Name'], css_class, h, w_s, w_m, w_l, w_xl)


        
        elif i['Type'] == 'com_sap_ip_bi_VizFrame' and i['vizType'] == 'info/stacked_column':
            name = i['Name']
            feed_items = json.loads(i['feedItems'])
            filter_data = json.loads(i.get('data', '[]')) if isinstance(i.get('data', '[]'), str) else i.get('data', [])


            # feed_items[0] = dimension
            # feed_items[1] = color
            # feed_items[2] = measure
            # all the above three are in dictionary
            key_value = {}

            dime = []
            meas = []
            color = []
            updated_filter = {}

            # Dimension
            dim_list = feed_items[0]['values']

            for val in dim_list:
                dime.append(val['name'])
                key_value[val['id']] = val['name']

            # Measure
            meas_list = feed_items[2]['values']   
            for val in meas_list:
                meas.append(val['name'])
                key_value[val['id']] = val['name']

            # Color
            color_list = feed_items[1]['values']
            for val in color_list:
                color.append(val['name'])
                key_value[val['id']] = val['name']


            parent_selector(i['Parent_Name'])

            create_chart(i['vizType'])

            # data-testid="valueAxis"  ------------ Measure
            try:
                measure = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@data-testid='valueAxis']")))
                measure.click()
            except (ElementClickInterceptedException, TimeoutException) as e:
                measure = driver.find_element(By.XPATH, "//div[@data-testid='valueAxis']")
                measure.click()

            for key_figure in meas:
                try:
                    measure_value = wait.until(EC.element_to_be_clickable((By.XPATH, f"//span[contains(text(), '{key_figure}')]")))
                    measure_value.click()
                except (ElementClickInterceptedException, TimeoutException) as e:
                    measure_value = driver.find_element(By.XPATH, f"//span[contains(text(), '{key_figure}')]")
                    measure_value.click()

            # to click outside to remove the popup of dimension or measure selection
            try:
                element = driver.find_element(By.ID, 'simple-popover')
                element.click()
            except (ElementClickInterceptedException, TimeoutException) as e:
                element = driver.find_element(By.ID, 'simple-popover')
                element.click()


            # data-testid="categoryAxis" -------------- Dimension
            try:
                dimension = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Add Dimension')]")))
                dimension.click()
            except (ElementClickInterceptedException, TimeoutException) as e:
                dimension = driver.find_element(By.XPATH, "//span[contains(text(), 'Add Dimension')]")
                dimension.click()


            for dim_value in dime:
                try:
                    x = wait.until(EC.element_to_be_clickable((By.XPATH, f"//input[@type='checkbox' and @value='{dim_value}']")))
                    x.click()
                except (ElementClickInterceptedException, TimeoutException) as e:
                    x = driver.find_element(By.XPATH, f"//input[@type='checkbox' and @value='{dim_value}']")
                    x.click()

            # to click outside to remove the popup of dimension or measure selection
            try:
                element = driver.find_element(By.ID, 'simple-popover')
                element.click()
            except (ElementClickInterceptedException, TimeoutException) as e:
                element = driver.find_element(By.ID, 'simple-popover')
                element.click()
            
            # Change the bar to horizontal if it is vertical
            try:
                input_element = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@type='text' and @placeholder='Select an option']")))
            except (ElementClickInterceptedException, TimeoutException) as e:
                input_element = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@type='text' and @placeholder='Select an option']")))
            
            # Get the current value of the input element
            current_value = input_element.get_attribute('value')
            # print(current_value)
            if current_value == "Horizontal":
                # Clear the current value
                input_element.click()
                try:
                    horiz = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Vertical')]")))
                    horiz.click()
                except (ElementClickInterceptedException, TimeoutException) as e:
                    horiz = driver.find_element(By.XPATH, "//span[contains(text(), 'Vertical')]")
                    horiz.click()
            else:
                # If the value is not "Vertical", do nothing
                pass

            right_panel_handler('Styling')

            change_name(name, css_class)

            if i['Parent_Type'] == 'PANEL_COMPONENT' or i['Parent_Type'] == 'BLOCK_COMPONENT':
                h = i.get('HEIGHT', 'auto')
                w = i.get('WIDTH', 'auto')
                t = i.get('TOP_MARGIN', 'auto')
                b = i.get('BOTTOM_MARGIN', 'auto')
                l = i.get('LEFT_MARGIN', 'auto')
                r = i.get('RIGHT_MARGIN', 'auto')
                sizing_for_elements_inside_panel(h, w, t, b, l, r)
            
            elif i['Parent_Type'] == 'ADAPTIVE_LAYOUT_COMPONENT':
                h = i.get('HEIGHT', '300')
                w_s = i['COL_SPAN_S']
                w_m = i['COL_SPAN_M']
                w_l = i['COL_SPAN_L']
                w_xl = i['COL_SPAN_XL']
                sizing_for_elements_inside_fpanel(i['Parent_Name'], i['Name'], css_class, h, w_s, w_m, w_l, w_xl)

            # # //input[@type='checkbox'] or //span[contains(text(), 'Show Chart as 100%')]
            # chart_100 = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Show Chart as 100%')]")))
            # chart_100.click()

            
        elif i['Type'] == 'com_sap_ip_bi_VizFrame' and i['vizType'] == 'info/number':
            name = i['Name']
            css_class = i.get('CSS_CLASS', '')
            
            feed_items = json.loads(i['feedItems'])
            filter_data = json.loads(i.get('data', '[]')) if isinstance(i.get('data', '[]'), str) else i.get('data', [])


            # feed_items[0] = measure - can be one or more

            

            meas= []
            color = []
            updated_filter = {}


            # Measure - actual values
            meas_list = feed_items[0]['values']   
            for val in meas_list:
                meas.append(val['name'])
                # key_value[val['id']] = val['name']



            # meas = meas_actual + meas_additional
        # print(name, dime, meas, filter_data, [h, w, t, b, l, r])
            parent_selector(i['Parent_Name'])
            create_chart(i['vizType'])

        # data-testid="valueAxis"  ------------ Measure
            try:
                measure = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@data-testid='valueAxis']")))
                measure.click()
            except (ElementClickInterceptedException, TimeoutException) as e:
                measure = driver.find_element(By.XPATH, "//div[@data-testid='valueAxis']")
                measure.click()

            # for key_figure in meas:
            #     measure_value = wait.until(EC.element_to_be_clickable((By.XPATH, f"//span[contains(text(), '{key_figure}')]")))
            #     measure_value.click()

            for key_figure in meas:
                try:
                    measure_value = wait.until(EC.element_to_be_clickable((By.XPATH, f"//div[@role='button']//span[contains(text(), '{key_figure}')]")))
                    measure_value.click()
                except (ElementClickInterceptedException, TimeoutException) as e:
                    measure_value = driver.find_element(By.XPATH, f"//div[@role='button']//span[contains(text(), '{key_figure}')]")
                    measure_value.click()

            # to click outside to remove the popup of dimension or measure selection
            try:
                element = driver.find_element(By.ID, 'simple-popover')
                element.click()
            except (ElementClickInterceptedException, TimeoutException) as e:
                element = driver.find_element(By.ID, 'simple-popover')
                element.click()


            right_panel_handler('Styling')

            change_name(name, css_class)

            if i['Parent_Type'] == 'PANEL_COMPONENT' or i['Parent_Type'] == 'BLOCK_COMPONENT':
                h = i.get('HEIGHT', 'auto')
                w = i.get('WIDTH', 'auto')
                t = i.get('TOP_MARGIN', 'auto')
                b = i.get('BOTTOM_MARGIN', 'auto')
                l = i.get('LEFT_MARGIN', 'auto')
                r = i.get('RIGHT_MARGIN', 'auto')
                sizing_for_elements_inside_panel(h, w, t, b, l, r)
            elif i['Parent_Type'] == 'ADAPTIVE_LAYOUT_COMPONENT':
                h = i.get('HEIGHT', '300')
                w_s = i['COL_SPAN_S']
                w_m = i['COL_SPAN_M']
                w_l = i['COL_SPAN_L']
                w_xl = i['COL_SPAN_XL']
                
                sizing_for_elements_inside_fpanel(i['Parent_Name'], i['Name'], css_class, h, w_s, w_m, w_l, w_xl)

            # if i['Parent_Type'] == 'PANEL_COMPONENT' or i['Parent_Type'] == 'BLOCK_COMPONENT':
            #     h = i.get('HEIGHT', 'auto')
            #     w = i.get('WIDTH', 'auto')
            #     t = i.get('TOP_MARGIN', 'auto')
            #     b = i.get('BOTTOM_MARGIN', 'auto')
            #     l = i.get('LEFT_MARGIN', 'auto')
            #     r = i.get('RIGHT_MARGIN', 'auto')
            #     print((h, w, t, b, l, r))
                
                
            #     sizing_for_elements_inside_panel(h, w, t, b, l, r)
            # elif i['Parent_Type'] == 'ADAPTIVE_LAYOUT_COMPONENT':
            #     h = i.get('HEIGHT', 'auto')
            #     w_s = i['COL_SPAN_S']
            #     w_m = i['COL_SPAN_M']
            #     w_l = i['COL_SPAN_L']
            #     w_xl = i['COL_SPAN_XL']

            #     sizing_for_elements_inside_fpanel(i['Parent_Name'], i['Name'], css_class, h, w_s, w_m, w_l, w_xl)

        elif i['Type'] == 'com_sap_ip_bi_VizFrame' and i['vizType'] == 'info/stacked_bar':
            name = i['Name']
            feed_items = json.loads(i['feedItems'])
            filter_data = json.loads(i.get('data', '[]')) if isinstance(i.get('data', '[]'), str) else i.get('data', [])


            # feed_items[0] = dimension
            # feed_items[1] = color
            # feed_items[2] = measure
            # all the above three are in dictionary
            key_value = {}

            dime = []
            meas = []
            color = []
            updated_filter = {}

            # Dimension
            dim_list = feed_items[0]['values']

            for val in dim_list:
                dime.append(val['name'])
                key_value[val['id']] = val['name']

            # Measure
            meas_list = feed_items[2]['values']   
            for val in meas_list:
                meas.append(val['name'])
                key_value[val['id']] = val['name']

            # Color
            color_list = feed_items[1]['values']
            for val in color_list:
                color.append(val['name'])
                key_value[val['id']] = val['name']


            parent_selector(i['Parent_Name'])

            create_chart(i['vizType'])

            # data-testid="valueAxis"  ------------ Measure
            try:
                measure = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@data-testid='valueAxis']")))
                measure.click()
            except (StaleElementReferenceException, TimeoutException) as e:
                measure = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@data-testid='valueAxis']")))
                measure.click()

            for key_figure in meas:
                try:
                    measure_value = wait.until(EC.element_to_be_clickable((By.XPATH, f"//span[contains(text(), '{key_figure}')]")))
                    measure_value.click()
                except (ElementClickInterceptedException, TimeoutException) as e:
                    measure_value = wait.until(EC.element_to_be_clickable((By.XPATH, f"//span[contains(text(), '{key_figure}')]")))
                    measure_value.click()

            # to click outside to remove the popup of dimension or measure selection
            try:
                element = driver.find_element(By.ID, 'simple-popover')
                element.click()
            except (ElementClickInterceptedException, TimeoutException) as e:
                element = driver.find_element(By.ID, 'simple-popover')
                element.click()


            # data-testid="categoryAxis" -------------- Dimension
            try:
                dimension = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Add Dimension')]")))
                dimension.click()
            except (StaleElementReferenceException, TimeoutException) as e:
                dimension = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Add Dimension')]")))
                dimension.click()

            for dim_value in dime:
                try:
                    x = wait.until(EC.element_to_be_clickable((By.XPATH, f"//input[@type='checkbox' and @value='{dim_value}']")))
                    x.click()
                except (ElementClickInterceptedException, TimeoutException) as e:
                    x = driver.find_element(By.XPATH, f"//input[@type='checkbox' and @value='{dim_value}']")
                    x.click()

            # to click outside to remove the popup of dimension or measure selection
            try:
                element = driver.find_element(By.ID, 'simple-popover')
                element.click()
            except (ElementClickInterceptedException, TimeoutException) as e:
                element = driver.find_element(By.ID, 'simple-popover')
                element.click()

            right_panel_handler('Styling')

            change_name(name, css_class)

            if i['Parent_Type'] == 'PANEL_COMPONENT' or i['Parent_Type'] == 'BLOCK_COMPONENT':
                h = i.get('HEIGHT', 'auto')
                w = i.get('WIDTH', 'auto')
                t = i.get('TOP_MARGIN', 'auto')
                b = i.get('BOTTOM_MARGIN', 'auto')
                l = i.get('LEFT_MARGIN', 'auto')
                r = i.get('RIGHT_MARGIN', 'auto')
                sizing_for_elements_inside_panel(h, w, t, b, l, r)
            
            elif i['Parent_Type'] == 'ADAPTIVE_LAYOUT_COMPONENT':
                h = i.get('HEIGHT', '300')
                w_s = i['COL_SPAN_S']
                w_m = i['COL_SPAN_M']
                w_l = i['COL_SPAN_L']
                w_xl = i['COL_SPAN_XL']
                sizing_for_elements_inside_fpanel(i['Parent_Name'], i['Name'], css_class, h, w_s, w_m, w_l, w_xl)

            
        elif i['Type'] == 'com_sap_ip_bi_VizFrame' and i['vizType'] == 'info/bubble':    
        # Bubble chart needs 5 things
        # 1. color [1] - dimension --> multiple selection
        # 2. measure X-axis - valueAxis1  [3] --> only one selection
        # 3. measure Y-axis - valueAxis2  [4] --> only one selection
        # 4. Dimension [0] --> only one selection
        # 5. Size - bubblewidth --> only one selection

            name = i['Name']
            feed_items = json.loads(i['feedItems'])
            filter_data = json.loads(i.get('data', '[]')) if isinstance(i.get('data', '[]'), str) else i.get('data', [])


            parent_selector(i['Parent_Name'])
            create_chart(i['vizType'])

            color_dime = []
            color_list = feed_items[1]['values']
            for val in color_list:
                color_dime.append(val['name'])
                key_value[val['id']] = val['name']

            # //span[text() = 'At least 1 Dimension/Measure required']
            try:
                color_selector = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text() = 'At least 1 Dimension/Measure required']")))
                color_selector.click()
            except (ElementClickInterceptedException, TimeoutException) as e:
                color_selector = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text() = 'At least 1 Dimension/Measure required']")))
                color_selector.click()

            # //input[@type='checkbox' and @value='Category']
            for dim_value in color_dime:
                dim_value = dim_value.replace(' ', '_')
                try:
                    x = wait.until(EC.element_to_be_clickable((By.XPATH, f"//input[@type='checkbox' and @value='{dim_value}']")))
                    x.click()
                except (ElementClickInterceptedException, TimeoutException) as e:
                    x = driver.find_element(By.XPATH, f"//input[@type='checkbox' and @value='{dim_value}']")
                    x.click()
            # to click outside to remove the popup of dimension or measure selection
            try:
                element = driver.find_element(By.ID, 'simple-popover')
                element.click()
            except (ElementClickInterceptedException, TimeoutException) as e:
                element = driver.find_element(By.ID, 'simple-popover')
                element.click()



            measure_x_axis = feed_items[3]['values'][0]['name']

            try:
                measure = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@data-testid='valueAxis']")))
                measure.click()
            except (ElementClickInterceptedException, TimeoutException) as e:
                measure = driver.find_element(By.XPATH, "//div[@data-testid='valueAxis']")
                measure.click()

            # //p[text() = 'SalesGrowth%']
            try:
                x = wait.until(EC.element_to_be_clickable((By.XPATH, f"//p[text() = '{measure_x_axis}']")))
                x.click()
            except (ElementClickInterceptedException, TimeoutException) as e:
                x = driver.find_element(By.XPATH, f"//p[text() = '{measure_x_axis}']")
                x.click()
            
            time.sleep(5)


            measure_y_axis = feed_items[4]['values'][0]['name']

            try:
                measure = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@data-testid='valueAxis2']")))
                measure.click()
            except (ElementClickInterceptedException, TimeoutException) as e:
                measure = driver.find_element(By.XPATH, "//div[@data-testid='valueAxis2']")
                measure.click()

            try:
                x = wait.until(EC.element_to_be_clickable((By.XPATH, f"//p[text() = '{measure_y_axis}']")))
                x.click()
            except (ElementClickInterceptedException, TimeoutException) as e:
                x = driver.find_element(By.XPATH, f"//p[text() = '{measure_y_axis}']")
                x.click()



            size = feed_items[5]['values'][0]['name']
            # size = size.replace('%', '_')
            # (//span[text() = 'At least 1 Measure required'])[3]
            try:
                size_selector = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text() = 'At least 1 Measure required']")))
                size_selector.click()
            except (ElementClickInterceptedException, TimeoutException) as e:
                size_selector = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text() = 'At least 1 Measure required']")))
                size_selector.click()


            try:
                x = wait.until(EC.element_to_be_clickable((By.XPATH, f"//p[text() = '{size}']")))
                x.click()
            except (ElementClickInterceptedException, TimeoutException) as e:
                x = driver.find_element(By.XPATH, f"//p[text() = '{size}']")
                x.click()

            try:
                # to click outside to remove the popup of dimension or measure selection
                element = driver.find_element(By.ID, 'simple-popover')
                element.click()
            except:
                pass

            dimension_bubble = (feed_items[0]['values'])

            if len(dimension_bubble) > 0:

                dimension_bubble = dimension_bubble[0]['name']
                
                try:
                    color_selector = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text() = 'At least 1 Dimension required']")))
                    color_selector.click()
                except (ElementClickInterceptedException, TimeoutException) as e:
                    color_selector = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text() = 'At least 1 Dimension required']")))
                    color_selector.click()

                try:
                    x = wait.until(EC.element_to_be_clickable((By.XPATH, f"//input[@type='checkbox' and @value='{dimension_bubble}']")))
                    x.click()
                except (ElementClickInterceptedException, TimeoutException) as e:
                    x = driver.find_element(By.XPATH, f"//input[@type='checkbox' and @value='{dimension_bubble}']")
                    x.click()

            right_panel_handler('Styling')

            change_name(name, css_class)

            if i['Parent_Type'] == 'PANEL_COMPONENT' or i['Parent_Type'] == 'BLOCK_COMPONENT':
                h = i.get('HEIGHT', 'auto')
                w = i.get('WIDTH', 'auto')
                t = i.get('TOP_MARGIN', 'auto')
                b = i.get('BOTTOM_MARGIN', 'auto')
                l = i.get('LEFT_MARGIN', 'auto')
                r = i.get('RIGHT_MARGIN', 'auto')
                sizing_for_elements_inside_panel(h, w, t, b, l, r)

            elif i['Parent_Type'] == 'ADAPTIVE_LAYOUT_COMPONENT':
                h = i.get('HEIGHT', '300')
                w_s = i['COL_SPAN_S']
                w_m = i['COL_SPAN_M']
                w_l = i['COL_SPAN_L']
                w_xl = i['COL_SPAN_XL']
                sizing_for_elements_inside_fpanel(i['Parent_Name'], i['Name'], css_class, h, w_s, w_m, w_l, w_xl)




        elif i['Type'] == 'TEXT_COMPONENT':
            parent_selector(i['Parent_Name'])
            text_component(i['TEXT'])
            name = i['Name']
            css_class = i.get('CSS_CLASS', '')

            right_panel_handler('Styling')

            change_name(name, css_class)
            if i['Parent_Type'] == 'PANEL_COMPONENT' or i['Parent_Type'] == 'BLOCK_COMPONENT' or i['Parent_Type'] == None:
                    h = i.get('HEIGHT', 'auto')
                    w = i.get('WIDTH', 'auto')
                    t = i.get('TOP_MARGIN', 'auto')
                    b = i.get('BOTTOM_MARGIN', 'auto')
                    l = i.get('LEFT_MARGIN', 'auto')
                    r = i.get('RIGHT_MARGIN', 'auto')
                    print((h, w, t, b, l, r))

                    # Add Name and CSS Class
                    sizing_for_elements_inside_panel(h, w, t, b, l, r)
            elif i['Parent_Type'] == 'ADAPTIVE_LAYOUT_COMPONENT':
                    h = i.get('HEIGHT', '300')
                    w_s = i['COL_SPAN_S']
                    w_m = i['COL_SPAN_M']
                    w_l = i['COL_SPAN_L']
                    w_xl = i['COL_SPAN_XL']

                    sizing_for_elements_inside_fpanel(i['Parent_Name'], i['Name'], css_class, h, w_s, w_m, w_l, w_xl)


    # Read the original CSS file
    with open('lumira_files/custom.css', 'r') as file:
        css_code = file.read()

    # Remove lines starting with //
    cleaned_css = "\n".join(line for line in css_code.splitlines() if not line.strip().startswith('//'))
    # Remove lines starting with //
    cleaned_css = "\n".join(line for line in css_code.splitlines() if not line.strip().startswith('//'))

    # If you want to further clean up any inline comments (e.g., within a line), use this:
    cleaned_css = "\n".join(
        line.split('//')[0].rstrip()  # Get the part before '//' and strip trailing whitespace
        for line in cleaned_css.splitlines()
    )
    # Write the cleaned CSS back to a new file
    with open('cleaned_custom.css', 'w') as file:
        file.write(cleaned_css)

    
    # Regular expression to find background-color properties
    background_color_pattern = re.compile(r'(\.\w+)\s*{\s*background-color:\s*([^;]+);', re.MULTILINE)

    # Extracting classes and their background colors
    background_colors = {match[0]: match[1].strip() for match in background_color_pattern.findall(css_code)}

    print(background_colors)

    res = ''

    for key, value in background_colors.items():
        res += f'{key} {{ background-color: {value}; }}\n'
        

    with open('cleaned_custom.css', 'w') as file:
        file.write(res)

    # Add CSS to the Dashboard
    css_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@title='Edit CSS']"))) 
    css_btn.click()
    time.sleep(5)
    text_area = wait.until(EC.element_to_be_clickable((By.TAG_NAME, "pre")))
    text_area.click()
    print('Clicked')


    ActionChains(driver).send_keys(res).perform()
# Saving the code
    actions = ActionChains(driver)

    # Simulate pressing Ctrl + S
    actions.key_down(Keys.CONTROL).send_keys('s').key_up(Keys.CONTROL).perform()
    try:
        search_box = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@type='search']")))
        search_box.click()
        search_box.clear()
        search_box.send_keys('Lumira_webi_SAC' + Keys.ENTER)
    except (ElementClickInterceptedException, TimeoutException, StaleElementReferenceException) as e:
        search_box = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@type='search']")))
        search_box.click()
        search_box.clear()
        search_box.send_keys('Lumira_webi_SAC' + Keys.ENTER)

    wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Lumira_webi_SAC')]"))).click()

    st_name = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder = 'Please enter a name' and @type='text']")))
    st_name.click()
    st_name.clear()
    st_name.send_keys(model_name + Keys.ENTER)

    save = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[.//bdi[text() = 'Save']]")))
    save.click()
    try:
        overwrite = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[.//bdi[text() = 'Overwrite']]")))
        overwrite.click()
    except (TimeoutException, NoSuchElementException, StaleElementReferenceException) as e:
        pass


    time.sleep(7)
    try:
        settings = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@title='Story Settings']")))
        settings.click()
    except (TimeoutException, NoSuchElementException, StaleElementReferenceException, ElementClickInterceptedException) as e:
        settings = driver.find_element(By.XPATH, "//button[@title='Story Settings']")
        settings.click()
    
    story_details = wait.until(EC.element_to_be_clickable((By.XPATH, "//li[@title='Story Details']")))
    story_details.click()

    try:
        mobile_support = wait.until(EC.element_to_be_clickable((By.XPATH, "(//div[contains(@class, 'sapMSwtCont') and @role='switch'])[4]")))
        mobile_support.click()
        print('Mobile support is enabled 1')
    except (StaleElementReferenceException, TimeoutException) as e:
        mobile_support = driver.find_element(By.XPATH, "(//div[contains(@class, 'sapMSwtCont') and @role='switch'])[4]")
        mobile_support.click()
        print('Mobile support is enabled 2')

    save = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[.//bdi[text() = 'Save']]")))
    save.click()

    actions.key_down(Keys.CONTROL).send_keys('s').key_up(Keys.CONTROL).perform()

    pbar.progress(100, text=f"Converted - 100%")
    st.balloons()
    st.toast("Converted lumira to SAC")
    time.sleep(3)
    st.rerun()
    # ENDDDDDD


def file_handler():
    pass




# ENDDDDDD

