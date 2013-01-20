import sublime, sublime_plugin, os, glob, re
from lib.inflector import *

class RailsSwitcherCommandBase(sublime_plugin.WindowCommand):
  VIEWS_DIR = os.path.join('app', 'views')
  CONTROLLERS_DIR = os.path.join('app', 'controllers')
  MODELS_DIR = os.path.join('app', 'models')

  def is_controller(self, file):
    return self.CONTROLLERS_DIR in file

  def is_rails_entity(self, file):
    return self.entity_type(file) is not None

  def entity_type(self, file):
    if self.VIEWS_DIR in file:
      return 'view'
    elif self.MODELS_DIR in file:
      return 'model'
    elif self.CONTROLLERS_DIR in file:
      return 'controller'
    else:
      return None

  def entity_name(self, file):
    if self.entity_type(file) == 'view':
      return self.view_name(file)
    elif self.entity_type(file) == 'controller':
      return self.controller_name(file)
    elif self.entity_type(file) == 'model':
      return self.model_name(file)
    else:
      return None

  def controller_name(self, current_file):
    return Inflector().singularize(self.base_file_name(current_file).replace('_controller', ''))

  def controller_action(self, file):
    if self.is_controller(file) == False:
      return None
    view = sublime.active_window().active_view()
    cursor_point = view.sel()[0].end()
    actions_definitions_regions = sublime.active_window().active_view().find_all('def \w+')
    for actions_definition_region in actions_definitions_regions:
      if actions_definition_region.b <= cursor_point:
        action_definition = view.substr(actions_definition_region)

    return action_definition.replace('def ', '')

  def model_name(self, current_file):
    return self.base_file_name(current_file)

  def view_name(self, current_file):
    regex = re.compile('.*/app/views/(.+)/.*')
    view_name = Inflector().singularize(regex.findall(current_file)[0])
    return view_name

  def related_controller(self, file):
    if self.is_controller == True:
      return None
    controller_file = Inflector().pluralize(self.entity_name(file)) + "_controller.rb"
    return os.path.join(self.rails_root_directory,self.CONTROLLERS_DIR, controller_file)

  def related_model(self, current_file):
    if self.is_rails_entity(current_file) == False:
      return None

    model_file = self.entity_name(current_file) + ".rb"
    return os.path.join(self.rails_root_directory, self.MODELS_DIR, model_file)

  def related_view(self, file):
    view_file = None
    if self.is_controller(file) == False:
      return None

    # posts (for example)
    plural_entity_name = Inflector().pluralize(self.entity_name(file))

    # posts/index (for example)
    file_without_extension = os.path.join(plural_entity_name, self.controller_action(file))

    file_without_extension_full_path = os.path.join(self.rails_root_directory, self.VIEWS_DIR, file_without_extension)

    # Using glob to support different extensions, like .erb, .haml, etc
    view_file_list = glob.glob(file_without_extension_full_path + ".*")

    if view_file_list:
      view_file = os.path.join(self.rails_root_directory, self.VIEWS_DIR, view_file_list.pop())

    return view_file

  def open_related_file(self, file):
    if file is None:
      print "Could not find related file."
    elif os.path.exists(file):
      sublime.active_window().open_file(file)
    else:
      print file + " not found"
      return False

  def base_file_name(self, file_path):
    return os.path.splitext(os.path.basename(file_path))[0]

  def rails_root_directory_from_active_window(self):
    directories = sublime.active_window().folders()
    file = sublime.active_window().active_view().file_name()

    for directory in directories:
      if directory in file and os.path.exists(os.path.join(directory, 'Rakefile')):
        return os.path.abspath(directory)

    return None

  def setup(self):
    self.rails_root_directory = self.rails_root_directory_from_active_window()
    self.current_file_path = sublime.active_window().active_view().file_name()

    return True if self.rails_root_directory else False

class OpenRelatedRailsControllerCommand(RailsSwitcherCommandBase):
  def run(self):
    if self.setup():
      related_controller = self.related_controller(self.current_file_path)
      self.open_related_file(related_controller)

class OpenRelatedRailsModelCommand(RailsSwitcherCommandBase):
  def run(self):
    if self.setup():
      related_model = self.related_model(self.current_file_path)
      self.open_related_file(related_model)

class OpenRelatedRailsViewCommand(RailsSwitcherCommandBase):
  def run(self):
    if self.setup():
      related_view = self.related_view(self.current_file_path)
      self.open_related_file(related_view)