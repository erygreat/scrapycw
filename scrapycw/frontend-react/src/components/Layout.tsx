import React, {FC} from 'react';
import { Layout, Menu } from 'antd';
import { QuestionCircleOutlined } from '@ant-design/icons';
import * as headerStyles from '@/stylesheets/layout/header.module.css';
import { Link } from "react-router-dom";

const LayoutHeader: FC = () => (
    <Layout.Header className="header">
      <div className="logo" />
      <div className="float-left">
        <Menu theme="dark" mode="horizontal" defaultSelectedKeys={['2']}>
            <Menu.Item key="1">爬虫管理</Menu.Item>
        </Menu>
      </div>
      <div className="float-right position-relative">
        <div className={"middle-center " + headerStyles['menu-btn']}>
          <Link to="/help">
            <QuestionCircleOutlined />
          </Link>
        </div>
      </div>
    </Layout.Header>
);

export { LayoutHeader };