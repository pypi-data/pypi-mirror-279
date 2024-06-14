from pydantic import BaseModel
import requests
from .settings import Settings


class DirectusSearch(BaseModel):
    table: str
    field: str
    operator: str
    value: str


def fetch_course_data(course_keyname, access_token, directus_base_url):
    """Refactor these functions, we could have only one search function"""
    course_search = DirectusSearch(
        **{
            "table": "courses",
            "field": "keyname",
            "operator": "_eq",
            "value": course_keyname,
        }
    )
    course_data = search_directus(course_search, access_token, directus_base_url)
    if course_data:
        open_courses = [c for c in course_data if c["inscription_open"]]
        if len(open_courses) > 1:
            raise Exception(f"Multiple open courses found for {course_keyname}")
        else:
            course = open_courses[0]
            return course
    else:
        print(f"Course {course_keyname} not found")


def fetch_courses_by_id(courses_ids: list, directus_access_token: str, directus_base_url: str):
    """
    Al inscribirse a varios cursos contamos con una lista de ids
    pero no de sus keynames. Para esto buscamos obtener la info de los cursos
    """
    courses_search = DirectusSearch(**{"table": 'courses', "field": "id", "operator": "_in", "value": courses_ids})
    courses = search_directus(courses_search, directus_access_token, directus_base_url)

    return courses


def fetch_product_data(product_keyname, access_token, directus_base_url):
    product_search = DirectusSearch(
        **{
            "table": "products",
            "field": "product_keyname",
            "operator": "_eq",
            "value": product_keyname,
        }
    )
    product_data = search_directus(product_search, access_token, directus_base_url)
    if product_data:
        if len(product_data) > 1:
            raise Exception(f"Multiple products found for {product_keyname}")
        else:
            product = product_data[0]
            return product
    else:
        print("Course not found")


def search_directus(search: DirectusSearch, access_token, directus_base_url) -> list:
    """Applies search in table. This "directus search" is because I couldnt filter by passing a
    dictionary as the documentation specifies."""
    url = f"{directus_base_url}/items/{search.table}?filter[{search.field}][{search.operator}]={search.value}"
    headers = {"Authorization": f"Bearer {access_token}"}
    r = requests.get(url, headers=headers)
    data = r.json().get("data", [])
    if r.ok:
        if (n := len(data)) == 1:
            return data
        elif n > 1:
            print("Multiple results found")
            return data
        else:
            print("No Directus results found")
            return data
    else:
        raise Exception(f"Error in Directus search {r.url}")


def fetch_all(
    table: str, access_token: str, directus_base_url: str, limit: int = -1
) -> list:
    """
    Applies search in table. This "directus search" is because I couldnt filter by passing a
    dictionary as the documentation specifies.

    Args:
        table: name of directus table to fetch
        access_token: directus token
        directus_base_url: directus app url
        limit: amount of register fetched (default is -1, means unlimited)

    Returns: a list of the data where each item is a row.

    """
    url = f"{directus_base_url}/items/{table}"
    headers = {"Authorization": f"Bearer {access_token}"}
    r = requests.get(url, headers=headers, params={"limit": limit})
    if r.ok:
        return r.json()["data"]
    else:
        raise Exception(
            f"Error in Directus search {r.url}, {r.content}, {r.status_code}"
        )


def post_directus(
    table: str, data: dict, access_token: str, directus_base_url: str
) -> requests.Response:
    """Post data to table"""
    url = f"{directus_base_url}/items/{table}"
    headers = {"Authorization": f"Bearer {access_token}"}
    r = requests.post(url, json=data, headers=headers)
    return r


def patch_directus(
    table: str, data: dict, item_id: str, access_token: str, directus_base_url: str
) -> requests.Response:
    """Update item in table"""
    url = f"{directus_base_url}/items/{table}/{item_id}"
    headers = {"Authorization": f"Bearer {access_token}"}
    r = requests.patch(url, json=data, headers=headers)
    return r

