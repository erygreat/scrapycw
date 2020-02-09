import React, {FC} from 'react';
import * as headerStyles from '@/stylesheets/layout/header.module.css';
import { Link } from "react-router-dom";
import { Layout, Menu } from 'antd';

const LayoutHeader: FC = () => (
    <Layout.Header className="header">
      <div className="logo" />
      <div className="float-left">
        
      </div>
      <div className="float-right position-relative">
        <div className={"middle-center " + headerStyles['menu-btn']}>
        </div>
      </div>
    </Layout.Header>
);

export { LayoutHeader };