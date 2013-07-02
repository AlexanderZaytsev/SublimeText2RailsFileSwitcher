import sublime, sublime_plugin, os, glob, re
from lib.inflector import *

class RailsFileSwitcher(object):
  VIEWS_DIR = os.path.join('app', 'views')
  CONTROLLERS_DIR = os.path.join('app', 'controllers')
  MODELS_DIR = os.path.join('app', 'models')
  SERVICES_DIR = os.path.join('app', 'services')
  MAILERS_DIR = os.path.join('app', 'mailers')
  RSPEC_MODELS_DIR = os.path.join('spec', 'models')
  RSPEC_CONTROLLERS_DIR = os.path.join('spec', 'controllers')

  def __init__(self, window, target_resource_name = None):
    self.window = window
    self.opened_file_name = self.window.active_view().file_name()
    self.rails_root_path = self.rails_root_path()

    if not self.is_rails_app():
      raise Exception('Not a Rails application')

  def is_rails_app(self):
    return True if self.rails_root_path else False

  def opened_resource_is_controller(self):
    return self.CONTROLLERS_DIR in self.opened_file_name

  def opened_resource_type(self):
    if self.VIEWS_DIR in self.opened_file_name:
      return 'view'
    elif self.MODELS_DIR in self.opened_file_name:
      return 'model'
    elif self.CONTROLLERS_DIR in self.opened_file_name:
      return 'controller'
    elif self.RSPEC_MODELS_DIR in self.opened_file_name:
      return 'rspec_model'
    elif self.RSPEC_CONTROLLERS_DIR in self.opened_file_name:
      return 'rspec_controller'
    else:
      return None

  def opened_resource_name(self):
    if self.opened_resource_type() == 'view':
      match = re.search('app/views/(.+)/', self.opened_file_name.replace('\\', '/'))
      if match:
        return match.group(1)
    elif self.opened_resource_type() == 'controller':
      match = re.search('app/controllers/(.+)_controller\.rb', self.opened_file_name.replace('\\', '/'))
      if match:
        return match.group(1)
    elif self.opened_resource_type() == 'model':
      match = re.search('app/models/(.+)\.rb', self.opened_file_name.replace('\\', '/'))
      if match:
        return match.group(1)
    elif self.opened_resource_type() == 'rspec_controller':
      match = re.search('spec/controllers/(.+)_controller_spec\.rb', self.opened_file_name.replace('\\', '/'))
      if match:
        return match.group(1)
    elif self.opened_resource_type() == 'rspec_model':
      match = re.search('spec/models/(.+)_spec\.rb', self.opened_file_name.replace('\\', '/'))
      if match:
        return match.group(1)
    else:
      return None

  def opened_resource_name_without_namespace(self):
    return re.split('/|::', self.opened_resource_name()).pop()


  def rails_root_path(self):
    directories = self.window.folders()

    for directory in directories:
      if directory in self.opened_file_name and os.path.exists(os.path.join(directory, 'Rakefile')):
        return os.path.abspath(directory)

    return None

  def open_file(self, file_path):
    if file_path is None:
      print 'Could not find related file'
    elif os.path.exists(file_path):
      self.window.open_file(file_path)
    else:
      print file_path + ' not found'
      self.show_create_file_input_panel(file_path)
      return False

  def show_create_file_input_panel(self, file_path):
    relative_file_path = self.file_path().replace(self.rails_root_path + '/', '')
    self.window.show_input_panel('The file does not exist. Press Enter to create it:', relative_file_path, self.create_file, None, None)

  def create_file(self, relative_file_path):
    view_file_path = os.path.join(self.rails_root_path, relative_file_path)

    view_file = open(view_file_path, 'w')
    view_file.write('')
    view_file.close()
    self.window.open_file(view_file_path)

class RailsModelSwitcher(RailsFileSwitcher):
  def run(self):
    self.open_file(self.file_path())

  def file_path(self):
    view = self.window.active_view()
    selection = view.substr(view.word(view.sel()[0]))

    # Check if current selection is uppercased (Post, etc)
    if selection != '' and selection[0].isupper():
      model_name = Inflector().underscore(selection)
    else:
      # We need to pluralize first, then singularize, because otherwise words like 'Address' get singularized into 'Addres'
      model_name = Inflector().singularize(Inflector().pluralize(self.opened_resource_name_without_namespace()))

    file_name = model_name + '.rb'
    if re.search('_service.rb$', file_name):
      return os.path.join(self.rails_root_path, self.SERVICES_DIR, file_name)
    elif re.search('_mailer.rb$', file_name):
      return os.path.join(self.rails_root_path, self.MAILERS_DIR, file_name)
    else:
      return os.path.join(self.rails_root_path, self.MODELS_DIR, file_name)

