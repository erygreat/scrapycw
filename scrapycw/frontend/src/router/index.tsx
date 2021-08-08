// import Dashboard from "@/components/Dashboard";
import Spiders from "@/components/Spiders";
import { XOR } from "@/types";
import { BugOutlined, DashboardOutlined } from "@ant-design/icons";

interface SubRouter {
    key: string,
    title: JSX.Element | string,
    link: string,
    view: JSX.Element | string,
    icon?: JSX.Element,
}

interface BaseRouter {
    key: string,
    title: string,
    icon?: JSX.Element,
}
interface RouterChildren extends BaseRouter {
    children: Array<SubRouter>,
}

interface RouterLink extends BaseRouter {
    link: string,
    view: JSX.Element | string,
}

const router: Array<XOR<RouterLink, RouterChildren>> = [
    // {
    //     key: "dashboard",
    //     title: "仪表盘",
    //     icon: <DashboardOutlined />,
    //     link: "/dashboard",
    //     view: <Dashboard />,
    // },
    {
        key: "spiders",
        title: "爬虫管理",
        icon: <BugOutlined />,
        link: "/spiders",
        view: <Spiders />
    }
]

export default router