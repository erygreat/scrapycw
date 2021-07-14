import React from 'react';
import style from "./Main.module.css"
import Sider from './Sider/Sider';

const Content = () => {
    return <div></div>
}

const Main: React.FC<React.HTMLAttributes<HTMLDivElement>> = (props) => {
    return <div className={ `${ props.className } ${ style.main }` }>
        <Sider />
        <Content />
    </div>
}

export default Main;