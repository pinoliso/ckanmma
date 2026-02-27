import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from .routes import mma_blueprint


class MmaPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IBlueprint)
    plugins.implements(plugins.ITemplateHelpers)

    def update_config(self, config):
        toolkit.add_template_directory(config, 'templates')
        toolkit.add_public_directory(config, 'public')

    def get_blueprint(self):
        return mma_blueprint

    def get_helpers(self):
        return {
            'mma_group_list': self.mma_group_list
        }

    def mma_group_list(self):
        context = {'ignore_auth': True}
        data_dict = {'all_fields': True}
        return toolkit.get_action('group_list')(context, data_dict)
    