import styled from "styled-components";
import { CollapseBtn, CollapseBtnProps } from "@ui/CollapseBtn"

const StyldControls = styled.div`
    padding: 10px 0;
    text-align: center;
`

const Controls: React.FC<CollapseBtnProps & React.HTMLAttributes<HTMLDivElement>> = props => {
    return <StyldControls className={ props.className } >
        <CollapseBtn openCollapse={ props.openCollapse } closeCollapse={ props.closeCollapse } /> 
    </StyldControls>
}

export default Controls;