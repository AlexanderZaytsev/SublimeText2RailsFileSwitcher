# Rails File Switcher for Sublime Text 2
Rails File Switcher is a plugin for Sublime Text 2 that allows you to switch between Models, Controllers and Views. And how!

No popups, just immediately switches to the related file.

## Commands
### open_related_rails_model (super+1)
- Opens the related model.
- If you put the caret inside a model's name (like Po│st) and run the command, it will open the model from any place in the application. This works for models, services and mailers (examples: `Post`, `PostService`, `PostMailer`).

### open_related_rails_controller (super+2)
- Opens the related controller from a model and rspec model & controller specs.
- Opens the related controller from a view. Centers the screen at the action definition. If Vintage is enabled, it also moves the caret to the action definition.

### open_related_rails_view (super+3)
- Opens the related view from a controller. You need to put the caret inside the controller action for it to work.

### open_related_rspec_model (super+4)
- Opens the related rspec model spec.
- If you put the caret inside a model's name (like Po│st) and run the command, it will open the model spec from any place in the application.

### open_related_rspec_controller (super+5)
- Opens the related rspec controller spec from a model and rspec model.

## Bindings
Here are the default bindings. You can change them in `Preferences > Key Bindings - User`
```json
{ "keys": ["super+1"], "command": "open_related_rails_model" },
{ "keys": ["super+2"], "command": "open_related_rails_controller" },
{ "keys": ["super+3"], "command": "open_related_rails_view" },
{ "keys": ["super+4"], "command": "open_related_rspec_model" },
{ "keys": ["super+5"], "command": "open_related_rspec_controller" },
```

## How is it different from [Rails Related Files](https://github.com/luqman/SublimeText2RailsRelatedFiles) and other similar plugins?
`Rails Related Files` shows you a list of related files which you can choose from.

`Rails File Switcher` switches between MVC files instantly. If you are in your User model and you press ⌘+2 (if that's your binding), you will instantly see UsersController.

## Contributing
Pull requests are appreciated. If something isn't working, you can fix and send a pull request or simply create an issue to let me know of the bugs.

## CHANGELOG

### July 2, 2013
- Add support for `services` and `mailers`.

### June 24, 2013
- Add support for singularly-named controllers.
- Add support for jumping from a namespaced controller to a non-namespaced model.
- Add support for RSpec models and controllers.
- Show file creation popup for all types when the file doesn't exist, not only for views.

### June 18, 2013
- Add support for ST3, use branch `python3` (by @dsnipe)

### March 14, 2013
- Allow creating views when switching to a non-existent view.

### March 7, 2013
- Include key bindings by default (by @deiga).

### January 27, 2013
- Add support for namespaces.

### January 26, 2013
- When switching from a view to the controller the screen is centered at the action definition. If Vintage is enabled, it also moves the caret to the action definition.

### January 21, 2013
- Allow switching to model by putting the caret (and running `open_related_rails_model`) inside its name anywhere in the application.

### January 18, 2013
- Make it work when there are multiple apps opened in the side bar (previously would look for files only in the first app). Thanks to @ccodre for pointing out.

### December 25, 2012
- Initial release

## License
The plugin is released under the [MIT License](http://www.opensource.org/licenses/MIT)