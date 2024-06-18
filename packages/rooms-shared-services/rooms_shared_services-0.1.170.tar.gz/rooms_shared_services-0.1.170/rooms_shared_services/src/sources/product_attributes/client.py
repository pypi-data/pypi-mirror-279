from uuid import UUID

from rooms_shared_services.src.models.products.attributes import ProductAttribute
from rooms_shared_services.src.models.texts.languages import Language
from rooms_shared_services.src.storage.dynamodb import DynamodbStorageClient
from rooms_shared_services.src.translation.client import TranslationClient
from rooms_shared_services.src.translation.providers.aws import AWSTranslationProvider


class ProductAttributeClient(object):
    def __init__(
        self,
        storage_client: DynamodbStorageClient,
        name_language_indexname: str,
    ) -> None:
        """Set Attributes.

        Args:
            storage_client (DynamodbStorageClient): _description_
            name_language_indexname (str): _description_
        """
        self.storage_client = storage_client
        self.name_language_indexname = name_language_indexname

    def retrieve_attribute(self, attr_id: UUID, language: Language):
        key = {"attr_id": attr_id, "attr_language": language}
        attr_data = self.storage_client.retrieve(key=key)
        return ProductAttribute.validate_dynamodb_item(attr_data)

    def save_attribute(self, product_attribute: ProductAttribute) -> dict:
        table_item = product_attribute.dynamodb_dump(exclude_unset=False)
        print("table_item: {}".format(table_item))
        return self.storage_client.create(table_item=table_item)

    def create_attribute(self, attr_name: str, attr_language: Language, attr_terms: list[str]) -> dict:
        product_attribute = ProductAttribute(attr_name=attr_name, attr_language=attr_language, attr_terms=attr_terms)
        return self.save_attribute(product_attribute=product_attribute)

    def create_all(self, attr_dict: dict):
        for attr_name in attr_dict:
            attr_params = {"attr_name": attr_name, "attr_language": Language.en, "attr_terms": attr_dict[attr_name]}
            self.create_attribute(**attr_params)

    def iterate_page_attributes(self, page: list[dict]):
        for prod_item in page:
            prod_item["attr_language"] = getattr(Language, prod_item["attr_language"]).value
            yield ProductAttribute.validate_dynamodb_item(prod_item)

    def iterate_attributes(self, language: Language = Language.en):
        filter_by = {"attr_language": language.name}
        for page in self.storage_client.get_by_pages(filter_by=filter_by):
            yield from self.iterate_page_attributes(page)

    def create_translated_attribute(self, product_attribute: ProductAttribute, translation: dict, language: Language):
        model_params = {
            "id": product_attribute.id,
            "attr_name": translation["attr_name"],
            "attr_terms": translation["attr_terms"],
            "attr_language": language.value,
        }
        translated_attribute = ProductAttribute.model_validate(model_params)
        self.save_attribute(product_attribute=translated_attribute)

    def translate_all(self, language: Language):
        for product_attribute in self.iterate_attributes():
            translation = self.translate_attribute(product_attribute=product_attribute, language=language)
            self.create_translated_attribute(
                product_attribute=product_attribute,
                translation=translation,
                language=language,
            )

    def translate_name(
        self,
        product_attribute: ProductAttribute,
        language: Language,
        translations: dict,
        translation_client: TranslationClient,
    ):
        translations["attr_name"] = getattr(
            translation_client.bulk_translate(
                source_language=Language.en,
                target_languages=[language],
                txt=product_attribute.attr_name,
            ),
            language.name,
        )

    def translate_terms(
        self,
        product_attribute: ProductAttribute,
        language: Language,
        translations: dict,
        translation_client: TranslationClient,
    ):
        translated_terms = []
        for term in product_attribute.attr_terms:
            translated_terms.append(
                getattr(
                    translation_client.bulk_translate(
                        source_language=Language.en,
                        target_languages=[language],
                        txt=term,
                    ),
                    language.name,
                ),
            )
        translations["attr_terms"] = translated_terms

    def translate_attribute(self, product_attribute: ProductAttribute, language: Language):
        translations = {}
        provider = AWSTranslationProvider()
        translation_client = TranslationClient(provider=provider)
        self.translate_name(
            product_attribute=product_attribute,
            language=language,
            translations=translations,
            translation_client=translation_client,
        )
        self.translate_terms(
            product_attribute=product_attribute,
            language=language,
            translations=translations,
            translation_client=translation_client,
        )
        return translations
