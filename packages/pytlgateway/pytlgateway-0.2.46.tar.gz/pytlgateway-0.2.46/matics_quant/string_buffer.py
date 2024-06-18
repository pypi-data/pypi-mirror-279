import threading
import json
import trace
class TcpStringBuffer:
    """_summary_:用于tcp 收发的string buffer类
    """
    def __init__(self) -> None:
        self.recv_string_buffer = ''
        self.send_string_buffer = ''
        self.magic_sign = '\r\n'
        self.recv_str_lock = threading.Lock()
        self.send_str_lock = threading.Lock()

    def is_recv_str_empty(self):
        """
        Returns:
            bool: 1 or 0
        """
        return len(self.recv_string_buffer) == 0

    def is_send_str_empty(self):
        """_summary_: check send_list_empty

        """
        return len(self.send_string_buffer) == 0

    def receive(self, data:str):
        """_summary_:get data from socket recv
        Args:
            data (str): input_data
        """
        with self.recv_str_lock:
            self.recv_string_buffer += data
    def get_send(self):
        """send send_string_buffer
        """
        if len(self.send_string_buffer) == 0:
            return
        with self.send_str_lock:
            string_buffer = self.send_string_buffer
            self.send_string_buffer = ''
            return string_buffer
    def push(self, data:dict):
        """
        add  delimiter for tcp_send
        Args:
            data (str): send_data
        """
        new_data = json.dumps(data) + '\r\n'
        with self.send_str_lock:
            self.send_string_buffer += new_data

    def get_recv(self):
        """
        _summary_: 将str_buffer拆成dict_list,并清空
        """
        dict_list = []
        if len(self.recv_string_buffer) == 0:
            return dict_list
        with self.recv_str_lock:
            # 分割字符串并创建字典
            items = self.recv_string_buffer.split(self.magic_sign)
            check_end = self.recv_string_buffer.endswith(self.magic_sign)
            self.recv_string_buffer = ''
            if check_end:
                for item in items[:-1]:
                    try:
                        _dict = json.loads(item)
                        dict_list.append(_dict)
                    except Exception as err:
                        print(f"error: item: {item}, error:{err}")
                        return []
                self.recv_string_buffer = items[-1]
        return dict_list