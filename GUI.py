import customtkinter as ctk
import socket
import requests
import dns.resolver

class ip():
    def __init__(self):
        self.local_ip = self.get_local_ip()
        self.public_ip = self.get_public_ip()
        self.dns_names = self.lookup_dns(self.public_ip)
        self.geolocation_info = self.get_ip_geolocation(self.public_ip)
    

    def get_local_ip(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))

            local_ip = s.getsockname()[0]
            s.close()
            return local_ip
        except Exception as e:
            return f"can't take local ip: {e}"

    def get_public_ip(self):
        try:
            response = requests.get("https://api.ipify.org?format=json")
            response.raise_for_status()
            return response.json()["ip"]
        except requests.exceptions.RequestException as e:
            return f"can't take public ip: {e}"
        
    def lookup_dns(self, ip_address):
        try:
            reversed_ip = '.'.join(ip_address.split('.')[::-1]) + '.in-addr.arpa'
            answers = dns.resolver.resolve(reversed_ip, 'PTR')
            dns_names = [str(rdata) for rdata in answers]
            return dns_names
        except dns.resolver.NXDOMAIN:
            return ["Can't find domain name (NXDOMAIN)"]
        except dns.resolver.NoAnswer:
            return ["Not have record PTR (NoAnswer)"]
        except dns.resolver.Timeout:
            return ["Over time to take DNS"]
        except Exception as e:
            return [f"ERROR with DNS: {e}"]

def get_ip_geolocation(self, ip_address):
    try:
        response = requests.get(f"https://ipapi.co/{ip_address}/json/")
        response.raise_for_status()
        data = response.json()
        if data.get("error"):
            return f"Error from geolocation API: {data['reason']}"

        city = data.get("city", "Unknown")
        region = data.get("region", "Unknown")
        country_name = data.get("country_name", "Unknown")
        latitude = data.get("latitude", "Unknown")
        longitude = data.get("longitude", "Unknown")
        org = data.get("org", "Unknown")

        return {
            "city": city,
            "region": region,
            "country_name": country_name,
            "latitude": latitude,
            "longitude": longitude,
            "org": org
        }
    except requests.exceptions.RequestException as e:
        return f"Error with geolocation API: {e}"


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("IP and dns app")
        self.geometry("1000x500")

     
        self.label = ctk.CTkLabel(self, text="Hello, CustomTkinter!")
        self.label.pack(pady=20)

        self.open_message_button = ctk.CTkButton(self, text = "Open Message Box", command = self.open_message)
        self.open_message_button.pack(pady = 20, padx = 20)

    def open_message(self):
        mess_box = message_box(self, "WARNING", "this is a message box")
        self.wait_window(mess_box)


class message_box(ctk.CTkToplevel):
    def __init__(self, parent, title, message):
        super().__init__(parent)
        self.title(title)
        self.geometry("400x400")
        self.resizable(False, False)

        self.grab_set()

        self.frame = ctk.CTkFrame(self)
        self.frame.pack(pady = 20, padx = 20, fill = 'both', expand = True)

        self.message_label = ctk.CTkLabel(self.frame, text = message, wraplength=300)
        self.message_label.pack(pady = 20, padx = 20)

        self.ok_button = ctk.CTkButton(self.frame, text = "OK", command=self.destroy)
        self.ok_button.pack(pady = 10)

        self.protocol("WM_DELETE_WINDOW",self.destroy_and_release) 

    def destroy_and_release(self):
        self.grab_release()
        self.destroy()

ip_instacne = ip()
print(f"Local IP: {ip_instacne.local_ip}")
print(f"Public IP: {ip_instacne.public_ip}")
print(f"DNS Names: {ip_instacne.dns_names}")
print(f"Geolocation Info: {ip_instacne.geolocation_info}")

app = App()
app.mainloop()