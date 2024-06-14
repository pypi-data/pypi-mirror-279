import requests
import re
import base64
from .utils import generate_human_code
from .settings import Settings


def get_edx_id(course: dict) -> str:
    """Obtener el course_id a partir de la info en directus"""
    # course-v1:Humai+python+python17.8.23
    # return course[EDX_COURSE_ID_KEY]
    return f'course-v1:Humai+{course["keyname"]}+{course["code"]}'

def get_edx_id_from_code(course_code: str) -> str:
    """Obtener el course_id a partir del code del curso"""
    # course-v1:Humai+python+python17.8.23
    keyname = re.search(r"^\D+", course_code.replace(" ", "").lower())[0]
    return f'course-v1:Humai+{keyname}+{course_code}'


def get_campus_jwt_token(settings: Settings) -> str:
    """
    Obtiene el Auth token para poder realizar acciones de staff
    con la api del campus
    """
    auth_token = base64.b64encode(f'{settings.campus_client_id}:{settings.campus_client_secret}'.encode("utf-8")).decode("utf-8")
    headers = {
        "Authorization": f"Basic {auth_token}", 
        "Cache-Control": "no-cache"
    }
    data = {
        "grant_type": "client_credentials", 
        "token_type": "jwt"
    }

    r = requests.post(
        f"{settings.campus_base_url}/oauth2/access_token", headers=headers, data=data
    )

    if r.ok:
        settings.campus_access_token = r.json()["access_token"]
        return r.json()["access_token"]
    else:
        raise ValueError(f'Se genero un error al obtener el access_token (status {r.status_code})')
    

def create_campus_user(member_mail: str, username: str, name:str, settings: Settings,
                       password: str = None, course_id: str = None) -> str:
    """
    Crear un usuario en el campus de humai
    Args:
        password (optional): se genera un password nuevo si no se adjunta
    """
    if password is None:
        password = generate_human_code()

    print(f'Creando usuario con mail {member_mail}')
    headers = {'Authorization': f'JWT {settings.campus_access_token}'}
    create_user_data = {
        "email": member_mail,
        "name": name,
        "username": username,
        "password": password,
        "terms_of_service": "true",
    }

    # Enroll mientras se crea el usuario
    if course_id is not None:
        create_user_data['course_id'] = course_id

    # Se debe guardar la informacion de registro
    response_create = requests.post(f'{settings.campus_base_url}/api/user/v1/account/registration/', 
                                    data=create_user_data, headers=headers)

    if response_create.status_code == 200:
        print(f'El usuario {create_user_data["username"]} se creo con exito. password: {password}')

        return create_user_data["username"]

    elif response_create.status_code == 209:
        try:
            error_info = response_create.json()
            print(f'El error obtenido es {error_info.get("error_code")}')
        except Exception:
            pass
        print(f'El usuario con mail {member_mail} ya existe')

    else:
        print(f'Error {response_create.status_code} al crear al usuario con mail {member_mail}')


def get_campus_username(member_mail: str, settings: Settings) -> str:
    """
    Obtener el username de edX para poder realizar el resto de requests
    """
    params = {'email': member_mail}
    headers = {'Authorization': f'JWT {settings.campus_access_token}'}
    response_user = requests.get(f'{settings.campus_base_url}/api/user/v1/accounts', params=params, headers=headers)

    if response_user.status_code == 200:
        users: list = response_user.json()
        return users[0]['username']
    
    elif response_user.status_code == 401:
        print('Error: Not Athorized')

    elif response_user.status_code == 404:
        # No user exists with the specified mail
        print(f'Error: No existe usuario con mail {member_mail}')

    else:
        print(f'ERROR {response_user.status_code}: user_email {member_mail}')


def get_users_info(usernames: list, settings: Settings):
    headers={"Authorization": f"JWT {settings.campus_access_token}"}

    params = {
        'username': ",".join(usernames)
    }
    r = requests.get(f'{settings.campus_base_url}/api/user/v1/accounts', params=params, headers=headers)

    if r.ok:
        print('Info de los usuarios')
        return r.json()
    else:
        raise ValueError(f'Error: no se pudo obtener la informacion de {len(usernames)} usuarios')


