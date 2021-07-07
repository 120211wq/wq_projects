import axios from 'axios'  //引入axios
import { ElMessage } from 'element-plus'

let apiUrl = "/api"
if (process.env.NODE_ENV === "development") { //开发环境
    console.log("当前环境：测试环境环境");
    apiUrl = "http://127.0.0.1:5200"
} else if (process.env.NODE_ENV === "production") {
    console.log("当前环境：生产环境");
    apiUrl = "http://192.168.0.26:5100"  //接口地址
}
//**其他环境可以自己再根据情况增加

// 创建并配置axios实例
const service = axios.create({
    baseURL: apiUrl ,  //请求的url
    method: 'get',  //默认请求方式

    //   timeout: 10000, // 请求超时时间
})



//添加请求拦截器
service.interceptors.request.use(
    config => {
        // 发送请求之前
        // 为头部增加token
        config.headers['token'] = localStorage.getItem('token') || ""
        // 为头部增加accId
        // config.headers['accId'] = localStorage.getItem("accid") || ""

        return config
    }
)

// 添加响应拦截器

export function push() {
    window.location.href = '/'
}
service.interceptors.response.use(response => {
    //接收到响应数据并成功后的一些共有的处理，关闭loading等
    // ElMessage.success(response.data.state.toString())
    return response

}, error => {
    /***** 接收到异常响应的处理开始 *****/
    if (error && error.response) {
        // 1.公共错误处理
        // 2.根据响应码具体处理
        switch (error.response.status) {
            case 400:
                error.message = error.response.data.state.toString()
                break;
            case 401:
                error.message = '未授权，请重新登录'
                break;
            case 403:
                error.message = '拒绝访问'
                break;
            case 404:
                error.message = '请求错误,未找到该资源'
                window.location.href = "/NotFound"
                break;
            case 405:
                error.message = '请求方法未允许'
                break;
            case 408:
                error.message = '请求超时'
                break;
            case 500:
                error.message = '服务器端出错'
                break;
            case 501:
                error.message = '网络未实现'
                break;
            case 502:
                error.message = 'token验证失败'
                setTimeout(push,2000);
                break;
            case 503:
                error.message = '服务不可用'
                break;
            case 504:
                error.message = '网络超时'
                break;
            case 505:
                error.message = 'http版本不支持该请求'
                break;
            default:
                error.message = `连接错误${error.response.status}`
        }
    } else {
        // 超时处理
        if (JSON.stringify(error).includes('timeout')) {
            ElMessage.error('服务器响应超时，请刷新当前页')
        }
        error.message('连接服务器失败')
    }

    ElMessage.error(error.message)
    /***** 处理结束 *****/
    //如果不需要错误处理，以上的处理过程都可省略
    return Promise.resolve(error.response)
})
//4.导入文件
export default service

