
// 任务类型和模型列表,需要实时更新
var modelList = {
    "cls": ["K近邻（KNN）", "支持向量机（SVM）", "朴素贝叶斯（BaiveBayes）", "决策树（CART）", "自适应增强（AdaBoost）", "多层感知机（MLP）", "随机森林（RandomForest）"],
    "reg": ["线性回归（LinearRegression）", "决策树（CART）", "随机森林（RamdomForest）", "多项式回归（Polynomia）","角回归（Lasso）","岭回归（Ridge）","支持向量机（SVM）","自适应增强（AdaBoost）","多层感知机（MLP）"],
    "clt": ["K均值（Kmeans）","谱聚类（Spectral clustering）","层次聚类（Agglomerative clustering）","二叉可伸缩聚类树（Birch）"],
}

// 更新轮播项的内容
function updateCarouselContent(task, model, dataset) {

    var subtitleTasks = document.getElementsByClassName('subtitle-task');
    var subtitleModels = document.getElementsByClassName('subtitle-model');
    var subtitleDatasets = document.getElementsByClassName('subtitle-dataset');

    if (task != null) {
        for (var i = 0; i < subtitleTasks.length; i++) {
            if(task=="cls"){
                subtitleTasks[i].textContent = "已选择的任务类型：分类任务" ;
            }
            else if(task=="reg"){
                subtitleTasks[i].textContent = "已选择的任务类型：回归任务" ;
            }
            else if(task=="clt"){
                subtitleTasks[i].textContent = "已选择的任务类型：聚类任务" ;
            }
        }

    }
    if (model != null) {
        for (var i = 0; i < subtitleModels.length; i++) {
            subtitleModels[i].textContent = "已选择的模型：" + model;
        }
    }
    if (dataset != null) {
        for (var i = 0; i < subtitleDatasets.length; i++) {
            subtitleDatasets[i].textContent = "已选择的数据集：" + dataset;
        }
    }
}

// 函数：点击跳转到下一轮播项
function nextCarouselItem() {
    $('.carousel').carousel('next');
}

