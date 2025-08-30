// static/js/script.js
// 获取天气信息
function getWeather() {
    // 这里使用模拟数据，实际应用中应调用天气API
    const cities = ['北京市', '上海市', '广州市', '深圳市', '杭州市', '成都市'];
    const temperatures = [28, 30, 32, 33, 29, 27];
    const weatherIcons = ['fa-sun', 'fa-cloud', 'fa-cloud-sun', 'fa-cloud-rain'];

    const randomCity = cities[Math.floor(Math.random() * cities.length)];
    const randomTemp = temperatures[Math.floor(Math.random() * temperatures.length)];
    const randomIcon = weatherIcons[Math.floor(Math.random() * weatherIcons.length)];

    document.getElementById('location').textContent = randomCity;
    document.getElementById('temperature').textContent = `${randomTemp}°C`;

    // 更新天气图标
    const weatherIcon = document.querySelector('.weather-icon');
    weatherIcon.className = `fas ${randomIcon} weather-icon`;
}

// 搜索功能
function setupSearch() {
    const searchBtn = document.querySelector('.search-btn');
    const searchInput = document.querySelector('.search-box');

    if (searchBtn && searchInput) {
        searchBtn.addEventListener('click', performSearch);
        searchInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                performSearch();
            }
        });
    }
}

function performSearch() {
    const searchTerm = document.querySelector('.search-box').value;
    if (searchTerm.trim() !== '') {
        // 实际应用中这里应该执行搜索操作
        console.log(`正在搜索: ${searchTerm}`);
    }
}

