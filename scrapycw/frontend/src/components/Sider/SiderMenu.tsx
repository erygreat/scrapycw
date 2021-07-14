import { Menu } from "@ui"
import routers from '@/router';
import styled from "styled-components";
import { Link } from "react-router-dom";
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
                return router.children 
                    ? <SubMenu key={ router.key } icon={ router.icon } title={ router.title }>
                        { 
                            router.children.map(subRouter => {
                                return <StyledMenuItem key={ subRouter.key } icon={ subRouter.icon }>
                                    <Link to={ subRouter.link }>{ subRouter.title }</Link>
                                </StyledMenuItem>
                            })
                        }
                    </SubMenu>
                    : <StyledMenuItem key={ router.key } icon={ router.icon }>
                        <Link to={ router.link }>{ router.title }</Link>
                    </StyledMenuItem>
            })
        }
    </Menu>
}

export default SiderMenu;