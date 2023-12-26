from xmlrpc.server import SimpleXMLRPCServer
import datetime

class HospitalServer:
    def __init__(self):
        self.waktu = {
            'Klinik Mata': 0,
            'Klinik THT': 0,
            'Klinik Kulit': 0,
            
        }

        self.klinik = {
            'Klinik Mata': [],
            'Klinik THT': [],
            'Klinik Kulit':[]
        }


    def save_data(self):
        with open("hospital_data.txt", mode='a') as file:
            for clinic_name, patients in self.klinik.items():
                for patient in patients:
                    file.write('\t'.join([str(patient[field]) for field in ['clinic_name', 'medical_record_number', 'name', 'birth_date', 'queue_number', 'register_time']]) + '\n')

    def register_pasien(self, clinic_name, medical_record_number, name, birth_date):
        if clinic_name not in self.klinik:
            return "Klinik tidak valid"

        queue_number = len(self.klinik[clinic_name]) + 1
        patient_data = {
            'clinic_name': clinic_name,
            'medical_record_number': medical_record_number,
            'name': name,
            'birth_date': birth_date,
            'queue_number': queue_number,
            'register_time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        self.klinik[clinic_name].append(patient_data)

        if queue_number == 1:
            self.waktu[clinic_name] = datetime.datetime.now()

        self.save_data()

        return f"Registrasi berhasil. Nomor antrean Anda di {clinic_name}: {queue_number}", queue_number, clinic_name



    def waktu_estimasi(self, clinic_name, queue_number):
        if clinic_name not in self.klinik:
            return "Silahkan registrasi terlebih dahulu"

        for patient in self.klinik[clinic_name]:
            if patient['queue_number'] == queue_number:
                register_time = patient['register_time']

                wait_time = (datetime.datetime.now() - self.waktu[clinic_name]).seconds
                i = 1
                while wait_time > 60:
                    i = i + 1
                    wait_time = wait_time - 60
                    
                
                if i > queue_number :
                    return "Antrean sudah terlewat"
                elif i == queue_number:
                    return "Sedang dilayani"
                elif queue_number-i > 1:
                    waktu_tunggu = (60 - wait_time)+(60*(queue_number-i-1)) 
                    return f"Perkiraan waktu antrean Anda di {clinic_name}: {waktu_tunggu} menit {i}"
                else :
                    waktu_tunggu = 60 - wait_time
                    return f"Perkiraan waktu antrean Anda di {clinic_name}: {waktu_tunggu} menit, antrian saat ini adalah{i}"

        return "Nomor antrean tidak ditemukan"
    
    def daftar_klinik(self):
        klinik = []
        for key in self.klinik:
            klinik.append(key)
        return klinik

def main():
    server = SimpleXMLRPCServer(('localhost', 8000), allow_none=True)
    server.register_instance(HospitalServer())
    print("Server ready on port 8000")
    server.serve_forever()

if __name__ == "__main__":
    main()
