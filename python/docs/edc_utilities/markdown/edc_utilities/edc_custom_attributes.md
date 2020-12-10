Module edc_utilities.edc_custom_attributes
==========================================

Classes
-------

`EDCCustomAttribute(settings_ref=None, configuration_file=None)`
:   Class to get, add, update, delete custom attributes
    
    Instance initialization
        settings_ref is a reference to an existing generic_settings object. If None, the settings will be collected
        from the configuration_file mentioned in the configuration_file argument
        If both settings_ref and configuration_file are set, the configuration_file argument will be ignored.

    ### Methods

    `create_custom_attribute(self, custom_attribute_values=None)`
    :   Create new custom attribute
        Will fail if attribute already exists

    `delete_custom_attribute(self, name='dummy', ignore_already_gone=True)`
    :   Delete a give custom attribute

    `fill_in_jinja_template_custom_attributes(self, the_template, custom_attribute_values)`
    :   the_template must be a Template object as retrieved through get_jinja_template

    `get_custom_attribute(self, name='dummy', expect_to_exist=True)`
    :   Get the EDC attribute
        This is an expensive operation, so we should cache it

    `reconnect(self)`
    :

    `update_custom_attribute(self, name='dummy')`
    :   Update a give custom attribute