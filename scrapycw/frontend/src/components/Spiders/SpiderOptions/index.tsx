import { FC } from 'react';
import RunButton, { RunProps } from "./Run"

type OptionsProps = RunProps;

const Options: FC<OptionsProps> = props => {
    return <div>
        <RunButton { ...props }></RunButton>
    </div>
}
export default Options;