import psutil
import time
import pyecharts.options as opts
from pyecharts.charts import Line
from perf_read import PerfData


class fileHandler:

    def __init__(self, filename):
        self.filename = filename
        with open(self.filename, 'w') as f:
            pass
        self.f = open(self.filename, 'a')

    def append(self, text):
        self.f.write(text + "\n")

    def close(self):
        self.f.close()


mem_total = psutil.virtual_memory().total
net_io = psutil.net_io_counters()
net_sent_old = net_io.bytes_sent
net_recv_old = net_io.bytes_recv
time.sleep(1)

file = fileHandler('perf_data.txt')
file.append('time,cpu,mem,net_sent,net_recv')
i = 0
while i != 10:
    time_clock = time.strftime("%H:%M:%S", time.localtime())
    cpu_util = psutil.cpu_percent()  # float
    mem_util = psutil.virtual_memory().percent

    net_io = psutil.net_io_counters()
    net_io_sent = net_io.bytes_sent
    net_sent_new = net_io_sent - net_sent_old
    net_io_recv = net_io.bytes_recv
    net_recv_new = net_io_recv - net_recv_old
    net_sent_read = net_sent_new / 1024  # kbps
    net_recv_read = net_recv_new / 1024
    net_sent_old = net_io_sent
    net_recv_old = net_io_recv

    # '{0:.2f} Mb'.format(net.bytes_recv / 1024 / 1024)
    txt_line = '{},{},{},{},{}'.format(time_clock, cpu_util, mem_util, round(net_sent_read, 2), round(net_recv_read, 2))
    file.append(txt_line)
    i += 1
    time.sleep(5)
file.close()


# Make a line chart with html file: line_base.html
class PerfData:
    def __init__(self):
        self.file = 'perf_data.txt'
        self.time, self.cpu_utils, self.mem_utils, self.net_sent, self.net_recv = [], [], [], [], []
        self.f = open(self.file, 'r')
        for line in self.f.readlines():
            units = line.split(',')
            self.time.append(units[0])
            self.cpu_utils.append(units[1])
            self.mem_utils.append(units[2])
            self.net_sent.append(units[3])
            self.net_recv.append(units[4])

    def get_time(self):
        return self.time[1:]

    def get_cpu(self):
        return self.cpu_utils[1:]

    def get_mem(self):
        return self.mem_utils[1:]

    def get_netSent(self):
        return self.net_sent[1:]

    def get_netRecv(self):
        return self.net_recv[1:]


"""
Line chart
https://gallery.pyecharts.org/#/Line/line_base
"""

perf = PerfData()
x = perf.get_time()
y1 = perf.get_cpu()
y2 = perf.get_mem()
c = (
    Line()
        .add_xaxis(x)
        .add_yaxis("CPU Utilization", y1)
        .add_yaxis("MEM Utilization", y2)
        .set_global_opts(title_opts=opts.TitleOpts(title="CPU and MEM util(%)"))
        .render("line_base.html")
)
