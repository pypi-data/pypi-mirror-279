from . import baseml_bp
from flask import render_template, jsonify,request
from .config import *
import json,re

@baseml_bp.route('/test')
def test():
    return jsonify({'message': 'test success!'})

@baseml_bp.route('/get_epoch',methods=['GET'])
def get_epoch():
    return jsonify({'metrics': global_varibles['metrics'],'value': global_varibles['value']})

@baseml_bp.route('/select_task',methods=['POST'])
def select_task():
    if request.method == 'POST':
        task = request.json.get("task")
        print("task option",task)
        set_task(task=task)
        print("task now ",global_varibles["task"])
        response_data = {'message': '设置成功!', 'selected_option': task}
        return jsonify(response_data)

@baseml_bp.route('/select_model',methods=['POST'])
def select_model():
    if request.method == 'POST':
        model = request.json.get("model")
        print("model option",model)
        model = re.search(r'（(.*?)）', model).group(1)
        print('send:', model)
        set_model(model=model)
        print("model now ",global_varibles["model"])
        response_data = {'message': '设置成功!', 'selected_option': model}
        return jsonify(response_data)




@baseml_bp.route('/dataset',methods=['GET'])
def dataset():
    return render_template('dataset.html')

@baseml_bp.route('/select_dataset',methods=['POST'])
def select_dataset():
    data = json.loads(request.data)
    dataset = data.get("dataset")
    # 取dataset最后一个文件夹名字以及父文件夹名字
    # 如果路径包含/
    if '/' in  dataset:
        dir_name = dataset.split("/")[len(dataset.split("/"))-2]
        file_name = dataset.split("/")[-1]
    else:
        dir_name = dataset.split("\\")[len(dataset.split("\\"))-2]
        file_name = dataset.split("\\")[-1]
    print("dir_name:",dir_name)
    print("file_name:",file_name)
    dataset = os.path.join(dir_name,file_name)
    print("dataset:",dataset)
    set_dataset(dataset=dataset)
    set_dataset_path(dataset_path=dataset)
    update_dataset_path()
    print("dataset now ",global_varibles["dataset"])
    print("dataset_path now ",global_varibles["dataset_path"])
    # path = pip_settings['workfolder'] + "/checkpoints/basenn_model/"
    path = os.path.join(pip_settings['workfolder'],"checkpoints","baseml_model")
    if not os.path.exists(os.path.join(path,dir_name)):
            os.makedirs(os.path.join(path,dir_name))
    return jsonify({'message': '设置成功!', 'success': True})


@baseml_bp.route('/set_base_cfg',methods=['POST'])
def set_base_cfg():
    if request.method == 'POST':
        try:
            random_seed = request.form['random_seed']
            if update_global_varibles(random_seed=random_seed):
                response_data = {'message': '设置成功!', 'success': True}
            else:
                response_data = {'message': '设置失败!', 'success': False}
        except:
            pass
        try:
            param = request.form['param']
            if update_global_varibles(para=param):
                response_data = {'message': '设置成功!', 'success': True}
            else:
                response_data = {'message': '设置失败!', 'success': False}
        except:
            pass
        try:
            metrics = request.form['metrics']
            if update_global_varibles(metrics=metrics):
                response_data = {'message': '设置成功!', 'success': True}
            else:
                response_data = {'message': '设置失败!', 'success': False}
        except:
            pass
        return jsonify(response_data)
    



@baseml_bp.route('/get_dataset',methods=['GET'])
def get_baseml_dataset():
    print("get_dataset",get_all_dataset())
    return jsonify({'dataset': get_all_dataset()})


