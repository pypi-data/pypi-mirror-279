import os
from flask import current_app

def back2pwd(pwd,level):
    """
    返回上`level`数级目录的绝对路径
    """
    for i in range(level+1):
        pwd = os.path.abspath(os.path.dirname(pwd))
    return pwd

pip_settings = {
    "workfolder" : os.getcwd(), # pip包安装特有
}

global_varibles = {
    "task":"reg",
    "model": "LinearRegression",
    "dataset":None,
    "dataset_path": back2pwd(__file__,3) + "?",
    "para":"",
    "checkpoints_path": back2pwd(__file__,3) + "/my_checkpoints", # save fold path
    "pretrained_path": None,
    "metrics": None, # options: acc mae mse
    "loss":"CrossEntropyLoss", # options: CrossEntropyLoss MSELoss L1Loss……
    "random_seed": "",
    "shuffle": True,
    "batch_size": 128,
    "optimizer":"Adam",
    "lr":0.01,
    "epochs":10,
    "value": 0,
}

# 设置每个参数，一个方法调整一个参数
def set_task(task):
    global_varibles["task"] = task

def set_model(model):
    global_varibles["model"] = model

def get_all_pkl(pwd):
    pth_list = []
    for file in os.listdir(pwd):
        if os.path.isdir(os.path.join(pwd,file)):
            pth_list.extend(get_all_pkl(os.path.join(pwd,file)))
        else:
            if file.split(".")[-1] == "pkl":
                pth_list.append(file)
    return pth_list

def set_batch_size(batch_size):
    global_varibles["batch_size"] = batch_size

def set_dataset_path(dataset_path):
    global_varibles["dataset_path"] = dataset_path

def set_baseml_checkpoints_path(checkpoints_path):
    global_varibles["checkpoints_path"] = checkpoints_path

def set_loss(loss):
    global_varibles["loss"] = loss

def set_random_seed(random_seed):
    global_varibles["random_seed"] = random_seed

def set_dataset(dataset):
    global_varibles["dataset"] = dataset

def update_global_varibles(**kwargs):
    for k,v in kwargs.items():
        global_varibles[k] = v
    print("global_varibles now ",global_varibles)
    return True

def update_dataset_path():
    # global_varibles["dataset_path"] = pip_settings["workfolder"] + "/datasets/" + global_varibles["dataset"]
    global_varibles["dataset_path"] = os.path.join(pip_settings["workfolder"],"datasets","baseml",global_varibles["dataset"])
    print(global_varibles['dataset'],global_varibles['dataset_path'])

def get_all_dataset():
    dataset_list = []
    # pwd = pip_settings["workfolder"] + "/datasets/basenn"
    pwd = os.path.join(pip_settings["workfolder"],"datasets","baseml")
    dirs = os.listdir(pwd)
    # print(dirs)
    for dir in dirs:
        for file in os.listdir(os.path.join(pwd,dir)):
            # print(os.path.join(pwd,dir,file))
            if os.path.isfile(os.path.join(pwd,dir,file)):
                dataset = os.path.join(pwd,dir,file)
                dataset_list.append(dataset)
    return dataset_list

def update_dataset_path():
    # global_varibles["dataset_path"] = pip_settings["workfolder"] + "/datasets/basenn/" + global_varibles["dataset"]
    global_varibles["dataset_path"] = os.path.join(pip_settings["workfolder"],"datasets","baseml",global_varibles["dataset"])

def _add_code(type,size,activation,**kwarg):
    if activation!="None":
        return f"model.add(layer='{type}',size={size},activation='{activation}')"
    else:
        return f"model.add(layer='{type}',size={size})"
    
def _add_optimizer(optimizer):
    return f"model.add(optimizer='{optimizer}')"

def check_if_regression():
    if global_varibles["metrics"] == "mse" or global_varibles["metrics"] == "mae":
        return True
    else:
        return False

def generate_baseml_code():
    update_dataset_path()
    full_code = ""
    # import
    if global_varibles['task'] == 'cls':
        import_part = "# coding:utf-8"+"\n"+"from BaseML import Classification as cls" + "\n"
    elif global_varibles['task'] == 'reg':
        import_part = "# coding:utf-8"+"\n"+"from BaseML import Regression as reg" + "\n"
    elif global_varibles['task'] == 'clt':
        import_part = "# coding:utf-8"+"\n"+"from BaseML import Cluster as clt" + "\n"
    else:
        import_part = "# coding:utf-8"+"\n"+"from BaseML import Regression as reg" + "\n"
    def_part = "def generated_train():"+"\n"
    
    if global_varibles['task'] == 'cls':
        model_part = "\t"+"model = cls('" + global_varibles['model'] + "')\n"
    elif global_varibles['task'] == 'reg':
        model_part = "\t"+"model = reg('" + global_varibles['model'] + "')\n"
    elif global_varibles['task'] == 'clt':
        model_part = "\t"+"model = clt('" + global_varibles['model'] + "')\n"
    else:
        model_part = "\t"+"model = reg('" + global_varibles['model'] + "')\n"
    # 如果dataset不是文件夹，那么设置dataset路径
    if len(global_varibles['random_seed'])>0:
        dataset_part = "\t"+f"model.load_tab_data(r'{global_varibles['dataset_path']}', random_seed={global_varibles['random_seed']})"+ "\n"
    else:
        dataset_part = "\t"+f"model.load_tab_data(r'{global_varibles['dataset_path']}')"+ "\n"
    # set_para
    if len(global_varibles['para'])>0:
        set_para_part = "\t"+f"model.set_para({global_varibles['para']})" + "\n"
    else:
        set_para_part = ""
    # train
    if global_varibles['model']=='MLP':
        train_part = "\t"+f"model.train(lr={global_varibles['lr']}, epochs={global_varibles['epochs']})" + "\n"+ f"\tmodel.save(r'{global_varibles['checkpoints_path']}/{global_varibles['task']}.pkl')\n"
    else:
        train_part = f"\tmodel.train()\n\tmodel.save(r'{global_varibles['checkpoints_path']}/{global_varibles['task']}.pkl')\n"

    valid_part = ''
    # valid
    if global_varibles['metrics']==None:
        if global_varibles['task'] == 'cls':
            global_varibles['metrics']='acc'
        elif global_varibles['task'] == 'reg':
            global_varibles['metrics']='r2'
        elif global_varibles['task'] == 'clt':
            global_varibles['metrics']='Silhouette Score'
    valid_part = f"\tmodel.valid(r'{global_varibles['dataset_path']}',metrics='{global_varibles['metrics']}')\n"

    entry_part = "\n"+"if __name__ == '__main__':"+"\n"+"\t"+"generated_train()"+"\n"
    full_code = import_part + "\n" + def_part +model_part + dataset_part + set_para_part + train_part + valid_part + entry_part
    with current_app.app_context():
        with open("baseml_code.py","w") as f:
            f.write(full_code)
        return full_code


# generate_code()