from grpc_tools import protoc
import os
import sys


IMPORT_PATH = '-I.'
PB2_PATH = '--python_out=.'
PB2_GRPC_PATH = '--grpc_python_out=.'

PROTOS_PATH = f'{os.getcwd()}\\protos'

SELECT_APP:dict[str, int] = {}
SELECT_SERVICE:dict[str, dict[str, int]] = {}
SELECT_PROTO:dict[str, dict[str, dict[str, int]]]  = {}

CURRUNT_ARG = ['--app', '-a', '--service', '-s', '--proto', '-p']

def set_selections(commands_arrguments: list[str]):
    for command in commands_arrguments:
        try:
            if command.startswith("--app") or command.startswith("-a"):
                set_select_app(command)
            elif command.startswith("--service") or command.startswith("-s"):
                set_select_service(command)
            elif command.startswith("--proto") or command.startswith("-p"):
                set_select_proto(command)
            else:
                pass
        except:
            message = """
error : command 형식이 맞지 않음

python -m protobuilder.build <option>
-> protos의 모든 proto file build

option ->
 app : build application 지정
    --app=<application_name> 
    -a=<application_name>
 service : build service 지정
    --service=<application_name>.<service_name> 
    -s=<application_name>.<service_name>
 proto : build proto 지정
    --proto=<application_name>.<service_name>.<proto_name>
    -s=<application_name>.<service_name>.<proto_name>
    비고 : 확장자 유무 상관 없음

ex)
python -m protobuilder.build -p=exam_app.exam_service.exam_proto
python -m protobuilder.build -p=exam_app.exam_service.exam_proto.proto
"""
            print(message)
            exit(0)

def set_select_app(command:str):
    try:
        option, app = command.split("=")
        SELECT_APP[app] = 0
    except:
        exit(0)

def set_select_service(command:str):
    try:
        option, value = command.split("=")
        app, service = value.split(".")
        if not app in SELECT_SERVICE:
            SELECT_SERVICE[app] = {}
        SELECT_SERVICE[app][service] = 0
    except:
        exit(0)

def set_select_proto(command:str):
    try:
        option, value = command.split("=")
        app, service, proto = value.split(".",3)
        if not proto.endswith(".proto"):
            proto += ".proto"

        if not app in SELECT_PROTO:
            SELECT_PROTO[app] = {}
        if not service in SELECT_PROTO[app]:
            SELECT_PROTO[app][service] = {}
        SELECT_PROTO[app][service][proto] = 0
    except:
        exit(0)

def main(commands_arrguments):
    set_selections(commands_arrguments)
    build()
    pass

def check(app, service=None, proto=None):
    for selection in [SELECT_APP, SELECT_SERVICE, SELECT_PROTO]:
        if len(selection) != 0:
            break
    else:
        return True
    if app in SELECT_APP:
        return True
    if app in SELECT_SERVICE:
        if not service:
            return True
        if service in SELECT_SERVICE[app]:
            return True
    if app in SELECT_PROTO:
        if not service:
            return True
        if service in SELECT_PROTO[app]:
            if not proto:
                return True
            if proto in SELECT_PROTO[app][service]:
                return True
    return False
    
def get_proto_path():
    """protos의 구조 반환"""
    path_dict:dict[str, dict[str, list[str]]] = {}
    try:
        for root, dirs, files in tuple(os.walk(PROTOS_PATH))[1:]:
            path = root[len(PROTOS_PATH)+1:].split('\\')

            app = path[0]
            service = None
            if len(path) == 1:
                if not check(app):
                    continue
                path_dict[app] = {}
                continue
            service = path[1]
            if not service or not check(app, service):
                continue
            if not service in path_dict[app]:
                path_dict[app][service] = []

            for file in files:
                if not file.endswith(".proto"):
                    continue
                if check(app, service, file):
                    path_dict[app][service].append(file)
    except Exception as e:
        message = """
error : 디랙토리 구조가 옳지 않음

protos : proto file 저장소
    application : application layer
        service : service layer
            proto : protofile
ex)
protos
├app_1
│ ├service_1
│ │ ├proto_1.proto
│ │ └proto_2.proto
│ └service_2
│   ├proto_1.proto
│   └proto_2.proto
└app2
  ├service_2
  │ ├proto_1.proto
  │ └proto_2.proto
  └service_2
    ├proto_1.proto
    └proto_2.proto
"""
        # print(message)
        print(e)
        exit(0)

    check_used_select()
    return path_dict

def check_used_select():
    for app in SELECT_APP:
        if SELECT_APP[app] == 0:
            print(f"warning : appplication {app}(이)가 존재하지 않음")
    for app in SELECT_SERVICE:
        for service in SELECT_SERVICE[app]:
            if SELECT_SERVICE[app][service] == 0:
                print(f"warning : service {app}.{service}(이)가 존재하지 않음")
    for app in SELECT_PROTO:
        for service in SELECT_PROTO[app]:
            for proto in SELECT_PROTO[app][service]:
                if SELECT_PROTO[app][service][proto] == 0:
                    print(f"warning : proto file {app}.{service}.{proto}(이)가 존재하지 않음")

def build():
    protos_path = get_proto_path()
    for app in protos_path:
        if len(protos_path[app]) == 0:
            print(f"warning : {app}의 service가 존재하지 않음")
        for service in protos_path[app]:
            if len(protos_path[app][service]) == 0:
                print(f"warning : {app}.{service}의 proto file이 존재하지 않음")
            for proto in protos_path[app][service]:
                try: 
                    protoc.main([
                        IMPORT_PATH,
                        PB2_PATH,
                        PB2_GRPC_PATH,
                        f"protos\\{app}\\{service}\\{proto}"
                    ])
                    print(f"{app}.{service}.{proto} 생성")
                except Exception as e:
                    print(f"error : {app}.{service}.{proto} 생성 생성 중 오류 발생")
                    print(e)
                    exit(0)
            
if __name__ == "__main__":
    sys.exit(main(sys.argv))
