# Rails File Switcher for Sublime Text 2
Rails File Switcher is a plugin for Sublime Text 2 that allows you to switch between Models, Controllers and Views. And how!

No popups, just immediately switches to the related file.

## Commands
### open_related_rails_model (super+1)
- Opens the related model from a controller or a view.
- If you put the cursor inside a model's name (like Po│st) and run the command, it will open the model from any place in the application.

### open_related_rails_controller (super+2)
- Opens the related controller from a model.
- Opens the related controller from a view. Centers the screen at the action definition. If Vintage is enabled, it also moves the caret to the action definition.

### open_related_rails_view (super+3)
- Opens the related view from a controller. You need to put the cursor inside the controller action for it to work.

## Bindings
Here are the default bindings. You can change them in `Preferences > Key Bindings - User`
```json
{ "keys": ["super+1"], "command": "open_related_rails_model" },
{ "keys": ["super+2"], "command": "open_related_rails_controller" },
{ "keys": ["super+3"], "command": "open_related_rails_view" },
```

## How is it different from [Rails Related Files](https://github.com/luqman/SublimeText2RailsRelatedFiles) and other similar plugins?
`Rails Related Files` shows you a list of related files which you can choose from.

`Rails File Switcher` switches between MVC files instantly. If you are in your User model and you press ⌘+2 (if that's your binding), you will instantly see UsersController.

## Contributing
Pull requests are appreciated. If something isn't working, you can fix and send a pull request or simply create an issue to let me know of the bugs.

## CHANGELOG

### March 7, 2013
- Include key bindings by default (by @deiga).

### January 27, 2013
- Add support for namespaces.

### January 26, 2013
- When switching from a view to the controller the screen is centered at the action definition. If Vintage is enabled, it also moves the caret to the action definition.

### January 21, 2013
- Allow switching to model by putting the cursor (and running `open_related_rails_model`) inside its name anywhere in the application.

### January 18, 2013
- Make it work when there are multiple apps opened in the side bar (previously would look for files only in the first app). Thanks to @ccodre for pointing out.

### December 25, 2012
- Initial release

## License
The plugin is released under the [MIT License](http://www.opensource.org/licenses/MIT)