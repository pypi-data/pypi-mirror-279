import requests

class Instance:
    def __init__(self, apikey, url):
        self.apikey = apikey
        self.url = url
        self.database = self.database(apikey, url)  # Initialize nested class instance
        self.files = self.files(apikey, url)  # Initialize nested class instance
        self.schedules = self.schedules(apikey, url)  # Initialize nested class instance
        self.users = self.users(apikey, url)  # Initialize nested class instance
        self.backups = self.backups(apikey, url)  # Initialize nested class instance
        self.startup_settings = self.startup(apikey, url)  # Initialize nested class instance
        self.headers = {
            "Authorization": "Bearer " + self.apikey,
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    def server_details(self, server_id):
        response = requests.get(self.url + "/api/client/servers/" + str(server_id), headers=self.headers)
        try:
            if response.json()["errors"] is not None:
                if response.json()["errors"]["code"] == "NotFoundHttpException":
                    return {"error": "Server not found"}
                else:
                    raise Exception(response.json()["errors"]["detail"])
        except:
            pass
        return response.json()
    def resource_usage(self, server_id):
        response = requests.get(self.url + "/api/client/servers/" + str(server_id) + "/resources", headers=self.headers)
        try:
            if response.json()["errors"] is not None:
                if response.json()["errors"]["code"] == "NotFoundHttpException":
                    return {"error": "Server not found"}
                else:
                    raise Exception(response.json()["errors"]["detail"])
        except:
            pass
        return response.json()
    def send_command(self, server_id, command):
        response = requests.post(self.url + "/api/client/servers/" + str(server_id) + "/command", headers=self.headers, json={"command": command})
        try:
            if response.json()["errors"] is not None:
                if response.json()["errors"]["code"] == "NotFoundHttpException":
                    return {"error": "Server not found"}
                else:
                    raise Exception(response.json()["errors"]["detail"])
        except:
            pass
        return {"success": True}
    def reboot(self, server_id):
        response = requests.post(self.url + "/api/client/servers/" + str(server_id) + "/power", headers=self.headers, json={"signal": "restart"})
        try:
            if response.json()["errors"] is not None:
                if response.json()["errors"]["code"] == "NotFoundHttpException":
                    return {"error": "Server not found"}
                else:
                    raise Exception(response.json()["errors"]["detail"])
        except:
            pass
        return {"success": True}
    def shutdown(self, server_id):
        response = requests.post(self.url + "/api/client/servers/" + str(server_id) + "/power", headers=self.headers, json={"signal": "stop"})
        try:
            if response.json()["errors"] is not None:
                if response.json()["errors"]["code"] == "NotFoundHttpException":
                    return {"error": "Server not found"}
                else:
                    raise Exception(response.json()["errors"]["detail"])
        except:
            pass
        return {"success": True}
    def start(self, server_id):
        response = requests.post(self.url + "/api/client/servers/" + str(server_id) + "/power", headers=self.headers, json={"signal": "start"})
        try:
            if response.json()["errors"] is not None:
                if response.json()["errors"]["code"] == "NotFoundHttpException":
                    return {"error": "Server not found"}
                else:
                    raise Exception(response.json()["errors"]["detail"])
        except:
            pass
        return {"success": True}
    def kill(self, server_id):
        response = requests.post(self.url + "/api/client/servers/" + str(server_id) + "/power", headers=self.headers, json={"signal": "kill"})
        try:
            if response.json()["errors"] is not None:
                if response.json()["errors"]["code"] == "NotFoundHttpException":
                    return {"error": "Server not found"}
                else:
                    raise Exception(response.json()["errors"]["detail"])
        except:
            pass
        return {"success": True}
    class database:
        def __init__(self, apikey, url):
            self.apikey = apikey
            self.url = url
            self.headers = {
                "Authorization": "Bearer " + self.apikey,
                "Content-Type": "application/json",
                "Accept": "application/json",
            }
            self.no_content_headers = {
                "Authorization": "Bearer " + self.apikey,
                "Accept": "application/json",
            }
        def list_databases(self, server_id):
            response = requests.get(self.url + "/api/client/servers/" + str(server_id) + "/databases", headers=self.headers)
            return response.json()
        def create_database(self, server_id, database_name, allowed_ips):
            response = requests.post(self.url + "/api/client/servers/" + str(server_id) + "/databases", headers=self.headers, json={"database": database_name, "remote": allowed_ips})
            return response.json()
        
        def rotate_password(self, server_id, database_id):
            response = requests.post(self.url + "/api/client/servers/" + str(server_id) + "/databases/" + str(database_id) + "/rotate-password", headers=self.no_content_headers)
            return response.json()
        def delete_database(self, server_id, database_id):
            response = requests.delete(self.url + "/api/client/servers/" + str(server_id) + "/databases/" + str(database_id), headers=self.no_content_headers)
            return response.json()
    class files:
        def __init__(self, apikey, url):
            self.apikey = apikey
            self.url = url
            self.headers = {
                "Authorization": "Bearer " + self.apikey,
                "Content-Type": "application/json",
                "Accept": "application/json",
            }
            self.no_content_headers = {
                "Authorization": "Bearer " + self.apikey,
                "Accept": "application/json",
            }
        def list_files(self, server_id, directory):
            response = requests.get(self.url + "/api/client/servers/" + str(server_id) + "/files/list?directory=" + directory, headers=self.headers)
            return response.json()
        def get_file_contents(self, server_id, file_path):
            response = requests.get(self.url + "/api/client/servers/" + str(server_id) + "/files/contents?file=" + file_path, headers=self.headers)
            return response.json()
        def write_file_contents(self, server_id, file_path, contents):
            response = requests.post(self.url + "/api/client/servers/" + str(server_id) + "/files/write?file=" + file_path, headers=self.headers, json={"contents": contents})
        def generate_download_file_url(self, server_id, file_path):
            response = requests.get(self.url + "/api/client/servers/" + str(server_id) + "/files/download?file=" + file_path, headers=self.headers)
            return response.json()
        def rename_file(self, server_id, old_path, new_path, root):
            response = requests.post(self.url + "/api/client/servers/" + str(server_id) + "/files/rename", headers=self.headers, json={"root": root, "from": old_path, "to": new_path})

        def copy_file(self, server_id, location):
            response = requests.post(self.url + "/api/client/servers/" + str(server_id) + "/files/copy", headers=self.headers, json={"location": location})

        def compress_file(self, server_id, files):
            response = requests.post(self.url + "/api/client/servers/" + str(server_id) + "/files/compress", headers=self.headers, json={"files": files})
            return response.json()
        def decompress(self, server_id, file, root):
            response = requests.post(self.url + "/api/client/servers/" + str(server_id) + "/files/decompress", headers=self.headers, json={"file": file, "root": root})
        def delete_file(self, server_id, files, root):
            response = requests.post(self.url + "/api/client/servers/" + str(server_id) + "/files/delete", headers=self.headers, json={"files": files, "root": root})
        def create_folder(self, server_id, folder_name, root):
            response = requests.post(self.url + "/api/client/servers/" + str(server_id) + "/files/create-folder", headers=self.headers, json={"name": folder_name, "root": root})
    class schedules:
        def __init__(self, apikey, url):
            self.apikey = apikey
            self.url = url
            self.headers = {
                "Authorization": "Bearer " + self.apikey,
                "Content-Type": "application/json",
                "Accept": "application/json",
            }
            self.no_content_headers = {
                "Authorization": "Bearer " + self.apikey,
                "Accept": "application/json",
            }
        def list_schedules(self, server_id):
            response = requests.get(self.url + "/api/client/servers/" + str(server_id) + "/schedules", headers=self.headers)
            return response.json()
        def create_schedule(self, server_id, name, minute, hour, day_of_month, month, day_of_week):
            response = requests.post(self.url + "/api/client/servers/" + str(server_id) + "/schedules", headers=self.headers, json={"name": name, "minute": minute, "hour": hour, "day_of_month": day_of_month, "month": month, "day_of_week": day_of_week, "is_active": True})
            return response.json()
        def get_schedule(self, server_id, schedule_id):
            response = requests.get(self.url + "/api/client/servers/" + str(server_id) + "/schedules/" + str(schedule_id), headers=self.headers)
            return response.json()
        def edit_schedule(self, server_id, schedule_id, name, minute, hour, day_of_month, month, day_of_week):
            response = requests.put(self.url + "/api/client/servers/" + str(server_id) + "/schedules/" + str(schedule_id), headers=self.headers, json={"name": name, "minute": minute, "hour": hour, "day_of_month": day_of_month, "month": month, "day_of_week": day_of_week, "is_active": True})
            return response.json()
        def delete_schedule(self, server_id, schedule_id):
            response = requests.delete(self.url + "/api/client/servers/" + str(server_id) + "/schedules/" + str(schedule_id), headers=self.no_content_headers)
        def add_task(self, server_id, schedule_id, action_type, payload):
            response = requests.post(self.url + "/api/client/servers/" + str(server_id) + "/schedules/" + str(schedule_id) + "/tasks", headers=self.headers, json={"action": action_type, "payload": payload, "time_offset": 0})
            return response.json()
        def edit_task(self, server_id, schedule_id, task_id, action_type, payload, time_offset):
            response = requests.put(self.url + "/api/client/servers/" + str(server_id) + "/schedules/" + str(schedule_id) + "/tasks/" + str(task_id), headers=self.headers, json={"action": action_type, "payload": payload, "time_offset": time_offset})
            return response.json()
        def delete_task(self, server_id, schedule_id, task_id):
            response = requests.delete(self.url + "/api/client/servers/" + str(server_id) + "/schedules/" + str(schedule_id) + "/tasks/" + str(task_id), headers=self.no_content_headers)
    class network:
        def __init__(self, apikey, url):
            self.apikey = apikey
            self.url = url
            self.headers = {
                "Authorization": "Bearer " + self.apikey,
                "Content-Type": "application/json",
                "Accept": "application/json",
            }
            self.no_content_headers = {
                "Authorization": "Bearer " + self.apikey,
                "Accept": "application/json",
            }
        def get_allocations(self, server_id):
            response = requests.get(self.url + "/api/client/servers/" + str(server_id) + "/network/allocations", headers=self.headers)
            return response.json()
        def set_primary_allocation(self, server_id, allocation_id):
            response = requests.post(self.url + "/api/client/servers/" + str(server_id) + "/network/allocations/" + str(allocation_id) + "/primary", headers=self.headers)
            return response.json()
        def assign_allocation(self, server_id, ip, alias, ports):
            response = requests.post(self.url + "/api/client/servers/" + str(server_id) + "/network/allocations", headers=self.headers, json={"ip": ip, "alias": alias, "ports": ports})
            return response.json()
        def delete_allocation(self, server_id, allocation_id):
            response = requests.delete(self.url + "/api/client/servers/" + str(server_id) + "/network/allocations/" + str(allocation_id), headers=self.no_content_headers)
    class users:
        def __init__(self, apikey, url):
            self.apikey = apikey
            self.url = url
            self.headers = {
                "Authorization": "Bearer " + self.apikey,
                "Content-Type": "application/json",
                "Accept": "application/json",
            }
            self.no_content_headers = {
                "Authorization": "Bearer " + self.apikey,
                "Accept": "application/json",
            }
        def list_users(self, server_id):
            response = requests.get(self.url + "/api/client/servers/" + str(server_id) + "/users", headers=self.headers)
            return response.json()
        def user_details(self, server_id, user_id):
            response = requests.get(self.url + "/api/client/servers/" + str(server_id) + "/users/" + str(user_id), headers=self.headers)
            return response.json()
        def add_user(self, server_id, email, permissions):
            response = requests.post(self.url + "/api/client/servers/" + str(server_id) + "/users", headers=self.headers, json={"email": email, "permissions": permissions})
            return response.json()
        def update_user(self, server_id, user_id, permissions):
            response = requests.put(self.url + "/api/client/servers/" + str(server_id) + "/users/" + str(user_id), headers=self.headers, json={"permissions": permissions})
            return response.json()
        def remove_user(self, server_id, user_id):
            response = requests.delete(self.url + "/api/client/servers/" + str(server_id) + "/users/" + str(user_id), headers=self.no_content_headers)
    class backups:
        def __init__(self, apikey, url):
            self.apikey = apikey
            self.url = url
            self.headers = {
                "Authorization": "Bearer " + self.apikey,
                "Content-Type": "application/json",
                "Accept": "application/json",
            }
            self.no_content_headers = {
                "Authorization": "Bearer " + self.apikey,
                "Accept": "application/json",
            }
        def list_backups(self, server_id):
            response = requests.get(self.url + "/api/client/servers/" + str(server_id) + "/backups", headers=self.headers)
            return response.json()
        def create_backup(self, server_id):
            response = requests.post(self.url + "/api/client/servers/" + str(server_id) + "/backups", headers=self.no_content_headers)
            return response.json()
        def download_backup(self, server_id, backup_uuid):
            response = requests.get(self.url + "/api/client/servers/" + str(server_id) + "/backups/" + str(backup_uuid) + "/download", headers=self.no_content_headers)
            return response.json()
        def backup_details(self, server_id, backup_uuid):
            response = requests.get(self.url + "/api/client/servers/" + str(server_id) + "/backups/" + str(backup_uuid), headers=self.headers)
            return response.json()
        def delete_backup(self, server_id, backup_uuid):
            response = requests.delete(self.url + "/api/client/servers/" + str(server_id) + "/backups/" + str(backup_uuid), headers=self.no_content_headers)
    class startup:
        def __init__(self, apikey, url):
            self.apikey = apikey
            self.url = url
            self.headers = {
                "Authorization": "Bearer " + self.apikey,
                "Content-Type": "application/json",
                "Accept": "application/json",
            }
            self.no_content_headers = {
                "Authorization": "Bearer " + self.apikey,
                "Accept": "application/json",
            }
        def get_variables(self, server_id):
            response = requests.get(self.url + "/api/client/servers/" + str(server_id) + "/startup", headers=self.headers)
            return response.json()
        def update_variable(self, server_id, key, value):
            response = requests.put(self.url + "/api/client/servers/" + str(server_id) + "/startup", headers=self.headers, json={"key": key, "value": value})
            return response.json()
    class settings:
        def __init__(self, apikey, url):
            self.apikey = apikey
            self.url = url
            self.headers = {
                "Authorization": "Bearer " + self.apikey,
                "Content-Type": "application/json",
                "Accept": "application/json",
            }
            self.no_content_headers = {
                "Authorization": "Bearer " + self.apikey,
                "Accept": "application/json",
            }
        def rename_server(self, server_id, new_name):
            response = requests.post(self.url + "/api/client/servers/" + str(server_id) + "/settings/rename", headers=self.headers, json={"name": new_name})
            return response.json()
        def reinstall_server(self, server_id):
            response = requests.post(self.url + "/api/client/servers/" + str(server_id) + "/settings/reinstall", headers=self.headers)
            return response.json()