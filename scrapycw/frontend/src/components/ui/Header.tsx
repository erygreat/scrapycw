import React from 'react';
import styled, { css } from 'styled-components'
import UIException from './exception';
import styleGet from './style';

interface HeaderProps {
    height?: number
    fixed?: boolean
    children?: React.ReactNode
}

interface HeaderItemProps {
    full?: boolean
}

const HeaderPlaceholder = styled.div<HeaderProps>`
    height: ${ props => (props.height || styleGet("size.height.header")) + "px" };
    line-height: ${ props => (props.height || styleGet("size.height.header")) + "px" };
    width: 100%;
`

const HeaderWrapper = styled.header<HeaderProps>`
    display: flex;
    height: ${ props => (props.height || styleGet("size.height.header")) + "px" };
    line-height: ${ props => (props.height || styleGet("size.height.header")) + "px" };
    color: ${ styleGet("color.text.header") };
    background: ${ styleGet("color.bg.header") };
    ${ props => props.fixed && css`position: fixed`};
    width: 100%;
    align-items: stretch;
    flex-wrap: nowrap;
`

const HeaderFixed = (props: HeaderProps) => {
    return <>
        <HeaderWrapper {...props} />
        <HeaderPlaceholder height={props.height}/>
    </>
}

const Header = (props: HeaderProps) => {
    React.Children.forEach<React.ReactNode>(props.children, item => {
        if(!React.isValidElement(item) || (item as React.ReactElement).type !== Item) {
            throw new UIException("Header 组件子组件只允许使用 Header.Item 组件")
        }
    })
    return props.fixed 
        ? <HeaderFixed {...props} />
        : <HeaderWrapper {...props} />
}

const Item = styled.div<HeaderItemProps>`
    display: flex;
    align-items: center;
    flex-wrap: nowrap;
    padding: 0 10px;
    ${ props => props.full && css`flex: auto` }
`

Item.displayName = "Header.Item"
Header.Item = Item

export default Header;