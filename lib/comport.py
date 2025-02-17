import serial


class ComportStream(object):
    def __init__(self, port, timeout):
        self.stream = serial.Serial(port=port, baudrate=115200, timeout=timeout)
        pass

    def close_stream(self):
        self.stream.close()

    def input_command(self, str_command):
        cmd = str_command + "\r"
        self.stream.write(cmd.encode(errors="ignore"))

        list_result = self.stream.readlines()

        for i in range(len(list_result)):
            list_result[i] = list_result[i].decode('utf-8')

        return list_result

    def show_result(self, list_result):
        for i in range(len(list_result)):
            print(list_result[i], end="")

    def read_current(self, size):
        self.stream.read(size)
        list_result = self.stream.readlines()

        for i in range(len(list_result)):
            list_result[i] = list_result[i].decode('utf-8')

        print(list_result)
        return list_result


