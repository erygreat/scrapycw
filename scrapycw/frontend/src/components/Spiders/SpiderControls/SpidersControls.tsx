import { FC } from "react";
import styled from "styled-components";
import SpidersOptions, { SpidersOptionsProps } from "./SpidersOptions";
import SpidersFilterName, { SpidersFilterNameProps } from "./SpidersFilterName";
import SpidersFilterProject, { SpidersFilterProjectProps } from "./SpidersFilterProject";

const StyledSpidersControls = styled.div`
    display: flex;
    padding: 10px 0;
    align-items: center;
`

type SpidersControlsProps = SpidersFilterProjectProps & SpidersFilterNameProps & SpidersOptionsProps;

const StyledSpace = styled.div`
    flex: auto;
`

const SpidersControls: FC<SpidersControlsProps> = props => {
    return <StyledSpidersControls>
        <SpidersFilterName {...props} />
        <SpidersFilterProject {...props}/>
        <StyledSpace />
        <div>
            <SpidersOptions {...props}></SpidersOptions>
        </div>
    </StyledSpidersControls>
}

export default SpidersControls;