document.addEventListener("DOMContentLoaded", function () {

    document.getElementById('task-submit-btn').addEventListener('click', function () {
        // 获取选中的任务类型
        var selectedTask = document.getElementById('task-select').value;
        
        // 构建请求数据
        var requestData = {
            task: selectedTask
        };
        // 发送POST请求到Flask后端
        fetch('/baseml/select_task', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(requestData)
        })
            .then(response => response.json())
            .then(data => {
                // 处理成功响应
                console.log(data);
                // 在这里可以执行其他操作，例如更新页面内容
            })
            .catch(error => {
                // 处理错误
                console.error(error);
            });
        
        updateCarouselContent(selectedTask, null, null);

        if (selectedTask == 'cls') {
            var modelSelect = document.getElementById('model-select');
            modelSelect.innerHTML = '';
            for (var i = 0; i < modelList['cls'].length; i++) {
                var option = document.createElement("option");
                option.text = modelList['cls'][i];
                option.value = modelList['cls'][i];
                modelSelect.appendChild(option);
            }
        }
        else if (selectedTask == 'reg') {
            var modelSelect = document.getElementById('model-select');
            modelSelect.innerHTML = '';
            for (var i = 0; i < modelList['reg'].length; i++) {
                var option = document.createElement("option");
                option.text = modelList['reg'][i];
                option.value = modelList['reg'][i];
                modelSelect.appendChild(option);
            }
        }
        else if (selectedTask == 'clt') {
            var modelSelect = document.getElementById('model-select');
            modelSelect.innerHTML = '';
            for (var i = 0; i < modelList['clt'].length; i++) {
                var option = document.createElement("option");
                option.text = modelList['clt'][i];
                option.value = modelList['clt'][i];
                modelSelect.appendChild(option);
            }
        }
        // 现在，您可以在JavaScript代码中使用modelList
        console.log(modelList);
        // 跳到下一个轮播项
        nextCarouselItem();
    });
    

    // 设置训练参数

    // 表单提交
    document.getElementById("train_cfg_form").addEventListener("submit", function (event) {
        event.preventDefault();

        var formData = new FormData(this);

        // todo：参数检查
        fetch('/baseml/set_base_cfg', {
            method: 'POST',
            body: formData
        })
            .then(response => response.json())
            .then(data => {
                // 处理成功响应
                console.log(data);
                // 在这里可以执行其他操作，例如更新页面内容
                // 显示模态框
                if (data.success) {
                    $('#myModal3').modal('show');
                }
                else {
                    alert("参数设置失败，请检查参数是否正确！");
                }

            })
            .catch(error => {
                // 处理错误
                console.error(error);
            })

    });

    // 提交其他参数到后端
    document.getElementById("advset-submit-btn").addEventListener("click", function (event) {
        event.preventDefault();
        var metricsSelect = document.getElementById("metrics-select");
        var metrics = metricsSelect.options[metricsSelect.selectedIndex].value;
        var lossSelect = document.getElementById("loss-select");
        var loss = lossSelect.options[lossSelect.selectedIndex].value;
        var pretrainedSelect = document.getElementById("pretrained-select");
        var pretrained = pretrainedSelect.options[pretrainedSelect.selectedIndex].value;

        var requestData = {
            "metrics": metrics,
            "loss": loss,
            "pretrained": pretrained
        };
        console.log(requestData);
        fetch('/baseml/set_advance_cfg', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(requestData)
        }).then(response => response.json())
            .then(data => {
                console.log(data);
                if (data.success) {
                    // 跳转到下一轮播页面
                    // $('#myCarousel').carousel('next');
                }
                else {
                    alert("参数设置失败，请检查参数是否正确！");
                }
            });
    });



    // 点击生成代码
    document.getElementById('code-generate-btn').addEventListener('click', function () {
        // 发送POST请求到Flask后端
        fetch('/baseml/get_code', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        })
            .then(response => response.json())
            .then(data => {
                // 处理成功响应
                console.log(data);
                // 在code标签中显示代码
                var code = document.getElementsByTagName('code')[0];
                code.innerHTML = data;
                // 渲染高亮
                hljs.highlightBlock(code);
            })
            .catch(error => {
                // 处理错误
                console.error(error);
            });
    });

    // 点击复制代码到剪贴板
    $(function () { $("[data-toggle='tooltip']").tooltip(); });
    function copyCode2Clipboard() {
        var clipboard = new ClipboardJS('#code-copy-btn');

        var clipbtn = document.getElementById('code-copy-btn');

        clipboard.on('success', function (e) {
            // alert("代码已经复制到剪贴板!");
            e.clearSelection();
            // clipbtn.setAttribute('title','copy to clipboard');
            $('#code-copy-btn').tooltip('show')

            setTimeout(function () {
                $('#code-copy-btn').tooltip('hide')
            }, 1000);


        });
    }

    copyCode2Clipboard();



    var G_totalEpoch = 0;
    var G_checkpoints_path = "";

    function get_epoch() {
        // 从后端获取总epoch
        fetch('/baseml/get_epoch', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            },
        })
            .then(response => response.json())
            .then(data => {
                console.log(data);
                G_totalEpoch = data['epoch'];
            });
    }


    var lossChart = echarts.init(document.getElementById('loss-chart'));
    var accChart = echarts.init(document.getElementById('acc-chart'));

    // 图表配置
    var lossOption = {
        title: {
            text: 'Loss Chart'
        },
        tooltip: {},
        legend: {
            data: ['loss']
        },
        xAxis: {
            data: [],
            name: 'epoch',

        },
        yAxis: {
            name: 'loss',
        },
        series: [{
            name: 'loss',
            type: 'line',
            smooth: true,
            data: []
        }]
    };

    var accOption = {
        title: {
            text: 'Accuracy Chart'
        },
        tooltip: {},
        legend: {
            data: ['accuracy']
        },
        xAxis: {
            data: [],
            name: 'epoch',
        },
        yAxis: {
            name: 'accuracy',
        },
        series: [{
            name: 'accuracy',
            type: 'line',
            smooth: true,
            data: []
        }]
    };





    var total_log_data = [];

    // 点击结束训练按钮，发送请求到后端
    document.getElementById('stop-train-btn').addEventListener('click', function () {
        fetch('/baseml/stop_thread', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            },
        })
            .then(response => response.json())
            .then(data => {
                console.log(data);
                // 训练按钮被启用
                document.getElementById('start-train-btn').disabled = false;
                lossChart.hideLoading();
                accChart.hideLoading();
                // console.log(total_log_data);
                if (data.success) {
                    $('#trainTerminateModal').modal('show');
                }
                else {
                    trainTerminateModal = document.getElementById('trainTerminateModal');
                    body = trainTerminateModal.getElementsByClassName("modal-body")[0];
                    p = body.getElementsByTagName("p")[0];
                    p.innerHTML = data.message;
                    // 设置自动换行
                    p.style.wordWrap = "break-word";
                    $('#trainTerminateModal').modal('show');
                }

            });
    });

    num = 0;
    const socket = io.connect('http://localhost:5000');

    function setTrainFinishModal(checkpoints_path) {
        console.log("setTrainFinishModal");
        var trainFinishModal = document.getElementById('trainFinishModal');
        trainFinishModal.setAttribute("aria-labelledby", "Train Finish");
        body = trainFinishModal.getElementsByClassName("modal-body")[0];
        p = body.getElementsByTagName("p")[0];
        p.innerHTML = "训练已经结束，模型权重和日志保存路径为:" + checkpoints_path;
        // 设置自动换行
        p.style.wordWrap = "break-word";
        $('#trainFinishModal').modal('show');
    }

    function setTrainProgressBar(epochs) {
        console.log("setTrainProgressBar", epochs, G_totalEpoch);
        console.log(epochs / G_totalEpoch);
        var percent = (epochs + 1) / G_totalEpoch * 100;
        // console.log(percent);
        var progressBar = document.getElementById('progress-bar');
        progressBar.setAttribute("aria-valuenow", percent.toString());
        progressBar.style.width = percent.toString() + "%";
    }

    function clearTrainProgressBar() {
        var progressBar = document.getElementById('progress-bar');
        progressBar.setAttribute("aria-valuenow", "0");
        progressBar.style.width = "0%";
    }

});
// 选择模型
document.getElementById('model-submit-btn').addEventListener('click', function () {
    // 获取选中的任务类型
    var selectedModel = document.getElementById('model-select').value;
    // 构建请求数据
    var requestData = {
        model: selectedModel
    };
    // 发送POST请求到Flask后端
    fetch('/baseml/select_model', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(requestData)
    })
        .then(response => response.json())
        .then(data => {
            // 处理成功响应
            console.log(data);
        })
        .catch(error => {
            // 处理错误
            console.error(error);
        });

    updateCarouselContent(null, selectedModel, null);
    // 跳到下一个轮播项
    nextCarouselItem();

});