class RspecModelSwitcher(RailsFileSwitcher):
  def run(self):
    self.open_file(self.file_path())

  def file_path(self):
    view = self.window.active_view()
    selection = view.substr(view.word(view.sel()[0]))

    # Check if current selection is uppercased (Post, etc)
    if selection != '' and selection[0].isupper():
      model_name = Inflector().underscore(selection)
    else:
      # We need to pluralize first, then singularize, because otherwise words like 'Address' get singularized into 'Addres'
      model_name = Inflector().singularize(Inflector().pluralize(self.opened_resource_name_without_namespace()))

    file_name = model_name + '_spec.rb'
    return os.path.join(self.rails_root_path, self.RSPEC_MODELS_DIR, file_name)

class RailsViewSwitcher(RailsFileSwitcher):
  def run(self):
    if not self.opened_resource_is_controller():
      raise Exception('This command can be run from a controller only')

    self.open_file(self.file_path())

  def file_path(self):
    file_path = None

    if self.controller_action() == None:
      return None

    # posts/index
    file_name_without_extension = os.path.join(self.opened_resource_name(), self.controller_action())

    full_path_without_extension = os.path.join(self.rails_root_path, self.VIEWS_DIR, file_name_without_extension)

    # Using glob to support different extensions, like .erb, .haml, etc
    views_list = glob.glob(full_path_without_extension + '.*')

    if views_list:
      # Views exist, choose the first one

      # Using pop(0) to prefer `html` to `js` and `json`
      file_path = os.path.join(self.rails_root_path, self.VIEWS_DIR, views_list.pop(0))
    else:
      # No view exists, we need to know what to name it if the user decides to create it
      file_path = full_path_without_extension + '.html.' + self.views_extension()

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

  def views_extension(self):
    # Using layouts to determine view extensions.
    layouts_dir = os.path.join(self.rails_root_path, self.VIEWS_DIR, 'layouts/*.*')
    layouts_list = glob.glob(layouts_dir)
    layout_file_name = layouts_list.pop()

    extension = layout_file_name.split('.').pop()
    return extension

class RailsControllerSwitcher(RailsFileSwitcher):
  def run(self):
    controller_action = self.controller_action()

    self.window.open_file(self.file_path())

    if controller_action:
      if self.window.active_view().is_loading():
        sublime.set_timeout(lambda: self.run(), 100)
      else:
        self.scroll_to_controller_action(controller_action)

  def file_path(self):
    file_name = Inflector().pluralize(self.opened_resource_name()) + '_controller.rb'
    return os.path.join(self.rails_root_path, self.CONTROLLERS_DIR, file_name)

  def controller_action(self):
    plural_controller_name = Inflector().pluralize(self.opened_resource_name())
    regex = re.compile('app/views/'+plural_controller_name+'/([^\.]+)')
    match = regex.findall(self.opened_file_name)
    if match:
      return match[0]

  def scroll_to_controller_action(self, controller_action):
    view = self.window.active_view()
    action_definition_region = view.find('def ' + controller_action, 0)

    if action_definition_region:
      view.show_at_center(action_definition_region)

      # If Vintage is enabled, we will move the caret to the action definition
      if view.get_status('mode'):
        view.sel().clear()

        # We need to do it this way because otherwise sometimes
        # the caret position is not updated
        view.run_command('enter_visual_mode')
        view.sel().add(action_definition_region)
        view.run_command('exit_visual_mode')

class RspecControllerSwitcher(RailsFileSwitcher):
  def run(self):
    self.window.open_file(self.file_path())

  def file_path(self):
    file_name = Inflector().pluralize(self.opened_resource_name()) + '_controller_spec.rb'
    return os.path.join(self.rails_root_path, self.RSPEC_CONTROLLERS_DIR, file_name)

class OpenRelatedRailsModelCommand(sublime_plugin.WindowCommand):
  def run(self):
    RailsModelSwitcher(sublime.active_window()).run()

class OpenRelatedRailsViewCommand(sublime_plugin.WindowCommand):
  def run(self):
    RailsViewSwitcher(sublime.active_window()).run()

class OpenRelatedRailsControllerCommand(sublime_plugin.WindowCommand):
  def run(self):
    RailsControllerSwitcher(sublime.active_window()).run()

class OpenRelatedRspecModelCommand(sublime_plugin.WindowCommand):
  def run(self):
    RspecModelSwitcher(sublime.active_window()).run()

class OpenRelatedRspecControllerCommand(sublime_plugin.WindowCommand):
  def run(self):
    RspecControllerSwitcher(sublime.active_window()).run()
