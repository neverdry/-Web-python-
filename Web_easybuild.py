import socket


class Webserver(object):
    # 初始化方法
    def __init__(self):
        # 1.创建套接字
        tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 2.设置地址重用                当前套接字           重用地址           默认True
        tcp_server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
        # 3.绑定端口
        tcp_server_socket.bind(("", 8081))
        # 4.设置监听
        tcp_server_socket.listen(128)
        # 5.接受客户端链接
        self.tcp_server_socket = tcp_server_socket

    def start(self):
        # 6.接收客户端连接， 并调用request_handler函数
        while True:
            new_client_socket, ip_port = self.tcp_server_socket.accept() # 返回元组对象
            print("新客户来了:", ip_port)
            self.request_handler(new_client_socket, ip_port)


    def request_handler(self, new_client_socket, ip_port):
        """接受信息并作出反应"""
        """7.接受客户端浏览器发出的请求协议"""
        request_data = new_client_socket.recv(1024)
        """本地IP: 192.168.3.4"""
        # print(request_data)

        # 8. 判断协议是否为空
        if not request_data:
            print("%s客户端已经下线！"% str(ip_port))
            new_client_socket.close()
            return

        """根据客户端的请求返回内容"""
        #   1.得到返回报文的字符串
        request_text = request_data.decode()
        #   2.截取第一个换行符出现之前的位置
        loc = request_text.find("\r\n")
        request_line = request_text[:loc]
        #   3.请求行按照空格拆分
        request_line_list = request_line.split(" ")

        #得到资源路径
        file_path = request_line_list[1]

        #设置默认首页(当没有写路径时)
        if file_path == "/":
            file_path = "/Welcome.html"

        #9.响应报文
        #9.1响应行
        response_line = "HTTP/1.1 200 OK\r\n"
        #9.2响应头
        response_header = "Server:myServer\r\n"
        #9.3响应空行
        response_blank = "\r\n"
        #9.4响应主体
        try:
            #打开文件
            with open("resource" + file_path, "rb") as file:
                response_body = file.read()
        # 打开失败
        except Exception as e:
            # 4.1 修改响应行为404
            response_line = "HTTP/1.1 404 Not Found\r\n"
            # 4.2 响应主题报告错误信息
            response_body = "Errors!(%s)" % str(e)
            response_body = response_body.encode()

        #response_body = "HelloWorld!\r\n"
        #10.发送响应报文
        response_data = (response_line + response_header + response_blank).encode() + response_body
        new_client_socket.send(response_data)
        new_client_socket.close()


def main():
    ws = Webserver()
    ws.start()


if __name__ == '__main__':
    main()



