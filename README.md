# Rails File Switcher for Sublime Text 2
Rails File Switcher is a plugin for Sublime Text 2 that allows you to switch between Models, Controllers and Views. And how!

No popups, just immediately switches to the related file.

*Note: To open a related view, put the cursor inside the controller action.*

The plugin does not create any key bindings automatically, it's up to you to add them.

There are 3 commands:
* `open_related_rails_model`
* `open_related_rails_controller`
* `open_related_rails_view`

Here's how you can bind them to keys (Go to `Preferences > Key Bindings - User`)
```json
{ "keys": ["super+1"], "command": "open_related_rails_model" },
{ "keys": ["super+2"], "command": "open_related_rails_controller" },
{ "keys": ["super+3"], "command": "open_related_rails_view" },
```

## How is it different from [Rails Related Files](https://github.com/luqman/SublimeText2RailsRelatedFiles)?
`Rails Related Files` shows you a list of related files which you can choose from.

`Rails File Switcher` switches between MVC files instantly. If you are in your User model and you press ⌘+2 (if that's your binding), you will instantly see UsersController.

This is the alpha version, if something is not working, create an issue.