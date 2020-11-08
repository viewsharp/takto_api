from aito.api import upload_entries, recommend
from aito.client import AitoClient
from django.conf import settings

client = AitoClient(
    instance_url=settings.AITO_INSTANCE_URL,
    api_key=settings.AITO_API_KEY,
)


def add_choices(entries):
    upload_entries(client, table_name='choice', entries=entries)


def get_recommendation(room_id):
    return recommend(
        client,
        query={
            "from": "choice",
            "where": {"room_id": room_id},
            "recommend": "business_id",
            "goal": {"chosen": True},
            "select": ["business_id"],
            "limit": 5
        }
    )
