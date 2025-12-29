import json
import pydash as _
from curl_cffi import requests
from concurrent.futures import ThreadPoolExecutor

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en',
    'authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRhIjp7InNvdXJjZSI6IkFQUCIsInVjaWQiOiI5MGZjZDMwNi0yMTljLWNlNmYtMzEwYi00NjgzZWIyZTgwZjQifSwiZXhwIjoxNzYwOTU3MzMyLCJpYXQiOjE3NjA5NTM3MzIsImp0aSI6ImZjMjQ4YTEzLWFkOTktMTFmMC04MWY2LWQ2NTM1YzhlZGFmMiJ9.SGP7Kfan8I7GozkGb-EPUMmBar58sIxPu8x8nVm6kKE',
    'origin': 'https://www.delhivery.com',
    'priority': 'u=1, i',
    'referer': 'https://www.delhivery.com/',
    'sec-ch-ua': '"Google Chrome";v="141", "Not?A_Brand";v="8", "Chromium";v="141"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'source': 'web',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36',
}
borzo_headers = {
    'accept': 'application/json',
    'accept-language': 'en-US,en;q=0.9',
    'content-type': 'application/json',
    'origin': 'https://borzodelivery.com',
    'priority': 'u=1, i',
    'referer': 'https://borzodelivery.com/in/order',
    'sec-ch-ua': '"Google Chrome";v="141", "Not?A_Brand";v="8", "Chromium";v="141"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36',
    'x-csrf-token': '5c63d701e5f37846e435496673d17b58:eeb006dec35011ef',
    'Cookie': 'first_visit_referrer=www.google.com%2F; first_visit_datetime=2025-10-15T10%3A16%3A21%2B03%3A00; dv-device=c9e0b7a91646cbf96f64e78a15770237afe27efc98b106814f2925b3334977f3; tildauid=1760512582499.588309; _gcl_au=1.1.321457268.1760512583; is_activated=0; _ga=GA1.1.1521286146.1760512583; _ym_uid=1760512584399692786; _ym_d=1760512584; _ymab_param=qdjCLwJiG0JpLIpPLAQvdU8jAc28o3PBaXZ_F4c0VFt4uqaN_XsSyPjoZ3-4tk7x4G1qcOY9_gVwOFfmSkzYF8HnrcE; _fbp=fb.1.1760512586536.327446962760236323; intercom-id-bq4mzzc4=3ef00e39-780d-4e10-b133-cd61d49e3b3f; intercom-device-id-bq4mzzc4=5af7f0a4-283a-4b02-9eb5-2eb675859ae7; country=in; utm_source=google; utm_medium=organic; utm_external_referrer=www.google.com%2F; timeOffset=19800; _gcl_gs=2.1.k1$i1761544825$u129937951; maestraDeviceUUID=1a20073e-c77c-4d56-975b-b92707890690; directCrm-session=%7B%22deviceGuid%22%3A%221a20073e-c77c-4d56-975b-b92707890690%22%7D; _ym_isad=2; _clck=d8crf9%5E2%5Eg0i%5E0%5E2114; session_in=eyJuYW1lc3BhY2UiOiJjbGllbnRfYXBpIiwicmVnaW9uX2lkIjoyNH0.YGSMT2sQ0nkrNpRKZsGpxwwQJK575WX207S3r13I95E.4e256ac97d; selectedRegionId=24; _gcl_aw=GCL.1761544832.CjwKCAjwjffHBhBuEiwAKMb8pOS5PeiMtdsVENIPkQE4ktswGmMHPsYwjzPB0frqAC_ILyIN_g6UsxoCW1UQAvD_BwE; intercom-session-bq4mzzc4=; e1_in=EXPERIMENT_CLIENT_ALTERNATIVE_INSURANCE_FEE.2; pages_load_counter=8; _ga_FDD3VERXPT=GS2.1.s1761544828$o2$g1$t1761546248$j58$l0$h405832619; _clsk=1jfq9p2%5E1761548575433%5E1%5E1%5El.clarity.ms%2Fcollect; country=in; first_visit_datetime=2025-10-15T10%3A16%3A21%2B03%3A00; first_visit_referrer=www.google.com%2F; session_in=eyJuYW1lc3BhY2UiOiJjbGllbnRfYXBpIiwicmVnaW9uX2lkIjoyNH0.YGSMT2sQ0nkrNpRKZsGpxwwQJK575WX207S3r13I95E.4e256ac97d'
}

