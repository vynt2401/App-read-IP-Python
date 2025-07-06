import socket# libary to connect with TCP/IP, UDP network
import requests # libary to send HTTP requests
import dns.resolver # libary to reslove DNS 



def get_local_ip(): # lấy địa chỉ ip cục bộ của máy tính đang connect to
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        #tạo socket udp và kế t nối đến địa chỉ gg: 8.8.8.8 ở port 80

        local_ip = s.getstockname()[0] # trả về địa chỉ ip cục bộ của máy tính kết nối và lưu ở local ip
        s.close()
        return local_ip
    except Exception as e:
        return f"khong the lay duoc dia chi IP cuc bo: {e}"
    

def get_public_ip(): # lấy địa chỉ ip public của máy, ip mà internet đang nhìn thấy
    try:
        response = requests.get("https://api.ipify.org?format=json") # gửi http requests đến địa chỉ này, sau đó server sẽ trả về một địa chỉ ip công cộng của máy dưới dạng JSON
        # -> cho thấy được ip mà web server nhìn thấy được từ máy của mình
        response.raise_for_status() #kiểm tra xem có lỗi gì trong quá trình thực thi kh, nếu có thì raise lỗi
        return response.json()["ip"] # trả về local ip từ response json
    except requests.exceptions.RequestException as e:
        return f"kh thhe lay duoc ip cong cong: {e}"
    
def lookup_dns(ip_address):
    """Tra cứu DNS cho một địa chỉ IP (sử dụng thư viện dnspython)."""
    try:
        # Tra cứu tên miền ngược (PTR record)
        # Chuyển đổi IP sang định dạng đảo ngược cho tra cứu PTR
        reversed_ip = '.'.join(ip_address.split('.')[::-1]) + '.in-addr.arpa'
        answers = dns.resolver.resolve(reversed_ip, 'PTR')
        dns_names = [str(rdata) for rdata in answers]
        return dns_names
    except dns.resolver.NXDOMAIN:
        return ["Không tìm thấy tên miền (NXDOMAIN)"]
    except dns.resolver.NoAnswer:
        return ["Không có bản ghi PTR (NoAnswer)"]
    except dns.resolver.Timeout:
        return ["Hết thời gian chờ tra cứu DNS"]
    except Exception as e:
        return [f"Lỗi khi tra cứu DNS: {e}"]
    
def get_ip_geolocation(ip_address):
    """Lấy thông tin địa lý (vùng, quốc gia) của một địa chỉ IP."""                         
    try:
        response = requests.get(f"https://ipapi.co/{ip_address}/json/")
        response.raise_for_status()
        data = response.json()
        if data.get("error"):
            return f"Lỗi từ API địa lý: {data['reason']}"

        city = data.get("city", "Không rõ")
        region = data.get("region", "Không rõ")
        country_name = data.get("country_name", "Không rõ")
        latitude = data.get("latitude", "Không rõ")
        longitude = data.get("longitude", "Không rõ")
        org = data.get("org", "Không rõ")

        return {
            "Thành phố": city,
            "Vùng": region,
            "Quốc gia": country_name,
            "Vĩ độ": latitude,
            "Kinh độ": longitude,
            "Tổ chức/ISP": org
        }
    except requests.exceptions.RequestException as e:
        return f"Không thể lấy thông tin địa lý: {e}"

def main():
    print("Đang lấy thông tin IP của thiết bị...")

    # Lấy IP cục bộ
    local_ip = get_local_ip()
    print(f"\nĐịa chỉ IP cục bộ: {local_ip}")

    # Lấy IP công cộng
    public_ip = get_public_ip()
    print(f"\nĐịa chỉ IP công cộng: {public_ip}")

    if "Không thể" not in public_ip:
        # Tra cứu DNS từ IP công cộng
        print(f"\nĐang tra cứu DNS cho IP công cộng ({public_ip})...")
        dns_names = lookup_dns(public_ip)
        print("Tên miền (DNS) liên quan:")
        for name in dns_names:
            print(f"- {name}")

        # Lấy thông tin địa lý từ IP công cộng
        print(f"\nĐang lấy thông tin địa lý cho IP công cộng ({public_ip})...")
        geolocation_info = get_ip_geolocation(public_ip)
        print("Thông tin địa lý:")
        if isinstance(geolocation_info, dict):
            for key, value in geolocation_info.items():
                print(f"- {key}: {value}")
        else:
            print(geolocation_info)
    else:
        print("\nKhông thể thực hiện tra cứu DNS và địa lý vì không lấy được IP công cộng.")

if __name__ == "__main__":
    main()