import sublime, sublime_plugin, os, glob, re
from lib.inflector import *

class RailsFileSwitcher(object):
  VIEWS_DIR = os.path.join('app', 'views')
  CONTROLLERS_DIR = os.path.join('app', 'controllers')
  MODELS_DIR = os.path.join('app', 'models')

  def __init__(self, window, target_resource_name = None):
    self.window = window
    self.opened_file = self.window.active_view().file_name()
    self.rails_root_path = self.rails_root_path()

  def is_rails_app(self):
    return True if self.rails_root_path else False

  def opened_resource_is_controller(self):
    return self.CONTROLLERS_DIR in self.opened_file

  def opened_resource_type(self):
    if self.VIEWS_DIR in self.opened_file:
      return 'view'
    elif self.MODELS_DIR in self.opened_file:
      return 'model'
    elif self.CONTROLLERS_DIR in self.opened_file:
      return 'controller'
    else:
      return None

  def opened_resource_name(self):
    if self.opened_resource_type() == 'view':
      regex = re.compile('.*/app/views/(.+)/.*')
      return Inflector().singularize(regex.findall(self.opened_file)[0])
    elif self.opened_resource_type() == 'controller':
      return Inflector().singularize(self.base_file_name(self.opened_file).replace('_controller', ''))
    elif self.opened_resource_type() == 'model':
      return self.base_file_name(self.opened_file)
    else:
      return None

  def rails_root_path(self):
    directories = self.window.folders()

    for directory in directories:
      if directory in self.opened_file and os.path.exists(os.path.join(directory, 'Rakefile')):
        return os.path.abspath(directory)

    return None

  def open_file(self, file_path):
    if file_path is None:
      print "Could not find related file"
    elif os.path.exists(file_path):
      self.window.open_file(file_path)
    else:
      print file_path + " not found"
      return False

  def base_file_name(self, file_path):
    return os.path.splitext(os.path.basename(file_path))[0]

  def run(self):
    if self.is_rails_app():
      self.open_file(self.file_path())
    else:
      print "Not a Rails application"

class RailsModelSwitcher(RailsFileSwitcher):
  def file_path(self):
    view = self.window.active_view()
    selection = view.substr(view.word(view.sel()[0]))

    # Check if current selection is uppercased (Post, etc)
    if selection != '' and selection[0].isupper():
      model_name = Inflector().underscore(selection)
    else:
      model_name = self.opened_resource_name()

    file_name = model_name + ".rb"
    return os.path.join(self.rails_root_path, self.MODELS_DIR, file_name)

class RailsViewSwitcher(RailsFileSwitcher):
  def file_path(self):
    file_path = None

    if self.opened_resource_is_controller() == False:
      print "Not a controller"
      return None

    # posts
    plural_resource_name = Inflector().pluralize(self.opened_resource_name())

    # posts/index
    file_name_without_extension = os.path.join(plural_resource_name, self.controller_action())

    full_path_without_extension = os.path.join(self.rails_root_path, self.VIEWS_DIR, file_name_without_extension)

    # Using glob to support different extensions, like .erb, .haml, etc
    views_list = glob.glob(full_path_without_extension + ".*")

    if views_list:
      file_path = os.path.join(self.rails_root_path, self.VIEWS_DIR, views_list.pop())

    print full_path_without_extension
    return file_path

  def controller_action(self):
    action = None
    view = self.window.active_view()
    cursor_point = view.sel()[0].end()
    actions_definitions_regions = view.find_all('  def \w+')
    for action_definition_region in actions_definitions_regions:
      if action_definition_region.a <= cursor_point:
        action = view.substr(action_definition_region).replace('  def ', '')

    return action

class RailsControllerSwitcher(RailsFileSwitcher):
  def file_path(self):
    file_name = Inflector().pluralize(self.opened_resource_name()) + "_controller.rb"

    return os.path.join(self.rails_root_path, self.CONTROLLERS_DIR, file_name)

class OpenRelatedRailsModelCommand(sublime_plugin.WindowCommand):
  def run(self):
    RailsModelSwitcher(sublime.active_window()).run()

class OpenRelatedRailsViewCommand(sublime_plugin.WindowCommand):
  def run(self):
    RailsViewSwitcher(sublime.active_window()).run()

class OpenRelatedRailsControllerCommand(sublime_plugin.WindowCommand):
  def run(self):
    RailsControllerSwitcher(sublime.active_window()).run()