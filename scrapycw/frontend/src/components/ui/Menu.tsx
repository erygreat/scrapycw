import { Menu, MenuProps as AntdMenuProps } from "antd"
import styled, { css } from "styled-components"

interface MenuProps extends AntdMenuProps {
    $subMenuActiveBgColor?: string
    $subMenuActiveColor?: string
    $subMenuActiveBorderColor?: string
}

export default styled(Menu)<MenuProps>`
    .ant-menu-submenu-arrow {
        color: inherit;
    }
    && .ant-menu-item {
        margin: 0;
        width: 100%;
    }
    .ant-menu:not(.ant-menu-horizontal) .ant-menu-item-selected {
        ${ props => props.$subMenuActiveBgColor && css`background-color: ${ props.$subMenuActiveBgColor }` };
        ${ props => props.$subMenuActiveColor && css`color: ${ props.$subMenuActiveColor }` };
        
    }
    .ant-menu-item::after {
        ${ props => props.$subMenuActiveBorderColor && css`border-right: 3px solid ${ props.$subMenuActiveBorderColor }` };
    }
`