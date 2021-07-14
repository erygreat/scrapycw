import { Menu } from "@ui"
import routers from '@/router';
import styled from "styled-components";
const { SubMenu } = Menu;
const MenuItem = Menu.Item;

export interface SiderMenuProps {
    collapse: boolean
    width?: number
    subMenuClassName?: string
    subMenuActiveBgColor?: string
    subMenuActiveColor?: string
    subMenuActiveBorderColor?: string
}

export const StyledMenuItem = styled(MenuItem)``

const SiderMenu: React.FC<React.HTMLAttributes<HTMLDivElement> & SiderMenuProps> = props => {
    return <Menu 
            $subMenuActiveBgColor={ props.subMenuActiveBgColor }
            $subMenuActiveColor={ props.subMenuActiveColor }
            $subMenuActiveBorderColor={ props.subMenuActiveBorderColor }
            className={ props.className }
            mode="inline"
            inlineCollapsed={ props.collapse }
        >
        {
            routers.map(router => {
                return <SubMenu key={ router.key } icon={ router.icon } title={ router.title }>
                    { router.children.map(subRouter => {
                        return <StyledMenuItem key={ subRouter.key }> { subRouter.content }</StyledMenuItem>
                    }) }
                </SubMenu>
            })
        }
    </Menu>
}

export default SiderMenu;