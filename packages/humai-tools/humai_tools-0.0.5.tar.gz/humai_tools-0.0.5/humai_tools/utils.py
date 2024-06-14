from datetime import datetime, timedelta
import uuid
import unidecode
from random import choices, randint
import requests
import pytz
from .settings import Settings

INSCRIBE_CF_URL = 'https://us-central1-humai-cloud.cloudfunctions.net/cf_courses'
# PRIVILEGED_TOKEN = os.getenv('PRIVILEGED_TOKEN')

def timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def generate_uuid():
    return str(uuid.uuid4())

def normalize(s):
    return unidecode.unidecode(s.lower().strip().replace(' ', '_'))

def generate_human_code():
    WORDS_URL = 'https://storage.googleapis.com/humai-datasets/nlp/borges_words.csv'
    words = requests.get(WORDS_URL).text.strip().split(',')
    return f"{choices(words)[0]}{''.join(str(randint(0,9)) for _ in range(3))}"


def inscribe_user(email: str, keyname: str, privileged_token: str = None, inscribe_cf_url: str = INSCRIBE_CF_URL) -> bool:
    """Inscripcion a un curso especifico utilizando `cf_courses` Cloud Function"""
    print(f"INFO inscribing {email} to {keyname}")
    data = {"action": "inscribe",
            'email': email,
            'keyname': keyname,
            'privileged_token': privileged_token}
    r = requests.post(inscribe_cf_url, json=data)
    print(f"inscribe cf response code = {r.status_code}")
    return r.ok


def inscribe_user_several_courses_by_id(email: str, courses_ids: list, privileged_token: str = None, inscribe_cf_url: str = INSCRIBE_CF_URL) -> bool:
    """Inscripcion a los cursos de una carrera utilizando `cf_courses` Cloud Function"""
    print(f"INFO inscribing {email} to courses ids {courses_ids}")
    data = {"action": "inscribe_several",
            'email': email,
            'courses_ids': courses_ids,
            'privileged_token': privileged_token}
    r = requests.post(inscribe_cf_url, json=data)
    print(f"inscribe cf response code = {r.status_code}")
    return r.ok


def get_member_inscriptions(member_id: int, directus_token: str, directus_base_url: str) -> list:
    """Obtener todos los registros de user_course del miembro member_id"""
    print(f"Getting inscriptions for member {member_id}")
    user_course_url = f"{directus_base_url}/items/user_course"
    headers = {"Authorization": f"Bearer {directus_token}"}
    params = {
        "filter[_and][0][member_id][_eq]": member_id,
        "filter[_and][1][course_id][_nnull]": "true",
        "fields[]": ["id", "course_id.id", "course_id.end_date", "course_id.keyname",  "course_id.name", "course_id.code", "course_id.discord_channel"]
    }
    get_usercourse_response = requests.get(user_course_url, headers=headers, params=params)
    user_course_info = get_usercourse_response.json().get('data', [])
    if len(user_course_info) == 0:
        print(f"User with member id  {member_id}, has not been inscribed in any course.")
        return []# None
    else:
        return user_course_info


def remove_member_inscription(member_id: int, user_course_info: list, settings: Settings) -> list:
    """"""
    print("removing course inscriptions")
    user_course_url = f"{settings.directus_base_url}/items/user_course"
    headers = {"Authorization": f"Bearer {settings.directus_access_token}"}
    # remove courses that hasn't finished neither started.
    user_course_ids_to_remove = []
    removed_course_keynames = []
    removed_course_info = []
    for user_course in user_course_info:
        print(f"user_course object {user_course}")
        if user_course["course_id"].get("end_date") is not None:
            end_date: datetime = datetime.fromisoformat(user_course["course_id"]["end_date"])
        else:
            end_date: datetime = datetime.now() + timedelta(days=1)
        print(f"course hasn't finished: {end_date > datetime.now()}")
        # Check for churn_date to not overwrite the past churn_date
        if end_date > datetime.now() and user_course.get('churn_date') is None:
            # the course hasn't finish
            user_course_ids_to_remove.append(user_course["id"])
            removed_course_keynames.append(user_course["course_id"]["keyname"])
            removed_course_info.append(user_course["course_id"])

    # update churn_date of courses
    if len(user_course_ids_to_remove) > 0:
        data = {
            "keys": user_course_ids_to_remove,
            "data": {
                "churn_date": datetime.now(pytz.timezone('America/Argentina/Buenos_Aires')).strftime('%Y-%m-%dT%H:%M:%S')
            }
        }
        update_response = requests.patch(user_course_url, headers=headers, json=data)

        if update_response.status_code == 200:
            print(f"Inscriptions for user with id {member_id} has been updated for courses {removed_course_keynames}")
        else:
            print(f"ERROR: Inscriptions could not be updated for user with id {member_id}, something has been wrong.")
    else:
        print(f"User with member id {member_id} has not active or incoming courses.")

    return removed_course_info


def send_discord_message(
        message, settings: Settings,
        channel_name: str = 'bugs-y-mejoras', thread: str = None
    ) -> bool:
    """
    Enviar un mensaje de notificacion al canal de discord
    :param message: mensaje con la informacion a enviar en el canal
    :param channel_name: nombre especifico del canal del servidor de discord
    """
    
    tito_headers = {
        "accept": "application/json",
        "access_token": settings.tito_api_key,
    }
    data = {
        'message': message,
        'channel_name': channel_name,
        'thread_name': thread
    }
    response = requests.post(f'{settings.tito_base_url}/send', params=data, headers=tito_headers)

    print(f'Se ejecuto envio el mensaje al canal {channel_name}: status code {response.status_code}')

    return response.ok
