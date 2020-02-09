import React, { FC, useState, useCallback } from 'react';
import { Menu, Button } from 'antd';
const { SubMenu } = Menu;
import { DashboardOutlined } from '@ant-design/icons';
import style from "@/stylesheets/app-container.module.css"
import CollapseBtn from "@/components/ui/CollapseBtn";
import { BrowserRouter as Router, Switch, Route, Link } from "react-router-dom";
import Spiders from './Spiders';

const AppContainerMenu = () => {
    const [collapse, setCollapse] = useState(false);
    return (
        <div className={style['spider-menu']}>
            <Menu className={style.menu} style={{ width: collapse ? 64 : 150 }} defaultSelectedKeys={['1']} defaultOpenKeys={['sub1']} mode="inline" theme="dark" inlineCollapsed={collapse}>
                <SubMenu key="sub1" icon={<DashboardOutlined />} title="仪表盘">
                    <Menu.Item key="8">
                        <Link to="/spiders">爬虫管理</Link>
                    </Menu.Item>
                </SubMenu>

                <CollapseBtn className={style['collapse-btn']} openCollapse={() => { setCollapse(false) }} closeCollapse={() => { setCollapse(true) }} />
            </Menu>
        </div>
    )
}

const SpiderManagement = () => {
    return (
        <div className={style['app-container']}>
            <AppContainerMenu></AppContainerMenu>
            <div>
                <Switch>
                    <Route exact path="/spiders">
                        <Spiders></Spiders>
                    </Route>
                </Switch>
            </div>
        </div>
    )
}

export default SpiderManagement;
