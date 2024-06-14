# Notitia core - pluggable payload procesing - everything is famous.. sort of..

```python
import motor.motor_asyncio
from bstk_notitia import Notitia

# An Investigator looks for and specialises in dealing with particular types of cases
# Observers watch for information that may or may not be useful to an investigator
# Informants provide new or supporting information upon request by the investigator
# Reporters are used by the investigator to disseminate information and receive feedback

# Only certain cases get investigated
# The investigator decides what cases to take
# Each case must run to completion, even if completion means new cases are created

motor_client = motor.motor_tornado.AsyncIOMotorClient(host=['localhost:27017'])

notitia = Notita(
    department="08e32fd8-9259-4a3e-891a-bc39b7c8ef22", # [str | None] - for tenancy isolation
)

notitia.set_driver(
    driver="mongodb"
    driver_settings={
        "async_client": motor_client,
        "database": 'myappdb',
        "collection_prefix": "bn_",
        "archive_suffix": "_arch",
        "completion_action": "immoliate",
    },
)

notitia.enlist(investigator="portaone/espf")

espf_payload = {
    "event-type": "Test/Event",
    "variables": {
        "i_event": 1,
        "i_account": 999
    }
}

# A valid case
try:
    case = await notitia.dispatch(
        observer="portaone/espf",
        information=espf_payload,
        completion_action="archive". # [archive | immoliate | None]
    )
    print(f"Tracking case as {case.number}")
except NotitiaInvalidCasePayloadException as ex:
    print(f"Invalid Payload: {ex.message}")

async for movement in notitia.spy(case):
    print(f"Case moved {movement.id}")


```