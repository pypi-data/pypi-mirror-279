# -*- coding: UTF-8 -*-
from flask import Flask,render_template,jsonify,redirect,url_for

import json
from multiprocessing import Process,Pipe 
import time
import os
import subprocess
from .apis.mmedu.config import set_mmedu_checkpoints_path,generate_mmedu_code
from .apis.baseml.config import set_baseml_checkpoints_path,generate_baseml_code
from .apis.baseml.config import global_varibles as baseml_global_varibles
from .extensions import app,socketio
from .apis.basenn.config import set_basenn_checkpoints_path,generate_basenn_code,back2pwd,global_varibles

from .apis.mmedu.config import global_varibles as mmedu_global_varibles



@app.route('/')
def index():
    return redirect(url_for('mmedu.index'),code=301)
@app.route('/baseml/')
def baseml():
    return render_template('basemlPage.html',dataset=baseml_global_varibles['dataset'])
@app.route('/basenn/')
def basenn():
    return render_template('basennPage.html',dataset=global_varibles['dataset'])



mmedu_shared_data = {
    'message':None,
    'IsRunning':False,
    'time_stamp':'',
    'train_times':0,
    "pid":None
}
baseml_shared_data = {
    'message':None,
    'IsRunning':False,
    'time_stamp':'',
    'train_times':0,
    "pid":None
}
basenn_shared_data = {
    'message':None,
    'IsRunning':False,
    'time_stamp':'',
    'train_times':0,
    "pid":None
}


mmedu_running_process = None
basenn_running_process = None
baseml_running_process = None



