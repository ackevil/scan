#encoding:utf-8
import requests
import json
import logging
import time
class SqlClient():
    def __init__(self):
        self.count=50
        self.timeout=300
        self.serverIP="http://127.0.0.1:8775"
        self.options={"optinos":{"smart":True}}
        self.headers={"Content-Type":"application/json"}
        self.newTask="/task/new"

    def addTask(self,url):
        try:
            taskid=requests.get(self.serverIP+self.newTask).json()["taskid"]
            #{"success": True, "taskid": taskid}
            if not len(taskid)>0 :
                return False
            r=requests.post(self.serverIP+"/option/"+taskid+"/set",data=json.dumps(self.options),headers=self.headers).json()
            #{"success": True}
            if not r["success"]:
                return False
            r=requests.post(self.serverIP + "/scan/" + taskid + "/start", data=json.dumps({'url':url}), headers=self.headers).json()
            #{"success": True, "engineid": DataStore.tasks[taskid].engine_get_id()}
            if not r["success"]:
                return False
            return {"taskid":taskid,"url":url,"startTime":time.time()}
        except Exception as e:
            logging.exception(e)
            return False
    
    def getTaskStatus(self,taskid):
        try:
            url=self.serverIP+"/scan/"+taskid+"/status"
            r=requests.get(url).json()
            #{"success": True,"status": status,"returncode": DataStore.tasks[taskid].engine_get_returncode()}
            # status = "not running"||"terminated"||"running
            if not r["success"]:
                return False
            return r["status"]
        except Exception as e:
            logging.exception(e)
            return False
    
    def getTaskResult(self,taskid):
        try:
            url=self.serverIP+"/scan/"+taskid+"/data"
            r=requests.get(url).json()
            #{"success": True, "data": json_data_message, "error": json_errors_message}
            if  r["success"] and len(r["data"])>0:
                return True
            return False
        except Exception as e:
            logging.exception(e)
            return False
    
    def killTask(self,taskid):
        try:
            requests.get(self.serverIP + '/scan/' + taskid + '/stop')
            requests.get(self.serverIP + '/scan/' + taskid + '/kill')
            requests.get(self.serverIP + '/task/' + taskid + '/delete')
        except Exception as e:
            logging.exception(e)
            return False
    def deleteTask(self,taskid):
        try:
            requests.get(self.serverIP + '/task/' + taskid + '/delete')
        except Exception as e:
            logging.exception(e)
            return False
    
    def run(self):
        f=open("unique-url.txt","r")
        f2=open("inject-url.txt","w")
        tasks=[]
        current=0;
        flag=False
        while True:
            if len(tasks)<self.count and flag==False:
                num=self.count-len(tasks)
                while num>0:
                    if flag:
                        break
                    url=f.readline()
                    url=url.strip()
                    print(url)
                    if url=="":
                        flag=True
                        break
                    if url !="":
                        r=self.addTask(url)
                        if r:
                            tasks.append(r)
                    num=num-1
            time.sleep(10)
            if len(tasks)==0:
                exit()
            for task in tasks:
                status=self.getTaskStatus(task["taskid"])
                if status:
                    if status=="running":
                        if time.time()-task["startTime"]>self.timeout:
                            self.kill(task["taskid"])
                            tasks.remove(task)
                    elif status=="terminated":
                        result=self.getTaskResult(task["taskid"])
                        if result:
                            print(task["url"]+" is injectable")
                            f2.write(task["url"]+"\n")
                        self.deleteTask(task["taskid"])
                        tasks.remove(task)
                    else :
                        self.deleteTask(task["taskid"])
                        tasks.remove(task)

if __name__=="__main__":
    client=SqlClient()
    client.run()
