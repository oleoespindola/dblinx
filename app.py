from src.downloads import EmployeeDownload, SalesDownload, MobilePlansDownload, InsuranceDownload
from src.upsert import EmployeesUpsert, SalesUpsert, MobilePlansUpsert, InsuranceUpsert

def run():
    timeout = 6
    download_time = 20

    EmployeeDownload(timeout, download_time)
    # EmployeesUpsert()
    
    SalesDownload(timeout, download_time)
    # SalesUpsert()

    MobilePlansDownload(timeout, download_time)
    # MobilePlansUpsert()

    InsuranceDownload(timeout, download_time)
    # InsuranceUpsert()

if __name__ == "__main__":
    run()