def get_coupon_usage_count(coupon, directus_token, directus_base_url):
    directus_headers = {'Authorization': f'Bearer {directus_token}'}
    get_pre_insc_url = f"{directus_base_url}/items/pre_inscription_info/?filter[coupon_code][_eq]={coupon}"
    pre_ins_info_response = requests.get(get_pre_insc_url, headers=directus_headers)

    mp_ext_ref = set()
    pp_ext_ref = set()
    uses = 0
    for pre_insc in pre_ins_info_response.json()['data']:
        if pre_insc.get('payment_platform') == 'mercadopago':
            mp_ext_ref.add(pre_insc.get('external_reference'))
        if pre_insc.get('payment_platform') == 'paypal':
            pp_ext_ref.add(pre_insc.get('external_reference'))
    
    if len(mp_ext_ref) > 0:
        params = {
            'filter[external_reference][_in]': list(mp_ext_ref)
        }
        mp_response = requests.get(f"{directus_base_url}/items/Payments", headers=directus_headers, params=params)
        if mp_response.ok:
            uses += len(set((payment.get('external_reference') for payment in mp_response.json()['data'])))

    if len(pp_ext_ref) > 0:
        params = {
            'filter[external_reference][_in]': list(pp_ext_ref)
        }
        pp_response = requests.get(f"{directus_base_url}/items/pp_payments", headers=directus_headers, params=params)
        if pp_response.ok:
            uses += len(set((payment.get('external_reference') for payment in pp_response.json()['data'])))

    # uses = len(pre_ins_info_response.json()['data'])
    return uses


def fetch_coupon_discount(coupon, access_token, directus_base_url):
    MEMBER_CODE_DISCOUNT = 20
    if not coupon:
        return {"discount": 0, "type": "None"}

    coupon_search = DirectusSearch(
        **{"table": "coupons", "field": "coupon", "operator": "_eq", "value": coupon}
    )
    coupon_data = search_directus(coupon_search, access_token, directus_base_url)
    if coupon_data:
        # Search in member table
        if not (n := coupon_data[0]['max_uses']):
            return {
                "discount": coupon_data[0]["discount"],
                "type": coupon_data[0]["type"],
            }
        else:
            coupon_usage_count = get_coupon_usage_count(coupon, access_token, directus_base_url)
            if  n > coupon_usage_count:
                return {
                    "discount": coupon_data[0]["discount"],
                    "type": coupon_data[0]["type"],
                }
            else:
                print(f'Coupon {coupon} no longer available.')

    member_coupon_search = DirectusSearch(
        **{
            "table": "members",
            "field": "member_code",
            "operator": "_eq",
            "value": coupon,
        }
    )
    member_coupon_data = search_directus(
        member_coupon_search, access_token, directus_base_url
    )
    if member_coupon_data:
        return {"discount": MEMBER_CODE_DISCOUNT, "type": "Member"}

    return {"discount": 0, "type": "None"}


def get_mail_info_directus(email_name: str, access_token, directus_base_url):
    """Obtener el mail de bienvenida desde directus"""
    # deberia estar en humai tools

    email_search_body = {
        "table": "emails",
        "field": "name",
        "operator": "_eq",
        "value": email_name,
    }  # complete value to send mail when is unique course payment
    email_info_search = DirectusSearch(**email_search_body)
    email_info_response = search_directus(
        search=email_info_search,
        directus_base_url=directus_base_url,
        access_token=access_token,
    )
    return email_info_response

def insert_user_event(
    member_id: str,
    event_type: str,
    settings: Settings,
    reason: str = "",
    product_credits: int = 0,
) -> bool:
    """"""
    event_to_insert = {
        "category": "credits",
        "member_id": int(member_id),
        "event_type": event_type,
        "amount": product_credits,
        "description": reason
    }

    post_response = post_directus(
        table="user_events",
        data=event_to_insert,
        access_token=settings.directus_access_token,
        directus_base_url=settings.directus_base_url,
    )

    if post_response.status_code == 200:
        print(f"member {member_id} user_event has been inserted.")
        return True
    else:
        print(f"member {member_id} user_event has not been inserted.")
        return False
