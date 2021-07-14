import { useState } from "react";
import styled from "styled-components";
import styleGet from "@ui/style";
import Controls from "./Controls"
import SiderMenu, { StyledMenuItem } from "./SiderMenu";

const ControlsWrapper = styled(Controls)`
    width: ${ styleGet("size.width.sider.shrink") };
    color: ${ styleGet("color.text.sider") };
`

const SiderMenuWrapper = styled(SiderMenu)`
    flex: auto;
    && {
        width: ${ props => props.collapse ? styleGet("size.width.sider.shrink") : styleGet("size.width.sider.expand") }px;
        background: ${ styleGet("color.bg.sider")};
        color: ${ styleGet("color.text.sider") };
    }
    ${ StyledMenuItem } {
        background: ${ styleGet("color.bg.menuItem")};
        color: ${ styleGet("color.text.sider") };
    }
`

const StyledSider = styled.div`
    display: flex;
    flex-direction: column;
    border-right: 1px solid ${ styleGet("color.border.sider") };
    background: ${ styleGet("color.bg.sider")};
`

const Sider = () => {
    const [collapse, setCollapse] = useState(false);
    return <StyledSider>
        <SiderMenuWrapper
            collapse={ collapse }
            subMenuActiveBgColor={ styleGet("color.bg.menuItemActive") }
            subMenuActiveColor={ styleGet("color.text.menuItemActive") }
            subMenuActiveBorderColor={ styleGet("color.border.menuItemActive") }/>
        <ControlsWrapper openCollapse={() => { setCollapse(false) }} closeCollapse={() => { setCollapse(true) }} />
    </StyledSider>
}

export default Sider