// 在页面渲染时，获取本地数据集
// 在跳转到第三个轮播项时，获取本地数据集
// 监听跳转到第三个页面：

$(document).ready(function () {
    $('#myCarousel').on('slid.bs.carousel', function () {
        var currentIndex = $('#myCarousel .active').index();
        if (currentIndex == 2) {
            fetch('/baseml/get_dataset', {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json'
                },
            })
                .then(response => response.json())
                .then(data => {
                    console.log(data);
                    // 将数据集列表添加到下拉框中
                    var datasetSelect = document.getElementById("dataset-select");
                    for (var i = 0; i < data.dataset.length; i++) {
                        var option = document.createElement("option");
                        // replace \\ with /
                        option.text = data.dataset[i];
                        option.value = data.dataset[i];
                        datasetSelect.add(option);
                    }
                });
        }

        else if (currentIndex == 0) {
            var selectedModel = document.getElementById('model-select').value;
            updateCarouselContent(null, selectedModel, null);
        }
        else if (currentIndex == 1) {
            var selectedTask = document.getElementById('task-select').value;
            updateCarouselContent(selectedTask, null, null);
        }
        // 跳转到训练页面
        else if (currentIndex == 4){
            fetch('/get_xedu_pkg', {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json'
                },
            })
            .then(response => response.json())
            .then(data => {
                console.log(data);
                if (data['BaseML'] == false) {
                    alert("没有安装BaseML，请先安装BaseML!");
                }
            });
        }
    });
});



// 选择数据集
document.getElementById('dataset-submit-btn').addEventListener('click', function () {
    // 获取选中的任务类型
    var selectedDataset = document.getElementById('dataset-select').value;
    // 构建请求数据
    var requestData = {
        dataset: selectedDataset
    };
    console.log(requestData);
    // 发送POST请求到Flask后端
    fetch('/baseml/select_dataset', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(requestData)
    })
        .then(response => response.json())
        .then(data => {
            // 处理成功响应
            console.log(data);
            // 在这里可以执行其他操作，例如更新页面内容
        })
        .catch(error => {
            // 处理错误
            console.error(error);
        });
    updateCarouselContent(null, null, selectedDataset);
    // 跳到下一个轮播项
    nextCarouselItem();

});
// 给goto-train-btn绑定事件，点击跳转到训练页面
document.getElementById('goto-train-btn').addEventListener('click', function () {
    console.log(111222)
    nextCarouselItem();
});

// 点击开始训练按钮，发送请求到后端
document.getElementById('start-train-btn').addEventListener('click', function () {
    console.log("start training");
    fetch('/baseml/start_thread', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        },
    }).then(response => response.json())
        .then(data => {
            console.log(data);
        });
    document.getElementById('start-train-btn').disabled = true;
    // 按钮被禁用
    // document.getElementById('start-train-btn').disabled = true;
});