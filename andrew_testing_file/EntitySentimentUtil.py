def get_text_entity_sentiment(text):
    from google.cloud import language
    from google.cloud.language_v1 import enums
    client = language.LanguageServiceClient()
    type_ = enums.Document.Type.PLAIN_TEXT
    language_ = "en"

    document = {"content": text, "type": type_, "language": language_}
    encoding_type = enums.EncodingType.UTF8

    response = client.analyze_entity_sentiment(document, encoding_type)
    for entity in response.entities:
        print(u"Representative name for the entity: {}".format(entity.name))
        print(u"Entity type: {}".format(enums.Entity.Type(entity.type).name))
        print(u"Salience score: {}".format(entity.salience))

        sentiment = entity.sentiment
        print(u"Entity sentiment score: {}".format(sentiment.score))
        print(u"Entity sentiment magnitude: {}".format(sentiment.magnitude))

        for metadata_name, metadata_value in entity.metadata.items():
            print(u"{} = {}".format(metadata_name, metadata_value))

        for mention in entity.mentions:
            print(u"Mention text: {}".format(mention.text.content))
            print(
                u"Mention type: {}".format(enums.EntityMention.Type(mention.type).name)
            )