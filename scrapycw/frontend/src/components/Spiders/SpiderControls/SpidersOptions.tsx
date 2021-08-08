import { Tooltip } from "@ui";
import styleGet from "@ui/style";
import { SyncOutlined } from "@ant-design/icons";
import { FC } from "react";
import styled from "styled-components";

const StyledOptionsIcon = styled.div`
    padding: 5px;
    cursor: pointer;
    :hover {
        background: ${ styleGet("color.bg.btn") };
    }
`

interface ReloadProps {
    loading: boolean
    onReload: () => void;
}

const Reload: FC<ReloadProps> = props => {
    return <StyledOptionsIcon>
        <Tooltip placement="bottom" title="刷新">
            <SyncOutlined spin={ props.loading } onClick={ props.onReload }/>
        </Tooltip>
    </StyledOptionsIcon>
}

type SpidersOptionsProps = ReloadProps

const SpidersOptions: FC<SpidersOptionsProps> = props => {
    return <Reload {...props}></Reload>
}

export { SpidersOptionsProps };
export default SpidersOptions;