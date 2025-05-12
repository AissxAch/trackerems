import requests
from bs4 import BeautifulSoup
from proxies import fetch_proxies, check_proxies, test_proxy  # Add these imports
import random

status_translations = {
    "En cours de Distribution": "جاري التوصيل",
    "Entrée en transit": "في مرحلة الاستعداد لنقل",
    "Expédier envoi hors du centre de tri (Ent)": "إرسال الشحنة خارج مركز الفرز",
    "Recevoir envoi au centre de tri (Ent)": "استلام الشحنة في مركز الفرز",
    "Dédouanement effectué": "تم التخليص الجمركي",
    "Présentation au service des Douanes": "عرضت على الجمارك",
    # Add more translations as needed
}
location_translations = {
    # EMS Agencies (Agence EMS)
    "Agence EMS ADRAR": "وكالة EMS أدرار",
    "Agence EMS CHLEF": "وكالة EMS الشلف",
    "Agence EMS LAGHOUAT": "وكالة EMS الأغواط",
    "Agence EMS OUM EL BOUAGHI": "وكالة EMS أم البواقي",
    "Agence EMS BATNA": "وكالة EMS باتنة",
    "Agence EMS BEJAIA": "وكالة EMS بجاية",
    "Agence EMS BISKRA": "وكالة EMS بسكرة",
    "Agence EMS BECHAR": "وكالة EMS بشار",
    "Agence EMS BLIDA": "وكالة EMS البليدة",
    "Agence EMS BOUIRA": "وكالة EMS البويرة",
    "Agence EMS TAMANRASSET": "وكالة EMS تمنراست",
    "Agence EMS TEBESSA": "وكالة EMS تبسة",
    "Agence EMS TLEMCEN": "وكالة EMS تلمسان",
    "Agence EMS TIARET": "وكالة EMS تيارت",
    "Agence EMS TIZI OUZOU": "وكالة EMS تيزي وزو",
    "Agence EMS ALGER": "وكالة EMS الجزائر",
    "Agence EMS DJELFA": "وكالة EMS الجلفة",
    "Agence EMS JIJEL": "وكالة EMS جيجل",
    "Agence EMS SETIF": "وكالة EMS سطيف",
    "Agence EMS SAIDA": "وكالة EMS سعيدة",
    "Agence EMS SKIKDA": "وكالة EMS سكيكدة",
    "Agence EMS SIDI BEL ABBES": "وكالة EMS سيدي بلعباس",
    "Agence EMS ANNABA": "وكالة EMS عنابة",
    "Agence EMS GUELMA": "وكالة EMS قالمة",
    "Agence EMS CONSTANTINE": "وكالة EMS قسنطينة",
    "Agence EMS MEDEA": "وكالة EMS المدية",
    "Agence EMS MOSTAGANEM": "وكالة EMS مستغانم",
    "Agence EMS MSILA": "وكالة EMS المسيلة",
    "Agence EMS MASCARA": "وكالة EMS معسكر",
    "Agence EMS OUARGLA": "وكالة EMS ورقلة",
    "Agence EMS ORAN": "وكالة EMS وهران",
    "Agence EMS EL BAYADH": "وكالة EMS البيض",
    "Agence EMS ILLIZI": "وكالة EMS إيليزي",
    "Agence EMS BORDJ BOU ARRERIDJ": "وكالة EMS برج بوعريريج",
    "Agence EMS BOUMERDES": "وكالة EMS بومرداس",
    "Agence EMS EL TARF": "وكالة EMS الطارف",
    "Agence EMS TINDOUF": "وكالة EMS تندوف",
    "Agence EMS TISSEMSILT": "وكالة EMS تيسمسيلت",
    "Agence EMS EL OUED": "وكالة EMS الوادي",
    "Agence EMS KHENCHELA": "وكالة EMS خنشلة",
    "Agence EMS SOUK AHRAS": "وكالة EMS سوق أهراس",
    "Agence EMS TIPAZA": "وكالة EMS تيبازة",
    "Agence EMS MILA": "وكالة EMS ميلة",
    "Agence EMS AIN DEFLA": "وكالة EMS عين الدفلى",
    "Agence EMS NAAMA": "وكالة EMS النعامة",
    "Agence EMS AIN TEMOUCHENT": "وكالة EMS عين تيموشنت",
    "Agence EMS GHARDAIA": "وكالة EMS غرداية",
    "Agence EMS RELIZANE": "وكالة EMS غليزان",

    # EMS Centers (Centre EMS)
    "Centre EMS ADRAR": "مركز EMS أدرار",
    "Centre EMS CHLEF": "مركز EMS الشلف",
    "Centre EMS ALGER": "مركز EMS الجزائر",
    "Centre EMS ORAN": "مركز EMS وهران",
    "Centre EMS CONSTANTINE": "مركز EMS قسنطينة",
    "Centre EMS ANNABA": "مركز EMS عنابة",
    "Centre EMS SKIKDA": "مركز EMS سكيكدة",
    "Centre EMS SETIF": "مركز EMS سطيف",
    "Centre EMS BATNA": "مركز EMS باتنة",
    "Centre EMS BLIDA": "مركز EMS البليدة",
    "Centre EMS TIZI OUZOU": "مركز EMS تيزي وزو",
    "Centre EMS BEJAIA": "مركز EMS بجاية",
    
    # National Centers
    "Centre d'Acheminement National": "المركز الوطني للتوجيه",
    "EMS Algiers International Center": "المركز الدولي EMS الجزائر",
}




