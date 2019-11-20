
from azure.cognitiveservices.language.luis.authoring import LUISAuthoringClient
from msrest.authentication import CognitiveServicesCredentials

import datetime, json, os, time

authoring_key = "bde233f61f5e4e3fa48ff5a11b0f304c"

region = "westus"

endpoint = "https://{}.api.cognitive.microsoft.com".format(region)


# Instatiating a LUIS client
client = LUISAuthoringClient(endpoint, CognitiveServicesCredentials(authoring_key))

def create_app():
    # Creating an new LUIS app
    app_name    =   "Fredchex AI"
    app_desc    =   "Terraform and Ansible assistant for Fredchex project"
    app_version =   "0.1"
    app_locale  =   "en-us"

    app_id = client.apps.add(dict(name=app_name,
                                    initial_version_id=app_version,
                                    description=app_desc,
                                    culture=app_locale))

    print("Fredchex AI app {} has been created\n with ID {}".format(app_name,app_id))

    return app_id, app_version



def add_intents(app_id, app_version):
    intentId = client.model.add_intent(app_id, app_version, "CreateResource")

    print("Intent CreateResource {} has been added.".format(intentId))


def  add_entities(app_id, app_version):
    resourceCategoryEntityId = client.model.add_entity(app_id, app_version, "Resource Category")
    print("resourceCategoryEntityId {} has been added.".format(resourceCategoryEntityId))

    resourceTypeId = client.model.create_entity_role(app_id, app_version, resourceCategoryEntityId, "Resource Type")
    print("resourceTypeId {} has been added.".format(resourceTypeId))

    numberOfResource = client.model.create_entity_role(app_id, app_version, resourceTypeId, "Number of Resource")
    print("numberOfResource {} has been added.".format(numberOfResource))

    client.model.add_prebuilt(app_id, app_version, prebuilt_extractor_names=["keyPhrase", "number"])

    compositeEntityId = client.model.add_composite_entity(app_id, app_version, name="Resource",
                                    children=["Resource Category", "Resource Type", "number", "keyphrase"])

    print("compositeEntityId {} has been added.".format(compositeEntityId))


def add_utterances(app_id, app_version):
    # Adding some sample utterances that a speaker may provide as an input.
    utterances = [create_utterance("Hey Terraform", "Can you create one virtual machine for me",
                                        ("Resource", "Terraform"),
                                        ("Resource Type", "Virtual Machine"),
                                        ("Number of Resource", "one")),                                        
                  create_utterance("Hey Terraform", "Can you create two virtual machine for me",
                                        ("Resource", "Terraform"),
                                        ("Resource Type", "Virtual Machine"),
                                        ("Number of Resource", "two")),
                  create_utterance("Hey Ansible", "Can you create one apache server for me",
                                        ("Resource", "Ansible"),
                                        ("Resource Type", "Apache server"),
                                        ("Number of Resource", "one")),
                  create_utterance("Hey Ansible", "Can you create one Minecraft server for me",
                                        ("Resource", "Ansible"),
                                        ("Resource Type", "Minecraft server"),
                                        ("Number of Resource", "one"))]

    client.examples.batch(app_id, app_version, utterances)
    print("{} example utterance(s) has been added.".format(len(utterances)))


def train_app(app_id, app_version):
    response = client.train.train_version(app_id, app_version)
    waiting = True

    while waiting:
        info = client.train.get_status(app_id, app_version)

        # Method get_status returns a list of training statuses, one for each model.
        # Loop through them and make sure all are done.

        waiting = any(map(lambda x: "Queued" == x.details.status or "InProgress" == x.details.status, info))
        if waiting:
            print("Waiting 10 seconds for training to complete...")
            time.sleep(10)

