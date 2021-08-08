import { Tooltip } from '@ui';
import styleGet from '@ui/style';
import { CaretRightOutlined } from '@ant-design/icons';
import {FC, useState} from 'react';
import styled from 'styled-components';
import { SpiderData } from '../../types.d';
import RunnerModal from './Modal';

const StyledButton = styled.button`
    padding: 3px;
    background: ${ styleGet("color.bg.btnBlue") };
    border: 0;
    border-radius: 2px;
    color: ${ styleGet("color.text.defaultWhite") };
    cursor: pointer;
    :hover {
        background: ${ styleGet("color.bg.btnBlueHover") };
    }
`

interface RunBottonProps {
    setVisible: (visible: boolean) => void
}

const RunBotton: FC<RunBottonProps> = props => {
    return <Tooltip placement="bottom" title="运行">
        <StyledButton onClick={() => props.setVisible(true) }>
            <CaretRightOutlined />
        </StyledButton>
    </Tooltip>
}

interface RunProps {
    spider: SpiderData
}
const Run: FC<RunProps> = props => {
    const [visible, setVisible] = useState(false);
    return <>
        <RunBotton setVisible={ setVisible }></RunBotton>
        <RunnerModal isVisible={ visible } hide={() => setVisible(false)} spider={ props.spider }/>
    </>
}

export { RunProps }
export default Run;