import { DashboardOutlined } from "@ant-design/icons";
import { Link } from "react-router-dom";

interface SubRouter {
    key: string,
    content: JSX.Element | string
}

interface Router {
    key: string,
    title: string,
    icon: JSX.Element,
    children: Array<SubRouter>
}

const router: Array<Router> = [
    {
        key: "dashboard",
        title: "仪表盘",
        icon: <DashboardOutlined />,
        children: [{
            key: "",
            content: "你好啊!"
            // content: <Link to="/spiders">爬虫管理</Link>
//                         <Link to="/jobs">任务管理</Link>
        }]
    },
    {
        key: "dashboard2",
        title: "仪表盘",
        icon: <DashboardOutlined />,
        children: [{
            key: "1",
            content: "你好啊!"
            // content: <Link to="/spiders">爬虫管理</Link>
//                         <Link to="/jobs">任务管理</Link>
        },
        {
            key: "2",
            content: "你好22啊!"
            // content: <Link to="/spiders">爬虫管理</Link>
//                         <Link to="/jobs">任务管理</Link>
        }]
    }
]
export default router