def mmedu_train_task(child_conn,workfolder):
    global mmedu_shared_data
    mmedu_shared_data['IsRunning'] = True
    global mmedu_running_process
    print("training_thread")
    mmedu_shared_data['message'] = "正在训练 ……"
    mmedu_shared_data['IsRunning'] = True
    print("isRunning",mmedu_shared_data['IsRunning'])
    import sys
    mmedu_running_process = subprocess.Popen([f"{sys.executable}",os.path.join(workfolder,"mmedu_code.py")],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print(mmedu_running_process.pid)
    child_conn.send(mmedu_running_process.pid)
    out,error = mmedu_running_process.communicate() # 尝试打印运行时的报错
    mmedu_shared_data['IsRunning'] = False
    if error:
    # 将error编码为utf-8
        try:
            error = error.decode('utf-8')
        except:
            error = error.decode('gbk')
        print("error",error)
    print("subprocess end")
    
def baseml_train_task():
    global baseml_shared_data
    baseml_shared_data['IsRunning'] = True
    global baseml_running_process
    print("training_thread")
    baseml_shared_data['message'] = "正在训练 ……"
    import sys
    mmedu_running_process = subprocess.Popen([f"{sys.executable}",os.path.join(workfolder,"baseml_code.py")],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    #baseml_poll_log_socket(baseml_running_process)
    print("subprocess end")
    baseml_shared_data['IsRunning'] = False
    print("isRunning",baseml_shared_data['IsRunning'])

def basenn_train_task():
    global basenn_shared_data
    basenn_shared_data['IsRunning'] = True
    global basenn_running_process
    print("training_thread")
    print(global_varibles)
    print(basenn_shared_data)
    import sys
    # basenn_running_process = subprocess.Popen([f"{sys.executable}",f"{workfolder}/basenn_code.py"],stdout=subprocess.PIPE, stderr=subprocess.PIPE,encoding='gb18030')
    basenn_running_process = subprocess.Popen([f"{sys.executable}",os.path.join(workfolder,"basenn_code.py")],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # 获取子进程输出
    basenn_poll_log_socket(basenn_running_process)
    basenn_running_process = None
    basenn_shared_data['IsRunning'] = False




@socketio.on('log')
def mmedu_poll_log_socket():
    global mmedu_shared_data
    time_stamp = mmedu_shared_data.get('time_stamp', '')
    last_line_num = 0
    print("log_task："+time_stamp)
    from .apis.mmedu.config import pip_settings as mmedu_pip_settings
    # log_path = mmedu_pip_settings['workfolder'] + "/my_checkpoints/" + "mmedu_"+time_stamp
    log_path = os.path.join(mmedu_pip_settings['workfolder'],"my_checkpoints","mmedu_"+time_stamp)
    while True:
        json_files = [x for x in os.listdir(log_path) if x.endswith('.json')]
        if len(json_files) != mmedu_shared_data['train_times']: # 防止多次训练时，没读取到最新的日志文件
            time.sleep(1)
        else:
            log_path = os.path.join(log_path, json_files[-1])
            break
    print("log_path",log_path)
    total_epoch = mmedu_global_varibles['epoch']
    while mmedu_shared_data['IsRunning']:
        if os.path.exists(log_path):
            with open(log_path, 'r') as f:
                lines = f.readlines()
                if len(lines) > last_line_num:
                    for line in lines[last_line_num:]:
                        log = json.loads(line)
                        log = json.dumps(log)
                        socketio.emit('log',log)
                        # print(log)
                        if last_line_num >1 and "val" in log:
                            log = json.loads(log)
                            # print("log",log)
                            if log['epoch'] == total_epoch:
                                print("log_task end")
                                mmedu_shared_data['IsRunning'] = False
                                break
                    last_line_num = len(lines)
                time.sleep(1)
        else:
            print("log_path not exist")
    print("log_task end")

@socketio.on('log')
def baseml_poll_log_socket(baseml_running_process):
    print("baseml_poll_log_socket")
    flag=True
    while flag:
        line = baseml_running_process.stdout.readline()
        error = baseml_running_process.stderr.read()
        if error:
            # 将error编码为utf-8
            try:
                error = error.decode('utf-8')
            except:
                error = error.decode('gbk')
            print("error",error)
            return jsonify({'message': error})
        if line:
            try:
                socketio.emit('log1',line.decode('utf-8'))
            except:
                socketio.emit('log1',line.decode('gbk'))
        else:
            flag=False
            print("log_task end")
            break
    return

@socketio.on('log')
def basenn_poll_log_socket(basenn_running_process):
    print("basenn_poll_log_socket")
    flag=True
    while flag:
        line = basenn_running_process.stdout.readline()
        error = basenn_running_process.stderr.read()
        if error:
            # 将error编码为utf-8
            try:
                error = error.decode('utf-8')
            except:
                error = error.decode('gbk')
            print("error",error)
            return jsonify({'message': error})
        if line:
            try:
                socketio.emit('log1',line.decode('utf-8'))
            except:
                socketio.emit('log1',line.decode('gbk'))
        else:
            flag=False
            print("log_task end")
            break
    return
running_process = None
@app.route('/baseml/start_thread',methods=['GET'])
def baseml_start_thread():
    global baseml_shared_data
    baseml_shared_data['train_times'] += 1
    global baseml_running_process
    if baseml_running_process and baseml_running_process.poll() is None:
        print("已经有一个模型在训练")
        return jsonify({'message': '已经有一个模型在训练'})
    else:
        baseml_shared_data['IsRunning'] = True
        if baseml_shared_data['IsRunning']:
            print("start_thread")
        baseml_train_task()
        return jsonify({'message': '训练已经开始'})


@app.route('/baseml/stop_thread',methods=['GET'])
def baseml_stop_thread():
    if baseml_running_process and baseml_running_process.poll() is None:
        baseml_running_process.terminate()
        return jsonify({'message': '已结束训练','success':True})
    else:
        return jsonify({'message': '没有正在训练的模型','success':False})

@app.route('/basenn/start_thread',methods=['GET'])
def basenn_start_thread():
    global basenn_shared_data
    basenn_shared_data['train_times'] += 1
    global basenn_running_process
    if basenn_running_process and basenn_running_process.poll() is None:
        print("已经有一个模型在训练")
        return jsonify({'message': '已经有一个模型在训练'})
    else:
        basenn_shared_data['IsRunning'] = True
        if basenn_shared_data['IsRunning']:
            print("start_thread")
        basenn_train_task()
        return jsonify({'message': '训练已经开始'})


@app.route('/basenn/stop_thread',methods=['GET'])
def basenn_stop_thread():
    if basenn_running_process and basenn_running_process.poll() is None:
        basenn_running_process.terminate()
        return jsonify({'message': '已结束训练','success':True})
    else:
        return jsonify({'message': '没有正在训练的模型','success':False})



running_process = None

@app.route('/mmedu/start_thread',methods=['GET'])
def mmedu_start_thread():
    global mmedu_shared_data
    mmedu_shared_data['train_times'] += 1
    global mmedu_running_process
    if mmedu_running_process and mmedu_running_process.poll() is None:
        print("已经有一个模型在训练")
        return jsonify({'message': '已经有一个模型在训练'})
    else:
        mmedu_shared_data['IsRunning'] = True
        parent_conn, child_conn = Pipe()
        running_process= Process(target=mmedu_train_task,args=(child_conn,workfolder,))
        running_process.start()
        # print("parent process get id",parent_conn.recv())
        train_pid = parent_conn.recv()
        mmedu_shared_data['pid'] = train_pid
        # mmedu_train_task()
        mmedu_poll_log_socket()
        return jsonify({'message': '训练已经开始'})


@app.route('/mmedu/stop_thread',methods=['GET'])
def mmedu_stop_thread():
    global mmedu_shared_data
    print(mmedu_shared_data)
    # 根据pid结束进程 
    if mmedu_shared_data['pid']:
        if os.name == 'nt':
            os.system("taskkill /pid "+str(mmedu_shared_data['pid'])+" /f")
        # 如果是linux系统，则使用下面的命令
        elif os.name == 'posix': 
            os.system("kill -9 "+str(mmedu_shared_data['pid']))
        mmedu_shared_data['pid'] = None
        return jsonify({'message': '已结束训练'},{'success':True})
    else:
        return jsonify({'message': '没有正在训练的模型','success':False})



@app.route('/mmedu/get_code',methods=['GET'])
def get_mmedu_code():
    global mmedu_shared_data
    print("get_mmedu_code")
    # make dir for checkpoints
    t = time.strftime('%Y%m%d_%H%M%S', time.localtime())
    from .apis.mmedu.config import pip_settings as mmedu_pip_settings
    # checkpoints_path = mmedu_pip_settings['workfolder'] + "/my_checkpoints/" + "mmedu_"+t
    checkpoints_path = os.path.join(mmedu_pip_settings['workfolder'],"my_checkpoints","mmedu_"+t)
    print("checkpoints_path: ",checkpoints_path)
    os.mkdir(checkpoints_path)
    set_mmedu_checkpoints_path(checkpoints_path=checkpoints_path)
    mmedu_shared_data['time_stamp'] = t
    print("time_stamp",mmedu_shared_data['time_stamp'])
    full_code = generate_mmedu_code()

    return jsonify(full_code)


@app.route('/baseml/get_code',methods=['GET'])
def get_baseml_code():
    print(1)
    global baseml_shared_data
    print("get_baseml_code")
    # make dir for checkpoints
    t = time.strftime('%Y%m%d_%H%M%S', time.localtime())
    from .apis.baseml.config import pip_settings as baseml_pip_settings
    # checkpoints_path = basenn_pip_settings['workfolder'] + "/my_checkpoints/"  + "basenn_"+t
    checkpoints_path = os.path.join(baseml_pip_settings['workfolder'],"my_checkpoints","baseml_"+t)
    print("checkpoints_path: ",checkpoints_path)
    os.mkdir(checkpoints_path)
    set_baseml_checkpoints_path(checkpoints_path=checkpoints_path)
    print("global_varibles",baseml_global_varibles)
    baseml_shared_data['time_stamp'] = t
    print("time_stamp",baseml_shared_data['time_stamp'])
    full_code = generate_baseml_code()
    return jsonify(full_code)


@app.route('/basenn/get_code',methods=['GET'])
def get_basenn_code():
    global basenn_shared_data
    print("get_basenn_code")
    # make dir for checkpoints
    t = time.strftime('%Y%m%d_%H%M%S', time.localtime())
    from .apis.basenn.config import pip_settings as basenn_pip_settings
    # checkpoints_path = basenn_pip_settings['workfolder'] + "/my_checkpoints/"  + "basenn_"+t
    checkpoints_path = os.path.join(basenn_pip_settings['workfolder'],"my_checkpoints","basenn_"+t)
    print("checkpoints_path: ",checkpoints_path)
    os.mkdir(checkpoints_path)
    set_basenn_checkpoints_path(checkpoints_path=checkpoints_path)
    print("global_varibles",global_varibles)
    basenn_shared_data['time_stamp'] = t
    print("time_stamp",basenn_shared_data['time_stamp'])
    full_code = generate_basenn_code()
    return jsonify(full_code)


@app.route('/get_xedu_pkg',methods=['GET'])
def get_xedu_pkg():
    import pkg_resources
    packages = [dist.project_name for dist in pkg_resources.working_set]
    res = {
        "MMEdu":False,
        "BaseML":False,
        "BaseNN":False,
    }
    # 如果packages中有BaseNN，则res中加入BaseNN:false,否则加入BaseNN:true
    if "BaseNN" in packages:
        res["BaseNN"] = True
    if "BaseML" in packages:
        res["BaseML"] = True
    if "MMEdu" in packages:
        res["MMEdu"] = True
    return jsonify(res)


def exist_or_mkdir(path):
    if not os.path.exists(path):
        os.mkdir(path)
    else:
        return

def check_workfolder(pwd):
    # 检查pwd下是否有datasets,checkpoints,my_checkpoints文件夹
    # exist_or_mkdir(pwd+"/datasets")
    exist_or_mkdir(os.path.join(pwd,"datasets"))
    # exist_or_mkdir(pwd+"/checkpoints")
    exist_or_mkdir(os.path.join(pwd,"checkpoints"))
    # exist_or_mkdir(pwd+"/my_checkpoints")
    exist_or_mkdir(os.path.join(pwd,"my_checkpoints"))
    # 检查datasets下是否有mmedu_cls,mmedu_det,basenn,basenn_文件夹
    # exist_or_mkdir(pwd+"/datasets/mmedu_cls")
    exist_or_mkdir(os.path.join(pwd,"datasets","mmedu_cls"))
    # exist_or_mkdir(pwd+"/datasets/mmedu_det")
    exist_or_mkdir(os.path.join(pwd,"datasets","mmedu_det"))
    # exist_or_mkdir(pwd+"/datasets/basenn")
    exist_or_mkdir(os.path.join(pwd,"datasets","basenn"))
    exist_or_mkdir(os.path.join(pwd,"datasets","baseml"))
    # 检查checkpoints下是否有mmedu_cls_model,mmedu_det_model,basenn_model文件夹
    # exist_or_mkdir(pwd+"/checkpoints/mmedu_cls_model")
    exist_or_mkdir(os.path.join(pwd,"checkpoints","mmedu_cls_model"))
    # exist_or_mkdir(pwd+"/checkpoints/mmedu_det_model")
    exist_or_mkdir(os.path.join(pwd,"checkpoints","mmedu_det_model"))
    # exist_or_mkdir(pwd+"/checkpoints/basenn_model")
    exist_or_mkdir(os.path.join(pwd,"checkpoints","basenn_model"))
    exist_or_mkdir(os.path.join(pwd,"checkpoints","baseml_model"))
    # 后续可做：下载预训练模型和数据集，放到对应文件夹下。
    


# 设置命令行参数解析
def get_args():
    import argparse
    parser = argparse.ArgumentParser(description='EasyTrain')
    parser.add_argument('--workfolder',default=os.getcwd(), help='workfolder path (default: current path)')
    return parser.parse_args()


workfolder = None
def main():
    pwd = get_args().workfolder
    check_workfolder(pwd)
    global workfolder
    workfolder = pwd
    from .apis.mmedu.config import pip_settings as mmedu_pip_settings
    from .apis.basenn.config import pip_settings as basenn_pip_settings
    from .apis.baseml.config import pip_settings as baseml_pip_settings
    mmedu_pip_settings["workfolder"] = pwd
    baseml_pip_settings["workfolder"] = pwd
    basenn_pip_settings["workfolder"] = pwd
    #basenn
    app.run(host='0.0.0.0',port=5000)


if __name__ == '__main__':
    # app.run(port=5000)
    # socketio.run(app,port=5000)
    # app.run(debug=True,port=5000)
    main()