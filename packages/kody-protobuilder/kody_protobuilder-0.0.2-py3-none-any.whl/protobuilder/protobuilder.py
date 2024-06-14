from grpc_tools import protoc
import os
import sys

IMPORT_PATH = '-I.'
PB2_PATH = '--python_out=.'
PB2_GRPC_PATH = '--grpc_python_out=.'

PROTOS_PATH = f'{os.path.dirname(os.path.abspath(__file__))}\\protos'

SELECT_APP = {}
SELECT_SERVICE:dict[str, list[str]] = {}

def main(commands_arrguments):
    for i in commands_arrguments:
        try:
            i = str(i)
            if str(i).startswith("--app"):
                SELECT_APP[i.split('=')[1]] = 0
            elif str(i).startswith("-a"):
                SELECT_APP[i.split('=')[1]] = 0
            elif str(i).startswith("--service"):
                app, service = i.split('=')[1].split('.')
                if app in SELECT_SERVICE:
                    SELECT_SERVICE[app].append(service)
                else:
                    SELECT_SERVICE[app] = [service]
            elif str(i).startswith("-s"):
                app, service = i.split('=')[1].split('.')
                if app in SELECT_SERVICE:
                    SELECT_SERVICE[app].append(service)
                else:
                    SELECT_SERVICE[app] = [service]
        except:
            print("error : option 형식의 맞지 않음 \n app : --app=<app> | -a=<app>\n service : --service=<app>.<service> | -s=<app>.<service>")
            exit(0)
    
    build()
    pass

def check_select_app(path: list[str]):
    if len(SELECT_APP) == 0 and len(SELECT_SERVICE) == 0:
        return True
    if path[0] in SELECT_APP:
        SELECT_APP[path[0]] += 1
    if path[0] in SELECT_SERVICE:
        return True
    return False

def check_select_service(path: list[str]):
    if len(SELECT_SERVICE) == 0:
        return True
    if path[0] in SELECT_SERVICE:
        if path[1] in SELECT_SERVICE[path[0]]:
            SELECT_SERVICE[path[0]].remove(path[1])
            return True
    return False

def get_proto_path():
    """protos의 구조 반환\n
    key -> app | value -> list[service]"""
    path_dict:dict[str, list[str]] = {}
    for root, dirs, files in tuple(os.walk(PROTOS_PATH))[1:]:
        path = root[len(PROTOS_PATH)+1:].split('\\')

        # option --app | -a check
        if not check_select_app(path):
            continue
        if len(path) == 1:
            path_dict[path[0]] = []
        elif len(path) == 2:

            # option --service | -s check
            if check_select_service(path):

                if f"{path[1]}.proto" in files: 
                    path_dict[path[0]].append(path[1])
                else:
                    print(f"warning : service {path[1]}(이)가 proto file을 포함하지 않음")
                    pass # service가 proto 파일을 포함하지 않음
        else:
            pass # 예외
    for app in SELECT_APP:
        if SELECT_APP[app] == 0:
            print(f"warning : appplication {app[0]}(이)가 존재하지 않음")
    for app in SELECT_SERVICE:
        for service in SELECT_SERVICE[app]:
            print(f"warning : service {app}의 {service}(이)가 존재하지 않음")
    return path_dict


def build():
    protos_path = get_proto_path()
    for app in protos_path:
        for proto_path in protos_path[app]:   
            try: 
                protoc.main([
                    IMPORT_PATH,
                    PB2_PATH,
                    PB2_GRPC_PATH,
                    f"protos\\{app}\\{proto_path}\\{proto_path}.proto"
                ])
                print(f"{app}의 {proto_path} 생성")
            except Exception as e:
                print(f"error : {app}의 {proto_path} 생성 중 오류 발생")
                print(e)
                exit(0)

if __name__ == "__main__":
    sys.exit(main(sys.argv))
