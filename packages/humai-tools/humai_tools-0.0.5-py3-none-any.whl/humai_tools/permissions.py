import requests
from .directus import fetch_courses_by_id, fetch_course_data, patch_directus, search_directus, DirectusSearch
from . import campus
from .settings import Settings
from datetime import datetime
import pytz


def post_discord_permission(
        new_courses: list, member_mail: str, action_type: str,
        settings: Settings
    ) -> bool:
    """
    Request a tito para actualizar los accesos de los usuarios en discord
    """
    headers = {
        "accept": "application/json",
        "access_token": settings.tito_api_key,
    }

    discord_search = DirectusSearch(table='discord_info', field='mail', operator='_eq', value=member_mail)
    discord_response = search_directus(discord_search, settings.directus_access_token, settings.directus_base_url)
    if len(discord_response) == 1:
        discord_data = discord_response[0]
    else:
        print(f"Member {member_mail} not in discord_info")
        return False


    discord_data_post = {
        'user': discord_data['username']
    }
    if action_type == 'add':
        discord_access = set([access
            for access in discord_data.get('access', '').strip().split(',')
            if len(access) > 0])
        discord_data_post['access'] = ','.join(discord_access.union(set(new_courses)))

    elif action_type == 'remove':
        discord_data_post['access'] = 'restricted'
        
    discord_response = requests.post(f'{settings.tito_base_url}/set_permissions', params=discord_data_post, headers=headers)

    return discord_response.status_code == 200


def discord_add_role(role_name: str, settings: Settings, email: str = None, username: str = None):
    """
    Add a role to a user in career inscription
    """
    headers = {
        "accept": "application/json",
        "access_token": settings.tito_api_key,
    }
    discord_data_post = {
        'role_name': role_name,
        'email': email,
        'user': username
    }
    discord_response = requests.post(f'{settings.tito_base_url}/roles', params=discord_data_post, headers=headers)

    return discord_response.status_code == 200


def deactivate_membership(member_id: int, directus_token: str, directus_base_url: str) -> requests.Request:
    """"""
    print(f"Deactivating membership for {member_id}")
    table = 'members'
    churn_date = datetime.now(pytz.timezone('America/Argentina/Buenos_Aires')).strftime('%Y-%m-%dT%H:%M:%S')
    data = {'is_active': False, 'is_suscriptor': False, 'churn_date': churn_date}
    update_response = patch_directus(table, data, member_id, directus_token, directus_base_url)
    return update_response


def deactivate_contribution(member_id: int, directus_token: str, directus_base_url: str) -> requests.Request:
    """"""
    print(f"Deactivating contribution for {member_id}")
    table = 'members'
    churn_date = datetime.now(pytz.timezone('America/Argentina/Buenos_Aires')).strftime('%Y-%m-%dT%H:%M:%S')
    data = {'is_contributor': False, 'churn_date': churn_date}

    update_response = patch_directus(table, data, member_id, directus_token, directus_base_url)
    return update_response


def process_enroll_course(member_mail: str, course_keyname: str, settings: Settings):
    """
    Dar de alta al curso correspondiente al keyname
    """
    course_info = fetch_course_data(course_keyname, settings.directus_access_token, settings.directus_base_url)
    if settings.campus_access_token is None:
        campus_token = campus.get_campus_jwt_token(settings)
        settings.campus_access_token = campus_token

    enroll_status = campus.handle_campus_inscription(member_mail, course_info.get('code'), settings)
    if not enroll_status:
        print(f'Error en campus: {course_keyname} del usuario {member_mail}')


    discord_response = post_discord_permission([course_keyname], member_mail, action_type='add', settings=settings)
    if not discord_response:
        print(f'Error al asignar acceso a {course_keyname} en discord al usuario {member_mail}')


def process_enroll_career(member_mail: str, courses_ids: str, career_role: str, settings: Settings):
    """
    Dar de alta a los cursos correspondiente a la carrera
    """
    courses = fetch_courses_by_id(courses_ids, settings.directus_access_token, settings.directus_base_url)
    settings.campus_access_token = campus.get_campus_jwt_token(settings)
    courses_codes = [c["code"] for c in courses]

    campus_response = campus.handle_campus_inscription(member_mail, courses_codes, settings=settings)
    if not campus_response:
        # TBD: manejar error a la inscripcion del campus
        print('Error en la inscripcion')

    # Inscribe in discord
    discord_response = post_discord_permission([career_role], action_type='add', settings=settings, member_mail=member_mail)
    if not discord_response:
        print(f'Error al asignar el rol {career_role} en discord al usuario {member_mail}')


def process_cancel_membership(
        member_mail: str,
        settings: Settings,
        member_id: int
    ):
    """
    Funcion para gestionar la baja de un miembro
    """

    campus_token = campus.get_campus_jwt_token(settings.campus_client_id, settings.campus_client_secret)
    username = campus.get_campus_username(member_mail, campus_token)

    unenroll: bool = campus.unroll_campus_course(username, campus_token)
    # unenroll: bool = campus.unroll_all_campus_courses(username, campus_token)

    discord_response = post_discord_permission(
        ['restricted'], member_mail,
        action_type='remove', 
        settings=settings
    )
    if not discord_response:
        print(f'Error al remover acceso en discord al usuario {member_mail}')

    member_response = deactivate_membership(member_id, settings.directus_access_token, directus_base_url=settings.directus_base_url)
    if not member_response.ok:
        print(f'Error al desactivar al usuario {member_mail} de directus')

    return unenroll