# Rails File Switcher for Sublime Text 2
Rails File Switcher is a plugin for Sublime Text 2 that allows you to switch between Models, Controllers and Views. And how!

No popups, just immediately switches to the related file.

The plugin does not create any key bindings automatically, it's up to you to add them.

## Commands:
### open_related_rails_model
Opens the related model from a controller or a view.
If you put the cursor inside a model's name (like Po|st) and run the command, it will open the model from any place in the application.

### open_related_rails_controller
Opens the related controller from a model or a view.

### open_related_rails_view
Opens the related view from a controller. You need to put the cursor inside the controller action for it to work.

## Bindings
Here's how you can bind them to keys (Go to `Preferences > Key Bindings - User`)
```json
{ "keys": ["super+1"], "command": "open_related_rails_model" },
{ "keys": ["super+2"], "command": "open_related_rails_controller" },
{ "keys": ["super+3"], "command": "open_related_rails_view" },
```

## How is it different from [Rails Related Files](https://github.com/luqman/SublimeText2RailsRelatedFiles) and other similar plugins?
`Rails Related Files` shows you a list of related files which you can choose from.

`Rails File Switcher` switches between MVC files instantly. If you are in your User model and you press ⌘+2 (if that's your binding), you will instantly see UsersController.

This is the alpha version, if something is not working, create an issue.

## CHANGELOG

### January 21, 2013
- Allow switching to model by putting the cursor (and running `open_related_rails_model`) inside its name anywhere in the application.

### January 18, 2013
- Make it work when there are multiple apps opened in the side bar (previously would look for files only in the first app). Thanks to @ccodre for pointing out.

### Dec 25, 2012
- Initial release

## License
The plugin is released under the [MIT License](http://www.opensource.org/licenses/MIT)