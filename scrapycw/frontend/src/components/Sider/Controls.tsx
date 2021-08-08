import styled from "styled-components";
import { CollapseBtn, CollapseBtnProps } from "@ui"

const StyldControls = styled.div`
    padding: 10px 0;
    text-align: center;
`

const Controls: React.FC<CollapseBtnProps & React.HTMLAttributes<HTMLDivElement>> = props => {
    return <StyldControls className={ props.className } style={ props.style }>
        <CollapseBtn openCollapse={ props.openCollapse } closeCollapse={ props.closeCollapse } /> 
    </StyldControls>
}

export default Controls;