def replace_campus_username(old_username: str, new_username: str, settings: Settings) -> bool:
    """
    Actualizar el username de una persona por uno nuevo
    """
    headers = {'Authorization': f'JWT {settings.campus_access_token}'}
    post_data = {
        'username_mappings': [
            {old_username: new_username}
        ]
    }
    response = requests.get(f'{settings.campus_base_url}/api/user/v1/accounts/replace_usernames/', json=post_data, headers=headers)

    if response.status_code == 200:
        usernames = response.json()
        print(usernames.get('successful_replacements'))
        print(f'Se actualizo el usuario {old_username} con el nuevo username {new_username}')
        return True
    
    else:
        print(f'ERROR {response.status_code}: user_email {old_username}. {response.text}')
        return False


def handle_campus_inscription(
        member_mail: str, courses_code: str, settings: Settings,
        action: str = "enroll", auto_enroll: bool = True, email_students: bool = False,
    ) -> bool:
    """
    Args:
        member_mail: member mail used to send enroll notification
        course_id: id generated in OpenEdx
        auto_enroll (bool): inscribe al usuario de forma automatica una vez registrado
        email_students (bool): el usuario recibe un email con la notificacion de la accion
    Info:
        action: determina el comportamiento segun los valores "enroll" o "unenroll"
    Returns:
        bool: the status of the request
    """

    if action not in ["enroll", "unenroll"]:
        print(f"Error invalid action argument: {action}")
        return False

    courses_ids = [get_edx_id_from_code(course_code) 
                   for course_code in courses_code.split(",")]
    headers = {
        'Authorization': f'JWT {settings.campus_access_token}'
    }
    data = {
        'action': action,
        'identifiers': member_mail,
        'auto_enroll': auto_enroll,
        'email_students': email_students,
        'courses': ','.join(courses_ids)
    }

    r = requests.post(f'{settings.campus_base_url}/api/bulk_enroll/v1/bulk_enroll', headers=headers, json=data)

    if r.status_code == 200:
        print(f'CAMPUS: El usuario {member_mail} se inscribio correcamente a {courses_code}')
    else:
        print(f'ERROR CAMPUS: no se inscribio al usuario {member_mail} a {courses_code}')

    return r.status_code == 200


def get_enrollments(username: str = None, course_id: str = None, settings: Settings = None):
    """
    Return all the inscriptions from a user or course.
    token: pass as argument `access_token` or assign `CAMPUS_ACCESS_TOKEN` env variable
    """

    headers={"Authorization": f"JWT {settings.campus_access_token}"}
    data = list()

    params = {
        'page_size': 300
    }
    if username is not None:
        params['username'] = username

    if course_id is not None:
        params['course_id'] = course_id

    r = requests.get(f'{settings.campus_base_url}/api/enrollment/v1/enrollments', params=params, headers=headers)

    if r.ok:
        print(f'Inscripciones status: {r.status_code}, next: {r.json()["next"]}')
        data.extend(r.json()['results'])
        while r.json()["next"]:
            r = requests.get(r.json()["next"], params=params, headers=headers)
            if r.ok:
                data.extend(r.json()['results'])
        return data
    else:
        raise ValueError('Error: no se pudo obtener la informacion de inscripciones.')


def enroll_campus_course(username: str, course_id: str, settings: Settings) -> bool:
    """Dar de alta en el curso especificado"""

    headers = {'Authorization': f'JWT {settings.campus_access_token}'}
    enroll_data = {
        'user': username,
        'is_active': True,
        'course_details': {'course_id': course_id},
    }
    enroll_response = requests.post(f'{settings.campus_base_url}/api/enrollment/v1/enrollment', headers=headers, json=enroll_data)

    if enroll_response.status_code == 200:
        print(f'The user {username} has been successfully enrolled in {course_id}')
        enrollments: dict = enroll_response.json()
        user_courses = enrollments['course_details']['course_name']
        print(f'User enrolled to {user_courses}')
        return True
    
    else:
        print(f'ERROR {enroll_response.status_code} with enroll user {username} in course {course_id}')
        return False