// 复制磁力链接
function setupCopyButtons() {
    const copyBtns = document.querySelectorAll('.magnet-btn');
    copyBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            // 实际应用中这里应该获取真实的磁力链接
            const magnetLink = "magnet:?xt=urn:btih:EXAMPLEHASH&dn=Example+Resource";

            navigator.clipboard.writeText(magnetLink).then(() => {
                // 显示复制成功提示
                const originalText = '<i class="fas fa-cloud-download-alt"></i>夸克资源下载';
                btn.innerHTML = '<i class="fas fa-check"></i> 已复制';

                setTimeout(() => {
                    btn.innerHTML = originalText;
                }, 2000);
            });
        });
    });
}

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', function() {
    getWeather();
    setupSearch();
    setupCopyButtons();

    // 每30分钟更新一次天气（模拟）
    setInterval(getWeather, 1800000);
});
// 夸克资源下载功能 - 优化版本
//function setupQuarkDownload() {
//    const quarkBtn = document.querySelector('.quark-btn');
//    if (!quarkBtn) return;
//
//    // 检测设备类型
//    function isMobileDevice() {
//        return /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
//    }
//
//    // 获取Cookie
//    function getCookie(name) {
//        const value = `; ${document.cookie}`;
//        const parts = value.split(`; ${name}=`);
//        if (parts.length === 2) return parts.pop().split(';').shift();
//        return null;
//    }
//
//    // 发送增量下载请求
//    function incrementDownload(articleId) {
//        const csrftoken = getCookie('csrftoken');
//        if (!csrftoken) {
//            console.error('CSRF token not found');
//            return;
//        }
//
//        fetch('/increment-download/', {
//            method: 'POST',
//            headers: {
//                'Content-Type': 'application/json',
//                'X-CSRFToken': csrftoken
//            },
//            body: JSON.stringify({article_id: articleId})
//        })
//        .then(response => {
//            if (!response.ok) throw new Error('网络响应不正常');
//            return response.json();
//        })
//        .then(data => {
//            console.log('下载量已记录:', data);
//
//            // 更新下载统计
//            const weeklyElem = document.getElementById('weekly-downloads');
//            const totalElem = document.getElementById('total-downloads');
//
//            if (weeklyElem) weeklyElem.textContent = data.weekly || 0;
//            if (totalElem) totalElem.textContent = data.total || 0;
//        })
//        .catch(error => {
//            console.error('记录下载量失败:', error);
//        });
//    }
//
//    // 检查模态框是否存在
//    function modalExists() {
//        return document.querySelector('.quark-modal');
//    }
//
//    // 移除模态框
//    function removeExistingModal() {
//        const existingModal = document.querySelector('.quark-modal');
//        if (existingModal) document.body.removeChild(existingModal);
//    }
//
//    // 显示错误消息
//    function showError(message) {
//        // 先移除现有模态框
//        removeExistingModal();
//
//        const modal = document.createElement('div');
//        modal.className = 'quark-modal';
//        modal.style.cssText = `
//            position: fixed;
//            top: 0;
//            left: 0;
//            width: 100%;
//            height: 100%;
//            background: rgba(0,0,0,0.7);
//            display: flex;
//            justify-content: center;
//            align-items: center;
//            z-index: 1000;
//        `;
//
//        const errorContainer = document.createElement('div');
//        errorContainer.style.cssText = `
//            background: white;
//            padding: 25px;
//            border-radius: 15px;
//            text-align: center;
//            max-width: 90%;
//            width: 300px;
//            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
//        `;
//
//        const title = document.createElement('h3');
//        title.textContent = '下载出错';
//        title.style.margin = '0 0 20px 0';
//        title.style.color = '#d9534f';
//
//        const errorMsg = document.createElement('p');
//        errorMsg.textContent = message;
//        errorMsg.style.margin = '0 0 20px 0';
//        errorMsg.style.color = '#333';
//
//        const closeBtn = document.createElement('button');
//        closeBtn.textContent = '关闭';
//        closeBtn.style.cssText = `
//            margin-top: 10px;
//            padding: 10px 25px;
//            background: #f0f0f0;
//            border: none;
//            border-radius: 30px;
//            cursor: pointer;
//            font-size: 1rem;
//            transition: background 0.3s;
//        `;
//        closeBtn.onmouseover = () => closeBtn.style.background = '#e0e0e0';
//        closeBtn.onmouseout = () => closeBtn.style.background = '#f0f0f0';
//        closeBtn.onclick = () => removeExistingModal();
//
//        errorContainer.appendChild(title);
//        errorContainer.appendChild(errorMsg);
//        errorContainer.appendChild(closeBtn);
//        modal.appendChild(errorContainer);
//        document.body.appendChild(modal);
//
//        modal.onclick = (e) => {
//            if (e.target === modal) removeExistingModal();
//        };
//    }
//
//    // 获取夸克存储链接
//    function getQuarkStorageLink(quarkLink, articleId) {
//        return new Promise((resolve, reject) => {
//            const csrftoken = getCookie('csrftoken');
//            if (!csrftoken) {
//                reject('CSRF token not found');
//                return;
//            }
//
//
//            fetch('/quark/qurak_storage/', {  // 使用绝对路径
//                method: 'POST',
//                headers: {
//                    'Content-Type': 'application/json',
//
//                },
//                body: JSON.stringify({
//                    Quark_link: quarkLink,
//                    network_id: articleId
//                })
//            })
//            .then(response => {
//                if (!response.ok) throw new Error('网络请求失败');
//                return response.json();
//            })
//            .then(data => {
//                if (data.error) {
//                    reject(data.error);
//                } else if (data.link) {
//                    resolve(data.link);
//                } else if (data.message) {
//                    reject(data.message);
//                } else {
//                    reject('未知错误');
//                }
//            })
//            .catch(error => {
//                reject(error.message || '网络请求异常');
//            });
//        });
//    }
//
//    // 显示二维码
//    function showQRCode(url) {
//        removeExistingModal();
//
//        const modal = document.createElement('div');
//        modal.className = 'quark-modal';
//        modal.style.cssText = `
//            position: fixed;
//            top: 0;
//            left: 0;
//            width: 100%;
//            height: 100%;
//            background: rgba(0,0,0,0.7);
//            display: flex;
//            justify-content: center;
//            align-items: center;
//            z-index: 1000;
//        `;
//
//        const qrContainer = document.createElement('div');
//        qrContainer.style.cssText = `
//            background: white;
//            padding: 25px;
//            border-radius: 15px;
//            text-align: center;
//            max-width: 90%;
//            width: 300px;
//            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
//        `;
//
//        const title = document.createElement('h3');
//        title.textContent = '扫码下载';
//        title.style.margin = '0 0 20px 0';
//        title.style.color = '#333';
//        title.style.fontSize = '1.5rem';
//
//        const qrImg = document.createElement('img');
//        qrImg.src = `https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=${encodeURIComponent(url)}`;
//        qrImg.alt = '下载二维码';
//        qrImg.style.display = 'block';
//        qrImg.style.margin = '0 auto';
//        qrImg.style.width = '200px';
//        qrImg.style.height = '200px';
//        qrImg.style.border = '1px solid #eee';
//
//        // 二维码加载失败处理
//        qrImg.onerror = function() {
//            this.src = `https://api.pwmqr.com/qrcode/create/?url=${encodeURIComponent(url)}`;
//            this.onerror = function() {
//                this.src = `https://chart.googleapis.com/chart?cht=qr&chs=200x200&chl=${encodeURIComponent(url)}`;
//                this.onerror = function() {
//                    const errorText = document.createElement('p');
//                    errorText.textContent = '二维码生成失败，请手动访问链接';
//                    errorText.style.color = 'red';
//                    errorText.style.margin = '15px 0 0';
//                    qrContainer.insertBefore(errorText, this.nextSibling);
//                };
//            };
//        };
//
//        const hint = document.createElement('p');
//        hint.textContent = '使用夸克APP扫码下载';
//        hint.style.margin = '20px 0 0 0';
//        hint.style.fontSize = '1rem';
//        hint.style.color = '#666';
//
//        const directLink = document.createElement('a');
//        directLink.href = url;
//        directLink.textContent = '直接访问链接';
//        directLink.style.display = 'block';
//        directLink.style.marginTop = '15px';
//        directLink.style.color = '#007bff';
//        directLink.target = '_blank';
//
//        const closeBtn = document.createElement('button');
//        closeBtn.textContent = '关闭';
//        closeBtn.style.cssText = `
//            margin-top: 20px;
//            padding: 10px 25px;
//            background: #f0f0f0;
//            border: none;
//            border-radius: 30px;
//            cursor: pointer;
//            font-size: 1rem;
//            transition: background 0.3s;
//        `;
//        closeBtn.onmouseover = () => closeBtn.style.background = '#e0e0e0';
//        closeBtn.onmouseout = () => closeBtn.style.background = '#f0f0f0';
//        closeBtn.onclick = () => removeExistingModal();
//
//        qrContainer.appendChild(title);
//        qrContainer.appendChild(qrImg);
//        qrContainer.appendChild(hint);
//        qrContainer.appendChild(directLink);
//        qrContainer.appendChild(closeBtn);
//        modal.appendChild(qrContainer);
//        document.body.appendChild(modal);
//
//        modal.onclick = (e) => {
//            if (e.target === modal) removeExistingModal();
//        };
//    }
//
//    // 按钮点击事件处理
//    quarkBtn.addEventListener('click', async function() {
//        const btn = this;
//        const quarkLink = btn.dataset.downloadUrl;
//        // 假设文章ID存储在data-article-id属性中
//        const articleId = btn.dataset.articleId || '';
//        const originalHTML = btn.innerHTML;
//
//        if (!quarkLink) {
//            showError('下载链接未配置!');
//            return;
//        }
//
//        // 保存原始按钮状态
//        btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> 准备中...';
//        btn.disabled = true;
//
//        try {
//            // 获取夸克存储链接
//            const downloadUrl = await getQuarkStorageLink(quarkLink, articleId);
//
//            // 发送增量下载请求
//            incrementDownload(articleId);
//
//            // 根据设备类型处理
//            if (isMobileDevice()) {
//                // 手机端：直接跳转
//                window.location.href = downloadUrl;
//            } else {
//                // 电脑端：显示二维码
//                if (!modalExists()) {
//                    showQRCode(downloadUrl);
//                }
//            }
//        } catch (error) {
//            console.error('下载出错:');
//            showError('该链接已失效');
//            setTimeout(() => {
//                btn.innerHTML = '<i class="fas fa-cloud-download-alt"></i> 该链接已失效';
//                btn.disabled = false;
//            }, 1000);
//        } finally {
//            // 恢复按钮状态
//            setTimeout(() => {
//                btn.innerHTML = '<i class="fas fa-cloud-download-alt"></i> 夸克资源下载';
//                btn.disabled = false;
//            }, 1000);
//        }
//    });
//
//    // 添加键盘事件支持
//    quarkBtn.addEventListener('keydown', function(e) {
//        if (e.key === 'Enter' || e.key === ' ') {
//            e.preventDefault();
//            this.click();
//        }
//    });
//}

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', function() {
    setupQuarkDownload();
});

// 如果使用Turbolinks或类似技术
if (typeof Turbolinks !== 'undefined' && Turbolinks.supported) {
    document.addEventListener('turbolinks:load', function() {
        setupQuarkDownload();
    });
}

// 页面加载完成后初始化夸克下载功能
document.addEventListener('DOMContentLoaded', function() {
    setupQuarkDownload();
});

// 标签点击功能
function setupTagClicks() {
    document.querySelectorAll('.resource-tag').forEach(tag => {
        tag.addEventListener('click', function() {
            // 在实际应用中，这里会跳转到标签搜索页
            const tagText = this.textContent;
            alert('将搜索标签: ' + tagText);
        });
    });
}

// 在DOM加载完成后初始化
document.addEventListener('DOMContentLoaded', function() {
    // ...原有代码...
    setupQuarkDownload();
    setupTagClicks();
});