def track_ems_package(tracking_number,p):
    base_url = "https://www.ems.dz/track/index.php"
    params = {"icd": tracking_number}
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Referer": "https://www.ems.dz/",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
    }
    
    # Get a working proxy
    proxy = p
    proxies_config = {
        'http': f'http://{proxy}',
        'https': f'http://{proxy}'
    } if proxy else None
    
    try:
        # Make the GET request with headers and proxy
        response = requests.get(
            base_url,
            params=params,
            headers=headers,
            proxies=proxies_config,
            timeout=10
        )
        
        # Check if the request was successful
        if response.status_code != 200:
            return {
                "error": f"Server returned {response.status_code} status code",
                "status": "Server error",
                "response": "The EMS server might be experiencing issues"
            }
        
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Check if tracking number was found
        main_heading = soup.find('div', class_='main-heading')
        if not main_heading or tracking_number not in main_heading.get_text():
            return {
                "error": "No tracking information found",
                "status": "Not found",
                "response": "The tracking number might be incorrect or not yet in the system"
            }
        
        # Find all timeline blocks
        timeline_blocks = soup.find_all('div', class_='cd-timeline__block')
        
        if not timeline_blocks:
            return {
                "error": "No tracking events found",
                "status": "No events",
                "response": "The package might not have any tracking events yet"
            }
        
        tracking_events = []
        for block in timeline_blocks:
            # Extract date
            date_span = block.find('span', class_='cd-timeline__date')
            date = date_span.get_text(strip=True) if date_span else "Unknown date"
            
            # Extract status
            status_h2 = block.find('h2')
            status = status_h2.get_text(strip=True) if status_h2 else "Unknown status"
            
            # Extract location
            location_p = block.find('p')
            location = location_p.get_text(strip=True) if location_p else "Unknown location"
            
            tracking_events.append({
                "date": date,
                "status": status_translations.get(status, status),  # Translate status
                "location": location_translations.get(location, location)  # Translate location
            })
        
        tracking_events.reverse()
        return {
            "tracking_number": tracking_number,
            "events": tracking_events,
            "status": "Success",
            "count": len(tracking_events)
        }
        
    except requests.exceptions.RequestException as e:
        return {
            "error": 'هناك خطاء في السيرفر يرجى ابلاغ المطور',
            "status": "Request failed",
            "response": "Network or connection error occurred"
        }
    except Exception as e:
        return {
            "error": 'هناك خطاء يرجى ابلاغ المطور',
            "status": "Processing failed",
            "response": "An error occurred while processing the response"
        }
