import xmlrpc.client

class HospitalClient:
    def __init__(self):
        self.proxy = xmlrpc.client.ServerProxy("http://localhost:8000", allow_none=True)
        self.antrian = 0
        self.klinik = ""

    def register_pasien(self, clinic_name, medical_record_number, name, birth_date):
        return self.proxy.register_pasien(clinic_name, medical_record_number, name, birth_date)

    def waktu_estimasi(self, clinic_name, queue_number):
        return self.proxy.waktu_estimasi(clinic_name, queue_number)
    def daftar_klinik(self):
        return self.proxy.daftar_klinik()

def main():
    client = HospitalClient()

    while True:
        print("1. Registrasi Pasien")
        print("2. Daftar Klinik")
        print("3. Perkiraan Waktu Tunggu")
        print("4. Keluar")

        inp = input("Pilih menu : ")

        if inp == "1":
            clinic_name = input("Masukkan nama klinik: ")
            medical_record_number = input("Masukkan nomor rekam medis: ")
            name = input("Masukkan nama: ")
            birth_date = input("Masukkan tanggal lahir (format: DD-MM-YYYY): ")

            result = client.register_pasien(clinic_name, medical_record_number, name, birth_date)
            client.antrian = result[1]
            client.klinik = result[2]
            print(result[0])

        elif inp == "2":
            list_klinik = client.daftar_klinik()
            print(list_klinik)

        elif inp == "3":
            time_estimate = client.waktu_estimasi(client.klinik, client.antrian)
            print(time_estimate)

        elif inp == "4":
            break

        else:
            print("Pilihan tidak sesuai. inputkan ulang pilihan menu")

if __name__ == '__main__':
    main()
