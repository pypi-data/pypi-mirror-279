from functools import cached_property

from invenio_base.utils import obj_or_import_string


class OARepoVocabularies(object):
    """OARepo extension of Invenio-Vocabularies."""

    def __init__(self, app=None):
        """Extension initialization."""
        self.type_resource = None
        self.type_service = None
        if app:
            self.init_app(app)

    def init_app(self, app):
        """Flask application initialization."""
        self.app = app
        self.init_config(app)
        self.init_services(app)
        self.init_resource(app)
        app.extensions["oarepo-vocabularies"] = self

    def init_services(self, app):
        """Initialize services."""
        self.type_service = app.config["OAREPO_VOCABULARY_TYPE_SERVICE"](
            config=app.config["OAREPO_VOCABULARY_TYPE_SERVICE_CONFIG"](),
        )

    @cached_property
    def ui_cache(self):
        from oarepo_vocabularies.services.cache import VocabularyCache

        return obj_or_import_string(
            self.app.config.get("OAREPO_VOCABULARIES_UI_CACHE", VocabularyCache)
        )()

    def init_config(self, app):
        """Initialize configuration."""
        from . import config

        for k in dir(config):
            if k.startswith("OAREPO_VOCABULARIES_"):
                app.config.setdefault(k, getattr(config, k))
            if k.startswith("OAREPO_VOCABULARY_"):
                app.config.setdefault(k, getattr(config, k))
            if k.startswith("DATASTREAMS_CONFIG_GENERATOR_"):
                app.config.setdefault(k, getattr(config, k))
            elif k.startswith("DATASTREAMS_"):
                app.config.setdefault(k, {}).update(getattr(config, k))
            if k.startswith("VOCABULARIES"):
                app.config.setdefault(k, getattr(config, k))
        app.config.setdefault(
            "VOCABULARIES_FACET_CACHE_SIZE", config.VOCABULARIES_FACET_CACHE_SIZE
        )
        app.config.setdefault(
            "VOCABULARIES_FACET_CACHE_TTL", config.VOCABULARIES_FACET_CACHE_TTL
        )
        app.config.setdefault(
            "INVENIO_VOCABULARY_TYPE_METADATA", config.INVENIO_VOCABULARY_TYPE_METADATA
        )

        if "OAREPO_PERMISSIONS_PRESETS" not in app.config:
            app.config["OAREPO_PERMISSIONS_PRESETS"] = {}

        for k in config.OAREPO_VOCABULARIES_PERMISSIONS_PRESETS:
            if k not in app.config["OAREPO_PERMISSIONS_PRESETS"]:
                app.config["OAREPO_PERMISSIONS_PRESETS"][k] = (
                    config.OAREPO_VOCABULARIES_PERMISSIONS_PRESETS[k]
                )

    def init_resource(self, app):
        """Initialize resources."""
        self.type_resource = app.config["OAREPO_VOCABULARY_TYPE_RESOURCE"](
            config=app.config["OAREPO_VOCABULARY_TYPE_RESOURCE_CONFIG"](),
            service=self.type_service,
        )

    def get_config(self, vocabulary_name):
        if isinstance(vocabulary_name, dict):
            vocabulary_name = vocabulary_name.get("id")

        vocabulary_type_metadata = self.app.config.get(
            "INVENIO_VOCABULARY_TYPE_METADATA", {}
        )
        return vocabulary_type_metadata.get(vocabulary_name, {})
