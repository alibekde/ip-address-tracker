from flask import Flask, render_template, request, jsonify
import requests
import os
from datetime import datetime

app = Flask(__name__)

class IPAddressTracker:
    """IP Address Tracking va Geolokatsiya"""
    
    # Free IP APIs
    IPAPI_URL = "https://ipapi.co/{ip}/json/"
    GEOIP_URL = "https://api.geoip.tool/api/v1/ip"
    IPINFO_URL = "https://ipinfo.io/{ip}/json"
    GEOCODING_URL = "https://nominatim.openstreetmap.org/search"
    
    def __init__(self):
        self.lookup_history = []
    
    def get_client_ip(self):
        """Foydalanuvchining haqiqiy IP address-ini olish"""
        if request.environ.get('HTTP_CF_CONNECTING_IP'):
            return request.environ.get('HTTP_CF_CONNECTING_IP')
        elif request.environ.get('HTTP_X_FORWARDED_FOR'):
            return request.environ.get('HTTP_X_FORWARDED_FOR').split(',')[0]
        return request.remote_addr
    
    def get_ip_info(self, ip_address):
        """
        IP address haqida ma'lumotlarni olish
        
        Args:
            ip_address (str): IP address
        
        Returns:
            dict: IP ma'lumotlari
        """
        try:
            # ipapi.co-dan olish (eng yaxshi)
            response = requests.get(
                self.IPAPI_URL.format(ip=ip_address),
                timeout=5
            )
            
            if response.status_code == 200:
                data = response.json()
                
                # Ma'lumotlarni format qilish
                info = {
                    'ip': ip_address,
                    'country': data.get('country_name', 'N/A'),
                    'country_code': data.get('country_code', 'N/A'),
                    'region': data.get('region', 'N/A'),
                    'city': data.get('city', 'N/A'),
                    'postal_code': data.get('postal', 'N/A'),
                    'timezone': data.get('timezone', 'N/A'),
                    'latitude': data.get('latitude'),
                    'longitude': data.get('longitude'),
                    'isp': data.get('org', 'N/A'),
                    'asn': data.get('asn', 'N/A'),
                    'network': data.get('network', 'N/A'),
                    'currency': data.get('currency', 'N/A'),
                    'calling_code': data.get('country_phone_prefix', 'N/A'),
                    'languages': data.get('languages', 'N/A'),
                    'is_vpn': data.get('is_vpn', False),
                    'is_proxy': data.get('is_proxy', False),
                    'is_datacenter': data.get('is_datacenter', False),
                    'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                
                # Tarixga qo'shish
                self.lookup_history.append(info)
                
                return info
            else:
                return None
        
        except Exception as e:
            print(f"Error: {e}")
            return None
    
    def get_ips_by_location(self, location):
        """
        Shahar yoki davlat nomi bo'ylab IP qidirish
        
        Args:
            location (str): Shahar yoki davlat nomi (masalan: "London", "Tashkent", "USA")
        
        Returns:
            list: Topilgan IP-lar va ma'lumotlar
        """
        try:
            # Geocoding-dan lokatsiya koordinatalarini olish
            params = {
                'q': location,
                'format': 'json',
                'limit': 1
            }
            
            response = requests.get(
                self.GEOCODING_URL,
                params=params,
                timeout=5,
                headers={'User-Agent': 'ip-tracker'}
            )
            
            if response.status_code == 200:
                data = response.json()
                
                if not data:
                    return None
                
                # Birinchi natijani olish
                result = data[0]
                lat = float(result.get('lat'))
                lon = float(result.get('lon'))
                display_name = result.get('display_name', location)
                
                # Lokatsiya ma'lumotlarini to'pla
                location_info = {
                    'query': location,
                    'display_name': display_name,
                    'latitude': lat,
                    'longitude': lon,
                    'location_type': self._detect_location_type(location),
                    'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                
                # Tarixga qo'shish
                self.lookup_history.append(location_info)
                
                return location_info
            
            return None
        
        except Exception as e:
            print(f"Error: {e}")
            return None
    
    def _detect_location_type(self, location):
        """Lokatsiya turini aniqlash (Shahar, Davlat, Region)"""
        # Davlatlar ro'yxati
        countries = {
            'USA': 'United States', 'US': 'United States',
            'UK': 'United Kingdom', 'China': 'China',
            'Japan': 'Japan', 'Russia': 'Russia',
            'India': 'India', 'Germany': 'Germany',
            'France': 'France', 'Italy': 'Italy',
            'Spain': 'Spain', 'Canada': 'Canada',
            'Australia': 'Australia', 'Uzbekistan': 'Uzbekistan',
            'O\\'zbekiston': 'Uzbekistan', 'Kazakhstan': 'Kazakhstan',
            'Tajikistan': 'Tajikistan', 'Kyrgyzstan': 'Kyrgyzstan'
        }
        
        # Shaxarlar ro'yxati
        cities = {
            'London': 'City', 'New York': 'City', 'Tokyo': 'City',
            'Paris': 'City', 'Berlin': 'City', 'Moscow': 'City',
            'Delhi': 'City', 'Shanghai': 'City', 'Mumbai': 'City',
            'Tashkent': 'City', 'Samarkand': 'City', 'Bukhara': 'City',
            'Almaty': 'City', 'Bishkek': 'City', 'Dushanbe': 'City'
        }
        
        for country in countries:
            if location.lower() == country.lower():
                return 'Country'
        
        for city in cities:
            if location.lower() == city.lower():
                return 'City'
        
        return 'Location'
    
    def is_valid_ip(self, ip_address):
        """
        IP addressning to'g'ri ekanligini tekshirish
        
        Args:
            ip_address (str): IP address
        
        Returns:
            bool: True agar to'g'ri bo'lsa
        """
        try:
            parts = ip_address.split('.')
            if len(parts) != 4:
                return False
            
            for part in parts:
                num = int(part)
                if num < 0 or num > 255:
                    return False
            
            return True
        except:
            return False
    
    def is_private_ip(self, ip_address):
        """
        Private IP ekanligini tekshirish
        
        Args:
            ip_address (str): IP address
        
        Returns:
            bool: True agar private bo'lsa
        """
        private_ranges = [
            ('10.0.0.0', '10.255.255.255'),
            ('172.16.0.0', '172.31.255.255'),
            ('192.168.0.0', '192.168.255.255'),
            ('127.0.0.0', '127.255.255.255'),
        ]
        
        try:
            ip_parts = [int(x) for x in ip_address.split('.')]
            for start_str, end_str in private_ranges:
                start_parts = [int(x) for x in start_str.split('.')]
                end_parts = [int(x) for x in end_str.split('.')]
                
                if self._compare_ip(start_parts, ip_parts) <= 0 and self._compare_ip(ip_parts, end_parts) <= 0:
                    return True
            return False
        except:
            return False
    
    def _compare_ip(self, ip1, ip2):
        """IP addresslarni solishtirish"""
        for a, b in zip(ip1, ip2):
            if a < b:
                return -1
            elif a > b:
                return 1
        return 0
    
    def get_history(self):
        """Lookup tarixini olish"""
        return self.lookup_history[-10:]  # Oxirgi 10 ta

# Tracker-ni yaratish
tracker = IPAddressTracker()

@app.route('/')
def index():
    """Asosiy sahifa"""
    client_ip = tracker.get_client_ip()
    return render_template('index.html', client_ip=client_ip)

@app.route('/api/lookup', methods=['POST'])
def api_lookup():
    """API: IP addressni qidirish"""
    try:
        data = request.json
        ip_address = data.get('ip', '').strip()
        
        if not ip_address:
            return jsonify({
                'success': False,
                'error': 'IP address kiritilmadi'
            }), 400
        
        # IP validatsiyasi
        if not tracker.is_valid_ip(ip_address):
            return jsonify({
                'success': False,
                'error': 'Noto\'g\'ri IP address formati'
            }), 400
        
        # Private IP tekshirish
        if tracker.is_private_ip(ip_address):
            return jsonify({
                'success': False,
                'error': 'Private IP address (localhost yoki internal network)',
                'is_private': True
            }), 400
        
        # IP ma'lumotlarini olish
        ip_info = tracker.get_ip_info(ip_address)
        
        if ip_info is None:
            return jsonify({
                'success': False,
                'error': 'IP address topilmadi yoki ma\'lumot olib bo\'lmadi'
            }), 404
        
        return jsonify({
            'success': True,
            'data': ip_info,
            'message': f'✅ {ip_address} uchun ma\'lumotlar topildi'
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/location-lookup', methods=['POST'])
def api_location_lookup():
    """API: Shahar/Davlat nomi bo'ylab qidirish"""
    try:
        data = request.json
        location = data.get('location', '').strip()
        
        if not location:
            return jsonify({
                'success': False,
                'error': 'Shahar yoki davlat nomi kiritilmadi'
            }), 400
        
        if len(location) < 2:
            return jsonify({
                'success': False,
                'error': 'Kamida 2 ta belgi kerak'
            }), 400
        
        # Lokatsiyani qidirish
        location_info = tracker.get_ips_by_location(location)
        
        if location_info is None:
            return jsonify({
                'success': False,
                'error': f'"{location}" topilmadi. Boshqa shahar yoki davlat nomi kiriting'
            }), 404
        
        return jsonify({
            'success': True,
            'data': location_info,
            'message': f'✅ "{location}" uchun lokatsiya topildi'
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/my-ip', methods=['GET'])
def api_my_ip():
    """API: O'z IP address-ni olish"""
    try:
        client_ip = tracker.get_client_ip()
        ip_info = tracker.get_ip_info(client_ip)
        
        if ip_info is None:
            return jsonify({
                'success': False,
                'error': 'Ma\'lumot olib bo\'lmadi',
                'ip': client_ip
            }), 400
        
        return jsonify({
            'success': True,
            'data': ip_info
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/batch-lookup', methods=['POST'])
def api_batch_lookup():
    """API: Ko'p IP addresslarni qidirish"""
    try:
        data = request.json
        ip_list = data.get('ips', [])
        
        if not ip_list or len(ip_list) == 0:
            return jsonify({
                'success': False,
                'error': 'IP address ro\'yxati bo\'sh'
            }), 400
        
        if len(ip_list) > 100:
            return jsonify({
                'success': False,
                'error': 'Maksimal 100 ta IP address'
            }), 400
        
        results = []
        for ip in ip_list:
            ip = ip.strip()
            if tracker.is_valid_ip(ip) and not tracker.is_private_ip(ip):
                ip_info = tracker.get_ip_info(ip)
                if ip_info:
                    results.append(ip_info)
        
        return jsonify({
            'success': True,
            'results': results,
            'count': len(results),
            'message': f'{len(results)} ta IP topildi'
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/history', methods=['GET'])
def api_history():
    """API: Lookup tarixi"""
    history = tracker.get_history()
    return jsonify({
        'success': True,
        'history': history,
        'count': len(history)
    })

@app.route('/api/validate-ip', methods=['POST'])
def api_validate_ip():
    """API: IP addressni tekshirish"""
    try:
        data = request.json
        ip_address = data.get('ip', '').strip()
        
        if not ip_address:
            return jsonify({
                'success': False,
                'error': 'IP address kiritilmadi'
            }), 400
        
        is_valid = tracker.is_valid_ip(ip_address)
        is_private = tracker.is_private_ip(ip_address) if is_valid else False
        
        return jsonify({
            'success': True,
            'ip': ip_address,
            'is_valid': is_valid,
            'is_private': is_private,
            'type': 'Private' if is_private else ('Public' if is_valid else 'Invalid')
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
