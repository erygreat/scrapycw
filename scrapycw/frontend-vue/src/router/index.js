import Vue from 'vue'
import VueRouter from 'vue-router'
import Help from '@/views/Help'
const Dashboard = () =>
    import ("@/views/Dashboard");
const Spiders = () =>
    import ("@/views/Spiders")
const Jobs = () =>
    import ("@/views/Jobs")

Vue.use(VueRouter)

const routes = [{
    path: '/help',
    name: 'Help',
    component: Help
}, {
    path: '/dashboard',
    name: 'Dashboard',
    component: Dashboard,
    children: [
        { path: '', component: Spiders },
        {
            path: 'spiders',
            component: Spiders
        },
        {
            path: 'jobs',
            component: Jobs
        },
    ]
}]

const router = new VueRouter({
    mode: 'history',
    base: process.env.BASE_URL,
    routes
})

// router.beforeEach((to, from, next) => {
//     console.log(from)
//     console.log(to)
//     next()
//     next(): 进行管道中的下一个钩子。如果全部钩子执行完了，则导航的状态就是 confirmed (确认的)。
//     next(false): 中断当前的导航。如果浏览器的 URL 改变了 (可能是用户手动或者浏览器后退按钮)，那么 URL 地址会重置到 from 路由对应的地址。
//     next('/') 或者 next({ path: '/' }): 跳转到一个不同的地址。当前的导航被中断，然后进行一个新的导航。你可以向 next 传递任意位置对象，且允许设置诸如 replace: true、name: 'home' 之类的选项以及任何用在 router-link 的 to prop 或 router.push 中的选项。
//     next(error): (2.4.0+) 如果传入 next 的参数是一个 Error 实例，则导航会被终止且该错误会被传递给 router.onError() 注册过的回调。
// 确保 next 函数在任何给定的导航守卫中都被严格调用一次。它可以出现多于一次，但是只能在所有的逻辑路径都不重叠的情况下，否则钩子永远都不会被解析或报错。
// });

export default router