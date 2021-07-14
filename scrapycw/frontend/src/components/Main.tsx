import React, { Children } from 'react';
import styled from 'styled-components';
import Sider from './Sider/Sider';
import { Route, Switch } from "react-router-dom";
import router from '@/router';

const StyledContent = styled.div`
    flex: auto;
`

const Content = () => {
    return <StyledContent>
        <Switch>
            { 
                router.map(item => {
                    return item.children 
                        ? item.children.map(childItem => <Route key={ childItem.key } exact path={ childItem.link }>{ childItem.view }</Route>)
                        : <Route key={ item.key } exact path={ item.link }>{ item.view }</Route>
                })
            }
        </Switch>
    </StyledContent>
}

const StyledMain = styled.div`
    display: flex;
`

const Main: React.FC<React.HTMLAttributes<HTMLDivElement>> = (props) => {
    return <StyledMain className={ `${ props.className }` }>
        <Sider />
        <Content />
    </StyledMain>
}

export default Main;