import psutil
import time
import cpuinfo


def cpu_uses():
    return psutil.cpu_percent(interval=1)


def ram_uses():
    time.sleep(1)

    return psutil.virtual_memory().percent


def ram_detail():
    return str(round(psutil.virtual_memory().total / 1024.0**3)) + " GB"


def cpu_detail():
    return str(cpuinfo.get_cpu_info()["brand_raw"])


# print(total_ram())
if __name__ == "__main__":
    # for i in range(10):
    #     print(cpu_detail())
    print(cpu_detail())