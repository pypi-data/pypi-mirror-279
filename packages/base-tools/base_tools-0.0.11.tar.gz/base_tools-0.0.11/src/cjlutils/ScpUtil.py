import sys

import paramiko


# ---------- 定义函数 ----------
def _is_empty(s: str) -> bool:
    return s is None or len(s) <= 0


def transport_files(host_name: str, account: str, password: str, push_file_path_list: list[list[str]] = None,
                    pull_file_path_list: list[list[str]] = None) -> bool:
    if push_file_path_list is None and pull_file_path_list is None:
        print('transport_files: nothing to be done')
        return True
    ssh = paramiko.SSHClient()
    # 允许连接不在know_hosts文件中的主机
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # 建立连接
    ssh.connect(host_name, username=account, port=22, password=password)

    transport = paramiko.Transport((host_name, 22))
    transport.connect(username=account, password=password)
    sftp = paramiko.SFTPClient.from_transport(transport)
    caught_exception = False
    if push_file_path_list is not None:
        for push_file_pair in push_file_path_list:
            try:
                if push_file_pair is None or len(push_file_pair) < 2:
                    continue
                print(f'pushing file from {push_file_pair[0]} to {push_file_pair[1]}')
                sftp.put(push_file_pair[0], push_file_pair[1])
            except Exception as e:
                print(f'push file error: {e}')
                caught_exception = True

    if pull_file_path_list is not None:
        for pull_file_pair in pull_file_path_list:
            try:
                if pull_file_pair is None or len(pull_file_pair) < 2:
                    continue
                print(f'pulling file from {pull_file_pair[0]} to {pull_file_pair[1]}')
                sftp.get(pull_file_pair[0], pull_file_pair[1])
            except Exception as e:
                print(f'pull file error: {e}')
                caught_exception = True

    transport.close()
    return not caught_exception


# ---------- 输入变量 ----------
if __name__ == '__main__':
    argv_len: int = len(sys.argv)
    print('请输入远程连接')
    host_name = sys.argv[1] if argv_len > 1 else input()
    print(host_name)

    print('请输入账号')
    account = sys.argv[2] if argv_len > 2 else input()
    print(account)

    print('请输入密码')
    password = sys.argv[3] if argv_len > 3 else input()
    print(password)

    print('请输入要上传文件的本地路径，需要包括文件名，空代表不上传。路径包括空格，可用双引号包裹空格')
    push_local_path = sys.argv[4] if argv_len > 4 else input()
    print(push_local_path)

    push_path_list = None
    if not _is_empty(push_local_path):
        print('请输入要上传文件的远端路径，需要包括文件名，空代表不上传')
        push_remote_path = sys.argv[5] if argv_len > 5 else input()
        print(push_remote_path)
        push_path_list = None if _is_empty(push_remote_path) else [
            [push_local_path, push_remote_path]
        ]
    print('上传参数：%s' % push_path_list)

    print('请输入要下载文件的远端路径，需要包括文件名，空代表不下载')
    pull_remote_path = sys.argv[6] if argv_len > 6 else input()
    print(pull_remote_path)

    pull_path_list = None
    if not _is_empty(pull_remote_path):
        print('请输入要下载文件的本地路径，需要包括文件名，空代表不下载')
        pull_local_path = sys.argv[7] if argv_len > 7 else input()
        print(pull_local_path)
        pull_path_list = None if _is_empty(pull_local_path) else [
            [pull_remote_path, pull_local_path]
        ]

    print('下载参数：%s' % pull_path_list)

    transport_files(host_name, account, password, push_path_list, pull_path_list)