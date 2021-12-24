import request from "../utils/request"
import { ElMessage } from 'element-plus'
export function simulation(data) {
    request({
        url: '/uploadData',
        method: 'post',
        data: data
    })
    ElMessage.success('上报成功')
    return request
}
export function get_box(data) {
    return request({
        url: '/getBoxes',
        method: 'post',
        data: data
    })
}

export function submit_createBox(data) {
    return request({
        url: '/createBox',
        method: 'post',
        data: data
    })
}

export function simulation_stopBox(data) {
    return request({
        url: '/stopBox',
        method: 'post',
        data: data
    })
}

export function get_simulationlist(data) {
    return request({
        url: '/getBoxes',
        method: 'post',
        data: data
    })
}
export function getProtocolList(data) {
    return request({
        url: '/getProtocolList',
        method: 'get',
        data: data
    })
}
export function stop_continuous(data) {
    return  request({
        url: '/stopContinue',
        method: 'post',
        data: data
    })
}

export function start_continuous(data) {
    return  request({
        url: '/uploadData',
        method: 'post',
        data: data
    })

}

export function do_login(data) {
    return  request({
        url: '/login',
        method: 'post',
        data: data
    })

}