def unroll_campus_course(username: str, settings: Settings, course_id: str = None) -> bool:
    """
    Dar de baja a un usuario a un curso unico o todos en edX
        course_id != None: dar de baja al curso especifico (Bearer token)
        course_id == None: dar de baja a todos los cursos  (JWT token)
    """
    unrollments_names = list()
    headers = {'Authorization': f'JWT {settings.campus_access_token}'}

    if course_id is not None:
        courses_ids = course_id.split(',')
    else: 
        courses_ids = [c.get('course_id') for c in get_enrollments(username=username, settings=settings) if c.get('is_active')]

    for id in courses_ids:
        unenroll_data = {
            'user': username,
            'is_active': False,
            'course_details': {'course_id': id},
        }
        response = requests.post(f'{settings.campus_base_url}/api/enrollment/v1/enrollment', headers=headers, json=unenroll_data)

        if response.status_code == 200:
            course_name = response.json().get('course_details', {}).get('course_name')
            unrollments_names.append(course_name)
        else:
            print(f'ERROR {response.status_code}: with user {username} in course {id}')

    # Para debug
    if len(unrollments_names) > 0:
        print(f'El usuario {username} se dio de baja a {unrollments_names}')
    
    return len(unrollments_names) > 0


def unroll_all_campus_courses(username: str, settings: Settings) -> bool:
    """
    Unenroll username to all courses
    https://github.com/openedx/edx-platform/blob/master/openedx/core/djangoapps/enrollments/views.py#L389

    Unused because returns: 404 Error with text 'No retirement request status for username.'
    """
    headers = {'Authorization': f'JWT {settings.campus_access_token}'}
    unenroll_data = {
        'username': username
    }
    response = requests.post(f'{settings.campus_base_url}/api/enrollment/v1/unenroll', headers=headers, json=unenroll_data)


    if response.status_code == 200:
        unenrollments: list = response.json()
        # user_courses = unenrollments['course_details']['course_name']
        print(f'User unenrolled from {unenrollments}')
        return True
    
    if response.status_code == 204:
        print('The user is already unenrolled from all courses')
        return True
    
    else:
        print(f'ERROR {response.status_code}: with user {username} in unroll all')
        return False
    

def get_campus_courses_info(settings: Settings) -> list:
    """Obtener informacion basica de los cursos del campus"""
    headers={"Authorization": f"JWT {settings.campus_access_token}"}
    course_info = list()
    r = requests.get(f'{settings.campus_base_url}/api/courses/v1/courses/', headers=headers)

    if r.ok:
        course_info.extend(r.json()['results'])
        while (new_url := r.json()["pagination"].get("next")):
            r = requests.get(new_url, headers=headers)
            if r.ok:
                course_info.extend(r.json()['results'])
        print(f'Informacion cursos, next: {r.json()["pagination"].get("next")}')
        return course_info
    else:
        raise ValueError(f'Error: {r.text}.')


def get_problems_content(code: str, settings: Settings, keyname: str = None):
    
    headers={"Authorization": f"JWT {settings.campus_access_token}"}
    responses = list()

    if keyname is None or len(keyname) == 0:
        keyname = re.search(r'^\D+', code)[0]

    r = requests.get(f'{settings.campus_base_url}/api/grades/v1/submission_history/course-v1%3AHumai%2B{keyname}%2B{code}/', headers=headers)

    if not r.ok:
        print('Se genero un erro en la primera iteracion')
        print(r.text)
        return []

    if len(r.json()['results']) == 0:
        raise ValueError(f"No se pudo obtener datos del curso {keyname}+{code}.\
            Revisar el keyname o code asignado en el campus"
        )

    responses += r.json()['results']
    while r.json().get('next') is not None:
        r = requests.get(r.json()['next'], headers=headers)

        if r.ok:
            responses += r.json()['results']

    return responses


def get_xblocks(code: str, settings: Settings):
    headers={"Authorization": f"JWT {settings.campus_access_token}"}

    params = {
        'username': 'admin',
        'depth': 'all',
        'block_types_filter': 'problem',
        'student_view_data': 'problem',
        'return_type': 'list',
        'course_id': get_edx_id_from_code(code)
    }
    url = f'{settings.campus_base_url}/api/courses/v2/blocks/'
    r = requests.get(url, params=params, headers=headers)

    if r.ok:
        print('Info de problemas')
        return r.json()
    else:
        raise ValueError(f'Error: {r.status_code} - {r.text}')