final_result = []

def Lat_lng_extractor(place_id):
    json_data = {
        'placeId': place_id,
    }
    response = requests.post('https://m.rapido.bike/pwa/api/unup/location/geocode/placeId', headers=headers,json=json_data)
    lat = _.get(response.json(),"data.lat","N/A")
    lng = _.get(response.json(),"data.lng","N/A")
    address = _.get(response.json(),"data.address","N/A")
    return lat, lng, address

def coordinate_extractor(address):
    json_data = {
        'searchWord': address,
    }
    response = requests.post('https://m.rapido.bike/pwa/api/unup/autocomplete/location', headers=headers, json=json_data)
    place_id = _.get(response.json(),'data[0].placeId',"N/A")
    fetch_lat, fetch_lng, fetch_address = Lat_lng_extractor(place_id)
    return fetch_lat, fetch_lng


def new_lat_lng(address):
    from swiggy import SwiggyKeyword
    loc_data = SwiggyKeyword(input_address=address)
    palce_id = loc_data.pin_to_place()['placeId']
    lat_long = loc_data.place_id_to_lat_long(placeId=palce_id)
    return lat_long["lat"], lat_long["long"]

def porter_scrape(pickup_add, pickup_city, dropoff_add, dropoff_city):
    pickup_coordinates = coordinate_extractor(pickup_add)
    pickup_latitude, pickup_longitude = pickup_coordinates

    # TODO:: dropoff_lat_lng
    dropoff_coordinates = coordinate_extractor(dropoff_add)
    dropoff_latitude, dropoff_longitude = dropoff_coordinates

    url = "https://customerapp-gateway.porter.in/customers/fetch_vehicles"

    params = {
        "geo_region_id": "6",
        "lat": str(pickup_latitude),
        "long": str(pickup_longitude)
    }

    headers = {
        "Accept": "*/*",
        "Accept-Charset": "UTF-8",
        "Accept-Encoding": "gzip",
        "app-session-id": "0a0b3aaf-bb11-423f-8888-9480b038f4bb",
        "auth-token": "ThF2kE7e1PGCas1H",
        "booking-session-id": "6b8d1ab7-b70d-4ac0-9ee1-f03622f53a94",
        "brand": "porter",
        "client-request-uuid": "2d671259-b061-4e3e-8e67-1705974e9852",
        "Connection": "Keep-Alive",
        "country": "in",
        "custom-app-version-code": "601",
        "geo-region-id": "6",
        "Host": "customerapp-gateway.porter.in",
        "host_type": "CAG",
        "installation-id": "75d6802b-3ab9-4815-9972-fac65d57b3cd",
        "login-id": "fc932f9e-c084-4759-b667-a343807ce471",
        "mobile": "9726149068",
        "preferred-languages": '{"app_language":"en"}',
        "source": "android",
        "User-Agent": "com.theporter.android.customerapp/6.45.1 Dalvik/2.1.0 (Linux; U; Android 12; SM-S9210 Build/PD1A.180720.030)",
        "version-name": "6.45.1"
    }

    vehicle_ids = []
    veh_det_response = requests.get(url, headers=headers, params=params)
    my_veh_det_json = veh_det_response.json()

    main_ids_list = _.get(my_veh_det_json, "vehicles.on_demand", "N/A")

    for ids in main_ids_list:
        vehicle_ids.append(_.get(ids, 'id', "N/A"))

    # TODO:: vehicle price details....
    url = "https://porter.in/customers/on_demand/quotations"

    headers = {
        "Accept": "*/*",
        "Accept-Charset": "UTF-8",
        "Accept-Encoding": "gzip",
        "app-session-id": "0a0b3aaf-bb11-423f-8888-9480b038f4bb",
        "auth-token": "ThF2kE7e1PGCas1H",
        "booking-session-id": "6b8d1ab7-b70d-4ac0-9ee1-f03622f53a94",
        "brand": "porter",
        "client-request-uuid": "2afd8d75-56b5-4813-82a1-ce168d5cea4c",
        "Connection": "Keep-Alive",
        "Content-Type": "application/json",
        "country": "in",
        "custom-app-version-code": "601",
        "geo-region-id": "6",
        "Host": "porter.in",
        "host_type": "OMS",
        "installation-id": "75d6802b-3ab9-4815-9972-fac65d57b3cd",
        "login-id": "fc932f9e-c084-4759-b667-a343807ce471",
        "mobile": "9726149068",
        "preferred-languages": '{"app_language":"en"}',
        "source": "android",
        "User-Agent": "com.theporter.android.customerapp/6.45.1 Dalvik/2.1.0 (Linux; U; Android 12; SM-S9210 Build/PD1A.180720.030)",
        "version-name": "6.45.1"
    }

    payload = {
        "vehicle_ids": vehicle_ids,
        "order": {
            "customer_mobile": "9726149068",
            "geo_region_id": 6,
            "from_address_lat": pickup_latitude,
            "from_address_long": pickup_longitude,
            "to_address_lat": dropoff_latitude,
            "to_address_long": dropoff_longitude,
            "waypoints_attributes": [],
            "value_added_services": [],
            "payment_mode": "cash",
            "business_order_info": None,
            "use_porter_credits": False
        },
        "selected_vehicle_id": None,
        "service_type": "TRUCKS"
    }

    proxy = {
        "http": 'http://f42a5b59aec3467e97a8794c611c436b91589634343:super=false&geoCode=in@proxy.scrape.do:8080',
        "https": 'http://f42a5b59aec3467e97a8794c611c436b91589634343:super=false&geoCode=in@proxy.scrape.do:8080',
    }

    price_response = requests.post(url, headers=headers, data=json.dumps(payload), impersonate="tor145", proxies=proxy,
                                   verify=False)
    my_price_response = price_response.json()

    vehicle_det_ids = _.get(my_veh_det_json, "vehicles.on_demand")
    for vehicle_det_id in vehicle_det_ids:
        veh_det_id = _.get(vehicle_det_id, "id", "N/A")
        veh_det_display_name = _.get(vehicle_det_id, "display_name", "N/A")
        veh_det_capacity = _.get(vehicle_det_id, "capacity", "N/A")

        vehicle_price_ids = _.get(my_price_response, "vehicle_wise_quotations")
        for vehicle_price_id in vehicle_price_ids:
            if vehicle_price_id.get("vehicle_id") == veh_det_id:
                delivery_charge = _.get(vehicle_price_id, "bill_details.fare_breakup[0][0].value", "N/A")
                total_price = _.get(vehicle_price_id, "bill_details.amount_payable", "N/A")
                total_fare = _.get(vehicle_price_id, "fare_info.fare", "N/A")
                if total_fare != "N/A":
                    item = {
                        'platfrom': "Porter",
                        'pickup address': pickup_add,
                        'pickup city': pickup_city,
                        'dropoff address': dropoff_add,
                        'dropoff city': dropoff_city,
                        'STATE': 'gujarat',
                        'vehicle type': veh_det_display_name,
                        'capacity display': veh_det_capacity,
                        'distance': 0,
                        'delivery charge': delivery_charge,
                        'base price': total_fare,
                        'total price': total_price, }
                    final_result.append(item)


