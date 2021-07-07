import {createRouter, createWebHistory} from 'vue-router'

const home_page = () => import("../views/home_page.vue")
const login = () => import("../views/login.vue")
const creat_box = () => import("../views/creat_box.vue")
const box_list = () => import("../components/box_list.vue")
const steam_simulation = () => import("../components/steam_simulation.vue")
const hot_water_simulation = () => import("../components/hot_water_simulation.vue")



// import HelloWorld from '../components/creat_box.vue'

const routerHistory = createWebHistory()


const router = createRouter({
    history: routerHistory,
    routes: [
        {
            path: '/',
            component: login,
            name:'login'
        },
        {
            path: '/home_page',
            component: home_page,
            name : 'home_page',
            children: [
                {
                    path: "creat_box",
                    component: creat_box
                },
                {
                    name:'box_list',
                    path: "box_list",
                    component: box_list,
                },
                {
                    name:'steam_simulation',
                    path: "/home_page/box_list",
                    component: steam_simulation
                },
                {
                    name:'hot_water_simulation',
                    path: "/home_page/box_list",
                    component: hot_water_simulation
                }

            ]
        }
    ]
})

export default router
