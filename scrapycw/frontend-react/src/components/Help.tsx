import React, {FC, useState, useCallback} from 'react';
import ReactMarkdown from 'react-markdown';
import { Menu } from 'antd';
const { SubMenu } = Menu;
import { MailOutlined, CalendarOutlined, AppstoreOutlined, SettingOutlined, LinkOutlined } from '@ant-design/icons';
import * as helpStyles from "@/stylesheets/help.module.css";
import CollapseBtn from "@ui/CollapseBtn"

const HelpMenu: FC = () => (
    <Menu mode="inline" defaultSelectedKeys={['1']}>
        <Menu.Item key="1">目录</Menu.Item>
    </Menu>
);

var input = "#11";
const Help: FC = () => {
    const [menuClassName, setMenuClassName] = useState(helpStyles['menu']);
    const openCollapse = () => {
        setMenuClassName(helpStyles['menu']);
    }
    const closeCollapse = () => {
        setMenuClassName(helpStyles['menu'] + " " + helpStyles['hide']);
    }
    return (
        <div className={ helpStyles['help-content']}>
            <div className={ menuClassName }>
                <HelpMenu />
            </div>
            <div>
                <ReactMarkdown source={input} />
            </div>
            <div className={helpStyles['controls']}>
                <CollapseBtn openCollapse={openCollapse} closeCollapse={closeCollapse}/> 
            </div>
        </div>
    )
}

export default Help;