def Borzo_scrape(pickup_add, pickup_city, dropoff_add, dropoff_city):
    headers = {
        'accept': 'application/json',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/json',
        'origin': 'https://borzodelivery.com',
        'priority': 'u=1, i',
        'referer': 'https://borzodelivery.com/',
        'sec-ch-ua': '"Google Chrome";v="141", "Not?A_Brand";v="8", "Chromium";v="141"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36',
    }

    # TODO:: From request for pickup placeid

    From_params = {
        'address': pickup_add,
        'region_id': '24',
        'order_form_filling_id': 'ebddf998-3be0-4fce-b6ed-3fbe83463d17',
    }

    From_response = requests.get('https://geo-in.borzodelivery.com/api/external/1.0/geo-suggestions',
                                 params=From_params, headers=headers)
    From_json_response = From_response.json()
    From_place_id = From_json_response.get("suggestions")[0].get("place_id")

    # TODO:: lat & lng request for pickiup

    From_ln_params = {
        'place_id': From_place_id,
        'order_form_filling_id': 'ebddf998-3be0-4fce-b6ed-3fbe83463d17',
    }
    From_ln_response = requests.get('https://geo-in.borzodelivery.com/api/external/1.0/place', params=From_ln_params,
                                    headers=headers)
    my_json = From_ln_response.json()
    From_ln_address = my_json.get("place").get("address")
    From_ln_latitude = my_json.get("place").get("latitude")
    From_ln_longitude = my_json.get("place").get("longitude")

    # TODO:: To request for dropoff placeid

    To_params = {
        'address': dropoff_add,
        'region_id': '24',
        'order_form_filling_id': 'ebddf998-3be0-4fce-b6ed-3fbe83463d17',
    }
    To_response = requests.get('https://geo-in.borzodelivery.com/api/external/1.0/geo-suggestions', params=To_params,
                               headers=headers)
    To_json_response = To_response.json()
    To_place_id = To_json_response.get("suggestions")[0].get("place_id")

    # TODO:: lat & lng request for Drop

    To_ln_params = {
        'place_id': To_place_id,
        'order_form_filling_id': 'ebddf998-3be0-4fce-b6ed-3fbe83463d17',
    }
    To_ln_response = requests.get('https://geo-in.borzodelivery.com/api/external/1.0/place', params=To_ln_params,
                                  headers=headers)
    my_json = To_ln_response.json()
    To_ln_address = my_json.get("place").get("address")
    To_ln_latitude = my_json.get("place").get("latitude")
    To_ln_longitude = my_json.get("place").get("longitude")

    weights_ls = [0, 1, 5, 10, 15, 20]

    for weights in weights_ls:
        url = "https://borzodelivery.com/in/order-r/calculate-order"
        payload = json.dumps({
            "region_id": 24,
            "form_type": "asap",
            "vehicle_type_id": 8,
            "total_weight": str(weights),
            "matter": "",
            "cargo_dimensions": None,
            "backpayment_details": "",
            "payment_method": "cash",
            "bank_card_id": None,
            "promo_code": "",
            "sms_notification": False,
            "recipients_sms_notification": True,
            "is_return_to_first_point_required": False,
            "points": [
                {
                    "point_id": None,
                    "uid": "1",
                    "address": From_ln_address,
                    "latitude": From_ln_latitude,
                    "longitude": From_ln_longitude,
                    "phone": "",
                    "contact_person": "",
                    "date": None,
                    "note": "",
                    "entrance_number": "",
                    "floor_number": "",
                    "apartment_number": "",
                    "invisible_mile_navigation_instructions": "",
                    "is_order_payment_here": True,
                    "is_contactless_delivery": False,
                    "money_operation_type": "none"
                },
                {
                    "point_id": None,
                    "uid": "2",
                    "address": To_ln_address,
                    "latitude": To_ln_latitude,
                    "longitude": To_ln_longitude,
                    "phone": "",
                    "contact_person": "",
                    "date": None,
                    "note": "",
                    "entrance_number": "",
                    "floor_number": "",
                    "apartment_number": "",
                    "invisible_mile_navigation_instructions": "",
                    "is_order_payment_here": False,
                    "is_contactless_delivery": False,
                    "money_operation_type": "none"
                }
            ],
            "insurance": "",
            "client_phone": "",
            "require_loading": False,
            "order_form_filling_id": "ebddf998-3be0-4fce-b6ed-3fbe83463d17"
        })

        final_response = requests.request("POST", url, headers=borzo_headers, data=payload)
        final_json = final_response.json()
        total_weight = final_json.get('order').get("total_weight_label")
        payment = final_json.get('order').get("payment")
        distance_meters = final_json.get('order').get("distance_meters")
        payment_details = final_json.get('order').get("payment_details")
        delivery_charges = ''
        for payment_detail in payment_details:
            if payment_detail.get("slug") == "delivery_fee":
                delivery_charges = payment_detail.get("amount")
                break

        item = {}
        item['platfrom'] = "Borzo"
        item['pickup address'] = pickup_add
        item['pickup city'] = pickup_city
        item['dropoff address'] = dropoff_add
        item['dropoff city'] = dropoff_city
        item['STATE'] = 'gujarat'
        item['vehicle type'] = "Bike"
        item['capacity display'] = total_weight
        item['distance'] = distance_meters
        item['delivery charge'] = delivery_charges if delivery_charges else 0
        item['base price'] = payment
        item['total price'] = payment
        final_result.append(item)


def scrape_location_data(pickup_add, pickup_city, dropoff_add, dropoff_city):
    global final_result
    final_result.clear()

    with ThreadPoolExecutor(max_workers=2) as executor:
        # Submit both functions
        future1 = executor.submit(porter_scrape, pickup_add, pickup_city, dropoff_add, dropoff_city)
        future2 = executor.submit(Borzo_scrape, pickup_add, pickup_city, dropoff_add, dropoff_city)

        # Wait for results (optional)
        result1 = future1.result()
        result2 = future2.result()
    return final_result
