import React, { FC } from 'react';
import style from './index.module.css';
import { Layout } from 'antd';

const Header: FC = () => (
    <Layout.Header className={ style.header }>
        <div className="logo" />
        <div className="float-left">

        </div>
        <div className="float-right position-relative">
            <div className={"middle-center " + style['menu-btn']}>
            </div>
        </div>
    </Layout.Header>
);

export default Header;